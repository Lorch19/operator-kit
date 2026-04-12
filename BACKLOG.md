# Operator Kit — Backlog

## Urgent

- [ ] **Learning session on Operator Kit** — Walk through the full kit end-to-end: what each pack does, when to use which skill, how routing works (CLAUDE.md → NAVIGATOR.md → SKILL.md), and hands-on practice with the top 5 daily drivers. Goal is fluency, not just awareness.

## High

- [ ] **Build `project-bootstrap` skill** — Scaffold CLAUDE.md + STATE.md + BACKLOG.md + docs/ + launch.json + context-sync for any project. Handles greenfield and retrofit. Mission: `missions/project-bootstrap-skill.md`
- [ ] **Build `context-sync-setup` skill** — Parameterized generator for context-sync scheduled tasks. Mission: `missions/context-sync-setup-skill.md`
- [ ] **Evaluate GitHub MCP integration** — Check claude.ai integrations page for GitHub MCP. Would unlock PR management, issue tracking from Claude directly. All 7 repos on GitHub (Lorch19).

## Priority

- [x] **Split skill-creator into SKILL.md + references** — Done. 486→246 lines. Extracted eval-workflow, description-optimization, and environment-guides into `references/`.
- [ ] **Add worked examples to pm-frameworks skills** — Several pm-frameworks skills (strategy-craft, prioritization-advisor, pestel-analysis, opportunity-solution-tree) reference templates without showing concrete output. Add a short "Example Output" section to the 5-10 most-used skills showing what good output looks like.
- [x] **Extract shared CLAUDE.md boilerplate** — Done. Created `meta-tools/operational-discipline/SKILL.md` (88 lines). Projects can replace duplicated sections with a one-line pointer.
- [ ] **Build `deploy-rsync` skill** — Codify the rsync+SSH deploy pattern from portfolio-system/scripts/deploy.sh into a reusable meta-tool. Mission: `missions/deploy-rsync-skill.md`
- [ ] **Build `health-check-monitor` skill** — Unified cross-project health digest (VPS, Railway, scheduled tasks) → single Telegram message. Mission: `missions/health-check-monitor-skill.md`
- [ ] **Evaluate Supabase MCP integration** — Direct DB queries and schema inspection for first-bloom-build + lorchprotfoliotracker.
- [x] **Extract shared CLAUDE.md boilerplate** — Done. Created `meta-tools/operational-discipline/SKILL.md`. Projects still need pointer replacement (separate task).


### Assess charter pattern for OpenClaw agents
Evaluate whether OpenClaw's agent definitions (AGENTS.md, SOUL.md, per-agent behavior) would benefit from adopting a formal "charter" pattern — explicit, versioned Markdown files per agent that define role, scope, boundaries, decision authority, and learning/memory rules. Inspired by the Squad project (github.com/bradygaster/squad) where each agent has a charter file that persists across runs and evolves. Currently OpenClaw agent behavior is partially implicit in code and cron configs rather than declarative charter docs. Compare: Squad charter format vs. current OpenClaw AGENTS.md structure vs. SKILL.md pattern from operator-kit. Also assess whether charters should include inter-agent delegation rules (who can invoke whom, escalation paths) and permission boundaries — directly relevant to Linx agentic identity governance thinking.
- **Acceptance criteria:** 1. Document current state: how each OpenClaw agent's role/scope/permissions are defined today. 2. Review Squad charter format (bradygaster/squad repo) and extract pattern. 3. Draft charter template for OpenClaw agents with fields: identity, scope, boundaries, tools/permissions, memory rules, delegation authority, escalation triggers. 4. Write sample charter for one agent (e.g. the nightly consolidation agent). 5. Decision doc: adopt/adapt/skip with rationale.
- **Status:** pending

## Strategic

- [x] **Add NAVIGATOR.md to analytics-tools and gtm-tools** — Done. Both created with skill tables + cross-pack references.
- [x] **Reduce doc-coauthoring to under 250 lines** — Done. 326→231 lines. Consolidated Stage 2 loop, condensed Tips and What NOT to Do.
- [ ] **Evaluate Telegram MCP integration** — Custom bot code per-project could be replaced with unified MCP. Would simplify notification layer across portfolio-system and scheduled tasks.
- [ ] **Migrate existing packs to .claude-plugin format** — New packs (operations, engineering, sales, design) use `.claude-plugin/plugin.json`. Older packs (pm-frameworks, domain-tools, analytics-tools, gtm-tools, meta-tools) still use SKILL.md only. Migration enables marketplace publishing and claude.ai compatibility. Start with meta-tools (most active).
- [ ] **Add CONNECTORS.md to existing packs** — New packs use the `~~category` connector pattern for tool-agnostic integration. Add CONNECTORS.md to domain-tools, analytics-tools, and gtm-tools.
- [ ] **Port financial-services-plugins deep models** — Anthropic's financial-services-plugins repo has 3-statement-model, DCF, LBO, comps-analysis, PE due diligence skills. Significantly deeper than current financial-analyst. Port as extension to domain-tools or new finance-tools pack.
- [ ] **Evaluate claude-md-management plugin** — Anthropic's official plugin that audits/improves CLAUDE.md files and captures session learnings. Could enhance context-management skill.
- [ ] **Add hooks support to operator-kit** — Security-guidance hook is added to meta-tools. Consider adding SessionStart hooks for auto-loading context and PreToolUse hooks for quality gates. Follow Anthropic's hookify pattern for creating hooks from conversation patterns.

## Non-priority

- [x] **Add `type`/`best_for` to remaining pm-agents skills** — Done. All 12 skills now have `type: component` and 4 `best_for` entries each.
- [x] **Verify pdf skill references exist** — Verified. `reference.md` (611 lines) and `forms.md` (294 lines) both exist and are populated.
- [ ] **Build `fastapi-scaffold` skill** — Template for FastAPI+Uvicorn+Pydantic+Docker+health-check backend. Only justified when a 3rd project needs this pattern (currently 2: WatchTogether, IL-ecommerce).
