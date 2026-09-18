#!/usr/bin/env python3
"""Collect every model-invoked skill description that would compete in a live session."""
import re, pathlib, json, sys

ROOTS = {
  "operator-kit": "/Users/omrilorch/operator-kit/.claude/worktrees/practical-noyce-5836aa",
  "user-skills":  "/Users/omrilorch/.claude/skills",
  "superpowers":  "/Users/omrilorch/.claude/plugins/cache/claude-plugins-official/superpowers/6.3.0/skills",
  "ux-agent":     "/Users/omrilorch/UX-Agent/skills",
  "synced":       "/Users/omrilorch/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin",
}
SKIP = re.compile(r"/(_deprecated|_incubator|\.dean-peters\.bak|node_modules|\.git|tests?)/")

def fm(p):
    t = p.read_text(errors="replace")
    m = re.match(r"^---\n(.*?)\n---", t, re.S)
    return m.group(1) if m else ""

rows = []
for origin, root in ROOTS.items():
    for p in pathlib.Path(root).rglob("SKILL.md"):
        if SKIP.search(str(p)): continue
        f = fm(p)
        if not f: continue
        if re.search(r"^disable-model-invocation:\s*true\s*$", f, re.M): continue  # user-invoked: not in context
        n = re.search(r"^name:\s*(.+)$", f, re.M)
        d = re.search(r"^description:\s*(.+(?:\n\s+.+)*)$", f, re.M)
        if not (n and d): continue
        rows.append({"origin": origin, "name": n.group(1).strip(),
                     "description": " ".join(d.group(1).split()), "path": str(p)})

seen, out = set(), []
for r in sorted(rows, key=lambda r: r["name"]):
    k = (r["name"], r["description"][:60])
    if k in seen: continue
    seen.add(k); out.append(r)

json.dump(out, open("/tmp/claude-501/roster.json","w"), indent=1)
print(f"model-invoked skills competing in context: {len(out)}")
from collections import Counter
for o,c in Counter(r["origin"] for r in out).items(): print(f"  {o:<14} {c}")
