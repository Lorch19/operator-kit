#!/usr/bin/env python3
"""Produce skill-anonymised copies of eval outputs for the blind comparator.

Originals are never modified. Every token that could reveal which contender
produced an output is replaced with a neutral placeholder.
"""
import re, sys, pathlib, json

# Order matters: longest / most specific first.
RULES = [
    # paths
    (r"/Users/omrilorch/\.claude/plugins/cache/claude-plugins-official/superpowers/[\d.]+/skills/[\w-]+", "[SKILL_PATH]"),
    (r"/Users/omrilorch/UX-Agent/skills/[\w-]+", "[SKILL_PATH]"),
    (r"/Users/omrilorch/Library/Application Support/Claude/[^\s`'\")]+", "[SKILL_PATH]"),
    (r"/Users/omrilorch/operator-kit[^\s`'\")]*", "[SKILL_PATH]"),
    # named artefacts unique to one contender
    (r"\bDESIGN[- ]TARGETS(\.md)?\b", "[TARGETS_DOC]"),
    (r"\bLESSONS(\.md)?\b", "[LESSONS_DOC]"),
    (r"\bCONTEXT\.md\b", "[CONTEXT_DOC]"),
    # skill names (word-boundary, case-insensitive)
    (r"\bdesign-tools/[\w-]+", "[SKILL]"),
    (r"\bengineering-tools/[\w-]+", "[SKILL]"),
    (r"\bmeta-tools/[\w-]+", "[SKILL]"),
    (r"\bux-reviewer\b", "[SKILL]"),
    (r"\bux-creator\b", "[SKILL]"),
    (r"\bux-review\b", "[SKILL]"),
    (r"\bdesign-critique\b", "[SKILL]"),
    (r"\bdesign-handoff\b", "[SKILL]"),
    (r"\baccessibility-review\b", "[SKILL]"),
    (r"\buser-research\b", "[SKILL]"),
    (r"\bux-copy\b", "[SKILL]"),
    (r"\bresearch-synthesis\b", "[SKILL]"),
    (r"\bdesign-system\b(?!\s+(token|colou?r))", "[SKILL]"),
    (r"\btest-driven-development\b", "[SKILL]"),
    (r"\bsystematic-debugging\b", "[SKILL]"),
    (r"\bdiagnosing-bugs\b", "[SKILL]"),
    (r"\bprd-partner\b", "[SKILL]"),
    (r"\bsuperpowers\b", "[SKILL_PACK]"),
    (r"\boperator[- ]kit\b", "[SKILL_PACK]"),
    (r"\bUX-Agent\b", "[SKILL_PACK]"),
    # the kit's house-style tell, present on both sides but named after the repo
    (r"\bproject CLAUDE\.md\b", "[PROJECT_RULES]"),
    (r"\bCLAUDE\.md\b", "[PROJECT_RULES]"),
]

LEAK_CHECK = re.compile(
    r"design-tools|engineering-tools|meta-tools|ux-reviewer|ux-creator|ux-review|"
    r"design-critique|design-handoff|accessibility-review|ux-copy|"
    r"test-driven-development|systematic-debugging|diagnosing-bugs|prd-partner|"
    r"superpowers|operator-kit|UX-Agent|DESIGN-TARGETS|omrilorch",
    re.I)

def scrub(text):
    for pat, rep in RULES:
        text = re.sub(pat, rep, text, flags=re.I)
    return text

def main(workspace):
    ws = pathlib.Path(workspace)
    out_root = ws / "_blind"
    report = []
    for src in sorted(ws.glob("eval-*/[AB]/outputs/output.md")):
        if "CONTAMINATED" in str(src): continue
        side = src.parts[-3]          # A or B
        ev   = src.parts[-4]          # eval-N
        dst  = out_root / ev / f"{side}.md"
        dst.parent.mkdir(parents=True, exist_ok=True)
        cleaned = scrub(src.read_text())
        dst.write_text(cleaned)
        leaks = sorted(set(m.group(0) for m in LEAK_CHECK.finditer(cleaned)))
        report.append((str(dst.relative_to(ws)), len(cleaned.splitlines()), leaks))
    ok = True
    for path, lines, leaks in report:
        status = "clean" if not leaks else f"LEAKS: {leaks}"
        if leaks: ok = False
        print(f"  {path:<24} {lines:>4} lines  {status}")
    print("\nALL CLEAN" if ok else "\nLEAKS REMAIN — fix RULES before comparing")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
