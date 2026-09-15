---
name: accessibility-review
description: Run a WCAG 2.1 AA accessibility audit on a design or page. TRIGGER with "audit accessibility", "check a11y", "is this accessible?", or when reviewing for color contrast, keyboard navigation, touch targets, or screen reader behavior.
argument-hint: "<Figma URL, URL, or description>"
---

# /accessibility-review

Audit a design or page for WCAG 2.1 AA compliance.

## WCAG 2.1 AA Quick Reference

### Perceivable
- **1.1.1** Non-text content has alt text
- **1.3.1** Info conveyed semantically
- **1.4.3** Contrast >= 4.5:1 (normal), >= 3:1 (large)
- **1.4.11** Non-text contrast >= 3:1

### Operable
- **2.1.1** All functionality via keyboard
- **2.4.3** Logical focus order
- **2.4.7** Visible focus indicator
- **2.5.5** Touch target >= 44x44px

### Understandable
- **3.2.1** No unexpected changes on focus
- **3.3.1** Error identification
- **3.3.2** Labels for inputs

### Robust
- **4.1.2** Name, role, value for all UI components

## Testing Approach

1. Automated scan (catches ~30%)
2. Keyboard-only navigation
3. Screen reader testing
4. Color contrast verification
5. Zoom to 200%

## Output

```markdown
## Accessibility Audit: [Name]
**Standard:** WCAG 2.1 AA

### Summary
**Issues:** [X] | **Critical:** [X] | **Major:** [X] | **Minor:** [X]

### Findings
| # | Issue | WCAG | Severity | Fix |
|---|-------|------|----------|-----|

### Color Contrast
| Element | FG | BG | Ratio | Required | Pass? |
|---------|----|----|-------|----------|-------|

### Keyboard Navigation
| Element | Tab Order | Enter/Space | Escape |
|---------|-----------|-------------|--------|

### Priority Fixes
1. [Critical fix]
2. [Major fix]
```

## Tips

1. **Start with contrast and keyboard** — Most common and impactful
2. **Test with assistive technology** — VoiceOver/NVDA catches more
3. **Prioritize by impact** — Fix blocking issues first
