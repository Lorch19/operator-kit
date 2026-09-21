# 0008 — The fork inventory is 29, not 11, and 19 of them are not quality questions

**Date:** 2026-09-21 · **Status:** measured mechanically. Reproduce with `scripts/fork-census.py`.

## What record 0003 had

0003 found **11** skills duplicated by name between the kit and the claude.ai synced
store, and treated them as one undifferentiated problem: *"the forks have diverged, and
the default winner is arbitrary."*

## What a full census finds

Comparing every `SKILL.md` across all five roots that hold installed skills — the kit,
`~/.claude/skills`, the claude.ai synced store, superpowers, and `~/UX-Agent` — and
hashing the **body separately from the frontmatter**:

| Category | Count | Meaning |
|---|---|---|
| **True fork** — body differs | **9** | Content has genuinely diverged |
| **Description-only** — body byte-identical | **19** | Same instructions, different trigger text |
| **Identical** | **1** | `web-artifacts-builder` |
| **Total duplicated names** | **29** | |

### The 9 true forks
`doc-coauthoring` · `docx` · `pdf` · `pptx` · `prd-partner` · `product-manager-toolkit` ·
`skill-creator` · `strategy-craft` · `xlsx`

### The 19 description-only duplicates
Almost the whole of two packs:

- **12 of `pm-agents`** duplicated in `compound-pm` — `analytical-thinking`,
  `behavioral-design`, `growth-systems`, `metrics-design`, `opportunity-evaluation`,
  `pm-operating-system`, `product-riff`, `simulation`, `solution-creativity`,
  `spec-review`, `stakeholder-buyin`, `vision-narrative`
- **5 of `domain-tools`** duplicated in `alireza` — `competitive-teardown`,
  `financial-analyst`, `marketing-demand-acquisition`, `marketing-strategy-pmm`,
  `revenue-operations`
- plus `ceo-advisor` and `product-strategist` (synced+user)

## Why the distinction matters more than the count

**A bake-off on a description-only duplicate is impossible in principle.** Identical
bodies produce identical instructions, so both copies do the same work. Running a blind
comparison would measure sampling noise. The only live question is which description wins
routing — which is measured by the method in [[0006-routing-not-invocation]], not by
comparing outputs.

That retires a chunk of the README's backlog without running anything: **19 of the "9
further forks" plus their kin need no contest.** Only the 9 true forks can have one, and
two are already settled — `prd-partner` (this branch) and `skill-creator`, where 0003
established the account runs the pre-split 485-line version against the kit's 253L.

## What this says about the packs

`pm-agents` is, in body, `compound-pm`. `domain-tools` is substantially `alireza`. Both
duplicate sets are installed simultaneously and both are model-invoked, so for every one
of those 17 skills two descriptions compete for the same queries and the loser is dead
weight in the context budget.

Record 0002 measured `pm-agents` at 2 invocations and `domain-tools` at 1 across 90 days.
Those counts were read as disuse. They are at least partly **self-competition** — the same
instructions reachable under two names, with the invocation split between them and the
transcript unable to say which copy fired. This is the same ambiguity 0003 flagged for the
11 synced duplicates, on a set nearly three times larger.

## Recommended, not done

- The 19 description-only duplicates can be resolved by deleting one copy of each — no
  content review needed, because the content is identical. That is 19 skills of context
  budget for zero capability loss. **It is still a deletion, and it is Omri's call.**
- None of the 29 is in the 17-skill promoted cohort, so resolving them would not
  contaminate the invocation experiment. Checked against `LIFECYCLE.md`'s cohort list.
- `prd-partner`: surviving position-controlled verdicts favour the **claude.ai 428L copy
  2-0**, but two of four voided, so n=2. Too thin to overwrite a 466-line file on.
  Recorded as direction, not decision.

## Reproduce

```bash
python3 scripts/fork-census.py
```
Note it must follow symlinks — `ux-reviewer` and `ux-creator` are symlinks into
`~/UX-Agent`, and an earlier version of this measurement silently omitted both.
