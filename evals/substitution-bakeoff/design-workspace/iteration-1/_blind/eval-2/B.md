# Projects Page — Empty State

**Skills run:** `[SKILL]` (primary), `[SKILL]` (diagnosis), `[SKILL]` (audit of the proposed design), `[SKILL]` (engineering spec).

---

## 0. Questions I would have asked, and what I assumed instead

This ran unattended, so here are the questions that would actually have changed the design, each with the assumption I proceeded under. **Check the ones marked ⚠ before building — they change the recommendation, not just the wording.**

| # | Question | Assumption I proceeded under | Impact if wrong |
|---|---|---|---|
| 1 | ⚠ Is "No projects" also shown while the list is still loading? | It is, or at least flashes. This is a top-3 suspect for the bounce and no copy fixes it. | If so, this is the actual fix. See Critique finding U-1. |
| 2 | ⚠ Is "No projects" also shown when the fetch **fails**? | It is — most single-string empty states are `if (!projects.length)`. | Users see a false "you have nothing" on a network error. Critical: see U-2. |
| 3 | ⚠ Can every user who reaches this page actually create a project? | No — viewer/guest roles exist in most team products. | Showing "Create project" to someone without permission produces an error on click, which is worse than bouncing. See variant E-5. |
| 4 | Do templates, an importer, or a sample project exist today? | Templates: no. Import: no. Both are recommended but gated behind Tier 2/3. | Tier 1 ships without them and still works. |
| 5 | What is a "project" to this audience — a client engagement, a codebase, a campaign, a personal to-do list? | A container for a unit of team work (tasks/files/updates). Copy is written for that. | Nouns in the body copy change; structure does not. |
| 6 | Is signup single-player or invited-into-a-team? | Mixed. Both paths are handled (E-5 covers the invited-but-empty case). | Changes which variant is the *common* case, not the set. |
| 7 | Brand voice? | Plain, confident, non-cute. No exclamation marks, no "Oops!", no mascot voice. | Tone variants are supplied in §2.2 for three other voices. |
| 8 | Existing design tokens? | Generic Tailwind-ish scale, named as tokens. Values in the handoff are placeholders to be swapped for yours. | Contrast findings hold; hex values need re-checking against your real palette. |

**One more thing I'd have pushed back on in person:** "add an empty state" may be the wrong frame. The best empty state is one the user never sees. See Critique → Biggest Opportunity.

---

## 1. Design Critique: Projects Page — Current Empty State

*(skill: [SKILL]. The artifact under review is the described current state: a projects page rendering the string "No projects".)*

### Overall Impression

"No projects" is not an empty state. It is a **status report on the database, written from the system's point of view.** It answers a question the user did not ask ("how many rows are there?") and ignores the three they are actually asking on day one: *What is this page for? What am I supposed to do here? Is this thing going to be worth my time?*

It is also, structurally, a dead end: the page has content but no exit. A user who has just signed up is at their highest-ever willingness to do work in your product, and the page gives them nothing to do with it. Bouncing is the rational response.

**What works:** it is honest and it is short. Do not lose either property. The failure mode of empty-state redesigns is a cheerful illustration plus 60 words of marketing copy that is *less* clear than "No projects."

**Biggest opportunity:** not better words on this screen — **not needing this screen on day one.** A brand-new account should arrive at a projects page that already has something in it (a starter project created during signup, or a read-only sample project) or should arrive with the create-project form already open. An empty state is a good consolation prize; it is a worse product than having no empty moment at all. Ship the empty state below — it is needed permanently, for all the non-day-one cases — and separately test removing the day-one instance entirely. I'd expect the removal to beat the redesign.

### Usability

| # | Finding | Severity | Recommendation |
|---|---|---|---|
| U-1 | The empty state is almost certainly also the **loading** state. If `projects` starts as `[]`, every user sees "No projects" for the duration of the fetch. On a slow connection that is 1–3 seconds of being told, falsely, that they have nothing. Day-one users on mobile networks are exactly the affected population. | **Critical** | Render a skeleton for `status === 'loading'`. The empty state may only render on `status === 'success' && items.length === 0`. This is a state-machine fix, not a copy fix, and it may be the entire bug. |
| U-2 | The empty state is almost certainly also the **error** state. A failed or 403'd fetch falls through to the same branch and reports "you have no projects," which is a false statement about the user's data. | **Critical** | Separate `error` from `empty`. A user who is told their projects are gone may create duplicates or churn on the spot. Distinguishing these two is the highest-severity item in this document. |
| U-3 | **No call to action.** There is nothing clickable. Even if a "New project" button exists in the page header, the user's eye is at the center of the page where the message is, and the message does not point at it. | **Critical** | Put the primary action inside the empty state, adjacent to the sentence that motivates it. Keep the header button too; they are not redundant, they serve different moments. |
| U-4 | **The blank-page problem is unaddressed.** Even a user who finds the button now faces "Project name: ___" with no idea what granularity you expect. Is a project a company, a quarter, a task? Hesitation here reads as a bounce in your funnel but is actually a naming problem. | **Major** | Two fixes, both cheap: (a) one line of body copy that says what people typically put here; (b) a pre-filled default name in the create form so the form is never blank. Templates (Tier 2) solve it properly. |
| U-5 | **No reversibility signal.** First-run users hesitate to create a durable-looking object in a product they have not decided to trust. | **Major** | One line: creation is reversible and renameable. Cheap, and it measurably moves first-object creation. |
| U-6 | **Filtered-to-zero and truly-empty are probably the same string.** If a user filters to "Archived" and sees "No projects," they may conclude their data is gone. | **Major** | Distinct copy plus a "Clear filters" action. See §2.3 E-2/E-3. |
| U-7 | **No second path.** A user who has existing work elsewhere (another tool, a spreadsheet) has no offer that matches their situation; "create one from scratch" is the only door. | Minor (Major if you have an importer) | Offer import / invite-teammate / view-example as a secondary action once they exist. |

### Visual Hierarchy

- **Eye draws to:** whatever is the largest element on the page — the nav, the header, or the "New project" button if one exists. Almost certainly *not* the empty-state text, which is small, grey, centered, and easily read as a disabled label rather than content. **Not correct.** In an empty state the empty state *is* the page; it should be the strongest thing on screen after the page title.
- **Reading flow:** currently a single dead-end token. There is no flow to describe, which is itself the finding.
- **Intended flow after redesign:** headline (what to do) → one line of body (why, and what to put in it) → primary button (do it) → secondary option (different door) → reassurance microcopy (it's safe). Five beats, strictly top to bottom, single column, no eye-jumps sideways.
- **Vertical position:** avoid true vertical centering in a tall viewport — it floats the content into the void and drops it below the fold on short ones. Anchor the block in the upper-middle of the content area (roughly 15–20% down), capped at a readable measure.

### Consistency Issues

| Element | Issue | Fix |
|---|---|---|
| Empty-state pattern | Almost certainly bespoke per page. There will be an "empty" string on projects, another on tasks, another on search, each worded differently. | Build one `EmptyState` component (spec in §4) and route every list through it. This is the change that stops the next five empty states from being bad. |
| Noun for the action | Header button may say "New project" while docs/onboarding say "Create a project". | Pick one verb and use it everywhere — recommendation: **Create project**. `[SKILL]` principle 3 (Consistent). |
| Grey body text | Muted grey on white is the default empty-state styling everywhere and is usually below the contrast floor. | See Accessibility A-1. |
| Loading treatment | If other lists use skeletons and this one doesn't, the inconsistency is itself a bug signal. | Standardize skeleton usage in the same component. |

### What Works Well

- Short. Not overwritten. Most redesigns regress on this.
- Honest — it doesn't pretend something is loading when it isn't.
- Centered single-column layout is the right container; only the contents are wrong.

### Priority Recommendations

1. **Split the four states** — loading / error / empty / no-permission. Copy changes cannot fix a state-machine problem, and two of these are currently telling users something false. (U-1, U-2)
2. **Put a primary action and a reason inside the empty state.** (U-3, U-4, U-5) — this is the copy in §2.
3. **Separately test not showing an empty state at all on day one** (starter project or auto-opened create form). Expect this to beat #2.
4. **Extract one reusable `EmptyState` component** so this is solved for every list in the product. (§4)

---

## 2. UX Copy: Projects page, zero-state family

*(skill: [SKILL]. Pattern applied: "Empty States — what this is + why it's empty + how to start.")*

### 2.1 Recommended copy — first-run empty (the day-one case)

> ### Create your first project
>
> A project holds the tasks, files, and updates for one piece of work. Most teams start with whatever they're working on this week.
>
> **[ Create project ]**  [ Start from a template ]
>
> Takes about a minute — you can rename or delete it later.

**Element-by-element:**

| Element | Copy | Char count |
|---|---|---|
| Heading | `Create your first project` | 25 |
| Body | `A project holds the tasks, files, and updates for one piece of work. Most teams start with whatever they're working on this week.` | 128 |
| Primary CTA | `Create project` | 14 |
| Secondary CTA | `Start from a template` | 21 |
| Helper text | `Takes about a minute — you can rename or delete it later.` | 57 |
| Tertiary link (Tier 2) | `Import from Asana, Trello, or CSV` | 33 |

### 2.2 Alternatives

| Option | Heading / body | Tone | Best for |
|---|---|---|---|
| **A — Recommended: instructive** | "Create your first project" / "A project holds the tasks, files, and updates for one piece of work. Most teams start with whatever they're working on this week." | Plain, directive, unembarrassed | Default. Tells them what to do *and* what to put in it. |
| B — Value-first | "Your work, organized in one place" / "Projects keep tasks, files, and decisions together instead of scattered across tools. Create one to see how it works." | Benefit-led | Self-serve signups who arrived from a marketing page and still need convincing. Weaker on the blank-page problem. |
| C — Warm | "Nothing here yet — let's fix that" / "Projects are where your team's work lives. Start with something small: this week's work is a good first project." | Friendly, informal | Consumer/prosumer, playful brand. Avoid for enterprise buyers. |
| D — Minimal / enterprise | "No projects yet" / "Create a project to organize work, files, and collaborators." | Terse, neutral | Regulated or enterprise contexts where warmth reads as unserious. Note this is close to today's copy — but with a CTA, which is the actual fix. |
| E — Anti-pattern, do not ship | "Oops! It's lonely in here 🦗 Looks like you haven't created any projects yet!" | Cute | Nothing. Adds words, adds no information, ages badly, translates badly, and reads as condescending to a user who is already unsure. |

### 2.3 The rest of the family — every zero-state this page can reach

Ship these together. Shipping only the first-run state is how "No projects" got here in the first place.

| ID | State | Heading | Body | Actions |
|---|---|---|---|---|
| **E-1** | First-run empty (user can create) | Create your first project | A project holds the tasks, files, and updates for one piece of work. Most teams start with whatever they're working on this week. | **Create project** · Start from a template |
| **E-2** | Filtered to zero | No projects match these filters | Try removing a filter, or create a project. | **Clear filters** · Create project |
| **E-3** | Search returns zero | No projects matching "*{query}*" | Check the spelling, or search all work instead of just projects. | **Clear search** · Search everything |
| **E-4** | All projects archived / completed | No active projects | You have {n} archived projects. | **View archived** · Create project |
| **E-5** | ⚠ User lacks create permission | You don't have access to any projects yet | Ask a workspace admin to add you to a project. | **Copy invite request** *(no Create button — see note)* |
| **E-6** | Error loading | We couldn't load your projects | This is a problem on our end, not with your data. | **Try again** · Contact support |
| **E-7** | Loading | *(no text — skeleton rows)* | — | — |

**Note on E-5:** never render a primary action the user cannot complete. A disabled "Create project" with a tooltip is acceptable; an enabled one that throws a 403 is not — it converts a mild disappointment into a trust problem, and it is a common cause of day-one bounce in invite-based signups. This is the state most teams forget and it is the one most likely to be silently affecting your numbers.

**Note on E-6:** the body line "This is a problem on our end, not with your data" is load-bearing, not politeness. Without it the user's working assumption on seeing an empty list is that their data is gone.

### 2.4 Rationale

- **"Create your first project" as the heading, not "No projects yet."** The heading is the one line everyone reads. Spending it on a fact the user can already see (the list is empty) wastes it. Spend it on the instruction. Matches `[SKILL]` CTA principle — start with a verb.
- **The body sentence does two jobs.** Clause one defines the object ("what this is"). Clause two — *"most teams start with whatever they're working on this week"* — is the one that actually moves the metric: it answers "what am I supposed to put here?", which is the real reason people stall at a blank name field. Social proof plus a concrete, small, low-stakes suggestion.
- **"Takes about a minute — you can rename or delete it later."** Removes commitment anxiety. A day-one user has not decided to trust you and is reluctant to create something permanent-looking. Naming reversibility explicitly is one of the highest-leverage sentences available in first-run UI. ⚠ Verify "about a minute" against your real create flow; if creating a project opens a six-field form, fix the form rather than lying in the microcopy.
- **Two actions, not five.** "Create project" (from scratch) and "Start from a template" (for people who want a shape to copy) cover the two genuine mental states. More options at zero context produces choice paralysis, not flexibility.
- **No exclamation marks, no apology, no "Oops."** The user has not made a mistake. Empty is the correct state of a new account.
- **Kept short deliberately.** The current copy's only virtue is brevity; the redesign is 5 short beats, all skimmable in about 4 seconds.

### 2.5 Localization notes

- **"first" in the heading** — some languages (e.g. German *Ihr erstes Projekt*, French *votre premier projet*) inflect for gender/number against the word "project". Do not template the ordinal; let translators write the full heading.
- **Never build the search-zero string by concatenation.** Use a full interpolated sentence with a named placeholder: `no_projects_matching: 'No projects matching "{query}"'`. Fragment concatenation breaks in every RTL and verb-final language.
- **E-4 has a plural** — `{n} archived projects` needs ICU plural rules (`one`/`other`, plus `few`/`many` for Slavic languages), not `n + " projects"`.
- **Budget +35% width for German/Finnish.** "Start from a template" → *Mit einer Vorlage beginnen* (28 chars). Buttons must not truncate; allow them to wrap to two lines or stack.
- **Em dash in the helper line** may be replaced by a period in locales that don't use it. Give translators permission to split it into two sentences.
- **"Project" must match the noun used in the nav and in your docs, in every locale.** If the sidebar says *Projekte*, the empty state cannot say *Vorhaben*. Add "project" to the termbase as a locked term.
- **Do not embed the brand voice in the string key names** — translators will see `empty_projects_heading`, so supply a tone note in the context field: "Instructional, plain, no humor."

---

## 3. Accessibility Audit: Proposed Projects Empty State

*(skill: [SKILL]. Standard: WCAG 2.1 AA. Audited against the proposed design in §2 plus the handoff spec in §4, since no live page exists. Every finding below is a build instruction, not a retro-fix.)*

### Summary

**Issues:** 9 | **Critical:** 3 | **Major:** 4 | **Minor:** 2

The three criticals are all in the same family: an empty state is a **dynamic content swap**, and the standard implementation announces nothing to a screen reader user, who is left on a page that finished loading in silence.

### Findings

| # | Issue | WCAG | Severity | Fix |
|---|---|---|---|---|
| A-1 | Muted grey body copy (the default empty-state treatment, typically `#9CA3AF` on `#FFFFFF` ≈ **2.5:1**) fails normal-text contrast. | 1.4.3 | **Critical** | Use `--color-text-secondary` at `#6B7280` or darker (4.83:1). Empty-state body copy is primary content, not a hint; stop styling it as de-emphasized. |
| A-2 | The list region swaps from skeleton → empty state with no announcement. Screen reader users get silence and cannot tell whether loading finished, failed, or returned nothing. | 4.1.3 / 1.3.1 | **Critical** | Wrap the list region in `aria-live="polite" aria-busy={isLoading}`, or move focus to the empty-state heading on transition. `aria-busy` flipping true→false plus the live region gives "Create your first project…". |
| A-3 | The error state (E-6) rendered as plain text is not identified as an error to assistive tech. | 3.3.1 / 4.1.3 | **Critical** | `role="alert"` on the error variant only (never on the ordinary empty variant — `alert` is assertive and interrupts). |
| A-4 | Decorative illustration gets a generated `alt` like "empty box illustration", which adds noise and no information. | 1.1.1 | Major | `alt=""` + `aria-hidden="true"` + `role="presentation"`. It is decorative. If it ever carries meaning the text must carry it too. |
| A-5 | Heading level chosen ad hoc (`<h1>` inside the page, or a styled `<div>`). Either breaks the document outline or removes the heading from the rotor entirely. | 1.3.1 / 2.4.6 | Major | The page keeps its `<h1>Projects</h1>`. The empty-state heading is `<h2>`. Never a `<div class="heading">`. |
| A-6 | Secondary action implemented as a styled `<div onClick>` or a link that behaves like a button. Not focusable, not Space-activatable, wrong role announced. | 2.1.1 / 4.1.2 | Major | `<button>` for actions that stay on the page; `<a href>` only for genuine navigation. No exceptions. |
| A-7 | After creating a project, focus is lost to `<body>` when the modal closes, dumping keyboard and SR users at the top of the document with no confirmation. | 2.4.3 / 4.1.3 | Major | Return focus to the newly created project's row (or its link), and announce "Project {name} created" in a polite live region. |
| A-8 | Centered fixed-width card (`width: 420px`) overflows or clips at 200% zoom / 320px viewport. | 1.4.4 / 1.4.10 | Minor | `max-width: 48ch` with `width: 100%`, padding in `rem`. Must reflow, never horizontally scroll. |
| A-9 | Button touch targets sized to text (e.g. 32px tall) on mobile. | 2.5.5 | Minor | Minimum 44×44 CSS px including padding; 8px minimum gap between the primary and secondary actions so a mistap on a 5" phone doesn't fire the wrong one. |

### Color Contrast

Values are against the assumed palette in §0/Q8 — **re-run these against your real tokens.**

| Element | FG | BG | Ratio | Required | Pass? |
|---|---|---|---|---|---|
| Heading (`h2`, 20px/600) | `#111827` | `#FFFFFF` | 16.9:1 | 4.5:1 | ✅ |
| Body copy (16px) | `#6B7280` | `#FFFFFF` | 4.83:1 | 4.5:1 | ✅ (no margin — do not lighten) |
| Body copy *if left at default muted* | `#9CA3AF` | `#FFFFFF` | 2.54:1 | 4.5:1 | ❌ **A-1** |
| Helper text (13px) | `#6B7280` | `#FFFFFF` | 4.83:1 | 4.5:1 | ✅ (13px is not "large text" — 4.5:1 applies) |
| Primary button label | `#FFFFFF` | `#2563EB` | 4.54:1 | 4.5:1 | ✅ (thin margin; verify your exact blue) |
| Secondary button border | `#D1D5DB` | `#FFFFFF` | 1.47:1 | 3:1 | ❌ Non-text contrast fail — darken to `#9CA3AF` (2.54:1, still short) or `#6B7280` (4.83:1 ✅). Use `#6B7280`. |
| Focus ring | `#2563EB` | `#FFFFFF` | 4.54:1 | 3:1 | ✅ |
| Error text (E-6) | `#B91C1C` | `#FFFFFF` | 6.4:1 | 4.5:1 | ✅ — and error must not be signalled by color alone (1.4.1): keep the "Try again" button and the explicit heading. |

### Keyboard Navigation

| Element | Tab order | Enter / Space | Escape |
|---|---|---|---|
| Skip link → main | 0 | Activates | — |
| `h1` Projects (not focusable) | — | — | — |
| Primary: **Create project** | 1 (first focusable in the empty state) | Opens create flow; focus moves into it | — |
| Secondary: Start from a template | 2 | Opens template picker | — |
| Tertiary link: Import | 3 | Navigates | — |
| Create modal (if used) | Focus trapped inside; first field focused on open | Submits | Closes, **returns focus to the button that opened it** |
| After successful create | Focus → new project row; polite announcement | — | — |

Focus indicator: 2px solid ring with 2px offset, visible against both the page background and the button fill. Do not rely on the browser default and do not `outline: none` without an equivalent replacement.

### Priority Fixes

1. **A-2 / A-3** — announce the loading→empty and loading→error transitions. Without this the page is silent for SR users, which is the accessibility version of the same bounce problem sighted users have.
2. **A-1** — darken the body copy. One token change, affects every empty state in the product.
3. **A-7** — focus management after create, so the success of the action is perceivable without sight.

---

## 4. Handoff Spec: `EmptyState` component + Projects page integration

*(skill: [SKILL]. Written to be implementable without a follow-up conversation. Token values are placeholders — swap for your real scale, keep the semantic names.)*

### Scope

One generic `<EmptyState>` component, plus a `ProjectsEmpty` composition that selects a variant from page state. Built this way, the other lists in the product (tasks, files, search, members) get fixed for free.

### Design Tokens Used

| Token | Value | Usage |
|---|---|---|
| `--color-text-primary` | `#111827` | Heading |
| `--color-text-secondary` | `#6B7280` | Body + helper text (⚠ not `--text-muted`; see A-1) |
| `--color-text-error` | `#B91C1C` | E-6 heading |
| `--color-border-strong` | `#6B7280` | Secondary button border (3:1 floor) |
| `--color-surface` | `#FFFFFF` | Container background |
| `--color-accent` | `#2563EB` | Primary button fill, focus ring |
| `--space-2 / -3 / -4 / -6 / -10` | 8 / 12 / 16 / 24 / 40px | Internal rhythm (see layout) |
| `--radius-md` | 8px | Buttons |
| `--font-size-lg` | 20px / 28px line-height / 600 | Heading |
| `--font-size-md` | 16px / 24px / 400 | Body |
| `--font-size-sm` | 13px / 20px / 400 | Helper |
| `--measure-prose` | 48ch | Max text width |
| `--duration-fast` | 150ms | Fade-in |
| `--ease-out` | `cubic-bezier(0.2, 0, 0, 1)` | Fade-in |

### Components

| Component | Variant | Props | Notes |
|---|---|---|---|
| `EmptyState` | `default` \| `error` \| `restricted` | `icon?: ReactNode` (decorative, `aria-hidden`), `heading: string` (required), `body?: string`, `primaryAction?: {label, onClick, disabled?, disabledReason?}`, `secondaryAction?: {label, onClick}`, `tertiaryLink?: {label, href}`, `helperText?: string`, `headingLevel?: 2\|3` (default 2), `tone?: 'default'\|'error'` | Presentational only. No data fetching, no state selection. Renders `role="alert"` **only** when `tone === 'error'`. |
| `ProjectsEmpty` | — | `status`, `items`, `filters`, `searchQuery`, `archivedCount`, `canCreate` | The state-selection logic. See decision table below. This is the piece that fixes U-1/U-2/E-5. |
| `ListSkeleton` | `rows: number` (default 4) | — | Rendered for `status === 'loading'`. **Never** falls through to `EmptyState`. |
| `Button` | `primary` \| `secondary` | existing | Reuse; do not fork. Enforce 44px min target. |

### State selection (the important part)

Evaluate in this order and return on first match — order matters:

| Order | Condition | Render |
|---|---|---|
| 1 | `status === 'loading'` | `<ListSkeleton />` — **never** the empty state (U-1) |
| 2 | `status === 'error'` | `EmptyState` E-6, `tone="error"` (U-2) |
| 3 | `items.length > 0` | The list |
| 4 | `searchQuery` non-empty | E-3 |
| 5 | any filter active | E-2 |
| 6 | `!canCreate` | E-5, no enabled primary action |
| 7 | `archivedCount > 0` | E-4 |
| 8 | otherwise | E-1 (first-run) |

Copy for each ID is in §2.3. Do not inline these strings — put them in the i18n catalog with the context notes from §2.5.

### Layout

Single column, horizontally centered, `max-width: var(--measure-prose)`. Anchored with `padding-top: clamp(40px, 12vh, 96px)` — not `justify-content: center`, which floats the block and pushes it below the fold on short viewports (Critique → Visual Hierarchy).

Vertical rhythm, top to bottom: icon (optional, 40px) → `--space-6` → heading → `--space-3` → body → `--space-6` → action row → `--space-4` → helper text. Action row is `flex`, `gap: --space-3`, `flex-wrap: wrap`.

### States and Interactions

| Element | State | Behavior |
|---|---|---|
| Primary button | default / hover / active / focus-visible / disabled | Hover: darken accent 8%. Focus-visible: 2px ring, 2px offset. Disabled (E-5 only): 40% opacity, `aria-disabled="true"`, tooltip carries `disabledReason` — and the reason must also be in the body copy, since tooltips are unreachable on touch. |
| Primary button | loading (create in flight) | Label → spinner + "Creating…", button `aria-busy="true"`, stays the same width to prevent layout shift. |
| Secondary button | as above | 1px `--color-border-strong` border, transparent fill. |
| Whole block | mount | Fade in over `--duration-fast`. **Only** after the fetch resolves, and skip entirely under `prefers-reduced-motion: reduce` (see Animation). |
| Whole block | list becomes non-empty | Unmount immediately, no exit animation. Focus moves to the new row (A-7). |
| Tertiary link | default / hover / focus | Underline on hover and focus; never color-only differentiation (WCAG 1.4.1). |

### Responsive Behavior

| Breakpoint | Changes |
|---|---|
| ≥1024px | As specified. Block centered in the content area, not the full viewport (respect the sidebar). |
| 768–1023px | Unchanged; `padding-top` clamps down. |
| <768px | Actions stack vertically, full-width, `gap: --space-3`, order: primary first. Horizontal page padding `--space-4`. Icon drops to 32px or is hidden. |
| <360px | Icon hidden. Heading may wrap to two lines — do not shrink below `--font-size-lg`, and never truncate the heading. |
| 200% zoom | Must reflow within `max-width` with no horizontal scroll (A-8). |

### Edge Cases

- **Empty state:** this document.
- **Long text (i18n):** heading wraps, never truncates, never ellipsizes. Buttons grow to fit and wrap to two lines rather than clipping. Test with German (+35%) and a 320px viewport together — that's the worst case.
- **Loading:** `ListSkeleton`, 4 rows, shimmer disabled under `prefers-reduced-motion`. Skeleton must appear for a **minimum of 200ms** once shown, to avoid a flash on fast connections; alternatively delay showing it by 150ms so instant responses never flicker.
- **Error:** E-6 with `role="alert"`, a working "Try again" that re-issues the fetch, and **never** the first-run copy. Log the underlying error; do not surface stack traces or status codes to the user.
- **Slow connection:** skeleton persists. There is no timeout at which we fall back to "No projects" — that is the original bug.
- **Offline:** if the app has an offline indicator, suppress the empty state entirely and show the offline state; asserting "you have no projects" while offline is a false statement about their data.
- **Race — project created in another tab:** on window refocus, re-fetch; if items arrive, unmount the empty state silently.
- **`canCreate === false`:** E-5, no enabled create path. Never render an action that will 403.
- **Optimistic create:** if creation is optimistic, swap the empty state for the row immediately and roll back visibly (with the error) on failure. Do not bounce back to the empty state with no explanation.

### Animation

| Element | Trigger | Animation | Duration | Easing |
|---|---|---|---|---|
| EmptyState block | Mount after fetch resolves | Fade + 4px rise | 150ms | `--ease-out` |
| Skeleton shimmer | While loading | Opacity pulse 0.6↔1.0 | 1200ms loop | `ease-in-out` |
| Primary button hover | Hover | Background color | 100ms | `linear` |

Under `prefers-reduced-motion: reduce`: no fade, no rise, no shimmer — render the skeleton as static grey blocks and the empty state at full opacity immediately.

### Accessibility Notes

- Page structure: `<h1>Projects</h1>` stays in the page header; the empty state renders `<h2>`. (A-5)
- List region: `<div role="region" aria-label="Projects" aria-live="polite" aria-busy={isLoading}>` wrapping both skeleton and empty state, so the transition is announced. (A-2)
- Error variant only: `role="alert"`. Never on the default variant. (A-3)
- Icon/illustration: `aria-hidden="true"`, `alt=""`. (A-4)
- Actions are `<button>`; the import link is `<a href>`. (A-6)
- Focus order: primary → secondary → tertiary. On create success, move focus to the new project row and announce "Project {name} created." (A-7)
- Touch targets ≥44×44px with ≥8px separation. (A-9)
- Body and helper text use `--color-text-secondary`, never `--color-text-muted`. (A-1)

### Instrumentation (so you can tell whether this worked)

The stated problem is a behavior ("users bounce"), so ship the measurement with the fix.

| Event | Properties | Why |
|---|---|---|
| `projects_empty_state_viewed` | `variant` (E-1…E-6), `is_first_session`, `time_to_render_ms` | ⚠ Variant distribution is the diagnostic. If a meaningful share of day-one views are **E-6** or **E-5**, the bounce was never a copy problem and this redesign will underperform — check this within 48h of shipping. |
| `projects_empty_state_action_clicked` | `variant`, `action` (primary/secondary/tertiary) | Click-through on the empty state. |
| `project_created` | `source` = `empty_state` \| `header_button` \| `template` \| `import` | Attribution; separates the empty state's contribution from the header button's. |
| `projects_page_exited_without_action` | `variant`, `dwell_ms` | The bounce itself, made countable. |

**Primary metric:** % of new accounts creating a first project within 24h of signup.
**Secondary:** empty-state → `project_created` conversion; time-to-first-project.
**Guardrail:** projects created and then deleted within 10 minutes — if a template or a pre-filled name inflates creation with junk projects, this catches it. A rise here means you moved the metric without moving the outcome.

### Delivery tiers

| Tier | Scope | Rough effort |
|---|---|---|
| **1 — ship this week** | State-machine split (loading/error/empty/restricted) + E-1, E-2, E-6 copy + primary CTA + contrast fix. No new backend. | ~1 day |
| **2** | Templates and/or import as the secondary action; E-3, E-4, E-5; reusable `EmptyState` rolled out to other lists. | ~1 week |
| **3** | Remove the day-one empty state entirely: starter project at signup or auto-opened create form; A/B against Tier 1–2. | ~2 weeks incl. experiment |

Tier 1 alone should recover most of the bounce, **if** the cause is the copy. Instrumentation above tells you within two days whether it was.

---

## 5. Stress Test

**What's weakest here.** The entire diagnosis rests on one sentence of secondhand description. I have not seen the page, the funnel data, or a session recording. "Users land here on day one and bounce" is a report of a correlation between a screen and an outcome; I have inferred causation and then designed against my inference. The honest version of this deliverable is: *here is a strictly better empty state, and here is the instrumentation that will tell you whether the empty state was ever the problem.* The instrumentation section is doing more work than it looks like it is.

**Assumptions that could be wrong, in descending order of damage:**

1. **The bounce may have nothing to do with this screen.** A day-one user who bounces on the projects page may have already decided during signup, or may be blocked upstream (email verification, a payment wall, an invite that landed them in the wrong workspace). Every word above would then be wasted effort that ships and moves nothing — and the team would conclude "empty states don't matter" and stop looking. The `projects_empty_state_viewed` variant split is the cheap test that prevents that.
2. **"No projects" may not be a copy problem at all.** If the string is also the loading state or the error state (U-1, U-2 — I flagged them Critical on suspicion, not evidence), then the best copy in the world is being shown to users at the wrong moment. I have ordered the handoff to fix this first for exactly that reason, but I am guessing about the implementation.
3. **The blank-page fix may be the wrong fix.** "Most teams start with whatever they're working on this week" assumes projects are small and weekly. If in your product a project is a client engagement or a year-long program, that line is actively misleading and will produce badly-scoped projects that users abandon — which is worse than bouncing, because it pollutes their workspace and your data. Q5 in §0 is the one I would most want answered before ship.
4. **"Takes about a minute" is an unverified promise.** If create is a six-field form, this sentence makes the product feel slower than it claimed, right at the moment of first trust.
5. **A better empty state may raise creation and not raise retention.** Templates and pre-filled names are proven to lift the creation metric and are also proven to produce empty shells nobody returns to. The 10-minute-deletion guardrail catches the crude version; it does not catch a project created, ignored, and never deleted.

**What a smart critic would say.**

*"You wrote four sections about a screen you've never seen, and buried the actual recommendation — don't show this screen on day one — in a critique subsection."* Fair. Stated plainly: **the highest-expected-value change is a starter project created during signup, and the empty state is the permanent, correct, but secondary fix.** I kept the empty state as the main deliverable because that is what was asked for and because E-2 through E-6 are needed regardless of what happens on day one.

*"Seven empty-state variants for a page that currently has one string is a classic over-spec — you've turned a one-line ticket into a two-week project."* Partly fair, which is why the tiers exist. But the counter holds: the reason this page shipped with "No projects" is that nobody distinguished empty from error from filtered, and shipping only E-1 rebuilds the same debt in nicer type. Tier 1 is three variants and a state-machine fix, and that is genuinely about a day.

*"Your contrast numbers are against a palette you invented."* Correct, and flagged. The ratios are arithmetically right for the hexes given; the hexes are placeholders. The structural findings (muted-grey body copy fails; border at 1.47:1 fails non-text contrast) hold for almost every default design system, which is why I'd bet on them — but bet, not assert.

*"A/B testing this is harder than you imply."* Also true. Day-one activation is slow-moving and noisy; at typical early-stage signup volumes an experiment on first-project creation may take longer to reach significance than the whole build took. If volume is low, ship Tier 1 on judgment, watch the variant distribution rather than a p-value, and reserve the A/B for Tier 3.
