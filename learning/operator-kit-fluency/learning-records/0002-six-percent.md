# 0002 — 6%

**Date:** 2026-09-12
**Status:** measured, not inferred. This one is evidence, not a proxy.

## The measurement

129 sessions, all within 90 days, scanned across every repo via
`~/.claude/projects/*/*.jsonl`.

| | |
|---|---|
| Operator Kit skills invoked | **9 of 141 — 6%** |
| Never invoked in 90 days | **132** |
| Share of all skill invocations going to the kit | **31 of 143 — 22%** |
| Packs with **zero** invocations | **9 of 15** |

The nine that live:

| Uses | Repos | Skill | Pack |
|---|---|---|---|
| 11 | 2 | `prd-partner` | prd-partner |
| 8 | 2 | `grilling` | thinking-tools |
| 3 | 1 | `press-release` | pm-frameworks |
| 2 | 2 | `research` | thinking-tools |
| 2 | 1 | `altitude-horizon-framework` | pm-frameworks |
| 2 | 1 | `strategy-craft` | pm-agents |
| 1 | 1 | `jobs-to-be-done` | pm-frameworks |
| 1 | 1 | `skill-creator` | meta-tools |
| 1 | 1 | `competitive-teardown` | domain-tools |

Nine packs with no invocation at all: `engineering-tools` (20 skills),
`operations-tools` (9), `sales-tools` (9), `design-tools` (7), `document-tools` (4),
`analytics-tools` (3), `gtm-tools` (3), `context-management` (1), `doc-coauthoring` (1).
**57 skills in packs that have never once fired.** `pm-frameworks` is 3 of 43.

## The finding that matters more than the percentage

The kit is not losing to *nothing*. It is losing to **substitutes already installed**:

| Used instead | Uses | Repos | Kit equivalent | Kit uses |
|---|---|---|---|---|
| `ux-reviewer` + `ux-creator` + `ux-review` | **31** | up to 10 | all 7 of `design-tools` | **0** |
| `test-driven-development` | 3 | 3 | `engineering-tools/tdd` | 0 |
| `systematic-debugging` | 3 | 2 | `engineering-tools/diagnosing-bugs` | 0 |
| `brainstorming` | 3 | 3 | `pm-agents/product-riff`, `solution-creativity` | 0 |
| `writing-skills` | 2 | 1 | `meta-tools/writing-great-skills` | 0 |

The UX trio alone was invoked **31 times — exactly matching the entire Operator Kit's
31 invocations**, while the kit's seven-skill design pack sat untouched.

And the single most-used skill on the machine, `michael` (22 uses across 11 repos), isn't
in the kit either. A working toolkit exists; it just isn't this one.

## Correction to record 0001, and to my own reasoning

In 0001 I proposed pruning by pack, then **retracted it** on the grounds that 12 of 15
packs appear in the Quick Start "Top 15 Daily Drivers" table.

That retraction was wrong, and the error is instructive: **I treated a self-reported list
as evidence.** The Quick Start table names `sales-tools/call-prep`,
`design-tools/design-critique`, `operations-tools/status-report` and others as daily
drivers. None has been invoked once in 90 days. The table is aspirational — a description
of the kit its author hoped to use.

Pack-level pruning was right the first time. Measurement says so; the self-report said
otherwise; the self-report lost.

## Hypothesis, explicitly unproven

The `Add invocation policy and bucket lifecycle` commit (2026-07-27) made 104 skills
user-invoked, stripping their descriptions from context to save ~8K tokens. A
user-invoked skill fires **only when recalled by name**. Every substitute above may well
be model-invoked — firing on its own while the kit's equivalent waits to be remembered.

If that holds, the disuse is not a discovery problem that fluency fixes. It is the
invocation policy working exactly as designed, with a cost nobody priced.

**Not tested.** 31 invocations across 9 skills is too small to split before/after the
commit without generating noise. The cheap check is whether the substitutes carry
descriptions; that requires looking at plugins outside this repo.

## What follows

1. **Bucket the 9 dead packs** to `_incubator/` — 57 skills, no judgement call needed;
   zero uses across 129 sessions and 90 days is not ambiguous.
2. **Resolve each substitution deliberately.** For every pair above, one should win. The
   kit's version is not automatically the loser — but it is currently losing by default,
   which is the worst of both.
3. **Settle the invocation question before pruning `pm-frameworks`.** If user-invocation
   is what killed usage, deleting 40 unused frameworks removes the evidence before the
   cause is understood.
4. **Retarget the lessons.** Lesson 01 drilled competitive and marketing near-neighbours —
   both in packs with zero usage. Lesson 02 should cover what actually gets used:
   `prd-partner`, `grilling`, `research`, and the substitution decisions above.
