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
need a commit. There is no telemetry in this repo, so **the audit produces candidates,
not verdicts.** The one input that would settle it — which skills you have actually run —
only you have.

That is why pruning follows the lessons rather than preceding them: working through the
kit is what converts a candidate into a decision.

## Revisit when

You can answer "which of these have I run?" for a pack. At that point bucket the rest to
`_incubator/` (not `_deprecated/` — that is for retirement with a named successor, per
`LIFECYCLE.md` rule 3).
