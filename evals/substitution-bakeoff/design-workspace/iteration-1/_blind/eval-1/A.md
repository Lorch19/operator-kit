# Design Critique: Onboarding Flow (Signup → Preferences → Dashboard)

**Skills run:** `[SKILL]` (primary), `[SKILL]` (secondary, for the copy rewrites in §6).
**Skills deliberately not run:** `[SKILL]`, `[SKILL]` — see §9 for why.

---

## 0. Read this first: what I can and cannot claim

I have no screenshots, no Figma, no code. Everything below is reasoned from your description of the flow's **shape** — three screens, email signup, preferences, dashboard — plus the symptom you reported ("feels heavy").

So I have adapted the critique template in one important way. The skill's output format has a **Findings** table, which implies observation. I have not observed anything. Every row is therefore a **candidate diagnosis** with a **prior** (how often this is the culprit in a flow shaped like yours) and a **10-minute test you can run yourself**. Run the tests; the ones that come back positive are your findings. Do not treat any row as a verified defect until you've run its test.

Where I write example "before" copy, it is a **reconstruction of the common pattern**, not a quote from your product. I've marked those clearly.

### Questions I'd normally ask, and what I'm assuming instead

Since this runs unattended, here are the five answers that would actually change my recommendation, and the assumption I'm proceeding under for each.

| # | Question | Assumption I'm using | What changes if I'm wrong |
|---|---|---|---|
| 1 | What does the preferences step collect, and what share of users change the default? | Mostly-defaulted settings; low change rate | If it feeds personalization the dashboard depends on, don't delete it — **defer** it (§4, D2b) |
| 2 | Does the dashboard show real content on first load, or a zero-state? | Zero-state or near-zero | If it's genuinely full and useful on load, the weight is front-loaded only and §3-D5 drops off the list |
| 3 | Is "heavy" from drop-off data, or from your own walkthrough? | Your own felt sense, no funnel data cited | With real per-screen drop-off, you'd skip my whole differential and go straight to the screen that bleeds |
| 4 | Is there any path to see the product before the account wall? | No — signup is screen one, mandatory | If a demo/guest path is feasible, D1 becomes the single highest-leverage fix |
| 5 | B2C/PLG self-serve, or B2B where an admin is provisioned? | Self-serve consumer or prosumer | B2B admins **expect** setup work; a configuration step reads as competence, not tax. Most of §3 softens by one severity level |

Also assuming: web, mobile-responsive; user arrives with some intent from a marketing page; dashboard is the product's home surface.

---

## 1. Overall impression — the one-line answer

You asked what the heaviness is and couldn't name it. Here is my best single-sentence candidate:

> **Your flow asks twice before it gives once.**

Screen 1 takes something from the user (credentials, commitment, an email address they now have to manage). Screen 2 takes something again (decisions, attention, a set of choices they are not yet equipped to make). Only at screen 3 does anything come back — and if screen 3 opens on an empty dashboard, the flow takes twice and gives **zero**.

That is what "heavy" usually is. Not pixels. **Ledger.** Users don't consciously count fields; they feel the running balance of effort spent against value received. Two consecutive debits with no credit is the exact shape that produces a vague, hard-to-articulate drag — which is precisely how you described it. Nothing on any single screen looks wrong, because nothing on any single screen *is* wrong. The problem is in the **sequence**, which is invisible when you review screens one at a time in Figma.

Fill in your own ledger:

| Screen | What it asks from the user | What it gives back |
|---|---|---|
| 1. Email signup | Email, password, (confirm?), (name?), consent decisions, the commitment of creating an account | *(likely nothing)* |
| 2. Preferences | N decisions, made without context about what the product does | *(likely nothing — or a promise: "we'll personalize…")* |
| 3. Dashboard | *(possibly more: a setup checklist)* | The first actual value — **if** it isn't empty |

If your "gives" column is blank for the first two rows, stop reading and go fix that. Everything else in this document is secondary.

### The second candidate, which you should take seriously

The alternative one-liner: **three screens built by three different people at three different times.** Signup screens are usually inherited from the marketing site's design language (big type, hero treatment, generous padding, brand-saturated button). Preference steps are usually built as forms (dense, utilitarian, left-aligned labels). Dashboards are built in the app's design system (compact, data-dense, muted). Walking those three in sequence produces a jolt at each seam, and "heavy" is a very common way people describe that jolt — the flow doesn't feel like one thing.

Test: screenshot all three at the same viewport width, drop them side by side on one canvas, and look at nothing but the type scale, the button style, and the horizontal margins. If the three don't look like siblings, that's a real part of your answer.

---

## 2. The weight budget — how to put a number on "heavy"

You couldn't name it, so measure it. Walk your own flow once and fill the **Yours** column. The **Target** column is my opinionated threshold, not a benchmark from a published study — treat it as a bar I'd hold you to in review, not as data.

| Metric | Yours | Target | Why it matters |
|---|---|---|---|
| Screens before the user sees anything valuable | ____ | 1 | Every screen before value is pure tax |
| Required input fields, total across the flow | ____ | 1–2 | Email alone, or SSO. Each extra field is a fresh decision |
| Decisions required (toggles, choices, radio sets) | ____ | 0 before first value | Decisions cost more than typing — typing is motor, deciding is cognitive |
| Words on screen, per screen | ____ | < 40 | Onboarding copy is where reassurance goes to become weight (§6) |
| Interactions (clicks + taps + field focuses) to dashboard | ____ | < 6 | Counts the mouse/keyboard switching that fields force |
| Wall-clock seconds, honest walkthrough, no autofill | ____ | < 30 | Time with autofill off is the real number; your browser is lying to you |
| Dead ends (no skip, no back, no "later") | ____ | 0 | Reversibility reduces felt weight even when nobody uses it |
| Post-"completion" tasks still remaining (setup checklist items) | ____ | 0 | See D5 — this is the one that retroactively makes everything heavier |

Two instructions for running this honestly:
1. **Turn off password autofill and use a fresh incognito window.** Your saved credentials are hiding the true cost of screen 1 from you every time you test it.
2. **Count the last row carefully.** If you tell a user "3 steps" and then hand them a dashboard with a 5-item "Get started" checklist, your flow is not 3 screens. It is 8 steps with a misleading progress indicator, and the user finds out at the exact moment they thought they were done. That betrayal is disproportionately heavy.

---

## 3. Candidate diagnoses, ranked

Severity assumes the diagnosis tests positive. **Prior** = how often this is a real culprit in a flow shaped like yours.

| # | Candidate diagnosis | Prior | Severity | 10-minute test |
|---|---|---|---|---|
| **D1** | **Commitment before comprehension.** The account wall is screen one, so the user pays before they know what they're buying. Heaviness here is really *risk* — "how much is this going to cost me, and I can't tell yet." | High | Critical | Ask someone who has never seen the product to walk it and narrate. If they hesitate at the email field and ask "what is this going to do with my email," that's it. |
| **D2** | **Premature preferences.** You're asking the user to configure a product they have not used. They have no basis for any answer, so every choice is a guess, and guessing under uncertainty is the most expensive kind of thinking there is. | High | Critical | Instrument it: what % of users change any default? If most ship the defaults, the screen is a toll booth with no road behind it. |
| **D3** | **Copy weight.** Headline + subhead + reassurance paragraph + helper text per field + legal line. Individually justified, collectively a wall. Users don't read it, but they *see* the volume and price it as effort. | High | Major | Word-count each screen. Over ~40 words, start cutting. See §6 for the rewrites. |
| **D4** | **Design-language seam.** Three screens, three visual dialects (marketing / form / app). Reads as disjointed, gets described as "heavy." | Med-High | Major | The side-by-side canvas test in §1. |
| **D5** | **The payoff doesn't land.** Screen 3 opens on zeros, placeholders, or *another* checklist. The felt cost of screens 1–2 is set retroactively by what screen 3 delivers — an empty room makes the walk there feel much longer. | High | Critical | Create a brand-new account right now and screenshot the dashboard at t=0. Would that screen alone have convinced you to sign up? |
| **D6** | **Field inflation on signup.** Confirm-password, full name, company, two consent checkboxes. Each defensible; together they double the screen. Confirm-password in particular is a legacy pattern — a show/hide toggle plus a password-reset flow does the same job for less. | Med-High | Major | Count required fields. Every one that isn't email or password: name the concrete thing that breaks without it *today*. Not "we might want it for segmentation." |
| **D7** | **The progress indicator is advertising the toll.** "Step 1 of 3" reduces anxiety on long, unavoidable forms. On a short flow it does the opposite: it tells a user who wasn't yet worried that there is more work coming. | Medium | Minor-Major | Is your flow short enough to just *be* short? If you can get it to two screens, remove the stepper rather than shortening it. |
| **D8** | **No escape hatch.** No skip, no "set this up later," no back. A corridor with no doors is heavier than the same corridor with doors nobody uses. | Medium | Major | Try to abandon the preferences step. If you can't without losing the account, that's the finding. |
| **D9** | **Literal visual weight.** Heavy container borders, large shadows, oversized controls, full-bleed saturated brand color, tight line-height on long copy. | Medium | Minor | Screenshot, blur to 10px, and look at the value structure. If it's dark and even with no clear light areas, the screen has no rest in it. |
| **D10** | **Transition latency.** A spinner, a full page reload, or a >400ms gap between screens. Literal heaviness — the flow feels like it's dragging something. | Low-Med | Major *(if present)* | Walk it on throttled 3G in DevTools. Time each transition. |

**A ranking caveat:** D1/D2/D5 are structural and sit at the top because they're the classic cause of *unnameable* heaviness — your inability to point at the problem is itself weak evidence for a structural cause rather than a visual one, since visual problems are usually the ones people *can* point at. But that's an inference from a single sentence you wrote, not evidence. If the blur test (D9) comes back obviously dark and crowded, believe your eyes over my ranking.

---

## 4. Priority recommendations

Ordered by impact-per-unit-effort. Each is a concrete change, not a direction.

### R1 — Move one real piece of value in front of the account wall *(highest impact, medium effort)*

Let the user do the smallest genuinely useful thing the product does — one search, one calculation, one preview, one generated result — before you ask for an email. Then sign up to **save** it.

This reframes the account from a toll into a receipt. The email field stops being "give me your data" and becomes "keep the thing you just made." Same field, same keystrokes, completely different felt weight.

If a pre-auth path is genuinely impossible (regulated data, team-provisioned accounts), fall back to R1b: put a single concrete, specific outcome line on the signup screen — not a benefit adjective. "Your first report is ready in about a minute" beats "Powerful analytics for modern teams."

### R2 — Delete the preferences step *(highest impact-per-effort)*

Default everything. Infer what you can from signup context, plan, or first actions. Surface the settings **in the product**, at the moment they first matter, where the user finally has enough context to answer well.

Deleting a screen is the only reliably successful UX optimization. Every other change trades one cost for another.

**R2b — if it must stay** (see §5 for when that's right):
- Cut it to **one** question. The single one with the highest fan-out on the user's experience.
- Show the effect immediately — the choice should visibly change something on-screen.
- Make "Skip" a real, visible, same-weight control. Not grey 12px text in the corner.
- Pre-select the best default so the primary button is a confirmation, not a decision.

### R3 — Make the dashboard's first frame earn the trip *(high impact, medium effort)*

Never open on zeros. Options in descending order of preference:
1. Real data, if anything at all can be computed or imported at t=0.
2. Seeded sample content, clearly labeled as a sample and one click to clear.
3. A single, specific, obvious first action — one primary control, not a grid of six equal cards.

And **do not put a setup checklist here** if you told the user the flow was three steps. Pick one: either the checklist is inside the flow and counted honestly, or the flow is over and the dashboard is the reward.

### R4 — Strip screen 1 to email and password *(low effort, immediate)*

Remove: confirm-password (use show/hide + a working reset flow), name, company, and any field whose absence doesn't break something today. Move marketing consent out of signup entirely — as an opt-in later, it's both lighter and cleaner under GDPR-style unbundled-consent rules.

**One flag:** whether terms acceptance can be an inline statement under the button rather than a checkbox depends on your jurisdiction and contract posture. I'm recommending the lighter pattern; get your counsel to confirm it before shipping. I'm not qualified to clear that.

### R5 — Unify the three screens' design language *(medium effort, fixes D4)*

Pick the app's system as the destination dialect and pull screens 1 and 2 toward it: same type scale, same button, same container width, same margins. The user should feel they are already inside the product on screen 1, not that they're being escorted from the website into the building.

### R6 — Cut the copy *(lowest effort, do it today)*

See §6 for line-by-line rewrites.

---

## 5. Where I'd push back on my own advice

Two cases where following R2 would be wrong:

- **The preferences step feeds the dashboard.** If those answers are what make screen 3 non-empty, deleting the step makes your worst problem (D5) worse. In that case: don't delete, **merge**. Fold the one load-bearing question into the signup screen or the dashboard's first frame, so the flow is two screens with the same information collected.
- **You're B2B with an evaluating buyer.** Admins configuring a tool for a team read setup as thoroughness. A too-light flow can read as a toy. The heaviness you're feeling may be *your* impatience on your eightieth walkthrough, not a user's on their first.

---

## 6. UX Copy — `[SKILL]` rewrites

Copy is the cheapest weight to remove and it's usually 20–30% of the felt load. Below, the "Before" lines are the **common industry pattern reconstructed**, not quotes from your product — swap in your actual strings and the same cuts will apply.

### Screen 1 — Signup

| Element | Before *(typical pattern)* | After | Why |
|---|---|---|---|
| Headline | "Welcome to [Product]!" | "[Verb] your first [core noun]" — e.g. "Publish your first report" | A welcome is about you. An outcome is about them, and it tells them what the email buys |
| Subhead | "Create your account to get started. It only takes a minute." | *(delete)* | "Only takes a minute" plants the idea that it might not. Never reassure about a cost the user hadn't noticed |
| Password helper | "Must be at least 8 characters and include one uppercase letter, one number, and one special character." | "At least 8 characters" — show the rest inline, only on violation | Five rules displayed up front is a pre-emptive list of ways to fail |
| Confirm password | "Confirm password" | *(delete — add show/hide toggle)* | A legacy pattern from before show/hide and working reset flows |
| Consent checkbox | "☐ I agree to the Terms of Service and Privacy Policy" | "By continuing, you agree to the Terms and Privacy Policy." *(inline, under button)* | Removes a required interaction. **Verify with counsel first** |
| Marketing checkbox | "☐ Send me product updates and tips" | *(remove from signup; ask after activation)* | Cleaner consent posture and one less decision at the most fragile moment |
| Primary CTA | "Submit" / "Continue" | "Create account" | Verb + object. The user should never have to infer what a button does |
| Error, taken email | "Error: This email address is already in use." | "That email already has an account. **Log in** or **reset your password**." | What happened + why + how to fix — with the fix as a live control, not a description of one |
| Error, weak password | "Invalid password." | "Passwords need at least 8 characters. Yours has 5." | Name the rule and the gap. "Invalid" makes the user diff their input against a spec they can't see |

### CTA alternatives

| Option | Copy | Tone | Best for |
|---|---|---|---|
| A | "Create account" | Neutral, plain | Default. Highest clarity, lowest risk |
| B | "Create free account" | Reassuring | If price anxiety is the drop-off cause and free is genuinely free |
| C | "Get started" | Friendly, vague | Avoid — says nothing about what happens next |
| D | "Save my [noun]" | Earned | **Only if you ship R1** — best possible version of this button, because it names value the user already has |

### Screen 2 — Preferences *(if it survives)*

| Element | Before *(typical pattern)* | After | Why |
|---|---|---|---|
| Headline | "Tell us about yourself" | "One question, then you're in." | Names the remaining cost honestly and caps it |
| Subhead | "This helps us personalize your experience." | *(delete, or make it concrete: "This sets what's on your home screen. You can change it anytime.")* | "Personalize your experience" is the most common empty sentence in onboarding. It promises nothing checkable |
| Skip | *(absent, or 12px grey "skip")* | "Skip for now" — same size and weight as the primary, secondary styling | A visible exit lowers felt weight for everyone, including the people who don't take it |
| CTA | "Next" | "Go to dashboard" | Name the destination. "Next" implies an unknown quantity of further nexts |

### Screen 3 — Dashboard first frame

| Element | Before *(typical pattern)* | After | Why |
|---|---|---|---|
| Empty state | "No data yet." | "Your [reports] will appear here. Create your first one — it takes about 30 seconds." + primary button | Empty-state pattern: what this is + why it's empty + how to start |
| Success/entry | "Setup complete! You're all set." | *(delete — just show the product)* | If you have to *tell* them it's done, the screen isn't showing it. Congratulation copy over an empty dashboard is the flow's worst moment |
| Zero metrics | Six cards reading "0" | Hide until they have values, or seed one labeled sample | Six zeros is a visual statement that the product is empty. It's also, literally, the heaviest-looking possible first frame |

**Localization note:** "Create account" and "Skip for now" expand roughly 30% in German and French. Size the buttons for the longest supported locale, not English. Avoid copy that depends on sentence-fragment continuation between a label and a button — it doesn't survive translation.

---

## 7. Visual hierarchy — what *should* draw the eye

Prescriptive, since I can't observe yours. On each screen, exactly one element should win the 2-second test:

| Screen | Should draw the eye | Common failure that dilutes it |
|---|---|---|
| 1. Signup | The email field, then the CTA | A large brand hero / illustration / logo lockup taking the top third, pushing the actual work below the fold on laptop screens |
| 2. Preferences | The single question | 6–8 equally-weighted toggles with no visual ranking, so the eye has nowhere to land and has to read all of them |
| 3. Dashboard | The one action that produces first value | A grid of equal-weight cards. Equal weight = no hierarchy = the user must evaluate every option before acting |

**Reading flow to aim for on all three:** one line of orientation → the input or action → everything else. If legal text, social proof, or navigation competes with the input for the eye, it's contributing weight without doing work.

**The squint test** is the fastest instrument here: blur each screen until you can't read type. Exactly one thing should still be obvious. If two things are equally loud, the user is being asked to arbitrate, and arbitration is felt as effort.

---

## 8. What is probably working

Stated as what I'd expect to hold, so you can verify rather than assume:

- **Three screens is the right order of magnitude.** You're not looking at a 9-step wizard. The fix is trimming and resequencing, not a rebuild — which means every recommendation above is cheap relative to its payoff.
- **The sequence is logically sound.** Identity → configuration → product is a coherent mental model. You've built the right steps; my argument is about *when* each one is asked for, not whether it belongs.
- **You noticed.** A flow that feels heavy to the person who built it is almost always much heavier to a first-time user — you have the benefit of knowing what's coming and you *still* feel the drag. Your instinct is the signal here; the work is just naming it.

---

## 9. Skills I did not run, and why

Honest routing matters more than covering all four skills in the pack.

- **`[SKILL]` — not run.** A WCAG 2.1 AA audit requires an artifact: real color values for contrast ratios, real DOM for focus order, real touch targets to measure. Producing a filled-in contrast table from a verbal description would be fabrication, and a fabricated audit is worse than no audit because it looks like a clean bill of health. **Run it when you have the URL or screenshots.** When you do, these are the four checks most likely to fail on a flow of this shape: (1) **1.4.3** — placeholder-only labels and grey helper text under fields, the most common contrast failure in signup forms; (2) **3.3.2** — placeholders used *as* labels, which vanish on focus and leave screen-reader users without a field name; (3) **2.4.7** — focus indicators suppressed by a CSS reset on custom-styled inputs and toggles; (4) **2.5.5** — preference toggles under 44×44px on mobile.
  One overlap worth noting now: **cognitive load is an accessibility concern**, not just a polish one. Every recommendation in §4 that removes a decision also helps users with cognitive disabilities. R2 and R4 are accessibility wins even though I'm not claiming a WCAG number for them.
- **`[SKILL]` — not run.** Handoff specs are for a design that's settled and heading to engineering. Yours is under diagnosis and I'm recommending you delete a screen. Writing tokens, props, and breakpoint tables for a flow that should lose a third of itself would be work you'd throw away. Run `[SKILL]` after you've picked from §4 and settled the new flow.

---

## 10. Stress test

Required by the skill rules, and genuinely warranted here — this analysis has real weaknesses.

**The weakest thing about this critique:** I have not seen the design. Every diagnosis is a prior, not an observation. If I'm wrong about the shape of your product, the entire ranking in §3 inverts. Treat §3 as a test plan, not a report.

**What a smart critic would say, and they'd have a point:**

1. **"You told him to delete the preferences step without knowing what it feeds."** Correct, and it's the sharpest objection. If that step populates the very thing that makes the dashboard non-empty, R2 makes D5 — my own top-ranked problem — strictly worse. I flagged this in §5, but it deserves to be louder: **answer question 1 before touching R2.** Deleting a screen is only free if nothing downstream depends on it.
2. **"Heavy might just mean heavy."** My whole framing is structural — ledger, sequence, asks vs gives. But "heavy" is a *visual* word and the obvious reading is that the screens are literally visually dense: dark buttons, heavy borders, tight leading, saturated color. I ranked D9 ninth on the reasoning that unnameable problems tend to be structural. That's an inference from one sentence, and it could be straightforwardly wrong. Run the blur test early; it takes two minutes and could reorder everything.
3. **"Three screens is already short — this may be a non-problem."** Plausible. You might be over-indexing on a flow that's fine because it's the surface you happen to be looking at, while the real drop-off is in week-one retention. Without funnel data, neither of us knows whether onboarding is where the loss is. The cheapest counter: pull per-screen drop-off before you spend a sprint here.
4. **"Optimizing for completion can make things worse."** Real risk, and it's the trap in R1/R4. Strip signup to one field and completion rate rises — but you may just be admitting more low-intent accounts that never activate. **Don't measure these changes on signup completion.** Measure on activation, or on day-7 retention of the signup cohort. A flow change that lifts signups 20% and drops activation 25% is a loss that looks like a win on the dashboard you'd naturally check.
5. **"Your assumption stack is load-bearing and untested."** Five assumptions in §0, all inferred from one sentence. The B2C/B2B one matters most: if this is B2B, most of §3 softens by a full severity level and R2 is probably wrong outright.

**What would change my mind fastest, in order of cost:** (a) the t=0 dashboard screenshot — 2 minutes, and it settles D5, my highest-ranked structural claim; (b) the blur test on all three screens — 2 minutes, settles the structural-vs-visual question the whole ranking rests on; (c) per-screen drop-off numbers — replaces this entire differential with evidence.
