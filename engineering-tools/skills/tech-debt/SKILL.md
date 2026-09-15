---
name: tech-debt
description: Identify, categorize, and prioritize technical debt. TRIGGER with "tech debt", "technical debt audit", "what should we refactor", "code health", or when evaluating refactoring priorities or maintenance backlog.
---

# Tech Debt Management

Systematically identify, categorize, and prioritize technical debt.

## Categories

| Type | Examples | Risk |
|------|----------|------|
| **Code debt** | Duplicated logic, poor abstractions | Bugs, slow development |
| **Architecture debt** | Wrong data store, monolith needs splitting | Scaling limits |
| **Test debt** | Low coverage, flaky tests | Regressions ship |
| **Dependency debt** | Outdated/unmaintained libraries | Security vulns |
| **Documentation debt** | Missing runbooks, tribal knowledge | Onboarding pain |
| **Infrastructure debt** | Manual deploys, no monitoring | Incidents, slow recovery |

## Prioritization

Score each item:
- **Impact**: How much does it slow the team? (1-5)
- **Risk**: What happens if we don't fix it? (1-5)
- **Effort**: How hard is the fix? (1-5, inverted)

Priority = (Impact + Risk) × (6 - Effort)

## Output

Prioritized list with estimated effort, business justification, and phased remediation plan alongside feature work.
