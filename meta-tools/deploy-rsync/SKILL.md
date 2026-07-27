---
name: deploy-rsync
disable-model-invocation: true
description: >
  Generate and execute rsync+SSH deployments to a VPS. Handles file sync with smart excludes,
  remote environment verification, post-deploy setup, health checks, and optional Telegram notification.
  Triggers: "deploy to VPS", "deploy via rsync", "push to server", "deploy this project",
  or when a project needs a deploy script.
best_for: Deploying Python or Node.js projects to a VPS via rsync+SSH
---

# Deploy via Rsync

Two modes: **generate** a reusable deploy.sh script, or **execute** a one-off deployment interactively.

## Mode 1: Generate Deploy Script

When the user says "create a deploy script" or "set up deployment".

### Inputs (ask only what's missing)

| Parameter | Required | Example |
|-----------|----------|---------|
| Remote host | Yes | `ubuntu@151.145.82.110` or `vps` (SSH alias) |
| Remote path | Yes | `/opt/my-project` or `/home/ubuntu/my-project` |
| Project type | Auto-detect | Python / Node.js / Docker |
| Required env vars | Ask | `ANTHROPIC_API_KEY`, `TELEGRAM_BOT_TOKEN`, etc. |
| Post-deploy commands | Ask | `pip3 install -r requirements.txt`, `npm install` |
| Health check | Ask | URL to curl, process to check, or script to run |
| Telegram notify | No | on/off (default: off) |

### Generated Script Structure

```bash
#!/bin/bash
# Deploy [PROJECT] to [HOST]:[PATH]
# Usage: bash scripts/deploy.sh [--local]
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# === Standard excludes (always applied) ===
EXCLUDES=(
  --exclude '.git/'
  --exclude '__pycache__/'
  --exclude '*.pyc'
  --exclude '.env'
  --exclude '.env.local'
  --exclude '.env.production'
  --exclude 'node_modules/'
  --exclude 'venv/'
  --exclude '.venv/'
  --exclude 'dist/'
  --exclude '.next/'
  --exclude '.claude/'
  --exclude '*.sqlite3'
  --exclude '*.db'
  # Project-specific excludes:
  [CUSTOM_EXCLUDES]
)

if [ "${1:-}" = "--local" ]; then
    # === Run on VPS after rsync ===
    echo "=== Local setup on $(hostname) ==="

    [PYTHON_SETUP or NODE_SETUP]

    # Verify environment
    MISSING=""
    [ENV_VAR_CHECKS]
    if [ -n "$MISSING" ]; then
        echo "WARNING: Missing env vars:$MISSING"
        exit 1
    fi

    # Post-deploy commands
    [POST_DEPLOY_COMMANDS]

    # Health check
    [HEALTH_CHECK]

    [TELEGRAM_NOTIFY]

    echo "=== Deploy complete ==="

else
    VPS_HOST="[HOST]"
    VPS_DIR="[PATH]"

    echo "=== Deploying to $VPS_HOST:$VPS_DIR ==="

    rsync -avz --delete "${EXCLUDES[@]}" \
        "$PROJECT_DIR/" "$VPS_HOST:$VPS_DIR/"

    echo "Files synced. Running remote setup..."
    ssh "$VPS_HOST" "cd $VPS_DIR && bash scripts/deploy.sh --local"
fi
```

### Stack-Specific Sections

**Python projects:**
```bash
# Python setup
python3 --version
python3 -c "import sys; assert sys.version_info >= (3, 10)" || { echo "Python 3.10+ required"; exit 1; }
pip3 install -r requirements.txt --quiet
```

**Node.js projects:**
```bash
# Node setup
node --version
npm ci --production --quiet
```

**Custom excludes by stack:**
- Python: add `data/`, `logs/`, `backups/`, `cache/`, `backtest/`
- Node.js: add `dist/`, `.next/`, `build/`, `coverage/`
- Docker: add `docker-compose.override.yml`

### Health Check Patterns

```bash
# HTTP endpoint
curl -sf http://localhost:8000/api/health || { echo "HEALTH CHECK FAILED"; exit 1; }

# Process check
pgrep -f "uvicorn" > /dev/null || { echo "Process not running"; exit 1; }

# Script-based
python3 scripts/health_check.py || { echo "Health check script failed"; exit 1; }

# Cron verification
crontab -l | grep -q "run_morning" || echo "WARNING: Cron jobs not configured"
```

### Telegram Notification (optional)

```bash
# Only if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are set
if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
    MSG="✅ [PROJECT] deployed to $(hostname) at $(date '+%H:%M %Z')"
    curl -sf -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d chat_id="$TELEGRAM_CHAT_ID" -d text="$MSG" > /dev/null
fi
```

Place the generated script at `scripts/deploy.sh` and make it executable.

---

## Mode 2: Interactive Deploy

When the user says "deploy now" or "push to VPS".

### Pre-Flight Checks

1. **Uncommitted changes?** — `git status --porcelain`. Warn if dirty.
2. **Tests pass?** — Run the project's test command. Abort if failing.
3. **Confirm target** — Show host, path, and what will be synced. Ask for confirmation.

### Execute

1. Run rsync with standard + custom excludes
2. SSH in and run `--local` setup
3. Verify health check
4. Report result to user
5. Send Telegram notification if configured

### Rollback Hint

If health check fails after deploy:
```
Deploy health check FAILED. Options:
1. SSH in and check logs: ssh [HOST] "tail -50 [PATH]/logs/latest.log"
2. Rollback to previous version: git stash && scripts/deploy.sh (from last known good commit)
3. The old files are gone (rsync --delete). If you need recovery, check backups.
```

---

## Rules
- **Never deploy with uncommitted changes** without explicit user approval
- **Never deploy if tests fail** — abort and show failures
- **Always confirm before deploying** — show what's being sent and where
- **.env is always excluded** — secrets stay on the server, never in rsync
- **Health check is mandatory** — if the user doesn't specify one, suggest options based on stack
- **Databases are always excluded** — .db, .sqlite3 files never get rsynced
