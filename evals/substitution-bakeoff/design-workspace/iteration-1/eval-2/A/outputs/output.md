# Projects page — zero states

**Skill:** `ux-creator` (Phases 1–5), with `ux-reviewer` run as the Phase 4 self-review in a
separate context that never saw the design being made. Both skills' reference checklists
were read before use, not run from memory.

**What was actually done, not just described:** the design was built as HTML at 1440×900 and
390×844, rendered in a browser, and measured — contrast against each element's *real* parent
surface, empty-band percentages, focal area, filled-ink share, touch-target heights. The
independent review measured it again and found four Blockers, three of which were things I
had *claimed* were fine. Those are fixed and re-measured. Every number below came out of the
render.

Files: `outputs/mock/zero-states.html` (six states, desktop) · `outputs/mock/directions.html`
(three directions, phone) · `outputs/mock/zero-states.prereview.html` (kept as the before).

---

## 1. Questions I would have asked, and what I assumed instead

This ran unattended, so these were never put to you. Each one has a branch point; I picked
the more likely answer and named what changes if I picked wrong.

| # | The question | Assumed | If the answer differs |
|---|---|---|---|
| Q1 | What is *inside* a project? | Tasks, files, people | Only two copy strings are keyed to this — trivial to change |
| Q2 | **Do templates exist, or can three be built this cycle?** | Yes, three exist | **The big one.** Without templates, Z1 loses a whole grid row and the trailing empty band grows from 37% to ~62%. The sample card would have to carry that row instead |
| Q3 | Is `/projects` the page users land on right after signup? | Yes | If a wizard runs first, Z1's teaching copy is redundant and should be cut to just the field |
| Q4 | Do most signups arrive as workspace creators, or invited? | Creators | **If mostly invited, Z2 is your volume state**, not Z1, and it deserves the attention Z1 is getting here |
| Q5 | Is the bounce from funnel data, session recordings, or a hunch? | Funnel drop at `/projects` | If it's a hunch, the empty state may be the wrong fix entirely — see Stress test |
| Q6 | Is there an importer (Trello / Asana / CSV)? | No | If yes, "Import" earns a slot and Direction C below becomes viable |

Everything that follows is built on those assumptions. Q2 and Q5 are the two worth answering
before anyone writes code.

---

## 2. The finding underneath the ask

You asked for an empty state. The defect is bigger and cheaper than that: **one string is
doing six different jobs.**

`/projects` renders "No projects" when the user is —

| | State | What "No projects" tells them | What's true |
|---|---|---|---|
| **Z0** | still loading | you have nothing | we haven't asked yet |
| **Z1** | brand new | you have nothing | correct, but useless |
| **Z2** | in a 23-project workspace, on none of them | you have nothing | 23 exist; none include you |
| **Z3** | filtered/searched to zero, owns 14 | **you have nothing** | you have 14 |
| **Z4** | archived everything | you have nothing | 7 are archived |
| **Z5** | the request failed | **you have nothing** | we couldn't reach the server |

Z3 and Z5 tell a user with data that their data is gone. Z5 does it on a network blip. Those
are trust bugs, not polish, and they're the cheapest things on this list to fix — an error
branch and a boolean. Z0 is the sleeper: **an empty state that renders before the response
arrives is the most common manufacturer of false-empty perception**, and it costs one
condition to prevent.

Day-one bounce is the reason this surfaced. It is not the whole defect, and fixing only Z1
leaves the two states that generate support tickets untouched.

---

## 3. Domain brief (condensed)

**Genre:** collection-list page in a self-serve B2B tool — same family as Linear, Notion,
Asana, Figma, Vercel, Airtable. Users arrive carrying strong conventions from those.

**Conventions, split by whether breaking them costs you:**

| Convention | Load-bearing? |
|---|---|
| A primary "New X" affordance is available on the list surface | **Load-bearing** — but on an empty list it may be the body rather than the header |
| Zero state explains the state and offers the next action | **Load-bearing** — the genre trained users to expect it |
| Cards/rows have a stable shape that persists from first project to five-hundredth | **Load-bearing** — teaches the page's permanent geometry |
| Centered illustration + one line + one button | **Habit, and a weak one.** It is the most-copied and least-useful pattern in the genre: the illustration carries no information, appears once, and the user still has to click to get anywhere |
| Sample/demo content seeded on signup | Habit — splits the audience; some read it as help, some as clutter |

**The design opening** is exactly where the genre is laziest: everyone ships the centered
illustration. It is decorative, it appears once per account, and it is visually alien to the
page it sits on, so it teaches the user nothing about the screen they'll live in.

**Session profile:** a first-run session is ~2 minutes and single-purpose. The user has one
piece of work in mind and no vocabulary for the product. They are on desktop (this is a work
tool) but a meaningful minority arrive on a phone from an invite email.

**The page's core moment:** not browsing the list — *creating the thing*. Everything on the
zero-state screen either feeds that or queues behind it.

---

## 4. The contract (DESIGN-TARGETS.md) — PROVISIONAL

**Targets (inferred, would normally be elicited):**

1. **Success:** a day-one user creates a *real* project this session, and that project still
   has activity on day 7. Created-and-abandoned is not success — it moves the activation
   number and nothing else.
2. **Who must love this:** the solo self-serve signup who arrived with one specific piece of
   work in mind and none of our vocabulary. Explicitly *not* the invited teammate (that's Z2,
   a different state) and not the tyre-kicker.
3. **The one feeling:** *"this is mine to fill in"* — the opposite of *"this app is empty, did
   I break something?"*, which is what a bare "No projects" produces.
4. **Constraints:** desktop-primary 1440×900, responsive to 390×844; WCAG 2.1 AA; ships inside
   the existing `/projects` route — no new route, no nav item, no table; the inline create form
   must be the existing New-project form, not a copy.

**Success criteria** (numbered, so the review can score them):

| # | Criterion | Verified by |
|---|---|---|
| C1 | First meaningful action (typing a name) costs 0 navigations and 0 clicks | `autofocus` present on Z1 only |
| C2 | Load → project created in ≤20s | Count interactions: focus(0) + type + 1 click. No dialog, no step 2 |
| C3 | Every zero state has a distinct headline and distinct primary action; none is "No projects" | String table |
| C4 | No state claims the user has nothing when they have something | Counts rendered from unfiltered data, never literals |
| C5 | A **state of the list, not a new surface**: 0 routes, 0 nav items, 0 tables; inline form == dialog form | Scope gate 3-of-5, artifact count |
| C6 | One mechanism per behavior | Count of entry points rendering distinct UI == 1 |
| C7 | **Interior** empty band ≤15% of viewport; **trailing** band ≤40% phone / ≤55% desktop | Measured per state (see note) |
| C8 | One element dominates by **both** area and saturation; the loudest element on screen sits *inside* it, never beside it | Measured area + filled ink |
| C9 | **Does it read as *Workbench*?** 0 decorative illustrations, 0 marketing sentences, and the first interactive element *in the content canvas* makes a project | Reviewer judgment + those three counts |
| C10 | AA against each element's **actual parent surface**; non-text boundaries ≥3:1; targets ≥44px at ≤768px; state change announced | Measured, not asserted |

> **C7 was rewritten after the review, and the rewrite matters.** It originally said "largest
> empty band ≤40%." I passed it on four screens by vertically centering the content — which
> halves one void into two and adds nothing. The review caught that as gaming the metric. The
> criterion now separates the *interior* band (slack pooled **between** content blocks — the
> actual canyon the rule was written about) from *trailing* page bottom under a top-anchored
> layout, which is normal. Measured now: **interior 3.1% on every state**; trailing 37.3%
> (Z1) to 65.6% (Z5). I did not re-centre to make the second number smaller.

**C9 is the criterion the measurable ones can't fake.** A design can satisfy C1–C8 and C10
completely and still be a decorated blank.

**Anti-goals:** no onboarding tour, checklist or wizard · not optimizing for the
browse-before-committing evaluator · not making this screenshot-pretty (it is seen once per
account; the populated grid is seen daily) · **no "Getting started" nav item** · not
redesigning the populated grid in this change.

---

## 5. Three directions, built and measured — then one locked

Each is a real screen at 390×844, not a moodboard. Each gives something up.

| | **A — Workbench** | **B — Showroom** | **C — Route** |
|---|---|---|---|
| **What it is** | The empty state *is* the create form, in the real card shape, in grid slot 1 | A populated read-only sample project rendered exactly as a real card, plus a create slot | Three equal-weight paths: template / import / blank |
| **Sacrifice** | Explains almost nothing about what a project *is*; a confused user types into a box they don't understand | Fake data to seed and maintain; delays creating by one decision; some users feel patronised | Choice paralysis at the moment of least knowledge; needs an importer that doesn't exist |
| **Measured** | interior band **1.4%**, trailing **8.1%**; the only saturated element on screen sits **inside** the focal card | trailing band **45.3%** (fails); focal sample card is **14.6%** of viewport and **0.33× the ink of the header button beside it** — the subject is quieter than the chrome | trailing band **42.3%** (fails); **no saturated element anywhere** — three equal rows cannot have a focal point, by construction |

**Locked: A — Workbench.** Not on taste. B and C both fail C7 and C8 as drawn, and C also
fails Q6. One element is borrowed from B — the sample card, demoted to a ghost in slot 3.

**Coverage split, written before locking (the rule exists because this gets skipped):** of the
six states in this change, 1 is Workbench (Z1) and 5 are the message/skeleton treatment. But
the treatment that covers the most *sessions over the product's life* is the **populated
grid** — seen every day, forever — while Z1 is seen once per account. So the empty state is
drawn in the populated grid's geometry rather than as a visually alien island. That is the
structural reason the create form sits in grid slot 1 in card shape, and the reason this
change introduces no new visual system. **The review then caught that I'd used this argument
to excuse five flat screens**, so Z2–Z5 were rebuilt in Z1's geometry too — same grid, same
card, with slot 3 carrying content each state already knows. The split is now 6 of 6.

---

## 6. The design

### 6.1 Flow — the top job

> *"I just signed up. Get the thing I'm working on into this tool."*

```
signup ──▶ /projects  (Z1)
              │  name field already focused — 0 clicks, 0 navigations
              ├─ type "Q3 website redesign" ──▶ [Create project] ──▶ /projects/:id   (~12s)
              ├─ click a template card ──────▶ /projects/:id pre-filled ──▶ rename inline
              └─ click "Look around" ────────▶ read-only sample ──▶ [Make this mine] ──▶ Z1
```

No step 2, no dialog, no wizard. The page they landed on is the page the project gets made on.

### 6.2 Z1 — First run

**Layout.** Grid row 1: create card spanning columns 1–2; sample ghost card in column 3.
Grid row 2: three template cards. Below: one quiet privacy line. Same 3-column grid the
populated page uses.

**Copy, verbatim:**

- Eyebrow — `YOUR FIRST PROJECT`
- Headline — **What are you working on?**
- Body — *A project holds the tasks, files and notes for one piece of work. Most people start with whatever is on their desk today — you can rename it later.*
- Field — placeholder `e.g. Q3 website redesign`, **autofocused**, 44px
- Primary — **Create project**
- Link line — *Not sure where to start? Three templates are below.*
- Sample ghost card — `Website redesign` `SAMPLE` · *12 tasks · 3 files · 2 people* · *Read-only. Disappears the moment you make your own.* · **Look around** button, with **×** to remove at the card's top-right, away from it
- Template cards — each names what it actually contains, not just a category:
  - **Content calendar** — *Weekly slots, draft → review → live, one owner per post*
  - **Product launch** — *Launch date, 6 workstreams, go / no-go checklist*
  - **Client retainer** — *Monthly cycle, hours budget, deliverables log*
- Footnote — *Projects you create are private to you until you invite someone.* (answers the question every day-one user in a shared workspace actually has, and nobody asks out loud)

**The header "New project" button does not render on Z1.** The create surface is already
open in slot 1; a second door to the same room, sitting in the highest-salience position on
the page and producing no visible change when clicked, is worse than no door.

**Measured:** interior band 3.1%, trailing 37.3%; focal card 19.8% of the content canvas; the
largest filled element on the entire screen is the `Create project` button — **inside** the
focal card, not beside it. On the phone: interior 1.4%, trailing 8.1%, zero targets under 44px.

### 6.3 The other five states

Every one uses Z1's geometry: same grid, focal card in slots 1–2, and **slot 3 carrying
something the state already knows** — which is what stops them being five flat screens.

**Z0 — Loading.** Six skeleton cards in the real grid shape, top-aligned so they sit exactly
where the content will land. No spinner, no text.
> **Hard rule, and the cheapest win in this document:** the empty state renders **only** after
> a settled, non-error response with `count === 0` **and** no active filters. In plain English:
> don't tell someone their list is empty until you've actually heard back from the server and
> confirmed they aren't filtering. One condition; prevents a whole class of false alarm.

**Z2 — Member of a populated workspace, on none of it.**
Headline **You're not on any of Acme's projects yet** · *Acme has 23 projects, but none of
them include you. You don't have to wait — anything you create is yours, and you can invite
people into it later.* · Primary **Create my own project** · Secondary **Ask Dana for access**
(resolves inline to `Request sent to Dana · 2:14pm`). Slot 3: *Who can add you* — Dana Levy
(Owner), Ron Cohen (Admin), Maya Barak (Admin).
The primary is *create*, not *ask*, because Target 1 defines success as **this** user creating
something — making the primary action a request hands their activation to someone else's inbox.

**Z3 — Filtered or searched to nothing, user owns 14.**
Filter chips stay visible, each individually removable. Headline **Nothing matches all three
filters at once** · eyebrow `14 PROJECTS · 0 SHOWN` · *Your projects are all still here — this
is a filter result, not an empty account. Loosening any one of the three brings some of them
back.* · Primary **Show all 14 projects** · Secondary **Drop "Owner: me" — 3 match**. Slot 3:
*Loosen one filter* — drop "Owner: me" → 3 match; drop "Status: active" → 5 match; drop
"redesign" → 9 match.
The count is read from the unfiltered total. The near-miss numbers are what turn a dead end
into a next action — and they are now **clickable**, which they weren't in my first draft.

**Z4 — Returning user, everything archived.**
Headline **Nothing active right now** · *All 7 of your projects are archived. The most recent
was "Spring campaign", archived 4 days ago.* · Primary **View archived (7)** · Secondary
**Restore "Spring campaign"**. Slot 3: the three most recently archived.
**No teaching copy.** This user knows what a project is; showing them Z1's onboarding would
be insulting.

**Z5 — The list failed to load.**
Warm surface **plus an icon** — not colour alone, and the tint alone is only 1.05:1 against
the page in greyscale, so the icon is load-bearing, not decoration. Headline **We couldn't
load your projects** · *Your projects are safe — this is a connection problem on our side, not
missing data. Last loaded 2 minutes ago.* · Primary **Try again** · Secondary **Show last
loaded list**. Slot 3: the cached list, dimmed, under its own "Last loaded · 2 min ago" label
— so the stale data is visibly stale rather than re-creating the trust bug one click later.

**Copy rules applied throughout:** every headline names the state's actual cause and is
reusable by no other state · every button says what happens (`View archived (7)`, never `OK`)
· every count comes from data, never from the string.

### 6.4 Scope gate (3-of-5), scored against the nearest existing surface

Nearest surface: the `/projects` list route itself, plus the existing New-project form.

| # | | |
|---|---|---|
| 1 | Variation of existing UI? | **Yes** — it's a render state of the list |
| 2 | Duplicates ≥70% of an existing flow? | **Yes, if built naively** — the inline card's fields are the New-project form's fields |
| 3 | New vocabulary? | No — project, template, sample, archived |
| 4 | Could a mode/toggle carry it? | **It *is* the mode** — this is the list's zero mode |
| 5 | Splits one job across two places? | **Risk** — header button + inline card are two doors to one job |

**Score: 3 soft-yes — so the flags land on my own design.**

- **(2) → the inline create card must BE the New-project form component, mounted inline** —
  one component, two mounts (`inline` | `dialog`). If engineering writes a second form, this
  ships the exact defect the review exists to catch. In plain English: the box you type into
  on the empty page and the box in the "New project" pop-up should be the *same piece of
  code*, shown in two places — not two boxes that happen to look alike and drift apart.
- **(5) → one mechanism.** Resolved by removing the header button on Z1 entirely.

**Artifacts added: 0 routes, 0 nav items, 0 tables, 0 new components.** One new prop on the
existing form (`variant="inline"`) — and if that would be its third-plus boolean flag, extract
`ProjectForm.Fields` and compose instead. Piling flags onto one component is how a simple
form becomes unmaintainable.

### 6.5 Accessibility, measured rather than asserted

- **Every text run measured against its actual computed parent surface**, not the page ground.
  Across all six states: **0 runs below 4.5:1**. On the phone direction: 0 below 4.5:1.
- Non-text: the sample card's dashed boundary is **3.28:1** against the ground and 3.58:1
  against its fill — it clears SC 1.4.11, which a 1.5px dash on bare ground did not.
- Targets: `Create project` and the name field are 44px; the phone frame has **zero** targets
  under 44px. Desktop header buttons and filter-chip `×` render 36px, which is the desktop
  norm — the ≥44px rule applies at ≤768px and is met there.
- Focus: `autofocus` on **Z1 only**. Auto-focusing on Z3/Z4/Z5 would hijack the keyboard of
  someone who came to do something else.
- Announcement: a visually-hidden `aria-live="polite"` sentence per state — **not** on the
  grid. A live region wrapping the grid would read all 14 projects aloud when a filter clears.
  Z5 uses `role="alert"`.
- Real `<button>` and `<input>` elements throughout, so focus order, focus ring, Esc and
  keyboard operation are *testable* rather than promised.

### 6.6 Instrumentation, with kill-triggers written before ship

Fire on Z1: `empty_state_shown`, `name_field_focused`, `first_keystroke`,
`project_created{source: blank|template|sample}`, `sample_opened`, `sample_removed`, and
**`abandoned_with_text`** — typed a name and never submitted, the highest-signal event here.
**Kill the sample card if `sample_opened` < 5%. Kill the template row if template-started
< 10%.** Both have a delete condition authored in advance, so neither becomes permanent
furniture by default.

### 6.7 If the budget is one day

In order. The first two are most of the value and neither is a design problem:

1. **Z5 and Z0** — stop rendering "no data" when the truth is "no answer yet". One boolean,
   one error branch. Trust fix, nearly free.
2. **Z3** — different string, true count, filters left visible. ~30 minutes.
3. **Z1 create card** — inline form in slot 1, autofocused.
4. Templates, sample card, Z2, Z4.

---

## 7. Independent review (Phase 4) — and what it changed

`ux-reviewer` was run in a fresh context that had not created the design, against the contract
above, with instructions to render the build and verify my claimed numbers rather than believe
them. **Verdict: fix-then-ship. 4 Blockers, 8 Majors, 12 Catches at the cap, 1 truncated
Major disclosed.** It was right about all four Blockers, and three of them were things I had
already declared fixed or fine.

| Finding | What it actually was | Status |
|---|---|---|
| **B1 · Blocker** | The phone placeholder was still **3.09:1** — and my spec described it in the past tense as a defect already caught. The fix had landed in one of two files | **Fixed.** Now 5.97:1; 0 text below AA in either file |
| **B2 · Blocker** | I wrote "≥44px unverified, the mock renders desktop only." The mock rendered 390×844 and **failed** — sample links at 18.8px, chips at 32px. I declined to measure a file I had already built | **Fixed.** 0 targets under 44px on the phone frame |
| **B3 · Blocker** | C8 failed on 4 of 6 states, and I'd only *scored* it on the one where it passed. 5 of 6 screens were the flattest treatment — and I used the "populated grid is the real coverage" argument to excuse it | **Fixed.** Z2–Z5 rebuilt in Z1's geometry with a companion card in slot 3; focal now out-inks everything outside it on all five |
| **B4 · Blocker** | Z3 had two buttons producing the same result, and no button for the genuinely useful move — which was reachable only via an 8.7×18.8px `×` | **Fixed.** One control per outcome; the near-miss is now the secondary action and a clickable list |
| **M1** | Loading skeletons sat 230px below where real content lands | Fixed — canvas is top-aligned everywhere |
| **M2** | Z2's primary handed the user's activation to someone else's inbox | Fixed — create is primary, ask is secondary with inline resolution |
| **M3** | The Z1 header button was a no-op | Fixed — it doesn't render on Z1 |
| **M4** | Z5's promised icon didn't exist, and the warm tint was 1.005:1 — invisible in greyscale | Fixed — icon shipped, tint darkened |
| **M5** | Zero `<button>`, zero `<input>`, zero ARIA in 319 lines. Four criteria were prose assertions inside the artifact built to stop prose assertions | Fixed — real semantics, 24 buttons, 7 inputs, 6 live regions |
| **M6** | `aria-live` on the whole canvas would read the entire grid aloud | Fixed — one hidden sentence per state |
| **M7** | Destructive "Remove" 16px from "Look around", identical styling, on the only card with no surface (1.57:1 boundary) | Fixed — filled surface, 3.28:1 dash, × moved to top-right |
| **M8** | The locked direction degraded templates to content-free chips on the phone, contradicting the spec's own rule | Fixed — stacked 44px rows reusing the desktop description strings verbatim |

**It also corrected the contract, not just the design** — C7 was measuring something that
could be improved by centering (see §4), C9's third count was unsatisfiable on any layout with
a sidebar, and C10 checked only text contrast, so it structurally could not see the 1.57:1
boundary in M7. Those are amended above.

**Not fixed, deliberately:**

- **Trailing empty band on Z2–Z5 is 59.8–65.6%.** Re-centering would halve the number and add
  nothing — which is exactly what the review caught the first time. Interior band is 3.1%
  everywhere, and that is the defect the rule was written about. Flagged rather than gamed.
- **C5's load-bearing half — "inline form == dialog form" — is unverifiable.** There is no
  codebase here. This is the criterion the whole scope gate turns on, and it is an instruction
  to engineering, not something I proved.
- **Z2–Z5 were never rendered at 390×844.** A 640px card needs a different layout at phone
  width; C7 and C8 are unmeasured there.

---

## 8. Stress test

**The weakest thing here.** Every number in §4's metrics matrix has an unknown baseline. "≥60%
signup→first-project" is a target invented against a number nobody has told me. A target with
no baseline can't be passed or failed, which makes the whole matrix decorative until someone
fills in today's figures.

**The assumption most likely to be wrong.** Q5 — that the bounce is visible in a funnel. If
"users bounce" is a hunch from watching two demos, then the empty state is a *symptom surface*
and this whole document is a well-measured answer to the wrong question. Day-one bounce on a
projects page is at least as often caused by value-prop mismatch at signup, a verification
email in the way, or an invite flow that dropped the user somewhere they had no business being.
**The instrumentation in §6.6 is the honest hedge**: it is deliberately cheap and it tells you
within a week whether the empty state was ever the constraint.

**What a smart critic would say.** Three things, and two of them land:

1. *"You've turned a one-line ask into six states and a template library. That's scope creep
   wearing a checklist."* — Partly fair. The counter is §6.7: the ordering puts Z5 and Z0
   first, and both are error-handling fixes measured in hours. If only items 1 and 2 ship, the
   two states that tell users their data is gone are fixed and nothing else changed. The
   templates and the sample card are genuinely optional and both have kill-triggers.
2. *"The sample project is the thing you'll regret."* — Probably right. Seeded fake data
   ages badly, confuses a fraction of users, and is one more thing to maintain. It's in because
   Direction B measured a real virtue (you see the destination before committing), but it is
   the first thing I'd cut, and it is the only element here with a <5% kill-trigger on it.
3. *"Removing the header button on Z1 breaks muscle memory."* — This one I'd push back on.
   There is no muscle memory on a user's first-ever page view, which is the only state where it
   is removed. But it is a one-line revert if the team disagrees.

**What would change my mind fastest.** If Q4's answer is "most of our signups arrive invited,"
then Z2 — not Z1 — is the volume state, and the emphasis in this document is misallocated. Z2
currently gets one card and a people list; it would deserve what Z1 got. That is a one-question
check and worth doing before any of this is built.

---

## 9. Evidence

| Claim | Measured | Where |
|---|---|---|
| 0 text runs below 4.5:1, against real parent surfaces | 51 runs checked, 0 failures | both mocks, `getComputedStyle` + contrast calc |
| Sample-card boundary clears 3:1 | 3.28:1 vs ground, 3.58:1 vs fill | `zero-states.html` |
| Interior empty band | 3.1% desktop (all states), 1.4% phone | per-state gap scan of laid-out elements |
| Trailing band | Z1 37.3%; Z2–Z5 59.8–65.6%; phone 8.1% | same scan |
| Focal out-inks everything outside it | true on Z1–Z5 (Z1: 5,183 vs 545) | filled-area × saturation |
| Distinct headlines, none "No projects" | 5 distinct; Z0 correctly has none | string extraction |
| One primary action per state | 1 on each of Z1–Z5 | DOM count |
| Phone targets ≥44px | 0 under 44px | `getBoundingClientRect` |
| 0 new routes / nav items / tables | sidebar byte-identical across all 6 frames | confirmed by the reviewer |

Not measured, and therefore not claimed: anything at 390×844 for Z2–Z5; real screen-reader
behaviour; real keyboard traversal; and whether the inline form is the same component as the
dialog, which has no codebase to check against.
