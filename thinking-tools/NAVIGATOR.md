# Thinking Tools — Navigator

6 domain-agnostic reasoning primitives. Not frameworks with templates — small, composable
moves you apply to *any* subject: a PRD, a hiring plan, a pricing model, a codebase.

Adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT). See `/CREDITS.md`.

## Which Skill?

| I need to... | Use this |
|---|---|
| Stress-test a plan, decision, or idea by relentless interview | `grill-me` (or `grilling` as a primitive) |
| Hand the current conversation to a fresh session without losing context | `handoff` |
| Delegate reading legwork to a background agent, cited to primary sources | `research` |
| Plan an effort too big for one session, as a map of decision tickets | `wayfinder` |
| Learn a topic over multiple sessions, in a stateful workspace | `teach` |

## How they compose

`grilling` is a **primitive** other skills call — it's model-invoked so anything can reach
it. It is the "one question at a time, you decide, I look up facts" discipline, not a
framework: the caller supplies the agenda, grilling supplies the rules.

**Three ways in:**

- `/grill-me` — the user-facing wrapper, for anything that isn't in a repo.
- `/grilling` — the primitive directly (model-invoked skills stay user-invocable too).
- **Say it in plain English** — "stress-test this", "poke holes in this", "what am I
  missing?", "talk me out of this". Claude fires it on its own; that's what its
  model-invoked description is for.

**Who calls it today:** `prd-partner` (Discovery Mode), `/pm:strategy` (Steps 1–5),
`wayfinder` (naming the destination, and every grilling-type ticket),
`engineering-tools/triage` (fleshing out a request), and
`engineering-tools/improve-codebase-architecture` (walking a chosen refactor).

```
loose idea
  ├─ small enough to hold in one session → /grill-me → /prd-partner or /pm:spec
  └─ too big / too foggy                 → /wayfinder → charts a map of decision
                                            tickets, resolves one per session,
                                            then hands off to a spec
context window filling up               → /handoff → open a fresh session against the file
a fact is blocking a decision           → /research → background agent, primary sources
```

## The two rules that make `grilling` work

1. **One question at a time.** Multiple questions at once is bewildering and produces
   shallow answers.
2. **Look up facts, ask about decisions.** If the environment can answer it, don't ask.

## Cross-Pack References

| If you need... | Go to... |
|---|---|
| Turn a sharpened idea into a PRD | `prd-partner` or `pm-frameworks/prd-development` |
| Multi-agent review of the result | `pm-agents` → `/pm:review` |
| Break a spec into tickets | `engineering-tools/to-tickets` |
| Turn a conversation into a spec | `engineering-tools/to-spec` |
| Persist project state across sessions | `context-management` |
| Write or edit a skill well | `meta-tools/writing-great-skills` |
