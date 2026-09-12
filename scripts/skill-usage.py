#!/usr/bin/env python3
"""Report which Operator Kit skills have actually been invoked, across every repo.

Git history shows what was *built*; it says nothing about what gets *used* — and
the kit is installed globally, so usage happens in other repos entirely. Claude
Code writes a JSONL transcript per session under

    ~/.claude/projects/<encoded-working-dir>/<session-id>.jsonl

one directory per working directory, so scanning them covers every repo at once.

Usage:
    python3 scripts/skill-usage.py                # everything on record
    python3 scripts/skill-usage.py --days 90      # sessions touched in 90 days
    python3 scripts/skill-usage.py --unused       # only the never-invoked list
    python3 scripts/skill-usage.py --json

Run it on the machine you actually work on. Transcripts are local, so a remote
or fresh container sees only its own session.

READ THE RESULT CAREFULLY. Absence of evidence is weak evidence here:

  * Transcripts can be rotated or cleared; an old session may simply be gone.
  * A skill read by another skill, or applied from memory, leaves no Skill call.
  * Only invocations through the Skill tool and `/slash` commands are recorded.

So treat a zero as "no record of use in this window" — a prune *candidate*,
never a verdict.
"""
import argparse
import glob
import json
import os
import re
import signal
import sys
import time
from collections import Counter, defaultdict

# Long output is meant to be piped into head/less; die quietly when they close.
if hasattr(signal, "SIGPIPE"):
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUCKETS = ("_incubator", "_deprecated")
PROJECTS = os.path.expanduser("~/.claude/projects")
CMD_RE = re.compile(r"<command-name>/?([A-Za-z0-9:_-]+)</command-name>")


def kit_skills():
    """{skill name: pack} for every promoted skill in this repo."""
    out = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "**", "SKILL.md"), recursive=True)):
        rel = os.path.relpath(os.path.dirname(path), ROOT)
        if rel.startswith(BUCKETS):
            continue
        try:
            fm = open(path, encoding="utf-8").read().split("---", 2)[1]
        except (IndexError, UnicodeDecodeError):
            continue
        m = re.search(r"^name:\s*(.+)$", fm, re.M)
        if m:
            out[m.group(1).strip()] = rel.split(os.sep)[0]
    return out


def blocks(message):
    content = message.get("content")
    return content if isinstance(content, list) else []


def scan(cutoff):
    """(counts, by_project, channels, stats) from every transcript on disk."""
    counts = Counter()
    by_project = defaultdict(set)
    channels = Counter()
    files = skipped = records = 0

    for path in glob.glob(os.path.join(PROJECTS, "*", "*.jsonl")):
        if cutoff and os.path.getmtime(path) < cutoff:
            skipped += 1
            continue
        files += 1
        project = os.path.basename(os.path.dirname(path))
        try:
            fh = open(path, encoding="utf-8", errors="replace")
        except OSError:
            continue
        with fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                records += 1
                msg = rec.get("message") or {}
                for blk in blocks(msg):
                    if not isinstance(blk, dict):
                        continue
                    # Channel 1: the Skill tool — model-invoked or typed by name.
                    if blk.get("type") == "tool_use" and blk.get("name") == "Skill":
                        name = (blk.get("input") or {}).get("skill", "")
                        name = name.split(":")[-1].strip()
                        if name:
                            counts[name] += 1
                            by_project[name].add(project)
                            channels["Skill tool"] += 1
                    # Channel 2: an expanded /slash command.
                    elif blk.get("type") == "text":
                        for hit in CMD_RE.findall(blk.get("text") or ""):
                            name = hit.split(":")[-1]
                            counts[name] += 1
                            by_project[name].add(project)
                            channels["/slash command"] += 1
                if isinstance(msg.get("content"), str):
                    for hit in CMD_RE.findall(msg["content"]):
                        name = hit.split(":")[-1]
                        counts[name] += 1
                        by_project[name].add(project)
                        channels["/slash command"] += 1

    return counts, by_project, channels, (files, skipped, records)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, help="only sessions modified in the last N days")
    ap.add_argument("--unused", action="store_true", help="print only the never-invoked list")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()

    if not os.path.isdir(PROJECTS):
        sys.exit(f"No transcripts at {PROJECTS}.\n"
                 "Run this on the machine you work on — transcripts are local.")

    cutoff = time.time() - args.days * 86400 if args.days else None
    counts, by_project, channels, (files, skipped, records) = scan(cutoff)
    skills = kit_skills()

    used = {n: c for n, c in counts.items() if n in skills}
    unused = sorted(n for n in skills if n not in used)
    foreign = sorted(n for n in counts if n not in skills)

    if args.as_json:
        json.dump({"window_days": args.days, "sessions_scanned": files,
                   "used": used, "unused": unused, "not_in_kit": foreign,
                   "projects": {k: sorted(v) for k, v in by_project.items()}},
                  sys.stdout, indent=2)
        print()
        return 0

    if args.unused:
        by_pack = defaultdict(list)
        for n in unused:
            by_pack[skills[n]].append(n)
        for pack in sorted(by_pack):
            print(f"\n{pack}  ({len(by_pack[pack])} with no record of use)")
            for n in by_pack[pack]:
                print(f"    {n}")
        return 0

    window = f"last {args.days} days" if args.days else "all transcripts on record"
    print(f"Scanned {files} session file(s), {records:,} records — {window}."
          + (f" Skipped {skipped} outside the window." if skipped else ""))
    if channels:
        print("Recorded via: " + ", ".join(f"{k} ({v})" for k, v in channels.most_common()))
    print()

    print(f"USED — {len(used)} of {len(skills)} kit skills")
    if used:
        width = max(len(n) for n in used)
        for n, c in sorted(used.items(), key=lambda kv: -kv[1]):
            repos = len(by_project[n])
            print(f"  {c:4}x  {n:{width}}  {skills[n]:<18} {repos} repo{'s' if repos != 1 else ''}")
    else:
        print("  (none — see the caveats in this file's docstring before concluding anything)")

    print(f"\nNO RECORD OF USE — {len(unused)} skills")
    print("  Prune candidates, not verdicts. `--unused` lists them by pack.")
    per_pack = Counter(skills[n] for n in unused)
    for pack, n in per_pack.most_common():
        print(f"    {n:3}  {pack}")

    if foreign:
        print(f"\nInvoked but not in this kit ({len(foreign)}): {', '.join(foreign[:12])}"
              + (" …" if len(foreign) > 12 else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
