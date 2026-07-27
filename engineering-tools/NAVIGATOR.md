# Engineering Tools — Navigator

Two families live here.

- **Advisory skills** (Anthropic knowledge-work-plugins) — produce a document: an ADR, a
  test plan, a postmortem, a standup. Good when you need the *artifact*.
- **Flow skills** (adapted from [mattpocock/skills](https://github.com/mattpocock/skills),
  MIT — see `/CREDITS.md`) — drive the *work* end to end, reading and writing your issue
  tracker. Good when you need the change shipped.

Run `/agent-context-setup` **once per repo** before first use of the flow skills — it
configures the issue tracker, triage labels, and `CONTEXT.md`/ADR layout that
`to-spec`, `to-tickets`, `triage`, and `wayfinder` all assume.

## The main flow: idea → shipped

```
/grill-me (thinking-tools)   sharpen the idea, one question at a time
   └─ needs a runnable answer? → /prototype → throwaway code, keep the decision
/to-spec                     conversation → spec, published to the tracker
/to-tickets                  spec → tracer-bullet vertical slices with blocking edges
/implement                   one ticket per fresh context, driving /tdd internally
/code-review                 review the diff before committing
```

Keep grill → spec → tickets in **one unbroken context window**. Start each `/implement`
fresh from its ticket.

**Too big for one session?** Start at `thinking-tools/wayfinder` instead — it charts a map
of decision tickets and hands off to `/to-spec` once the fog clears.

## Quick Decision Tree

### Build & Ship
- Sharpen a loose idea into a spec → `to-spec`
- Break a spec into agent-grabbable tickets → `to-tickets`
- Build one ticket → `implement`
- Build a behaviour test-first → `tdd`
- Answer a design question with throwaway code → `prototype`
- Architecture decision or system design → `architecture`, `system-design`
- Pre-deployment verification → `deploy-checklist`
- Writing technical docs → `documentation`
- Test strategy for a feature/system → `testing-strategy`

### Review & Improve
- Reviewing code changes → `code-review`
- Find deepening opportunities across the codebase → `improve-codebase-architecture`
- Design a single module's shape → `codebase-design`
- Identifying and prioritizing tech debt → `tech-debt`

### Debug & Respond
- A hard bug, flake, or perf regression → `diagnosing-bugs` *(build the feedback loop first)*
- A quick, obvious bug → `debug`
- Production incident → `incident-response`

### Vocabulary & Upkeep
- Pin down domain terms, write ADRs → `domain-modeling`
- Move incoming issues/PRs through triage states → `triage`
- Daily standup update → `standup`
- One-time repo config for the flow skills → `agent-context-setup`

## All Skills

| Skill | Use When | Source |
|-------|----------|--------|
| `agent-context-setup` | One-time repo config: tracker, triage labels, doc layout | flow |
| `architecture` | ADRs, technology choices, design evaluation | advisory |
| `code-review` | PR review for security, performance, correctness | advisory |
| `codebase-design` | Deep-module vocabulary: module, interface, depth, seam, adapter | flow |
| `debug` | Structured debugging (reproduce, isolate, diagnose, fix) | advisory |
| `deploy-checklist` | Pre/during/post deployment verification | advisory |
| `diagnosing-bugs` | Hard bugs — builds a tight red-capable feedback loop before theorising | flow |
| `documentation` | READMEs, API docs, runbooks, onboarding guides | advisory |
| `domain-modeling` | Ubiquitous language, `CONTEXT.md` glossary, ADRs | flow |
| `implement` | Build one ticket, TDD-driven, review before commit | flow |
| `improve-codebase-architecture` | Scan for deepening opportunities, HTML report | flow |
| `incident-response` | Triage, communicate, mitigate, postmortem | advisory |
| `prototype` | Throwaway code answering one design question (logic or UI) | flow |
| `standup` | Daily standup generation from recent activity | advisory |
| `system-design` | Requirements, high-level design, scalability | advisory |
| `tdd` | Red → green loop, seams, test anti-patterns | flow |
| `tech-debt` | Categorize and prioritize technical debt | advisory |
| `testing-strategy` | Test plans, coverage, testing pyramid | advisory |
| `to-spec` | Conversation → spec/PRD published to the tracker | flow |
| `to-tickets` | Spec → tracer-bullet tickets with blocking edges | flow |
| `triage` | Move issues and external PRs through triage states | flow |

## Overlaps, on purpose

| Pair | Take the flow skill when… |
|---|---|
| `debug` vs `diagnosing-bugs` | The bug resisted a first glance, is intermittent, or is a perf regression |
| `architecture` vs `codebase-design` | You're shaping one module's interface, not choosing a technology |
| `testing-strategy` vs `tdd` | You're writing the tests now, not planning coverage |
