---
name: status-report
disable-model-invocation: true
description: Generate a status report with KPIs, risks, and action items. Use when writing a weekly or monthly update for leadership, summarizing project health with green/yellow/red status, surfacing risks and decisions that need stakeholder attention, or turning project tracker activity into a readable narrative.
argument-hint: "[weekly | monthly | quarterly] [project or team]"
---

# /status-report

Generate a polished status report for leadership or stakeholders.

## Output

```markdown
## Status Report: [Project/Team] — [Period]
**Author:** [Name] | **Date:** [Date]

### Executive Summary
[3-4 sentence overview]

### Overall Status: 🟢 On Track / 🟡 At Risk / 🔴 Off Track

### Key Metrics
| Metric | Target | Actual | Trend | Status |
|--------|--------|--------|-------|--------|

### Accomplishments This Period
- [Win 1]
- [Win 2]

### In Progress
| Item | Owner | Status | ETA |
|------|-------|--------|-----|

### Risks and Issues
| Risk/Issue | Impact | Mitigation | Owner |
|------------|--------|------------|-------|

### Decisions Needed
| Decision | Context | Deadline | Recommended Action |
|----------|---------|----------|--------------------|

### Next Period Priorities
1. [Priority 1]
2. [Priority 2]
```

## Tips

1. **Lead with the headline** — Busy leaders read the first 3 lines
2. **Be honest about risks** — Surfacing issues early builds trust
3. **Make decisions easy** — Context + recommendation for each
