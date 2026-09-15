---
name: design-critique
description: Get structured design feedback on usability, hierarchy, and consistency. TRIGGER with "review this design", "critique this mockup", "what do you think of this screen?", or when sharing a Figma link or screenshot for feedback.
argument-hint: "<Figma URL, screenshot, or description>"
---

# /design-critique

Get structured design feedback across multiple dimensions.

## What I Need

- **The design**: Figma URL, screenshot, or description
- **Context**: What is this? Who is it for? What stage?
- **Focus** (optional): "Focus on mobile" or "Focus on onboarding"

## Critique Framework

### 1. First Impression (2 seconds)
- What draws the eye? Is that correct?
- Is the purpose immediately clear?

### 2. Usability
- Can the user accomplish their goal?
- Are interactive elements obvious?

### 3. Visual Hierarchy
- Clear reading order? Right elements emphasized?
- Whitespace and typography hierarchy?

### 4. Consistency
- Follows design system? Spacing/colors/typography consistent?

### 5. Accessibility
- Color contrast, touch targets, text readability

## Output

```markdown
## Design Critique: [Name]

### Overall Impression
[What works, biggest opportunity]

### Usability
| Finding | Severity | Recommendation |
|---------|----------|----------------|

### Visual Hierarchy
- **Eye draws to**: [Element] — [Correct?]
- **Reading flow**: [Description]

### Consistency Issues
| Element | Issue | Fix |
|---------|-------|-----|

### What Works Well
- [Positive observations]

### Priority Recommendations
1. [Most impactful change]
2. [Second priority]
```

## Tips

1. **Share context** — "Checkout flow for B2B SaaS" helps relevance
2. **Specify stage** — Exploration gets different feedback than final polish
3. **Ask to focus** — "Just look at navigation" gives more depth
