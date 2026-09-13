# 0003 — Invocation, not discovery, is what suppresses usage

**Date:** 2026-09-13
**Status:** measured. The hypothesis in 0002 now has evidence; a confound is stated and unresolved.

## The test

0002 hypothesised that the 2026-07-27 invocation policy — which made 104 of 141 skills
user-invoked, stripping their descriptions from context — was what killed usage. Splitting
usage before/after that date would have been noise. Splitting by **invocation mode**
across the same 90 days is not.

| | Used | Pool | Rate | Invocations |
|---|---|---|---|---|
| Model-invoked | 5 | 37 | **13.5%** | 24 |
| User-invoked | 4 | 104 | **3.8%** | 7 |

Per skill that is ~10× the invocation volume. Conservatively — dropping the three names
that exist in both the kit and the synced account skills, where the transcript cannot say
which copy fired:

| | Used | Pool | Rate |
|---|---|---|---|
| Model-invoked | 3 | 29 | **10.3%** |
| User-invoked | 3 | 101 | **3.0%** |

Still 3.4×, on the measurement that cannot be gamed by the duplicate ambiguity.

## The confound, stated plainly

**The model-invoked set is not a random sample.** `LIFECYCLE.md` selected it deliberately:
[A] deliverable triggers, [B] primitives other skills call, [C] things the agent notices
first. Those are, by construction, the skills most likely to come up. Some of the gap is
selection, not causation.

What the confound cannot explain is the *floor*: 101 user-invoked skills produced **6
invocations in 90 days across 129 sessions**. Whatever their quality, they are not
reaching the work.

## The discovery that reframes the prune

The account's claude.ai-synced skills are installed alongside the kit — **22 of them, all
model-invoked** — and **11 duplicate an Operator Kit skill by name**:

`competitive-teardown` · `doc-coauthoring` · `docx` · `marketing-strategy-pmm` · `pdf` ·
`pptx` · `prd-partner` · `product-manager-toolkit` · `skill-creator` ·
`web-artifacts-builder` · `xlsx`

Two consequences:

**1. Some "unused" packs are shadowed, not unwanted.** All four `document-tools` skills
and `doc-coauthoring` have model-invoked synced twins. Their zero usage does not mean
"Omri doesn't make documents" — it means the twin fires first. 0002's prune list treated
these as dead work. Wrong reason; the pack may still go, but as *redundancy*, not disuse.

**2. The forks have diverged, and the default winner is arbitrary.** Every duplicate pair
differs except `web-artifacts-builder`:

| Skill | Kit | Synced |
|---|---|---|
| `docx` | 595L | 91L |
| `xlsx` | 296L | 99L |
| `product-manager-toolkit` | 131L | 504L |
| `skill-creator` | 253L | 485L |
| `prd-partner` | 466L | 428L |

`skill-creator` is diagnostic. `BACKLOG.md` records: *"Split skill-creator into SKILL.md +
references — Done. 486→246 lines."* The kit's copy is 253L; the synced copy is 485L. **The
account is running the pre-split version** — the work was done and never reached the copy
that actually fires.

Eleven skills exist in two versions, and the model-invoked one wins by default whether or
not it is the better one.

## What this changes

0002 recommended bucketing 9 dead packs. That is still broadly right, but the reasoning
was too coarse. Three distinct causes need three different actions:

| Cause | Packs | Action |
|---|---|---|
| **Shadowed** by a model-invoked twin | `document-tools`, `doc-coauthoring` | Resolve the fork; the loser goes |
| **Suppressed** by user-invocation | most of `pm-frameworks`, `engineering-tools` | Fix invocation *before* judging |
| **Irrelevant** — work not done | unknown until asked | Bucket, no evaluation |

Deleting a suppressed skill destroys the evidence before the cause is fixed. Deleting a
shadowed one is fine — but pick which fork survives first.

## The uncomfortable implication

The invocation policy was adopted to cut description context from ~11.5K to ~3.1K tokens.
It worked. It also correlates with 101 skills producing six invocations in three months.

That trade was never priced, because nothing measured the other side of it. Cheap context
and unreachable skills look identical on every dashboard the kit had — which is the whole
argument for `scripts/skill-usage.py` existing.

Reversing wholesale would restore the context cost. The proportionate move is to promote
back the handful with a genuine [A]/[B]/[C] claim — and let the rest be judged after they
have had a fair chance to fire.
