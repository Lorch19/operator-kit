# Next Steps: Linx Operator Kit

**Last session:** 2026-04-16
**Branch:** `claude/resume-stuck-session-hskc6`
**Status:** Operator-kit improvements done. Linx brief not yet produced.

---

## What Was Completed

1. **AUDIT.md** — Three-bucket assessment of all 124 skills (keep / improve / archive)
2. **compliance-tracking** expanded: 39 → 237 lines (frameworks, control mapping, audit prep)
3. **internal-comms** expanded: 59 → 408 lines (10 templates, audience matrix, anti-patterns)
4. **cohort-analysis** expanded: 119 → 234 lines (B2B dimensions, Python skeleton, pitfalls)

All changes are generic (no Linx-specific content). Pushed to origin.

---

## What Remains

### Priority 1: Produce the Linx Claude Code Brief — DONE (`LINX-CLAUDE-CODE-BRIEF.md`)

A self-contained prompt file (`LINX-CLAUDE-CODE-BRIEF.md`) that Omri pastes into Claude Code running on his Linx account (where Notion MCP connectors are available). The brief must:

- Be fully self-explanatory — Claude Code executes without asking questions
- Include all Linx domain context from `sessions/linx-security-onboarding.md`
- Build 3 skills in order with quality checkpoints between each:
  1. **`linx-security-domain-context`** — Foundation skill. Glossary, product positioning, competitive landscape, buyer personas, market data, compliance frameworks. Sources from Notion + the onboarding session file.
  2. **`prd-partner` overlay** — Linx-adapted PRD creation. Adds security/compliance sections, identity security domain terms, CISO/Security Architect/SOC Analyst/GRC Manager personas.
  3. **`competitive-teardown` overlay** — Linx-adapted competitive analysis. Adds identity security scoring dimensions (threat coverage, protocol support, SIEM integration, NHI support), pre-built competitor stubs for SailPoint, CyberArk, Saviynt, ConductorOne, Lumos, Opal, Zluri, ServiceNow/Veza.
- Include test scenarios for each skill to validate quality
- Include update/maintenance mechanism (staleness indicators, refresh protocol)

### Priority 2: Execute in Linx Claude Code

1. Omri pastes brief into Linx Claude Code (where Notion connectors live)
2. Claude Code builds skills one at a time, Omri validates each
3. Omri copies finished SKILL.md files back to this session (or a new one scoped to `Lorch19/Linx-Operator-Kit`)
4. Skills get committed to `Lorch19/Linx-Operator-Kit` on GitHub

### Priority 3: Future Skills (after the first 3 are validated)

- `security-buyer-personas` — Deep persona library for CISO, Security Architect, SOC Analyst, GRC Manager
- `compliance-feature-mapper` — Maps product features ↔ compliance framework controls
- `pm-weekly-rhythm` — Weekly operating rhythm for PM at Linx
- Linx-adapted overlays for: discovery-process, jobs-to-be-done, beachhead-segment, competitive-battlecard, call-summary, positioning-workshop, tam-sam-som-calculator

### Priority 4: Update Mechanism

Skills referencing Linx domain context go stale as the product, market, and competitors evolve. Planned approach:

- **V1 (now):** Each skill has a `last_updated` field and `staleness_indicators` section listing what to check. Manual monthly refresh.
- **V2 (month 2):** SessionStart hook that checks staleness on session open and auto-refreshes from Notion if >30 days old.
- **V3 (if needed):** Scheduled sync that diffs Notion against skill files and creates PRs for material changes.

---

## Repo Strategy (Agreed)

| Repo | Purpose | Contains |
|------|---------|----------|
| `Lorch19/operator-kit` | Generic PM/builder toolkit | All 124 skills, unchanged. Additive improvements only. |
| `Lorch19/Linx-Operator-Kit` | Linx-specific PM skills | Domain context, buyer personas, compliance mapper, Linx-adapted overlays. Own CLAUDE.md routing. |

Operator-kit is upstream. Linx-Operator-Kit references or imports from it but never pushes Linx-specific content back.
