# Operator Kit Fluency Resources

The unusual thing about this mission: the highest-trust source is **your own repo**, not
the open web. No external author knows what is in your kit. External sources are only
useful for the general model of how skills and invocation work.

## Knowledge

- [`CLAUDE.md`](../../CLAUDE.md) — routing table + pack index.
  The only index Claude has for the 104 user-invoked skills. Use for: which skill handles
  which task; the 37/104 invocation split.
- [`LIFECYCLE.md`](../../LIFECYCLE.md) — invocation policy and buckets.
  The [A]/[B]/[C] rule for what earns model-invocation, the `_incubator/` and
  `_deprecated/` rules, and the routing-table sync procedure. Use for: why a skill is
  user-invoked; how to retire one properly.
- Each pack's `NAVIGATOR.md` — e.g. [`pm-frameworks/NAVIGATOR.md`](../../pm-frameworks/NAVIGATOR.md).
  The middle routing layer: decision trees within a pack. Use for: choosing among
  near-neighbours once you know the pack.
- Skill frontmatter — the `description:` block of any `SKILL.md`.
  **The authoritative tiebreaker.** 58 skills carry an explicit `DO NOT use for… — use X
  instead` clause. Use for: settling any two skills that sound alike.
- [`meta-tools/writing-great-skills`](../../meta-tools/writing-great-skills/SKILL.md) + its `GLOSSARY.md`.
  Why the kit is shaped as it is — context load, cognitive load, leading words, the seven
  failure modes. Use for: judging whether a skill earns its place.
- [Claude Code skills documentation](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill)
  The official mechanics of `disable-model-invocation` and who can fire a skill. Cited by
  `LIFECYCLE.md` itself. Use for: the platform-level model, not your kit specifically.

## Wisdom (Communities)

Not yet established — see Gaps. You have a WhatsApp group where tools and prompts get
shared; that is the nearest thing to a practitioner community for this and may be where
kit-shaped questions get real answers.

## Gaps

- ~~**No usage telemetry.**~~ **Closed 2026-09-12.** Claude Code writes a JSONL
  transcript per session under `~/.claude/projects/<encoded-working-dir>/`, one directory
  per working directory — so it covers every repo, which is where the kit is actually
  used. Every skill invocation is a `Skill` tool_use record naming the skill.
  [`scripts/skill-usage.py`](../../scripts/skill-usage.py) reads them and cross-references
  the kit. **Run it on your own machine** — transcripts are local, so a remote session
  sees only itself. Read its docstring first: a zero means "no record in this window",
  which is a prune candidate, not proof of non-use.
- **No worked examples.** Your own `BACKLOG.md` flags this: several `pm-frameworks`
  skills reference templates without ever showing what good output looks like. Until
  that lands, lessons cannot show you the target artifact.
- **Community for agent-skill design** not identified. Worth finding one before treating
  any of my structural advice as settled.
