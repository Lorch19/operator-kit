# "Helps with data analysis tasks" — why it can't fire, and what to replace it with

Your description isn't a weak trigger. It has **zero** triggers. That's a different problem with a different fix, and it's why tinkering with the wording ("Helps with data analysis and reporting tasks") won't move anything.

Below: one check that could make this whole exercise moot, the diagnosis, the rewrite procedure, and how to prove the fix worked instead of hoping.

---

## 0. First, the ten-second check that could make this moot

Before rewriting anything, look at the skill's frontmatter:

```bash
sed -n '1,10p' path/to/your-skill/SKILL.md
```

If you see `disable-model-invocation: true`, **stop — no description can fix this.** That flag strips the description out of the agent's reach entirely. The skill becomes invisible to the model and reachable only by you typing its name. The description field is still there, but it's now a note for humans, not a trigger for the agent.

This is a live hypothesis, not a formality. "Helps with data analysis tasks" is *exactly* what a human-facing one-line summary looks like — short, descriptive, no trigger language. Someone may have written it that way on purpose, or copied it from a skill where it was correct. If the flag is set, deleting that one line is your entire fix.

Two lesser versions of the same check, both cheap:

```bash
# Is the skill even on disk where it gets discovered?
ls ~/.claude/skills/ ~/.claude/plugins/*/skills/ 2>/dev/null | grep -i <skill-name>

# Does another skill share the name? A collision resolves to one winner.
find ~/.claude -name SKILL.md -exec grep -l "^name: <skill-name>" {} \;
```

Everything below assumes these come back clean: the skill is discoverable, uniquely named, and model-invocable. If so, the description really is the bug.

---

## 1. Why this exact string cannot fire

A description does two jobs: say what the skill is, and list the **situations** that should pull it in. Yours attempts the first and skips the second entirely. Three independent failures, each fatal on its own:

**It names a topic, not a moment.** The agent doesn't fire a skill because a skill is topically adjacent to what you're doing. It fires when the situation in front of it matches a situation the description described. "Data analysis tasks" is a category label. There is no moment in it — nothing for the agent to match a real prompt against. Compare: *"Use when the user shares a CSV and asks what it says"* is a moment. *"data analysis tasks"* is a shelf label.

**The first three words are dead.** "Helps with" is where the description does its hardest invocation work, and you've spent that position on filler that describes every skill ever written. The strongest word should be first and it should be a word you actually type.

**It fails the only test that matters: does it change behaviour versus the default?** The agent already does data analysis, competently, without loading anything. So the description gives it no reason to treat your prompt as *a moment for a skill* rather than *a moment to just start working*. This is the deepest of the three problems. An instruction the model already obeys by default costs you context and buys nothing — and that principle applies to descriptions just as hard as to skill bodies. "Helps with data analysis tasks" describes the model's baseline behaviour. It's a no-op wearing a frontmatter key.

There's a fourth thing worth naming, because it explains the *"when I actually need it"* part of your complaint. You notice the failure precisely on the hard cases — the ones where you needed the skill's specific method rather than generic competence. But those are the cases whose prompts contain the most specific language ("is this lift real or noise?", "break ARR by cohort"), and a description made of maximally generic language matches specific prompts *worst*. The vaguer the description, the more it fails exactly when it matters.

---

## 2. What a description actually is

Plain English, because this is the mental model that makes the rest obvious:

A description is a **pointer** sitting in the agent's context every single turn. It names something not currently loaded (your skill) and encodes the condition for going and getting it. The target doesn't decide when the agent reaches — **the wording does.** A brilliant skill behind a vague pointer is unreachable, and the agent will never know what it missed.

That's the whole mechanism. You are not writing a summary for a catalogue. You are writing the if-condition on a branch the agent evaluates every turn.

---

## 3. The fix, in four moves

### Move 1 — Harvest your own words, don't invent triggers

The single most common mistake here is writing the description from the skill's point of view ("what does this skill do?") instead of from your prompt's point of view ("what do I say when I want it?"). Those produce different vocabularies, and only one of them is what the agent sees at trigger time.

So go get the real language. Your last few months of prompts are on disk:

```bash
cd ~/.claude/projects && grep -rh '"type":"user"' ./*/*.jsonl 2>/dev/null | python3 -c "
import sys, json, re
KEYWORDS = r'analy|dataset|csv|metric|cohort|funnel|retention|churn|chart|numbers|breakdown'
seen=set()
for line in sys.stdin:
    try: d=json.loads(line)
    except: continue
    c=d.get('message',{}).get('content')
    t=c if isinstance(c,str) else ' '.join(b.get('text','') for b in c if isinstance(b,dict)) if isinstance(c,list) else ''
    t=' '.join(t.split())
    if not t or t.startswith(('<','[Request')) or len(t)>200: continue
    if re.search(KEYWORDS, t, re.I) and t not in seen:
        seen.add(t); print('-', t)
" | head -40
```

(Swap `KEYWORDS` for terms that fit your skill. This is a rough net — it over-collects, which is what you want at this stage.)

Now read the output and pull out the 10–20 lines where you genuinely wanted this skill. **Those verbatim phrasings are your raw material.** Not paraphrases of them.

### Move 2 — Collapse the list into distinct branches

You'll have duplicates in disguise. *"check if the funnel is leaking"* and *"where are people dropping off in signup"* are one situation written twice. Merge them. Spending description tokens on two names for one case is pure cost: it inflates the length without adding a single new moment the skill can catch.

Keep the cases that are **genuinely different paths through the skill** — different enough that the skill would do different work. Aim for 3–5. If you end up with 12, you have a scope problem, not a description problem (see §5).

### Move 3 — Front-load the word you actually use

Pick the one compact term that lives in your prompts, your docs, and your file names when this work comes up — and put it first. Shared vocabulary is what makes triggering reliable: when the same word appears in how you ask, how your repo is named, and how the skill is described, the agent links them. A term the model already understands beats a coined one, because you get its meaning for free instead of paying tokens to define it.

### Move 4 — Cut everything the body already says

The description isn't a preview of the skill. Anything explaining *how* the skill works belongs in the body — it's loaded only when the skill fires, where it's free. The description carries triggers, and nothing else, because it's paying rent every turn whether the skill fires or not.

---

## 4. The rewrite, worked

**Before**

```yaml
description: Helps with data analysis tasks
```

**The shape to write**

```yaml
description: "<Strong verb> <specific object> — <the 2-4 concrete outputs>. Use when <trigger 1>, <trigger 2>, <trigger 3>, or <trigger 4>."
```

**After** *(filled with my best guess at your skill — see the assumptions in §8; swap the triggers for the ones your harvest produced)*

```yaml
description: "Analyze a dataset end to end — profile it, clean it, segment it, and test whether the claim the numbers are being used to support actually holds. Use when the user shares a CSV, export, or query result and asks what it says; wants a metric broken down by segment; asks whether a movement in a number is real or noise; or asks which cut of the data explains a trend."
```

Four distinct moments, each phrased the way a person actually types it. Front position spent on "Analyze a dataset" rather than "Helps with." Nothing in there that the agent would do identically without the skill.

**The house pattern, from skills that do fire.** This shape isn't theoretical — it's what the working analytics skills in your kit already use:

> `ab-test-analysis`: "Analyze A/B test results with statistical significance, sample size validation, confidence intervals, and ship/extend/stop recommendations. **Use when** evaluating experiment results, checking if a test reached significance, interpreting split test data, or deciding whether to ship a variant."

> `cohort-analysis`: "Perform cohort analysis on user engagement data — retention curves, feature adoption trends, and segment-level insights. **Use when** analyzing user retention by cohort, studying feature adoption over time, investigating churn patterns, or identifying engagement trends."

> `sql-queries`: "Generate SQL queries from natural language descriptions. … **Use when** writing SQL, building data reports, exploring databases, or translating business questions into queries."

Same skeleton every time: strong verb, specific deliverables, then `Use when` plus four distinct situations. Match it.

---

## 5. If you can't list four distinct triggers, the description isn't the problem

This is the outcome I'd actually bet on, and it's worth saying plainly because it's the uncomfortable answer.

If the honest description of when you want this skill is *"whenever data is involved,"* then no wording rescues it. A skill that claims all of data analysis is competing with the model's defaults on ground the model already holds — it will lose, because from the agent's side there's no distinguishable moment to fire on. Vagueness in the description is usually a symptom of vagueness in the skill.

The fix then isn't lexical, it's structural:

- **Narrow it.** What does this skill do that the agent visibly does *worse* without it? That — and only that — is the skill. Everything else is the default, and you should let the default handle it.
- **Or split it.** If it genuinely holds three unrelated jobs, three sharply-triggered skills beat one blurry one. But each new description is permanent rent on your context window, so only split where you have a real, distinct word that should pull each piece in on its own.

Test: write the sentence *"Without this skill, the agent would get X wrong."* If you can't finish it concretely, fix the skill before the description.

---

## 6. Check the neighbours

Your kit already ships `ab-test-analysis`, `cohort-analysis`, and `sql-queries`, each with a sharp, specific description (quoted above). If your skill's territory overlaps any of them, a vague description loses the competition every time — the agent picks the pointer that matches the situation most precisely, and "data analysis tasks" is the least precise thing in the room.

So after rewriting, run:

```bash
grep -rh "^description:" ~/.claude/skills/*/SKILL.md ~/.claude/plugins/*/skills/*/SKILL.md 2>/dev/null
```

Read your new description next to its nearest three neighbours and ask: for each of my four triggers, is there another skill whose description also plausibly claims it? Where there is, either carve the boundary explicitly in one of them, or accept that you've got two skills doing one job and merge them.

---

## 7. Prove it fired — don't ship on a vibe

"It feels like it's firing more" is not a result, and you'll be tempted to accept it because rewriting felt productive. Do this instead — it's about twenty minutes:

1. **Build a probe set.** 5 prompts lifted *verbatim* from your harvest in §1 that should fire the skill, plus 4 near-misses that should *not* (adjacent data questions the skill isn't for). Write them down before you change anything.
2. **Baseline first.** Run all 9 against the *current* description, each in a fresh session, recording fired / didn't. This is your before number. Skipping it means you'll never know whether the rewrite helped or you just got luckier prompts.
3. **Rewrite, then re-run the same 9.**
4. **Score both directions.** Fires on the 5 is the thing you're fixing. Silence on the 4 is the thing you can easily break: a description tuned only for recall starts firing on everything, and then you're paying context load plus the cost of the agent detouring through a skill that doesn't fit. A good result is 5/5 and 0/4, not 9/9.

Fresh session per probe matters — mid-conversation the agent is already committed to a task, and that suppresses firing independently of your wording. You'd be measuring conversational momentum rather than the description.

---

## 8. Still silent? Read the failure shape

The *pattern* of failure tells you which lever to pull next:

| What you observe | What it means | Next move |
|---|---|---|
| Never fires, even on a prompt quoting your description verbatim | Not a wording problem | Re-check §0: the invocation flag, discovery path, name collision |
| Fires in a fresh session, not mid-task | Attention, not wording | Expected. Type the name, or get the leading word into your habitual prompts (§9) |
| Fires *late* — after the agent has already started the analysis | Trigger matched, but too weakly | Move the matching phrase to the front of the description |
| A different skill fires instead | Neighbour competition | §6 — carve the boundary or merge |
| Fires on everything now | Over-corrected in §7 | Drop the broadest trigger; re-run the 4 near-misses |

---

## 9. The half of the fix that isn't in the file

Triggering gets more reliable when the same term lives in your prompts, your directory names, and your docs — not just in the description. The agent links that shared language to the skill. So the highest-leverage version of this fix is: pick the term, put it in the description **and** start using it when you ask.

Which means the loop is: harvest the words you already use → put them in the description → and then keep using them deliberately. That's a habit, not an edit, and it's why description work tends to pay off over a few weeks rather than instantly.

---

## Questions I'd have asked, and what I assumed instead

I couldn't ask, so here's each question, my assumption, and where it would have changed the answer:

1. **Is `disable-model-invocation: true` set?** Assumed no — otherwise your premise (that the description matters) wouldn't hold. But it's a genuinely plausible cause given how human-facing your current string reads, which is why it's §0 and not a footnote. If it's set, sections 1–9 are moot and deleting one line is the whole fix.
2. **What does the skill actually do?** Assumed a general "take a dataset, produce decision-ready analysis" skill, since that's the most common thing behind that wording. The §4 example is built on that guess — replace its four triggers with yours. The *shape* transfers regardless of what I guessed.
3. **What were you typing the last five times it should have fired?** Unknowable from here, which is exactly why §1 is a command that extracts it from your transcripts rather than a suggestion that you recall it. Recalled triggers are reconstructions; harvested ones are evidence.
4. **Never fires, or fires late?** Assumed never. If it's actually late-firing, skip to the §8 row — that's a front-position problem, a much smaller fix.
5. **Does it overlap the three analytics skills already in your kit?** Assumed possible, so §6 is included as a check rather than a conclusion. If it substantially overlaps, the real answer may be "merge it into `cohort-analysis`" rather than "fix the description."

---

## Stress Test

**The weakest thing here.** I've diagnosed a description I can see, for a skill I can't. My confidence that "Helps with data analysis tasks" cannot fire is high and doesn't depend on the skill's content. My confidence that a rewrite *fixes your problem* is much lower — because the most likely story is §5: the description is vague because the skill's job is vague, and the rewrite just moves the vagueness into better prose. Watch for this signal: if filling in the four triggers feels like inventing rather than recalling, you're in §5 and §4 is a distraction.

**An assumption that could be wrong.** I've treated the description as the sole cause. Firing is also affected by how many skills are loaded, how far into a conversation you are, and what the model is already committed to. If you're running a large kit — and you are, well past a hundred skills — some of your misses may be crowding rather than wording, and a rewrite will produce a real-but-smaller improvement than §7 leads you to expect. The 4 should-not-fire probes are partly there to catch this: if *other* skills fire on them, crowding is in play.

**What a smart critic would say.** "You told him to measure with nine probes and single runs each. Invocation is stochastic — a single run per probe has real variance, so a 3/5 → 5/5 move might be noise." That's correct and I'd accept the correction: if the before/after gap is narrow (say 3/5 → 4/5), run each probe three times before believing it. I kept single runs because the failure you described sounds near-total, and a near-total failure moving to consistent firing is visible above the noise floor. A marginal result deserves the heavier protocol.

**The counter-argument I'd take seriously.** "Just make it user-invoked and type the name." Not unreasonable — it's zero context load and 100% reliable, and for a skill you always know you want, it's strictly better. The reason to keep fixing the description is only this: you want the agent to reach for it at moments *you* didn't recognise as the moment. If, on reflection, you always know when you need it, the honest fix is the flag and your fingers, not better prose.
