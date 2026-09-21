#!/usr/bin/env python3
"""Enumerate every skill name that exists in more than one place, and classify the fork."""
import re, pathlib, hashlib
from collections import defaultdict

ROOTS = {
 "kit":        "/Users/omrilorch/operator-kit/.claude/worktrees/practical-noyce-5836aa",
 "user":       "/Users/omrilorch/.claude/skills",
 "synced":     "/Users/omrilorch/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin",
 "superpowers":"/Users/omrilorch/.claude/plugins/cache/claude-plugins-official/superpowers/6.3.0/skills",
 "ux-agent":   "/Users/omrilorch/UX-Agent/skills",
}
SKIP = re.compile(r"/(_deprecated|_incubator|\.dean-peters\.bak|node_modules|\.git|/tests?/|evals/)")

def split(p):
    t = p.read_text(errors="replace")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", t, re.S)
    if not m: return None, None, None
    fm, body = m.group(1), m.group(2)
    n = re.search(r"^name:\s*(.+)$", fm, re.M)
    d = re.search(r"^description:\s*(.+(?:\n\s+.+)*)$", fm, re.M)
    return (n.group(1).strip() if n else None,
            " ".join(d.group(1).split()) if d else "",
            hashlib.md5(body.strip().encode()).hexdigest())

seen = defaultdict(list)
for origin, root in ROOTS.items():
    for p in pathlib.Path(root).rglob("SKILL.md"):
        if SKIP.search(str(p)+"/"): continue
        name, desc, bh = split(p)
        if not name: continue
        seen[name].append((origin, desc, bh, p))

dupes = {k: v for k, v in seen.items() if len({o for o,_,_,_ in v}) > 1}
cats = defaultdict(list)
for name, entries in sorted(dupes.items()):
    bodies = {bh for _,_,bh,_ in entries}
    descs  = {d for _,d,_,_ in entries}
    origins = "+".join(sorted({o for o,_,_,_ in entries}))
    if len(bodies) == 1 and len(descs) == 1: cats["identical"].append((name,origins))
    elif len(bodies) == 1:                   cats["description-only"].append((name,origins))
    else:                                    cats["true fork (body differs)"].append((name,origins))

for cat in ("true fork (body differs)","description-only","identical"):
    rows = cats.get(cat,[])
    print(f"\n{cat.upper()}  —  {len(rows)}")
    for n,o in rows: print(f"   {n:<34} {o}")
print(f"\nTOTAL duplicated names across roots: {len(dupes)}")
