# Context Management — Quick Guide for Humans

## What This System Does

Keeps your AI coding agent oriented across sessions. Two small files at project root give the agent everything it needs to pick up where you left off.

---

## The Files

### CLAUDE.md — "How to work with me"
**What:** Your agent's instructions. Role, rules, coding standards, and a pointer index to deeper docs.
**When to edit:** Rarely. Only when your working style or project rules change.
**Size:** under 8 KB. Measured in bytes (`wc -c`), not lines — long lines defeat a line limit.

### STATE.md — "Where we are right now"
**What:** Current task, project status, next priorities.
**When to edit:** Every session (when you ask the agent to update it).
**Size:** under 6 KB (`wc -c`). There's a built-in reminder at the top to keep it lean.
**Freshness:** Carries a `Last verified: [DATE] (against git HEAD [SHA])` line, not "Last updated." A stale STATE.md is worse than none — sessions trust it and plan on a false picture. Back it with a mechanical check (a Stop hook comparing the file's age against the latest commit); prose reminders don't hold.

### docs/CONTEXT-PROTOCOL.md — "How to update context"
**What:** The rules the agent follows when you ask "should we update context?" at session end.
**Why separate:** Keeping it outside CLAUDE.md means the agent only loads update logic when it's actually needed, not during the 99% of the session where you're building. This keeps the agent focused and precise.
**When to edit:** Rarely. The protocol is generic and works across projects.

### Agent memory — the agent's own notes (optional, separate system)
**What:** Claude Code's memory — a *directory* of one-fact-per-file markdown, outside your repo, with `MEMORY.md` as a pure index (one pointer line per fact, never content). The agent accumulates these across all your projects: how you like to work, cross-project goals, useful references.
**Who controls it:** The agent. This is NOT part of your curated, repo-scoped context.
**The boundary that matters:** Where the project stands right now → STATE.md. How to work in this repo → CLAUDE.md. How to work with you *anywhere*, or cross-project goals → agent memory. Never let the same fact live in both — repo-scoped facts belong in the repo, which versions them; memories rot invisibly because nothing does.

### BACKLOG.md — "What to do next"
**What:** A prioritized task list shared between you and the agent. Five tiers: Urgent (ASAP), High (1-3 days), Priority (within 2 weeks), Strategic (no deadline), Non-priority (someday).
**When to edit:** Anytime. Either you or the agent can add/update/delete tasks.
**Size:** No hard limit, but prune completed items monthly.

### missions/ — "Detailed task specs"
**What:** Complex backlog items get a dedicated file with full implementation details (goal, steps, acceptance criteria, files to modify).
**When to create:** When a task touches 3+ files, has architectural implications, requires multi-step verification, or could break existing behavior. The agent proactively suggests creating one when warranted.
**Size:** No limit. These load on-demand when working on that task.

### docs/ — "Deep dives"
**What:** Detailed context per domain. Architecture decisions, lessons learned, complex system docs.
**When to create:** Only when a domain gets complex enough to need its own file.
**Size:** No limit. These load on-demand, not every session.

---

## How to Run a Session

### Starting
1. Open your agent (Claude Code, Cursor, etc.)
2. The agent reads CLAUDE.md and STATE.md automatically
3. The agent scans BACKLOG.md — if you don't have a specific task, it suggests the top priority item
4. Tell it what you want to work on (or pick from the backlog)
5. It loads any relevant docs/ or missions/ files if needed

### During work
Just work normally. The agent has the context it needs.
If a non-urgent task comes up mid-session, the agent adds it to BACKLOG.md instead of derailing your current work.

### Ending
Ask: **"Should we update context?"**

The agent reads `docs/CONTEXT-PROTOCOL.md` and checks:
- Did the current task change?
- Did a feature ship or break?
- Was an architectural decision made?
- Was a critical lesson learned?
- Is anything in STATE.md now outdated?

If yes to any → it suggests specific edits. You approve or adjust. When STATE.md changes, the agent re-verifies it against the code and bumps the `Last verified` date + commit SHA.
If no → you're done.

---

## Golden Rules

1. **You control updates.** The agent never modifies context files without you asking.
2. **Pointers, not summaries.** Context files reference file paths. They don't explain what's in those files. The agent can read them itself.
3. **Prune aggressively.** If STATE.md is growing past 6 KB (`wc -c`), move stuff to docs/ or delete it. Cut content — don't compress by writing longer lines.
4. **One file per domain.** When a system gets complex (payments, auth, scraping), give it a docs/ file.
5. **Decisions, not descriptions.** Write "We chose Stripe because X", not "Stripe is a payment processor that..."

---

## Setting Up a New Project

Ask the agent to set up context management. It will interview you and generate the files.

**In Claude Code:**
```
@path/to/context-management.skill — set up context management for this project.
Interview me about my preferences, the project, and current status,
then create the context files.
```

**In other agents:**
Drop the template files in your project root and ask:
```
Read the template files in this project root. Interview me about my
preferences and project details, then fill them in properly.
```

The agent asks you questions, generates the files, and you review and approve. One setup per project. The protocol inside the files keeps the system alive from that point forward.

---

## When Does a Task Become a Mission?

Not every backlog item needs a mission file. Here's the rule of thumb:

| Stays in BACKLOG.md only | Gets a mission file in missions/ |
|---|---|
| Single-file change | Touches 3+ files |
| Clear, self-contained task | Has architectural implications |
| No risk of breaking things | Could break existing behavior |
| One-step verification | Requires multi-step verification |

The agent proactively assesses complexity when you add a task and suggests creating a mission file when warranted.

---

## Claude Code: `.claude/` Directory

If you're using Claude Code, these files help configure your environment:

```
.claude/
├── settings.json    # Permissions, allowed tools, env vars
├── skills/          # Project-specific skills
└── launch.json      # Dev server configs (for preview)
```

These are project-specific and can't be templated, but setting them up early saves time. Ask the agent to help configure them during setup.

---

## Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| Pasting code into context files | Use file paths instead |
| Writing long explanations | Bullet points and pointers |
| Updating context every 5 minutes | Only at session end, when you ask |
| Keeping all history | Prune. Only current state matters |
| One giant file for everything | Split: instructions / state / deep docs |
| Summarizing what the agent can grep | Delete it, add a pointer |

---

Created by Omri Lorch
