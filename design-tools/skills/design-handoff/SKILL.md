---
name: design-handoff
disable-model-invocation: true
description: Generate developer handoff specs from a design. Use when a design is ready for engineering and needs specs covering layout, design tokens, component props, interaction states, responsive breakpoints, and edge cases.
argument-hint: "<Figma URL or design description>"
---

# /design-handoff

Generate comprehensive developer handoff documentation.

## What to Include

- **Visual**: Measurements, design tokens, responsive breakpoints, variants
- **Interaction**: Click/tap, hover states, transitions, gestures
- **Content**: Character limits, truncation, empty/loading/error states
- **Edge Cases**: Min/max content, i18n, slow connections, missing data
- **Accessibility**: Focus order, ARIA labels, keyboard interactions

## Output

```markdown
## Handoff Spec: [Feature/Screen]

### Design Tokens Used
| Token | Value | Usage |
|-------|-------|-------|

### Components
| Component | Variant | Props | Notes |
|-----------|---------|-------|-------|

### States and Interactions
| Element | State | Behavior |
|---------|-------|----------|

### Responsive Behavior
| Breakpoint | Changes |
|------------|---------|

### Edge Cases
- **Empty state**: [What to show]
- **Long text**: [Truncation rules]
- **Loading**: [Skeleton or spinner]
- **Error**: [Error state]

### Animation
| Element | Trigger | Animation | Duration | Easing |
|---------|---------|-----------|----------|--------|

### Accessibility Notes
- [Focus order, ARIA labels, keyboard interactions]
```

## Principles

1. **Don't assume** — Specify everything
2. **Use tokens, not values** — `spacing-md` not `16px`
3. **Show all states** — Default, hover, active, disabled, loading, error, empty
4. **Describe the why** — Helps developers make good judgment calls
