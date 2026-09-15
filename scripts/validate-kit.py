#!/usr/bin/env python3
"""Enforce the Operator Kit lifecycle rules. See LIFECYCLE.md.

Usage:  python3 scripts/validate-kit.py [--quiet] [--fix]

The routing table in CLAUDE.md is the only index Claude has for the 100+
user-invoked skills, so a skill missing from it is unreachable. `--fix` appends
a row for every promoted skill that lacks one, marked TODO: the tool guarantees
reachability, a human still writes the routing prose.

Exits non-zero on any violation.
"""
import glob
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUCKETS = ("_incubator", "_deprecated")
ROUTING_HEADING = "## Full Routing Table"

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
    # Invocation experiment, 2026-09-15 -> re-measure 2026-10-15.
    # All [A]: each of these declares its own `TRIGGER with "..."` list in its
    # description, i.e. it was authored to fire on a named output and was
    # bulk-switched to user-invoked by the 2026-07-27 policy commit. Measured
    # usage after that: user-invoked 3.8% vs model-invoked 13.5%. The other 87
    # user-invoked skills are the control. See learning-records/0005.
    "accessibility-review": "A", "design-critique": "A", "user-research": "A",
    "ux-copy": "A", "documentation": "A", "system-design": "A",
    "tech-debt": "A", "testing-strategy": "A", "internal-comms": "A",
    "compliance-tracking": "A", "process-optimization": "A", "risk-assessment": "A",
    "account-research": "A", "call-prep": "A", "competitive-intelligence": "A",
    "daily-briefing": "A", "draft-outreach": "A",
}
JUSTIFIED_PREFIX = ("pm-agents/",)  # components the /pm: commands pull in mid-run

# Which routing-table section a pack's skills belong to. Consulted only by --fix
# to place a generated row. Several packs legitimately span sections (most of
# pm-frameworks sits under Product Management, but its market-sizing and pricing
# skills sit elsewhere), so a generated row may need moving by hand.
PACK_SECTION = {
    "thinking-tools": "Thinking Primitives",
    "document-tools": "Documents & Files",
    "doc-coauthoring": "Documents & Files",
    "pm-frameworks": "Product Management",
    "prd-partner": "Product Management",
    "pm-agents": "Multi-Agent Workflows",
    "analytics-tools": "Analytics & Data",
    "gtm-tools": "Go-to-Market",
    "domain-tools": "Financial",
    "operations-tools": "Operations",
    "engineering-tools": "Engineering",
    "sales-tools": "Sales",
    "design-tools": "Design",
    "meta-tools": "Meta / Tooling",
    "context-management": "Meta / Tooling",
}


def frontmatter(text):
    if not text.startswith("---"):
        return None
    return text.split("---", 2)[1]


def description_of(fm):
    """The description value as one line.

    Handles both YAML forms in the kit: block scalars (`>-`, `|`) and quoted
    strings. An unstripped quote ends up in a generated routing phrase.
    """
    m = re.search(r"^description:\s*(.*(?:\n[ \t]+.*)*)", fm, re.M)
    if not m:
        return ""
    body = " ".join(re.sub(r"^[>|][-+]?", "", m.group(1).strip()).split())
    if len(body) > 1 and body[0] == body[-1] and body[0] in "\"'":
        body = body[1:-1].strip()
    return body


def routing_table(text):
    """(start, end, lines) bounding the Full Routing Table, or None if absent.

    Scoping to the table matters: matching a skill name against the whole of
    CLAUDE.md passes any skill merely mentioned in the prose pack listings,
    which is exactly how a skill goes unrouted without anyone noticing.
    """
    lines = text.split("\n")
    start = next((i for i, l in enumerate(lines)
                  if l.startswith(ROUTING_HEADING)), None)
    if start is None:
        return None
    end = next((i for i, l in enumerate(lines[start + 1:], start + 1)
                if l.startswith("## ")), len(lines))
    return start, end, lines


def routed_refs(lines, start, end):
    """{skill basename: [full backticked tokens]} for the table's references.

    A cell may hold several references, a slash command (`/pm:spec`), or a home
    path (`~/linx-advisor/`); only the skill-shaped tokens are collected.
    """
    refs = defaultdict(list)
    for line in lines[start:end]:
        for tok in (t.strip() for t in re.findall(r"`([^`]+)`", line)):
            if tok.startswith(("/", "~")):
                continue
            refs[tok.rstrip("/").split("/")[-1]].append(tok)
    return refs


def draft_phrase(description):
    """A first-draft routing phrase from a description. Sharpened by a human."""
    head = re.split(r"(?<=[.;])\s|\s+Use when\b|\s+DO NOT\b", description)[0]
    head = head.rstrip(" .")
    return head[:68].rstrip() + "…" if len(head) > 68 else head or "describe this skill"


def apply_fix(text, missing):
    """Append a TODO row per missing skill. Returns (new_text, unplaced)."""
    start, end, lines = routing_table(text)
    headers = [(i, m.group(1).strip())
               for i in range(start, end)
               for m in [re.match(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*\|\s*$", lines[i])]
               if m]

    pending, unplaced = defaultdict(list), []
    for name, pack, phrase in missing:
        section = PACK_SECTION.get(pack)
        if section is None or section not in {s for _, s in headers}:
            unplaced.append((name, pack))
            continue
        pending[section].append(f"| TODO — {phrase} | `{pack}/{name}` |")

    # Insert bottom-up so earlier line indices stay valid.
    for idx in range(len(headers) - 1, -1, -1):
        i, section = headers[idx]
        if section not in pending:
            continue
        stop = headers[idx + 1][0] if idx + 1 < len(headers) else end
        while stop > i and not lines[stop - 1].strip():
            stop -= 1
        lines[stop:stop] = pending.pop(section)

    return "\n".join(lines), unplaced


def main():
    quiet = "--quiet" in sys.argv
    fix = "--fix" in sys.argv
    os.chdir(ROOT)
    errors, warnings = [], []
    names = defaultdict(list)

    claude_md = open("CLAUDE.md").read()
    region = routing_table(claude_md)
    if region is None:
        print(f"FAIL  CLAUDE.md has no `{ROUTING_HEADING}` section")
        return 1
    r_start, r_end, r_lines = region
    refs = routed_refs(r_lines, r_start, r_end)

    # A generated row still carrying its marker is reachable but never sharpened.
    # Warn rather than fail: --fix should leave a green tree, and the reminder
    # then survives every run until someone writes a real trigger phrase.
    for i in range(r_start, r_end):
        m = re.match(r"^\|\s*TODO\s*—\s*.*?\|\s*`([^`]+)`", r_lines[i])
        if m:
            warnings.append(
                f"CLAUDE.md:{i + 1}: `{m.group(1)}` still carries a generated TODO "
                f"phrase — rewrite it as a real task trigger")

    active = bucketed = model = user = 0
    missing = []

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
        listed = name in refs

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
            missing.append((name, d.split("/")[0], draft_phrase(description_of(fm))))
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

    # A routed reference that resolves to no skill: a rename or deletion left the
    # table pointing at nothing. Pack directories are legitimate targets.
    for base, tokens in sorted(refs.items()):
        if base in names or any(os.path.isdir(t) for t in tokens):
            continue
        errors.append(
            f"CLAUDE.md routing table: `{tokens[0]}` matches no skill — "
            f"stale row left by a rename or deletion")

    # Context budget, reported not enforced.
    budget = 0
    for path in glob.glob("**/SKILL.md", recursive=True):
        if path.startswith(BUCKETS):
            continue
        fm = frontmatter(open(path).read()) or ""
        if re.search(r"^disable-model-invocation:\s*true\s*$", fm, re.M):
            continue
        budget += len(description_of(fm))

    if fix and missing:
        new_text, unplaced = apply_fix(claude_md, missing)
        open("CLAUDE.md", "w").write(new_text)
        placed = len(missing) - len(unplaced)
        print(f"--fix: added {placed} routing row(s) to CLAUDE.md, each marked TODO.")
        print("       Sharpen the task phrasing and move any row to a better section.")
        for name, pack in unplaced:
            print(f"WARN   no section mapped for pack `{pack}` — add `{name}` by hand")
        errors = [e for e in errors if "not in the CLAUDE.md routing table" not in e]

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
        if any("not in the CLAUDE.md routing table" in e for e in errors):
            print("Run with --fix to generate the missing routing rows.")
        return 1
    if not quiet:
        print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
