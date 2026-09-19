# 0007 — A blind verdict flipped when the outputs swapped places

**Date:** 2026-09-19 · **Status:** measured, n=3 swap tests. One flip observed.

## What happened

The last two bake-offs ran the same harness as `23fc9d2`. In the ideation contest the
randomiser independently drew the same assignment three times — the substitute sat in
slot A in all three evals (p = 1/8). That makes blind position perfectly correlated with
contender identity, so a judge with a position preference would be indistinguishable
from a real quality difference.

Three swap tests: identical files, identical briefs, positions exchanged.

| Eval | Original | Swapped | Held? |
|---|---|---|---|
| 1 | kit (slot B) | kit (slot A) | **held** |
| 2 | kit (slot B) | substitute (slot B) | **FLIPPED** |
| 3 | substitute (slot A) | substitute (slot B) | **held** |

Eval 2 flipped. **Both runs picked slot B**, on the same two documents.

## Why the flip is informative rather than just noise

The two judges did not disagree about the facts. Both independently recorded that the
*substitute's* output was the only one diagnosing the user's stated fixation ("I keep
landing on 'add search'... can't get past it"). They weighted it differently:

- Original: evaluation apparatus, metrics and stress test outweigh the fixation miss.
- Swapped: candidate distinctness plus the fixation diagnosis carry it.

Same evidence, opposite conclusion, both landing on B. On a genuinely close call the
rubric does not determine the winner; the weighting does, and the weighting is unstable.

Corroborating instability: in eval 3 the *same losing document* scored 6.9 in one run and
8.3 in the other — a 1.4-point swing on identical text.

## Consequences

**1. Score precision is lower than the numbers imply.** Differences under ~1 point should
be read as "no measured difference", not as a narrow win. Several verdicts across all five
contests fall inside that band.

**2. The three earlier contests carry untested risk.** Design, engineering and prd-partner
(`23fc9d2`) were each decided by a single unswapped comparison. Close calls there —
7.6/8.8, 8.7/9.3, 8.9/9.5, 8.9/9.5 — sit exactly in the unstable band. No evidence says
they flipped; no evidence says they did not. Their splits may be softer than reported.

**3. Position control belongs in the harness, not in luck.** Randomising assignment is not
enough: it can draw degenerate. Either force a balanced assignment, or run every
comparison twice with positions exchanged and treat disagreement as a void.

## What the two contests actually found

| Contest | Result | Position control |
|---|---|---|
| `meta-tools/writing-great-skills` vs `superpowers/writing-skills` | **kit 3-0** (8.0/9.0, 9.8/8.7, 9.2/8.3) | self-controlled: kit won from slot B once and slot A twice |
| `pm-agents` ideation vs `superpowers/brainstorming` | kit 1, substitute 1, **1 void** | all three swap-tested |

The writing sweep is the kit's only clean win across five contests. It is also the largest
underdog on paper — 102 lines against 679 — so it is not winning on coverage. In all three
evals the deciding factor was executable correctness: the comparators ran the shell
commands both sides shipped. The substitute's transcript-harvest `jq` filter **exits 0
while silently dropping 76% of matching prompts**, returning machine-authored SDK prompts
instead of the typed ones it claims to extract. That is the proxy trap in its purest form —
a command that looks like it worked.

## Two findings outside the verdicts

**A third fork, unrecorded.** `product-riff` and `solution-creativity` each exist twice:
the kit's copies and `compound-pm`'s in `~/.claude/skills`. The **bodies are byte-identical**;
only the descriptions differ. Record 0003 catalogued 11 name-duplicates against the synced
claude.ai store — these two are not on that list, so the fork count is higher than recorded.
For this pair, quality transfers to both copies automatically and the only live question is
which description wins routing.

**`product-riff` was never tested.** Both kit runs read it, judged it out of scope (it is
scoped to analysing someone else's announcement) and used `solution-creativity` instead.
The ideation contest was therefore `solution-creativity` vs `brainstorming`. `product-riff`
has no verdict. Worth noting that the pack self-routed correctly under pressure.

**Also unlike the design contest:** both kit ideation skills were already model-invoked.
Their zero usage against `brainstorming`'s 3 cannot be blamed on invocation mode — both
sides were reachable and in context.

## Harness defect found and not yet fixed

`sanitize.py` replaces identities with bracketed tokens like `[SKILL]`, which read as
visible redaction markers. One comparator scored such a token as author sloppiness. It did
not change an outcome — in both affected evals the side carrying *more* placeholders won
anyway, so the bias ran against the eventual winner — but the fix is to substitute natural
language ("the method") rather than bracketed tokens. Better still, the source-level
instruction used in these two contests (tell the agent to put its skill name only in a
sidecar file) prevented the leak entirely; the sanitizer should be a silent net behind it.

## Not done

No skill bucketed, moved, reworded, or re-moded. `validate-kit.py`: 141 active,
54 model-invoked, 87 user-invoked. See [[0006-routing-not-invocation]] for why
`design-critique` must be scored per-skill on 2026-10-15.
