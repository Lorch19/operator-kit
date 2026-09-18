# Settings redesign → engineering handoff · Wed 2026-09-16

**Skill:** `[SKILL]` (primary) · `[SKILL]` Phase 2 for the [TARGETS_DOC] draft in Part 3.
Reviewer triggers matched: *"before shipping any user-facing surface, even when nobody asks"* and
*"where should X live"*. Creator is not the right primary here — a redesign already exists; I am not
designing it, I am checking it and packaging it.

**Confidence: LOW-MEDIUM, and the reason matters.** Pass 0 of `[SKILL]` requires a codebase
scan and, if a build exists, rendered frames before code. I have neither: no spec, no mocks, no
routes, no screenshots, no `docs/design/[TARGETS_DOC]`. Per the skill's own rule I am saying so
rather than silently downgrading to vibes. **So this is not a review of your settings redesign.** It
is (a) the handoff package engineering needs, which is answerable without seeing your file, and
(b) the five passes converted into falsifiable checks *you* run against your file — each one names
the countable artifact, the trigger, and the cheaper alternative, so you get a yes/no in minutes,
not an opinion.

---

## The one thing, before anything else

**Thursday is tomorrow.** Today is Wednesday 2026-09-16; Thursday is 2026-09-17. You have roughly
one working day, not a week. Every checklist below is therefore triaged by *what stalls the build*,
not by what would be nice to have. If you actually meant Thursday the 24th, ignore the time budget
and do all three tiers properly — but the ranking still holds.

**If you do only one thing today:** the parity map (Tier 0 #4). A settings redesign's most expensive
and most common failure is not an ugly screen — it is a setting that existed on Monday and exists
nowhere on the new IA, discovered three weeks into the build or, worse, by a customer. Every other
artifact here can be answered in a meeting. That one cannot, and no engineer can invent it for you.

---

## What I would have asked you first (and what I assumed instead)

This runs unattended, so here are the five questions, each with the assumption I proceeded under and
what changes if the assumption is wrong. **Answer Q1 and Q3 before you spend an hour on anything
below** — they are the two that move real work.

| # | Question | Assumption I used | If wrong |
|---|---|---|---|
| Q1 | Is Thursday a **handoff** (they start building Friday) or a **review** (they give feedback)? | Handoff — build starts immediately | If it's a review: bring the contract (Part 3) and the open-questions list only. Skip Tier 1 and 2 entirely; producing them before feedback is waste. |
| Q2 | Does any written success criteria / [TARGETS_DOC] doc exist for this redesign? | No | If one exists, replace Part 3 with it and score against it instead. |
| Q3 | Is this a **re-skin** (same settings, new IA/visuals) or a **scope change** (settings added, merged, removed)? | IA + visual redesign with some consolidation | Pure re-skin → parity map is trivial and the redirect list becomes the top risk. Scope change → parity map is the whole job and Tier 0 #4 needs half your day. |
| Q4 | Do you have telemetry on which settings actually get changed, and how often? | Partial or none | No telemetry means "the top 3 settings" in C2 below is a guess. **That is itself a finding** — see B3. Ask support for their top 5 "where do I change X" tickets as a same-day substitute. |
| Q5 | Has engineering seen anything yet, and who owns the build? | They've seen mocks in passing, have no written contract | If they've been in the design reviews all along, drop the explanatory framing and lead with the open questions. |

---

# Part 1 — The handoff package

Ranked by what happens if it's missing. The failure mode to design against is not "engineering asks
a question" — it's **engineering silently invents an answer at 6pm on Friday**, ships it, and you
discover the decision in staging. Everything in Tier 0 is a decision someone *will* make; the only
question is whether it's you.

### Tier 0 — the build stalls or drifts without it (must be in Thursday's handoff)

| # | Artifact | What engineering invents without it | Est. |
|---|---|---|---|
| 1 | **Screen inventory + state table** — every screen × `loading / saving / saved / save-failed / permission-denied / offline / first-run-empty`. Each cell is "designed", "reuse pattern X", or "deferred — v2". A blank cell is not a state. | They'll build the happy path and bolt on a generic error toast. | 45m |
| 2 | **The save model, in one sentence, plus its exceptions.** Auto-save per control, or explicit Save/Cancel with dirty state? What happens on navigate-away with unsaved changes? | Per-section improvisation — the single most damaging outcome in a settings redesign (see B1). | 15m |
| 3 | **Permission matrix** — setting (or section) × role → `editable / read-only-with-reason / hidden`. Include what a non-permitted user actually sees. | They'll hide everything, and your admins will file bugs saying features disappeared. | 45m |
| 4 | **Parity / migration map** — one row per setting that exists today: `old path → new location \| merged into X \| removed \| renamed`, plus *what happens to the stored value* on migration. | Settings get orphaned in the schema and quietly stop working. Unrecoverable politically once shipped. | 60–90m |
| 5 | **Destructive-action spec** — which actions are destructive, confirm pattern per action (inline confirm / typed confirmation / undo window), and which are genuinely irreversible. | A one-click "Delete workspace" with a native `confirm()`. | 20m |
| 6 | **Settings nav at ≤768px** — one frame. Does the sidebar collapse to a drill-in with back, an accordion, or a select? | Whatever the CSS does by default. This is the #1 thing engineers invent and the #1 thing rejected in review. | 30m |
| 7 | **Redirect list** — every settings URL that moved: `old → new`. Support docs, onboarding emails, and in-product links point at the old ones. | 404s from your own email footers on day one. | 20m |
| 8 | **"What must not change"** — 5–10 lines naming what is load-bearing and why (see Part 4). Cheapest item here and it prevents the most build drift. | They optimize away the thing the redesign was for. | 15m |

**Tier 0 total ≈ 4.5–5 hours.** That is a realistic Wednesday. It is also the honest floor.

### Tier 1 — they'll build it, and build it wrong (Thursday if possible, Friday AM at the latest)

| # | Artifact | Why |
|---|---|---|
| 9 | **Copy deck** — every label, helper text, error message, empty state, button verb, as a *table they can copy-paste*, not text inside mocks. | Copy retyped from a screenshot drifts, and the string in the code becomes the real spec. |
| 10 | **Validation rules per field** — format, required, async uniqueness (slug, domain, email), and what the server error looks like inline. | Async validation is architecture, not polish. Decided late, it forces a rewrite of the form layer. |
| 11 | **Side-effect settings** — which changes trigger work elsewhere (domain change → re-verification, plan change → proration, locale → re-index) and what the UI shows while it's pending. | A toggle that flips instantly but takes 40s to take effect is a support ticket generator. Needs a *status*, not a *state*. |
| 12 | **Component reuse decision** — for each new-looking element: new component, or existing one parameterized? Name the existing one. | This is where a settings redesign quietly forks your form layer into two systems. |
| 13 | **Accessibility spec** — label association, `fieldset`/`legend` for toggle groups, `aria-describedby` on errors, focus target after save, toggle vs. checkbox semantics. | Retrofitting form a11y after the components exist costs 3–5× more than specifying it now. |

### Tier 2 — ship without it, pay later (next week, but assign an owner and a date on Thursday)

| # | Artifact | Why |
|---|---|---|
| 14 | **Telemetry events** — `settings_section_viewed`, `setting_changed(key, from, to)`, `save_failed(reason)`. | Without these the metrics matrix in Part 3 is fiction and you cannot tell whether the redesign worked. Instrument before ship or you lose the baseline permanently. |
| 15 | **Open-questions list with owner + date** — every unresolved decision, named. | An open question without an owner is resolved by whoever hits it first, at the worst possible moment. |

---

# Part 2 — Run this against your own file before you hand off

The five reviewer passes, converted to checks you can run without me. Format is the skill's own:
**Ask · Trigger · Cheaper alternative**, each resolving to a countable artifact. Severity is *if it
trips*. Ranked — B1 and B2 are worth more than the rest combined.

### Catches (Blocker / Major if tripped)

**B1 · Blocker · The save model differs between sections.**
*Count:* distinct save mechanisms across all sections. *Trigger:* more than 1, without a written
rule that says which applies where. *Why it's a Blocker and not a nit:* "one mechanism per behavior"
— if some sections auto-save and others have a Save button, a user cannot tell whether their change
stuck, and the recovery is to re-check every screen. *Cheaper alternative:* one sentence, e.g.
"toggles and selects auto-save with an inline 'Saved' within 1s; multi-field interdependent forms
(billing address, custom domain) use explicit Save/Cancel." One rule, one named exception class,
implemented consistently.

**B2 · Blocker · A setting that exists today appears nowhere in the new spec.**
*Count:* rows in Tier 0 #4 with no destination. *Trigger:* any count above zero. *Cheaper
alternative:* build the map as a literal table before Thursday; "removed" is a perfectly good answer,
but it has to be *written* as a decision with a call on the stored value. Silence here is not
deferral, it's data loss.

**B3 · Blocker · The most-changed settings got deeper.**
*Count:* clicks from app shell to each of the top 3 most-changed settings, old IA vs. new. *Trigger:*
any of the three gaining a level. *Why:* this is the Airbnb "Neighborhoods" failure — a genuinely
better structure that adds friction to the most-travelled path is net-negative. A tidy IA that buries
the one setting everyone touches has optimized for the org chart. *Cheaper alternative:* surface the
top 3 at the settings root (or inline where they take effect) and let the tidy IA hold the long tail.
*If you have no telemetry (Q4), that absence is the finding* — you are reorganizing by intuition.
Support's top 5 "where do I change X" tickets are a same-day proxy.

**B4 · Major · Section labels name system concepts, or there's a dumping ground.**
*Count:* section labels that are bare category nouns; plus any section named General / Advanced /
Misc / Other / Preferences / Configuration. *Trigger:* any dumping-ground section — **Blocker if it
holds more than ~20% of the settings**, because that's the IA admitting it isn't finished. *Cheaper
alternative:* name sections after the job the user came to do ("Billing", "Who has access",
"Notifications"), and redistribute the dumping ground's contents by job. A user says "turn off the
weekly email", never "adjust my preferences".

**B5 · Major · The redesign adds settings and removes none.**
*Count:* settings added vs. removed. *Trigger:* net positive with zero removals — that's a
reorganization wearing a redesign's clothes. *Why:* every toggle is a decision the product declined
to make on the user's behalf, and each one is a permanent branch in state, QA, and support. *Cheaper
alternative:* for each toggle, name the % of users who change it from default. Anything where the
answer is "almost nobody" is a candidate for a smart default and deletion. Ship the deletions *with*
the redesign — a settings redesign is the only politically cheap moment to remove settings, and it
does not come round again for years.

**B6 · Blocker · Permission states are undesigned.**
*Count:* cells in the setting × role matrix with no specified rendering. *Trigger:* any. *Cheaper
alternative:* pick a default rule — read-only-with-a-reason beats hidden, because hidden makes the
feature look broken or absent and generates "where did X go" tickets — then enumerate only the
exceptions to it.

**B7 · Major · Destructive actions share a card and rhythm with routine ones.**
*Count:* destructive controls sitting in the same visual container/spacing as non-destructive ones;
destructive actions with no confirm or undo specified. *Trigger:* any of either. *Cheaper
alternative:* a separate terminal region per section, real spacing between destructive and safe
targets, and match the confirm to the stakes — undo for recoverable, typed confirmation for
irreversible. Never both-at-once on the same action; that just trains people to click through.

**B8 · Blocker · Moved URLs with no redirect, or sections with no stable URL.**
*Count:* settings routes whose path changed and that have no redirect row; sections not addressable
by URL. *Trigger:* any. *Why:* this follows from the cold read in B9 — most settings sessions do not
start at the settings landing page. *Cheaper alternative:* freeze the old paths as permanent
redirects, and make every section deep-linkable before you make it pretty.

**B9 · Major · The design assumes people arrive at the settings home.**
*Cold read, and it's the one that changes settings IA most.* Settings is a low-frequency,
high-intent surface. The realistic user is not a first-timer exploring — they are a 90-day user
arriving from an email footer, a support article, or in-app search, with exactly one thing to change,
who will not browse. *Count:* the top 3 jobs, walked from a *mid-IA entry point* rather than the
landing page. *Trigger:* any of them requires visiting the landing page to orient. *Cheaper
alternative:* every section self-describing (name the job at the top of the section, not only in the
nav), breadcrumbs that work when the nav isn't how you got there, and in-section search if sections
exceed ~7.

**B10 · Major · No frame for settings nav below 768px.**
*Count:* mobile frames in the spec. *Trigger:* zero. *Cheaper alternative:* one frame showing the
drill-in pattern and its back affordance. Thirty minutes now, or a week of rework later.

**B11 · Major · Nothing in the contract can catch "generic admin panel".**
*Count:* criteria in your success criteria that are purely measurable (click depth, contrast, timing).
*Trigger:* all of them. *Why:* a design can pass every measurable criterion and still be rejected on
sight — this has happened twice in this skill's history and it's the reason Part 3 has a C9. Settings
is the surface most likely to drift into an off-the-shelf admin template. *Cheaper alternative:* name
the visual direction in one word and score against it; see C9.

**B12 · Major · A section-level summary hides a per-item exception.**
*Count:* summary strings that roll up a per-item state someone acts on — "Notifications: On" while
one channel is muted; "2 integrations connected" while one is in an error state. *Trigger:* any
aggregate whose erased detail is something a user would act on. *Cheaper alternative:* items with
exceptions get their own line. An aggregate may summarize the normal; it must never hide the
abnormal.

### Minor & polish (compressed — do not let these consume Tier 0 time)

- Toggle labels that name a category ("Notifications") rather than what happens when on ("Email me when someone comments").
- "Enabled / Disabled" text beside a toggle that already shows its own state — the row states the fact twice.
- Helper text living only in a tooltip: invisible on touch, invisible to keyboard.
- Toggle rows under 44px, or destructive and safe targets within a thumb-width of each other.
- Focus destination after save unspecified — focus is lost to `<body>` and screen-reader users lose their place.
- Dates / currency / plurals not locale-formatted in the settings that display them.
- More than ~4 type sizes on one settings screen.
- No settings search while section count exceeds ~7.
- Section headers restating a fact the group already establishes on every row.

### Truncated

**Truncated: none — the 12 Catches above are everything the passes produced that is checkable
without the artifact, and 12 is exactly the cap, so read this as a full list that happens to land
at the ceiling rather than a ranked list that overflowed.** Checks the passes could not run at all
for lack of an artifact are listed under Part 5, not here — an unrun check is not a truncated
finding, and collapsing the two would let "I couldn't look" read as "I looked and found nothing."

---

# Part 3 — Provisional [TARGETS_DOC]

Paste into `docs/design/[TARGETS_DOC]`, correct the guesses, get it approved Thursday. **This is
the artifact that makes the rest of the handoff reviewable** — without it, "is the build right?" has
no answer but taste, and taste arrives after the code. Ten minutes of your attention on the numbers
below is worth more than an hour of polish on the mocks.

```markdown
# [TARGETS_DOC]: Settings Redesign

**Status:** PROVISIONAL — drafted by [SKILL] 2026-09-16, NOT approved.
Omri: correct the bracketed guesses, then mark approved.
**Domain brief:** none — not written for this surface.

## Targets

1. A user who arrives with one thing to change completes it and leaves, without
   browsing. Settings is a destination people pass through, not one they explore.
2. Must love this: the 90-day admin arriving from a support article or an email
   footer — not a first-time user, and not us.
3. The feeling: "that was where I expected it." Settings should be forgettable.
4. Constraints: [platform] · handoff to engineering 2026-09-17 · WCAG 2.1 AA floor ·
   no backend config-schema changes in v1.

## Experience thesis

Settings is the product's index, not its dashboard. Its job is to be predictable
enough that people find things by guessing, and honest enough that they trust a
change took effect. Success is a short visit; there is no engagement goal here.

## Success criteria

| # | Criterion | How the reviewer verifies it |
|---|---|---|
| C1 | A user arriving from a deep link completes their change without visiting the settings landing page. | Cold read of the top 3 jobs, each started mid-IA. |
| C2 | The 3 most-changed settings are ≤2 clicks from the app shell, and no deeper than today. | Click count, old vs. new, per setting. |
| C3 | One save model. A user can tell whether a change saved, without being told how the screen works. | Count distinct save mechanisms (target: 1 + named exception class); every control confirms within 1s. |
| C4 | Every setting that exists today lands somewhere, or is removed as a written decision including its stored value. | Parity map, zero unaccounted rows. |
| C5 | A permission-limited user sees why, never a blank or a dead end. | Role matrix has no unspecified cells; viewer-role walkthrough. |
| C6 | No section named General / Advanced / Misc; every label names a job a user would say aloud. | Read the labels aloud; count bare category nouns. |
| C7 | Destructive actions are spatially separated and each is undoable or typed-confirmed. | Count destructive controls sharing a container with routine ones (target: 0). |
| C8 | Sad paths designed per section: loading, saving, saved, save-failed, permission-denied, offline, first-run. | State table, zero blank cells. |
| C9 | **Settings reads as [our product], not as a generic admin panel.** | Crop the logo out of 3 settings screens; can a daily user name the product? Plus: on each section the primary control group dominates by both area and contrast — area alone is not salience. |
| C10 | AA floor: 4.5:1 text measured against the surface the text actually sits on (not the page background), 44px targets, labels programmatically associated, errors announced. | Measure per screen; check the baseline, not just the ratio. |

C9 is the criterion the measurable ones cannot fake. Do not drop it because it is the
soft-looking one — it is the only line here that catches a design which passes
everything and still gets rejected on sight.

## Metrics matrix

| Metric | Type | Target | Measured by | Review proxy (pre-launch) |
|---|---|---|---|---|
| Task success, top 3 jobs | Task | ≥95%, no dead ends | funnel + session replay | cold-read walkthrough |
| Time to change the most-changed setting | Task | ≤ today's median | `setting_changed` deltas | click count vs. old IA |
| Silent save failures | Trust | 0 | `save_failed` events vs. error impressions | state table review |
| "Where do I change X" support tickets | Adoption | ↓ vs. 30-day pre-launch baseline | support tagging | labels read-aloud test |
| Net settings count | Engagement | ≤ today | spec count | added vs. removed in spec |
| Deep-link integrity | Task | 0 404s from docs/emails | redirect monitor | redirect table completeness |

**Capture the pre-launch baseline before Thursday** for the last three rows. Post-launch
you cannot recover it, and every one of these metrics is a delta.

## Anti-goals

- Not changing the underlying config schema in v1.
- Not adding settings search in v1 if sections stay ≤7.
- Not optimizing settings for engagement or time-on-page — a shorter visit is a better one.
- Not personalizing or auto-reordering settings per user.

## Open questions

Q1–Q5 from the handoff review, 2026-09-16. Each needs an owner and a date on Thursday.
```

---

# Part 4 — "What must not change" (you write this; here's why and how)

The reviewer's output format has a `What must not change` section, and I can't fill it in — I haven't
seen your design, so I don't know what's load-bearing. **But this is the highest-value 15 minutes in
the whole handoff**, so here's the template and the reason.

During a build, engineers hit friction and make locally-sensible calls: this animation is expensive,
this grouping is awkward in the component model, this empty state needs a spinner instead. Most of
those are fine. One or two of them are the *reason the redesign exists*, and nobody told them.

Write 5–10 lines, each in this shape:

> **[Element / behavior] must stay [how].** It exists because [the specific problem it solves]. If
> it's expensive, come back to me — do not substitute.

Plausible examples for a settings redesign, to be replaced with yours:

- **Every control confirms its own save within 1s.** It exists because the old settings gave no
  feedback and people re-clicked and re-checked. If optimistic UI is hard, we change the save model
  deliberately — we do not drop the confirmation.
- **Destructive actions stay in their own region.** It exists to make an accidental workspace
  deletion structurally unlikely, not just confirmed.
- **Section names stay in user language.** If a name reads oddly against the config keys, the code
  can map — the label does not change to match the schema.

That last one is the whole point. The failure this skill exists to catch is the data model quietly
dictating the interface, and the handoff is exactly when it happens.

---

# Part 5 — Unverifiable without the artifact

Checks the passes could not run. Each is 5–20 minutes for you, with the artifact in front of you.

1. **Pass 0 — nearest existing surface.** Which existing form/shell does the new settings page most
   resemble? If the answer is "it's a new shell that looks 90% like our existing form layout," that's
   a reuse-vs-clone Blocker and the cheaper alternative is parameterizing the existing one.
2. **Pass 2 — judge the set, not the frame.** I could not see a single screen, let alone the run of
   them. Put the sections side by side in the order someone actually moves through them and check
   whether the register holds. Half-converted loops pass screen-by-screen and fail on sight.
3. **Pass 4 — treatment coverage split, UNRUN.** The rule is: the treatment covering the most screens
   must carry the most energy, and *the count gets stated even when it passes* — an unstated count is
   an unrun check, so I am stating plainly that I could not run it. Do the count yourself: list every
   settings screen, group by how they look, write the split (e.g. "9 of 12 are the plain list
   treatment, 3 are the card treatment"). Flag if the largest group is the flattest. Settings is
   allowed to be utilitarian — but that should be a decision you wrote down, not the default that
   happened.
4. **Pass 4 — squint test per section.** What pops? Is it the primary control for that section's job,
   or the section header / the destructive button / an illustration?
5. **Pass 5 — contrast against the real surface.** Measure text against the panel it actually sits on,
   not the page background. Two defects have shipped past green tests in this skill's history from
   exactly that wrong baseline (real ratio 4.07:1 while the test asserted against the page ground).
6. **Pass 1 — full criteria scorecard.** C1–C10 above can only be scored with the artifact. Score
   them yourself Thursday morning; anything that isn't a clear pass is a "risk", not a pass.
7. **B3's click counts.** Needs both the old and new IA in front of you. This is the single most
   valuable number in the whole review and it takes ten minutes.

---

# Stress Test

**Weakest thing here:** I have not seen the design. Part 2 is a well-aimed checklist, not a review,
and I've labelled it as such — but a checklist derived from what settings redesigns *usually* get
wrong will miss what *yours* gets wrong. If your redesign's real problem is something idiosyncratic,
nothing above finds it. The only fix is running `[SKILL]` properly against the actual file, in a
fresh context, with the screens rendered.

**Assumption most likely to be wrong:** that Thursday is a build handoff rather than a feedback
meeting (Q1). If it's a feedback meeting, most of Tier 1 is premature and I've sent you to spend
hours on artifacts that may be invalidated in the room. Check that first.

**Second most likely:** that the parity map doesn't already exist. If it does — and it plausibly does
if you've been at this a while — then B2 and Tier 0 #4 are noise, and your real top risk moves to B1
(save model) and B3 (click depth), neither of which most teams have written down.

**What a smart critic would say:** "You gave a PM a 30-item checklist the day before a handoff. Most
of it won't get done, and the effect is guilt, not quality." Fair — which is why Tier 0 is capped at
~5 hours, why it's ordered by cost of omission rather than by category, and why there's a single
named "if you do one thing" item at the top. If you get the parity map, the save-model sentence, and
the state table into Thursday's packet and nothing else, the handoff is materially better than most.

**The honest counter-argument to my own B5:** telling a team to *remove* settings the day before a
handoff is scope creep from the reviewer. I'm keeping it because a settings redesign is the only
cheap political window for deletion and it doesn't recur for years — but if your Thursday is already
tight, B5 becomes a list you bring to the meeting, not work you do tonight.

**What would change my mind about the whole framing:** if engineering has been embedded in the design
process all along. Then the handoff isn't an information transfer and most of this is ceremony; the
only items that still earn their place are the parity map, the redirect list, and "what must not
change" — the three things that live in your head and nowhere else no matter how many reviews they
attended.
