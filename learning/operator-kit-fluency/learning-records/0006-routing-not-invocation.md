# 0006 — For design-tools, the blocker is description dominance, not invocation mode

**Date:** 2026-09-18 · **Status:** measured, small sample. Read the caveats.

Written before 2026-10-15 because it changes how record 0005's decisive sub-test
must be read. Nothing was edited as a result; the experiment is untouched.

## What was measured

The bake-off (commit `23fc9d2`) held invocation constant by handing each agent its
skill, so it measured **quality only**. Quality came back a dead heat: design 2-2,
engineering 2-1, prd-partner fork 2-2, with every output passing every stated
expectation in every contest.

That makes quality a settled non-issue and points at the untested variable: **would
the skill fire at all?** So: 162 model-invoked descriptions — every skill that
actually competes in a live session, from operator-kit (54), `~/.claude/skills` (72),
the synced claude.ai store (20), superpowers (14) and `~/UX-Agent` (2) — plus six
realistic queries, routed under two conditions.

## Result

| # | Target | No hook | With hook |
|---|---|---|---|
| 1 | `design-critique` | `ux-reviewer` | `ux-reviewer` |
| 2 | `ux-copy` | **`ux-copy`** | **`ux-copy`** |
| 3 | `accessibility-review` | **`accessibility-review`** | **`accessibility-review`** |
| 4 | `user-research` | **`user-research`** | **`user-research`** |
| 5 | `design-critique` | `ux-reviewer` | `ux-reviewer` |
| 6 | (near-miss, want NONE) | `diagnosing-bugs` | `diagnosing-bugs` |

**Hook changed 0 of 6 outcomes. Hit-rate 3/6 in both conditions.**

## Two findings, one of them a correction

**1. The SessionStart hook is redundant, not causal.** A `SessionStart` hook
(`~/.claude/hooks/ux-reviewer-announce.sh`, registered in `settings.json`) injects a
standing directive to invoke `ux-reviewer` before designing any user-facing surface.
On seeing it I claimed it explained the 31-to-0 gap and would manufacture a false
null on 15 Oct. **The measurement refutes the marginal-effect claim**: `ux-reviewer`
wins those queries on its description alone. The hook's carve-outs (copy tweaks,
backend-only work) held cleanly in both near-miss cases — it is well-scoped. It may
still affect *consistency* or willingness to fire unasked; it does not change *which*
skill is chosen here.

**2. `design-critique` is structurally unroutable.** `ux-reviewer`'s description
claims a strict superset of its surface — "review this design/screen/flow/mock", "is
this the right design", "a flow with more clicks than the job needs". `design-critique`
offers "review this design", "critique this mockup" and no distinguishing claim. As
written it has no query it can win. Promotion to model-invoked did not and cannot fix
this; the competition is decided on description specificity, not mode.

**3. The pack does not fail uniformly.** Three of the four promoted design skills —
`ux-copy`, `accessibility-review`, `user-research` — won their queries cleanly, each
because the description named the artifact literally ("empty states", "color
contrast", "interview guide").

## What this does to 0005's decisive sub-test

0005 pre-registered: design-tools still zero + `ux-*` still firing → *"invocation is
not the blocker — the substitutes are simply better. The bake-off decides, and
design-tools goes."*

Both halves of that inference are now unsafe.

- The bake-off **has** decided, and it says quality is a tie, with design-tools
  holding the two widest winning margins in the exercise (9.3/7.4, 9.5/8.0).
- A zero for `design-critique` specifically carries no information about invocation
  mode, because it cannot win routing in any mode.

A zero for `ux-copy`, `accessibility-review` or `user-research` **is** still
informative — they can win routing, so their zero would mean the work did not come up,
or the mode genuinely does not help.

**Score the design cohort per-skill on 15 Oct, not as a block.**

## Caveats — this is a small measurement

- **Six queries, one routing agent per condition, one run.** No variance estimate. A
  0/6 hook effect is consistent with a small real effect this design cannot detect.
- **Simulated routing, not observed routing.** An agent reasoning over a roster is a
  proxy for the real mechanism. It is a better proxy than counting invocations of a
  skill that cannot fire, but it is still a proxy.
- Both conditions were judged by the same model, which may converge regardless of
  context — an alternative explanation for the null that this design cannot separate.
- Query 6 was meant to be a true negative and was not: two catch-all debugging
  descriptions (`diagnosing-bugs`, `systematic-debugging`) claim it. Same mechanism as
  finding 2, different pack — broad descriptions crowd out precise ones.

## What was deliberately NOT done

No skill bucketed, moved, or reworded. No invocation mode changed. The hook was not
edited. `validate-kit.py`: 141 active, 54 model-invoked, 87 user-invoked — the
cohort/control split 0005 registered.

Rewording `design-critique` would be the obvious fix and is the one thing that must
wait: it would change a cohort member mid-experiment. After 15 Oct.

## Reproduce

```bash
python3 /tmp/claude-501/build_roster.py     # rebuild the 162-skill roster
# then route the queries in /tmp/claude-501/routing/queries.json under both conditions
```
Note: the roster builder must follow symlinks — `ux-reviewer` and `ux-creator` are
symlinks into `~/UX-Agent`, and a first version of this measurement silently omitted
both, which would have handed design-tools a walkover against an absent opponent.
