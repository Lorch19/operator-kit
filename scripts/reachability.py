#!/usr/bin/env python3
"""Report which kit skills are actually reachable in a session.

validate-kit.py counts SKILL.md files in the repo. A skill only reaches a session
if its pack is enabled in ~/.claude/settings.json. Those numbers can differ a lot,
and file presence standing in for reachability is exactly the kind of proxy that
makes an unused skill look like an unwanted one.

Usage:  python3 scripts/reachability.py [--json]
"""
import json, re, pathlib, sys

SETTINGS = pathlib.Path.home() / ".claude" / "settings.json"
SKIP = re.compile(r"/(_deprecated|_incubator|evals|node_modules|\.git)/")

def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    try:
        enabled_raw = json.loads(SETTINGS.read_text()).get("enabledPlugins", {})
    except (OSError, json.JSONDecodeError) as e:
        print(f"cannot read {SETTINGS}: {e}", file=sys.stderr); return 2
    enabled = {k.split("@")[0] for k, v in enabled_raw.items()
               if v and k.endswith("@operator-kit")}

    packs = {}
    for p in root.rglob("SKILL.md"):
        if SKIP.search(str(p) + "/"): continue
        rel = p.relative_to(root).parts
        if len(rel) < 2: continue
        pack = rel[0]
        fm = re.match(r"^---\n(.*?)\n---", p.read_text(errors="replace"), re.S)
        if not fm: continue
        user_inv = bool(re.search(r"^disable-model-invocation:\s*true\s*$", fm.group(1), re.M))
        d = packs.setdefault(pack, {"total": 0, "model": 0, "enabled": pack in enabled})
        d["total"] += 1
        d["model"] += not user_inv

    tot  = sum(d["total"] for d in packs.values())
    mod  = sum(d["model"] for d in packs.values())
    rtot = sum(d["total"] for d in packs.values() if d["enabled"])
    rmod = sum(d["model"] for d in packs.values() if d["enabled"])

    if "--json" in sys.argv:
        print(json.dumps({"counted": {"active": tot, "model_invoked": mod},
                          "reachable": {"active": rtot, "model_invoked": rmod},
                          "packs": packs}, indent=2)); return 0

    print(f"{'pack':<22}{'skills':>7}{'model':>7}   enabled?")
    print("-" * 52)
    for name, d in sorted(packs.items()):
        print(f"{name:<22}{d['total']:>7}{d['model']:>7}   "
              f"{'yes' if d['enabled'] else '*** NO ***'}")
    print("-" * 52)
    print(f"counted in repo   : {tot} active, {mod} model-invoked")
    print(f"reachable in session: {rtot} active, {rmod} model-invoked")
    unreachable = tot - rtot
    if unreachable:
        print(f"\nUNREACHABLE: {unreachable} skills ({unreachable/tot*100:.0f}% of the kit) "
              f"— their pack is not in enabledPlugins, so they cannot fire in any\n"
              f"invocation mode. A zero for these measures installation, not fit.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
