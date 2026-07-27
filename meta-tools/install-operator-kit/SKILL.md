---
name: install-operator-kit
disable-model-invocation: true
description: Install or update Operator Kit on this machine and across Claude interfaces (Claude Code, claude.ai, Cowork). Run on a fresh machine, after a big kit change, or when a skill isn't showing up.
---

# Install Operator Kit

Get Operator Kit's 140 skills onto whichever Claude surface the user is on, then verify
they actually loaded.

**There is no account-level sync.** Claude Code reads skills from disk; claude.ai stores
them per-account. These are separate systems with separate install paths, so a skill
installed in one is invisible to the other. Do not tell the user "it's everywhere now"
unless you have installed and verified each surface they asked for.

## Step 0 — Establish the situation

Ask, one question at a time (this is a `/grilling`-shaped task — recommend an answer with
each question):

1. **Which surfaces?** Claude Code on this machine / claude.ai (web + desktop) / Cowork
   / all of them.
2. **Fresh install or update?** Check whether `~/.claude/skills/` or an existing clone
   already has kit content before assuming.
3. **Where should the repo live?** Default `~/operator-kit`. Only relevant if not cloned.

Then find or clone the repo. Prefer an existing clone over a second one:

```bash
ls ~/operator-kit 2>/dev/null || git clone https://github.com/Lorch19/operator-kit.git ~/operator-kit
cd ~/operator-kit && git pull
python3 scripts/validate-kit.py
```

If the validator fails, **stop and report** — do not install a kit that violates its own
lifecycle rules.

## Step 1 — Claude Code (this machine)

Two routes. **Recommend the marketplace** unless the user wants to edit skills in place.

### Route A — plugin marketplace (recommended)

Subscribes to the repo; `git pull` plus a plugin update refreshes everything. Installs
are clean, versioned, and namespaced.

```
/plugin marketplace add Lorch19/operator-kit
/plugin install pm-frameworks@operator-kit
```

Fifteen plugins are available — install only what they actually use. Ask which, and
recommend the daily drivers:

| Plugin | Skills | Why |
|---|---|---|
| `thinking-tools` | 6 | `grill-me`, `handoff`, `wayfinder` — the primitives |
| `pm-frameworks` | 43 | The framework library |
| `prd-partner` | 1 | Personalized PRD flow |
| `engineering-tools` | 20 | Advisory + the tracker-driven flow skills |
| `meta-tools` | 15 | Skill authoring and toolkit upkeep |
| `document-tools` | 4 | docx / pptx / xlsx / pdf |

Others: `pm-agents`, `analytics-tools`, `gtm-tools`, `domain-tools`, `operations-tools`,
`sales-tools`, `design-tools`, `doc-coauthoring`, `context-management`.

### Route B — symlink into personal skills

Pick this when the user wants to **edit skills and see changes immediately**. Each entry
is a symlink into the repo, so `git pull` updates every installed skill at once.

```bash
mkdir -p ~/.claude/skills
find ~/operator-kit -name SKILL.md -not -path '*/_deprecated/*' -not -path '*/_incubator/*' \
  -exec dirname {} \; | while read -r d; do
    ln -sfn "$d" ~/.claude/skills/"$(basename "$d")"
  done
```

`~/.claude/skills/` covers **every project on this machine** — not other machines, and
not claude.ai. Re-run after adding or renaming a skill.

Do not use both routes for the same pack: two copies of one skill name shadow each other
and make it unclear which is running.

## Step 2 — claude.ai (web + desktop) and Cowork

A different system: skills are uploaded per-skill as **zip files** under
Settings → Capabilities → Skills. They are private to the user's account, and **Cowork
and cloud sessions sync from here**, so this one step covers both.

**Say this plainly before starting:** `disable-model-invocation` is a Claude Code
extension to the Agent Skills standard, not part of the standard. On claude.ai it may be
ignored, which would put all 140 descriptions back in context and undo the kit's context
budget. So do **not** bulk-upload the kit. Upload a short list the user names.

Recommend at most 5–10, favouring skills that work without a repo: `grill-me`,
`handoff`, `prd-partner`, `competitive-teardown`, `beachhead-segment`, `status-report`.
Skip anything that assumes a codebase or an issue tracker — `to-spec`, `to-tickets`,
`implement`, `tdd`, `triage`, `agent-context-setup` — it has nothing to read there.

Build the zips (each must contain the **folder**, not a bare `SKILL.md`):

```bash
cd ~/operator-kit && mkdir -p /tmp/ok-zips
for s in thinking-tools/grill-me thinking-tools/handoff prd-partner; do
  ( cd "$(dirname "$s")" && zip -qr "/tmp/ok-zips/$(basename "$s").zip" "$(basename "$s")" )
done
ls -la /tmp/ok-zips
```

Then hand off — uploading is a UI action you cannot do for them:

> "Zips are in `/tmp/ok-zips`. Go to claude.ai → Settings → Capabilities → Skills →
> `+ Create skill` → upload each. They'll be available on web, desktop, and Cowork."

## Step 3 — Verify, don't assume

Installation is not the deliverable; a working skill is.

- **Claude Code:** run `claude plugin list` (Route A) or
  `ls ~/.claude/skills | head` (Route B). Then actually invoke one — `/grill-me` — and
  confirm it loads.
- **Context budget:** re-run `python3 scripts/validate-kit.py`. It reports the
  description budget; ~3.0K tokens is expected. A much larger number on a surface means
  `disable-model-invocation` is being ignored there.
- **claude.ai:** ask the user to confirm the skills appear in their settings list.

Report per surface: installed and verified / installed but unverified / not attempted.
Never report a surface you did not touch as done.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Skill not in `/` menu | Not installed on *this* surface | Re-run the step for that surface |
| Claude never fires a skill on its own | It's one of the 103 user-invoked ones — by design | Type `/<name>`. See `LIFECYCLE.md` |
| `/code-review` runs the wrong thing | Kit skill shadows Claude Code's bundled one | Known; see `LIFECYCLE.md` |
| Two skills with one name | Both marketplace and symlink routes used | Pick one route, remove the other |
| Plugin won't install | Manifest drift | `claude plugin validate . --strict` in the repo |
| Changes don't show up | Repo stale, or plugin cached | `git pull`, then update the plugin |
