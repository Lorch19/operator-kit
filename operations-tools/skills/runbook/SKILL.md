---
name: runbook
disable-model-invocation: true
description: Create or update an operational runbook for a recurring task or procedure. Use when documenting a task that on-call or ops needs to run repeatably, turning tribal knowledge into exact step-by-step commands, adding troubleshooting and rollback steps, or writing escalation paths.
argument-hint: "<process or task name>"
---

# /runbook

Create a step-by-step operational runbook for a recurring task or procedure.

## Output

```markdown
## Runbook: [Task Name]
**Owner:** [Team/Person] | **Frequency:** [Daily/Weekly/Monthly/As Needed]
**Last Updated:** [Date]

### Purpose
[What this runbook accomplishes and when to use it]

### Prerequisites
- [ ] [Access or permission needed]
- [ ] [Tool or system required]

### Procedure

#### Step 1: [Name]
```
[Exact command or instruction]
```
**Expected result:** [What should happen]
**If it fails:** [What to do]

### Verification
- [ ] [How to confirm success]

### Troubleshooting
| Symptom | Likely Cause | Fix |
|---------|-------------|-----|

### Rollback
[How to undo if something goes wrong]

### Escalation
| Situation | Contact | Method |
|-----------|---------|--------|
```

## Tips

1. **Be painfully specific** — "Run `python sync.py --prod --dry-run` from the ops server"
2. **Include failure modes** — What can go wrong at each step
3. **Test the runbook** — Have someone unfamiliar follow it
