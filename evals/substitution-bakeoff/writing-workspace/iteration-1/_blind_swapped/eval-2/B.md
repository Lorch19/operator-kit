# Cutting a 900-line SKILL.md

## What I'd ask first, and what I assumed instead

I can't ask, so here are the questions and the assumption I acted on for each.

| Question | Assumption I acted on |
|---|---|
| Which file? | The repo has exactly one SKILL.md near 900 lines — `pm-frameworks/ai-shaped-readiness-advisor/SKILL.md`, at **915**. I assumed that's it. The method transfers to any file; the line-by-line cut list below doesn't. |
| Did the two people say "too long to read", or "the agent stopped following it"? | Readability — no misbehaviour was reported. The cut is nearly the same either way; only the verification differs, so I've given you checks that catch both. |
| Still user-invoked? | Yes — `disable-model-invocation: true` is in the frontmatter. That matters: splitting it into more skills costs *your memory*, not context window, which makes splitting worse here, not better. |
| Should the maturity rubric be reusable by other skills? | No. If yes, it goes to a shared file outside this folder instead of inside it. |
| Is the Step 7 dependency rule authoritative or a heuristic you override? | Authoritative — it's written as four hard rules. That's what licenses turning it into a script. If you override it in practice, script only the arithmetic and keep the judgement call in prose. |

---

## First, the reframe: length is the symptom, not the defect

"Too long" is a proxy. Three different 915-line files have three different diseases and three different cures:

- **Repeated meaning** — the same thing said in two places. Cure: pick one home, delete the other.
- **Stale layers** — content that made sense two versions ago. Cure: delete.
- **Genuine length** — every line live, unique, and still too much on screen at once. Cure: *move*, don't delete.

Your file has all three, which is why "just cut the fluff" won't get you there — most of the 915 lines are not fluff. The real defect is **reachability**: right now every run loads the plan for all five priorities when only one applies, and recites five competency ladders' worth of text it needs sequentially, not simultaneously. Fix reachability and length falls out as a side effect.

**The bar isn't a line count.** It's: *every line left in SKILL.md is needed on every run.* For calibration, I counted the 141 non-deprecated SKILL.md files in this repo — median **134** lines, 75th percentile **301**, max **915** (yours). Landing near 140 is normal here, not aggressive.

---

## The sorting rule

Everything in the file goes to one of four places. Decide by asking what the agent *does* with it:

| Tier | Test | Destination |
|---|---|---|
| 1 | The agent performs it, in order, every run | Stays in `SKILL.md` |
| 2 | The agent must **reason with** it every run | Stays in `SKILL.md` |
| 3 | The agent **recites** it, or only some runs need it | `references/` behind a pointer |
| 4 | The result is the same every time given the same input | `scripts/` |
| — | No run needs it | Delete |

Two of those tests do nearly all the work:

**The branch test.** Does *every* path through the skill need this, or only some? Inline what every path needs; move out what only some paths reach. This is mechanical — you count branches, you don't judge importance.

**The reason-vs-recite test.** This is the one people miss, and it's the one that unlocks your file. "Needed every run" and "needed in context from turn one" are different claims. Text the agent reads aloud to the user is a template; it belongs in a file opened at the moment of use. Your maturity ladders are needed on every run, but the Level 3 wording for competency 5 does not need to sit in context while the agent is conducting competency 1.

---

## The cut, in order

Order matters for a practical reason: **never relocate something you were going to delete, and never disclose a duplicate into two files.** Deletions first, de-duplication second, moves third.

### Pass 1 — Delete (free, reversible, do it first)

| Block | Lines | Why it goes |
|---|---|---|
| Examples 1–3 (`771–850`) | 80 | Three filled-in runs. The agent is going to produce a filled-in run; showing it three finished ones is reassurance for a human reader, not instruction. **Don't bin them — promote them to test fixtures** (see Pass 4). |
| Common Pitfalls 1–5 (`851–897`) | 47 | Pitfall 1 restates the Purpose's "Critical Insight" and the comparison table's *Advantage* row. Pitfall 2 restates Step 7's dependency logic. The two that aren't duplicates belong inside the rubric, where they'd actually fire, not in a list at the end nobody reaches mid-assessment. |
| Anti-Patterns — "What This Is NOT" (`132–140`) | 9 | Steering by prohibition backfires: naming the wrong behaviour puts it in the frame. "When to Use This Skill" already states the scope positively. |
| Transcript scaffolding throughout | ~25 | `**Agent asks:**`, `**User response:** [Selection]`, `**Agent records:**`, the `---` rules between every block. The model conducts a conversation by default; this is paying tokens to describe turn-taking. |
| Further Reading / External Frameworks (`908–915`) | 6 | Bare citations no run opens. Keep `Related Skills` — those cross-links are live. |

**Pass 1 total: about −165 lines, zero risk.**

### Pass 2 — De-duplicate the competency definitions

Your five competencies are defined **twice at full length**:

- `34–131` (98 lines) — concept definitions with *What it includes / Key Principle / AI-first version / AI-shaped version*
- `255–420` (166 lines) — the same five subjects as four-level maturity ladders

The ladders win. Level 1 and Level 4 of each competency state the AI-first and AI-shaped versions more concretely than the concept section does — compare "AI-first version: Pasting PRDs into ChatGPT; no context boundaries" against Step 1's Level 1, which says the same thing with a diagnosis attached.

Keep, from the concept section, only each competency's one-line identity and its Key Principle. Everything under *What it includes*, *AI-first version*, and *AI-shaped version* is the ladder said twice.

**98 → about 12 lines. −86.**

### Pass 3 — Move what the agent recites

**3a. Steps 1–5 → `references/maturity-rubric.md`**

These are not five steps. They are one step run five times over a rubric: ask, present four levels, record the selection. The only thing that varies is the rubric text.

Replace all 166 lines with roughly this in `SKILL.md`:

```
### Step 1: Assess the five competencies

Work through the competencies in the order listed in
`references/maturity-rubric.md`. For each, present its four levels
verbatim — do not paraphrase them; the wording is what makes scores
comparable across sessions — and record the user's selection.

All five competencies must have a recorded level before Step 2.
If a profile is internally implausible (Level 4 Strategic
Differentiation on Level 1 Context Design), say so and re-ask
before scoring.
```

**166 → about 10 lines. −156.**

**3b. Step 8 → `references/plans/*.md`, one file per priority**

This is your single biggest win: **243 lines, of which exactly one branch fires per run.** `If Priority = Context Design` through `If Priority = Strategic Differentiation` are mutually exclusive; about 195 of those lines are dead weight on every session.

Five files — `context-design.md`, `agent-orchestration.md`, `outcome-acceleration.md`, `team-ai-facilitation.md`, `strategic-differentiation.md`. `SKILL.md` keeps the step, the completion criterion, and the mapping.

**243 → about 12 lines. −231.**

### Pass 4 — Script the deterministic middle

Steps 6 and 7 (`421–508`, 88 lines) contain no judgement. Step 6 averages five integers and maps the result to one of four labels. Step 7 applies four stated dependency rules to pick a priority. In plain English: that's arithmetic plus an if/else tree, written out as 88 lines of prose for a model to re-derive every single run — which is both slower and less reliable than computing it, because a model can slip on arithmetic and a script can't.

`scripts/score.py` takes five integers and prints the profile table, the overall label, and the recommended priority. `SKILL.md` keeps about 10 lines: run the script, present its output, and the one thing the script can't do — sanity-check the answers before feeding them in.

**And this is where your three Examples go.** Each one is a set of five levels and the priority that should come out. That is a test case. `scripts/test_score.py` turns them from 80 lines of context cost into a passing check that your dependency logic still works.

**88 → about 10 lines. −78.**

### Pass 5 — Split into separate skills: don't

Worth naming so you don't reach for it later. The five competencies look like five skills. They aren't:

- They're assessed together — the priority rule needs all five scores at once.
- Five new skills means five more things you have to remember exist, since this one is user-invoked. That cost is real and it's yours, not the context window's.
- The branching in this file is in the **plan**, not the **assessment**. Plans are reference material. Reference behind a pointer is already the cheapest form of this; a skill is the most expensive.

**−0. Skip it.**

---

## Where it lands

| Block | Now | After | Action |
|---|---|---|---|
| Frontmatter + Purpose | 17 | 10 | Tighten — Purpose restates the description |
| AI-First vs AI-Shaped table | 14 | 14 | **Keep in full** |
| 5 Competencies (deep defs) | 98 | 12 | Collapse into rubric |
| Anti-Patterns | 9 | 0 | Delete |
| When to Use | 16 | 10 | Tighten |
| Facilitation Source of Truth | 14 | 8 | Keep the cross-skill contract |
| Application + Protocol + Session Start | 58 | 25 | Keep the mandatory protocol, cut scripted dialogue |
| Step 0: Gather Context | 23 | 15 | Keep |
| Steps 1–5 | 166 | 10 | → `references/maturity-rubric.md` |
| Step 6: Profile | 34 | 4 | → `scripts/score.py` |
| Step 7: Priority Gap | 54 | 6 | → `scripts/score.py` + plan headers |
| Step 8: Action Plan | 243 | 12 | → `references/plans/` ×5 |
| Step 9: Track Progress | 18 | 8 | Keep, tighten |
| Examples ×3 | 80 | 0 | → `scripts/test_score.py` fixtures |
| Common Pitfalls ×5 | 47 | 0 | Two fold into the rubric; three are duplicates |
| References | 18 | 8 | Keep Related Skills only |
| **SKILL.md** | **915** | **~142** | |

Roughly **−85%**, with nothing of substance lost — the plans, the rubric, and the worked examples all still exist, they're just reached when needed instead of carried always. Lines actually read on one session: ~142 plus the rubric plus one plan file, and the plan only loads after the priority is known.

---

## What never leaves SKILL.md, no matter the length

1. **The ordered steps and their completion criteria.** "All five competencies must have a recorded level" is what stops the agent declaring the assessment done at three.
2. **The AI-first vs AI-shaped distinction** (`20–33`). This is the one idea the whole skill turns on — the concept the agent thinks *with* while running everything else. It's 14 lines and it's the last thing you should touch.
3. **Anything the agent must reason with**, as opposed to recite.
4. **The pointers themselves**, worded as conditions.
5. **The mandatory facilitation protocol.** It governs turn-by-turn behaviour; behind a pointer it gets read once and forgotten by turn six.

---

## Word the pointers as conditions, not labels

This is where a cut like this usually fails. A pointer's *wording*, not its location, decides whether the agent actually opens the file.

**Weak (a label — this is how relocations quietly break):**
```
See references/plans/ for action plans.
```

**Strong (condition + file + what to do with it):**
```
Once the priority is recorded, read
`references/plans/<priority-slug>.md` and deliver it in full.
Do not summarise it — the phases, weekly sequence, and success
criteria are the deliverable.
```

Name the triggering state, name the file, and say what to do with the contents. If a pointer to must-have material doesn't fire reliably, **fix the wording before you consider pulling the material back inline.**

---

## How to know the cut worked — checks you can measure, not judge

1. `wc -l SKILL.md` → target ≤ 200. Repo median is 134 across 141 skills.
2. Run the full assessment 3 times. Grep each transcript for `maturity-rubric.md` and for the plan filename. **Must be 3/3.** Below that, the pointer wording is the bug.
3. Count the levels recited per run: must be exactly **20** (5 competencies × 4 levels). If a run recites three levels for a competency, the rubric is being skimmed rather than presented, and your scores stop being comparable between sessions.
4. `python3 scripts/test_score.py` — the three ex-Examples must still produce their original recommended priority.
5. **The one that actually settles it:** run the same five answers against the old file and the new one. The prose will differ. The *recommended priority and the plan delivered must be identical.* If they diverge, you changed behaviour, not just length.

Do this on a branch, and run check 5 before you merge.

---

## Stress Test

**Weakest link: I inferred your file from a line count.** 915 was the only near-900 match in the repo. If it's a different file, the five passes and the sorting rule transfer intact; every specific line number above does not.

**The relocation most likely to bite you is the rubric, not the plans.** The plans are a clean branch cut — one fires, four don't, nothing can go subtly wrong. The rubric is different: it's material the agent must present *verbatim*. If it starts paraphrasing from the file instead of quoting it, users pick levels against slightly different wording each session and your scores silently stop being comparable. That is a consistency regression introduced by a readability fix, and it is far harder to notice than 915 lines. Check 3 exists for exactly this. If it fails twice after sharpening the pointer, put the rubric back inline and accept the length — 300 lines that work beat 142 that drift.

**What a smart critic would say:** two people is two data points, and both are humans reading a file written for a machine. Human readability and agent consistency correlate but are not the same thing. If the skill currently produces good assessments, "too long" is an aesthetic complaint about an artifact that works. That's why check 5 is the one that matters — it's the only one that tests the thing you actually care about rather than the thing that's easy to count.

**Over-correction risk in Pass 4.** Scripting Steps 6–7 removes the agent's opportunity to notice that a user's answers don't hang together — Level 4 Strategic Differentiation on Level 1 Context Design is implausible under your own dependency rules and is probably a mis-click. A script will compute a confident priority from nonsense. That's why the implausibility check stays in `SKILL.md` as prose, ahead of the script call. Don't drop it for tidiness.

**The target itself is a proxy.** 142 lines of dense conditional logic can be harder for an agent to follow than 300 lines of a clean table. What you're optimising is lines *read per run*, and whether each one changes behaviour — not the number `wc -l` prints.
