---
name: architecture
disable-model-invocation: true
description: Create or evaluate an architecture decision record (ADR). Use when choosing between technologies (e.g., Kafka vs SQS), documenting a design decision with trade-offs, reviewing a system design proposal, or designing a new component from requirements and constraints.
argument-hint: "<decision or system to design>"
---

# /architecture

Create an Architecture Decision Record (ADR) or evaluate a system design.

## Modes

- **Create an ADR**: "Should we use Kafka or SQS for our event bus?"
- **Evaluate a design**: "Review this microservices proposal"
- **System design**: "Design the notification system for our app"

## Output — ADR Format

```markdown
# ADR-[number]: [Title]

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** [Date] | **Deciders:** [Who]

## Context
[Situation and forces at play]

## Decision
[The change we're proposing]

## Options Considered

### Option A: [Name]
| Dimension | Assessment |
|-----------|------------|
| Complexity | [Low/Med/High] |
| Cost | [Assessment] |
| Scalability | [Assessment] |
| Team familiarity | [Assessment] |

**Pros:** [List] | **Cons:** [List]

### Option B: [Name]
[Same format]

## Trade-off Analysis
[Key trade-offs with clear reasoning]

## Consequences
- [What becomes easier]
- [What becomes harder]

## Action Items
1. [ ] [Implementation step]
```

## Tips

1. **State constraints upfront** — "Must ship in 2 weeks" or "Must handle 10K rps"
2. **Name your options** — Explicit alternatives give a more balanced analysis
3. **Include non-functional requirements** — Latency, cost, expertise, maintenance
