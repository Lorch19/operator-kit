#!/usr/bin/env python3
"""VALIDATION FIXTURE - not part of your pipeline. Delete after reading.

Exists for one reason: to prove ticker_audit.py is red-capable and that its
same-tickers-or-different verdict actually separates the two classes of cause.
Each DROP_MODE is a real drop mechanism transcribed from production code I have seen.

  none            control - nothing dropped
  pool_swallow    worker-pool future raises; the `except Exception: continue` eats it
  retry_exhaust   429/503 from the vendor; retries exhausted, ticker skipped
  symbol_collision  BRK.B normalised to BRK-B, then dedup keeps one of the pair
  dropna          a required field is null, an inner join / dropna silently filters the row
  tail_batch      len(universe) % batch_size != 0 and the final partial batch is dropped

Usage: DROP_MODE=pool_swallow python3 fake_pipeline.py universe.txt out.csv
"""
import csv
import hashlib
import os
import random
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

MODE = os.environ.get("DROP_MODE", "none")
RATE = float(os.environ.get("DROP_RATE", "0.02"))
BATCH = int(os.environ.get("BATCH_SIZE", "64"))


def stable_hash(t: str) -> int:
    return int(hashlib.md5(t.encode()).hexdigest(), 16)


def fetch(ticker: str) -> dict:
    if MODE == "pool_swallow" and random.random() < RATE:
        raise TimeoutError(f"vendor read timed out for {ticker}")
    if MODE == "retry_exhaust" and random.random() < RATE:
        return None  # all retries used up; caller skips
    if MODE == "dropna" and stable_hash(ticker) % int(1 / RATE) == 0:
        return {"ticker": ticker, "close": None}  # required field null
    return {"ticker": ticker, "close": round(10 + stable_hash(ticker) % 4000 / 10, 2)}


def main() -> int:
    universe = [ln.strip() for ln in open(sys.argv[1]) if ln.strip()]
    out_path = sys.argv[2]
    rows = []

    if MODE == "tail_batch":
        batches = [universe[i:i + BATCH] for i in range(0, len(universe), BATCH)]
        if len(batches[-1]) < BATCH:
            batches.pop()  # "incomplete batch, skip it"
        universe_eff = [t for b in batches for t in b]
    else:
        universe_eff = universe

    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(fetch, t): t for t in universe_eff}
        for f in as_completed(futures):
            try:
                r = f.result()
            except Exception:
                continue  # <-- the swallow
            if r is None:
                continue  # <-- the retry-exhausted skip
            rows.append(r)

    rows = [r for r in rows if r["close"] is not None]  # <-- the dropna filter

    if MODE == "symbol_collision":
        seen, kept = set(), []
        for r in rows:
            k = r["ticker"].upper().replace(".", "-")
            if k in seen:
                continue  # <-- dedup on a normalised key discards the twin
            seen.add(k)
            kept.append(r)
        rows = kept

    rows.sort(key=lambda r: r["ticker"])
    with open(out_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["ticker", "close"])
        w.writeheader()
        w.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
