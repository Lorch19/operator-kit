"""Regression tests for: the nightly pipeline drops ~1 ticker in 50.

Seam under test: run_nightly(universe) -> {"rows", "failures"}.

This is the correct seam. A unit test on fetch() cannot catch this bug: fetch()
raises correctly. The defect lives in the aggregation boundary, so the test must
observe that boundary. Expected values come from the input universe (an independent
source of truth), never recomputed the way the pipeline computes them.

Run against either implementation:
    IMPL=pipeline_legacy python3 -m pytest test_no_silent_drops.py -q   # RED
    IMPL=pipeline_fixed  python3 -m pytest test_no_silent_drops.py -q   # GREEN
"""
import importlib
import os
import random

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "pipeline_fixed"))

UNIVERSE = [f"T{i:03d}" for i in range(500)]


def accounted_for(result):
    return {r["ticker"] for r in result["rows"]} | {f["ticker"] for f in result["failures"]}


def test_every_ticker_is_either_a_row_or_a_named_failure():
    """The conservation invariant. No ticker may vanish without a reason."""
    random.seed(7)
    result = impl.run_nightly(UNIVERSE)
    missing = [t for t in UNIVERSE if t not in accounted_for(result)]
    assert missing == [], f"{len(missing)} ticker(s) vanished with no failure record: {missing[:10]}"


def test_a_vendor_error_surfaces_as_a_failure_not_a_missing_row(monkeypatch):
    """The minimised repro: exactly one ticker errors. It must be reported, not swallowed."""
    def one_bad_apple(ticker):
        if ticker == "T042":
            raise TimeoutError("vendor read timed out for T042")
        return {"ticker": ticker, "close": 100.0}

    monkeypatch.setattr(impl, "fetch", one_bad_apple)
    result = impl.run_nightly(UNIVERSE)

    assert "T042" not in {r["ticker"] for r in result["rows"]}
    assert "T042" in {f["ticker"] for f in result["failures"]}, \
        "T042 failed and was silently dropped instead of reported"
    assert len(result["rows"]) == 499


def test_a_clean_run_produces_the_whole_universe_and_no_failures():
    """Control: the test can go green, so a pass means something."""
    def always_ok(ticker):
        return {"ticker": ticker, "close": 100.0}

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(impl, "fetch", always_ok)
        result = impl.run_nightly(UNIVERSE)

    assert [r["ticker"] for r in sorted(result["rows"], key=lambda r: r["ticker"])] == UNIVERSE
    assert result["failures"] == []
