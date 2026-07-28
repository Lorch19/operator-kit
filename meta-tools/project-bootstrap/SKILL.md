---
name: project-bootstrap
disable-model-invocation: true
description: >
  Zero-interview project context setup. Auto-detects stack, generates CLAUDE.md + STATE.md + BACKLOG.md + docs/ + launch.json.
  Use when bootstrapping a new project or retrofitting context onto an existing repo.
  Triggers: "bootstrap this project", "set up context", "add CLAUDE.md", "initialize project",
  "retrofit context", "this project needs context files", or when opening a repo that has no CLAUDE.md.
best_for: Setting up or retrofitting project context management files
---

# Project Bootstrap

Generates the full context management structure for any project in one pass — no interview needed. Auto-detects stack, recent activity, and project shape from the filesystem and git history.

## When to Use
- New project with no context files
- Existing project missing CLAUDE.md / STATE.md / BACKLOG.md
- Retrofitting a project that has a .cursorrules or other legacy context file

## What It Creates

```
project-root/
├── CLAUDE.md              # Agent instructions (from defaults + auto-detected stack)
├── STATE.md               # Current state (from git log + filesystem analysis)
├── BACKLOG.md             # Empty structured backlog with priority tiers
├── docs/
│   ├── LESSONS.md         # Empty template
│   └── CONTEXT-PROTOCOL.md # Standard update protocol
├── missions/              # Empty directory (created on demand)
└── .claude/
    └── launch.json        # Dev server config (if detected)
```

## Execution Flow

### Step 1: Auto-Detect Project Shape

Read the filesystem and git history. Do NOT ask the user for any of this.

```bash
# Stack detection
ls package.json pyproject.toml requirements.txt Cargo.toml go.mod pom.xml 2>/dev/null
cat package.json 2>/dev/null | head -30   # framework, scripts, dependencies
cat pyproject.toml 2>/dev/null | head -30
cat requirements.txt 2>/dev/null

# Activity and purpose
git log --oneline -15
git log --format='%s' -30 | head -30  # commit message patterns

# Existing context (migrate, don't duplicate)
cat .cursorrules 2>/dev/null
cat CLAUDE.md 2>/dev/null
cat README.md 2>/dev/null | head -50

# Project structure
ls -la src/ app/ lib/ components/ pages/ api/ 2>/dev/null
ls -la Dockerfile docker-compose.yml Makefile justfile 2>/dev/null
ls -la .env .env.example .env.local 2>/dev/null
ls -la .github/workflows/ 2>/dev/null
ls -la supabase/ prisma/ alembic/ 2>/dev/null
ls -la tests/ test/ __tests__/ 2>/dev/null
```

### Step 2: Classify What You Found

From the detection, determine:

| Dimension | Detection Method |
|-----------|-----------------|
| **Language** | package.json → JS/TS, pyproject.toml/requirements.txt → Python, etc. |
| **Framework** | package.json deps (react, next, vite, express), pyproject (fastapi, django, flask) |
| **Database** | supabase/ → Supabase, prisma/ → Prisma, alembic/ → SQLAlchemy, sqlite3 imports |
| **Deployment** | Dockerfile → Docker, railway.toml → Railway, vercel.json → Vercel, deploy.sh → VPS |
| **Testing** | vitest/jest in package.json → JS tests, pytest in requirements → Python tests |
| **Dev server** | package.json scripts.dev → npm run dev, uvicorn in requirements → Python server |
| **UI library** | tailwind in deps → Tailwind, shadcn in components → shadcn/ui |
| **AI/LLM** | anthropic in deps → Anthropic SDK, langchain → LangChain |

### Step 3: Generate CLAUDE.md

Use the co-founder template from `~/.claude/skills/context-management/assets/DEFAULTS.md` as the personality base. Layer on:

1. **Role section** — Co-founder/CTO (standard from DEFAULTS.md)
2. **User context** — Standard from DEFAULTS.md
3. **Project overview** — 2-3 lines from README/commits/structure
4. **Stack section** — Auto-detected, listed as bullet points
5. **Key architecture** — Top-level directory → purpose mapping (from filesystem)
6. **Code standards** — Stack-appropriate defaults:
   - Python: type hints, pytest, logging, Pydantic
   - TypeScript: strict types (no `any`), ESLint
   - React: component structure, hooks pattern, state management
7. **Session discipline** — Standard from DEFAULTS.md
8. **Context management** — Standard one-liner pointing to docs/CONTEXT-PROTOCOL.md
9. **Pointer index** — Generated from docs/ files

**If .cursorrules exists:** Migrate its content into the appropriate CLAUDE.md sections, then note in the output that .cursorrules can be deleted.

**Keep CLAUDE.md under 120 lines.** If the project is simple, aim for 60-80.

### Step 4: Generate STATE.md

```markdown
<!-- This file must stay under 80 lines. If it grows, prune or move content to docs/. -->
# [Project Name] — Current State
Last updated: [TODAY]

## Project Summary
[2-3 lines derived from README, package.json description, or commit messages]

## Status: [Active/Stable/Early/Paused]
[Based on commit frequency: daily = Active, weekly = Stable, monthly+ = Paused]

## Recent Work
[Summarize last 5-10 commits into 3-5 bullet points]

## Known Issues
[From git log patterns, TODO comments, or obvious gaps like missing .gitignore entries]

## Next Up
- Review BACKLOG.md for priorities
```

### Step 5: Generate Remaining Files

**BACKLOG.md** — Use the standard template with empty tiers. If any obvious tasks were found during detection (missing .gitignore entries, no tests, no CI), add them to appropriate tiers.

**docs/CONTEXT-PROTOCOL.md** — Copy the standard protocol from `~/.claude/skills/context-management/assets/CONTEXT-PROTOCOL.md`, adapting the trigger examples to the detected stack.

**docs/LESSONS.md** — Empty template with a one-line description.

**missions/** — Create directory only, no files.

### Step 6: Generate .claude/launch.json (if applicable)

Detect dev server from:
- `package.json` → `scripts.dev` (npm run dev, port from vite.config or default 5173/3000)
- `pyproject.toml` / `requirements.txt` with uvicorn → uvicorn command
- Docker compose → docker-compose up

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "[project-name]",
      "runtimeExecutable": "[npm|python3|docker-compose]",
      "runtimeArgs": ["[run dev|run main.py|up]"],
      "port": [detected-port]
    }
  ]
}
```

Skip this step if no dev server is detected or if `.claude/launch.json` already exists.

### Step 7: Present for Review

Show the user a summary of what was generated:

```
Generated context files for [project-name]:

  CLAUDE.md       — [N] lines (stack: [React+Vite+TS], role: co-founder/CTO)
  STATE.md        — [N] lines (status: [Active], last commit: [date])
  BACKLOG.md      — [N] items pre-populated
  docs/LESSONS.md — empty template
  docs/CONTEXT-PROTOCOL.md — standard protocol
  .claude/launch.json — [dev server command] on port [port]

[If .cursorrules found]: Content migrated to CLAUDE.md. You can delete .cursorrules.
[If any security issues found]: .env not in .gitignore — added as Urgent backlog item.

Review and let me know if anything needs adjustment.
```

## Rules
- **Never ask what the user can see in the codebase.** Auto-detect everything.
- **One question max** — only if the project purpose is truly ambiguous from commits + README.
- **Keep CLAUDE.md under 120 lines.** Pointers over content.
- **Keep STATE.md under 80 lines.**
- **.gitignore check:** Always verify .env is in .gitignore. Flag if not.
- **Don't overwrite:** If CLAUDE.md already exists, ask before replacing. Offer to merge.
- **Defaults from:** `~/.claude/skills/context-management/assets/DEFAULTS.md`
