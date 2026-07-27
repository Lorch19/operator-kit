# Operator Kit — Backlog

## Urgent

- [ ] **Learning session on Operator Kit** — Walk through the full kit end-to-end: what each pack does, when to use which skill, how routing works (CLAUDE.md → NAVIGATOR.md → SKILL.md), and hands-on practice with the top 5 daily drivers. Goal is fluency, not just awareness.

## High

- [x] **Build `project-bootstrap` skill** — Done; shipped at `meta-tools/project-bootstrap` (185 lines).
- [x] **Build `context-sync-setup` skill** — Done; shipped at `meta-tools/context-sync-setup` (139 lines).
- [ ] **Evaluate GitHub MCP integration** — Check claude.ai integrations page for GitHub MCP. Would unlock PR management, issue tracking from Claude directly. All 7 repos on GitHub (Lorch19).

## Priority

- [x] **Split skill-creator into SKILL.md + references** — Done. 486→246 lines. Extracted eval-workflow, description-optimization, and environment-guides into `references/`.
- [ ] **Add worked examples to pm-frameworks skills** — Several pm-frameworks skills (strategy-craft, prioritization-advisor, pestel-analysis, opportunity-solution-tree) reference templates without showing concrete output. Add a short "Example Output" section to the 5-10 most-used skills showing what good output looks like.
- [x] **Extract shared CLAUDE.md boilerplate** — Done. Created `meta-tools/operational-discipline/SKILL.md` (88 lines). Projects can replace duplicated sections with a one-line pointer.
- [x] **Build `deploy-rsync` skill** — Done; shipped at `meta-tools/deploy-rsync` (188 lines).
- [x] **Build `health-check-monitor` skill** — Done; shipped at `meta-tools/health-check-monitor` (154 lines).
- [ ] **Evaluate Supabase MCP integration** — Direct DB queries and schema inspection for first-bloom-build + lorchprotfoliotracker.
- [x] **Extract shared CLAUDE.md boilerplate** — Done. Created `meta-tools/operational-discipline/SKILL.md`. Projects still need pointer replacement (separate task).

## Strategic

- [x] **Add NAVIGATOR.md to analytics-tools and gtm-tools** — Done. Both created with skill tables + cross-pack references.
- [x] **Reduce doc-coauthoring to under 250 lines** — Done. 326→231 lines. Consolidated Stage 2 loop, condensed Tips and What NOT to Do.
- [ ] **Evaluate Telegram MCP integration** — Custom bot code per-project could be replaced with unified MCP. Would simplify notification layer across portfolio-system and scheduled tasks.
- [x] **Migrate existing packs to .claude-plugin format** — Done. All 15 packs have `plugin.json`; repo root is a marketplace (`.claude-plugin/marketplace.json`). Regenerate with `scripts/gen-plugin-manifests.py`; validate with `claude plugin validate . --strict`.
- [ ] **Add CONNECTORS.md to existing packs** — New packs use the `~~category` connector pattern for tool-agnostic integration. Add CONNECTORS.md to domain-tools, analytics-tools, and gtm-tools.
- [ ] **Port financial-services-plugins deep models** — Anthropic's financial-services-plugins repo has 3-statement-model, DCF, LBO, comps-analysis, PE due diligence skills. Significantly deeper than current financial-analyst. Port as extension to domain-tools or new finance-tools pack.
- [ ] **Evaluate claude-md-management plugin** — Anthropic's official plugin that audits/improves CLAUDE.md files and captures session learnings. Could enhance context-management skill.
- [ ] **Add hooks support to operator-kit** — Security-guidance hook is added to meta-tools. Consider adding SessionStart hooks for auto-loading context and PreToolUse hooks for quality gates. Follow Anthropic's hookify pattern for creating hooks from conversation patterns.

## Non-priority

- [x] **Add `type`/`best_for` to remaining pm-agents skills** — Done. All 12 skills now have `type: component` and 4 `best_for` entries each.
- [x] **Verify pdf skill references exist** — Verified. `reference.md` (611 lines) and `forms.md` (294 lines) both exist and are populated.
- [ ] **Build `fastapi-scaffold` skill** — Template for FastAPI+Uvicorn+Pydantic+Docker+health-check backend. Only justified when a 3rd project needs this pattern (currently 2: WatchTogether, IL-ecommerce).

## From the mattpocock/skills review

- [ ] **Prune pm-frameworks descriptions** — 43 skills average 447 chars of description each. Now that most are user-invoked the context cost is gone, but the `DO NOT use` disambiguation clauses were doing a router's job. Collapse them into the `CLAUDE.md` routing table and shorten each description to one human-facing line. See `meta-tools/writing-great-skills` → "Writing the description".
- [ ] **Hunt for sediment across the kit** — 150K words over 140 skills (~1,070 each) vs. mattpocock/skills' ~640. Run the pruning discipline from `writing-great-skills` (relevance check, then the no-op test sentence by sentence) over the 20 longest skills.
- [ ] **Decide on `code-review` name collision** — `engineering-tools/skills/code-review` shadows Claude Code's bundled `/code-review`. Keep and rename, or drop ours. Noted in `LIFECYCLE.md`.
- [ ] **Consider adopting `to-spec`/`to-tickets` for PM work** — they publish to an issue tracker and assume a codebase. A PM-flavoured variant (spec → epics → stories on Linear/Jira) would connect `prd-partner` to execution.
- [x] **Wire `grilling` into existing PM skills** — Done. `prd-partner` Discovery Mode and `/pm:strategy` Steps 1-5 now run as grilling sessions; description rewritten for standalone natural-language triggering. Still unwired: `pm-frameworks/product-strategy-session`, `discovery-process`, `positioning-workshop`, and the other `*-workshop` skills — same one-line change if the pattern holds up in use.
