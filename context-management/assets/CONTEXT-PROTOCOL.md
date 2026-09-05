# Context Update Protocol

When the user asks "should we update context?", evaluate using these triggers:

| Trigger | Action |
|---------|--------|
| Current task changed | Update STATE.md → Current Task |
| Feature shipped or broke | Update STATE.md → System Status |
| Architectural decision made | Update docs/ARCHITECTURE.md |
| System-critical lesson learned | Update docs/LESSONS.md |
| Info in STATE.md is outdated | Remove it |
| STATE.md `Last verified` is behind HEAD | Re-verify against the code, then bump the date + SHA |
| New domain became complex enough | Create docs/[DOMAIN].md |
| An agent memory holds a repo-scoped fact | Move it into STATE.md / CLAUDE.md / docs — the repo wins; then delete the memory |
| Review process revealed a gap | Update CLAUDE.md Review Discipline |
| Context file growing bloated | Prune — move reference material to docs/ |

## Rules

- Never update context files without user request.
- Every entry must be a pointer or a decision, not a description.
- Never summarize code that can be read from file paths.
- When suggesting updates, be specific: quote what to add/remove/change.
- STATE.md must stay under 6 KB — check with `wc -c`, not line count. If over, CUT content; never compress by lengthening lines.
- Agent memory is a separate system (a one-fact-per-file directory the agent controls). Never duplicate a fact across a memory and a context file — repo-scoped facts belong in the repo, which versions them; memories rot invisibly.
- **Every word in context files must earn its place.** CLAUDE.md is loaded into every session — bloat dilutes instructions. Behavioral rules belong in CLAUDE.md. Reference material (pointers, ownership maps, connection details) belongs in docs/. If a line can be derived by reading the codebase, delete it. If it hasn't changed behavior in 3+ sessions, question whether it's needed. Periodically challenge: "Would removing this line cause a mistake?"

## What Makes a Good Entry

Bad pointer: `Payment → /src/payments/`
Good pointer: `Payment (Stripe webhooks, LemonSqueezy checkout) → /src/payments/`

Bad entry: `We use Firebase for authentication and it handles user sessions`
Good entry: `Auth: Firebase (chose over Supabase, needed phone auth) → /src/auth/`

## After Evaluation

Present changes as a checklist:
```
Context updates:
- [ ] STATE.md: Update current task to "..."
- [ ] STATE.md: Mark [feature] as ✅ Live
- [ ] docs/ARCHITECTURE.md: Add decision about [X]
- [ ] No other changes needed
```

Wait for user approval before making any changes.
