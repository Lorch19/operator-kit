# Operator Kit

Tools for building, shipping, and running products. PM frameworks, multi-agent workflows, executable scripts, document generation, analytics, and an always-on strategic advisor. Each pack includes a `NAVIGATOR.md` — start there to find the right skill.

---

## Quick Start — Top 15 Daily Drivers

| Task | Skill | Pack |
|------|-------|------|
| Write a PRD | `prd-partner` (personalized) or `pm-frameworks/prd-development` (generic) | Root / PM Frameworks |
| **Stress-test any plan or decision** | `thinking-tools/grill-me` | Thinking Tools |
| **Hand off a full context window** | `thinking-tools/handoff` | Thinking Tools |
| Competitive analysis | `domain-tools/competitive-teardown` | Domain Tools |
| Strategy session | `/pm:strategy` | PM Agents |
| Market sizing | `pm-frameworks/tam-sam-som-calculator` | PM Frameworks |
| Create a slide deck | `document-tools/pptx` | Document Tools |
| Build a spreadsheet model | `document-tools/xlsx` | Document Tools |
| A/B test analysis | `analytics-tools/ab-test-analysis` | Analytics Tools |
| Go-to-market entry | `gtm-tools/beachhead-segment` | GTM Tools |
| Growth flywheel design | `gtm-tools/growth-loops` | GTM Tools |
| Financial modeling | `domain-tools/financial-analyst` | Domain Tools |
| Discovery workflow | `pm-frameworks/discovery-process` | PM Frameworks |
| Multi-agent spec review | `/pm:review` | PM Agents |
| Create/optimize skills | `meta-tools/skill-creator` | Meta Tools |
| Plan an automation | `meta-tools/automation-planner` | Meta Tools |
| **Linx: any product work** | `~/linx-advisor/` (standalone) | Linx Advisor |
| Incident response | `engineering-tools/incident-response` | Engineering Tools |
| Code review | `engineering-tools/code-review` | Engineering Tools |
| Sales call prep | `sales-tools/call-prep` | Sales Tools |
| Pipeline review | `sales-tools/pipeline-review` | Sales Tools |
| Design critique | `design-tools/design-critique` | Design Tools |
| Status report | `operations-tools/status-report` | Operations Tools |
| Process documentation | `operations-tools/process-doc` | Operations Tools |
| Build frontend UI | `meta-tools/frontend-design` | Meta Tools |

---

## Installed Packs

### 1. PM Frameworks (`pm-frameworks/`)
44 battle-tested product management frameworks. See `pm-frameworks/NAVIGATOR.md` for the full decision tree.

**Key skills:**
- `prd-development` — Write PRDs using best-practice templates
- `jobs-to-be-done` — JTBD discovery and analysis
- `opportunity-solution-tree` — Teresa Torres' OST framework
- `product-strategy-session` — Full strategy facilitation
- `discovery-process` — End-to-end discovery workflow
- `prioritization-advisor` — Framework-based prioritization
- `pestel-analysis` — Market environment analysis
- `positioning-workshop` — Geoffrey Moore positioning
- `roadmap-planning` — Roadmap creation and alignment
- `tam-sam-som-calculator` — Market sizing
- `company-research` — Deep company intelligence
- `saas-revenue-growth-metrics` — SaaS metrics analysis
- `press-release` — Amazon Working Backwards
- `career-growth-advisor` — PM→Director→VP/CPO career transitions

### 2. PM Agents (`pm-agents/`)
Multi-agent PM system that compounds with each use. See `pm-agents/NAVIGATOR.md` for command reference.

**Key commands:**
- `/pm:spec` — Write specs with parallel agent review
- `/pm:review` — 6 agents review your work simultaneously
- `/pm:strategy` — Strategy development with bias checking
- `/pm:simulate` — Stress-test your strategy
- `/pm:opportunity` — Opportunity discovery workflow
- `/pm:riff` — Brainstorm and ideate freely
- `/pm:lfg` — Full pipeline (discovery → spec → review)

**Key skills:**
- `strategy-craft` — Strategic thinking frameworks
- `metrics-design` — Metrics and success criteria
- `opportunity-evaluation` — Evaluate opportunities rigorously
- `vision-narrative` — Craft compelling product vision
- `stakeholder-buyin` — Stakeholder alignment tactics

### 3. Domain Tools (`domain-tools/`)
6 specialist skills with 11 Python scripts for founder/consultant workflows. See `domain-tools/NAVIGATOR.md` for script reference.

**Key skills:**
- `competitive-teardown` — Deep competitive analysis with scoring
- `financial-analyst` — Financial modeling (DCF, ratios, variance, forecasting) + 4 Python scripts
- `revenue-operations` — RevOps and pipeline optimization + 3 Python scripts
- `marketing-strategy-pmm` — GTM, launch plans, battlecards, sales enablement
- `marketing-demand-acquisition` — Paid media, SEO, partnerships, attribution
- `product-manager-toolkit` — RICE prioritization + customer interview analysis scripts

### 4. Document Tools (`document-tools/`) — NEW
4 Anthropic official skills for creating real document files. Each includes scripts and production-grade templates.

**Skills:**
- `docx` — Create/read/edit Word documents (.docx) with formatting, tables, images
- `pptx` — Create/edit PowerPoint presentations with design guidance
- `xlsx` — Create/edit Excel spreadsheets with formulas, charts, financial formatting
- `pdf` — PDF manipulation: merge, split, forms, OCR, encryption

### 5. Analytics Tools (`analytics-tools/`) — NEW
Quantitative analysis skills for data-driven PM work. From Pawel Huryn's PM Skills collection.

**Skills:**
- `ab-test-analysis` — Statistical A/B test analysis (confidence intervals, chi-squared, MDE)
- `sql-queries` — Natural language → SQL query generation
- `cohort-analysis` — Retention and cohort pattern analysis

### 6. GTM Tools (`gtm-tools/`) — NEW
Go-to-market execution skills. From Pawel Huryn's PM Skills collection.

**Skills:**
- `beachhead-segment` — Market entry scoring (burning pain × willingness × winnable × referral)
- `competitive-battlecard` — Sales enablement battlecards (different from competitive-teardown analysis)
- `growth-loops` — Self-reinforcing flywheel and growth loop design

### 7. Meta Tools (`meta-tools/`)
Skills for building and optimizing your toolkit itself.

**Skills:**
- `skill-creator` — Create, test, evaluate, and benchmark Claude skills (Anthropic official)
- `web-artifacts-builder` — Build interactive React+shadcn HTML artifacts
- `adr-writer` — Write Architecture Decision Records with structured rationale
- `automation-planner` — Plan background automations with safety guards (timeouts, circuit breakers, monitoring)
- `frontend-design` — Distinctive, production-grade frontend interfaces (anti-AI-slop aesthetics)
- `internal-comms` — Status reports, 3P updates, newsletters, FAQs
- `webapp-testing` — Playwright-based web app testing with screenshots
- `security-guidance` — PreToolUse hook monitoring 9 security patterns (XSS, injection, eval)
- `writing-great-skills` — The *editorial* half of skill authoring: invocation choice, information hierarchy, progressive disclosure, leading words, and the six failure modes (premature completion, duplication, sediment, sprawl, no-op, negation). Pair with `skill-creator`, which handles scaffolding and evals.

### 8. Operations Tools (`operations-tools/`)
9 operational excellence skills from Anthropic's knowledge-work-plugins. `.claude-plugin` format. See `operations-tools/NAVIGATOR.md`.

**Skills:**
- `capacity-plan` — Workload analysis and utilization forecasting
- `change-request` — Change management with impact analysis and rollback
- `compliance-tracking` — SOC 2, ISO 27001, GDPR audit readiness
- `process-doc` — SOPs, RACI matrices, flowcharts
- `process-optimization` — Streamline inefficient workflows
- `risk-assessment` — Identify, assess, and mitigate operational risks
- `runbook` — Step-by-step operational procedures
- `status-report` — Leadership updates with KPIs and risks
- `vendor-review` — Vendor evaluation, TCO analysis, negotiation

### 9. Engineering Tools (`engineering-tools/`)
21 engineering skills in two families. `.claude-plugin` format. See `engineering-tools/NAVIGATOR.md`.

**Advisory skills** (Anthropic knowledge-work-plugins) — produce an artifact:
- `architecture` — ADRs and system design evaluation
- `code-review` — Security, performance, correctness review
- `debug` — Structured debugging (reproduce, isolate, diagnose, fix)
- `deploy-checklist` — Pre/during/post deployment verification
- `documentation` — READMEs, API docs, onboarding guides
- `incident-response` — Triage, communicate, mitigate, postmortem
- `standup` — Daily standup generation from activity
- `system-design` — Requirements, architecture, scalability
- `tech-debt` — Categorize and prioritize technical debt
- `testing-strategy` — Test plans with pyramid approach

**Flow skills** (from mattpocock/skills, MIT — see `CREDITS.md`) — drive the work through your issue tracker. Run `/agent-context-setup` once per repo first.
- `agent-context-setup` — One-time repo config: issue tracker, triage labels, `CONTEXT.md`/ADR layout
- `to-spec` — Conversation → spec/PRD, published to the tracker
- `to-tickets` — Spec → tracer-bullet vertical slices with explicit blocking edges
- `implement` — Build one ticket per fresh context, TDD-driven, review before commit
- `tdd` — Red → green loop: seams, what a good test is, the four anti-patterns
- `prototype` — Throwaway code answering one design question (logic branch or UI branch)
- `diagnosing-bugs` — Hard bugs: build a tight, red-capable feedback loop *before* hypothesising
- `codebase-design` — Deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality)
- `domain-modeling` — Ubiquitous language, `CONTEXT.md` glossary, ADRs written as decisions land
- `improve-codebase-architecture` — Scan for deepening opportunities, HTML report, grill the pick
- `triage` — Move incoming issues and external PRs through a triage state machine

### 10. Sales Tools (`sales-tools/`)
9 sales workflow skills from Anthropic's knowledge-work-plugins. `.claude-plugin` format. See `sales-tools/NAVIGATOR.md`.

**Skills:**
- `account-research` — Company/person research with actionable intel
- `call-prep` — Account context, attendee research, suggested agenda
- `call-summary` — Notes/transcript → action items + follow-up email
- `competitive-intelligence` — Interactive competitor battlecards
- `create-an-asset` — Landing pages, decks, one-pagers for prospects
- `daily-briefing` — Morning sales briefing with priorities
- `draft-outreach` — Research-first personalized outreach
- `forecast` — Weighted forecast with scenarios and gap analysis
- `pipeline-review` — Pipeline health, deal prioritization, risk flags

### 11. Design Tools (`design-tools/`)
7 product design skills from Anthropic's knowledge-work-plugins. `.claude-plugin` format. See `design-tools/NAVIGATOR.md`.

**Skills:**
- `accessibility-review` — WCAG 2.1 AA accessibility audit
- `design-critique` — Structured feedback on usability, hierarchy, consistency
- `design-handoff` — Developer specs: tokens, states, responsive, edge cases
- `design-system` — Audit, document, or extend design systems
- `research-synthesis` — Distill interviews/surveys into themes and actions
- `user-research` — Plan studies, interview guides, survey design
- `ux-copy` — Microcopy, error messages, empty states, CTAs

### 12. Doc Coauthoring (`doc-coauthoring/`)
Structured co-authoring workflow with three phases: context gathering, section-by-section refinement, and fresh-eyes reader testing. Anthropic official skill.

### 13. PRD Partner (`prd-partner/`)
Personalized PRD creation skill. Discovery Mode (sharpen thinking) or PRD Mode (generate document). Three output modes: AI-Build, Dev-Team, Stakeholder.

### 14. Context Management (`context-management/`)
Context management system for AI coding agents (Claude Code, Cursor, etc.). Maintains project context across sessions with two lean files + on-demand docs.

**Key files:**
- `SKILL.md` — Full skill instructions and session workflow
- `assets/CLAUDE.template.md` — Template for agent instructions file
- `assets/STATE.template.md` — Template for project state file
- `assets/CONTEXT-PROTOCOL.md` — Context update protocol
- `references/GUIDE.md` — Human-readable quick guide

### 15. Thinking Tools (`thinking-tools/`)
6 domain-agnostic reasoning primitives, from mattpocock/skills (MIT — see `CREDITS.md`). Not frameworks with templates — small composable moves you apply to any subject. See `thinking-tools/NAVIGATOR.md`.

**Skills:**
- `grilling` — Relentless one-question-at-a-time interview. **A primitive** — model-invoked, so any other skill can call it mid-session. Looks up facts itself; puts only *decisions* to you.
- `grill-me` — User-facing wrapper: run a grilling session on anything.
- `wayfinder` — Plan an effort too big for one session as a shared map of **decision tickets** on your issue tracker. Fog of war, frontier, out-of-scope; produces decisions, not deliverables, then hands off to `to-spec`.
- `handoff` — Compact the current conversation into a handoff doc so a fresh session can pick up. Forks the context; `/compact` continues it.
- `research` — Delegate reading legwork to a background agent, cited to primary sources only.
- `teach` — Learn a topic across sessions in a stateful workspace (mission, lessons, learning records, reference docs).

### 16. Linx Advisor (standalone at `~/linx-advisor/`)

Linx Advisor has been moved to its own standalone directory at `/Users/omrilorch/linx-advisor/`. It is no longer part of the operator-kit repo. See the linx-advisor directory directly for its SKILL.md, knowledge files, and rhythm files. 8 scheduled tasks maintain its daily/weekly cadence.

---

## Full Routing Table

| Task | Use this skill |
|------|---------------|
| **Thinking Primitives** | |
| Stress-test a plan, decision, or idea | `thinking-tools/grill-me` |
| Interrogate the user mid-session (callable primitive) | `thinking-tools/grilling` |
| Plan an effort too big for one session | `thinking-tools/wayfinder` |
| Hand a full context window to a fresh session | `thinking-tools/handoff` |
| Delegate research to a background agent | `thinking-tools/research` |
| Learn a topic across multiple sessions | `thinking-tools/teach` |
| **Documents & Files** | |
| Write a Word doc | `document-tools/docx` |
| Create a slide deck | `document-tools/pptx` |
| Build a spreadsheet | `document-tools/xlsx` |
| Manipulate PDFs | `document-tools/pdf` |
| Co-author a document | `doc-coauthoring` |
| **Product Management** | |
| Write a PRD | `prd-partner` or `pm-frameworks/prd-development` |
| Discovery workflow | `pm-frameworks/discovery-process` |
| JTBD analysis | `pm-frameworks/jobs-to-be-done` |
| Opportunity mapping | `pm-frameworks/opportunity-solution-tree` |
| Prioritization | `pm-frameworks/prioritization-advisor` |
| Roadmap | `pm-frameworks/roadmap-planning` |
| User stories | `pm-frameworks/user-story` |
| **Strategy & Research** | |
| Strategy session | `pm-agents` → `/pm:strategy` |
| Competitive analysis | `domain-tools/competitive-teardown` |
| Market sizing | `pm-frameworks/tam-sam-som-calculator` |
| Positioning | `pm-frameworks/positioning-workshop` |
| PESTEL analysis | `pm-frameworks/pestel-analysis` |
| Company research | `pm-frameworks/company-research` |
| Press release (Working Backwards) | `pm-frameworks/press-release` |
| **Analytics & Data** | |
| A/B test analysis | `analytics-tools/ab-test-analysis` |
| SQL query generation | `analytics-tools/sql-queries` |
| Cohort/retention analysis | `analytics-tools/cohort-analysis` |
| SaaS metrics | `pm-frameworks/saas-revenue-growth-metrics` |
| **Go-to-Market** | |
| Market entry (beachhead) | `gtm-tools/beachhead-segment` |
| Sales battlecard | `gtm-tools/competitive-battlecard` |
| Growth loops | `gtm-tools/growth-loops` |
| GTM strategy | `domain-tools/marketing-strategy-pmm` |
| Demand gen | `domain-tools/marketing-demand-acquisition` |
| **Financial** | |
| Financial modeling | `domain-tools/financial-analyst` |
| Revenue operations | `domain-tools/revenue-operations` |
| RICE prioritization | `domain-tools/product-manager-toolkit` |
| **Multi-Agent Workflows** | |
| Write + review spec | `/pm:spec` then `/pm:review` |
| Full pipeline | `/pm:lfg` |
| Brainstorm | `/pm:riff` |
| Simulate/stress-test | `/pm:simulate` |
| **Operations** | |
| Process documentation / SOP | `operations-tools/process-doc` |
| Operational runbook | `operations-tools/runbook` |
| Status report for leadership | `operations-tools/status-report` |
| Risk assessment | `operations-tools/risk-assessment` |
| Vendor evaluation | `operations-tools/vendor-review` |
| Change management request | `operations-tools/change-request` |
| Capacity planning | `operations-tools/capacity-plan` |
| Compliance/audit tracking | `operations-tools/compliance-tracking` |
| Process optimization | `operations-tools/process-optimization` |
| **Engineering** | |
| Architecture decision (ADR) | `engineering-tools/architecture` |
| Code review | `engineering-tools/code-review` |
| Debugging session | `engineering-tools/debug` |
| Deploy checklist | `engineering-tools/deploy-checklist` |
| Technical documentation | `engineering-tools/documentation` |
| Incident response | `engineering-tools/incident-response` |
| Standup update | `engineering-tools/standup` |
| System design | `engineering-tools/system-design` |
| Tech debt audit | `engineering-tools/tech-debt` |
| Test strategy | `engineering-tools/testing-strategy` |
| Configure a repo for the flow skills (run once) | `engineering-tools/agent-context-setup` |
| Conversation → spec on the tracker | `engineering-tools/to-spec` |
| Spec → tracer-bullet tickets | `engineering-tools/to-tickets` |
| Build one ticket end to end | `engineering-tools/implement` |
| Write a behaviour test-first | `engineering-tools/tdd` |
| Throwaway prototype to settle a design question | `engineering-tools/prototype` |
| Hard bug, flake, or perf regression | `engineering-tools/diagnosing-bugs` |
| Shape a module's interface (deep modules) | `engineering-tools/codebase-design` |
| Ubiquitous language + ADRs | `engineering-tools/domain-modeling` |
| Find refactors that deepen the codebase | `engineering-tools/improve-codebase-architecture` |
| Triage incoming issues and external PRs | `engineering-tools/triage` |
| **Sales** | |
| Account/prospect research | `sales-tools/account-research` |
| Sales call prep | `sales-tools/call-prep` |
| Call summary + follow-up | `sales-tools/call-summary` |
| Competitive intelligence | `sales-tools/competitive-intelligence` |
| Sales asset creation | `sales-tools/create-an-asset` |
| Daily sales briefing | `sales-tools/daily-briefing` |
| Draft outreach email | `sales-tools/draft-outreach` |
| Sales forecast | `sales-tools/forecast` |
| Pipeline review | `sales-tools/pipeline-review` |
| **Design** | |
| Accessibility audit | `design-tools/accessibility-review` |
| Design critique/feedback | `design-tools/design-critique` |
| Developer handoff specs | `design-tools/design-handoff` |
| Design system management | `design-tools/design-system` |
| Research synthesis | `design-tools/research-synthesis` |
| User research planning | `design-tools/user-research` |
| UX copy writing | `design-tools/ux-copy` |
| **Meta / Tooling** | |
| Create/optimize a skill | `meta-tools/skill-creator` |
| Edit a skill for predictability (vocabulary + failure modes) | `meta-tools/writing-great-skills` |
| Build interactive artifact | `meta-tools/web-artifacts-builder` |
| Document a decision | `meta-tools/adr-writer` |
| Plan an automation | `meta-tools/automation-planner` |
| Build frontend UI | `meta-tools/frontend-design` |
| Write internal comms | `meta-tools/internal-comms` |
| Test a web app | `meta-tools/webapp-testing` |
| Security guidance hook | `meta-tools/security-guidance` |
| Context management | `context-management` |
| Career transition | `pm-frameworks/career-growth-advisor` |
| **Linx-Specific** | |
| Any Linx product work | `~/linx-advisor/` (standalone, not in operator-kit) |
