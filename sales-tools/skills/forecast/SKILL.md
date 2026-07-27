---
name: forecast
disable-model-invocation: true
description: Generate a weighted sales forecast with best/likely/worst scenarios, commit vs. upside breakdown, and gap analysis. Use when preparing a quarterly forecast call, assessing gap-to-quota, deciding which deals to commit vs. call upside, or checking pipeline coverage.
argument-hint: "<period>"
---

# /forecast

Generate a weighted sales forecast with scenario analysis.

## What I Need

- Quota for the period
- Deals (CSV, pasted, or described)
- Already-closed amount
- Timeline

## Default Stage Probabilities

| Stage | Probability |
|-------|------------|
| Negotiation | 80% |
| Proposal | 60% |
| Evaluation | 40% |
| Discovery | 20% |
| Prospecting | 10% |

## Output

```markdown
## Forecast: [Period]

### Summary
| Metric | Value |
|--------|-------|
| Quota | $[X] |
| Closed | $[X] |
| Pipeline | $[X] |
| Weighted Forecast | $[X] |
| Gap | $[X] |
| Coverage Ratio | [X]x |

### Scenarios
| Scenario | Amount | Assumptions |
|----------|--------|-------------|
| Best | $[X] | [Key deals close] |
| Likely | $[X] | [Weighted by stage] |
| Worst | $[X] | [Only commits] |

### Commit vs. Upside
| Category | Amount | Deals |
|----------|--------|-------|

### Risk Flags
- [Deal with risk and reason]

### Gap Analysis
- [Options to close the gap]
```
