# 0007 — A blind verdict flipped when the outputs swapped places

**Date:** 2026-09-19 · **Updated:** 2026-09-20 with all 17 verdicts swap-tested.
**Status:** measured. **6 of 17 verdicts flipped (35%).**

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


---

# Update 2026-09-20 — all 17 verdicts swap-tested

Every verdict across all five contests was re-judged with the two documents in
exchanged positions, same brief, same expectations. Rule fixed in advance: a verdict
that changes when the documents change places is **void**, applied uniformly.

**6 of 17 flipped — 35%.**

| Contest | As first reported | Position-controlled |
|---|---|---|
| design | 2-2 split | **2-2 split — all four held** |
| engineering | "2-1 to superpowers" | **kit 1, 2 void** — inverted |
| prd-partner fork | "2-2, neither better" | **synced 2, kit 0, 2 void** |
| writing | "kit 3-0 sweep" | **kit 2, 1 void** |
| ideation | kit 2-1 | kit 1, sub 1, 1 void |

Surviving verdicts across everything: **kit 6, substitutes/synced 5, void 6.**

## Three claims I made in-session that the swaps refuted

1. **"Engineering goes 2-1 to superpowers."** Both substitute wins were slot artifacts.
   The kit's single win is the best-evidenced verdict in the exercise — mutation test,
   refactor test, and an independent re-derivation of the refactor test from the
   opposite position all agree.
2. **"The prd fork is a dead heat, neither version better."** Both kit wins voided; the
   two surviving verdicts favour the **claude.ai synced 428L copy**.
3. **"Writing is a clean 3-0 sweep."** Eval 1 flipped. It is 2-0 with a void.

## Why the tests were run on everything, not the close ones

6 of 11 original verdicts sat under a 1.0 margin, and **4 of those 6 favoured the
substitute**. In design and engineering specifically, every kit win was wide (1.9, 1.5,
2.5) and every substitute win was narrow (0.6, 0.3, 0.6, 0.4). Swap-testing only the
fragile set would have been an instrument that could essentially only move one way —
toward the kit — even under a threshold stated in advance.

Testing all of them was the right call on the evidence: **prd eval 3 and eval 4 were kit
wins and both flipped.** The selected set would have missed both.

## What separates a verdict that holds from one that flips

Verdicts backed by something **executed** held. Verdicts backed by **weighting** flipped.

- Engineering eval 2 held and hardened: the swap judge independently re-derived the
  behaviour-preserving refactor test (13/13 surviving vs 4/12 failing).
- Design eval 2 held: the swap judge **re-rendered both mock files** and reproduced the
  measurements exactly — interior band 3.1%, trailing bands 37.3%/59.8-65.6%, the
  3.28:1 boundary, 0 text runs below AA, 0 targets under 44px.
- Ideation eval 2 flipped: both judges recorded the *same* fact — only one side
  diagnosed the user's stated fixation — and weighted it oppositely.

Corroborating instability: the same losing document scored 6.9 and 8.3 across two runs
of identical text.

## Standing rules this produces

1. **A single blind comparison is not a result.** 35% of them do not survive a swap.
   Every verdict needs both positions before it can be cited.
2. **Sub-1-point margins are no measured difference**, not narrow wins.
3. **Comparators must execute what they judge.** Every verdict that held was anchored in
   something run; the defects that decided them — a `jq` filter exiting 0 while dropping
   76% of its population, a glob matching nothing under zsh, a `ledger.py` that fails to
   import standalone, an `order-bisect.sh` that crashes on bash 3.2, a focus ring
   presented at 4.25:1 that is really 3.02:1 — were all found by running, never by reading.
4. **Balance the assignment in the harness.** The ideation randomiser drew the same
   side three times (p=1/8), which is how this was noticed at all.

## What it does NOT change

No skill is retired on this evidence. Six voids and a near-even split across surviving
verdicts is weaker support for pruning than the pre-swap numbers looked, not stronger.
`design-tools` in particular came through fully controlled at 2-2 — a genuine quality
tie against the substitute that has 31 invocations to its 0.

See [[0006-routing-not-invocation]]: `design-critique` cannot win routing in any
invocation mode, so score that cohort per-skill on 2026-10-15, not as a block.
