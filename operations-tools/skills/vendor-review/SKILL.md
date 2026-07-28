---
name: vendor-review
disable-model-invocation: true
description: Evaluate a vendor — cost analysis, risk assessment, and recommendation. Use when reviewing a new vendor proposal, deciding whether to renew or replace a contract, comparing vendors side-by-side, or building a TCO breakdown before procurement sign-off.
argument-hint: "<vendor name or proposal>"
---

# /vendor-review

Evaluate a vendor with structured analysis covering cost, risk, performance, and fit.

## What I Need From You

- **Vendor name**: Who are you evaluating?
- **Context**: New evaluation, renewal, or comparison?
- **Details**: Contract terms, pricing, proposal document, or performance data

## Evaluation Framework

### Cost Analysis (TCO)
- License/subscription, implementation, training, support, exit costs

### Risk Assessment
- Financial stability, security posture, concentration risk, lock-in, BC/DR

### Performance
- SLA compliance, support response times, uptime, feature cadence

## Output

```markdown
## Vendor Review: [Vendor Name]
**Date:** [Date] | **Type:** [New / Renewal / Comparison]

### Summary
[2-3 sentence recommendation]

### Cost Analysis
| Component | Annual Cost | Notes |
|-----------|-------------|-------|

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|

### Strengths & Concerns
- Strengths: [list]
- Concerns: [list]

### Recommendation
[Proceed / Negotiate / Pass] — [Reasoning]

### Negotiation Points
- [Leverage point 1]
```

## Tips

1. **Upload the proposal** — I can extract pricing, terms, and SLAs
2. **Compare vendors** — "Compare A vs B" gets side-by-side analysis
3. **Include current spend** — For renewals, knowing current costs helps
