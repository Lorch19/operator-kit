---
name: health-check-monitor
disable-model-invocation: true
description: >
  Unified cross-project health monitoring. Checks all deployed services and sends a single
  Telegram digest with green/red status per project.
  Triggers: "check health", "system status", "are my services up", "health report",
  or runs automatically as a daily scheduled task.
best_for: Monitoring deployed services across multiple projects
---

# Health Check Monitor

Checks all deployed services and sends a single Telegram digest. Designed to run as a daily scheduled task or on-demand.

## Monitored Services

| Service | Type | Health Check |
|---------|------|-------------|
| portfolio-system | VPS (SSH) | Pipeline logs + open positions + cron status |
| WatchTogether-Agent | Railway | `https://watchtogether.up.railway.app/api/health` |
| first-bloom-build | Lovable | HTTP response from `https://first-bloom-build.lovable.app/` |
| Scheduled tasks | Claude platform | Task list — flag any that missed their expected run |

## Execution Flow

### Step 1: Check Portfolio System (VPS)

The most critical check — this handles real money.

```bash
ssh vps 'echo "=== LOGS ==="; tail -3 /home/ubuntu/portfolio-system/logs/latest.log 2>/dev/null || echo "NO LOGS"; echo "=== POSITIONS ==="; sqlite3 /home/ubuntu/portfolio-system/data/portfolio.db "SELECT COUNT(*) FROM sim_positions WHERE status='\''open'\''" 2>/dev/null || echo "DB ERROR"; echo "=== CRON ==="; crontab -l 2>/dev/null | grep -c "run_" || echo "NO CRONS"; echo "=== DISK ==="; df -h / | tail -1 | awk "{print \$5}"'
```

**Parse results:**
- Logs: check timestamp of last line — if older than 24h on a weekday, flag as stale
- Positions: count should be a reasonable number (0-30). Negative or error = red
- Cron: should have 4+ entries (morning, evening, weekly, monthly). Missing = red
- Disk: if >85% full, flag as warning

### Step 2: Check WatchTogether (Railway)

```bash
curl -sf --max-time 10 https://watchtogether.up.railway.app/api/health
```

**Parse results:**
- 200 OK = green
- Timeout or error = red
- Non-200 status = yellow (degraded)

### Step 3: Check first-bloom-build (Lovable)

```bash
curl -sf --max-time 10 -o /dev/null -w "%{http_code}" https://first-bloom-build.lovable.app/
```

**Parse results:**
- 200 = green
- 3xx = yellow (redirect, probably fine)
- 4xx/5xx or timeout = red

### Step 4: Check Scheduled Tasks

```
mcp__scheduled-tasks__list_scheduled_tasks
```

For each enabled task with a cron schedule:
- Compare `lastRunAt` with expected schedule
- If a task hasn't run when it should have (missed by >2x the interval), flag it
- Ignore one-shot tasks that have already fired

**Key tasks to watch:**
- `pre-market-portfolio-review` — must run Mon-Fri before 16:30 IST
- `post-market-daily-review` — must run Mon-Fri before midnight IST
- `portfolio-context-sync` — must run within last 3 days
- `linx-morning-brief` — must run Sun-Thu mornings

### Step 5: Check Git Freshness (Optional)

For each project, check if there are uncommitted changes older than 3 days:

```bash
for repo in /Users/omrilorch/portfolio-system /Users/omrilorch/WatchTogether-Agent /Users/omrilorch/first-bloom-build /Users/omrilorch/IL-ecommerce-Agent /Users/omrilorch/lorchprotfoliotracker; do
  name=$(basename "$repo")
  dirty=$(git -C "$repo" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  last_commit=$(git -C "$repo" log -1 --format='%ar' 2>/dev/null)
  [ "$dirty" -gt 0 ] && echo "$name: $dirty uncommitted files (last commit: $last_commit)"
done
```

### Step 6: Compose Telegram Digest

Format as a single message:

```
🏥 Daily Health Check — [DATE]

Portfolio System (VPS):
  [✅/❌] Pipeline: [last log timestamp]
  [✅/❌] Positions: [N] open
  [✅/❌] Crons: [N] active
  [✅/⚠️] Disk: [N]% used

WatchTogether (Railway):
  [✅/❌/⚠️] API: [status]

First Bloom (Lovable):
  [✅/❌] Frontend: [status]

Scheduled Tasks:
  [✅/⚠️] [N] of [M] tasks on schedule
  [List any missed tasks]

[If any git freshness issues:]
Git:
  [⚠️] [repo]: [N] uncommitted files

[If all green:]
All systems nominal.
```

### Step 7: Send via Telegram

```bash
curl -sf -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d chat_id="${TELEGRAM_CHAT_ID}" \
  -d text="$(cat /tmp/health_digest.txt)" \
  -d parse_mode="Markdown" > /dev/null
```

If Telegram env vars are not available, print the digest to stdout instead.

## Configuration

The monitor reads its service list from the check steps above. To add a new service:
1. Add a new check step
2. Add a new section to the digest template
3. If it's a URL check, add to the curl checks
4. If it's SSH-based, add to the VPS check command

## Error Handling

- If SSH to VPS fails: report "VPS unreachable" as red, continue with other checks
- If curl times out: report "timeout" as red, continue with other checks
- If scheduled tasks API fails: skip that section, note in digest
- Never let one failed check block the others

## Rules
- **Portfolio-system is highest priority** — it handles real money. Always check first.
- **Single message** — never send multiple Telegram messages. One digest, all services.
- **Fail-open on checks** — if a check itself errors, report the error and move on. Don't crash.
- **Weekday-aware** — portfolio crons only run Mon-Fri. Don't flag missing weekend runs.
- **Cost-sensitive** — this runs daily. Keep LLM reasoning minimal. Most logic is bash commands.
