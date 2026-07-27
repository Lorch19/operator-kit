---
name: deploy-checklist
disable-model-invocation: true
description: Pre-deployment verification checklist. Use when about to ship a release, deploying with database migrations or feature flags, verifying CI status and approvals before production, or documenting rollback triggers.
argument-hint: "[service or release name]"
---

# /deploy-checklist

Generate a pre-deployment checklist to verify readiness.

## Output

```markdown
## Deploy Checklist: [Service/Release]
**Date:** [Date] | **Deployer:** [Name]

### Pre-Deploy
- [ ] All tests passing in CI
- [ ] Code reviewed and approved
- [ ] No known critical bugs
- [ ] Database migrations tested (if applicable)
- [ ] Feature flags configured (if applicable)
- [ ] Rollback plan documented
- [ ] On-call team notified

### Deploy
- [ ] Deploy to staging and verify
- [ ] Run smoke tests
- [ ] Deploy to production (canary if available)
- [ ] Monitor error rates and latency for 15 min

### Post-Deploy
- [ ] Confirm metrics are nominal
- [ ] Update release notes / changelog
- [ ] Notify stakeholders
- [ ] Close related tickets

### Rollback Triggers
- Error rate exceeds [X]%
- P50 latency exceeds [X]ms
- [Critical user flow] fails
```

## Customization

Tell me about your deploy and I'll customize:
- "We use feature flags" → flag verification steps
- "Database migration" → migration-specific checks
- "Breaking API change" → consumer notification steps
