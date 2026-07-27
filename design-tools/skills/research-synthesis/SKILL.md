---
name: research-synthesis
disable-model-invocation: true
description: Synthesize user research into themes, insights, and recommendations. Use when you have interview transcripts, survey results, usability test notes, or support tickets that need distilling into patterns and prioritized next steps.
argument-hint: "<research data, transcripts, or survey results>"
---

# /research-synthesis

Synthesize user research data into actionable insights.

## What I Accept

- Interview transcripts or notes
- Survey results (CSV, pasted data)
- Usability test recordings or notes
- Support tickets or feedback
- NPS/CSAT responses, app store reviews

## Output

```markdown
## Research Synthesis: [Study Name]
**Method:** [Type] | **Participants:** [X] | **Date:** [Range]

### Executive Summary
[3-4 sentence overview]

### Key Themes

#### Theme 1: [Name]
**Prevalence:** [X of Y participants]
**Summary:** [Description]
**Supporting Evidence:**
- "[Quote]" — P[X]
**Implication:** [Product impact]

### Insights → Opportunities
| Insight | Opportunity | Impact | Effort |
|---------|-------------|--------|--------|

### User Segments
| Segment | Characteristics | Needs | Size |
|---------|----------------|-------|------|

### Recommendations
1. **[High priority]** — [Why, based on which findings]

### Questions for Further Research
- [What we still don't know]
```

## Tips

1. **Include raw quotes** — Makes insights credible and memorable
2. **Separate observations from interpretations**
3. **Quantify where possible** — "7 of 10 users" not "most users"
