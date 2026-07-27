---
name: change-request
disable-model-invocation: true
description: Create a change management request with impact analysis and rollback plan. Use when proposing a system or process change that needs approval, preparing a change record for CAB review, documenting risk and rollback steps before a deployment, or planning stakeholder communications for a rollout.
argument-hint: "<change description>"
---

# /change-request

Create a structured change request with impact analysis, risk assessment, and rollback plan.

## Change Management Framework

### 1. Assess
- What is changing? Who is affected? How significant?

### 2. Plan
- Communication plan, training plan, support plan, timeline

### 3. Execute
- Announce the "why", train, monitor adoption, address resistance

### 4. Sustain
- Measure adoption, reinforce, document lessons learned

## Output

```markdown
## Change Request: [Title]
**Requester:** [Name] | **Date:** [Date] | **Priority:** [Critical/High/Medium/Low]

### Description
[What is changing and why]

### Business Justification
[Why this change is needed]

### Impact Analysis
| Area | Impact | Details |
|------|--------|---------|
| Users | [High/Med/Low] | [Who and how] |
| Systems | [High/Med/Low] | [What systems] |
| Processes | [High/Med/Low] | [What workflows] |

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|

### Implementation Plan
| Step | Owner | Timeline | Dependencies |
|------|-------|----------|--------------|

### Rollback Plan
- Trigger: [When to roll back]
- Steps: [How to roll back]
- Verification: [How to confirm]

### Approvals Required
| Approver | Role | Status |
|----------|------|--------|
```

## Tips

1. **Be specific about impact** — "200 users in billing" not "everyone"
2. **Always have a rollback plan**
3. **Communicate early** — Surprises create resistance
