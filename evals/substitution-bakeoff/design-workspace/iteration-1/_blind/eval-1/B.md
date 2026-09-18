# UX Review: Onboarding flow (signup → preferences → dashboard) — 2026-09-16

**Skill:** `[SKILL]` (five passes, run in order). Not `[SKILL]` — this is an existing design.

**Against:** `docs/design/[TARGETS_DOC]` — **does not exist**. Drafted PROVISIONAL targets below (§7) and scored against them, per the skill's Inputs rule. Those targets are mine, not yours; confirm or overwrite them before treating any score as a verdict.

**Verdict: rethink the middle screen — fix-then-ship the other two.** Advisory. You decide.

**Confidence: LOW, and here is exactly why.** Pass 0 could not run. There is no codebase to scan, no build to render, and no frames to measure. Per this skill's own precondition — *"If a build exists, render it and read the frames before the code"* — a prose review of a renderable screen is a weak review. I saw **zero of three screens**. That limit is itself the largest finding in this review, and it is the one this checklist has historically missed most. Every finding below that would need pixels to confirm is tagged **[needs build]**. Findings without that tag are structural — they follow from the *order and count* of the screens you described, and pixels cannot rescue them.

---

## 1. The headline

You said it feels heavy but you can't name it. Here is the name:

> **The flow asks twice and pays once — and on day 0, the one payoff is empty.**

Weight in an onboarding flow is not screen count. It is the **ratio of asks to payoffs**, and the **position of the first payoff**. Yours reads:

| Screen | What it asks of the user | What it gives back |
|---|---|---|
| 1 · Email signup | Email, password, (likely) verification | Nothing yet |
| 2 · Preferences | N decisions about a product they have not seen | Nothing yet |
| 3 · Dashboard | — | A dashboard with no data in it |

Two tolls, zero payoffs, then a terminal screen whose entire job is to display data the user has not created yet. Three screens is a perfectly normal length. **2:0 is not.** A four-screen flow where screen 2 shows the user something real feels lighter than this three-screen one, which is why counting screens never located the problem.

**Vocabulary, so you can say it next time.** "Heavy" decomposes into five things. Yours is almost certainly (a) and (d):

| | Dimension | Countable as | Your flow |
|---|---|---|---|
| a | **Toll count** | Required asks before first value | 2 (target: ≤1) |
| b | **Decision load** | Choices whose consequence is not visible when made | All of screen 2, by construction |
| c | **Commitment asymmetry** | What you hand over before you know it's worth it | Account + preferences, before any value |
| d | **Terminal payoff** | True user-specific facts on the last screen | Likely 0 on day 0 |
| e | **Visual density** | Ink, contrast, elements per screen | Unmeasurable — no frames |

Note that (e) — the thing "heavy" sounds like it means — is the one I cannot check and the one least likely to be the cause. If you shipped this and users drop off, they will drop at screen 2, not because it's ugly.

---

## 2. Pass 0 — Codebase-aware prep

- **Nearest existing surface for screen 2:** your **Settings** screen. Screen 2 is almost certainly a first-run rendering of fields that already have a permanent home. *Unconfirmed — I could not open either.* The one check that settles it is in §5.
- **Routes:** unknown. You said three screens. I do not believe the real number is three — see M1.
- **Data model:** unknown.

No codebase access → review runs on the artifact text alone, marked lower-confidence. Not silently downgraded to vibes: every finding below still names a countable artifact you can go count.

---

## 3. Pass 2 — Cold read (evidence for the Catches)

First-time user, top job: *"do the thing I came here to do."* First person, no designer knowledge.

> **Screen 1.** A form. Email, password. I haven't seen the product. I'm deciding whether it's worth an account based on a landing page and a hunch. *(Stall: low, this is a normal price of entry — but I'm paying it before I know the price is fair.)*
>
> I submit. **→ Check your email.** I leave the app. I'm in my mail client now. There's other mail in there. *(Stall: high. This is where I go do something else. **This screen was not in your list of three.**)*
>
> I come back. **Screen 2. Preferences.** I'm being asked to choose things. I don't know what any of these do to the product, because I haven't seen the product. I can't answer these questions — I can only guess. *(Stall: high. Two responses available to me: pick defaults blindly and feel like I did it wrong, or actually think about it and resent the flow. Both are weight.)*
>
> Is there a Skip? Can I change these later? Nothing tells me. So I assume they're permanent and I slow down. *(This is the single cheapest thing on this list to fix.)*
>
> I submit. **→ Screen 3. Dashboard.** Cards. Charts. Empty. Zeros and dashes where numbers go. *(Stall: terminal. I just paid twice and this is the receipt. I don't know what to do next — there are eight things on this screen and none of them is obviously first.)*

**Day-2 return read:** I open the app. Same empty dashboard. Nothing has changed, because nothing happened. There is no reason for me to have come back and no reason to stay. *(This is the shape of a retention problem that gets misdiagnosed as an onboarding-copy problem.)*

**Screens I did not see: all three.** Plus the verification interstitial I believe exists, plus whatever renders on a failed signup. Stated per the "judge the set, not the frame" rule — an unstated limit is an unrun check.

---

## 4. Criteria scorecard (Pass 1, against PROVISIONAL targets in §7)

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| C1 | First value within ≤2 screens | **fail** | First candidate value is screen 3; on a new account it renders no user data, so real first value is later than screen 3 |
| C2 | ≤1 required ask before first value | **fail** | Two: signup, then preferences |
| C3 | Every onboarding choice is reversible, and visibly so | **unverifiable** | Needs screen 2's copy. If there is no "change this later" line, this auto-fails |
| C4 | Zero choices whose consequence is invisible when made | **fail** (structural) | Screen 2 precedes screen 3 by construction. Every preference is a prediction about a screen not yet seen |
| C5 | Last onboarding screen renders ≥1 true, user-specific fact | **risk** | A dashboard on a zero-data account is a zero-state. **[needs build]** |
| C6 | Abandonment is resumable with nothing re-entered | **unverifiable** | Depends on when the account record is written. See M3 |
| C7 | Accessibility floor (contrast, 44px, focus order, no color-only) | **unverifiable** | **[needs build]** — cannot be judged from prose, and asserting otherwise is how the 4.07:1 defect shipped past a green test |
| C8 | Reads as one named visual direction; highest-coverage treatment carries the most energy | **fail** | No direction is named anywhere. Treatment split below |
| C9 | The real screen count equals the count the team believes it has | **risk** | You said three. I count 4–6. See M1 |

**Visual-treatment coverage split — stated even though it can't be confirmed, because an unstated count is an unrun check.** From the description, the three screens group into two treatments: **2 of 3 are form treatment** (signup, preferences), **1 of 3 is data/dashboard treatment**. The treatment covering the majority of the flow is the flattest, most utilitarian one. That is the exact pattern flagged in `review-passes.md` — and per `[LESSONS_DOC]`, the fix is to **move energy into the high-coverage treatment, not to add a fourth screen**. Do not respond to this by adding a welcome splash. Make the signup screen itself the one with a point of view.

> Word-collision guard observed: "heavy" here is your verdict on how the flow *feels to move through*, not a claim about visual density. I ran the treatment count anyway, mechanically, as the checklist requires.

---

## 5. Catches

**9 findings (3 Blocker, 6 Major) against the ~12 cap. Under the cap — nothing was cut to fit.** Ranked; lead finding first.

---

### B1 · Blocker — The preferences step is a *mode*, not a screen. Scope gate: 4 of 5.

**Countable artifact:** one route in the onboarding stack whose fields also exist on your Settings screen.

**Scope gate, scored against Settings as the nearest existing surface:**

| | Question | |
|---|---|---|
| 1 | Is it a variation of existing UI, not a genuinely separate object? | **yes** — these are settings, shown early |
| 2 | Does it duplicate ≥~70% of an existing flow? | **yes** — same fields, same controls, same writes |
| 3 | Does it add vocabulary the user wouldn't use unprompted? | **yes** — nobody says "I'm going to do my preferences" |
| 4 | Could a mode/toggle/default on an existing surface achieve the same outcome? | **yes** — ship defaults, expose each control where its effect renders |
| 5 | Does it split one job across two places? | **yes** — set here, manage in Settings, forever |

**3+ → Blocker.** This is the canonical catch this reviewer exists for, in its onboarding costume: *"recurring orders" became a table → screen → form → nav tab when a toggle was the whole feature.* Here, "let the user configure things" became a step in the critical path when **a set of defaults** was the whole feature.

**Cheaper alternative:** Delete the screen. Ship a defaulted state for every preference. Move each control to the point on the dashboard where its consequence is visible, with an inline affordance. For any preference that genuinely cannot be defaulted, ask it **at the moment it first matters** — the first time the user hits the thing it configures — not up front. Expected result: −1 screen, −N blind decisions, and every surviving choice gets made with its consequence on screen.

**The one condition under which B1 is wrong — read this before acting.** If screen 2's answers *materially change what screen 3 renders*, and the dashboard would be meaningless without them, then it is **not a preferences step — it is a seeding step**, and it earns its place. The fix then is the opposite of deletion: rename it in the user's language, and **show the dashboard assembling live as they choose**, so the step pays out while it asks. A seeding step that shows its work is one of the lightest-feeling patterns there is. A preferences step that doesn't is one of the heaviest. *Which one you have is the single highest-value thing to determine, and it takes 60 seconds — see the check below.*

**The 60-second check:** open Settings and screen 2 side by side and count overlapping fields. **≥70% overlap → it's a preferences step → delete it.** **<70%, and the non-overlapping fields visibly change the dashboard → it's a seeding step → keep and reframe it.**

---

### B2 · Blocker — Two tolls before any payoff. This is the heaviness.

**Countable artifact:** screens before the first screen rendering user-specific content = **3** (4+ with verification). Required fields before that point ≈ 2 + N preferences.

**Evidence:** the table in §1. Nothing in screens 1 or 2 returns anything to the user.

**Cheaper alternative — invert one toll.** Pick whichever is true of your product:

- **If the product can do anything useful without an account:** let them do the job first. Ask for the email at the moment the account becomes structurally necessary — save, sync, invite, share, export. The ask stops being a toll and becomes a consequence of something they wanted. This is the largest available win and it removes weight rather than relocating it.
- **If the product genuinely cannot function without an account** (multi-device, team data, billing at the door): keep signup first — that's legitimate, see §8 — but then **screen 2 must go** (B1) and **screen 3 must not be a dashboard** (M4). One toll, one payoff.

**Do not fix this by merging three screens into one long scroll.** That relocates the weight into a taller form; it does not remove it. The screen count is a symptom.

---

### B3 · Blocker — Nothing in this flow is designed to produce a feeling, which is why "heavy" has no address.

**Countable artifact:** the number of named visual directions in the design contract: **zero**. There is no `[TARGETS_DOC]`, and even the provisional one I wrote is 8 measurable criteria and 1 that isn't.

**Evidence:** you asked a *feeling* question ("feels heavy") about an artifact defined entirely by structure (three nouns and an order). A contract made only of behavioural criteria — comprehension, timing, thumb zones — can be satisfied in full by a design that is then rejected on sight. In this reviewer's own calibration log that has happened twice, and it is the only confirmed miss on record: a design passed 9 of 9 findings and was rejected on the built app with the verdict *"no point of view."*

**Cheaper alternative:** before touching the screens, name the direction in the product's own language and write it into the contract as criterion C8 — *"does this screen read as [name]?"* Then make the **form treatment** carry it, because that is 2 of your 3 screens. Concretely: the signup screen is the most-seen screen in this flow and is currently, by default, the flattest thing in the product. It is the only screen every single user sees. Treat it as the product's opening statement rather than a gate.

---

### M1 · Major — The flow is not three screens, and that is the weight you couldn't count.

**Countable artifact:** routes in the onboarding stack. You named 3. Email+password signup almost always implies: `check your email` → *app exit to mail client* → `verification landing` → sometimes `welcome`. **Real count: 4–6**, at least one of which is outside your app entirely.

**Evidence:** the cold read in §3 — the highest-stall moment in the entire walkthrough is a screen that was not in your list. Uncounted screens are the most common source of heaviness a team can't locate, precisely because the team's mental model of the flow doesn't contain them.

**Cheaper alternative:** collapse verification into the same step — magic link or OAuth — or defer it entirely until it's load-bearing (verify on first share/invite/export). If neither is possible, at minimum count it, design it, and measure drop-off across it as its own step.

---

### M2 · Major — Every choice on screen 2 is made blind, by construction.

**Countable artifact:** number of controls on screen 2 whose effect is not visible on screen 2. Given its position in the flow, this is **all of them**.

**Evidence:** Pass 4, recognition over recall — inverted. You are not asking the user to recall something from another screen; you are asking them to **predict** a screen they have never seen. That is strictly harder than recall, and it is the reason a 6-field preferences step feels heavier than a 12-field checkout.

> *"If you need to explain how to use a feature, you're in a failure state."* — via Lenny's Newsletter (K. Rudin). The corollary: if a choice needs the user to imagine its result, it's in the wrong place in the flow.

**Cheaper alternative:** if the step survives B1, render the consequence live beside the controls — a real preview that changes as they choose. If it can't be previewed, it can't be chosen well here, and it belongs at point-of-need.

---

### M3 · Major — No visible reversibility signal, and probably no Skip.

**Countable artifact:** presence/absence of (a) a Skip affordance on screen 2, (b) one line of copy saying these are changeable later. Neither appears in your description.

**Evidence:** people slow down on choices they believe are permanent. The perceived cost of a decision is what generates weight, not the actual cost — and silence about reversibility is read as permanence. This is the **cheapest fix on the entire list**: two elements, no architecture change.

**Cheaper alternative:** add both today, independent of whether you act on B1. Then instrument the Skip. **The skip rate is the measurement that settles B1 for you** — if most users skip, the step was never earning its place and you have your evidence rather than my inference.

---

### M4 · Major — The day-0 dashboard is a zero-state wearing a dashboard's clothes, and it offers N next actions when the user needs exactly one.

**Countable artifact:** (a) cards/widgets on the dashboard rendering a zero, dash, or "No data yet" for an account created 10 seconds ago; (b) distinct actionable elements competing for the first click. **[needs build — one screenshot of a brand-new account settles both]**

**Evidence:** a dashboard's job is to summarise accumulated state. A new user has none. The flow's terminal reward is therefore a grid of empty containers — and Pass 4's competing-primary-task check fires: the one thing a new user must do is buried among the N things an established user does.

**Cheaper alternative:** for the first session only, the dashboard renders **one** primary action at full width and holds the rest back until there's data to fill them. Not a modal tour, not coachmarks — the same surface, composed for the state it's actually in. Per `[LESSONS_DOC]`, this needs to be an output of the record (does this user have data?), not a copy variant on a fixed template: **rank the blocks by a claim computed from the data and drop everything under a floor.** Ranking alone only reorders the same empty cards.

---

### M5 · Major — Abandonment cost is unknown and probably total.

**Countable artifact:** the resume point for a user who quits on screen 2 and returns tomorrow. Do they land on screen 2, or screen 1? Is the account record written at screen 1's submit, or only at the end of screen 3?

**Evidence:** not described. If the account is only written at the end, the flow is all-or-nothing — which is the maximum possible weight, because every step carries the risk of losing every previous step. Users can feel this even when they can't articulate it.

**Cheaper alternative:** write the account at screen 1 submit; resume at the furthest screen reached; never re-ask a field already answered.

---

### M6 · Major — State coverage is silent across all three screens.

**Countable artifact:** 3 screens × 5 states (empty / loading / error / offline / first-run) = **15 cells. Zero named.** Silence is a finding, not a default.

**Evidence:** your description names no error or edge state. The four that actually occur in this flow and reliably get missed: **email already registered** (the single most common signup error, and the one most often handled as a generic red banner), **expired or already-used verification link**, **offline mid-signup after the password was typed**, and **slow dashboard first-load** (a spinner where a zero-state belongs reads as broken).

**Cheaper alternative:** design those four. Explicitly defer the other 11 in writing, so deferral is a decision rather than an omission.

---

## 6. Minor & polish

Compressed, one line each. These do not consume the Catches budget and none of them is your heaviness.

- "Preferences" is system vocabulary — nobody says it out loud. Mental-model mismatch (Lens B).
- Password rules revealed only on submit → error *explained* where it could be error *prevented*.
- "Continue" / "Next" name the sequence, not the outcome — and the same word appears twice for two different results.
- "Dashboard" as a nav label is a system word; "Home" is what people say. **[needs build]**
- A Skip styled as a ghost link beside a saturated primary reads as a penalty for skipping. **[needs build]**
- Signup's sparsest state: two fields on an 844px viewport pools all slack into one band. Split the slack (~3:1 held the thumb zone in a prior project), don't pool it; put the field block on a real surface so it reads as placed rather than floating. **[needs build]**
- Back from screen 2 → screen 1: does it exist, and does it drop typed input?
- Email field: `type=email`, `autocomplete`, correct mobile keyboard, password-manager compatibility.
- Dashboard first render: locale-correct dates, currency, plurals — including the zero case ("0 items", not "0 item").
- Focus order after browser autofill on screen 1. **[needs build]**

---

## 7. Truncated

**Truncated: none — everything the passes produced is listed above.**

Catches: **9 (3 Blocker, 6 Major) against the ~12 cap.** Under the cap; nothing was dropped to fit. One merge for honesty: a separate finding about the progress indicator ("Step 2 of 3" advertises the toll count; but its absence on a 3-step form is also a defect — the real finding is that the flow is long enough to need one) was folded into **B2** rather than listed separately. That is a merge, not a cut.

Minor & Polish: 10, uncapped, all listed.

---

## 8. What must not change

Protecting these from a well-meant fix:

1. **Signup-first is legitimate if the product is genuinely account-bound.** Multi-device, team data, or anything with real persistence — don't bolt on a guest mode to satisfy B2. Take the other branch of B2's counter-proposal instead.
2. **Three screens is not the problem.** Do not merge them into one long scroll. Weight comes from the ask:payoff ratio, not the screen count — a long form is the same weight with worse orientation.
3. **If screen 2 is genuinely a seeding step, keep it.** Do not delete a step that makes screen 3 possible because a reviewer called it a preferences step. Run the 60-second check in B1 first.
4. **Landing on the real product surface is right.** Do not "fix" the empty dashboard with a product tour, a modal carousel, or coachmarks. That adds tolls on top of tolls and is the most common wrong answer to M4.

---

## 9. Unverifiable from this artifact

What I could not judge, and precisely what would settle it:

| Open | What settles it |
|---|---|
| C3 (reversibility), C6 (resumability) | Screen 2's copy; where the account record is written |
| C5 (terminal payoff), C7 (accessibility floor), all density/hierarchy/contrast findings | **Three frames at a real viewport (e.g. 390×844) with real day-0 content.** Wait out transitions before capturing — a screenshot fired mid-animation lies about colour. Measure contrast against the surface the text *actually* sits on, not the page ground |
| The true screen count (M1) | The router / route list |
| Preferences ↔ Settings overlap (B1) | The two field lists side by side — the 60-second check |
| Whether the dashboard is a zero-state (M4) | One screenshot of an account created 10 seconds ago |
| Whether any of this is *the* heaviness | **Per-screen funnel drop-off.** One telemetry chart would replace this entire review. My prediction, recorded so it can be scored: **the largest single drop is at screen 2 or at the verification exit, not at signup.** If it's at signup, everything above is mis-aimed and the problem is upstream of this flow — positioning, not onboarding |

---

## 10. Questions I would have asked

This ran unattended, so these are written down rather than asked. **Q1 is the one that changes the most.**

1. **Is screen 2 required, or skippable?** If skippable with a visible Skip, **B1 drops Blocker → Major**.
2. **Do screen 2's answers change what screen 3 renders?** If yes, it's a seeding step, and B1's counter-proposal inverts from *delete* to *keep and show it assembling*.
3. **What does the dashboard show for an account created 10 seconds ago?** If it's genuinely populated (templates, samples, team data already there), **M4 and C5 drop entirely** and B2 weakens substantially.
4. **Is there a verification step?** If it's a magic link or OAuth with no app exit, **M1 drops**.
5. **Can the product do anything useful without an account?** This selects which branch of B2 applies.
6. **Web or native, and what viewport?** Gates every `[needs build]` item.

**Assumptions I proceeded under** — each is a place this review can be wrong, and each is cheap for you to falsify:

- **A1** Consumer-or-prosumer SaaS; the dashboard is the recurring home surface.
- **A2** "Email signup" means email + password with a verification step (→ M1).
- **A3** Screen 2 is required and not obviously skippable (→ B1 severity).
- **A4** A Settings surface exists or is planned (→ B1's duplication argument).
- **A5** The day-0 dashboard has no user data in it (→ B2, M4, C5).

If **A3 and A5 are both false**, this review's top three findings collapse and the heaviness is somewhere I cannot see without frames — most likely density on screen 3.

---

## 11. PROVISIONAL [TARGETS_DOC]

Save to `docs/design/[TARGETS_DOC]`. **Marked PROVISIONAL — I invented these; targets are supposed to be elicited from you, not generated.** Overwrite them, then the scorecard in §4 means something.

```markdown
# [TARGETS_DOC]: Onboarding (signup → first value)

**Status:** PROVISIONAL — drafted by [SKILL] 2026-09-16, NOT approved
**Domain brief:** none

## Targets (to be set with the user — placeholders below)
1. A new user reaches something that is theirs, and useful, in one sitting.
2. Who must love this: the user who signed up on a hunch and has not yet
   decided this product is worth their time.
3. The one feeling: momentum. Nothing in the flow should feel like paperwork.
4. Constraints: [platform, accessibility floor, auth requirements — TBD]

## Experience thesis
Onboarding is not a gate the user passes; it is the first thing the product
does for them. Every step either returns something or is deleted.

## Success criteria
| # | Criterion | How the reviewer verifies it |
|---|---|---|
| C1 | First value within <=2 screens and <=60s | timed cold-read walkthrough |
| C2 | <=1 required ask before first value | count the asks |
| C3 | Every onboarding choice reversible, and visibly so | read the copy; find the words |
| C4 | Zero choices whose consequence is invisible when made | per-control audit of screen 2 |
| C5 | Last onboarding screen renders >=1 true user-specific fact | screenshot, 10-second-old account |
| C6 | Abandon at any step, resume with nothing re-entered | walk it |
| C7 | Contrast >=4.5:1 on the actual backing surface; targets >=44px;
       focus order matches visual order; no color-only signals | measured on frames |
| C8 | The flow reads as [DIRECTION — not yet named], and the treatment
       covering the most screens carries the most energy | screens-per-treatment split |
| C9 | The real screen count equals the count the team believes it has | route list vs. the team's answer |

C8 is the criterion the measurable ones can't fake. It is currently unfillable
because no visual direction has ever been locked — which is finding B3.

## Metrics matrix
| Metric | Type | Target | Measured by | Review proxy (pre-launch) |
|---|---|---|---|---|
| Signup -> first value completion | Task | [TBD] | per-screen funnel | cold-read stall count |
| Largest single-step drop | Task | no step >[TBD]% | funnel | which screen the cold read stalls hardest on |
| Screen-2 skip rate | Adoption | measured, not targeted | event | does the step earn its place? |
| D1 return | Retention | [TBD] | analytics | day-2 return read: is there a reason to come back? |

## Anti-goals
- Not optimizing signup conversion at the cost of day-2 return.
- Not adding a product tour, modal carousel, or coachmarks to compensate
  for a flow that returns nothing.

## Open questions
Q1-Q6 in the review, section 10. Q1 (is screen 2 required?) blocks the
severity of the lead finding.
```

---

## 12. Do this in order

1. **Run B1's 60-second check** — field overlap between screen 2 and Settings. It decides whether you delete a screen or reframe it, and it is free.
2. **Ship M3 today** — a Skip and one line of reversibility copy on screen 2. Two elements, no architecture, and the skip rate becomes the evidence that settles B1 without argument.
3. **Screenshot a 10-second-old account's dashboard.** Confirms or kills M4, C5, and half of B2.
4. **Count the real routes** (M1). If there's an app exit for verification, that's your uncounted weight.
5. **Only then** touch the flow's shape. B2's fix depends on the answers to 1, 3, and 4.

---

## Stress Test

**What's weakest here.** I reviewed a sentence, not a design. Three nouns and an ordering is the thinnest possible artifact, and this skill's own calibration log records a 50% run-to-run noise floor on *rich* artifacts. Treat the ranked list as a differential diagnosis with checks attached — which is why every finding above ships with the one measurement that kills it — not as a verdict.

**Which assumption is doing the most work.** A5, that the day-0 dashboard is empty. It is load-bearing for B2, M4, and C5 — three of my nine Catches. I believe it because a dashboard by definition summarises accumulated state and a new account has none, but products that seed templates or land users into existing team data break this completely. One screenshot decides it.

**What a smart critic would say.** *"You diagnosed a preferences step you've never seen, using a lens tuned on a kitchen app's recurring orders."* Fair. The scope gate scored 4/5 on inference, not inspection — questions 1, 2 and 5 all assume a Settings screen I never opened. If your screen 2 is genuinely a seeding step, B1's premise is wrong and I built the top of the review on it. I flagged that fork explicitly rather than burying it, but a reader skimming for the headline will act on "delete the screen" and may delete the wrong thing.

**Where the review is structurally blind.** If "heavy" turns out to be *visual* — density, contrast, type weight, cramped spacing on screen 3 — nothing above touches it, because I have no frames. I ranked visual density last (dimension (e) in §1) on the reasoning that flow-shape problems produce inarticulate heaviness while visual problems usually produce articulate ones ("it's cluttered", "it's cramped"). Your inability to name it is itself my main evidence for a structural cause. That's an inference from *how you phrased the question*, which is weaker evidence than I'd like to be leaning on.

**The honest counterfactual.** One per-screen funnel chart would outperform this entire review. If the drop is at signup rather than screen 2, the problem is upstream of onboarding — positioning, not flow — and none of these nine findings matters.
