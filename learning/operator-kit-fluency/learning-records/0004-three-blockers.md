# 0004 — Three blockers found while clearing the open items

**Date:** 2026-09-14
**Status:** measured. Two need a decision from Omri before acting.

## 1. 58% of skills cannot be packaged for claude.ai

Packaging the kit's `skill-creator` for upload fails validation:

```
❌ Unexpected key(s) in SKILL.md frontmatter: best_for, type.
   Allowed: allowed-tools, compatibility, description, license, metadata, name
```

**82 of 141 skills** carry keys outside the allowed set:

| Key | Skills |
|---|---|
| `type` | 78 |
| `best_for` | 50 |
| `scenarios` / `estimated_time` / `theme` | 14 each |
| `triggers` | 2 |

Concentrated in `pm-frameworks` (43), `pm-agents` (13), `meta-tools` (8).

**Nothing reads them.** No script, no navigator, no generator — the only matches for
`scenarios` and `theme` elsewhere are unrelated (financial forecast scenarios, RICE
themes). They are inert metadata.

But they were added deliberately: `BACKLOG.md` records *"Add `type`/`best_for` to
remaining pm-agents skills — Done. All 12 skills now have `type: component` and 4
`best_for` entries each."*

This likely explains the fork divergence in record 0003. A clean upload path from the kit
to claude.ai does not exist, so the account copies were made some other way and drifted.

**Decision needed:** strip the inert keys and gain a working sync path, or keep them as
human documentation and accept that claude.ai copies stay hand-maintained.

## 2. Five broken invocation directives

`LIFECYCLE.md` states that a user-invoked skill is unreachable by other skills, and that
clause [B] — *called by another skill* — is **decisive** for model-invocation. Five
places instruct Claude to invoke a skill that cannot be invoked:

| Caller | Directive | Target |
|---|---|---|
| `implement` | "Once done, use /code-review to review the work." | `code-review` |
| `to-spec` | "run `/agent-context-setup`" | `agent-context-setup` |
| `to-tickets` | "run `/agent-context-setup`" | `agent-context-setup` |
| `triage` | references `/agent-context-setup` | `agent-context-setup` |
| `wayfinder` | references `/agent-context-setup` | `agent-context-setup` |

**A first pass claimed 39.** That was wrong — the regex matched `DO NOT use for X — use Y
instead` clauses in *description* frontmatter, which are routing hints, not calls. A
second pass over bodies only gave 33, still wrong: most were `**Use:**
skills/X/SKILL.md`, a **file path**. Claude reads that file whether or not the skill is
model-invoked, so nothing is broken. Only directives to *invoke* fail. Five.

Recorded because the error is the instructive part: three passes, each narrowing, and the
first number was off by 8×. A self-check answerable by grep count is not a self-check.

**Two fixes, and they are not equivalent:**

- **Promote the targets to model-invoked.** Correct by the rule, but `CLAUDE.md` notes
  `engineering-tools/code-review` deliberately shadows the bundled `/code-review` —
  promoting it makes two skills compete. And `agent-context-setup` writes repo config;
  letting it fire unprompted is aggressive for a setup skill.
- **Fix the callers' wording** — "ask the user to run `/agent-context-setup`" rather than
  "run" it. Less invasive, and arguably more correct for a skill that writes config.

Leaning: wording fix for `agent-context-setup`, promotion for `code-review` only if the
shadowing question is settled first.

## 3. The lab repo was never cloned

`cd template` failed because `video-shotcraft-lab` does not exist locally. Not a defect —
noted so the next session does not re-diagnose it.
