# 0001 — The kit was built, not used

**Date:** 2026-09-12
**Status:** evidence gathered; the decision it feeds is still yours

## Context

Before designing lessons I audited which skills have ever received individual attention,
to decide what fluency should even cover.

## What the evidence shows

Across the repo's 35 commits:

| Signal | Value |
|---|---|
| Active skills | 141 |
| Skills with a **focused** commit (one touching ≤3 skills) | **7** — and one of those is today's |
| Bulk commits (≥10 skills at once) | 9 of 35 |
| Skills ever retired to `_deprecated/` | 2 |
| `_incubator/` | empty |
| Skills named in your own Quick Start table | ~24 |

The seven with focused work: `prd-partner`, `context-management`, `grilling`,
`security-guidance`, `install-operator-kit`, `linx-advisor` (since moved out), and
`writing-great-skills`.

Everything else arrived in a bulk import and was never individually touched again.

## Two corroborating findings from the same audit

1. **Six skills were unreachable and nobody noticed.** Five `pm-agents` components and
   `product-strategy-session` were missing from the routing table — which, per
   `LIFECYCLE.md`, means Claude had no way to reach them at all. Fixed in PR #2.
2. **Nine cross-references pointed at packs deleted in March.** `dean-peters/…` and
   `compound-pm/…` survived six months inside `description:` frontmatter, steering
   invocation at directories that do not exist. Fixed in the same PR.

Both are rot that only survives where nobody walks the path.

## The lesson

**A kit's size is not its capability.** 141 skills where ~24 are claimed drivers and 7
show any sign of iteration is not a large toolkit; it is a small one inside a large
index. And the index has a cost `CLAUDE.md` names itself: competing near-identical
descriptions make the wrong skill fire.

## What this does *not* prove

Editing history is not usage history. A skill can be excellent, used often, and never
need a commit. So **the audit produces candidates, not verdicts.**

There is a second, worse flaw, and Omri caught it rather than me: **the kit is installed
globally and used across repos.** This repo's git history was never going to show usage,
because the usage does not happen here. Measuring a cross-repo tool by one repo's commits
was the wrong instrument for the question.

## Correction — the usage data does exist (2026-09-12)

Claude Code writes a JSONL transcript per session under
`~/.claude/projects/<encoded-working-dir>/`, **one directory per working directory**, so
the store spans every repo at once. Each invocation appears as a `Skill` tool_use record
naming the skill.

[`scripts/skill-usage.py`](../../scripts/skill-usage.py) scans them all and cross-
references the kit's 141 skills. It must run on the machine the work happens on —
transcripts are local.

Its zeros still are not verdicts: transcripts rotate, a skill invoked by another skill
leaves no record, and knowledge applied from memory leaves none either. But "no record of
use across every repo, over 90 days" is a far stronger candidate signal than "no focused
commit", and it is the right instrument.

Pruning still follows the lessons — the script narrows the field; working through what
survives is what converts a candidate into a decision.

## Revisit when

You can answer "which of these have I run?" for a pack. At that point bucket the rest to
`_incubator/` (not `_deprecated/` — that is for retirement with a named successor, per
`LIFECYCLE.md` rule 3).
