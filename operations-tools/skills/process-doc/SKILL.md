---
name: process-doc
disable-model-invocation: true
description: Document a business process — flowcharts, RACI, and SOPs. Use when formalizing a process that lives in someone's head, building a RACI to clarify who owns what, writing an SOP for a handoff or audit, or capturing the exceptions and edge cases of how work actually gets done.
argument-hint: "<process name or description>"
---

# /process-doc

Document a business process as a complete standard operating procedure (SOP).

## How It Works

Walk me through the process — describe it, paste existing docs, or just tell me the name and I'll ask the right questions.

## Output

```markdown
## Process Document: [Process Name]
**Owner:** [Person/Team] | **Last Updated:** [Date] | **Review Cadence:** [Quarterly/Annually]

### Purpose
[Why this process exists]

### RACI Matrix
| Step | Responsible | Accountable | Consulted | Informed |
|------|------------|-------------|-----------|----------|

### Process Flow
[ASCII flowchart or step-by-step]

### Detailed Steps

#### Step 1: [Name]
- **Who**: [Role]
- **When**: [Trigger or timing]
- **How**: [Detailed instructions]
- **Output**: [What this step produces]

### Exceptions and Edge Cases
| Scenario | What to Do |
|----------|-----------|

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
```

## Tips

1. **Start messy** — Tell me how it works today, I'll structure it
2. **Include the exceptions** — "Usually X, but sometimes Y" is the most valuable part
3. **Name the people** — Who does what today
