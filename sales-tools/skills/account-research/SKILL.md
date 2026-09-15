---
name: account-research
description: Research a company or person and get actionable sales intel. Works standalone with web search, supercharged with enrichment tools or CRM. TRIGGER with "research [company]", "look up [person]", "intel on [prospect]", "who is [name] at [company]", or "tell me about [company]".
---

# Account Research

Get a complete picture of any company or person before outreach.

## How It Works

1. **Parse Request** — Company name, person, or both
2. **Web Search** — Company overview, recent news, hiring signals, key people, product/service
3. **Enrichment** (if connected) — Verified emails, tech stack, org chart
4. **CRM Check** (if connected) — Prior relationship, past opportunities
5. **Synthesize** — Actionable output

## Output

```markdown
## Account Research: [Company]

### Quick Take
[2-3 sentence summary with qualification signal]

### Company Profile
- Industry, size, HQ, founded, funding

### Recent News
- [Relevant events, funding, leadership changes]

### Hiring Signals
- [Open roles indicating priorities]

### Key People
| Name | Title | Talking Points |
|------|-------|---------------|

### Qualification Signals
[Why this is/isn't a good fit]

### Recommended Approach
- [Outreach strategy]
- [Discovery questions to ask]
```
