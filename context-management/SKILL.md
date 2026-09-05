---
name: context-management
disable-model-invocation: true
description: >
  Context management system for vibe coders working with AI coding agents (Claude Code, Cursor, etc.).
  Use when a user wants to set up or improve how they maintain project context across sessions with a coding agent.
  Triggers: "set up context management", "create CLAUDE.md", "create STATE.md", "manage context",
  "start a new project", "session management", "context files", or when the user is struggling with
  context loss between sessions. Also use when the user asks to update, review, or restructure their
  project's context files.
type: workflow
best_for:
  - "Setting up CLAUDE.md + STATE.md for a project"
  - "Maintaining context across AI coding sessions"
  - "Structuring project knowledge for Claude Code or Cursor"
---

# Context Management for AI Coding Agents

A system for maintaining project context across sessions. Two files + on-demand docs.

## Core Philosophy

1. **Context is finite.** Every token competes for model attention. Write less, mean more.
2. **Pointers over content.** Never write in context what the agent can find by reading the codebase. Reference file paths, not summaries of what's inside them.
3. **User controls updates.** Never update context files unless the user asks. When asked, evaluate what actually changed.
4. **The agent is a CTO.** Treat it as a senior partner who takes ownership, not a tool that executes commands.

## System Architecture

```
project-root/
├── CLAUDE.md          # HOW to work (stable, under 8 KB)
├── STATE.md           # WHERE we are (volatile, under 6 KB)
├── BACKLOG.md         # WHAT to do next (shared task backlog)
├── missions/          # Detailed specs for complex backlog items
└── docs/              # Deep context (on-demand)
    ├── CONTEXT-PROTOCOL.md
    ├── ARCHITECTURE.md
    ├── LESSONS.md
    └── [DOMAIN].md
```

**Always loaded:** CLAUDE.md + STATE.md (together under 14 KB)

**Budget in bytes, never lines.** A line limit is trivially satisfied by writing longer
lines, and that is exactly what happens under pressure. Measured case: a STATE.md sitting
at exactly the "80 line" limit was 11.4 KB at 142 chars/line — passing the rule while
carrying ~4x the intended payload. Check with `wc -c`, and when over budget **cut
content**; never compress by lengthening lines.
**Scanned at session start:** BACKLOG.md (priority tiers only)
**On-demand:** docs/ files and missions/, loaded only when working on that domain

## File Responsibilities

### CLAUDE.md — Instructions (stable, rarely changes)

Defines behavior, rules, and a pointer index to deeper docs.

Contains:
- Role + communication style (brief)
- Problem-solving rules
- Code standards
- Pointer index: a table mapping domains to file paths in docs/
- One-line pointer to the Context Update Protocol (see below)

Does NOT contain: current tasks, project status, code snippets, domain details, or the full update protocol.

### STATE.md — Current State (volatile, updated per session)

Always loaded. Tells the agent where the project stands.

Contains:
- 2-3 line project summary (stable anchor at top)
- Current task + acceptance criteria
- System status table (what's live, in progress, planned)
- Next 3 priorities
- Self-enforcing size rule at the top

Does NOT contain: behavioral instructions, architecture details, lessons learned.

**Critical:** STATE.md must include a size constraint that the agent sees every time:
`<!-- BUDGET: under 6,000 bytes. Check with wc -c, not line count. If over, CUT content. -->`

**Freshness is not optional, and cannot be enforced by prose.** A STATE.md that has gone
stale is worse than none — sessions read it, trust it, and plan on top of a false picture.
Reminders like "nudge the user to update context" do not work; this has been observed
failing twice on the same project while the file drifted 28 days / 38 commits behind HEAD.
Give the file a `Last verified: [DATE]` line and back it with a mechanical check (a Stop
hook comparing the file's mtime against the latest commit timestamp is cheap and enough).
If a scheduled task owns the refresh, never write "the task handles staleness" anywhere —
that sentence turns a silent failure into an enforced blind spot.

### BACKLOG.md — Shared Task Backlog (scanned at session start)

A prioritized list of tasks shared between the user and the agent. Either can add, update, or delete items.

Contains:
- Five priority tiers: Urgent (ASAP), High (1-3 days), Priority (within 2 weeks), Strategic (no deadline), Non-priority (someday)
- Each task: description, acceptance criteria, optional Ref link to mission file, status
- Links to `missions/` for complex tasks

Does NOT contain: detailed implementation specs (those go in missions/).

### missions/ — Detailed Task Specs (on-demand)

Complex backlog items get a dedicated mission file with full implementation details.

**When a task becomes a mission:**
- Touches 3+ files
- Has architectural implications
- Requires multi-step verification
- Could break existing behavior

Simple single-file changes stay in BACKLOG.md only. The agent proactively assesses complexity and suggests creating a mission file when warranted.

**Mission lifecycle (execution gate).** A mission carries a status: `DRAFT` → `READY` → `IN_PROGRESS` → `DONE`. A DRAFT mission has unresolved `[OPEN]` decisions in its Open Decisions section, surfaced by the template's forcing questions (integration boundaries, conflict scenarios, trigger/lifecycle, opinionated defaults, blast radius). **An agent must refuse to execute a DRAFT mission** and instead list the open decisions for the user to resolve; only a READY mission (all decisions `[RESOLVED]`) can be picked up. See `assets/MISSION.template.md`.

### docs/ — Deep Context (on-demand)

Loaded only when working on a specific domain.

- **CONTEXT-PROTOCOL.md** — the context update protocol (see section below)
- **ARCHITECTURE.md** — tech stack, key decisions with rationale, key file paths
- **LESSONS.md** — only system-critical lessons (not every bug fix)
- **[DOMAIN].md** — one file per complex system (payments, scraper, auth, etc.)

## Context Update Protocol

The update protocol lives in its own file: `docs/CONTEXT-PROTOCOL.md`. It is NOT inside CLAUDE.md.

CLAUDE.md contains only a one-line pointer:
`When I ask "should we update context?" → read docs/CONTEXT-PROTOCOL.md and follow it.`

**Why separate?** Two reasons.

1. **Attention.** If the full protocol lives inside CLAUDE.md, the agent sees update instructions at the start of every session, taking up attention while the user is in the middle of building. By externalizing it, the agent only loads those instructions when actually needed: at session end.

2. **Precision.** The agent knows the protocol file exists (it's referenced in CLAUDE.md) and will use it when asked. But the protocol is short and focused. Injecting it at the right moment keeps the agent precise about how to evaluate and update, rather than "freestyling" updates based on vague memory of the rules.

The protocol is loaded on-demand only when the user asks "should we update context?" at session end. See `assets/CONTEXT-PROTOCOL.md` for the full protocol (to be placed at `docs/CONTEXT-PROTOCOL.md` in the project).

## What Makes a Good Pointer

Bad: `Payment → /src/payments/`
Good: `Payment (Stripe webhooks, LemonSqueezy checkout) → /src/payments/`

The extra few words save a file read to determine relevance.

## Agent memory — complementary, not part of this system

Claude Code's memory is **a directory of one-fact-per-file markdown**, not a single
notebook. Each file carries frontmatter (`name`, `description`, `metadata.type` of
`user` | `feedback` | `project` | `reference`), and `MEMORY.md` is a pure **index** —
one pointer line per memory, never content.

- CLAUDE.md + STATE.md = user-curated, per-project, in the repo (you control)
- memory/ = agent-accumulated, cross-project, outside the repo (agent controls)

**The boundary that actually matters.** Memory's `project` and `feedback` types overlap
STATE.md and CLAUDE.md, so state the split explicitly or the same fact lands in both and
they drift apart:

| Fact | Home | Why |
|---|---|---|
| Where this project stands right now | **STATE.md** | Volatile, repo-scoped, versioned with the code |
| How to work in this repo | **CLAUDE.md** | Applies only inside the project |
| How to work with this user, anywhere | **memory (`feedback`)** | Follows them across every project |
| Cross-project goals and context | **memory (`project`)** | Not derivable from any one repo |

**Rules.**
- Never duplicate a fact across a memory and a context file. If it belongs in the repo,
  it belongs in the repo — memories go stale invisibly because nothing versions them.
- Never keep in memory what the harness already injects each session (the skill list, the
  file tree, the git history). It rots and then actively misleads.
- Periodically re-read memories: they are point-in-time observations, so verify any
  file path, flag, or command still exists before acting on one.
- Do not reference the memory directory from CLAUDE.md or STATE.md.

## Session Workflow

1. Agent reads CLAUDE.md → sees pointer index + rules
2. Agent reads STATE.md → sees current task + project status
3. Agent scans BACKLOG.md → if no specific task, suggests top Urgent/High item
4. Agent loads relevant docs/ or missions/ based on the task (if needed)
5. Work happens — non-urgent tasks that surface go to BACKLOG.md
6. When user asks "should we update context?" → agent reads `docs/CONTEXT-PROTOCOL.md` and follows it

## Setting Up a New Project

When the user asks to set up context management:

1. **Load personal defaults first.** Read `assets/DEFAULTS.md` — it contains the user's role, communication style, agent mindset, session discipline, and standard rules. Do NOT re-ask about anything already covered there.
2. **Interview for project-specific details only:** project name, what it does, who it's for, current status, tech stack, and any project-specific rules or standards.
3. Generate CLAUDE.md from defaults + project answers using the template in `assets/CLAUDE.template.md`.
4. Generate STATE.md from project answers using the template in `assets/STATE.template.md`.
5. Create `BACKLOG.md` from the template in `assets/BACKLOG.template.md`.
6. Place `assets/CONTEXT-PROTOCOL.md` at `docs/CONTEXT-PROTOCOL.md`.
7. Create `docs/LESSONS.md` from the template in `assets/LESSONS.template.md`.
8. Create `docs/ARCHITECTURE.md` from the template in `assets/ARCHITECTURE.template.md` (if the project has multiple components).
9. Create the `missions/` folder (empty — mission files are created as complex tasks arise).
10. Present the generated files for user review and approval before saving.

**Note on `.claude/` directory (Claude Code users):**
If the project uses Claude Code, consider setting up:
- `.claude/settings.json` — permissions and allowed tools
- `.claude/skills/` — project-specific skills
- `.claude/launch.json` — dev server configs (for preview)
