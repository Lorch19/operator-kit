# Substitution bake-off

Usage measurement (`learning/operator-kit-fluency/learning-records/0002`) found that the
kit is not losing to nothing — it is losing to **substitutes already installed**, and to
**forks of itself** on claude.ai. In both cases the winner is currently decided by
invocation mode, not by quality.

These eval sets settle each contest on output instead.

## What is contested

| Contest | Their uses (90d) | Kit uses | Kind |
|---|---|---|---|
| `design-tools` (7 skills) vs `ux-reviewer` / `ux-creator` / `ux-review` | **31** | 0 | substitute |
| `engineering-tools/tdd` vs `test-driven-development` | 3 | 0 | substitute |
| `engineering-tools/diagnosing-bugs` vs `systematic-debugging` | 3 | 0 | substitute |
| `meta-tools/writing-great-skills` vs `writing-skills` | 2 | 0 | substitute |
| `pm-agents/product-riff` + `solution-creativity` vs `brainstorming` | 3 | 0 | substitute |
| `prd-partner` — kit 466L vs claude.ai 428L | 11 combined | — | **fork** |
| `meta-tools/skill-creator` — kit 253L vs claude.ai 485L | 1 | — | **fork** |
| 9 further forks | — | — | fork |

A **substitute** contest asks which of two different skills to keep. A **fork** contest
asks which version of the same skill should exist in both places — the account copy is
currently stale in at least one confirmed case (`skill-creator` is the pre-split 486-line
version; the split was done in the kit and never synced).

## Running one

These must run on the machine where **both** contestants are installed — the substitutes
live outside this repo. Use `meta-tools/skill-creator`'s blind comparison, which judges
outputs without knowing which skill produced them:

```
/skill-creator
```

then point it at an eval set here and ask for the blind comparison workflow
(`references/eval-workflow.md` → *Advanced: Blind comparison*). It spawns both runs in
parallel, grades with `agents/comparator.md`, and opens the viewer.

## Reading the result

The kit's version is **not** the presumed winner. It is currently losing by default, which
is the worst of both outcomes — either it deserves to lose and should go, or it deserves
to win and cannot, because it is user-invoked and never fires.

Whichever wins, act on it:

- **Substitute wins** → bucket the kit skills to `_incubator/`, note the winner in
  `LIFECYCLE.md`'s retirement log.
- **Kit wins** → promote it to model-invoked under the [A]/[B]/[C] rule so it can actually
  fire, and uninstall or rename the substitute so the two stop competing.
- **Fork** → the winner is published to both places. Two divergent copies of one skill is
  the failure state regardless of which is better.

Record the outcome as a **precedent** (see `meta-tools/writing-great-skills`): rule,
precedent, self-check. A bake-off nobody wrote down gets re-litigated in six months.

## Prompts

Prompts are deliberately realistic rather than clean — the kind of thing actually typed
mid-task, with the ambiguity left in. A prompt that names the deliverable precisely tests
compliance; one that describes a messy situation tests judgement, which is what separates
these skills.
