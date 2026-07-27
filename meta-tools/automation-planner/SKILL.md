---
name: automation-planner
disable-model-invocation: true
description: >-
  Plan and configure background automations, scheduled tasks, and cron jobs with
  production-grade safety patterns. Use when setting up recurring agents, scheduled
  scripts, monitoring jobs, or any background automation. Covers scheduling, failure
  handling, concurrency, and monitoring.
  Do NOT use for one-off scripts or manual workflows.
type: workflow
---

# Automation Planner

## Purpose

Background automations are powerful but dangerous when misconfigured. This skill helps you design reliable scheduled tasks with proper safety guards — failure thresholds, timeouts, concurrency control, and monitoring.

## When to Use

- Setting up a new cron job or scheduled task
- Configuring background agents (Claude Code scheduled tasks, VPS cron, CI/CD)
- Designing a monitoring/alerting pipeline
- Planning recurring data collection or reporting
- Any automation that runs without human supervision

## Planning Checklist

For every automation, answer these questions before deploying:

### 1. What Does It Do?
- **Task name:** Clear, descriptive (e.g., `daily-dependency-check`, `hourly-inbox-triage`)
- **Description:** One sentence explaining what and why
- **Prompt/Script:** The actual instructions or code to execute
- **Expected output:** What does success look like?

### 2. Schedule Configuration

| Pattern | Cron Expression | Use When |
|---------|----------------|----------|
| Every 15 minutes | `*/15 * * * *` | Real-time monitoring, queue processing |
| Hourly | `0 * * * *` | Status checks, data sync |
| Daily at 9am | `0 9 * * *` | Morning briefs, daily reports |
| Weekdays at 9am | `0 9 * * 1-5` | Business-day tasks |
| Weekly Monday 9am | `0 9 * * 1` | Weekly summaries, reviews |
| Monthly 1st at midnight | `0 0 1 * *` | Monthly reports, cleanup |

**Rules:**
- Minimum interval: 15 minutes (shorter = usually a design smell)
- Avoid :00 and :30 marks when exact timing doesn't matter (reduces API thundering herd)
- Always specify timezone explicitly
- For load-sensitive tasks, add 1-5 minute jitter

### 3. Safety Guards

#### Concurrency Control
- **One at a time:** Only one instance runs at a time. If the previous run isn't finished, skip this run.
- **Queue:** Allow stacking but limit queue depth (e.g., max 3 pending)
- **Replace:** Kill the running instance and start fresh

**Default recommendation:** One at a time. Prevents resource conflicts and data corruption.

#### Failure Handling
```
failure_threshold: 3          # Auto-pause after N consecutive failures
timeout_minutes: 30           # Kill if running longer than this
retry_delay_minutes: 5        # Wait before retrying after failure
reset_on_success: true        # Reset failure counter on any success
```

**Circuit breaker pattern:**
1. First failure → log warning, retry on next schedule
2. Second failure → log error, retry on next schedule
3. Third failure → **auto-pause**, send alert, require manual re-enable

#### Timeout Protection
- Set a timeout for EVERY automation. No exceptions.
- Default: 2x the expected runtime
- Maximum: 90 minutes (if it takes longer, it should be a different architecture)

### 4. Monitoring & Alerting

For each automation, define:
- **Health check:** How do you know it's working? (log output, file created, API response)
- **Alert on failure:** Who gets notified and how? (Telegram, email, Slack)
- **Alert on degradation:** What metrics indicate the automation is struggling before it fails?

**Status model:**
| Status | Meaning |
|--------|---------|
| **Enabled** | Running on schedule, no issues |
| **Degraded** | Running but has had 1-2 recent failures |
| **Paused** | Auto-paused after hitting failure threshold |
| **Disabled** | Manually turned off |

### 5. Resource Considerations

- **API rate limits:** Does this automation hit external APIs? What's the rate limit? Add backoff.
- **Storage:** Does it create files/logs? Set up rotation or cleanup.
- **Cost:** If using paid APIs (LLM calls, cloud functions), estimate monthly cost at full schedule.
- **Dependencies:** What external services must be available? What happens if they're down?

## Automation Specification Template

```yaml
name: {task-name}
description: {one-line description}
schedule:
  cron: "{expression}"
  timezone: "{IANA timezone}"
safety:
  concurrency: one-at-a-time
  failure_threshold: 3
  timeout_minutes: 30
  retry_delay_minutes: 5
monitoring:
  health_check: "{how to verify success}"
  alert_channel: "{telegram|email|slack}"
  alert_on: [failure, degradation, timeout]
resources:
  api_limits: "{relevant limits}"
  estimated_cost: "{monthly cost}"
  dependencies: ["{service1}", "{service2}"]
prompt: |
  {The actual task instructions}
```

## Common Patterns

### Morning Brief Generator
```yaml
name: morning-brief
schedule:
  cron: "0 8 * * 1-5"
  timezone: "Asia/Jerusalem"
safety:
  timeout_minutes: 10
  failure_threshold: 3
```

### Dependency/Security Check
```yaml
name: dependency-audit
schedule:
  cron: "0 6 * * 1"  # Weekly Monday 6am
safety:
  timeout_minutes: 15
  concurrency: one-at-a-time
```

### Inbox Triage Agent
```yaml
name: inbox-triage
schedule:
  cron: "*/30 * * * *"  # Every 30 min
safety:
  timeout_minutes: 5
  failure_threshold: 5  # Higher threshold for frequent tasks
```

## Anti-Patterns

- **No timeout** — Every automation MUST have a timeout. Runaway processes waste resources and can corrupt data.
- **No failure handling** — Without a circuit breaker, a broken automation will retry forever, burning API credits and filling logs.
- **Too frequent** — If you're running every minute, you probably need a different architecture (event-driven, webhook, queue).
- **Silent failures** — If nobody gets alerted, nobody fixes it. Always configure alerts.
- **Hardcoded credentials** — Use environment variables or secret managers. Never put API keys in the automation config.
- **No idempotency** — Automations should be safe to re-run. If running twice causes problems, add deduplication logic.
