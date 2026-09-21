# Cutting a 900-line SKILL.md

## The short answer

**Length is not the defect. Unreachability is.**

900 lines is roughly 5,000 words — call it 6–8k tokens — and all of it loads, in full,
every time the skill fires, whether the task needed 40 lines of it or all 900. The
problem isn't size. The problem is that content needed 10% of the time is priced as if
it's needed 100% of the time.

So the fix is mostly **relocation, not compression**. The same words, moved into files
that load only when a task actually reaches for them. Very little of a 900-line file
deserves deletion; most of it deserves a different address.

That reframes the question from "what do I delete" (agonising, subjective) to "what has
to stay loaded" (mechanical, answerable in an hour).

One thing to do before you cut anything: go back to the two people and ask **where** they
were when it felt long, not whether it's long. "Too long" is a report about an experience,
not a diagnosis. Nine times out of ten the useful answer is a location — "I was trying to
find the error-handling bit and scrolled past four pages of API tables" — and that
location names the first thing to move out.

---

## Questions I'd normally ask first, and what I'm assuming instead

I can't ask, so here are the four answers that would change my advice, with the assumption
I'm proceeding on:

| Question | Why it changes the answer | Assumed |
|---|---|---|
| Does this skill **enforce a rule** that gets skipped under pressure, or does it **teach a method**? | Rule-enforcing skills have repetitive-looking sections that are load-bearing (see "What does not get cut"). Method skills don't. | Mixed: mostly method, with a couple of rules in it. |
| Did the two readers say "too long", or did they say "the agent ignored the part about X"? | Human reading discomfort and agent behaviour failure are different defects with different fixes. | They said long. No measured agent failure yet. |
| Is it one flat SKILL.md, or does it already have supporting files? | Determines whether you're creating a structure or extending one. | One flat file. |
| Is it invoked automatically, or does someone type its name? | Automatic invocation puts more load on the description field, which changes what must stay near the top. | Automatic. |

If assumption 1 is wrong — if this is a pure reference skill with no rules in it — skip
the "what does not get cut" section entirely and cut harder.

---

## Step 1 — Measure before you cut (15 minutes)

Don't cut from memory. Get a size-ranked map of the file first. These three commands are
tested and work as written on macOS; run them from the skill's directory.

**Where the lines actually are.** Prints every heading with the number of lines under it,
biggest first. The `awk` script tracks whether it's inside a fenced code block, so that
comments inside examples don't get counted as headings:

```bash
awk '
/^```/ {f=!f; next}
!f && /^#+ / {if(h!=""){printf "%5d  %s\n", NR-s, h} h=$0; s=NR}
END {if(h!=""){printf "%5d  %s\n", NR-s+1, h}}' SKILL.md | sort -rn | head -20
```

Expect the top 5 sections to hold 40–60% of the file. That top 5 is your whole cutting job.

**How much of it is code.** Code blocks are usually the largest single category and the
easiest to relocate:

```bash
awk '/^```/{f=!f; c++; next} f{n++} END{printf "%d of %d lines (%d%%) inside %d blocks\n", n, NR, 100*n/NR, c/2}' SKILL.md
```

**Which blocks are worth moving.** Anything over ~50 lines belongs in a file, not inline:

```bash
awk '/^```/{if(!f){f=1;s=NR;lang=substr($0,4)}else{f=0;printf "%4d lines  at L%-4d %s\n", NR-s-1, s, (lang==""?"(no lang)":lang)}}' SKILL.md | sort -rn | head
```

Also get the real word count — `wc -w SKILL.md` — because words, not lines, are what
costs you. A file of 900 short bullet lines is cheaper than 500 lines of dense prose.

---

## Step 2 — The classification test

Go through the size-ranked list from Step 1 and put every section in exactly one of three
buckets. One question per bucket, in this order:

1. **Does the agent need this to decide what to DO, on essentially every invocation?**
   → **Stays inline.** This is the decision layer: when to use, the core procedure, the
   quick-reference table, the failure modes.

2. **Does the agent need this only sometimes — only when implementing, only for one
   branch of the work?** → **Moves to a file**, linked from SKILL.md with one line saying
   what's in it and when to open it.

3. **Is it there for you, the author — history, rationale, credits, hypothetical cases?**
   → **Delete.** Not relocate. Git has the history.

The dividing line between 1 and 2 is the useful one: **SKILL.md is the decision layer,
supporting files are the execution layer.** An agent should be able to read SKILL.md,
know what to do and in what order, and know which file to open for the details of the
step it's actually on.

---

## Step 3 — The cut list, in order

Ordered by lines recovered per unit of risk. Run them top to bottom and stop when you hit
your budget. Yield figures are what's typical for a 900-line file — Step 1 gives you the
real numbers for yours.

| # | What | Where it goes | Typical yield | Risk |
|---|---|---|---|---|
| 1 | **Heavy reference material** — API surfaces, flag tables, schema dumps, syntax catalogues, exhaustive enumerations. Anything an agent *consults* rather than *follows*. | `reference/<topic>.md`, one file per topic | 150–350 | Low |
| 2 | **Runnable code over ~50 lines** | `scripts/` | 50–200 | Low |
| 3 | **Duplicate examples** — the same pattern in three languages, or four variations of one idea | Keep the single best one. Delete the rest. | 80–200 | Low |
| 4 | **Explanations the model already has** — what a PDF is, what a race condition is, how `pip` works | Delete | 30–80 | Low |
| 5 | **Narrative and provenance** — "in the October session we found…", changelogs, credits, rationale essays | Delete | 30–100 | None |
| 6 | **Decorative diagrams** — flowcharts encoding a linear sequence or reference content | Numbered list (≈⅓ the lines) or a table | 20–60 | Low |
| 7 | **Content duplicated from another skill or doc** | Name the other skill in one line and point at it | 20–60 | Med |
| 8 | **Option menus** — "you could use A, or B, or C, or D" | One default plus one escape hatch for the case that breaks it | 15–40 | Med |
| 9 | **Version-conditional and deprecated content** | A collapsed `<details>` "old patterns" block at the very bottom, or delete | 10–50 | Low |

Notes on the two that need care:

**#2 is the best line-for-line trade in the list.** Code in `scripts/` gets *executed*,
not read into context, so moving a 60-line script removes its cost outright rather than
deferring it. Inline code only earns its place when the agent needs to adapt it, not run it.

**#7, the pointer, must be a name — not an `@`-style auto-loading link.** Those file
references that force-load on sight will pull the whole target into context before the
agent needs it, which costs you more than you cut. Write `See the X skill for Y` and let
the agent decide to open it.

Running 1 through 9 in order normally lands a 900-line file somewhere between 200 and 300
without a single behaviour-bearing sentence being touched. If you're still over budget
after that, the remaining fat is in prose density, and *that's* when you start rewriting
sentences — not before.

---

## Step 4 — What does not get cut, even though it looks like padding

This is where shortening passes usually do their damage.

**The description field.** The most tempting compression move is to summarise the skill's
method into its description — "does X by doing A, then B, then C". Don't. A description
that summarises the workflow hands the agent a shortcut, and it will take the shortcut:
follow the three-step summary and never open the body. The description's job is *when to
use this*, full stop. Triggering conditions and symptoms, nothing about method.

**Trigger conditions and the "when NOT to use" list.** Usually the highest-earning lines
in the whole file, and they read like filler because they're terse. Keep them, keep them
early, keep the searchable words in them.

**Rationalization tables and red-flag lists — *if* the skill enforces a rule.** These are
the sections that look most cuttable: repetitive, obvious-sounding, a wall of short rows.
They are also the part that works. Each row exists because someone argued their way around
the rule in that exact wording, and the row is what closes that argument. Cutting them is
the single most common way a shortening pass makes a skill quietly worse — the file gets
shorter and compliance drops, which nobody notices for weeks.

The mirror of that: **if your skill has no rule anyone has an incentive to break, those
tables genuinely are padding.** Cut them without ceremony. This is why the first question
in the table above matters so much.

**The one worked example.** Keep exactly one, and keep it complete and runnable. Examples
are expensive and a complete one is worth four fragments.

**Explicit no-exception clauses.** "Don't keep it as reference, don't adapt it, delete
means delete" reads as belt-and-braces. It's the belt.

---

## Step 5 — A budget for what's left

Aim for **under 500 lines as the ceiling, 200–300 as the target**. Rough allocation for a
250-line SKILL.md:

| Section | Lines |
|---|---|
| Frontmatter (name, description) | 4 |
| Overview — core principle, 1–2 sentences | 5–10 |
| When to use / when not to | 15 |
| Quick-reference table | 25 |
| The core procedure or pattern | 80–120 |
| One worked example | 30 |
| Common mistakes | 25 |
| Pointers to reference files and scripts | 8 |

That comes to ~200–240 with headroom. If a section wants more than its allocation, that's
the signal it's a reference file wearing a section's clothing.

For each file you split out: if it ends up over 100 lines, **put a contents list at the
top.** An agent previewing a long file with `head` needs to see the full scope of what's
in there, or it'll act on a partial read.

And keep every reference **one level deep from SKILL.md**. Don't let `reference/api.md`
point at `reference/api-details.md` — agents follow the first hop reliably and the second
hop badly, often previewing instead of reading. Everything links directly from the front
page.

---

## Step 6 — Prove the cut didn't break anything

This is the step people skip, and it's the one that makes the difference between a
shorter skill and a worse one. Editing a skill is editing behaviour; you verify it the
same way you'd verify a code change.

**Before you cut:**

1. Pick 3 real tasks this skill exists to handle — the actual jobs, not toy versions.
2. Run each in a fresh session with the current 900-line skill. Save what the agent did.
   This is your baseline. You're not judging whether the output is *good*; you're
   recording *what the agent does* so you can tell if it changes.

**After you cut:** rerun the same 3 tasks with the trimmed version and diff the
**behaviour**, not the prose. Specifically:

- Did any step the agent used to take disappear?
- Did it stop opening a file you expected it to open?
- Did the shape of the output change — sections missing, order different?

**How to read the result:**

- *Behaviour unchanged* → the cut content was genuinely dead weight. Ship it.
- *A step disappeared, and it was in content you moved to a file* → the pointer isn't
  explicit enough. Fix the pointer line first ("read `reference/x.md` before doing Y") —
  don't reflexively pull the content back inline. That's the whole mechanism failing, not
  the content being needed.
- *A step disappeared, and it was in content you deleted* → it was load-bearing. Restore
  it inline, in the shortest form that reproduces the behaviour.

One caution on sampling: if what you're checking is wording-sensitive — whether the agent
follows a rule, say, rather than whether it can find an API — **a single run tells you
almost nothing.** Do 5 runs per version. And treat the *spread* as data in its own right:
if five runs of the trimmed version produce five different interpretations, the wording
isn't binding any more, even if no single run looks wrong.

---

## Two cuts that will make it worse

1. **Compressing the method into the description.** Covered above; it's the single
   highest-damage move available and it looks like pure win.
2. **Nesting your new files** to keep the top level tidy — `SKILL.md` → `advanced.md` →
   `details.md`. The content is now technically reachable and practically invisible. Flat,
   one level, always.

---

## Do it in 90 minutes

1. **(10 min)** Ask the two readers *where* they bounced. Note the locations.
2. **(15 min)** Run the three audit commands. Print the size-ranked heading map.
3. **(10 min)** Run the 3 baseline tasks against the current file. Save the transcripts.
4. **(30 min)** Work the cut list, items 1–9 in order, stopping at ~250 lines.
5. **(10 min)** Add contents lists to any split-out file over 100 lines. Check every
   reference is one level deep and no auto-loading links slipped in.
6. **(15 min)** Rerun the 3 tasks. Diff behaviour against the baseline. Fix pointers,
   restore anything load-bearing.

Commit the split-out files and SKILL.md together, so the before/after is one revision and
you can revert as a unit if the behaviour diff goes bad later.

---

## Stress test

**What's weakest here.** The yield numbers in Step 3 are estimates for a typical 900-line
skill, not measurements of yours. If your file is 900 lines of tight prose with no code,
no tables and no examples, items 1–3 recover almost nothing and the entire cut has to come
from rewriting sentences — a much slower, more judgement-heavy job than this plan implies.
Step 1 tells you within fifteen minutes which world you're in; if code + reference is under
about 25% of the file, throw out this ordering and treat it as an editing job.

**Assumptions that could be wrong.** (a) That the two readers were reacting to bulk rather
than to disorganisation. If the file is 900 well-organised lines, moving content out won't
help them at all — they needed a table of contents, and you'd be solving the agent's
problem while ignoring theirs. (b) That length is currently costing you something. If the
skill fires rarely and works fine when it does, 900 lines is a real but small tax, and
this whole exercise is optional — two complaints is two data points about reading comfort,
not evidence of a behaviour failure. The baseline runs in Step 6 are what turn that into
a measurement; if the baseline is clean and the trimmed version is also clean, you've
learned the file was never broken, just bulky.

**What a sharp critic would say.** "You've moved 600 lines into three files the agent now
has to *decide* to open. You replaced a guaranteed-loaded 900 lines with a 250-line file
plus a coin flip on the rest." That's the real risk of progressive disclosure, and the
honest answer is that the pointer lines are now the most important sentences in the skill
— each one has to say what's in the file *and* under what condition to open it, or the
content is effectively deleted. Step 6's behaviour diff exists precisely to catch this,
and "the agent stopped opening the file" is the failure mode to watch for above all others.

**The uncomfortable one.** A 900-line skill is sometimes two or three skills that were
never separated. If the audit in Step 1 shows two or three top-level sections that don't
share triggering conditions — different tasks, different moments, no overlap in when
you'd want them — splitting into separate skills beats trimming one. That's a bigger
change than you asked about, so I'd want the Step 1 output in hand before pushing it, but
it's worth a look at the heading map before you commit to the trimming path.
