---
name: design-system
disable-model-invocation: true
description: Audit, document, or extend your design system. Use when checking for naming inconsistencies, writing component documentation, or designing new patterns that fit the existing system.
argument-hint: "[audit | document | extend] <component or system>"
---

# /design-system

Manage your design system — audit, document, or extend.

## Modes

```
/design-system audit                    # Full system audit
/design-system document [component]     # Document a component
/design-system extend [pattern]         # Design new component/pattern
```

## System Components

### Design Tokens
Colors, typography, spacing, borders, shadows, motion

### Components
Variants, states (default/hover/active/disabled/loading/error), sizes, behavior, accessibility

### Patterns
Forms, navigation, data display, feedback (toasts, modals, inline messages)

## Output — Audit

```markdown
## Design System Audit
**Components:** [X] | **Issues:** [X] | **Score:** [X/100]

### Token Coverage
| Category | Defined | Hardcoded Values Found |
|----------|---------|----------------------|

### Component Completeness
| Component | States | Variants | Docs | Score |
|-----------|--------|----------|------|-------|

### Priority Actions
1. [Most impactful improvement]
```

## Output — Document

```markdown
## Component: [Name]
### Variants, Props, States, Accessibility, Do's and Don'ts
```

## Output — Extend

```markdown
## New Component: [Name]
### Problem, Existing Patterns, Proposed API, Tokens, Accessibility, Open Questions
```

## Principles

1. **Consistency over creativity**
2. **Flexibility within constraints**
3. **Document everything**
4. **Version and migrate**
