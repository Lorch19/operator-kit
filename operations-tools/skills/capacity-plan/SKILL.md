---
name: capacity-plan
disable-model-invocation: true
description: Plan resource capacity — workload analysis and utilization forecasting. Use when heading into quarterly planning, the team feels overallocated and you need the numbers, deciding whether to hire or deprioritize, or stress-testing whether upcoming projects fit the people you have.
argument-hint: "<team or project scope>"
---

# /capacity-plan

Analyze team capacity and plan resource allocation.

## What I Need From You

- **Team size and roles**: Who do you have?
- **Current workload**: What are they working on?
- **Upcoming work**: What's coming next quarter?
- **Constraints**: Budget, hiring timeline, skill requirements

## Utilization Targets

| Role Type | Target | Notes |
|-----------|--------|-------|
| IC / Specialist | 75-80% | Leave room for reactive work and growth |
| Manager | 60-70% | Management overhead, meetings, 1:1s |
| On-call / Support | 50-60% | Interrupt-driven work is unpredictable |

## Output

```markdown
## Capacity Plan: [Team/Project]
**Period:** [Date range] | **Team Size:** [X]

### Current Utilization
| Person/Role | Capacity | Allocated | Available | Utilization |
|-------------|----------|-----------|-----------|-------------|

### Capacity Summary
- **Total capacity**: [X] hours/week
- **Currently allocated**: [X] hours/week ([X]%)
- **Available**: [X] hours/week ([X]%)

### Upcoming Demand
| Project/Initiative | Start | End | Resources Needed | Gap |
|--------------------|-------|-----|-----------------|-----|

### Bottlenecks & Recommendations
1. [Hire / Contract / Reprioritize / Delay]

### Scenarios
| Scenario | Outcome |
|----------|---------|
| Do nothing | [What happens] |
| Hire [X] | [What changes] |
| Deprioritize [Y] | [What frees up] |
```

## Tips

1. **Include all work** — BAU, projects, support, meetings
2. **Plan for buffer** — Target 80% utilization
3. **Update regularly** — Review monthly
