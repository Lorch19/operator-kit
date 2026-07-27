---
name: call-summary
disable-model-invocation: true
description: Process call notes or transcript — extract action items, draft follow-up email, generate internal summary. Use when pasting notes after a discovery/demo/negotiation call, drafting a customer follow-up, or capturing objections and next steps.
argument-hint: "<call notes or transcript>"
---

# /call-summary

Process call notes or transcript into structured output.

## What I Accept

- Rough notes from a call
- Full transcripts (Gong, Fireflies, etc.)
- Informal description of what happened

## Output

```markdown
## Call Summary: [Company] — [Date]

### Internal Summary
**Attendees:** [List]
**Meeting Type:** [Discovery/Demo/Negotiation/QBR]

### Key Discussion Points
- [Point 1]

### Customer Priorities
1. [Priority with context]

### Objections Raised
| Objection | Our Response | Status |
|-----------|-------------|--------|

### Competitive Intel
- [Competitor mentions]

### Action Items
| Action | Owner | Due |
|--------|-------|-----|

### Next Steps
- [Agreed next step with date]

### Deal Impact
[How this call changes the deal outlook]
```

### Follow-Up Email
[Plain text follow-up email draft]
