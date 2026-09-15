# 0005 — The invocation experiment

**Started:** 2026-09-15 · **Re-measure:** 2026-10-15 · **Status:** running

Pre-registered before the data exists, so the result cannot be rationalised afterwards.

## Hypothesis

Record 0003 measured, over the same 90 days: **model-invoked skills used 13.5%,
user-invoked 3.8%** (conservatively 10.3% vs 3.0%). If invocation mode is *causing* the
disuse rather than merely correlating with it, restoring model-invocation should raise
usage of the restored skills — and leave the rest where they are.

The rival explanation is selection: `LIFECYCLE.md` chose the model-invoked set for being
deliverable-triggers and primitives, so they may simply be the more useful skills.

## Design

**Cohort (17, promoted).** Selection rule, applied mechanically rather than by judgement:
*the skill's own description contains an explicit `TRIGGER with "..."` list.* Such a skill
was **authored** to fire on a named output and was bulk-switched to user-invoked by the
2026-07-27 policy commit — its trigger list has been inert ever since. All 17 are
therefore clause [A].

| Pack | Promoted |
|---|---|
| design-tools | `accessibility-review` `design-critique` `user-research` `ux-copy` |
| engineering-tools | `documentation` `system-design` `tech-debt` `testing-strategy` |
| sales-tools | `account-research` `call-prep` `competitive-intelligence` `daily-briefing` `draft-outreach` |
| operations-tools | `compliance-tracking` `process-optimization` `risk-assessment` |
| meta-tools | `internal-comms` |

**Excluded on purpose:** `code-review` met the rule but deliberately shadows Claude Code's
bundled `/code-review`, and Omri had just chosen to leave its invocation alone. Promoting
it would have made two skills compete and muddied the result.

**Control (87).** Every other user-invoked skill, untouched.

**Cost.** 37 → 54 model-invoked; description budget 3019 → 3978 tokens. Pre-policy was
~11.5K, so this buys the experiment at roughly a third of what the policy saved.

## Baseline (90 days to 2026-09-12, 129 sessions)

All 17 cohort members: **zero invocations.** Every pack they come from was at zero.

## The decisive sub-test

The cohort is sales-, ops- and engineering-heavy — packs Omri may simply not work in. A
zero there after 30 days means *role*, not invocation, and proves nothing.

**`design-tools` is the sharp test.** He demonstrably does this work: `ux-reviewer`,
`ux-creator` and `ux-review` were invoked **31 times across up to 10 repos** in the same
window while all seven `design-tools` skills sat at zero. The work exists; only the kit's
version never fired.

Pre-registered readings:

| Outcome on 2026-10-15 | Conclusion |
|---|---|
| design-tools cohort fires ≥3 times | **Invocation was the cause.** Promote more of the control, on the same rule. |
| Still zero, `ux-*` still firing | Invocation is not the blocker — the substitutes are simply better. The bake-off decides, and `design-tools` goes. |
| Both fire | Genuine overlap. Pick one deliberately; two skills competing is the failure state. |
| Everything still zero, `ux-*` too | Measurement or window problem, not a skill problem. Check `SESSIONS` before concluding anything. |

## How to re-measure

```bash
python3 scripts/skill-usage.py --days 30        # on Omri's machine, not a remote session
```

Compare cohort usage against control usage over the same window. Absolute counts will be
small; the comparison is what carries the signal.

## Threats to validity

- **Thirty days is short** and 17 skills is a small cohort. A null result is weak evidence,
  a positive result is strong — the asymmetry is worth remembering when reading it.
- **Not randomised.** The cohort is skills that declared TRIGGER lists, which likely
  correlates with being written by Anthropic's knowledge-work-plugins authors — plausibly
  better-written than average. This is the same selection confound as 0003, narrowed but
  not removed. Only the design-tools sub-test escapes it, because there the competing
  substitute is already measured.
- **Observation may change behaviour.** Omri now knows which skills were promoted.
- **Transcripts rotate.** Confirm `SESSIONS` looks sane before reading anything into the
  counts.
- **A surface change would invalidate this outright.** (Raised 2026-09-15, while the
  experiment was running.) `skill-usage.py` reads `~/.claude/projects/*.jsonl` — Claude
  **Code** transcripts, the format verified directly. Work done on a surface that does not
  write there is invisible to it. If Omri's usage moves to the Claude desktop chat app, or
  claude.ai, or Cowork, the promoted cohort will read as "still not firing" when the truth
  is "the work moved" — and that points at exactly the wrong conclusion, since a false null
  here exonerates nothing and condemns 17 skills that were never given their chance.

  **Check this first on 2026-10-15**, before reading any counts: ask which surfaces were
  used over the window. If a meaningful share of the work happened outside Claude Code,
  the result is *unreadable*, not negative — extend the window rather than concluding.
  Whether the chat desktop app records invocations anywhere comparable has **not been
  verified**; find out before relying on either answer.

## If it confirms

Promote the rest of the control on the same rule, in batches, re-measuring each time.
Do not promote all 87 — the point of the policy was real, and the finding is that it was
priced on one side only.

## If it refutes

Invocation is exonerated and the 6% is about fit, not reach. Then the prune proceeds on
the evidence 0002 already gathered, and the bake-offs settle the contested pairs.
