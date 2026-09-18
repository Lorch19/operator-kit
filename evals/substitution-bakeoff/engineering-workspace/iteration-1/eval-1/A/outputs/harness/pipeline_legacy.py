"""Stand-in for the current nightly pipeline: the shape that drops silently."""
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

FAIL_RATE = 0.02


def fetch(ticker):
    if random.random() < FAIL_RATE:
        raise TimeoutError(f"vendor read timed out for {ticker}")
    return {"ticker": ticker, "close": 100.0}


def run_nightly(universe):
    rows = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(fetch, t): t for t in universe}
        for f in as_completed(futures):
            try:
                rows.append(f.result())
            except Exception:
                continue          # <-- the silent drop
    return {"rows": rows, "failures": []}
