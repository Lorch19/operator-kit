"""
Stand-in for the nightly ticker pipeline.

THIS IS NOT YOUR PIPELINE. It exists so the tests in test_no_silent_drops.py
have something real to go RED against. It reproduces the *shape* of the
failure you described -- a small, variable fraction of tickers vanishing
between input and output with no error raised -- using five drop mechanisms
that are each common in real market-data pipelines.

Its only job: prove the test suite and the ledger can actually catch a silent
drop. It proves NOTHING about which mechanism is in your pipeline.

Stages, matching the boundaries any nightly ticker pipeline has:

    universe -> fetch -> normalize -> enrich -> persist

Run it directly to see the failure:

    python3 pipeline.py                  # default bug: inner-join drop, ~2%
    python3 pipeline.py --bugs race      # non-deterministic drop
    python3 pipeline.py --bugs none      # clean run, nothing lost
"""

from __future__ import annotations

import argparse
import json
import random
import string
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

# --------------------------------------------------------------------------
# Universe construction
# --------------------------------------------------------------------------


def build_universe(n: int = 500, seed: int = 7) -> list[str]:
    """Build a realistic ticker universe.

    Deliberately includes the symbol shapes that break naive pipelines:
    dotted class shares (BRK.B), hyphenated variants (BRK-B), 5-letter
    symbols, and single-letter symbols.
    """
    rng = random.Random(seed)
    symbols: list[str] = []

    # Plain 1-4 letter symbols
    while len(symbols) < n - 24:
        length = rng.choice([1, 2, 3, 3, 4, 4, 4])
        sym = "".join(rng.choice(string.ascii_uppercase) for _ in range(length))
        if sym not in symbols:
            symbols.append(sym)

    # Class shares in both notations -- these collide under naive normalisation
    for base in ["BRK", "BF", "LEN", "HEI", "CWEN", "MOG"]:
        symbols += [f"{base}.A", f"{base}.B"]
    for base in ["STZ", "GEF", "PBR", "RDS", "UHAL", "CRD"]:
        symbols += [f"{base}-A", f"{base}-B"]

    # A handful of bases listed in BOTH notations by different vendors.
    # `BRK.B` and `BRK-B` are distinct rows that a naive key collapses into one.
    for base in ["BRK", "BF", "LEN"]:
        symbols += [f"{base}-A", f"{base}-B"]

    return sorted(set(symbols))


def build_metadata(universe: list[str], missing_rate: float = 0.02, seed: int = 11):
    """Reference/metadata table -- the thing a nightly run joins against.

    `missing_rate` is the fraction of the universe with no metadata row. In a
    real pipeline this is a corporate-actions or sector table that lags the
    universe file by a day or two.
    """
    rng = random.Random(seed)
    return {
        sym: {"sector": rng.choice(["Tech", "Energy", "Health", "Fin"])}
        for sym in universe
        if rng.random() >= missing_rate
    }


# --------------------------------------------------------------------------
# The pipeline
# --------------------------------------------------------------------------


@dataclass
class Row:
    symbol: str
    close: float | None = None
    history_days: int = 400
    sector: str | None = None
    meta: dict = field(default_factory=dict)


def _parse_symbol(symbol: str) -> str:
    """Naive symbol parser. Raises on dotted symbols -- a real bug shape:
    a downstream vendor SDK that rejects `BRK.B` and expects `BRK-B`."""
    if "." in symbol:
        raise ValueError(f"vendor rejected symbol: {symbol}")
    return symbol


def fetch(universe: list[str], bugs: frozenset[str], seed: int = 3) -> list[Row]:
    """Stage 1: pull a quote per ticker.

    BUG 'swallow': the classic bare except inside the per-ticker loop. One
    ticker raising means one ticker missing, and the run reports success.

    BUG 'race': results appended from a thread pool with a lost-update window.
    Drops a different set of tickers every night.
    """
    rng = random.Random(seed)
    rows: list[Row] = []

    if "race" in bugs:
        # Simulated lost update: worker reads len(rows), writes at that index.
        # Two workers reading the same length means one result is overwritten.
        slots: list[Row | None] = [None] * len(universe)
        counter = {"n": 0}

        def work(sym: str) -> None:
            i = counter["n"]  # read
            if rng.random() < 0.02:
                pass  # simulate the interleaving window -- no increment
            else:
                counter["n"] = i + 1  # write
            if i < len(slots):
                slots[i] = Row(symbol=sym, close=round(rng.uniform(5, 500), 2))

        with ThreadPoolExecutor(max_workers=1) as pool:
            list(pool.map(work, universe))
        return [r for r in slots if r is not None]

    for sym in universe:
        try:
            if "swallow" in bugs:
                _parse_symbol(sym)
            rows.append(
                Row(
                    symbol=sym,
                    close=round(rng.uniform(5, 500), 2),
                    # ~2% of the universe listed recently -- too little
                    # history for a trailing field to compute.
                    history_days=12 if rng.random() < 0.02 else 400,
                )
            )
        except Exception:
            continue  # <-- the bug: a swallowed exception is an invisible drop
    return rows


def normalize(rows: list[Row], bugs: frozenset[str]) -> list[Row]:
    """Stage 2: clean up symbols and numeric fields.

    BUG 'dedupe': normalising `BRK.B` and `BRK-B` to the same key `BRKB`, then
    de-duplicating, silently collapses two real tickers into one.

    BUG 'nan': dropping rows with nulls removes newly-listed tickers that have
    too little history to compute a trailing field.
    """
    out = list(rows)

    if "nan" in bugs:
        for r in out:
            if r.history_days < 60:
                r.close = None
        out = [r for r in out if r.close is not None]  # <-- dropna()

    if "dedupe" in bugs:
        seen: set[str] = set()
        deduped = []
        for r in out:
            key = r.symbol.replace(".", "").replace("-", "").upper()
            if key in seen:
                continue  # <-- collision silently discards a real ticker
            seen.add(key)
            deduped.append(r)
        out = deduped

    return out


def enrich(rows: list[Row], metadata: dict, bugs: frozenset[str]) -> list[Row]:
    """Stage 3: join the quote rows against the metadata table.

    BUG 'innerjoin': an inner join against a table that lags the universe.
    Every ticker missing from metadata disappears, with no error. This is the
    single most common silent-drop mechanism in data pipelines.
    """
    out = []
    for r in rows:
        meta = metadata.get(r.symbol)
        if meta is None and "innerjoin" in bugs:
            continue  # <-- inner join semantics: no match, no row
        r.sector = (meta or {}).get("sector", "Unknown")
        out.append(r)
    return out


def persist(rows: list[Row]) -> list[dict]:
    """Stage 4: write out. Returns the records that reached storage."""
    return [{"symbol": r.symbol, "close": r.close, "sector": r.sector} for r in rows]


DEFAULT_BUGS = frozenset({"innerjoin"})


def run_nightly(
    universe: list[str],
    metadata: dict,
    bugs: frozenset[str] = DEFAULT_BUGS,
    seed: int = 3,
) -> list[dict]:
    """The nightly run, exactly as it exists today: no accounting between
    stages, no error on loss, exit code 0 either way."""
    rows = fetch(universe, bugs, seed=seed)
    rows = normalize(rows, bugs)
    rows = enrich(rows, metadata, bugs)
    return persist(rows)


# --------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bugs", default="innerjoin",
                    help="comma-separated: swallow,race,dedupe,nan,innerjoin,none")
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--out", help="write nightly output as JSON to this path")
    args = ap.parse_args(argv)

    bugs = frozenset(b for b in args.bugs.split(",") if b and b != "none")
    universe = build_universe()
    metadata = build_metadata(universe)
    out = run_nightly(universe, metadata, bugs, seed=args.seed)

    lost = sorted(set(universe) - {r["symbol"] for r in out})
    print(f"universe={len(universe)}  persisted={len(out)}  "
          f"lost={len(lost)} ({len(lost) / len(universe):.2%})")
    if lost:
        print(f"lost symbols: {lost[:12]}{' ...' if len(lost) > 12 else ''}")
    print("exit code: 0   <-- the run reports success either way")

    if args.out:
        with open(args.out, "w") as fh:
            json.dump(out, fh)
    return 0


if __name__ == "__main__":
    sys.exit(main())
