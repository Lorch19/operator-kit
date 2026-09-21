# Fixing a skill that won't fire

## Short answer

`Helps with data analysis tasks` is a category label, not a trigger. The router
never sees your task — it sees your description and decides whether to open the
skill at all. Nobody types "I have a data analysis task"; they type "why did
signups drop in March" or "what's in this CSV." Those strings have nothing to
match against, so the skill stays shut.

The fix is a description made of **triggering conditions and concrete nouns**,
not a capability summary. But rewrite it second. Rewrite it *first* and you'll
have swapped one guess for another with no way to tell if you improved anything.
Build the failing test first: collect the real prompts where it should have
fired, confirm they miss today, then rewrite until they hit.

---

## Questions I'd ask, and what I'm assuming instead

| Question | Assumption I'm proceeding on |
|---|---|
| What does the skill actually do — exploratory analysis, statistical testing, chart generation, pipeline code? | Tabular data work: load, clean, summarize, compare, chart. If yours is narrower, the *formula* below still holds; swap the nouns. |
| What prompts were you using when it failed to fire? | You don't have them written down. Step 2 recovers them from your transcripts. |
| Are there neighboring skills that might be winning the match instead? | At least one exists (a SQL skill, a spreadsheet skill, or a charting skill). Step 1 checks for this — "didn't fire" and "a sibling fired instead" need different fixes. |
| Is the skill even loading? | Unverified, so Step 0 checks it. A malformed frontmatter looks identical to a bad description from where you're sitting. |
| Is this skill model-invoked, or does your setup require you to call it by name? | Model-invoked. If it's user-invoked-only, no description on earth will fire it and the fix is a config change, not a wording change. |

---

## Step 0 — Rule out the causes that aren't the description

You asserted the description is the problem. It probably is, but four other
faults produce the identical symptom, and tuning prose against a skill that
never loads is pure waste. Ten minutes:

**1. Is it parsed and listed?** Run `claude plugin list` (or your runtime's
equivalent) and confirm the skill appears with the description you expect. If it
isn't in the list, nothing downstream matters.

**2. Does the frontmatter parse?** A stray colon, a tab, or an unquoted `:` in
the description silently drops the whole file:

```bash
python3 -c "import yaml,sys; print(yaml.safe_load(open(sys.argv[1]).read().split('---')[1]))" path/to/SKILL.md
```

It should print a dict with `name` and `description`. An exception means the
skill is invisible.

**3. Is the name legal and unique?** Letters, numbers, hyphens only — no spaces,
no parentheses, no underscores in some runtimes. And if two installed skills
share a name, one shadows the other:

```bash
grep -rh '^name:' ~/.claude/skills ~/.claude/plugins 2>/dev/null | sort | uniq -d
```

Any output is a collision.

**4. Is it losing to a neighbor rather than being ignored?** In the sessions
where it should have fired, did *some other* skill fire instead? That's a
different problem — a boundary dispute, fixed by editing **both** descriptions
so each names what it is not. Making only yours louder just produces two skills
that both claim the territory.

If all four are clean, the description is the cause. Proceed.

---

## Step 1 — What's actually wrong with those five words

| Defect | Why it kills the match | Repair |
|---|---|---|
| **"Helps with"** | Every skill helps with something. The first words carry the most weight and yours spend them on filler that distinguishes nothing. | Open with `Use when` and go straight to the situation. |
| **"data analysis tasks"** is a category, not a situation | The router compares your description against the *user's actual words*. Users describe symptoms and artifacts ("this CSV", "the numbers look off", "is this significant"), never the category they fall under. Matching happens at the level of the words people type. | Enumerate the situations in the phrasing people use. |
| **Zero keyword surface** | Thirty characters, none of them a file type, a tool, a statistic, an error, or a symptom. There is almost nothing for a match to land on. | Name the artifacts (`CSV`, `Excel`, `query results`), the operations (`summarize`, `compare`, `chart`), and the vocabulary (`p-value`, `outlier`, `missing values`, `correlation`). |
| **No negative boundary** | Nothing tells the router when a *different* skill is the right one, so overlapping skills compete on noise. | Add one short "not for X" clause naming the nearest neighbor. |
| **Describes the skill, not the moment** | "Data analysis" is what the skill is about. It never says *when in the conversation* to open it. | Triggering conditions are the whole job of this field. |

Note the shape of the failure. This is not an agent ignoring a rule it read —
it's an agent that never read anything. So the repair is discovery surface, not
stronger language. Adding `IMPORTANT` or `ALWAYS` to the description does
nothing here; you cannot emphasize your way into a match that isn't happening.

---

## Step 2 — Write the failing test before you touch the description

You currently have an impression ("keeps not firing"), which can't tell you when
you're done. Convert it into a fixed set of prompts, scored the same way before
and after.

**Recover the real prompts.** Your session transcripts hold what you actually
typed. This pulls one line per typed prompt, skipping tool output and system
injections:

```bash
jq -r 'select(.type=="user" and has("promptSource"))
       | (.message.content
          | if type=="string" then . else (map(select(.type=="text").text)|join(" ")) end)
       | gsub("\\s+";" ")' ~/.claude/projects/*/*.jsonl 2>/dev/null \
  | grep -v '^<' \
  | grep -iE 'csv|spreadsheet|dataframe|chart|plot|correlat|outlier|p-value|significan|cohort|metric|why did .* (drop|spike|fall)' \
  | sort -u
```

Widen or narrow the pattern to fit your skill. You're mining for the phrasings
*you* use, which are the phrasings the description has to match.

**Build the set.** Aim for:

- **10–15 positives** — prompts where the skill genuinely should have fired.
  Include the boring ones ("take a look at this file"), because those are the
  ones a keyword-poor description misses.
- **5+ negatives** — prompts where it should stay shut, especially ones near a
  sibling skill's territory. Without these you'll "fix" triggering by making the
  skill fire on everything, which is a worse failure that's harder to notice.

**Run the baseline.** For each prompt, a fresh agent gets only the skill
*metadata* (names + descriptions of the installed set, current wording) and the
prompt, and answers one question: which skill, if any, should be opened? One
sample per call, fresh context every time — no accumulated hints. Record
hit/miss.

**You need the baseline to actually fail.** If the current description already
hits 12 of 15, the description isn't your problem and you should go back to Step
0. Don't skip this because you're sure. Five minutes of measurement here is what
makes every later change interpretable instead of a vibe.

---

## Step 3 — The rewrite

**Formula:**

```
Use when <situation, in the words the user types>
       + <concrete artifacts: file types, data shapes, tools>
       + <symptom vocabulary: what they say when the need arises>
       + <one negative boundary naming the nearest neighbor>
```

**Applied, under my stated assumption about scope:**

```yaml
---
name: analyzing-tabular-data
description: Use when the user has tabular data — a CSV, Excel file, query
  result, exported report, or pasted table — and wants it explored, cleaned,
  summarized, compared, or charted; when they ask why a metric moved, whether a
  difference is real, which rows are outliers, or what the data shows; or when
  they mention dataframes, pandas, pivot tables, correlation, p-values,
  distributions, or missing values. Not for authoring SQL against a live
  warehouse, or for production pipeline code.
---
```

476 characters. The frontmatter cap is 1024 total; under 500 for the description
is the working target, so there's room but not much — spend it on trigger
vocabulary, not on prose.

**Rename too, if the name is as generic as the description was.** The name is
metadata the router also reads, and a verb-first or gerund name carries real
signal: `analyzing-tabular-data` over `data-analysis`, `exploring-datasets` over
`data-helper`. Name by what you *do*.

**Re-derive it for your real scope** by answering four questions and pasting the
answers into the formula:

1. **What's in front of the user when they need this?** A file? A pasted table?
   A failing number on a dashboard? Name those objects literally.
2. **What do they type?** Pull five actual phrasings from the grep in Step 2.
   Not paraphrases — their literal words.
3. **What vocabulary is unique to this territory?** Statistics, formats, library
   names, error strings. These are your highest-value tokens because nothing
   else in your skill set contains them.
4. **Which neighboring skill gets confused with this one?** Name it in a "not
   for" clause, and add the mirror-image clause to *that* skill's description.

---

## Step 4 — The trap on the other side

There's a second failure mode that a rewrite can walk you straight into, and
it's sneakier than the one you have because the skill *does* fire, so it looks
fixed.

**Don't summarize the workflow in the description.**

```yaml
# Creates a new problem
description: Use when analyzing data — load the file, check for nulls, compute
  summary stats, run significance tests, then chart the result.

# Correct
description: Use when the user has tabular data — a CSV, Excel file, query
  result... [triggers and nouns only]
```

The description is injected into the agent's context; the skill body is not,
until the skill opens. If the description already reads like an abbreviated
procedure, the agent has a usable shortcut and will act on the four-step summary
instead of opening the file and following the fifteen-step real thing. You end
up with a skill that fires reliably and gets followed shallowly — and because
the routing now looks correct, you'll spend a long time not understanding why
the outputs are thin.

Nouns are safe. Verb sequences are not. `pivot tables, p-values, missing values`
tells the router what territory this is. `first do X, then do Y` tells the agent
it no longer needs to read.

---

## Step 5 — Measure, then close the gaps

Re-run the identical prompt set against the new metadata, same protocol, fresh
context each time. Then read each result by hand — don't trust the tally alone,
because a "hit" where the agent picked your skill for the wrong stated reason is
a coincidence that will stop working.

Three failure modes and their distinct repairs:

| What you see | What it means | Repair |
|---|---|---|
| Still missing specific prompts | Those prompts' vocabulary isn't in the description | Add the literal words from the missed prompts. Not synonyms — the actual words. |
| Now firing on the negatives | Description over-claims | Tighten the trigger clause and strengthen the "not for" boundary. Don't just delete keywords; you'll re-break the positives. |
| A neighbor skill wins on prompts that should be yours | Boundary dispute, not a discovery failure | Edit both descriptions. Each names the other's territory as out of scope. Only editing yours produces two skills claiming the same ground. |

**Variance is a signal, not noise.** Run each prompt 5+ times. If the same
prompt routes differently across repeats, the description isn't binding yet —
five different readings mean the wording is ambiguous, and the answer is a
sharper form, not more words. Consistent results across repeats, positives
hitting and negatives staying shut, is your stopping condition.

Keep the prompt set in the skill's directory. Next time you edit the
description, you already have the test.

---

## Checklist

- [ ] Skill appears in the installed list with the expected description
- [ ] Frontmatter parses; `name` and `description` both present
- [ ] Name is letters/numbers/hyphens, unique across installed skills, verb-first
- [ ] 10–15 positive prompts collected from real transcripts
- [ ] 5+ negative prompts, including ones near a sibling skill
- [ ] Baseline run with current wording — **and it actually fails**
- [ ] Description starts with `Use when`, third person
- [ ] Contains artifacts, operations, and domain vocabulary as literal keywords
- [ ] Contains one negative boundary clause
- [ ] Contains **no** step-by-step workflow summary
- [ ] Under 500 characters (1024 hard cap on frontmatter)
- [ ] Neighbor skill's description updated with the mirror boundary
- [ ] Re-run: positives hit, negatives stay shut, 5+ reps each, every result read by hand
- [ ] Prompt set committed alongside the skill

---

## Stress Test

**Weakest part of this.** I've assumed the failure is discovery. It could be
adjacency instead: the skill fires fine on obvious prompts and misses only at
the edges, which reads as "keeps not firing" when you're the one living it but
is a much smaller problem. Step 0's baseline is what separates these, which is
exactly why skipping it to get to the rewrite is the most likely way this goes
wrong.

**Assumption that could be wrong.** I treated the scope as tabular-data
analysis. If the skill is actually about something narrower — a specific
in-house dataset, a particular statistical method, one reporting pipeline — then
my candidate description is too broad and will fire on prompts it can't serve.
That's the over-firing failure in the Step 5 table, and it's worse than what you
have now: a skill that fires and doesn't help costs you context and trust, where
a skill that stays shut just costs you a manual invocation.

**What a critic would say.** "This is a lot of process for one line of YAML."
Fair, and if you have one skill, wing it. The process earns its keep at the
second and third skill, when descriptions start competing and a change that
fixes one skill's routing quietly breaks another's. The prompt set is the only
thing that catches that, and it's cheap once it exists.

**What would change my mind.** If the baseline shows the current description
hitting most of your positives, the routing is fine and the real complaint is
about what the skill does once opened — a body problem, not a metadata problem,
and none of the above applies.

**Unresolved tension worth naming.** There are two defensible schools on this
field: "triggers only" and "what it does plus when to use it." They conflict on
the margin. My resolution — nouns describing territory are safe, verb sequences
describing procedure are not — is a reading, not a settled fact. If your skill
bodies are short enough that a shortcut costs nothing, the stricter rule buys
you less than it costs in keyword surface.
