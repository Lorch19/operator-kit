---
name: product-manager-toolkit
disable-model-invocation: true
description: >-
  Comprehensive toolkit for product managers including RICE prioritization, customer interview analysis, PRD templates, discovery frameworks, and go-to-market strategies.
  Use when you need RICE prioritization or customer interview analysis with Python scripts.
  DO NOT use for strategic prioritization framework selection — use dean-peters prioritization-advisor instead.
type: workflow
best_for:
  - "RICE scoring and feature prioritization"
  - "Analyzing customer interview transcripts"
  - "PRD template selection and drafting"
---

# Product Manager Toolkit

Essential tools and frameworks for modern product management, from discovery to delivery.

## When to Use

- **RICE prioritization** of a feature backlog → run `scripts/rice_prioritizer.py`
- **Customer interview analysis** from transcripts → run `scripts/customer_interview_analyzer.py`
- **PRD drafting** from a template → see `references/prd_templates.md`
- **Framework reference** (RICE formula, MoSCoW, Kano, JTBD) → see `references/frameworks.md`

## What NOT to Use This For

- **Choosing which prioritization framework to use** → use `prioritization-advisor` instead
- **Writing a full PRD from scratch** → use `prd-partner` or `prd-development` instead
- **Strategic roadmap planning** → use `roadmap-planning` instead
- **Customer discovery process design** → use `discovery-process` instead

---

## Core Workflows

### Feature Prioritization

```
Gather → Score → Analyze → Plan → Validate → Execute
```

1. **Gather** feature requests from customer feedback, sales, tech debt, and strategic initiatives
2. **Score** with RICE:
   ```bash
   python scripts/rice_prioritizer.py features.csv --capacity 20
   ```
3. **Analyze** portfolio: quick wins vs big bets, effort distribution, strategic alignment
4. **Generate roadmap**: quarterly capacity, dependencies, communication plan
5. **Validate**: compare priorities against goals, run sensitivity analysis, check with stakeholders
6. **Execute**: share roadmap, track actual vs estimated effort, revisit quarterly

See `references/tools-reference.md` for CSV format, command options, and example output.

### Customer Discovery

```
Plan → Recruit → Interview → Analyze → Synthesize → Validate
```

1. **Plan**: define research questions, identify segments, create interview script
2. **Recruit**: 5-8 per segment, mix power users and churned
3. **Interview**: semi-structured, focus on problems not solutions, record with permission
4. **Analyze**:
   ```bash
   python scripts/customer_interview_analyzer.py transcript.txt
   ```
   Extracts: pain points with severity, feature requests, JTBD patterns, sentiment, key quotes
5. **Synthesize**: group pain points, identify patterns (3+ mentions), map to opportunity areas
6. **Validate**: create solution hypotheses, test with prototypes, measure behavior vs stated preference

### PRD Development

```
Scope → Draft → Review → Refine → Approve → Track
```

1. **Choose template** from `references/prd_templates.md` (Standard, One-Page, Feature Brief, or Agile Epic)
2. **Draft**: lead with problem statement, define success metrics, state out-of-scope, include wireframes
3. **Review cycle**: engineering (feasibility), design (UX), sales (market), support (ops)
4. **Refine**: address constraints, adjust scope, document trade-offs
5. **Approve and kick off**: stakeholder sign-off, sprint planning, team communication
6. **Track**: compare metrics vs targets, user feedback, document learnings

---

## Quick Reference

```bash
# Prioritization
python scripts/rice_prioritizer.py features.csv --capacity 15

# Interview Analysis
python scripts/customer_interview_analyzer.py interview.txt

# Generate sample data
python scripts/rice_prioritizer.py sample

# JSON output (for integration with Jira, dashboards, etc.)
python scripts/rice_prioritizer.py features.csv --output json
python scripts/customer_interview_analyzer.py interview.txt json
```

---

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| **Solution-First** — jumping to features before understanding problems | Start every PRD with problem statement |
| **Analysis Paralysis** — over-researching without shipping | Set time-boxes for research phases |
| **Feature Factory** — shipping without measuring impact | Define success metrics before building |
| **Ignoring Tech Debt** — not allocating for platform health | Reserve 20% capacity for maintenance |
| **Stakeholder Surprise** — not communicating early enough | Weekly async updates, monthly demos |
| **Metric Theater** — optimizing vanity metrics | Tie metrics to user value delivered |

---

## Reference Documents

- `references/prd_templates.md` — PRD templates for different contexts
- `references/frameworks.md` — Detailed framework documentation (RICE, MoSCoW, Kano, JTBD)
- `references/tools-reference.md` — Full tool documentation: CSV formats, command options, example I/O

## Integration Points

JSON export enables integration with most tools (Jira, Linear, ProductBoard, Amplitude, etc.):
```bash
python scripts/rice_prioritizer.py features.csv --output json > priorities.json
python scripts/customer_interview_analyzer.py interview.txt json > insights.json
```
