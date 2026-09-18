#!/usr/bin/env python3
"""ticker_audit - a red/green signal for "the nightly pipeline silently drops tickers".

This is the feedback loop. It does not guess at causes; it turns "about one in fifty
goes missing" into a deterministic pass/fail verdict plus the one measurement that
halves the hypothesis space: are the SAME tickers dropped every night, or different ones?

Subcommands
-----------
  audit     one universe + one output file  -> exactly which keys went missing (exit 1 if any)
  replay    run the pipeline N times        -> drop rate + same-tickers-or-different verdict
  backfill  N nights of existing outputs    -> the same verdict from artifacts you already have

Zero pipeline dependencies. Reads .txt .csv .tsv .json .jsonl .ndjson, and .parquet if
pandas is installed. Exit code 0 = green (nothing dropped), 1 = red (drops found),
2 = harness could not run.
"""
from __future__ import annotations

import argparse
import csv
import glob as globmod
import json
import os
import shlex
import statistics
import subprocess
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

# --------------------------------------------------------------------------- loading


def load_keys(path: str, key: str) -> list[str]:
    """Return the key column of `path` in file order, duplicates preserved.

    Duplicates are deliberately NOT collapsed: a fan-out join and a silent drop can
    produce the same row count, and only the duplicate census tells them apart.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    ext = p.suffix.lower()

    if ext in (".txt", ".lst", ""):
        return [ln.strip() for ln in p.read_text().splitlines() if ln.strip()]

    if ext in (".csv", ".tsv"):
        delim = "\t" if ext == ".tsv" else ","
        with p.open(newline="") as fh:
            rows = list(csv.DictReader(fh, delimiter=delim))
        if rows and key not in rows[0]:
            raise KeyError(f"column {key!r} not in {path}; columns={list(rows[0])}")
        return [r[key] for r in rows if r.get(key) is not None]

    if ext in (".jsonl", ".ndjson"):
        out = []
        for ln in p.read_text().splitlines():
            ln = ln.strip()
            if ln:
                out.append(json.loads(ln)[key])
        return out

    if ext == ".json":
        data = json.loads(p.read_text())
        if isinstance(data, dict):  # {"rows": [...]} or {"AAPL": {...}}
            data = data.get("rows", data.get("data", list(data.keys())))
        return [d if isinstance(d, str) else d[key] for d in data]

    if ext in (".parquet", ".pq"):
        import pandas as pd  # optional dependency, only for parquet

        return pd.read_parquet(p)[key].astype(str).tolist()

    raise ValueError(f"unsupported extension {ext!r} for {path}")


def norm(t: str) -> str:
    """The loosest plausible match: case, whitespace, and . / - / _ separators."""
    return t.strip().upper().replace(".", "-").replace("_", "-")


# --------------------------------------------------------------------------- audit


def audit(universe: list[str], produced: list[str]) -> dict:
    uni, prod = list(universe), list(produced)
    uni_set, prod_set = set(uni), set(prod)

    missing_exact = [t for t in uni if t not in prod_set]

    # A key that is missing exactly but present once normalised was MANGLED, not dropped.
    prod_norm = {norm(t) for t in prod}
    mangled = [t for t in missing_exact if norm(t) in prod_norm]
    missing_real = [t for t in missing_exact if norm(t) not in prod_norm]

    dup_counts = {t: c for t, c in Counter(prod).items() if c > 1}
    unexpected = sorted(prod_set - uni_set)

    return {
        "universe_n": len(uni),
        "produced_n": len(prod),
        "produced_unique_n": len(prod_set),
        "missing_n": len(missing_exact),
        "missing": missing_exact,
        "missing_dropped": missing_real,      # genuinely absent
        "missing_mangled": mangled,           # present under a different spelling
        "duplicates": dup_counts,
        "unexpected": unexpected,
        "green": len(missing_exact) == 0 and not unexpected,
    }


def print_audit(a: dict) -> None:
    v = "GREEN" if a["green"] else "RED"
    print(f"[{v}] universe={a['universe_n']} produced={a['produced_n']} "
          f"unique={a['produced_unique_n']} missing={a['missing_n']} "
          f"({a['missing_n'] / max(a['universe_n'], 1):.2%})")
    if a["missing_dropped"]:
        print(f"  dropped  ({len(a['missing_dropped'])}): {', '.join(a['missing_dropped'][:25])}"
              + (" ..." if len(a["missing_dropped"]) > 25 else ""))
    if a["missing_mangled"]:
        print(f"  MANGLED  ({len(a['missing_mangled'])}) - present under another spelling, "
              f"not dropped: {', '.join(a['missing_mangled'][:25])}")
    if a["duplicates"]:
        print(f"  duplicates ({len(a['duplicates'])}): "
              f"{', '.join(f'{k}x{v}' for k, v in list(a['duplicates'].items())[:15])}")
    if a["unexpected"]:
        print(f"  not in universe ({len(a['unexpected'])}): {', '.join(a['unexpected'][:15])}")


# ------------------------------------------------------------------- stability stats


def stability(dropped_sets: list[set[str]], universe_n: int) -> dict:
    """Same tickers every night, or different ones? The fork that halves the search.

    Compares observed pairwise Jaccard overlap against the overlap you would expect if
    each night drew its victims uniformly at random from the universe. For k drops out
    of N, E|A n B| ~ k^2/N, so E[J] ~ k / (2N - k). Observed >> that means the victims
    share an attribute (deterministic cause). Observed ~= that means the cause is
    run-dependent (concurrency, transient I/O, timing).
    """
    nonempty = [s for s in dropped_sets if s]
    events = Counter()
    for s in dropped_sets:
        events.update(s)

    pairs = [
        len(a & b) / len(a | b)
        for a, b in combinations(nonempty, 2)
        if a | b
    ]
    mean_k = statistics.mean(len(s) for s in nonempty) if nonempty else 0.0
    expected_j = mean_k / (2 * universe_n - mean_k) if universe_n and mean_k else 0.0
    observed_j = statistics.mean(pairs) if pairs else 0.0

    repeat_offenders = {t: c for t, c in events.items() if c > 1}
    total_events = sum(events.values())
    repeat_share = (
        sum(c for c in repeat_offenders.values()) / total_events if total_events else 0.0
    )

    if not nonempty:
        verdict = "NO DROPS OBSERVED - loop never went red; raise --runs or check the wiring"
    elif observed_j >= max(0.30, expected_j * 10):
        verdict = ("DETERMINISTIC - the same tickers are dropped every run. The cause is an "
                   "ATTRIBUTE of those tickers (symbol format, missing field, listing venue, "
                   "corporate action). Go read the dropped list; the pattern is in it.")
    elif observed_j <= expected_j * 3:
        verdict = ("RUN-DEPENDENT - different tickers each run, overlap indistinguishable from "
                   "chance. The cause is in the RUN, not the ticker: concurrency, transient I/O, "
                   "retry exhaustion, timeouts, partial-batch handling.")
    else:
        verdict = ("MIXED - overlap above chance but not stable. Suspect a small deterministic "
                   "subset on top of a stochastic background, or a load-dependent threshold. "
                   "Split the repeat offenders out and treat them as two separate bugs.")

    return {
        "runs": len(dropped_sets),
        "runs_with_drops": len(nonempty),
        "mean_drops_per_run": round(mean_k, 2),
        "drop_rate": round(mean_k / universe_n, 4) if universe_n else 0.0,
        "unique_tickers_ever_dropped": len(events),
        "total_drop_events": total_events,
        "observed_pairwise_jaccard": round(observed_j, 4),
        "expected_jaccard_if_random": round(expected_j, 4),
        "repeat_offender_share": round(repeat_share, 3),
        "top_offenders": events.most_common(15),
        "verdict": verdict,
    }


def print_stability(s: dict) -> None:
    print("\n=== stability ===")
    print(f"runs={s['runs']} (with drops: {s['runs_with_drops']})  "
          f"mean drops/run={s['mean_drops_per_run']}  drop rate={s['drop_rate']:.2%}")
    print(f"unique tickers ever dropped={s['unique_tickers_ever_dropped']}  "
          f"total drop events={s['total_drop_events']}")
    print(f"pairwise Jaccard: observed={s['observed_pairwise_jaccard']}  "
          f"expected-if-random={s['expected_jaccard_if_random']}  "
          f"repeat-offender share={s['repeat_offender_share']}")
    print(f"top offenders: {s['top_offenders'][:10]}")
    print(f"VERDICT: {s['verdict']}")


# --------------------------------------------------------------------------- runners


def cmd_audit(args) -> int:
    a = audit(load_keys(args.universe, args.key), load_keys(args.output, args.key))
    print_audit(a)
    if args.json:
        Path(args.json).write_text(json.dumps(a, indent=2))
    return 0 if a["green"] else 1


def cmd_replay(args) -> int:
    universe = load_keys(args.universe, args.key)
    env = dict(os.environ)
    for kv in args.env or []:
        k, _, v = kv.partition("=")
        env[k] = v

    dropped_sets, per_run, failures = [], [], 0
    for i in range(args.runs):
        Path(args.output).unlink(missing_ok=True)
        r = subprocess.run(args.cmd, shell=True, env=env,
                           capture_output=True, text=True, timeout=args.timeout)
        if r.returncode != 0 or not Path(args.output).exists():
            failures += 1
            print(f"run {i:>3}: PIPELINE FAILED rc={r.returncode} "
                  f"{(r.stderr or '').strip()[:200]}")
            continue
        a = audit(universe, load_keys(args.output, args.key))
        dropped_sets.append(set(a["missing"]))
        per_run.append(a["missing_n"])
        print(f"run {i:>3}: missing={a['missing_n']:>3}  "
              f"{', '.join(sorted(a['missing'])[:8])}")

    if failures:
        print(f"\n{failures}/{args.runs} runs failed outright - that is its own finding.")
    s = stability(dropped_sets, len(universe))
    print_stability(s)
    if args.json:
        Path(args.json).write_text(json.dumps(
            {"per_run_missing": per_run,
             "dropped_sets": [sorted(x) for x in dropped_sets],
             "stability": s}, indent=2))
    return 0 if s["total_drop_events"] == 0 and not failures else 1


def cmd_backfill(args) -> int:
    files = sorted(globmod.glob(args.outputs))
    if not files:
        print(f"no files matched {args.outputs!r}", file=sys.stderr)
        return 2
    universes = sorted(globmod.glob(args.universe_glob)) if args.universe_glob else None
    if universes and len(universes) != len(files):
        print(f"universe count {len(universes)} != output count {len(files)}", file=sys.stderr)
        return 2

    dropped_sets, uni_n = [], 0
    print("=== per-night ===")
    for i, f in enumerate(files):
        uni = load_keys(universes[i] if universes else args.universe, args.key)
        uni_n = max(uni_n, len(uni))
        a = audit(uni, load_keys(f, args.key))
        dropped_sets.append(set(a["missing"]))
        print(f"{Path(f).name:<32} universe={a['universe_n']:>5} produced={a['produced_n']:>5} "
              f"missing={a['missing_n']:>3} ({a['missing_n']/max(a['universe_n'],1):.2%})"
              + (f"  MANGLED={len(a['missing_mangled'])}" if a["missing_mangled"] else "")
              + (f"  DUPS={len(a['duplicates'])}" if a["duplicates"] else ""))
    s = stability(dropped_sets, uni_n)
    print_stability(s)
    print("\nStep change or ramp? Read the per-night missing column top to bottom. A step "
          "means a deploy or config change; a ramp means growth crossing a limit.")
    if args.json:
        Path(args.json).write_text(json.dumps(
            {"files": files, "dropped_sets": [sorted(x) for x in dropped_sets],
             "stability": s}, indent=2))
    return 0 if s["total_drop_events"] == 0 else 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="sub", required=True)

    def common(sp):
        sp.add_argument("--key", default="ticker", help="key column/field (default: ticker)")
        sp.add_argument("--json", help="also write raw results here")

    a = sub.add_parser("audit", help="one universe vs one output")
    a.add_argument("--universe", required=True)
    a.add_argument("--output", required=True)
    common(a)
    a.set_defaults(func=cmd_audit)

    r = sub.add_parser("replay", help="run the pipeline N times and aggregate")
    r.add_argument("--cmd", required=True, help="shell command that runs the pipeline")
    r.add_argument("--universe", required=True)
    r.add_argument("--output", required=True, help="file the pipeline writes (deleted before each run)")
    r.add_argument("--runs", type=int, default=30)
    r.add_argument("--timeout", type=int, default=1800)
    r.add_argument("--env", action="append", help="K=V passed to the pipeline (repeatable)")
    common(r)
    r.set_defaults(func=cmd_replay)

    b = sub.add_parser("backfill", help="audit N nights of existing outputs")
    b.add_argument("--outputs", required=True, help="glob of nightly output files")
    b.add_argument("--universe", help="single universe file used for every night")
    b.add_argument("--universe-glob", help="per-night universe files, sorted to match --outputs")
    common(b)
    b.set_defaults(func=cmd_backfill)

    args = p.parse_args(argv)
    if args.sub == "backfill" and not (args.universe or args.universe_glob):
        p.error("backfill needs --universe or --universe-glob")
    try:
        return args.func(args)
    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"harness error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
