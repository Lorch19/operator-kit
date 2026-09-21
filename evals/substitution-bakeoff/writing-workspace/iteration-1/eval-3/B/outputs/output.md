# Making the rollback correction stick

Short version: you've been fixing this with the one form of guidance that reliably
fails for this class of problem. The rule is right; the *shape* you're putting it in
is wrong. Below is the diagnosis, a 20-minute step to confirm it before you build
anything, the artifacts to paste in, and a way to check it actually stuck instead of
hoping.

---

## What I'd ask first — and what I'm assuming instead

I can't ask, so here are the five questions that would change my answer, each with the
assumption I'm proceeding on. If one is wrong, the section it affects is flagged.

| Question | Assumption I'm using | What changes if I'm wrong |
|---|---|---|
| What counts as "a rollback step" — a `down`/reverse block in the migration file, a procedure written in the PR, or a migration you've actually run backwards? | A reverse block **inside the migration artifact itself**, plus an explicit note when the change can't be fully reversed. | If it's a PR-body procedure, the template goes in your PR template instead of the migration file. Same mechanics, different file. |
| One repo, or several? | One primary repo. | Several repos → skip to Tier 3 (the skill), which travels; a per-repo instructions file doesn't. |
| Which migration tool? | A file-per-migration tool with an up/down convention (Alembic, Rails, Prisma, Knex, golang-migrate, Flyway…). | If your tool already scaffolds an empty `down`, the fix shrinks to "enforce non-empty" and you can drop the template entirely. |
| When you correct it, does it then write a *good* rollback, or a token one? | A good one — the failure is **omission**, not incompetence. | This is the load-bearing assumption. Step 1 tests it. If it's writing bad rollbacks, the template makes things worse and you need the verification loop instead. |
| Are some of these migrations genuinely irreversible (drop column, destructive backfill)? | Yes, sometimes. | Drives one specific design choice below: an irreversible migration gets a *different required slot*, never an exemption. |

---

## Why six corrections didn't stick

Two separate things are going on, and only one of them is about wording.

**1. There were never six corrections. There were six sessions that each got told once.**

A correction you give in session 4 does not exist in session 5. Nothing carries over
except what's written to a file that gets loaded. So the pattern that feels like
stubbornness — "I've told it six times" — is six independent first-time tellings. The
count is evidence that the behavior is stable and worth fixing permanently; it is not
evidence that repetition is failing to sink in. Repetition was never in play.

That also means: six occurrences is well past the bar for formalizing this. One
occurrence would be a hypothesis. Six is a pattern. Build the permanent thing.

**2. A prose reminder is the wrong form for a missing-element failure.**

Classify what's actually going wrong before choosing how to write the rule, because
the form that fixes one failure type measurably backfires on another:

| What the failure looks like | Form that works | Form that fails |
|---|---|---|
| It knows the rule and skips it under pressure (deadline, "just ship it") | A hard prohibition, plus explicit counters to each excuse it makes | Soft guidance — "prefer", "consider" |
| It complies, but the output is the wrong shape (bloated, buried, restated) | A positive recipe: state what the output **is**, its parts, in order | A list of prohibitions — it will negotiate with "don't X" |
| **It omits a required element from something it already produces** | **Structural: a required slot in the artifact it fills in** | **Prose reminders sitting near that artifact** |
| Behavior should depend on a condition | A conditional on something observable: "if X is present, do Y" | An unconditional rule plus exemption clauses |

You're in row three. The migration file is something Claude already produces
competently; one section is missing from it. The fix is to make the section part of
the thing being filled in, not a sentence that has to be remembered while filling it
in.

This is why volume didn't help and why adding CAPS or a sixth bullet to your
instructions file won't either. A prose reminder competes for attention with
everything else in context. A slot in the file doesn't compete — it's the thing being
worked on. Empty slots are visible; forgotten sentences aren't.

---

## Step 1 — Reproduce it before you fix it (20 minutes)

Don't skip this. You're about to write a rule based on a remembered pattern, and the
remembered pattern is unmeasured. Two specific things can be true that would send you
to a different fix, and both are cheap to check.

**Get the actual rate.** Run this against your migrations directory (adjust the path
and the marker list to your tool):

```bash
# Every tracked migration that has no reverse section at all.
RB='^[[:space:]]*(--|#|//)?[[:space:]]*#*[[:space:]]*rollback|migrate down|def downgrade|function down|IRREVERSIBLE'

for f in $(git ls-files 'db/migrations/*'); do
  grep -qiE "$RB" "$f" || echo "MISSING: $f"
done | tee /tmp/migration-baseline.txt

wc -l < /tmp/migration-baseline.txt   # your baseline number
echo "$(git ls-files 'db/migrations/*' | wc -l) migrations total"
```

That turns "it keeps doing this" into a number. 11 of 11 and 2 of 11 are different
problems deserving different amounts of machinery.

**Then classify the failure.** Open three migrations that *do* have a rollback and
three that don't, and answer one question: **when a rollback is present, is it
correct?** Would it actually run, and would it actually restore the prior state?

- **Rollbacks present are fine; they're just often absent** → omission. Assumption
  four holds. Build the template (Tier 1). This is the common case.
- **Rollbacks present are wrong, empty, or wouldn't run** → not omission. A template
  here makes it *worse*: you've created a required slot that gets filled with
  confident-looking garbage that now passes review. Skip the template. Your fix is
  the verification loop — the apply/rollback/re-apply run in Step 3 — plus the
  judgment notes about which operations can't be reversed.

Also worth ten minutes: if you still have the sessions, pull the corrections verbatim.

```bash
grep -rl "rollback" ~/.claude/projects/*/*.jsonl | tail -20
```

The exact words of what it did — and what it said when corrected — tell you which
wording to counter. "I'll add the down migration in a follow-up" and "this migration
is additive so it doesn't need one" call for different sentences.

---

## Step 2 — The fix, in three tiers

Do Tier 1. Add Tier 2 when Tier 1 leaks. Do Tier 3 only if this spans repos.

### Tier 1 (primary): put the requirement in the artifact

Create `db/migrations/_TEMPLATE.sql`:

```sql
-- Migration: <short imperative name, e.g. "add index on orders.customer_id">
-- Ticket:    <link, or "none">

-- ## FORWARD  (required)



-- ## ROLLBACK (required — fill exactly one of the two blocks below, delete the other)

-- [A] REVERSIBLE. Statements that return the schema to its prior state.



-- [B] IRREVERSIBLE. This change cannot be undone by SQL. Fill in all three:
--     What is permanently lost:
--     Recovery path (backup to restore, or the backfill that re-derives it):
--     How that path was verified:


-- ## VERIFIED (required — check against a scratch copy, not production)
-- [ ] forward applied
-- [ ] rollback applied
-- [ ] forward re-applied cleanly after rollback
```

Then four lines in your project's `CLAUDE.md`:

```markdown
## Database migrations

Every file in `db/migrations/` starts as a copy of `db/migrations/_TEMPLATE.sql`.
Copy it first, then fill it in. FORWARD, ROLLBACK, and VERIFIED are all required
sections; a migration with an empty section is unfinished, not a draft.

If the change cannot be reversed, fill the IRREVERSIBLE block — naming what is lost
and the recovery path — rather than leaving ROLLBACK empty.
```

**In plain English, what this does and why it's shaped this way:**

The template makes the rollback a *blank to fill*, the same as the forward SQL. You
are no longer relying on a rule being recalled at the right moment; you're relying on
an empty section being visible, which is a much lower bar. The `VERIFIED` checkboxes
do the same trick for testing: an unchecked box is conspicuous in a diff in a way that
"did you test the rollback?" in a document is not.

Two deliberate choices worth understanding, because they're the ones that are easy to
get wrong:

- **The irreversible case is a different required slot, not an exception.** The
  tempting version is "always include a rollback *unless* the migration is
  irreversible." Don't write that. An exemption clause doesn't stay in its lane —
  once "unless it's irreversible" exists, it becomes the reason a reversible migration
  ships without a down block, and you're back where you started. Block [B] is still a
  required fill, and it's *more* work than block [A], not less. The escape hatch costs
  more than compliance.
- **No softeners anywhere.** "A migration with an empty section is unfinished" is a
  statement of fact about your repo. "Try to fill in the rollback where it makes
  sense" is an invitation to decide it doesn't. Adding a single hedging clause to
  otherwise-working wording is enough to make the behavior inconsistent again.

### Tier 2: a gate, so it can't be skipped quietly

This part is mechanically checkable, and anything mechanically checkable should be
checked by a machine rather than remembered. Save the prose for the judgment calls
(*which* operations are reversible, what a real recovery path is) and let a script
handle presence.

`scripts/check-migration-rollback.sh`:

```bash
#!/usr/bin/env bash
# Runs after Claude writes a file. If that file is a migration and has no rollback
# section, exit 2 — which hands the message below back to Claude as a blocking
# error it has to resolve before moving on.
set -uo pipefail

payload=$(cat)
file=$(printf '%s' "$payload" | python3 -c \
  'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' \
  2>/dev/null)

case "$file" in
  */migrations/*) ;;
  *) exit 0 ;;                    # not a migration — say nothing
esac
[ -f "$file" ] || exit 0

if grep -qiE '^[[:space:]]*(--|#|//)?[[:space:]]*#*[[:space:]]*rollback|migrate down|def downgrade|function down|IRREVERSIBLE' "$file"; then
  exit 0
fi

cat >&2 <<'MSG'
BLOCKED: this migration has no ROLLBACK section.

A migration is not finished until it states how to undo it. Add either:
  - the reverse statements, or
  - an IRREVERSIBLE block naming what is lost and the recovery path.

Then verify on a scratch copy: apply, roll back, re-apply.
MSG
exit 2
```

Wire it up in `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/scripts/check-migration-rollback.sh"
          }
        ]
      }
    ]
  }
}
```

Run the same script in CI over changed files, so the rule holds for migrations you
write by hand too — and give the checker a self-test, so it can't rot into a green
light that means nothing:

```bash
# scripts/check-migration-rollback.test.sh — assert the checker still catches a known-bad file.
# The fixture must sit under a /migrations/ path, or the checker ignores it and the
# test passes for the wrong reason.
mkdir -p /tmp/fixture/migrations
printf -- '-- ## FORWARD\nALTER TABLE t ADD COLUMN c int;\n' \
  > /tmp/fixture/migrations/no-rollback.sql
echo '{"tool_input":{"file_path":"/tmp/fixture/migrations/no-rollback.sql"}}' \
  | scripts/check-migration-rollback.sh >/dev/null 2>&1
[ $? -eq 2 ] || { echo "checker is broken: it passed a migration with no rollback"; exit 1; }
echo "checker self-test OK"
```

That five-line test is not ceremony. Writing this up, the first version of the pattern
above matched `-- ROLLBACK` but not `-- ## ROLLBACK` — meaning it rejected every file
produced by its own template. A checker nobody checks is an assumption wearing a
badge.

**What this proves and what it doesn't.** It proves a rollback section *exists*. It
says nothing about whether that rollback works. That's the correct division: the
script covers the mechanical half (presence), the template and your review cover the
judgment half (correctness). Don't let a green check stand in for "the rollback was
tested" — the thing that proves that is the apply/rollback/re-apply run, and nothing
else.

### Tier 3: a skill — only if this spans repos

Skip this if it's one repo; a project instructions file is the right home for a
project convention. Reach for a skill when the rule follows you across repos *and*
carries real judgment (which operations are irreversible, expand/contract sequencing,
backfills that can't be undone).

If you do write one, the frontmatter is where these go wrong:

```yaml
---
name: writing-reversible-migrations
description: Use when creating, editing, or reviewing a database migration; when a
  schema change drops a column, rewrites data, or backfills; or when a deploy may
  need to be rolled back
---
```

**The trap to avoid:** do not let the description summarize the procedure. A
description like `"...writes a down block and verifies it against a scratch database"`
reads as the whole instruction, and the body — where all your hard-won detail lives —
gets skipped in favor of the one-line summary. Descriptions state *when to reach for
this*. The body states what to do. Keep that line clean and the body gets read.

---

## Step 3 — Verify it stuck

One good session proves nothing; you'd have gotten one good session by luck at least
once in the last six. Run this and you'll know:

1. **Five fresh sessions**, each given the same realistic ask: *"add a
   `deleted_at timestamptz` column to `orders` and backfill it from the archive
   table."* One session per run, no carryover.
2. **Plus a control** — one session with the template renamed out of the way. If the
   control produces a rollback anyway, the problem has already fixed itself and you
   can stop.
3. **Read all six outputs yourself.** Don't trust the grep. A rollback header with
   nothing under it, or a `down` block that drops the wrong column, passes a script
   and fails you. The script checks that the section exists; only you check that it
   would work.
4. **Count two things:** how many included a real rollback (target: 5/5), and how much
   the five differ from each other. Five near-identical shapes means the template is
   binding. Five different interpretations means it isn't — tighten the structure
   before you add more words.

Fifteen minutes, and it converts "I think this worked" into a number you can quote.

---

## If it still leaks

Match the repair to what you actually observed, not to what's easiest to add:

| What you see | Repair |
|---|---|
| Rollback section present but empty or `-- none` | The gate has become a ritual. Tighten the check to require non-blank content under the header — don't add more prose. |
| Rollback skipped only on "simple"/additive migrations | Add the one-line counter to the template header: *additive migrations are reversible, therefore they get a rollback.* Target the specific excuse, verbatim. |
| "I'll add the down migration in a follow-up" | Sequencing failure. Put the requirement at the moment of writing — Tier 2's blocking hook — not at review. |
| Template ignored entirely; file written from scratch | The copy step isn't happening. Make the generator/command that creates migrations copy the template, so there's no path to a blank file. |
| Rollbacks present but wrong | Not an omission problem at all. The fix is the verification run against a scratch database, plus notes on which operations can't be reversed. |

---

## Common mistakes with this specific fix

- **Escalating the prose.** Bold, caps, a sixth bullet, "CRITICAL:" — more emphasis
  on the wrong form is still the wrong form.
- **Adding "unless…" to the rule.** Exemption clauses spread. Give the exception its
  own required slot that costs more than compliance.
- **Treating the grep as proof.** Presence of the word is not presence of a working
  rollback. Say the weaker true thing: "has a rollback section," not "rollback
  tested."
- **Writing all three tiers on day one.** Tier 1 plus Step 3's check is usually the
  whole fix. Add the gate when you've observed it leaking, not in anticipation.
- **Declaring it fixed after one clean session.** Five plus a control, or you don't
  know.

---

## Order of operations

1. Run the baseline count. **(5 min)** — and keep the number.
2. Open six migrations, classify: omission, or bad rollbacks? **(15 min)**
3. Omission → write `_TEMPLATE.sql` + the four CLAUDE.md lines. **(15 min)**
4. Five fresh sessions plus a control; read all six. **(15 min)**
5. Still leaking → add the hook and re-run step 4. **(20 min)**

About an hour, and the seventh correction never happens.

---

## Stress Test

**The weakest point is assumption four.** Everything above routes through "Claude
writes a fine rollback once reminded; it just forgets." If it's actually writing
rollbacks that wouldn't run, a required slot is *actively harmful* — it manufactures
plausible-looking content in a section reviewers will now trust because the checkbox
is ticked. Step 1 exists solely to falsify this before you build anything, and it's
the step most likely to get skipped because the diagnosis feels obvious. It isn't
obvious; it's a coin flip you can resolve in fifteen minutes.

**A grep-based gate degrades silently.** Rename the directory, switch migration tools,
adopt a new down-block convention, and the check quietly passes everything forever —
a green check that means nothing. The self-test above is the mitigation, and it is not
hypothetical: the first draft of that pattern failed against its own template. Expect
the same class of mismatch when your conventions drift, and note that the self-test
catches a *broken* checker, not a *stale* one — if you switch tools, you must also add
the new convention to the pattern by hand.

**What a sharp critic would say:** "This is three artifacts for a problem your
migration tool already solves. Rails migrations are reversible by default, Alembic
autogenerates a `downgrade` stub, `prisma migrate diff` emits a down script. You're
building a template to reintroduce a feature you turned off." If your tool scaffolds
a down stub, that critic is right and the fix collapses to one line: enforce that the
stub is non-empty, and delete the template. I assumed a tool without that scaffolding
because you described the rollback as absent rather than empty — worth five minutes
to check whether your generator has a flag you're not passing.

**The evidence is six anecdotes, not six measurements.** Six occurrences clears the
bar for building something permanent, but you don't yet know whether it's 11 of 11 or
2 of 11, and you don't know whether the six shared a cause (all destructive
migrations? all near the end of long sessions?). A shared cause would point at a
narrower and cheaper fix than a blanket template. The baseline command is the cheapest
way to find out, and it costs five minutes against an hour of building.

**One thing I can't test from here:** whether the correction you've been giving is
actually the same correction six times. "No rollback step" could mean a missing down
block, an untested down block, or a down block that doesn't handle the data as well as
the schema. If the six were subtly different asks, the single required slot will fix
some and miss others — and the miss will feel like the fix failing when it's really
the diagnosis being too coarse. The verbatim transcript pull is the check for that.
