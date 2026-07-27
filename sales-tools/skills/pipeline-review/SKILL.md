---
name: pipeline-review
disable-model-invocation: true
description: Analyze pipeline health — prioritize deals, flag risks, get weekly action plan. Use when running a weekly pipeline review, deciding which deals to focus on, spotting stale opportunities, or auditing pipeline hygiene.
argument-hint: "<segment or rep>"
---

# /pipeline-review

Analyze pipeline health with prioritized actions.

## What I Accept

- CSV export from CRM
- Pasted deal list
- Verbal description of pipeline

## Pipeline Health Score (0-100)

Scored across 4 dimensions:
- **Stage progression** — Are deals moving?
- **Activity recency** — When was last touch?
- **Close date accuracy** — Are dates realistic?
- **Contact coverage** — Multi-threaded or single-threaded?

## Prioritization Weights

| Factor | Weight |
|--------|--------|
| Close Date | 30% |
| Deal Size | 25% |
| Stage | 20% |
| Activity | 15% |
| Risk | 10% |

## Output

```markdown
## Pipeline Review — [Date]

### Pipeline Health Score: [X]/100

### Priority Actions This Week
1. [Action with deal context]

### Deal Prioritization
| Deal | Stage | Size | Risk | Action |
|------|-------|------|------|--------|

### Risk Flags
- [Stale 14+ days, stuck 30+ days, past close date, single-threaded]

### Hygiene Issues
- [Bad close dates, missing fields]

### Pipeline Shape
[By stage, close month, deal size distribution]

### Deals to Consider Removing
- [Deal with reason]
```
