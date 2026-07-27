# Operator Kit — Skill Lifecycle

Two policies keep a 141-skill kit usable: **invocation** (who can fire a skill) and
**buckets** (whether a skill is shipped at all). Both are enforced by
`scripts/validate-kit.py`, which runs clean on every commit.

Adapted from [mattpocock/skills](https://github.com/mattpocock/skills). See `CREDITS.md`.

---

## 1. Invocation policy

Every skill description is loaded into context **on every turn**. 140 descriptions cost
~11.5K tokens and, worse, make routing less accurate — the more near-identical
descriptions compete, the more often the wrong one fires.

Claude Code gives three states ([docs](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill)):

| Frontmatter | You invoke | Claude invokes | Description in context |
|---|---|---|---|
| *(default)* | yes | yes | **always** |
| `disable-model-invocation: true` | yes | no | never |
| `user-invocable: false` | no | yes | always |

### The rule

A skill stays **model-invoked** only if at least one of these holds:

- **[A] Deliverable trigger** — the user names an *output*, never the skill. "Make me a
  deck" must reach `pptx`; nobody types `/pptx`.
- **[B] Called by another skill** — it's a primitive in someone else's flow. `implement`
  drives `tdd`; `wayfinder` fires `research` subagents. A user-invoked skill is
  unreachable by other skills, so this is decisive.
- **[C] Agent notices first** — the user doesn't know they need it.
  `security-guidance` fires on a code pattern; `prd-partner` fires on PRD-shaped input
  even when "PRD" is never said.

**Everything else is user-invoked.** A framework you *choose* — PESTEL, a beachhead
scoring, a pipeline review — is a deliberate act. Making it model-invoked buys nothing
and costs context every turn.

Current split: **37 model-invoked / 104 user-invoked**, ~3.1K tokens of description in
context, down from ~11.5K.

### The cost, stated plainly

A user-invoked skill trades **context load** for **cognitive load**: you now have to
remember it exists. That debt is paid by the routing table in `CLAUDE.md`, which is
always in context and **must list every active skill**. The validator enforces this — if
routing is stale, the skill is effectively lost.

Claude can still *recommend* a user-invoked skill (it reads the routing table); it just
can't fire one unasked.

### Changing a skill's invocation

Adding `[B]` reachability is the usual reason to promote a skill back to model-invoked —
if a new skill needs to call it, it must be model-invoked or the call silently fails.

---

## 2. Buckets

A pack directory (`pm-frameworks/`, `sales-tools/`, …) is the **promoted** set: shipped,
supported, and listed in `CLAUDE.md`. Two underscore-prefixed buckets sit outside it.

| Bucket | Meaning | In routing table | Invocation |
|---|---|---|---|
| `<pack>/` | Promoted — shipped and supported | **required** | per the rule above |
| `_incubator/` | Draft, not ready to ship | **forbidden** | user-invoked |
| `_deprecated/` | Retired; kept for reference | **forbidden** | user-invoked |

Underscore-prefixed so they sort away from packs and never read as one.

### Rules

1. A skill in a pack **must** appear in the `CLAUDE.md` routing table. A skill in a
   bucket **must not**.
2. Every skill in `_incubator/` and `_deprecated/` carries
   `disable-model-invocation: true`, so a retired skill can never fire on its own.
3. Every `_deprecated/` skill opens with a banner naming **what supersedes it** and
   **why** it was retired. A retirement without a replacement named is just deletion —
   use `git rm` for that.
4. Skill `name:` values are unique across the whole repo, buckets included.

### Moving a skill

```bash
git mv pm-frameworks/foo _deprecated/foo    # then: add banner, set the flag,
                                            # remove its routing-table row
python3 scripts/validate-kit.py             # must pass before commit
```

Promoting out of `_incubator/` is the reverse: `git mv` into a pack, decide its
invocation by the rule, add the routing row.

### Currently retired

| Skill | Superseded by | Why |
|---|---|---|
| `debug` | `engineering-tools/skills/diagnosing-bugs` | Matt Pocock's version refuses to hypothesise until it has one command that already goes red on the bug. The name also collided with Claude Code's **bundled** `/debug`. |
| `skill-authoring-workflow` | `meta-tools/skill-creator` + `meta-tools/writing-great-skills` | Referenced a repo-root `scripts/` directory that never existed, so its workflow could not run. |

### Known name collisions with bundled Claude Code skills

`engineering-tools/skills/code-review` shadows the bundled `/code-review`. Left in place
deliberately — the kit's version is richer — but rename it if the bundled one is
preferred.

---

## 3. Packaging

Every pack ships as a Claude Code plugin; the repo root is the marketplace
(`.claude-plugin/marketplace.json`, 15 plugins). Three pack layouts, three treatments:

| Layout | Example | `plugin.json` |
|---|---|---|
| `<pack>/skills/<skill>/` | `engineering-tools` | nothing — default scan finds them |
| `<pack>/<skill>/` (flat) | `pm-frameworks` | explicit `skills` array, one path per skill |
| `<pack>/SKILL.md` | `prd-partner` | nothing — auto single-skill plugin |

Flat packs list every skill path explicitly rather than relying on `"skills": ["./"]`,
which is ambiguous between "a directory of skills" and "a single skill at the root".

After adding, renaming, or moving a skill in a **flat** pack, regenerate that pack's
`skills` array and run:

```bash
claude plugin validate . --strict          # the marketplace
claude plugin validate <pack> --strict     # the pack
python3 scripts/validate-kit.py            # lifecycle rules
```

A `CLAUDE.md` at a plugin root is **never loaded as context** when the plugin is
installed. `pm-agents/CLAUDE.md` was renamed to `README.md` for exactly this reason —
keeping it would have looked like it was doing something it wasn't. Ship standing
instructions as a skill, not as a stray `CLAUDE.md`.
