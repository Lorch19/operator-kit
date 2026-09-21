# Making the rollback rule stick

## What I'd have asked first

I'm running unattended, so here are the four questions and the assumption I acted on for each.

1. **Which migration tool?** Rails, Alembic, knex/Prisma, or raw SQL with a runner like Flyway/sqitch. It decides whether the inverse is a function, a paired file, or a comment block. → *Assumed you have one of these; the rule below is written once and instantiated four ways.*
2. **Are any of your migrations genuinely irreversible?** Destructive backfills and `DROP COLUMN` on populated data can't be inverted losslessly. → *Assumed yes, at least sometimes. This matters more than it looks: an unhandled exception is the argument that kills the rule on run seven. It gets its own numbered rule below.*
3. **Does CI run migrations against a scratch database?** → *Assumed you can run them locally but CI doesn't gate on it yet. I've written the local check as the primary and the CI gate as the upgrade.*
4. **One repo or everywhere?** → *Assumed one repo — you said "migrations," which implies a specific codebase. Put this in that repo's `CLAUDE.md`, not the global one. If it turns out to be three repos, the rule text is identical; only the file it lives in changes.*

---

## Why six corrections didn't take

Three separate things are failing, and you have only been fixing the first one — by hand, every session.

**1. Storage.** Each correction lived in a conversation that was discarded at session end. Session seven starts from exactly the same prior as session one. Six repetitions of a thing that is never written down is one repetition, six times. This is the obvious layer, and it's the one "just add a line to CLAUDE.md" fixes.

**2. Durability.** A bare imperative — `Always include a rollback step in migrations` — is an *assertion*. Assertions get weighed against whatever the model is reasoning about in the moment, and they lose to a plausible local argument: *this migration is additive, so nothing to undo*; *the down would just be a no-op*; *this is a one-off backfill*. Nobody in session eight remembers the rule cost you six corrections, so it gets softened once, and once it has been softened without consequence it is gone. The cure is to record the rework *beside the rule*. An assertion is argued with. Evidence is only disproven.

**3. Enforcement.** Even a well-motivated rule with a fuzzy check is unenforced while appearing checked. *"Did I include a rollback?"* is answerable by feeling — it returns whatever the model already believes, and it returns **yes** for a `down()` containing `pass`, or a `-- TODO: rollback` comment. Any check satisfiable by judgment is decorative. The check has to produce output you can read.

There's a fourth thing, subtler: **your correction arrives after the migration is already written.** It's a repair, not an instruction. Repairs don't change the next run's behaviour because they never touched the definition of what "writing a migration" means.

---

## The move: change what "done" means

Don't add a step to the migration workflow. Redefine its finish line.

> A migration is not done when the `up` is written. It is done when the `down` has been executed.

This works because "wrote the migration" is a vague bound, and vague bounds invite stopping early — the model's attention slips to *being finished* the moment the `up` looks right. "The `down` ran and here is the output" is binary. There is nothing to feel about it.

**Use `down` as the word, not "rollback step."** This isn't style. `down` is already in the model's priors from every migration framework it has ever read — it knows a `down` is the peer of an `up`, that it lives in the same file, and that it is a thing you *run*. "Rollback step" is a phrase, and a phrase can be satisfied by a comment that says rollback. If your stack doesn't already have up/down, create the convention anyway so the word in the rule and the word in the file are the same token. Then use `down` in your own prompts too — shared vocabulary between you, the rule, and the code is what makes the rule attach to the work instead of floating above it.

---

## The rule block — paste this

Numbered, because the number is how you'll cite it later (in a PR comment, a commit message, a future correction: *"DB-001"* is a whole argument in seven characters). **Never renumber.** Append new ones; retire old ones by marking them retired in place. A reused number silently rewrites what every past citation points at.

```markdown
## Database rules

### DB-001 — Every migration ships with its `down`

**Rule.** Every migration you write includes a `down` that restores the exact
prior schema, and you run `up → down → up` against a scratch database before
proposing the change. Paste the command output in the message.

**Precedent.** Six sessions in a row (<dates>) the same correction was given by
hand after the migration was already written: "<paste your actual words here>".
Every one was a repair, not a prevention — the migration was never wrong once
corrected, it was just never right unprompted. Strength: strong on recurrence
(six independent sessions, no drift in the complaint), weak on cost — no
production rollback has yet failed because of this. If one has, replace this
paragraph with that incident; it is the stronger precedent and this one retires.

**Self-check.** Not "did I consider a rollback." Run the round-trip and read the
output:

    <round-trip command for your stack — see below>

Count the migration files added or modified in this change. Count the ones whose
round-trip you just ran clean. The two numbers match, or the change isn't done.

### DB-002 — An irreversible migration says so in the file

**Rule.** When the inverse is lossy, capture what the `up` destroys before
destroying it — copy affected rows to a `<table>_pre_<migration_id>` backup
table — and write the `down` to restore from that capture. When you are choosing
not to capture, the migration file's first line is
`-- irreversible: <one-line reason>` and the same sentence goes in the PR body.

**Precedent.** This rule exists to stop DB-001 dying. The argument that kills a
reversibility rule is always "this particular one can't be reversed," and it is
sometimes true. Without a legible way to say so, a true exception reads as the
rule having been forgotten, and after two of those the rule is dead. Strength:
structural, not incident-bought — it is here to protect DB-001, and it should be
retired if you find it never fires.

**Self-check.** `grep -L 'irreversible' <migration files with no down body>`
returns nothing. Every migration either has a working `down` or is explicitly
marked. No third state.
```

### The one field I can't fill for you

The **Precedent** paragraph in DB-001 has slots. I've written the parts you told me (six sessions, correction always post-hoc) and left the dates and your verbatim words as blanks — on purpose.

A precedent is the one thing in this block that's exempt from the usual "is this line still earning its place?" pruning, because it's evidence rather than opinion. That exemption is exactly why it has to be real. A precedent invented at the desk is a stale line wearing armour: it survives every cleanup you'd otherwise do, and it argues with authority it didn't earn. If you can't source it, leave the rule bare rather than dress it in a story.

Your six corrections are recoverable in about two minutes. They're in your session transcripts:

```bash
grep -rl "rollback" --include="*.jsonl" ~/.claude/projects
```

*(Verified on your machine just now — 92 transcript files across your projects mention the term. Note the quotes around `*.jsonl`: zsh expands it otherwise and the grep silently finds nothing.)*

Narrow to the repo in question — the project directories are named after the path with slashes turned into dashes — then pull your own turns out:

```bash
grep -rh "rollback" --include="*.jsonl" ~/.claude/projects/<your-repo-slug> \
  | python3 -c "
import sys, json
for line in sys.stdin:
    try: d = json.loads(line)
    except Exception: continue
    if d.get('type') == 'user':
        print(d.get('timestamp', '?'), repr(d.get('content'))[:300])
"
```

Take the two or three sharpest phrasings and the date range. That's your precedent, verbatim and sourced.

---

## The round-trip command, by stack

Pick yours and paste it into DB-001's self-check. Every one of these is `up → down → up` — the last `up` matters, because a `down` that leaves the schema subtly different only shows up when you try to re-apply.

| Stack | Command |
|---|---|
| Rails | `bin/rails db:migrate && bin/rails db:rollback STEP=1 && bin/rails db:migrate` |
| Alembic | `alembic upgrade head && alembic downgrade -1 && alembic upgrade head` |
| knex | `npx knex migrate:up && npx knex migrate:down && npx knex migrate:up` |
| Raw SQL / sqitch | `sqitch deploy && sqitch revert -y && sqitch deploy` |

Run against a scratch database, not your dev one — otherwise the check is expensive enough that it gets skipped, and a check that gets skipped is a check that doesn't exist. A throwaway container or a `createdb scratch_$(date +%s)` is enough.

---

## Where it lives

Four places it could go, ranked by whether it's actually loaded at the moment a migration is being written.

**1. The repo's own `CLAUDE.md` — do this one.** It is in context on every turn of every session in that repo, which is the only property that matters here, and it costs you nothing to remember. That context is a budget, though: every line is paid on every turn, including the many sessions that never touch a database. So keep what's inline short — the rule sentence and the self-check command. If the precedent paragraphs grow, that's when you split.

**2. A pointer to a precedent file, once the block outgrows the budget.** Keep the rule and the command inline; move the rework stories to `docs/precedents/database.md`. Then the pointer's wording does all the work — a bare `See docs/precedents/database.md` gets read roughly never, because nothing tells the model *when*. Word it with the trigger:

> Before writing a migration, read `docs/precedents/database.md`.

A must-read behind a weak pointer is the most common way a rule silently stops firing. If you sharpen the wording and it still doesn't get read, pull the content back inline and pay the tokens.

**3. A dedicated skill.** Right when this grows from one rule into a procedure — choosing the migration strategy, the backfill pattern, the deploy ordering, the lock-duration check — that needs to fire on its own without you naming it. That's roughly five-plus related rules and a sequence. Not worth it for one rule, and it costs a permanent slice of every session's context to keep it discoverable.

**4. A CI gate or hook — the only layer that isn't persuasion.** Everything above raises the probability. This sets it to 1 for the mechanical part:

```bash
# fails when a migration lands with an empty down and no irreversible marker
for f in $(git diff --name-only origin/main...HEAD -- '*migrations*'); do
  if ! grep -qE 'def downgrade|-- *down|exports.down' "$f" \
     || grep -qE '^\s*(pass|-- *TODO)\s*$' "$f"; then
    grep -q 'irreversible:' "$f" || { echo "DB-001: $f has no down"; exit 1; }
  fi
done
```

It catches the empty `down` but not the *wrong* one — only the executed round-trip does that. So CI is the floor, not the ceiling.

**Sequencing:** do 1 now. Add 4 the first time the rule is violated *after* 1 is in place — that violation is the evidence that persuasion alone isn't enough, and it also becomes DB-001's second precedent line. Don't build the hook today; six corrections justify writing the rule down, they don't yet tell you the written rule will fail.

---

## Ten-minute version

1. Run the grep, pull your two sharpest verbatim corrections and the date range.
2. Paste the block into the repo's `CLAUDE.md`, fill DB-001's precedent slots, drop your stack's round-trip command into the self-check.
3. Next migration: say *"DB-001"* instead of re-explaining. If that's enough, the rule is live. If you find yourself re-explaining anyway, the rule text is wrong, not the placement — most likely the self-check is still answerable by feeling.

---

## Stress test

**Weakest part: the precedent is thin on cost.** Six corrections prove the behaviour recurs. They do not prove it's expensive — no rollback has actually failed in production because of this, as far as I know. A rule bought by irritation is softer than one bought by an incident, and DB-001 says so out loud rather than hiding it. If a real incident exists, use it; it retires this precedent and the rule gets much harder to argue away.

**Assumption that could be wrong: that the model is the problem.** If your migration files have no `down` scaffold — no template, no existing file with a filled-in `down` to pattern-match against — then the codebase is teaching the opposite of the rule on every read, and it will out-vote a line of prose. Check three existing migrations. If most have empty or missing `down` blocks, fix those first; the rule will keep losing until the neighbours agree with it.

**What a critic would say:** *"This is a lot of ceremony for one line in CLAUDE.md."* Partly fair — the rule sentence alone gets you most of the way, and if it holds, the precedent paragraph was overhead. The counter is that you're not at repetition one, you're at repetition six, and the thing that keeps failing is durability under a plausible local argument. That's exactly what the bare line doesn't survive. Small risk, though, and worth naming: two rules and their precedents is the start of a rulebook, and rulebooks accumulate faster than they get pruned. Set yourself a ceiling now — if `CLAUDE.md` passes five database rules, it's a skill, not a list.

**Second-order risk: the round-trip check gets skipped when slow.** If it takes more than a few seconds, it will quietly stop being run and you'll have a rule that looks enforced and isn't — worse than no rule, because you'll stop watching. If the scratch-database round-trip is slow on your schema, drop to the CI grep as the everyday gate and reserve the full round-trip for migrations touching populated tables.
