---
name: adr-writer
disable-model-invocation: true
description: >-
  Write Architecture Decision Records (ADRs) that document technical and product decisions
  with structured rationale, alternatives, and consequences. Use when making significant
  architectural, infrastructure, or product decisions that should be recorded for future reference.
  Do NOT use for minor implementation choices or style preferences.
type: workflow
---

# ADR Writer

## Purpose

Architecture Decision Records capture the **why** behind significant decisions — architectural choices, technology selections, process changes, integration patterns. They prevent future teams (or future you) from re-litigating settled questions or accidentally undoing intentional trade-offs.

## When to Write an ADR

- Choosing between technologies, frameworks, or vendors
- Defining system boundaries or integration patterns
- Establishing conventions that affect multiple components
- Making trade-offs with lasting consequences (security vs. UX, speed vs. cost)
- Changing a previous decision (superseding an older ADR)

## ADR Template

```markdown
# ADR-{NUMBER}: {Decision Title}

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-{N}
**Date:** {YYYY-MM-DD}
**Decision Makers:** {Who was involved}

## Context

What is the issue or situation that motivates this decision? Include:
- The problem or need
- Relevant constraints (technical, business, timeline, team)
- What triggered this decision now

## Decision

State the decision clearly in 1-2 sentences. Be specific.

> We will {do X} because {primary reason}.

## Alternatives Considered

| Option | Pros | Cons | Why Not |
|--------|------|------|---------|
| {Option A} | ... | ... | ... |
| {Option B} | ... | ... | ... |
| {Chosen option} | ... | ... | **Selected** |

## Consequences

### Positive
- What becomes easier or better

### Negative
- What becomes harder or what we give up

### Risks
- What could go wrong and how we'd detect it

## Implementation Notes

- Key boundaries or rules to enforce
- What changes in the codebase
- Migration path if replacing something existing
```

## Process

### Step 1: Understand the Decision
Ask the user:
- What decision are you making?
- What triggered it? (incident, scaling issue, new requirement, tech debt)
- Who else is involved in this decision?
- What constraints matter most? (cost, speed, security, simplicity, team skill)

### Step 2: Map Alternatives
For each option considered:
- What are the concrete pros and cons?
- Has anyone on the team used this before?
- What's the switching cost if this doesn't work?

### Step 3: Draft the ADR
Write the ADR using the template above. Be:
- **Specific** — "We chose PostgreSQL over DynamoDB" not "We chose a database"
- **Honest about trade-offs** — Every decision has downsides. Name them.
- **Forward-looking** — What would make us revisit this decision?

### Step 4: Review
Check that the ADR answers:
- [ ] Could a new team member understand WHY this decision was made?
- [ ] Are the alternatives genuinely considered (not strawmen)?
- [ ] Are consequences realistic, not just the happy path?
- [ ] Is the status correct?

## Naming Convention

Store ADRs in a `docs/adr/` or `decisions/` directory:
```
docs/adr/
├── 0001-single-provider-scm-boundaries.md
├── 0002-shared-session-contracts.md
├── 0003-authentication-token-strategy.md
```

Use sequential numbering with kebab-case titles.

## Anti-Patterns

- **ADR as documentation dump** — An ADR is a decision record, not a design doc. Keep it focused on the choice.
- **Missing alternatives** — If you only list the chosen option, it's not a decision record, it's an announcement.
- **Vague consequences** — "This might cause issues" helps no one. Be specific about what could go wrong.
- **Never updating status** — When a decision is superseded, mark it and link to the new ADR.
