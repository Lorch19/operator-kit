"""
The reconciliation ledger: the instrument that turns a silent drop into a
named, attributed, loud failure.

THIS IS THE PART YOU PORT INTO YOUR PIPELINE. `Ledger` has no dependency on
the stand-in pipeline -- it only needs the set of symbols entering and leaving
each stage.

The idea in one sentence: every stage must account for its own row-count
delta. A stage may shed tickers, but only ones it *declares*, with a reason.
Anything else is an unaccounted loss and stops the run.

Porting it is four lines per stage boundary:

    before = {r.symbol for r in rows}
    rows = my_stage(rows)
    after = {r.symbol for r in rows}
    led.checkpoint("my_stage", before, after, declared=my_stage_exclusions)
"""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field

import pipeline


class TickersLost(Exception):
    """Raised when a stage loses tickers it did not declare."""


@dataclass(frozen=True)
class StageLoss:
    symbol: str
    stage: str


@dataclass
class LedgerReport:
    run_id: str
    universe_size: int
    stage_counts: list[tuple[str, int, int]] = field(default_factory=list)
    unaccounted_losses: list[StageLoss] = field(default_factory=list)
    declared_exclusions: list[tuple[str, str, str]] = field(default_factory=list)
    persisted: list[dict] = field(default_factory=list)

    @property
    def loss_rate(self) -> float:
        return len(self.unaccounted_losses) / max(self.universe_size, 1)

    def to_jsonl(self) -> str:
        """One line per event -- append this to your nightly log so the next
        two weeks of runs produce a dataset instead of an anecdote."""
        lines = []
        for stage, n_in, n_out in self.stage_counts:
            lines.append(json.dumps(
                {"run": self.run_id, "event": "stage", "stage": stage,
                 "in": n_in, "out": n_out, "delta": n_out - n_in}))
        for loss in self.unaccounted_losses:
            lines.append(json.dumps(
                {"run": self.run_id, "event": "unaccounted_loss",
                 "symbol": loss.symbol, "stage": loss.stage}))
        for sym, stage, reason in self.declared_exclusions:
            lines.append(json.dumps(
                {"run": self.run_id, "event": "declared_exclusion",
                 "symbol": sym, "stage": stage, "reason": reason}))
        return "\n".join(lines)


class Ledger:
    """Accountant for a multi-stage run. Thread-safe: stages may be concurrent,
    and an instrument that undercounts under concurrency is worse than none."""

    def __init__(self, run_id: str, universe: list[str], fail_fast: bool = True):
        self.run_id = run_id
        self.universe = list(universe)
        self.fail_fast = fail_fast
        self._lock = threading.Lock()
        self._report = LedgerReport(run_id=run_id, universe_size=len(universe))

    def checkpoint(
        self,
        stage: str,
        symbols_in: set[str],
        symbols_out: set[str],
        declared: dict[str, str] | None = None,
    ) -> None:
        """Assert conservation across one stage boundary.

        symbols_in  -- what entered the stage
        symbols_out -- what left it
        declared    -- {symbol: reason} the stage intentionally excluded

        Anything in `symbols_in` that is neither in `symbols_out` nor in
        `declared` is an unaccounted loss.
        """
        declared = declared or {}
        with self._lock:
            self._report.stage_counts.append((stage, len(symbols_in), len(symbols_out)))
            for sym, reason in sorted(declared.items()):
                if sym in symbols_in and sym not in symbols_out:
                    self._report.declared_exclusions.append((sym, stage, reason))
            lost = sorted(symbols_in - symbols_out - set(declared))
            for sym in lost:
                self._report.unaccounted_losses.append(StageLoss(sym, stage))

        if lost and self.fail_fast:
            raise TickersLost(
                f"stage {stage!r} lost {len(lost)} undeclared tickers "
                f"({len(lost) / max(len(self.universe), 1):.2%} of universe): "
                f"{lost[:10]}"
            )

    def finish(self, persisted: list[dict]) -> LedgerReport:
        self._report.persisted = persisted
        return self._report


# --------------------------------------------------------------------------
# Wiring the ledger into the stand-in pipeline -- the insertion pattern you
# copy. Note nothing inside pipeline.py changed: the ledger wraps boundaries,
# it does not require you to first understand which stage is guilty.
# --------------------------------------------------------------------------


def run_nightly_with_ledger(
    universe: list[str],
    metadata: dict,
    bugs: frozenset[str] = pipeline.DEFAULT_BUGS,
    fail_fast: bool = True,
    halted: dict[str, str] | None = None,
    run_id: str = "run",
    seed: int = 3,
) -> LedgerReport:
    halted = halted or {}
    led = Ledger(run_id, universe, fail_fast=fail_fast)

    entering = set(universe)

    rows = pipeline.fetch(universe, bugs, seed=seed)
    led.checkpoint("fetch", entering, {r.symbol for r in rows})

    before = {r.symbol for r in rows}
    rows = pipeline.normalize(rows, bugs)
    rows = [r for r in rows if r.symbol not in halted]
    led.checkpoint("normalize", before, {r.symbol for r in rows}, declared=halted)

    before = {r.symbol for r in rows}
    rows = pipeline.enrich(rows, metadata, bugs)
    led.checkpoint("enrich", before, {r.symbol for r in rows})

    persisted = pipeline.persist(rows)
    led.checkpoint("persist", {r.symbol for r in rows},
                   {r["symbol"] for r in persisted})

    return led.finish(persisted)
