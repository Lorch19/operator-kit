#!/usr/bin/env python3
"""Enforce the Operator Kit lifecycle rules. See LIFECYCLE.md.

Usage:  python3 scripts/validate-kit.py [--quiet]
Exits non-zero on any violation.
"""
import glob
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUCKETS = ("_incubator", "_deprecated")

# Model-invoked skills, with the clause of the rule that earns each one its place.
# [A] deliverable trigger  [B] called by another skill  [C] agent notices first
JUSTIFIED = {
    "docx": "A", "pptx": "A", "xlsx": "A", "pdf": "A",
    "ab-test-analysis": "A", "sql-queries": "A", "cohort-analysis": "A",
    "doc-coauthoring": "A", "web-artifacts-builder": "A",
    "grilling": "B", "research": "B", "tdd": "B", "prototype": "B",
    "domain-modeling": "B", "codebase-design": "B",
    "workshop-facilitation": "B", "finance-metrics-quickref": "B",
    "webapp-testing": "B",
    "diagnosing-bugs": "C", "incident-response": "C", "security-guidance": "C",
    "frontend-design": "C", "skill-creator": "C", "prd-partner": "C",
}
JUSTIFIED_PREFIX = ("pm-agents/",)  # components the /pm: commands pull in mid-run


def frontmatter(text):
    if not text.startswith("---"):
        return None
    return text.split("---", 2)[1]


def main():
    quiet = "--quiet" in sys.argv
    os.chdir(ROOT)
    errors, warnings = [], []
    names = defaultdict(list)
    routing = open("CLAUDE.md").read()

    active = bucketed = model = user = 0

    for path in sorted(glob.glob("**/SKILL.md", recursive=True)):
        d = os.path.dirname(path)
        in_bucket = d.startswith(BUCKETS)
        text = open(path).read()
        fm = frontmatter(text)
        if fm is None:
            errors.append(f"{path}: no YAML frontmatter")
            continue

        m = re.search(r"^name:\s*(.+)$", fm, re.M)
        if not m:
            errors.append(f"{path}: frontmatter has no `name:`")
            continue
        name = m.group(1).strip()
        names[name].append(path)

        if not re.search(r"^description:\s*\S", fm, re.M):
            errors.append(f"{path}: frontmatter has no `description:`")

        user_invoked = bool(re.search(r"^disable-model-invocation:\s*true\s*$", fm, re.M))
        listed = name in routing

        if in_bucket:
            bucketed += 1
            # Rule 2: bucketed skills can never fire on their own.
            if not user_invoked:
                errors.append(
                    f"{path}: in {d.split('/')[0]}/ but missing "
                    f"`disable-model-invocation: true` (LIFECYCLE rule 2)")
            # Rule 1: bucketed skills must not be routed to.
            if listed:
                errors.append(
                    f"{path}: `{name}` is in a bucket but still appears in the "
                    f"CLAUDE.md routing table (LIFECYCLE rule 1)")
            # Rule 3: a retirement names its replacement.
            if d.startswith("_deprecated") and "**DEPRECATED**" not in text:
                errors.append(
                    f"{path}: no DEPRECATED banner naming what supersedes it "
                    f"(LIFECYCLE rule 3)")
            continue

        active += 1
        # Rule 1: every promoted skill is reachable from the routing table.
        if not listed:
            errors.append(
                f"{path}: `{name}` is not in the CLAUDE.md routing table "
                f"(LIFECYCLE rule 1) — a user-invoked skill nobody can find is lost")

        if user_invoked:
            user += 1
        else:
            model += 1
            base = os.path.basename(d)
            if base not in JUSTIFIED and not d.startswith(JUSTIFIED_PREFIX):
                errors.append(
                    f"{path}: `{name}` is model-invoked but not justified under the "
                    f"invocation rule — add it to JUSTIFIED with its [A]/[B]/[C] "
                    f"clause, or set `disable-model-invocation: true`")

    # Rule 4: names are unique repo-wide.
    for name, paths in sorted(names.items()):
        if len(paths) > 1:
            errors.append(f"duplicate skill name `{name}`: {', '.join(paths)}")

    # Context budget, reported not enforced.
    budget = 0
    for path in glob.glob("**/SKILL.md", recursive=True):
        if path.startswith(BUCKETS):
            continue
        fm = frontmatter(open(path).read()) or ""
        if re.search(r"^disable-model-invocation:\s*true\s*$", fm, re.M):
            continue
        dm = re.search(r"^description:\s*(.*(?:\n[ \t]+.*)*)", fm, re.M)
        budget += len(dm.group(1).replace("\n", " ").strip()) if dm else 0

    if not quiet:
        print(f"active: {active}  ({model} model-invoked, {user} user-invoked)")
        print(f"bucketed: {bucketed}")
        print(f"description context budget: ~{budget // 4} tokens")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"FAIL  {e}")
    if errors:
        print(f"\n{len(errors)} violation(s). See LIFECYCLE.md.")
        return 1
    if not quiet:
        print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
