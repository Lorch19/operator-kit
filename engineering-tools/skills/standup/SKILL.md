---
name: standup
disable-model-invocation: true
description: Generate a standup update from recent activity. Use when preparing for daily standup, summarizing yesterday's commits/PRs/tickets, formatting into yesterday/today/blockers, or structuring rough notes into a shareable update.
argument-hint: "[yesterday | today | blockers]"
---

# /standup

Generate a standup update by pulling together recent activity.

## What I Need

**Option A: Let me pull it** — If tools are connected, just say `/standup`
**Option B: Tell me what you did** — "Worked on auth migration, reviewed 3 PRs, blocked on rate limiting"

## Output

```markdown
## Standup — [Date]

### Yesterday
- [Completed item with ticket reference]

### Today
- [Planned item with ticket reference]

### Blockers
- [Blocker with context and who can help]
```

## Tips

1. **Run it every morning** — Build a habit
2. **Add context** — Nuance about blockers or priorities
3. **Share format** — Ask for Slack, email, or team-specific format
