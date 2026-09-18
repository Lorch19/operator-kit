# Projects Page — Empty State

**Skills run:** `design-tools/design-critique` (on the current state), `design-tools/ux-copy` (the copy itself), `design-tools/accessibility-review` (on the proposed design), `design-tools/design-handoff` (build spec). Run in that order — critique establishes *why* it fails, copy and spec fix it, a11y gates it.

---

## Questions I would have asked (and the answers I'm assuming)

This ran unattended, so here are the questions that would actually have changed the design, with the assumption I proceeded on. **Check the starred ones before building — they change the shape of the fix, not just the wording.**

| # | Question | Assumption I proceeded on | Changes what? |
|---|---|---|---|
| 1 | ★ Is the page *genuinely* empty, or is the loading/error state rendering as "No projects"? | It is genuinely empty, but I have specced the loading/error separation anyway because this is the single most common cause of a day-one bounce that looks like an empty-state problem. | Whether this is a copy job or a bug. See Finding U-1. |
| 2 | ★ Can every user who lands here create a project? (seats, roles, viewer-only, invited-to-org-not-to-project) | Most can; a minority cannot. I've specced a permission-aware variant. | Showing a CTA a user can't action is worse than "No projects". |
| 3 | ★ Do you have templates, an importer, or a sample/demo project today? | You have none of them yet. The primary path works alone; templates/import/sample are specced as progressive adds with a build order. | How many secondary paths ship in v1. |
| 4 | What *is* a project in your product — a workspace, a doc container, a client engagement, a build? | Generic container for work + files + collaborators. Copy has a single domain-specific line called out for you to swap. | One sentence of body copy. |
| 5 | Is "bounce" measured, or inferred? What's the current day-1 project-creation rate? | Inferred from behaviour, not instrumented. I've specced the events and the baseline you need. | Whether you can tell if this worked. |
| 6 | Design system in place? Token names? | A conventional token set exists; I've used generic names (`--space-4`, `--color-text-secondary`) with concrete fallback values so the spec is buildable either way. | Token names only. |
| 7 | Desktop-first or mobile-heavy? | Desktop-primary, mobile supported. Both layouts specced. | Layout order, not content. |
| 8 | Brand voice? | Plain, competent, warm-but-not-cute. Four tone variants provided if that's wrong. | Which copy row you pick. |

Everything below is delivered in full under those assumptions.

---

# Part 1 — Design Critique: Current Projects Empty State

**Artifact reviewed:** described only — the projects page renders the string "No projects" when the user has none. No screenshot available, so this critiques the *pattern*, not pixel execution.

### Overall Impression

"No projects" is a **null state**, not an empty state. It's a database fact rendered as UI. It answers the one question the user did not ask ("how many projects do I have?") and none of the three they did: *what is this page for, why is it blank, and what do I do now?*

The bounce is not a motivation problem. A day-one user who signed up is, by definition, motivated — they already did the hardest thing. They're bouncing because the page terminates the flow. Signup hands them a door, the door opens onto an empty room with a label on the wall, and there is no next affordance in their line of sight. The most valuable real estate in the product — the first screen after activation, with the user's attention at its lifetime peak — is currently spending 11 characters of it.

**Biggest opportunity:** the empty projects page is not a degraded version of the projects page. For a day-one user it *is* the onboarding. Treat it as a designed screen with a job, not as a fallback.

### Usability

| Finding | Severity | Recommendation |
|---|---|---|
| **U-1. "No projects" may be rendering for loading and error states too.** If the fetch is slow or fails, most implementations fall through to the same zero-length-array branch. A user who *has* projects sees "No projects" and concludes their data is gone; a user with a failed fetch gets no retry. This alone can produce the bounce you're seeing, and no amount of copy fixes it. | **Critical** | Split into four explicit states: `loading` → skeleton; `error` → error + Retry; `empty-first-run` → onboarding; `empty-filtered` → clear-filters. Never render an empty state until data has resolved successfully. Verify this first — it's cheap and it may be the whole bug. |
| **U-2. No next action in the user's focus.** The only way forward is a header "+ New project" button at the top-right — outside the user's gaze, which is centred on the message they were just given. The message and the action are in different places. | **Critical** | Put the primary CTA inside the empty-state block, centred, directly under the headline. Line of sight = line of action. |
| **U-3. Zero-commitment path is missing.** "Create a project" is a commitment: name it, maybe invite people, maybe pick settings. A day-one evaluator who hasn't decided you're worth it yet will not pay that cost to find out what's behind it. This is the classic chicken-and-egg: value is locked behind setup, setup is justified by value. | **Major** | Offer a look-before-you-leap path: a sample/demo project, or a template that prefills everything. The user should be able to *see* a populated project in one click with nothing to fill in. |
| **U-4. Nothing teaches what a populated page looks like.** The user cannot form a mental model of what success looks like, so "create a project" has no imagined payoff. | **Major** | Show ghost/placeholder project cards behind the panel (static, non-animated, aria-hidden). It costs nothing and makes the shape of the filled page legible. |
| **U-5. Filtered-empty and truly-empty almost certainly share this string.** A user who types a search with no match gets "No projects" and reasonably concludes their projects were deleted. | **Major** | Separate copy + a "Clear filters" action for the filtered case. Never show onboarding content on a filtered empty result. |
| **U-6. No permission-awareness.** If viewer-role or unseated users land here, a "Create a project" CTA either fails or opens an upgrade wall — both worse than silence. | **Major** | Permission-gated variant with a different action ("Ask your admin for access", "Request a seat"). |
| **U-7. No sense of effort or scope.** The user doesn't know if creating a project is a 30-second act or a 20-minute configuration. Unknown cost is assumed high. | **Minor** | State the cost if it's honestly low ("takes about a minute"). Delete the claim if it isn't true — a broken promise here is worse than no promise. |

### Visual Hierarchy

- **Eye draws to:** the words "No projects", because it's the only content on the screen. **Is that correct?** No. The eye should land on the action. Right now the most prominent element is a statement of absence — the page's emotional peak is a negative.
- **Reading flow:** starts at "No projects", terminates immediately. There is no second element to move to, so the flow exits the page. A well-formed empty state has a three-beat flow: *orient* (what this is) → *explain* (why it's blank) → *act* (do this now). The current design has one beat, and it's the least useful of the three.
- **Whitespace:** a large empty region with a small centred string reads as "broken" or "still loading" rather than "ready for you". Whitespace amplifies whatever it surrounds; here it amplifies nothing.
- **Fix:** invert the hierarchy. Largest element = headline that is an *invitation*, not a *count*. Highest-contrast element = the primary button. The statement of emptiness disappears entirely — the user can see the page is empty; they don't need to be told.

### Consistency Issues

| Element | Issue | Fix |
|---|---|---|
| Header "+ New project" vs. empty-state CTA | Two identically-styled primary buttons doing the same job splits attention and creates a "which one is the real one?" pause. | While the empty state is shown, demote the header button to secondary/ghost. Restore it to primary once ≥1 project exists. |
| CTA verb | "New project" (header) vs. "Create project" (likely elsewhere, e.g. modal title) vs. "Add project" | Pick one verb and use it everywhere. Recommendation: **Create**. "New" is an adjective pretending to be a verb; "Add" implies something that already exists elsewhere. |
| Noun casing | "project" vs. "Project" as a product concept | Lowercase in prose, sentence case in UI labels. Decide once and put it in the voice guide. |
| Empty-state pattern | If other zero-states in the product (team, files, integrations) each improvise, users relearn the pattern every time. | Build this as a reusable `<EmptyState>` component with icon / title / description / primary / secondary / footer-link slots, and migrate the others. |

### What Works Well

- It's honest and it's short. Whatever replaces it must not become a wall of onboarding text — the failure mode on the other side of this fix is a paragraph nobody reads.
- The page presumably keeps its header and navigation, so the user isn't trapped. Preserve that; a full-bleed takeover empty state that hides the nav would trade one bounce cause for another.
- Zero-state exists at all and doesn't crash. Low bar, but plenty of products ship a blank white rectangle here.

### Priority Recommendations

1. **Verify the loading/error fall-through (U-1) before designing anything.** If the empty state is being shown to users who aren't empty, that's your bounce and it's a one-line fix.
2. **Move the primary CTA into the user's line of sight and make it the visually dominant element (U-2).**
3. **Add one zero-commitment path — sample project or prefilled template (U-3).** This is the single highest-leverage anti-bounce move for evaluators.
4. **Split the four states properly: loading / error / first-run empty / filtered empty (U-1, U-5).**
5. **Add the permission-aware variant (U-6)** so you never show an action the user can't take.

---

# Part 2 — UX Copy: Projects Empty State

**Pattern applied:** *what this is + why it's empty + how to start*. **User state:** day one, just signed up, high intent but low investment, no mental model of your product's object model, actively deciding whether to keep going. **Tone target:** plain, competent, warm; zero exclamation marks; no "Oops!", no "Looks like it's empty in here".

### Recommended Copy — Variant A: First-run (0 projects, never had one)

**Headline (25 chars):**
> Create your first project

**Body (118 chars):**
> A project holds your work, files, and teammates in one place. Setting up your first one takes about a minute.

> **Swap this line for your domain.** The body's job is to define the noun, and only you know what a project *is* here. Keep it to one sentence, ≤140 characters, and name concrete things the user will recognise:
> - Client/agency work: "A project is one client engagement — briefs, deliverables, and everyone working on it in one place."
> - Dev tool: "A project connects a repo to your builds, environments, and logs."
> - Design/creative: "A project holds your files, versions, and the people reviewing them."

**Primary CTA (16 chars):**
> Create a project

**Secondary CTA (21 chars):**
> Start from a template

**Footer link (30 chars):**
> Just looking? Explore a sample

> If you have neither templates nor a sample project yet, **ship the headline + body + primary CTA alone.** That is already a large improvement over "No projects". Do not invent a secondary path just to fill the slot — two weak actions convert worse than one clear one.

### Recommended Copy — Variant B: Filtered / search, no results

**Headline:** No projects match "{query}"
**Body:** Try a different search, or clear your filters to see everything.
**Primary:** Clear filters
**Secondary:** *(none)*

> Critical rule: **never** show first-run onboarding copy here. A user with 40 projects who mistypes a search must not be told to create their first project.

### Recommended Copy — Variant C: Returning user, genuinely zero (all archived/deleted)

**Headline:** No active projects
**Body:** Everything here has been archived. You can bring one back or start something new.
**Primary:** Create a project
**Secondary:** View archived (12)

> Same emptiness, different user — this person already knows what a project is. Explaining it again reads as condescending and wastes their time.

### Recommended Copy — Variant D: No permission to create

**Headline:** Nothing shared with you yet
**Body:** Projects you're added to will appear here. Ask an admin to add you to one.
**Primary:** Request access *(only if you can actually route the request; otherwise omit and show no button)*
**Secondary:** *(none)*

### Alternatives

| Option | Headline | Body | Primary CTA | Tone | Best for |
|---|---|---|---|---|---|
| **A1 (recommended)** | Create your first project | A project holds your work, files, and teammates in one place. Setting up your first one takes about a minute. | Create a project | Plain, low-friction | Default. Safe across B2B and prosumer. |
| **A2** | Start your first project | Projects are where your work lives. Make one and invite your team, or explore a sample first. | Create a project | Warm, guided | Non-technical users, first-time category buyers |
| **A3** | This is where your projects will live | Nothing here yet. Create one to bring your work, files, and teammates together. | Create a project | Orienting, spatial | Products where "project" is an unfamiliar or novel concept |
| **A4** | Your work starts with a project | Every file, task, and teammate in {Product} lives inside a project. Create one to begin. | Create a project | Outcome-led, slightly formal | Enterprise, procurement-driven buyers |
| **A5** | Ready when you are | Create a project to get going — or poke around a sample one first. | Create a project | Playful, light | Consumer/prosumer, strong personality brands. **Use only if your voice is genuinely this.** Playful copy on a confused user reads as smug. |

**CTA alternatives, ranked:**

| CTA | Verdict |
|---|---|
| **Create a project** | ✅ Recommended. Verb-first, specific, names the object, matches what happens next. |
| Create project | Acceptable. Terser; slightly more "system" than "human". Fine if your product voice is compact. |
| New project | ❌ Not a verb. Weak call to action. Keep it in the header where it's a label, not a summons. |
| Get started | ❌ Says nothing about what will happen. Generic CTAs reliably underperform specific ones. |
| Add project | ❌ Implies moving something that already exists into this page. |
| Create your first project | ❌ Redundant with the headline, and too long for a button. |

### Rationale

- **The headline is an imperative, not a status.** "Create your first project" does three jobs at once: it names the object (orientation), implies the page is empty by design (explanation), and states the action (direction). "No projects" does one of those, badly. The word **"first"** matters — it frames emptiness as a normal starting point rather than a failure, and it quietly promises there will be a second.
- **The page no longer says it's empty.** The user can see that. Spending the largest type on a negative fact is the core mistake; the replacement spends it on an invitation.
- **The body defines the noun.** A day-one user doesn't know what your "project" contains or why they'd want one. Listing two or three concrete things it holds ("work, files, teammates") builds the mental model in one line and makes the CTA's payoff imaginable.
- **"Takes about a minute" prices the action.** Unknown effort is assumed expensive, and assumed-expensive actions get deferred — and deferral on day one is the bounce. **Only ship this clause if it's true.** If project creation involves a six-field form or an integration connect, cut the clause; an under-delivered promise on the first action is a worse outcome than silence.
- **"Just looking? Explore a sample" names the user's actual state.** A meaningful share of day-one traffic is evaluating, not adopting. Giving that user a legitimate low-cost path keeps them on the page instead of sending them to the back button. It also converts later: a user who has seen a populated project has a reason to create a real one.
- **One primary action only.** Empty states that offer four equal-weight options reproduce the paralysis they're meant to cure. One primary button, one secondary, one text link — a clear descending weight.
- **No "Oops", no exclamation marks, no empty-desert metaphors.** Nothing has gone wrong; apologising for a normal state invents a problem. Jokes cost the user a parse and return nothing.

### Localization Notes

- **Do not concatenate.** Variant B's headline must be one interpolated string — `No projects match "{query}"` — not `"No projects match" + query`. Word order varies by language.
- **Expect +35% length** for German/Finnish. Headline must wrap to two lines without clipping; the container cannot be fixed-height.
- **Button labels must not be width-constrained.** "Create a project" → "Ein Projekt erstellen" (+38%). Buttons are `width: auto` with `min-width`, never fixed; the two CTAs stack vertically below the tablet breakpoint.
- **"Project" may already be a translated product-level term.** Use your existing glossary entry — do not let the translator re-decide it here, or the empty state will use one word while the nav uses another.
- **Variant C's "View archived (12)"** — the count is a separate interpolated variable and needs plural forms (many languages have more than two).
- **"Just looking?"** is idiomatic and translates poorly. Give translators an explicit note: *intent = "if you are only evaluating and not ready to commit"; do not translate literally.*
- **RTL:** the layout is centred and symmetric so it mirrors cleanly, but the footer-link arrow `→` must flip to `←`. Use a logical-property icon or CSS `transform: scaleX(-1)` under `[dir="rtl"]`.

---

# Part 3 — Accessibility Audit: Proposed Empty State

**Standard:** WCAG 2.1 AA. Audited against the proposed design (Part 4 spec), not the current page.

### Summary

**Issues:** 7 | **Critical:** 2 | **Major:** 3 | **Minor:** 2

These are the issues the proposed design will have **if built naively** — this is a pre-emptive audit so they get designed out rather than retrofitted.

### Findings

| # | Issue | WCAG | Severity | Fix |
|---|---|---|---|---|
| A-1 | Empty state replaces page content dynamically after data loads. Screen-reader users get no announcement — the page just goes quiet and they may believe it's still loading. | 4.1.2, 1.3.1 | **Critical** | Wrap the empty-state block in `role="status"` `aria-live="polite"`. Announce once when it mounts. Do not put `aria-live` on the whole list container or every render churns the buffer. |
| A-2 | Ghost/skeleton placeholder cards behind the panel are read by screen readers as real (empty) project cards, and read by low-vision users as broken content. | 1.1.1, 1.3.1 | **Critical** | `aria-hidden="true"` + `pointer-events: none` on the ghost layer. It is decoration. Additionally: **do not animate it** — a shimmer reads as "loading", which contradicts the message. |
| A-3 | Decorative icon/illustration above the headline exposed to AT with no alt or, worse, a meaningless filename. | 1.1.1 | Major | Inline SVG with `aria-hidden="true"` and `focusable="false"`. The headline carries the meaning; the icon carries none. If you replace it with an illustration that *does* carry meaning, give it a real `alt`. |
| A-4 | Default `gray-300` (#D1D5DB) border on the secondary outline button against a white surface = **1.47:1**, below the 3:1 required for UI component boundaries. | 1.4.11 | Major | Use `#6B7280` (gray-500) for the secondary button border → **4.83:1**. `gray-400` (#9CA3AF) is **2.54:1** and also fails — this is the common wrong fix. |
| A-5 | Focus lands nowhere useful when the empty state renders, so keyboard users must tab from the top of the document past all nav to reach the CTA. | 2.4.3 | Major | Do **not** auto-focus the button (that's an unexpected context change, 3.2.1, and it hijacks screen-reader reading order). Instead: give the empty-state block `tabindex="-1"` and ensure the skip-link / main-content landmark targets it, so the CTA is the first interactive element inside `<main>`. |
| A-6 | Touch targets: a text-only footer link ("Just looking? Explore a sample") is typically ~20px tall. | 2.5.5 | Minor | Min 44×44px hit area on mobile via padding (visual size can stay small). *Accuracy note: 2.5.5 Target Size (44px) is Level AAA in WCAG 2.1; the AA requirement is WCAG 2.2's 2.5.8 at 24×24px. The skill's checklist uses 44px — that's the stricter, better target and costs nothing here.* |
| A-7 | Secondary/footer link distinguished from body text by colour alone. | 1.4.1 | Minor | Add underline (or underline-on-hover plus a non-colour cue such as the trailing arrow, which is present here). |

### Color Contrast

Values computed for the proposed palette on a white (`#FFFFFF`) surface. Substitute your own tokens and re-check — do not assume your existing greys pass.

| Element | FG | BG | Ratio | Required | Pass? |
|---|---|---|---|---|---|
| Headline (24px semibold) | `#111827` | `#FFFFFF` | **17.74:1** | 3:1 (large) | ✅ |
| Body text (15px regular) | `#4B5563` | `#FFFFFF` | **7.56:1** | 4.5:1 | ✅ |
| Footer link text (14px) | `#4F46E5` | `#FFFFFF` | **6.29:1** | 4.5:1 | ✅ |
| Primary button label | `#FFFFFF` | `#4F46E5` | **6.29:1** | 4.5:1 | ✅ |
| Secondary button label | `#111827` | `#FFFFFF` | **17.74:1** | 4.5:1 | ✅ |
| Secondary button **border** | `#D1D5DB` | `#FFFFFF` | **1.47:1** | 3:1 | ❌ → use `#6B7280` (**4.83:1**) |
| Muted helper text if used (15px) | `#6B7280` | `#FFFFFF` | **4.83:1** | 4.5:1 | ✅ (no margin — don't go lighter) |
| Focus ring | `#4F46E5` | `#FFFFFF` | **6.29:1** | 3:1 | ✅ |
| Ghost cards | `#F3F4F6` | `#FFFFFF` | ~1.1:1 | n/a | ✅ decorative only, `aria-hidden` |

**Dark mode:** re-run every row. Inverting a light palette by swapping tokens routinely breaks the primary button — `#4F46E5` on a dark surface loses contrast against white label text in one direction and against the surface in the other. Test both.

### Keyboard Navigation

| Element | Tab order | Enter/Space | Escape |
|---|---|---|---|
| Skip link → `<main>` | 0 | Moves focus to the empty-state container | n/a |
| Primary "Create a project" | 1 | Opens create flow; focus moves to first field in the modal/page | n/a (focus is in the empty state, nothing to dismiss) |
| Secondary "Start from a template" | 2 | Opens template picker; focus to first template | Closes picker, returns focus to the secondary button |
| Footer "Explore a sample" | 3 | Opens sample project | n/a |
| Ghost cards | — | Not focusable (`aria-hidden`, no tabindex) | — |

- Visible focus indicator on all three: 2px solid `#4F46E5`, 2px offset. Never `outline: none` without a replacement (2.4.7).
- When the create modal opens: trap focus inside it, and on close return focus to the button that opened it. A modal that dumps focus back to `<body>` strands keyboard users at the top of the document.

### Additional checks

- **Zoom to 200%:** the centred panel must reflow, not clip. Use `max-width: 480px` with `%`-based margins; no fixed pixel heights anywhere in the block. At 320px-equivalent width, buttons stack (1.4.10 Reflow).
- **`prefers-reduced-motion`:** if you add any entrance transition, disable it under the media query. The ghost layer is static by spec, so nothing else moves.
- **Semantic structure:** headline is an `<h2>` (the page `<h1>` is "Projects"). Don't use a styled `<div>` — heading navigation is how screen-reader users scan a page.
- **Buttons vs links:** "Create a project" and "Start from a template" are `<button>` if they open in-page UI, `<a>` if they navigate. "Explore a sample" navigates → `<a>`. Getting this wrong breaks expected keyboard behaviour (Space vs Enter) and AT role announcement.

### Priority Fixes

1. **A-1** — `role="status"` / `aria-live="polite"` so the state change is announced.
2. **A-2** — `aria-hidden` the ghost layer and keep it unanimated.
3. **A-4** — secondary border to `#6B7280`; this one silently ships broken in most design systems.
4. **A-5** — main-landmark focus target, no auto-focus.
5. **A-3, A-6, A-7** — icon hidden, 44px hit areas, links not colour-only.

---

# Part 4 — Handoff Spec: Projects Empty State

### Layout

**Desktop (≥1024px)**

```
┌────────────────────────────────────────────────────────────────┐
│  Projects                                    [ New project ]   │  ← page header stays
│                                                 (ghost/secondary
│                                                  while empty)
├────────────────────────────────────────────────────────────────┤
│                                                                │
│    ░░░░░░░░░░░░   ░░░░░░░░░░░░   ░░░░░░░░░░░░                  │  ← ghost cards
│    ░░░░░░░░░░░░   ░░░░░░░░░░░░   ░░░░░░░░░░░░     (static,     │
│                                                    aria-hidden)│
│         ┌────────────────────────────────────────┐             │
│         │                 ◇                      │             │
│         │      Create your first project         │  ← h2 24px  │
│         │                                        │             │
│         │  A project holds your work, files, and │  ← 15px     │
│         │  teammates in one place. Setting up    │     max 2   │
│         │  your first one takes about a minute.  │     lines   │
│         │                                        │             │
│         │  [ Create a project ] [ Start from a   │             │
│         │                         template ]     │             │
│         │                                        │             │
│         │      Just looking? Explore a sample →  │             │
│         └────────────────────────────────────────┘             │
│                                                                │
│    ░░░░░░░░░░░░   ░░░░░░░░░░░░   ░░░░░░░░░░░░                  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

- Panel `max-width: 480px`, horizontally centred, vertically positioned at ~38% of the available content height (optical centre — true vertical centring sits too low and reads as floating).
- Ghost cards use the **real** project-card grid and dimensions, so the user is seeing the actual future shape of the page.

**Mobile (<768px)**

```
┌──────────────────────────┐
│ Projects            [+]  │
├──────────────────────────┤
│   ░░░░░░░░░░░░░░░░░░░    │
│                          │
│           ◇              │
│  Create your first       │
│  project                 │
│                          │
│  A project holds your    │
│  work, files, and        │
│  teammates in one place. │
│                          │
│ ┌──────────────────────┐ │
│ │  Create a project    │ │  full-width
│ └──────────────────────┘ │
│ ┌──────────────────────┐ │
│ │ Start from a template│ │
│ └──────────────────────┘ │
│                          │
│  Explore a sample  →     │
│                          │
│   ░░░░░░░░░░░░░░░░░░░    │
└──────────────────────────┘
```

- Body copy truncates to the first sentence on mobile (drop the "takes about a minute" clause) to keep the CTA above the fold on a 667px-tall viewport.
- Only one ghost card row above and below; three columns of ghosts on a phone is noise.

### Design Tokens Used

| Token | Value | Usage |
|---|---|---|
| `--color-text-primary` | `#111827` | Headline, secondary button label |
| `--color-text-secondary` | `#4B5563` | Body copy |
| `--color-accent` | `#4F46E5` | Primary button bg, link text, focus ring |
| `--color-accent-hover` | `#4338CA` | Primary button hover |
| `--color-border-strong` | `#6B7280` | Secondary button border (**not** gray-300 — see A-4) |
| `--color-surface` | `#FFFFFF` | Panel background |
| `--color-ghost` | `#F3F4F6` | Ghost card fill |
| `--space-2` | 8px | Button gap, icon→headline |
| `--space-3` | 12px | Headline→body |
| `--space-5` | 24px | Body→button row |
| `--space-6` | 32px | Button row→footer link |
| `--radius-md` | 8px | Buttons |
| `--radius-lg` | 12px | Ghost cards |
| `--font-size-xl` | 24px / 32px line | Headline |
| `--font-size-base` | 15px / 24px line | Body |
| `--font-size-sm` | 14px / 20px line | Footer link |
| `--font-weight-semibold` | 600 | Headline, button labels |
| `--focus-ring` | 2px solid `--color-accent`, 2px offset | All interactive elements |

Values are fallbacks for teams without a token set. **Map to your existing tokens; ship none of these hex codes raw.**

### Components

| Component | Variant | Props | Notes |
|---|---|---|---|
| `EmptyState` | `first-run` \| `filtered` \| `archived-only` \| `no-permission` | `icon?`, `title`, `description?`, `primaryAction?`, `secondaryAction?`, `footerLink?`, `showGhosts?: boolean` | Build generic. You have the same problem on the team, files, and integrations pages — solve it once. All action props optional: the no-permission variant renders with none. |
| `Button` | `primary` \| `secondary` | `label`, `onClick`, `size="lg"` | Existing component. `size="lg"` = 44px height. |
| `GhostGrid` | — | `rows: number`, `columns: number` | Static, `aria-hidden="true"`, `pointer-events: none`, **no animation**. Mirrors `ProjectCard` dimensions exactly. |
| `PageHeader` | — | `actionVariant: 'primary' \| 'ghost'` | New prop. Pass `'ghost'` while the empty state is visible so the page has exactly one primary action. |

### States and Interactions

| Element | State | Behavior |
|---|---|---|
| Page | `loading` | Skeleton grid. **Never** render any empty state before the request resolves. No minimum-delay hack; just gate on resolved status. |
| Page | `error` | Error block + `Retry`. Must not fall through to the empty state. This is Finding U-1 — the most likely current bug. |
| Page | `empty` + first-run | Variant A. `showGhosts: true`. |
| Page | `empty` + active filter/search | Variant B. `showGhosts: false`. No onboarding copy. |
| Page | `empty` + user has archived projects | Variant C. `showGhosts: false`. |
| Page | `empty` + user lacks create permission | Variant D. No primary CTA unless a real request-access route exists. |
| Primary button | default / hover / active / focus / loading / disabled | hover → `--color-accent-hover`; focus → focus ring; on click → inline spinner + label "Creating…", button disabled, **no layout shift** (reserve label width). |
| Secondary button | default / hover / focus | hover → background `#F9FAFB`, border unchanged. |
| Footer link | default / hover / focus | hover → underline; arrow translates 2px right (skip under `prefers-reduced-motion`). |
| Ghost grid | static only | No hover, no focus, no animation, not in tab order. |
| Header action | `ghost` while empty, `primary` once ≥1 project | Prevents two competing primaries. |

### Responsive Behavior

| Breakpoint | Changes |
|---|---|
| ≥1280px | Panel 480px centred; ghost grid 4 columns × 2 rows |
| 1024–1279px | Panel 480px; ghost grid 3 × 2 |
| 768–1023px | Panel `max-width: 440px`; ghost grid 2 × 2; buttons stay side-by-side |
| 480–767px | Panel full width minus `--space-5` gutters; **buttons stack full-width**, primary on top; ghost grid 1 × 1 above and below |
| <480px | As above; body copy drops the second sentence; icon shrinks 48→40px |
| Zoom 200% | Reflows as the <480px layout. No clipping, no horizontal scroll (1.4.10). |

### Edge Cases

- **Empty state:** this document.
- **Loading:** skeleton grid matching `ProjectCard` dimensions. Critically, **loading must never render "No projects"** — see U-1.
- **Error:** dedicated error block with `Retry`. A failed fetch that renders as "empty" tells the user their data is gone. Highest-severity edge case here.
- **Race condition:** if the user creates a project in another tab, the empty state must not reappear on refocus. Re-validate on window focus.
- **Long text / i18n:** headline wraps to 2 lines max at 480px; no fixed panel height; buttons `width: auto` + `min-width`, stacking below 768px. German +35%.
- **Truncation:** none in the empty state. If body copy overflows two lines at a given breakpoint, that's a copy-length bug — fix the copy, don't add an ellipsis.
- **No sample project available** (feature not built / plan doesn't include it): omit the footer link entirely. Do not render a disabled or "coming soon" link.
- **No templates available:** omit the secondary button. The primary widens to `min-width: 200px` and centres alone.
- **Permission-gated:** Variant D, no unusable CTA.
- **Seat/plan limit reached with zero projects:** Variant D copy with an upgrade CTA — and be honest about the limit in the body.
- **Slow connection:** ghost cards are CSS-only, no image request. The icon is inline SVG. The empty state must render with zero additional network calls — an illustration PNG that loads after the text is exactly the wrong asset on the wrong screen.
- **RTL:** layout mirrors; footer arrow flips.
- **Dark mode:** re-verify every contrast pair (see audit).

### Animation

| Element | Trigger | Animation | Duration | Easing |
|---|---|---|---|---|
| Empty-state panel | Mount, after data resolves | Fade + 4px rise | 180ms | `cubic-bezier(0.2, 0, 0, 1)` |
| Ghost grid | — | **None** | — | — |
| Primary button | Hover | Background colour | 120ms | `ease-out` |
| Footer link arrow | Hover | `translateX(2px)` | 120ms | `ease-out` |

All of the above disabled under `prefers-reduced-motion: reduce`. **The ghost grid must never shimmer** — shimmer is the universal signal for "loading", and using it here tells the user to wait for content that is never coming.

### Accessibility Notes

- Container: `role="status"` `aria-live="polite"` `tabindex="-1"`, announced once on mount.
- Headline: `<h2>` (page `<h1>` is "Projects").
- Icon: inline SVG, `aria-hidden="true"`, `focusable="false"`.
- Ghost grid: `aria-hidden="true"`, `pointer-events: none`, not focusable.
- Tab order: primary → secondary → footer link. No auto-focus (3.2.1).
- Focus ring: 2px `--color-accent`, 2px offset, on all three.
- Touch targets: 44×44px minimum, achieved with padding on the footer link.
- Semantics: `<button>` for in-page actions, `<a href>` for navigation. Don't use a `<div onClick>`.
- Links carry a non-colour affordance (underline and/or arrow).

### Instrumentation (ship with the design, not after)

You described the problem as a bounce, which means you need to be able to tell whether this worked. Fire these:

| Event | Properties | Why |
|---|---|---|
| `projects_empty_state_viewed` | `variant` (first-run/filtered/archived/no-permission), `account_age_hours`, `is_first_session` | Baseline. Also immediately reveals if `filtered` is firing far more than you expect — evidence for U-5. |
| `projects_empty_state_cta_clicked` | `action` (create/template/sample), `variant` | The conversion numerator. |
| `project_created` | `source` (empty_state/header/template/sample), `time_since_empty_state_view_ms` | Attributes creation to this surface specifically. |
| `sample_project_opened` | — | Tests the U-3 hypothesis directly. |
| `projects_page_error_shown` | `error_type` | **Fire this even before you redesign anything.** If it's non-trivial, U-1 is your bounce and the copy was never the problem. |

**Success metric:** % of new accounts that create ≥1 project within 24h of first viewing `/projects`. **Guardrail:** % of first projects that are still empty 7 days later. It is easy to raise the first number by pressuring people into creating a hollow project they never use — that's the metric moving while the outcome doesn't. Watch both or you'll ship a win you didn't get.

### Build Order

1. **Separate loading / error / empty states** (U-1). Fix the bug before designing around it.
2. **Variant A: headline + body + primary CTA, centred.** ~80% of the benefit. Ship it alone if that's all you have.
3. **Variants B, C, D.** Cheap once the `EmptyState` component exists, and B prevents a genuinely alarming false alarm.
4. **Ghost grid.** Pure CSS, no dependencies.
5. **Sample project / templates.** Real product work — sequence it on its own merits, and only if the data from steps 1–4 says the remaining gap is evaluation friction rather than comprehension.

---

## Stress Test

**What's weakest here.** I never saw the page. Everything above is reasoned from eleven characters of description, which means the critique is of a *pattern*, not of your implementation. If your empty state already has a CTA and I've critiqued a strawman, Part 1's findings U-2 through U-4 collapse and only U-1, U-5, and U-6 survive. The severity ratings in particular are pattern-frequency estimates, not observations.

**The assumption most likely to be wrong: that this is an empty-state problem at all.** "Users land here on day one and bounce" is a description of behaviour with a cause attached by inference. Equally consistent with that sentence: the signup flow oversold something the product doesn't do; the page took four seconds to load; the fetch failed; the user arrived expecting their imported data and found none; the product's value is genuinely visible only after real work is in it, and no empty state can fake that. A better empty state improves every one of those situations slightly and fixes none of them. **Before building Part 4, look at one recording of a bouncing day-one session.** One observed session is worth more than this whole document.

**The second-weakest assumption: that the bounce is on this page rather than at the next step.** If users *do* click "create a project" today via the header and then abandon a six-field creation modal, the empty state is the wrong surface entirely and this work will move the click-rate metric while leaving activation flat. The `project_created` event with `time_since_empty_state_view_ms` is specifically designed to detect that — check it before congratulating anyone.

**What a smart critic would say.** Three things. First: *"You've written a lot of spec for a screen that might only need one button."* Fair, and the Build Order concedes it — step 2 is the whole fix if steps 3–5 turn out unnecessary. Second: *"The sample-project recommendation is the most expensive item here and rests on the least evidence."* Also fair. It's a genuinely strong pattern (Figma, Notion, Linear all use it) but it's real product work, it creates a demo-data cleanup problem, and it can actively backfire — a sample project full of someone else's fictional content can read as clutter to a user who wanted a clean start. That's why it's last in the build order and gated on data. Third: *"Nothing here validates that 'project' is the right first object."* True, and it's the deepest version of the problem: if a day-one user has to create a container before doing anything, the empty state is a symptom of an object model that front-loads setup. Products that solved this best didn't write better empty-state copy — they removed the requirement, auto-creating a first project at signup so the user lands on something populated. **That option isn't in this deliverable because you asked for an empty state, but it is the strictly better fix if your architecture permits it, and it would make Parts 1–4 moot.** Worth ten minutes before you spend a sprint.

**What would falsify the recommendation.** If instrumentation shows `projects_empty_state_viewed` firing mostly with `variant: filtered` or alongside `projects_page_error_shown`, this is a bug report, not a design brief — stop after step 1.
