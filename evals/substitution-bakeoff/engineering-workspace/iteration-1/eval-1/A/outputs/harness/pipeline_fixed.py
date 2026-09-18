"""The same pipeline with the conservation invariant enforced.

The fix is not "catch this one exception". It is: make a silent drop impossible.
Every input ticker must leave the stage as either a row or a named failure, and the
ledger refuses to close if any are unaccounted for.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed

from pipeline_legacy import fetch


class LedgerBreach(RuntimeError):
    """Raised when a stage loses a ticker without recording why."""


class TickerLedger:
    """in == out + failed, checked at every stage boundary."""

    def __init__(self, stage, universe):
        self.stage, self.expected = stage, list(universe)
        self.ok, self.failed = [], []

    def record_ok(self, ticker):
        self.ok.append(ticker)

    def record_failure(self, ticker, reason):
        self.failed.append({"ticker": ticker, "stage": self.stage, "reason": reason})

    def close(self):
        seen = set(self.ok) | {f["ticker"] for f in self.failed}
        unaccounted = [t for t in self.expected if t not in seen]
        if unaccounted:
            raise LedgerBreach(
                f"stage {self.stage!r} lost {len(unaccounted)} ticker(s) with no reason "
                f"recorded: {unaccounted[:10]}"
            )
        return self.failed


def run_nightly(universe):
    ledger = TickerLedger("fetch", universe)
    rows = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(fetch, t): t for t in universe}
        for f in as_completed(futures):
            ticker = futures[f]
            try:
                rows.append(f.result())
                ledger.record_ok(ticker)
            except Exception as e:                       # still caught - but now NAMED
                ledger.record_failure(ticker, f"{type(e).__name__}: {e}")
    return {"rows": rows, "failures": ledger.close()}
