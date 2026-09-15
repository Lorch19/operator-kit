---
name: ux-copy
description: Write or review UX copy — microcopy, error messages, empty states, CTAs. TRIGGER with "write copy for", "what should this button say?", "review this error message", or when naming CTAs, wording dialogs, filling empty states, or writing onboarding text.
argument-hint: "<context or copy to review>"
---

# /ux-copy

Write or review UX copy for any interface context.

## What I Need

- **Context**: What screen, flow, or feature?
- **User state**: What are they trying to do? How are they feeling?
- **Tone**: Formal, friendly, playful, reassuring?
- **Constraints**: Character limits, platform guidelines?

## Principles

1. **Clear**: No jargon, no ambiguity
2. **Concise**: Fewest words with full meaning
3. **Consistent**: Same terms everywhere
4. **Useful**: Every word helps the user
5. **Human**: Helpful person, not a robot

## Copy Patterns

### CTAs
Start with a verb, be specific: "Create account" not "Submit"

### Error Messages
What happened + Why + How to fix

### Empty States
What this is + Why it's empty + How to start

### Confirmation Dialogs
Make action clear, describe consequences, label buttons with actions

## Output

```markdown
## UX Copy: [Context]

### Recommended Copy
**[Element]**: [Copy]

### Alternatives
| Option | Copy | Tone | Best For |
|--------|------|------|----------|

### Rationale
[Why this works]

### Localization Notes
[Anything translators should know]
```

## Tips

1. **Be specific about context** — "Error when payment fails" not just "error"
2. **Share brand voice** — "Professional but warm" helps tone
3. **Consider emotional state** — Errors need empathy, success can celebrate
