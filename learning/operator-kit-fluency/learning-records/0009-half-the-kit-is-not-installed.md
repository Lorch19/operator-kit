# 0009 — 36% of the kit cannot fire, and that includes the experiment's decisive sub-test

**Date:** 2026-09-21 · **Status:** measured. Reproduce with `scripts/reachability.py`.

Found while checking which copy of 19 duplicated skills to delete. The deletion was
not performed; this is why.

## The measurement

A kit skill reaches a session only if its pack appears in `enabledPlugins` in
`~/.claude/settings.json`. Eight packs do not.

```
enabledPlugins (operator-kit): context-management, document-tools,
  engineering-tools, meta-tools, pm-frameworks, prd-partner, thinking-tools
```

| | Counted by `validate-kit.py` | Actually reachable |
|---|---|---|
| Active skills | 141 | **90** |
| Model-invoked | 54 | **25** |

**51 skills — 36% of the kit — cannot fire in any session, in any invocation mode.**

Not enabled: `design-tools` (7) · `sales-tools` (9) · `operations-tools` (9) ·
`pm-agents` (13) · `domain-tools` (6) · `analytics-tools` (3) · `gtm-tools` (3) ·
`doc-coauthoring` (1).

## What this does to record 0005

**12 of the 17 promoted cohort skills are in packs that are not installed** —
`design-tools` (4), `sales-tools` (5), `operations-tools` (3). The 2026-09-15 promotion
changed their frontmatter from user-invoked to model-invoked. It could not have changed
their usage, because they were never loaded.

Worse, `design-tools` is 0005's **decisive sub-test** — chosen precisely because Omri
demonstrably does design work (`ux-*` fired 31 times to design-tools' 0). 0005's
pre-registered reading of a continued zero is:

> *"Invocation is not the blocker — the substitutes are simply better. The bake-off
> decides, and `design-tools` goes."*

That inference is unsafe. The zero measures **installation**, not fit, not quality, and
not invocation mode. On 15 Oct the cohort will read near-zero for 12 of 17 skills for a
reason that has nothing to do with what the experiment is testing.

This is the third distinct cause found for the same symptom, and they stack:

| Cause | Scope | Record |
|---|---|---|
| Pack not installed | 12 of 17 cohort skills | **this record** |
| Description out-claimed by a rival | `design-critique` specifically | [[0006-routing-not-invocation]] |
| User-invocation strips the description | the 87-skill control | [[0003-invocation-is-the-cause]] |

A skill can be blocked by all three at once. `design-critique` is.

## The proxy trap, inside our own tooling

`validate-kit.py` counts `SKILL.md` files in the repo and reports "141 active, 54
model-invoked, description context budget ~3978 tokens". Every one of those numbers is a
repo statistic presented as a session statistic. The real figures are 90, 25, and a
correspondingly smaller budget.

I ran that validator after every commit this session and read "OK" as confirmation the
kit was in good order. It was confirming the files were well-formed — which is not the
same claim, and is exactly the substitution the `proxy-metric-traps` memory warns about:
**file presence standing in for reachability.** `scripts/reachability.py` now makes the
honest check one command.

## What it does to the bake-offs

Nothing about their verdicts — those compared output quality with both skills handed
directly to an agent, so installation never entered into it. `design-tools` winning 2-2
against `ux-reviewer` stands.

But it settles the question the bake-offs were meant to inform. The kit was not losing
to substitutes on quality; on quality it is roughly even. It was losing because half of
it was never installed, and the substitutes were.

## Corrections to claims made earlier in this session

- **"19 description-only duplicates can be deleted for zero capability loss."** Wrong
  twice. Five of the 19 are user-invoked kit copies, i.e. members of the 87-skill
  **control group** that 0005 registered and the handoff forbids pruning. And for those
  five the kit copy is user-invoked while the twin is model-invoked, so the twin is their
  only reachable route — deleting it removes capability rather than duplication.
- **`pm-agents` "duplicates" are not double-loaded.** The kit's `pm-agents` is not
  installed, so only the `compound-pm` copy is ever in context. There is no duplicate
  context cost to recover there, and deleting `compound-pm` would remove those 13 skills
  outright.

## Recommended next, none of it done

1. **Do not read the 15 Oct cohort result for the 12 unreachable skills.** They are
   unreadable, not negative. Score only `engineering-tools` (4) and `meta-tools` (1),
   which are installed — and per 0006, score those per-skill.
2. **Decide whether to enable the eight packs.** One line in `settings.json`. It is the
   only way the cohort question becomes answerable — and it changes what is in context
   during a live experiment, so it is a deliberate choice with a cost, not a fix.
3. **Teach `validate-kit.py` about reachability**, or have it call
   `scripts/reachability.py`, so "OK" stops meaning "the files parse".
4. Re-run the fork census ([[0008-fork-census]]) against *reachable* skills only; several
   of the 29 duplicates are not duplicates in any session.
