#!/usr/bin/env python3
"""
drop_forensics.py -- turn 14 nights of output files into a drop-event dataset.

You already have the data to answer the decisive question; it is sitting in
your nightly output files. This reads them and reports whether the SAME
tickers drop every night (a deterministic property of those tickers) or a
DIFFERENT set each night (timing, concurrency, or an upstream flake).

Those two answers point at disjoint sets of causes, and every hour spent
guessing before you know which one you have is wasted.

Stdlib only -- no install needed.

    python3 drop_forensics.py --nights 'out/*.json' --universe universe.txt
    python3 drop_forensics.py --nights 'out/*.csv' --symbol-col ticker

If you have no universe file, omit --universe: the union of all nights is used
as the expected set. That undercounts (a ticker dropped on ALL nights is
invisible), which the report states explicitly.
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import math
import os
import re
import sys
from collections import Counter

SYMBOL_KEYS = ("symbol", "ticker", "sym", "Symbol", "Ticker", "SYMBOL", "code")


# --------------------------------------------------------------------------
# Loading -- tolerant of csv / json / jsonl / plain text
# --------------------------------------------------------------------------


def _symbols_from_records(records: list[dict], symbol_col: str | None) -> set[str]:
    if not records:
        return set()
    keys = [symbol_col] if symbol_col else [
        k for k in SYMBOL_KEYS if k in records[0]
    ]
    if not keys:
        raise SystemExit(
            f"no symbol column found; columns are {list(records[0])[:12]}. "
            f"Pass --symbol-col."
        )
    key = keys[0]
    return {str(r[key]).strip() for r in records if r.get(key)}


def load_symbols(path: str, symbol_col: str | None = None) -> set[str]:
    ext = os.path.splitext(path)[1].lower()
    with open(path) as fh:
        text = fh.read()
    if not text.strip():
        return set()

    if ext == ".csv":
        return _symbols_from_records(list(csv.DictReader(text.splitlines())), symbol_col)
    if ext in (".jsonl", ".ndjson"):
        return _symbols_from_records(
            [json.loads(line) for line in text.splitlines() if line.strip()], symbol_col)
    if ext == ".json":
        data = json.loads(text)
        if isinstance(data, dict):
            data = next((v for v in data.values() if isinstance(v, list)), list(data))
        if data and isinstance(data[0], str):
            return {s.strip() for s in data}
        return _symbols_from_records(data, symbol_col)
    # .txt / anything else: one symbol per line
    return {line.strip() for line in text.splitlines() if line.strip()}


# --------------------------------------------------------------------------
# The decisive statistic
# --------------------------------------------------------------------------


def recurrence_verdict(drop_events: dict[str, set[str]], expected: set[str]) -> dict:
    """Are the same tickers dropping every night, or different ones?

    Under the null hypothesis 'drops are independent coin flips at rate p',
    the number of DISTINCT tickers that ever drop across N nights is
    approximately  |U| * (1 - (1-p)^N).  If the observed number of distinct
    droppers is far BELOW that, the same tickers are recurring: the drop is a
    deterministic property of those tickers, not chance.
    """
    nights = len(drop_events)
    total_drops = sum(len(v) for v in drop_events.values())
    distinct = len({s for v in drop_events.values() for s in v})
    u = max(len(expected), 1)
    p = total_drops / (u * max(nights, 1))

    expected_distinct = u * (1 - (1 - p) ** nights) if nights else 0.0
    # Concentration ratio: 1.0 = pure chance, ->0 = same tickers every night
    ratio = distinct / expected_distinct if expected_distinct > 0 else float("nan")

    counts = Counter()
    for v in drop_events.values():
        for s in v:
            counts[s] += 1
    hist = Counter(counts.values())

    if nights < 3:
        verdict = "INCONCLUSIVE - need at least 3 nights"
    elif ratio < 0.5:
        verdict = "DETERMINISTIC - the same tickers drop repeatedly"
    elif ratio > 0.85:
        verdict = "STOCHASTIC - a different set drops each night"
    else:
        verdict = "MIXED - a recurring core plus a random tail"

    return {
        "nights": nights, "universe": u, "total_drops": total_drops,
        "distinct_droppers": distinct, "per_night_rate": p,
        "expected_distinct_if_random": expected_distinct,
        "concentration_ratio": ratio, "recurrence_hist": dict(sorted(hist.items())),
        "verdict": verdict, "counts": counts,
    }


def property_profile(dropped: set[str], kept: set[str]) -> list[tuple[str, str]]:
    """Does any cheap symbol property separate dropped from kept?

    A property that is 5x enriched among the dropped is a lead. A property
    with no enrichment rules that mechanism out. Both are useful.
    """
    def frac(pred, pool):
        return sum(1 for s in pool if pred(s)) / len(pool) if pool else 0.0

    props = {
        "contains '.'": lambda s: "." in s,
        "contains '-'": lambda s: "-" in s,
        "contains a digit": lambda s: any(c.isdigit() for c in s),
        "length >= 5": lambda s: len(s) >= 5,
        "length == 1": lambda s: len(s) == 1,
        "lowercase present": lambda s: s != s.upper(),
        "non-ASCII": lambda s: not s.isascii(),
        "leading/trailing space": lambda s: s != s.strip(),
        "^ or / or space inside": lambda s: bool(re.search(r"[ /^]", s)),
    }
    rows = []
    for name, pred in props.items():
        fd, fk = frac(pred, dropped), frac(pred, kept)
        if fd == 0 and fk == 0:
            continue
        lift = (fd / fk) if fk > 0 else float("inf")
        flag = "  <-- LEAD" if fd > 0 and (lift > 3 or fk == 0) else ""
        rows.append((name, f"dropped {fd:6.1%}   kept {fk:6.1%}   lift {lift:>5.1f}x{flag}"))
    return rows


def batch_alignment(dropped: set[str], expected: set[str]) -> list[str]:
    """If the universe is processed in sorted order in fixed-size batches, a
    pagination/chunking bug puts drops at predictable positions. Look for
    drops clustering at one residue mod a common batch size."""
    order = sorted(expected)
    idx = {s: i for i, s in enumerate(order)}
    positions = sorted(idx[s] for s in dropped if s in idx)
    out = []
    if len(positions) < 4:
        return ["too few drops to test batch alignment"]
    for size in (10, 16, 25, 32, 50, 64, 100, 128, 250):
        if size >= len(order):
            continue
        residues = Counter(p % size for p in positions)
        top, n = residues.most_common(1)[0]
        share = n / len(positions)
        # Under uniformity each residue holds ~1/size of the drops
        if share > max(0.5, 4.0 / size):
            out.append(f"batch size {size:>4}: {share:.0%} of drops at position "
                       f"{top} within the batch  <-- LEAD")
    # Edge-of-run clustering: last N of the sorted order
    tail = sum(1 for p in positions if p >= len(order) - max(len(positions), 10))
    if tail / len(positions) > 0.5:
        out.append("drops cluster at the END of the sorted universe  <-- LEAD "
                   "(truncation, timeout, or an unflushed final batch)")
    return out or ["no batch-size alignment detected (pagination/chunking unlikely)"]


# --------------------------------------------------------------------------


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nights", required=True, help="glob of nightly output files")
    ap.add_argument("--universe", help="file listing the expected ticker universe")
    ap.add_argument("--symbol-col", help="column name holding the symbol")
    args = ap.parse_args(argv)

    paths = sorted(glob.glob(args.nights))
    if not paths:
        raise SystemExit(f"no files matched {args.nights!r}")

    nights = {os.path.basename(p): load_symbols(p, args.symbol_col) for p in paths}

    if args.universe:
        expected = load_symbols(args.universe, args.symbol_col)
        source = args.universe
    else:
        expected = set().union(*nights.values())
        source = "union of all nights (UNDERCOUNTS: a ticker absent every "
        source += "night is invisible to this run -- supply --universe)"

    drop_events = {night: expected - present for night, present in nights.items()}

    print("=" * 74)
    print("DROP FORENSICS")
    print("=" * 74)
    print(f"nights analysed : {len(nights)}")
    print(f"expected set    : {len(expected)} tickers, from {source}")
    print()
    print(f"{'night':<28}{'present':>9}{'dropped':>9}{'rate':>9}")
    for night, present in nights.items():
        d = len(drop_events[night])
        print(f"{night:<28}{len(present):>9}{d:>9}{d / max(len(expected),1):>8.2%}")

    v = recurrence_verdict(drop_events, expected)
    print()
    print("-" * 74)
    print("IS IT THE SAME TICKERS EVERY NIGHT?")
    print("-" * 74)
    print(f"total drop events         : {v['total_drops']}")
    print(f"distinct tickers involved : {v['distinct_droppers']}")
    print(f"expected distinct if pure chance at this rate: "
          f"{v['expected_distinct_if_random']:.1f}")
    print(f"concentration ratio       : {v['concentration_ratio']:.2f}   "
          f"(1.0 = chance, 0 = same tickers every night)")
    print(f"recurrence histogram      : "
          f"{ {f'{k} night(s)': n for k, n in v['recurrence_hist'].items()} }")
    print()
    print(f"  VERDICT: {v['verdict']}")
    print()

    repeaters = [s for s, c in v["counts"].most_common(15) if c > 1]
    if repeaters:
        print(f"  most frequent droppers: {repeaters[:15]}")
        print()

    all_dropped = {s for d in drop_events.values() for s in d}
    kept = expected - all_dropped
    print("-" * 74)
    print("DOES ANY SYMBOL PROPERTY SEPARATE DROPPED FROM KEPT?")
    print("-" * 74)
    for name, line in property_profile(all_dropped, kept):
        print(f"  {name:<26}{line}")
    print()
    print("-" * 74)
    print("BATCH / POSITION ALIGNMENT")
    print("-" * 74)
    for line in batch_alignment(all_dropped, expected):
        print(f"  {line}")

    print()
    print("=" * 74)
    print("NEXT COMMAND")
    print("=" * 74)
    if v["verdict"].startswith("DETERMINISTIC"):
        print("  The drop is a property of those specific tickers. Replay ONLY")
        print("  them through the pipeline -- that is your red-capable loop, and")
        print("  it runs in seconds instead of overnight:")
        print(f"    <your-runner> --tickers {','.join(sorted(repeaters)[:8])} --with-ledger")
    elif v["verdict"].startswith("STOCHASTIC"):
        print("  The drop is NOT a property of the tickers -- it is timing,")
        print("  concurrency, or an upstream flake. Replay the SAME input set")
        print("  repeatedly and vary only concurrency:")
        print("    for i in $(seq 20); do <your-runner> --replay <fixed-input> "
              "--with-ledger --workers 1;  done")
        print("    # if 20 serial runs lose nothing, concurrency is implicated")
    else:
        print("  Split the set: analyse the repeat droppers and the one-night")
        print("  droppers as two separate investigations. They are two bugs.")
    print()
    print("  In every branch, arm the stage ledger first (see ledger.py) so the")
    print("  NEXT run records where the ticker was lost, not merely that it was.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
