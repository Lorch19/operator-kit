"""Run the pipeline with the ledger armed and print the attribution report.

This is the command that answers "where did it go", which an output diff
cannot answer. Usage:  python3 diagnose.py --bugs innerjoin
"""
import argparse, sys
import ledger, pipeline


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--bugs", default="innerjoin")
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--jsonl", action="store_true", help="emit machine-readable events")
    args = ap.parse_args(argv)

    bugs = frozenset(b for b in args.bugs.split(",") if b and b != "none")
    universe = pipeline.build_universe()
    metadata = pipeline.build_metadata(universe)

    rep = ledger.run_nightly_with_ledger(
        universe, metadata, bugs=bugs, fail_fast=False, seed=args.seed)

    if args.jsonl:
        print(rep.to_jsonl())
        return 1 if rep.unaccounted_losses else 0

    print(f"run={rep.run_id}  universe={rep.universe_size}")
    print(f"{'stage':<12}{'in':>7}{'out':>7}{'delta':>8}")
    for stage, n_in, n_out in rep.stage_counts:
        flag = "  <-- LOSS" if n_out < n_in else ""
        print(f"{stage:<12}{n_in:>7}{n_out:>7}{n_out - n_in:>8}{flag}")

    by_stage: dict[str, list[str]] = {}
    for loss in rep.unaccounted_losses:
        by_stage.setdefault(loss.stage, []).append(loss.symbol)
    print()
    if not by_stage:
        print("no unaccounted losses")
    for stage, syms in by_stage.items():
        print(f"unaccounted at {stage}: {len(syms)} ({len(syms)/rep.universe_size:.2%})")
        print(f"  {sorted(syms)[:12]}")
    print(f"\nexit code: {1 if rep.unaccounted_losses else 0}")
    return 1 if rep.unaccounted_losses else 0


if __name__ == "__main__":
    sys.exit(main())
