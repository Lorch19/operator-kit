## UX Review: dark-theme accessibility — verbal description, no artifact — 2026-09-16

**Skill:** `ux-reviewer` (five passes; Pass 5 floor checks carry most of the weight here)
**Against:** `DESIGN-TARGETS.md` — **PROVISIONAL**. None exists; I drafted the ten criteria
below from the evident purpose and marked them for your confirmation. Drafting them is in
this skill's job description, not an overreach — but they are mine, not yours, until you say so.
**Verdict: fix-then-ship** (advisory — you decide).

---

### The short answer

**No — not on what you've described, and you already named two of the three near-certain failures.**

- The **mid-blue button with a white label is the most likely hard failure.** A typical mid-blue
  (`#3B82F6`) under white text measures **3.68:1** — under the 4.5:1 AA floor. Not marginal.
- The **grey-on-grey is a coin flip that you are probably losing twice**: once on the numbers,
  and once on *which background you measured against*.
- The part that will actually generate a complaint isn't in your question at all: **focus
  visibility**. If your focus ring is the brand blue, then on the blue button it measures
  **1.00:1** — a keyboard user cannot see where they are on your single most important control.

The good news: every one of these is a token change, not a redesign. The dark theme is not the
problem. Its calibration is.

**Why blue specifically, in plain English:** the contrast formula weights the three colour
channels by how much your eye uses them for brightness — green counts for **72%**, red **21%**,
and blue only **7%**. So a blue can look vivid and confident while being, to the maths, almost as
dark as the near-black behind it. That is why blue primary buttons fail this test more reliably
than any other colour, and why the failure always surprises people: it looks fine.

---

### Pass 0 — what I could actually see (read this before trusting anything below)

**I reviewed zero screens.** No build, no screenshot, no code, no Figma, no token file. This
skill's checklist treats rendering the build as a precondition, not an option — twice on a prior
project a spec read well and the built screen was rejected on sight, and the first review to work
from rendered frames found two defects no prose review could reach. **I could not meet that
precondition, so this review is explicitly lower-confidence** and every finding below is written
as a *prediction with a threshold attached*, so you can falsify it in minutes rather than argue
with it.

Screens I did not see: **all of them.** I do not know how many there are, what they do, or which
of them the greys and the blue actually appear on.

- **Screens-per-treatment split: not computed — uncomputable.** The checklist requires me to
  count how many screens share each visual treatment and confirm the highest-coverage treatment
  carries the most energy. The artifact is one sentence and names no screens. I am recording this
  as *unrun*, not as passed; an unstated count is an unrun check.
- **No locked visual direction exists.** There is no `DESIGN-TARGETS.md`, so no criterion names
  what this should *look* like. That absence is itself a finding (C10 below): it means every
  criterion in play is measurable, and nothing in the contract can catch "has no point of view."

**What I did instead of eyeballing:** computed WCAG 2.1 ratios and APCA Lc values across a sweep
of plausible dark-theme tokens, so the thresholds below are numbers you can check, not adjectives.

---

### Questions I could not ask, and what I assumed instead

This ran unattended. These are the questions that would have changed the review, with the
assumption I proceeded under. **Where an assumption is wrong, the finding it supports changes —
I've said how.**

| # | Question | Assumed | If the answer differs |
|---|---|---|---|
| Q1 | What are the actual hex values — page, panel, each grey, the blue? | Page `#0B0B0E`, panel `#1C1F26`, greys `#6E7681`–`#8A8F98`, blue `#3B82F6` | Find your real row in the tables below; the shape of the conclusion holds, the exact numbers move |
| Q2 | Is the primary button's label white? | Yes (the overwhelming default) | If it's dark text on the blue, **B1 drops entirely** — `#3B82F6` with a near-black label is 5.34:1 and passes |
| Q3 | Does text sit on the near-black page, or on cards/panels above it? | Both, and the tokens were tuned against the page | If everything is flat on the page with no elevated surfaces, **B3 drops** |
| Q4 | What conformance bar are you held to — AA, AA+VPAT, or "no complaints"? | **WCAG 2.2 AA**, the default commercial bar | AAA moves the text floor from 4.5:1 to 7:1 and fails more greys; "no complaints" makes M1 the finding that matters most |
| Q5 | Is dark the only theme, or is there a light one / `prefers-color-scheme` support? | Dark-only | If a light theme exists and is reachable, **M6 drops to Minor** |
| Q6 | Is the focus ring colour the brand blue? | Yes (the default in most systems) | If it's white or near-white, **B2 drops** |

---

### Criteria scorecard — PROVISIONAL targets, drafted by this review

Scored strictly: "probably fine" is **risk**, never pass. Pass needs evidence, and I have very
little. That most of this column is not "pass" is a statement about my inputs, not about your design.

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| C1 | Body and secondary text ≥ 4.5:1 **against the surface it actually renders on** | **risk → likely fail** | "Lots of grey-on-grey" is the single highest-yield predictor of this failure. `#7D848E` measures 5.21:1 on the page and **4.37:1 on a `#1C1F26` panel** — passes and fails depending on baseline |
| C2 | Body text reaches APCA **Lc ≥ 75** (readability, not just legality) | **fail (predicted)** | Any grey that merely scrapes 4.5:1 on dark lands at Lc 34–45. `#8A8F98` is AA-compliant at 5.08:1 and **Lc 39.9** — non-text territory. See M1 |
| C3 | Primary button: fill ≥ 3:1 vs its surface **and** label ≥ 4.5:1 vs fill | **fail**, conditional on Q2 | `#3B82F6` + white = **3.68:1**. The window where both halves pass is narrow — see the table in B1 |
| C4 | Focus indicator ≥ 3:1 against **every** surface it can land on, including the primary button's own fill | **fail**, conditional on Q6 | Brand-blue ring on brand-blue fill = **1.00:1**. Even `#93C5FD` on `#2563EB` is 2.87:1, under the floor |
| C5 | No state or status conveyed by colour alone | **unverifiable** | Not mentioned. In a dark UI with a blue/grey ramp this is where the second wave of defects lives |
| C6 | Disabled is distinguishable from enabled by more than opacity | **risk** | Standard dark-theme practice (opacity reduction) collapses into the grey ramp — see M4 |
| C7 | Container boundaries survive forced-colors / Windows High Contrast | **risk** | Panel-vs-page elevation measures **1.06–1.47:1** — see M3 |
| C8 | Touch targets ≥ 24px (WCAG 2.2 AA 2.5.8); 44px practical | **unverifiable** | No layout seen |
| C9 | 200% text zoom and 400% reflow without loss | **unverifiable** | No layout seen |
| C10 | The design reads as a named, deliberate visual direction | **fail — no criterion exists** | There is no locked direction to score against. This is the one criterion the measurable ones cannot fake, and it is absent. See M7 |

---

### Catches

**9 findings (3 Blocker, 6 Major) against the ~12 Catches cap. Under the cap. Nothing cut.**

Ranked. The counter-proposal leads.

---

**B1 · Blocker · The primary button's label fails AA against its own fill**

*Countable artifact:* the primary button's `label` colour token against its `fill` token.

*Evidence.* Two independent requirements collide on this one control, and a mid-blue sits in the
gap between them. The fill must reach 3:1 against the page so the button's edge is perceivable
(WCAG 1.4.11); the label must reach 4.5:1 against the fill (1.4.3). Measured:

| Blue fill | Fill vs `#0B0B0E` page (need 3:1) | **White label** (need 4.5:1) | Near-black label |
|---|---|---|---|
| `#1D4ED8` | 2.93 ✗ | 6.70 ✓ | 2.93 ✗ |
| **`#2563EB`** | **3.80 ✓** | **5.17 ✓** | 3.80 ✗ |
| **`#2F6FEE`** | **4.33 ✓** | **4.54 ✓** | 4.33 ✗ |
| `#3B82F6` ← *typical "mid-blue"* | 5.34 ✓ | **3.68 ✗** | 5.34 ✓ |
| `#4C8DF6` | 6.03 ✓ | 3.26 ✗ | 6.03 ✓ |
| `#60A5FA` | 7.73 ✓ | 2.54 ✗ | 7.73 ✓ |

Read the white-label column: it crosses the 4.5:1 line between `#2F6FEE` and `#3B82F6`. **Every
blue lighter than roughly `#2F6FEE` fails with white text**, and lighter is exactly the direction
people push a blue to make it "pop" on near-black. Meanwhile `#1D4ED8` and darker fail the *other*
requirement. The usable window for a white-labelled blue on near-black is about **`#2563EB` to
`#2F6FEE` — narrow, and your described colour is most likely above it.**

*Cheaper alternative.* Change one token: **fill `#2563EB`, label `#FFFFFF`** (5.17:1 label, 3.80:1
fill). Do not keep the lighter blue and switch to a dark label — technically it passes at 5.34:1,
but dark text on a blue button is a convention break that will read as a bug, and it removes your
margin on the *next* palette tweak. One caveat: `#2563EB` measures only **3.19:1 against a
`#1C1F26` panel**. If the primary button ever sits on a card rather than the page, it clears 3:1
by 0.19 — so fix the token and then verify it on the card, not only on the page.

---

**B2 · Blocker · The focus ring is invisible on the primary button**

*Countable artifact:* the `:focus-visible` ring colour token, evaluated against the primary
button's fill.

*Evidence.* Focus indicators are non-text and need 3:1 against adjacent colours. The near-universal
default is to reuse the brand colour for the ring — which means on the brand-coloured button:

| Ring | vs page | vs panel | **vs blue fill `#2563EB`** |
|---|---|---|---|
| `#3B82F6` (brand blue) | 5.34 ✓ | 4.48 ✓ | **1.00 ✗** — identical colour, literally invisible |
| `#93C5FD` (light blue) | 10.90 ✓ | 9.15 ✓ | **2.87 ✗** |
| `#A5B4FC` | 9.86 ✓ | 8.27 ✓ | 1.84 ✗ |
| **`#E6E9EE`** | 16.15 ✓ | 13.55 ✓ | **4.25 ✓** |
| **`#FFFFFF`** | 19.65 ✓ | 16.49 ✓ | **5.17 ✓** |

This is the finding most likely to produce an actual accessibility complaint, because it does not
degrade gracefully: a keyboard-only user tabbing through your UI hits the primary action and the
cursor vanishes. It also passes every contrast audit that checks rings against the *page*, which is
why it survives to production.

*Cheaper alternative.* Make the ring **`#FFFFFF` or `#E6E9EE`, 2px, with a 2px offset painted in
the page-ground colour**. The offset is what lets one ring token work on both the dark page and
the blue fill — you get a light-dark-light sandwich that is visible against anything. One token,
one shadow rule, every control covered.

---

**B3 · Blocker · The greys were almost certainly measured against the wrong background**

*Countable artifact:* every text colour token whose contrast was checked against `--bg-page`
rather than against the nearest opaque ancestor it actually renders on.

*Evidence.* This is the defect that ships past green automated tests, and "lots of grey-on-grey"
plus a dark theme is its exact habitat. The same grey, three baselines:

| Grey | on page `#0B0B0E` | on `#16181D` | on panel `#1C1F26` |
|---|---|---|---|
| `#6E7681` | 4.28 ✗ | 3.87 ✗ | 3.59 ✗ |
| **`#7D848E`** | **5.21 ✓** | **4.70 ✓** | **4.37 ✗** ← passes and fails depending on baseline |
| `#8A8F98` | 6.05 ✓ | 5.47 ✓ | 5.08 ✓ |

`#7D848E` is a perfectly respectable secondary-text grey that **passes AA on the page ground and
fails on a card.** An audit that checks it once, against the page, returns green and means nothing.
On a prior project this exact mistake shipped body text at 4.07:1 across all ten themes with a
passing test suite: the measurement was correct, the baseline was wrong.

*Cheaper alternative.* Re-run every text token against the **darkest surface it can legally appear
on**, not the page — and if a token can appear on several, hold it to the worst case. Then state the
rule in the token file next to the value, so the next person cannot re-derive it against the page:
`--text-secondary: #A8AEB8; /* min baseline: --surface-raised #1C1F26, 7.39:1 */`. A comment costs
nothing and outlives the audit.

---

**M1 · Major · The greys that pass AA will still be too dim to read**

*Countable artifact:* the body-text colour token.

*Evidence.* WCAG 2.x contrast maths is polarity-blind — it is a ratio, so it gives the same score to
a pair whether you put the light colour on top or the dark one. That is known to **over-credit dark
backgrounds**, and it is why dark UIs so often feel squinty despite passing. Measured on the panel:

| Grey | WCAG | APCA Lc | APCA reading |
|---|---|---|---|
| `#8A8F98` | 5.08 ✓ AA | **39.9** | below the Lc 60 content floor — not fit for text |
| `#949AA3` | 5.82 ✓ AA | 45.4 | large headlines only |
| `#A8AEB8` | 7.39 ✓ | 56.2 | approaching content-text |
| **`#C9CED6`** | 10.43 ✓ | **74.6** | **first value that reaches the Lc 75 body floor** |

So: **a grey has to hit roughly 10:1 on a dark panel before it is genuinely comfortable body text,
not 4.5:1.** If your greys are clustered where they "look right" on an OLED screen in a dim room,
they are almost certainly in the Lc 30–50 band — legal, and tiring.

*Cheaper alternative.* Ship to AA for compliance, but set the **body token by the APCA number**:
`#C9CED6` or lighter for anything you expect someone to read a paragraph of. Use AA as the floor
for everything else. You do not need to adopt APCA as a standard to use it as a sanity check.

---

**M2 · Major · Luminance is doing two jobs, and accessibility eats the range the other one needs**

*Countable artifact:* the number of distinct grey **text** tokens — flag at 4+.

*Evidence.* This is the structural reason naive contrast fixes make dark designs worse, and it is
the finding I would most want you to take away. Grey-on-grey uses luminance to carry **hierarchy**
(this matters more than that). The accessibility floor forces luminance to carry **legibility**
(everything must clear a bar). On a dark theme those two demands fight, because the usable range is
lopsided:

- Between a compliant body (`#C9CED6`, Lc 74.6) and pure white there is only **31 Lc of headroom** —
  that is your entire budget for headings, emphasis, and anything louder than body.
- Everything *below* body that is still AA-legal sits at **Lc 34–45** — technically permitted, but
  APCA classes it as non-text. Your "quieter" tier is quiet because it is unreadable.

So a five-step grey ramp on dark cannot exist: the top three steps are crushed into 31 Lc and the
bottom two are sub-readable. Raise them all for contrast and the hierarchy flattens; keep the
spread and the bottom fails. There is no setting of the greys that satisfies both.

*Cheaper alternative.* **Stop making luminance carry hierarchy. Move hierarchy onto weight, size,
and spacing, and let luminance serve legibility alone.** Concretely: collapse to **two** text greys
(`#C9CED6` body, `#A8AEB8` secondary — 10.43:1 and 7.39:1 on panel, Lc 74.6 and 56.2), and express
every distinction you currently make with a third and fourth grey as a type-weight or type-size
step instead. This is cheaper than it sounds — it deletes tokens rather than adding them — and it is
the move that makes the contrast fix *not* flatten the design.

---

**M3 · Major · Surface elevation is not a usable channel on dark either**

*Countable artifact:* any container (card, menu, modal, popover, dropdown) whose only boundary is
a `background-color` difference.

*Evidence.* The dark-theme habit of separating layers by lightening the fill barely registers:

| Panel | vs page `#0B0B0E` |
|---|---|
| `#121317` | 1.06 |
| `#16181D` | 1.11 |
| `#1C1F26` | 1.19 |
| `#23262E` | 1.30 |
| `#2B2F39` | 1.47 |

Every one of these is far below 3:1. For a low-vision user the card has no edge. In Windows High
Contrast / forced-colors mode, background colours are overridden outright and the container
disappears entirely — a dropdown becomes text floating over text. This compounds M2: with hierarchy
squeezed out of text luminance *and* out of elevation, a dark UI has fewer channels than a light one
and has to use the remaining ones deliberately.

*Cheaper alternative.* Give **load-bearing** containers only — menus, modals, popovers, anything
that overlaps other content — a **1px border at ≥3:1** against both surfaces. Not every card;
bordering everything is the over-correction that makes dark UIs look like spreadsheets. Decorative
grouping can keep using fill alone.

---

**M4 · Major · Disabled and de-emphasised will look identical**

*Countable artifact:* the `disabled` token compared against the lowest-tier text token.

*Evidence.* Dark themes almost always implement disabled as reduced opacity. On a grey-on-grey
ramp, a dimmed secondary grey lands on top of the tertiary grey — so "you cannot interact with
this" and "this is less important" become the same pixel value. The user's only way to tell them
apart is to click and get nothing, which is the definition of a mis-affordance.

*Cheaper alternative.* Make disabled differ on a **second channel**: remove the fill entirely and
keep an outline, or drop the affordance's shadow/border, or add a cursor and `aria-disabled` change.
One non-luminance difference is enough. (Note the counter-pressure: disabled controls are exempt
from contrast requirements, so it is tempting to push them very dark — but exempt from the
*requirement* is not the same as *usable*, and a form whose submit button is invisible is not a
form.)

---

**M5 · Major · Colour-only signalling — flagged by its absence from your description**

*Countable artifact:* every status indicator whose only differentiator is `color`.

*Evidence.* You described three things and all three are colour. Nothing in your question touches
non-colour signalling, which in a dark UI is where the second wave of defects lives: status dots,
chips, badges, validation states, chart series, diff highlighting. Two compounding problems on dark
grounds — hue separation compresses (saturated colours all trend toward "bright thing on black"),
and red, the standard error colour, is the second-worst hue after blue under the luminance formula.
I cannot confirm this is a defect. I can confirm it is unexamined, which at ship time is the same
risk.

*Cheaper alternative.* Audit every place colour carries meaning and add a second cue — an icon
shape, a text label, or a pattern. Cheapest version: error states get an icon plus text, status dots
get a label, chart series get direct labels rather than a colour legend.

---

**M6 · Major · If dark is the only theme, some users have no way out** *(conditional on Q5)*

*Countable artifact:* the presence or absence of a light token set, and whether
`prefers-color-scheme` is honoured.

*Evidence.* Dark mode is an accessibility *win* for some users (photophobia, migraine) and a
*loss* for others — many people with low vision or astigmatism read light-on-dark worse, because
light glyphs on dark ground bloom optically (halation) and thin strokes smear. Neither WCAG nor any
audit requires you to offer both, so this never shows up as a violation; it shows up as a support
ticket. It also covers the mundane case: your app in direct sunlight.

*Cheaper alternative.* Honour `prefers-color-scheme` and expose a manual toggle. If a full light
theme is out of scope for this release, say so as a **deliberate deferral in the design targets**
rather than leaving it undecided — that is the difference between a known gap and a surprise.

---

**M7 · Major · The design contract has no criterion that can catch "looks wrong"** *(process, not pixels)*

*Countable artifact:* `docs/design/DESIGN-TARGETS.md` — does not exist.

*Evidence.* Every criterion in the scorecard above is measurable, because I generated them from an
accessibility question. A design can pass all ten and still be rejected on sight; contrast ratios
cannot encode whether the screen has a point of view. You are about to fix nine contrast defects
and ship a theme that no written target describes.

*Cheaper alternative.* When you accept the token changes, write them into a
`docs/design/DESIGN-TARGETS.md` along with **one named visual direction** in your product's own
language ("does this read as *Console*?"), plus the coverage split — how many screens each
treatment covers. Ten minutes now; it is what makes the next review scoreable instead of
re-derived, and it stops the greys drifting back.

---

### Minor & polish

- **Do not overshoot.** Pure white body on near-black is **19.65:1, Lc 107.7** — over-contrast, and
  the direct cause of halation for astigmatic readers. Cap body around `#DDE1E7`–`#EDEFF2`.
- **Placeholder text** is usually the bottom of the grey ramp and is still text; it is exempt from nothing.
- **Links vs body text**: if a blue link is distinguished from grey body by colour alone, the two need 3:1 *between them* — a blue-on-grey pairing in a dark palette frequently misses this. Underline is the cheap fix.
- **`:visited`, selection highlight, and text-selection colours** are routinely left at browser defaults that were designed for light backgrounds.
- **Dividers, hairlines, and scrollbars** below 3:1 vanish; they are non-text UI when load-bearing.
- **Error/success text**: red and green are the two worst-behaved hues on dark grounds; measure them explicitly rather than reusing the light-theme values.
- **Chart and data-viz palettes** need a separate pass from UI colours — series separation is a ΔE problem between *adjacent* colours, not a contrast problem against the ground.
- **Text over images, gradients, or video** has no fixed baseline; needs a scrim with a stated minimum.
- **200% zoom / 400% reflow** (WCAG 1.4.4, 1.4.10) — unexamined.
- **Touch targets** — WCAG 2.2 AA requires 24px minimum (2.5.8); 44px is the practical bar. Unexamined.
- **`prefers-reduced-motion`** — unexamined; nothing essential should be conveyed by animation alone.

### Truncated

```
Truncated: none — everything the passes produced is listed above.
```

Catches list is **9 (3 Blocker, 6 Major) against the ~12 cap — under it, nothing cut.** Minor and
polish are compressed above and uncapped. Passes 2, 3 and 4 (cold read, structure, craft) produced
almost nothing not because the design is clean but because **I had no screens to run them against**
— that is a limit of the input, and I am recording it as such rather than reporting a quiet pass.
The one structural finding those passes did yield is M2.

### What must not change

Three things, because the obvious fixes to the findings above would damage all three.

1. **The dark theme itself.** Nothing here argues against it. Every defect is a calibration error
   inside a legitimate choice. Do not read "nine accessibility findings" as "go light".
2. **Grey-on-grey as a technique.** Using luminance steps instead of boxing everything is a quieter,
   more confident way to build hierarchy, and it is why the design presumably looks good to you.
   M3 asks for borders on *load-bearing containers only* — menus, modals, popovers. Bordering
   everything is the over-correction, and it is a worse outcome than the bug.
3. **Restraint in the text palette.** The reflexive fix is to push every grey toward white. That
   fails twice: it flattens the hierarchy (M2) and it creates halation (Minor #1). The fix is
   *fewer* greys placed deliberately, not *brighter* greys.

### Unverifiable from this artifact

Needs the running build. Every one of these is a promise coming due — when the build exists,
re-run this review against rendered frames and settle them:

- **All of C1, C3, C4** as *actual* rather than predicted values — the real hex tokens against the real surfaces.
- **C5** colour-only signalling — needs an inventory of every status/validation surface.
- **C8** touch targets, **C9** zoom and reflow — need layout at a real viewport.
- **The screen sequence.** This skill's checklist requires judging the *set* of screens someone
  moves through in one sitting, not one frame — verdicts like "this feels cheap" are almost always
  about the run, not the screen. I saw no sequence at all.
- **The treatment coverage split** — uncomputable here (see Pass 0). Recorded as unrun.
- **Forced-colors / High Contrast mode** — needs a Windows render.
- **Whether any of the nine findings are already fixed.** I am reasoning from one sentence.

---

### The 30-minute procedure that settles this properly

Because I cannot see your build, the most useful thing I can hand you is the test that replaces
this review's guesses with your numbers. In order, cheapest first:

1. **Open your token file and list every text colour and every surface colour.** (2 min)
2. **For each text token, identify the *darkest surface it can render on* — not the page.** Write it
   down next to the token. This single step is B3, and it is the one most audits skip. (5 min)
3. **Measure each pair.** Any browser devtools contrast checker, or the script pattern in this
   review. Flag anything under 4.5:1 — and separately flag anything under ~10:1 that carries body
   copy, which is M1. (10 min)
4. **Measure the primary button twice**: fill vs the surface behind it (need 3:1), and label vs fill
   (need 4.5:1). This is B1 and it takes 60 seconds. (2 min)
5. **Tab through one screen with the mouse untouched.** Watch for where the focus ring disappears.
   Do it on the primary button specifically. This is B2 and no tool will find it for you. (5 min)
6. **Screenshot one screen, desaturate it to greyscale.** Anything you can no longer tell apart is
   M5. (3 min)
7. **Disable one control and put it next to a de-emphasised one.** If you cannot tell which is
   which, that is M4. (3 min)

Steps 4, 5 and 7 need no tooling and cover two of the three Blockers.

---

### Stress Test

**What's weakest here.** I reviewed a sentence. Every number in this document comes from a palette
I invented to be plausible, not from your build — so the *specific* values are illustrative and the
*shape* of the argument is what should survive. If your blue is `#2563EB` rather than `#3B82F6`, B1
evaporates. If your greys are already at `#C9CED6`, M1 and M2 evaporate. I have written the
findings as predictions with thresholds precisely so you can kill them fast, but a review that can
be killed that fast is a hypothesis, not an audit. **Treat this as a prioritised test plan that
happens to come with a probable answer, not as a verdict.**

**Assumptions that could be wrong.** The biggest is Q2 — that the button label is white. It's the
default, but if the label is dark then the loudest finding in this review is simply wrong. The
second is that elevated surfaces exist at all; a genuinely flat dark theme drops B3. The third is
that "mid-blue" means something around `#3B82F6` — that phrase covers a range wide enough to sit on
either side of the failure line.

**Where a smart critic would push back.**
- *"APCA isn't a standard — you're holding me to a draft."* Fair, and I flagged it: AA is the
  shipping bar, APCA is the sanity check. But the critic who dismisses M1 entirely ships a legally
  compliant UI that users describe as hard to read, and then has no vocabulary for why. The gap
  between 4.5:1 and Lc 75 on dark backgrounds is real whatever you call it.
- *"Nine findings from one sentence is padding."* The honest answer is that three of them (B1, B2,
  B3) come from the description and the maths, and six are the standard dark-theme failure set that
  the description doesn't rule out. M5 in particular is flagged *because* it was absent from your
  question, which is weaker evidence than a defect I observed. If you want the ruthless version:
  **fix B1, B2, B3 and you have addressed most of the real risk.**
- *"You never looked at whether the design is any good."* Correct, and deliberate — you asked an
  accessibility question. But M7 is the note that this cuts both ways: there is no written target
  describing what this theme is *trying* to be, so nine contrast fixes will land against no stated
  intent. Accessibility is a floor. Passing a floor is not a design.

**The thing most likely to bite you that isn't in this review at all:** whichever of these you fix
in the token file will quietly regress the next time someone adjusts the palette, because nothing
in the codebase records *why* a value is what it is. The comment in B3's counter-proposal is the
cheapest possible guard against that, and it is worth more over six months than any single fix here.
