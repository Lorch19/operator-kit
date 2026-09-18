"""
The failing test that reproduces the bug, written before any fix exists.

Run:  python3 -m pytest test_no_silent_drops.py -v
"""

import pytest

import ledger
import pipeline


# --------------------------------------------------------------------------
# TEST 1 -- the conservation invariant
#
# The break it catches: any stage that discards a ticker without recording it.
# The production change that makes this fail: any silent filter, inner join,
# swallowed exception, dedupe collision, or dropped future anywhere in the run.
#
# Expected value is derived by hand: the universe list itself. It is NOT
# computed by the pipeline, so this cannot become a mirror assertion.
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bug",
    ["innerjoin", "swallow", "race", "dedupe", "nan"],
    ids=["inner-join", "swallowed-exception", "concurrency", "dedupe-collision", "dropna"],
)
def test_every_universe_ticker_reaches_persisted_output(bug):
    universe = pipeline.build_universe()
    metadata = pipeline.build_metadata(universe)

    persisted = pipeline.run_nightly(universe, metadata, bugs=frozenset({bug}))

    missing = sorted(set(universe) - {row["symbol"] for row in persisted})
    assert missing == [], (
        f"{len(missing)} of {len(universe)} tickers "
        f"({len(missing) / len(universe):.2%}) never reached persisted output "
        f"and the run exited 0: {missing[:10]}"
    )


# --------------------------------------------------------------------------
# TEST 2 -- attribution
#
# Test 1 tells you a ticker is gone. It does not tell you WHERE it went, which
# is exactly the position you are in today. This test demands the run name the
# boundary that lost each ticker.
#
# The break it catches: a stage that changes row count without accounting for
# the delta. Delete the accounting from any single stage and this goes red and
# names that stage.
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bug,expected_stage",
    [
        ("innerjoin", "enrich"),
        ("swallow", "fetch"),
        ("dedupe", "normalize"),
        ("nan", "normalize"),
    ],
)
def test_ledger_attributes_each_lost_ticker_to_the_stage_that_lost_it(bug, expected_stage):
    universe = pipeline.build_universe()
    metadata = pipeline.build_metadata(universe)

    report = ledger.run_nightly_with_ledger(
        universe, metadata, bugs=frozenset({bug}), fail_fast=False
    )

    assert report.unaccounted_losses, "expected this bug to lose tickers"
    stages = {loss.stage for loss in report.unaccounted_losses}
    assert stages == {expected_stage}, (
        f"losses attributed to {sorted(stages)}, expected only {expected_stage!r}"
    )


# --------------------------------------------------------------------------
# TEST 3 -- the gate
#
# The break it catches: removing the raise, so a lossy run exits 0 again.
# This is the single assertion that turns "silent drop" into "loud failure",
# and it is the one line whose deletion must never pass CI.
# --------------------------------------------------------------------------


def test_run_raises_instead_of_exiting_zero_when_a_ticker_is_lost():
    universe = pipeline.build_universe()
    metadata = pipeline.build_metadata(universe)

    with pytest.raises(ledger.TickersLost) as exc:
        ledger.run_nightly_with_ledger(
            universe, metadata, bugs=frozenset({"innerjoin"}), fail_fast=True
        )

    assert "enrich" in str(exc.value)


# --------------------------------------------------------------------------
# TEST 4 -- declared exclusions are not losses
#
# A pipeline that fails on every missing ticker is unusable: some tickers are
# legitimately excluded (halted, delisted, no trade that session). Those must
# be RECORDED with a reason, not silently filtered -- otherwise "expected"
# drops become the hiding place for unexpected ones.
#
# The break it catches: an exclusion path that returns nothing, so a real drop
# can be mistaken for a declared one.
# --------------------------------------------------------------------------


def test_declared_exclusions_carry_a_reason_and_do_not_trip_the_gate():
    universe = ["AAA", "BBB", "CCC"]
    metadata = {s: {"sector": "Tech"} for s in universe}

    report = ledger.run_nightly_with_ledger(
        universe, metadata, bugs=frozenset(), halted={"BBB": "trading halt"}
    )

    assert report.unaccounted_losses == []
    assert report.declared_exclusions == [("BBB", "normalize", "trading halt")]
    assert {r["symbol"] for r in report.persisted} == {"AAA", "CCC"}


# --------------------------------------------------------------------------
# TEST 5 -- the ledger must not itself be racy
#
# The break it catches: accounting that uses a non-atomic counter and
# undercounts under concurrency -- which would make the instrument lie in
# exactly the scenario it was built to diagnose.
# --------------------------------------------------------------------------


def test_ledger_accounts_correctly_under_the_concurrent_stage():
    universe = pipeline.build_universe()
    metadata = pipeline.build_metadata(universe)

    report = ledger.run_nightly_with_ledger(
        universe, metadata, bugs=frozenset({"race"}), fail_fast=False
    )

    lost = {loss.symbol for loss in report.unaccounted_losses}
    actually_missing = set(universe) - {r["symbol"] for r in report.persisted}
    assert lost == actually_missing
    assert all(loss.stage == "fetch" for loss in report.unaccounted_losses)
