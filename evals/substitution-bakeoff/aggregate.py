#!/usr/bin/env python3
"""Unblind the comparator verdicts against the randomised key and tally each contest."""
import json, pathlib, sys

CONTESTS = {
    "design":            ("design-workspace/iteration-1",
                          {"kit": "design-tools (kit)", "sub": "ux-reviewer/ux-creator (substitute)"}),
    "engineering":       ("engineering-workspace/iteration-1",
                          {"kit": "engineering-tools (kit)", "other": "superpowers (substitute)"}),
    "prd-partner-fork":  ("prd-partner-fork-workspace/iteration-1",
                          {"kit": "prd-partner 466L (operator-kit)", "other": "prd-partner 428L (claude.ai synced)"}),
    "writing":           ("writing-workspace/iteration-1",
                          {"kit": "meta-tools/writing-great-skills (kit)", "sub": "superpowers/writing-skills"}),
    "ideation":          ("ideation-workspace/iteration-1",
                          {"kit": "pm-agents ideation (kit)", "sub": "superpowers/brainstorming"}),
}

for name, (ws, labels) in CONTESTS.items():
    wsp = pathlib.Path(ws)
    key = json.load(open(wsp / "_blind" / "key.json"))
    print(f"\n{'='*74}\n{name.upper()}\n{'='*74}")
    tally, rows = {}, []
    for ev in sorted(key, key=int):
        cpath = wsp / f"eval-{ev}" / "comparison.json"
        if not cpath.exists():
            rows.append((ev, "PENDING", "", "", "")); continue
        c = json.loads(cpath.read_text())
        w = c.get("winner", "?")
        side = key[ev].get(w) if w in ("A", "B") else "TIE"
        # swap test: same files, positions exchanged. If the unblinded winner
        # changes, the verdict tracked the slot rather than the content.
        spath = wsp / f"eval-{ev}" / "comparison_swapped.json"
        if spath.exists():
            import hashlib
            h = lambda q: hashlib.md5(pathlib.Path(q).read_bytes()).hexdigest()
            orig = {t: h(wsp/"_blind"/f"eval-{ev}"/f"{t}.md") for t in "AB"}
            swp  = {t: h(wsp/"_blind_swapped"/f"eval-{ev}"/f"{t}.md") for t in "AB"}
            inv  = {v: t for t, v in orig.items()}
            sw   = json.loads(spath.read_text()).get("winner")
            if sw in ("A","B"):
                side_sw = key[ev][inv[swp[sw]]]
                side = side if side_sw == side else "VOID (flipped on swap)"
        sa = c.get("rubric", {}).get("A", {}).get("overall_score", "")
        sb = c.get("rubric", {}).get("B", {}).get("overall_score", "")
        rows.append((ev, w, side, sa, sb))
        if side: tally[side] = tally.get(side, 0) + 1
    print(f"{'eval':<6}{'blind':<7}{'actual winner':<38}{'A':>6}{'B':>6}")
    for ev, w, side, sa, sb in rows:
        print(f"{ev:<6}{w:<7}{labels.get(side, side):<38}{str(sa):>6}{str(sb):>6}")
    print("-"*74)
    for k, v in sorted(tally.items(), key=lambda x: -x[1]):
        print(f"  {labels.get(k,k):<50} {v}")
    if len(set(tally.values())) == 1 and len(tally) > 1:
        print("  >> SPLIT — no decisive winner")
