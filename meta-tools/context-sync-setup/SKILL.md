---
name: context-sync-setup
disable-model-invocation: true
description: >
  Generate a scheduled context-sync task for any project. Creates a bi-daily task that keeps
  STATE.md and BACKLOG.md fresh by comparing with git log and optional health checks.
  Triggers: "set up context sync", "add auto-sync", "create sync task", "keep context fresh",
  or when bootstrapping a new project that needs automated maintenance.
best_for: Creating automated context freshness tasks for projects
---

# Context Sync Setup

Generates a scheduled task that keeps a project's STATE.md and BACKLOG.md up to date by running every 2 days.

## When to Use
- After bootstrapping a new project with context files
- When a project has context files but no automated sync
- When converting a manually-maintained project to auto-sync

## Inputs

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| Project name | Yes | — | Human-readable name for the task |
| Project path | Yes | — | Absolute path to project root |
| Health check | No | none | Optional command to check external service health (SSH, curl, etc.) |
| Schedule | No | every 2 days, staggered | Cron expression — auto-staggered to avoid conflicts |
| Notify | No | false | Send Telegram notification on completion |

## Execution Flow

### Step 1: Check for Conflicts

List existing scheduled tasks to determine a non-conflicting schedule minute:

```
mcp__scheduled-tasks__list_scheduled_tasks
```

Existing context-sync tasks typically run at these minutes past 8:00 AM:
- :23 (portfolio-system)
- :27 (linx-advisor)
- :31 (shopagent)
- :35 (watchtogether)
- :39 (first-bloom)

Pick the next available 4-minute-staggered slot (e.g., :43, :47, etc.).

### Step 2: Generate Task Prompt

Use this template, filling in the project-specific values:

```
Lightweight context sync for [PROJECT_NAME]. Be cost-sensitive — use Haiku-level reasoning, skip deep analysis.

## Steps

1. **Read current state** (fast):
   ```bash
   cd [PROJECT_PATH]
   git log --oneline -10
   ```
   Read STATE.md and BACKLOG.md.

[IF HEALTH_CHECK provided:]
2. **Check service health** (one call):
   ```bash
   [HEALTH_CHECK_COMMAND]
   ```

[NEXT_STEP_NUMBER]. **Update STATE.md** if anything changed:
   - Update "Last updated" timestamp
   - Update component status table if git log shows changes
   - Update "Current task" and "Next Up" based on recent commits
   - Update "Known issues" — mark resolved items, add new ones

[NEXT_STEP_NUMBER]. **Update BACKLOG.md** if needed:
   - Mark completed items as done (cross-reference with git log)
   - Move blocked items if blockers resolved
   - Don't add new items — just maintain accuracy

[NEXT_STEP_NUMBER]. **Skip if nothing changed** — if git log shows no commits since last sync, do nothing.

## Rules
- Read before writing. Never overwrite blindly.
- Keep STATE.md under 80 lines. Keep BACKLOG.md structured.
- Don't touch CLAUDE.md, architecture docs, or config files.
[IF HEALTH_CHECK:] - If service is unhealthy, note it in STATE.md known issues.
- Total runtime target: under 30 seconds of LLM time.
```

### Step 3: Create the Scheduled Task

```
mcp__scheduled-tasks__create_scheduled_task(
  taskId: "[project-name]-context-sync",
  description: "Update [PROJECT_NAME] STATE.md and BACKLOG.md with current codebase state every 2 days",
  cronExpression: "[STAGGERED_MINUTE] 8 */2 * *",
  prompt: [GENERATED_PROMPT],
  notifyOnCompletion: [NOTIFY]
)
```

### Step 4: Update Project CLAUDE.md

Add a note to the project's CLAUDE.md if it doesn't already mention context sync:

```markdown
## Automated Context Sync
A scheduled task (`[project-name]-context-sync`) runs every 2 days to update STATE.md and BACKLOG.md against the actual codebase. Don't duplicate this work manually — the task handles staleness.
```

### Step 5: Confirm

```
Created context-sync task for [PROJECT_NAME]:
  Task ID: [project-name]-context-sync
  Schedule: Every 2 days at 8:[MM] AM
  Health check: [yes/no]
  Notification: [on/off]

Recommend running it once manually to verify: click "Run now" in the Scheduled Tasks sidebar.
```

## Health Check Examples

| Project Type | Health Check Command |
|-------------|---------------------|
| VPS (SSH) | `ssh user@host 'tail -3 /path/logs/latest.log && echo OK'` |
| Railway | `curl -sf https://app.railway.app/api/health` |
| Supabase Edge | `curl -sf https://project.supabase.co/functions/v1/health` |
| Local SQLite | `sqlite3 /path/db.sqlite "SELECT COUNT(*) FROM main_table"` |
| Docker | `docker ps --filter name=project --format '{{.Status}}'` |

## Rules
- **Auto-stagger** — never schedule at the same minute as an existing task
- **Cost-sensitive** — task prompt instructs Haiku-level reasoning
- **Skip if idle** — task does nothing if no commits since last sync
- **Read before write** — every task checks current state before modifying
