# Settings Redesign — Engineering Handoff Packet

**Skills running:** `[SKILL]` (primary), with `[SKILL]` and `[SKILL]` folded in as the two sections `[SKILL]` explicitly requires ("Accessibility", "Content"). `[SKILL]` is *not* run — you're past critique, you're shipping.

**Ship date:** Thursday. **Today:** Wednesday, 16 Sep 2026 — so this is a two-day window, and the sequencing below assumes that.

---

## 0. What I'd ask you first (and what I'm assuming instead)

This ran unattended, so I couldn't ask. Here are the five questions that would actually change this document, and the assumption I proceeded under for each. **Correct any that are wrong before you send this — a wrong assumption here is a wrong spec, not a cosmetic issue.**

| # | Question I'd ask | Assumption I proceeded under |
|---|---|---|
| 1 | **What changed structurally?** Is this a visual reskin of the same settings pages, or a re-architecture of what lives where? | **Re-architecture.** Settings moved from a flat list of pages into grouped categories with sections inside them. This is the expensive assumption and it drives Section 5 (migration) — if it's a pure reskin, Section 5 collapses to almost nothing. |
| 2 | **Web, mobile, or both?** | **Responsive web app**, desktop-primary, with a mobile web breakpoint. Native app specs would need a separate gesture/navigation pass. |
| 3 | **Does a design system exist, and are these its components?** | **Yes, a design system exists**, and the redesign reuses it with 2–3 genuinely new components. Token names below are semantic placeholders — map them to your real token names before sending. |
| 4 | **Is it one release or phased?** | **One release behind a feature flag**, old settings kept alive for rollback. |
| 5 | **Are settings scoped by role/plan?** (admin vs. member, free vs. paid) | **Yes** — there's a role dimension. This is the single most common thing designers under-specify on settings work, so it gets its own matrix in Section 3.7. |

One more thing I'd say to your face: **"shipping to engineering Thursday" is a handoff, not a ship.** If Thursday is the day eng starts, the packet below is right. If Thursday is the day eng is expected to *finish estimating and commit to a date*, you additionally need Section 6 (open decisions) closed, not just listed — an estimate on top of five unresolved decisions is a guess wearing a number.

---

## 1. The short answer: what engineering needs from you

Twelve artifacts. Ranked by **what blocks them on day one** versus what you can deliver by end of week one. If you're short on time, produce 1–7 for Thursday and commit to dates for 8–12.

| # | Artifact | Why eng is blocked without it | Effort | Thursday? |
|---|---|---|---|---|
| 1 | **Scope & screen inventory** — every settings screen, marked *new / redesigned / unchanged / removed* | They cannot estimate. "Settings redesign" could be 3 screens or 30. | 1 hr | **Blocking** |
| 2 | **Component inventory** — new vs. modified vs. reused-as-is | Determines whether this is a week or a month. New components are 3–5x the cost of reused ones. | 1–2 hr | **Blocking** |
| 3 | **The save model decision** (Section 3.5) | Autosave vs. explicit save changes the API shape, the error handling, and the state management. Getting this wrong means a rewrite, not a tweak. | 30 min + a decision | **Blocking** |
| 4 | **Permissions/role matrix** (Section 3.7) | Every field needs a visibility and an editability answer per role. Missing this means eng invents one, and they'll invent "show it disabled" when you meant "hide it". | 1–2 hr | **Blocking** |
| 5 | **States matrix** — default, hover, focus, active, disabled, loading, error, empty, for every interactive element | Half of all build-time questions are "what does this look like when…". | 2 hr | **Blocking** |
| 6 | **Exact copy strings** (Section 4) — labels, helper text, every error, every empty state, every confirmation | Otherwise you get lorem, or worse, eng-written copy that ships. | 2–3 hr | **Blocking** |
| 7 | **URL / deep-link migration map** (Section 5) | Old settings URLs are in support docs, emails, bookmarks, and in-product links. Without the map, you ship 404s on day one. | 1 hr | **Blocking** |
| 8 | **Redlines / measurement specs** or a clean, inspectable design file with published components | Modern handoff is inspect-driven, so a well-built file counts. A messy file does not. | 2 hr (file cleanup) | Strongly preferred |
| 9 | **Responsive behavior** at each breakpoint (Section 3.8) | Mobile settings is where layouts break. | 1 hr | Strongly preferred |
| 10 | **Accessibility spec** (Section 3.10) — focus order, ARIA, keyboard, contrast results | Cheap now, expensive after build. Settings is form-dense, so a11y debt compounds here faster than anywhere else. | 2 hr | Strongly preferred |
| 11 | **Analytics events** (Section 6) | If you don't spec it now, it gets added in a follow-up sprint, and you'll have no before/after data on the redesign. | 45 min | Week 1 |
| 12 | **Acceptance criteria / QA checklist** (Section 7) | Gives you and QA a shared definition of done that isn't "looks right". | 1 hr | Week 1 |

**The five-minute version to paste into Slack:**

> For Thursday I'm bringing: the screen inventory with scope marked, the component list split into new/modified/reused, the save-model decision, the role-permission matrix, the full states matrix, final copy strings, and the old→new URL map. Redlines, responsive, and the a11y spec land Friday. Analytics events and acceptance criteria early next week. Three decisions still need an owner — they're listed at the bottom of the doc with dates.

---

## 2. Scope & screen inventory

Fill this in for your actual screens. The point of the table is that **"unchanged" and "removed" are load-bearing rows** — engineering estimates the diff, not the design.

| Screen / section | Status | Notes for eng |
|---|---|---|
| Profile | Redesigned | Layout only; fields unchanged |
| Account & security | Redesigned | Password + 2FA moved here from a separate page |
| Notifications | **New structure** | Flat toggle list → grouped by channel. New component: preference matrix |
| Billing & plan | Unchanged | Do not touch. Embedded as-is in new shell |
| Team / members | Redesigned | Role column added |
| Integrations | Redesigned | Card grid → list rows |
| Appearance / theme | **New** | Did not exist before |
| API keys | Unchanged | Do not touch |
| Advanced / danger zone | **New grouping** | Existing destructive actions consolidated |
| Legacy "Preferences" page | **Removed** | Contents split across Notifications and Appearance — see redirect map, Section 5 |

**Rule of thumb to state explicitly in the doc:** anything not listed is out of scope for this release. Say it in one sentence. It prevents the "while you're in there…" conversation on day three.

---

## 3. Handoff spec

### 3.1 Design tokens used

Map these semantic names to your real system before sending. Specify tokens, never raw hex or pixel values — a raw value is a value that drifts from the system the first time the system changes.

| Token | Proposed value | Usage in settings |
|---|---|---|
| `color-surface-page` | App background | Page canvas behind cards |
| `color-surface-raised` | Card background | Settings section cards |
| `color-border-subtle` | Divider | Between rows within a section |
| `color-border-default` | Card outline | Section card borders, input borders |
| `color-border-focus` | Focus ring | 2px ring, 2px offset, on every focusable element |
| `color-text-primary` | Body | Setting labels |
| `color-text-secondary` | Muted | Helper text under labels |
| `color-text-disabled` | Muted-er | Locked settings — **must still hit 4.5:1**, see 3.10 |
| `color-text-danger` | Error | Validation messages, danger zone |
| `color-accent-default` | Brand | Toggle on-state, primary buttons, selected nav item |
| `space-xs / sm / md / lg / xl` | 4 / 8 / 16 / 24 / 32 | Row padding, section gaps, card padding |
| `radius-md` | Card + input corner | Section cards, inputs |
| `font-label` | Body medium | Setting name |
| `font-helper` | Body small | Description under a setting |
| `font-section-title` | Heading small | Section headers |
| `shadow-raised` | Card elevation | Section cards (if not using borders) |
| `duration-fast` / `easing-standard` | 150ms / ease-out | Toggle, expand, hover |

**Gap to close before Thursday:** if the settings redesign introduces any value that is *not* already a token — a new spacing step, a new muted grey, a new card radius — flag it explicitly. Either it becomes a new token ([SKILL] change, needs a [SKILL] owner) or it snaps to an existing one (your call, make it now). Untokenized one-off values are how a design system quietly dies.

### 3.2 Layout & structure

| Region | Spec |
|---|---|
| Settings shell | Two-column: nav rail left, content right |
| Nav rail width | Fixed 240px desktop; collapses at `md` — see 3.8 |
| Content column | Max-width 720px, left-aligned within the remaining space (not centered — centering makes long pages feel like they drift) |
| Section card | `radius-md`, `space-lg` internal padding, `space-lg` gap between cards |
| Setting row | Label + helper text left, control right, vertically centered; `space-md` vertical padding; `color-border-subtle` divider between rows, none after the last row |
| Page header | Settings category name + one-line description; sticky on scroll at desktop |
| Save affordance | See 3.5 — position depends on the save model decision |

### 3.3 Components

The split that matters. **New** components are the estimate.

| Component | Status | Props / variants | Notes |
|---|---|---|---|
| `SettingsNavRail` | **New** | `items[]`, `activeId`, `collapsed` | Needs active, hover, focus states; keyboard arrow-key navigation within the list |
| `SettingRow` | **New** | `label`, `helperText`, `control`, `state: default \| disabled \| locked \| error`, `badge?` | The workhorse. Every setting is one of these. Build it once and everything else is composition |
| `PreferenceMatrix` | **New** | `rows[]`, `channels[]`, `values` | Notifications grid (setting × channel). Highest-risk new component — see edge cases in 3.9 |
| `SectionCard` | Modified | Add `title`, `description`, `footerAction?` slots | Existing card + header slots |
| `Toggle` | Reused as-is | — | Do not modify. If the redesign implies a new toggle size, that's a [SKILL] change, not a settings change |
| `Select`, `TextInput`, `Button`, `Banner`, `Modal` | Reused as-is | — | Confirm no visual overrides are hiding in the file |
| `UpgradePrompt` | Modified | Add inline/row variant | For plan-gated settings |

**Ask engineering directly:** "Are these three new components, or can `SettingRow` be composed from something you already have?" Ten minutes of that conversation on Thursday can remove a week.

### 3.4 States and interactions

| Element | State | Behavior |
|---|---|---|
| Setting row | Default | Label `color-text-primary`, helper `color-text-secondary` |
| Setting row | Hover | No background change (rows aren't clickable — only the control is). **If the whole row is clickable, say so explicitly**; mixed models here are a real bug source |
| Setting row | Disabled (no permission) | Control non-interactive, label at `color-text-disabled`, lock icon + tooltip: see copy in 4.3 |
| Setting row | Locked (plan gate) | Control non-interactive, inline `UpgradePrompt`, not a lock icon — different cause, different affordance |
| Setting row | Saving | Inline spinner replaces the control's right edge; control stays interactive-looking but rejects input |
| Setting row | Saved | Checkmark fades in for 2s, then out. No toast for a single-field save |
| Setting row | Error | Red border on control, message below in `color-text-danger`, control stays focused |
| Toggle | Click / Space / Enter | Fires save per 3.5 |
| Nav rail item | Active | `color-accent-default` left bar + medium weight. Never color alone (see 3.10) |
| Nav rail item | Focus | `color-border-focus` ring, visible against both surface tokens |
| Destructive action | Click | Opens confirmation modal, typed confirmation for account/workspace deletion only — not for every destructive action, or people stop reading it |
| Unsaved changes | Attempt to navigate away | Blocking dialog — copy in 4.4. **Only applies under explicit-save model** |

### 3.5 The save model — decide this before Thursday

This is the one that quietly determines the architecture. Engineering cannot build without an answer, and if they pick for you they'll pick whatever's easiest, which is usually explicit-save-everywhere.

**Recommendation: a hybrid, specified per control type.**

| Control type | Save model | Why |
|---|---|---|
| Toggle, radio, select | **Autosave on change** | The change *is* the intent. A Save button after a toggle is a second, meaningless confirmation |
| Text input (name, email, URL) | **Explicit save**, per-section | Mid-typing autosave produces garbage states and noisy API traffic |
| Destructive / structural (delete, transfer ownership, change plan) | **Explicit + confirmation modal** | Irreversible |

**What this forces engineering to handle, and what you must spec:**

1. **Optimistic vs. pessimistic UI for autosave.** Recommend optimistic — flip the toggle instantly, revert with an error banner if the request fails. Spec the revert: control returns to its previous value, inline error appears, error persists until the next successful change on that row.
2. **Rapid toggling.** User flips a toggle four times in two seconds. Debounce 300ms and send the final value; do not queue four requests.
3. **Dependent settings.** If turning off a parent disables three children, spec whether children are saved as off, or retained-and-hidden. Recommend **retained** — turning the parent back on restores prior child values, which is what people expect and almost nobody builds.
4. **Concurrent edits.** Two admins editing team settings simultaneously. Minimum viable answer: last write wins, and the loser sees a "this changed while you were editing" banner on next load. Say this out loud or it silently becomes "last write wins, no banner."
5. **Explicit-save sections** need: dirty-state detection, Save enabled only when dirty, Cancel that reverts, and the navigation-guard dialog from 3.4.

### 3.6 Responsive behavior

| Breakpoint | Changes |
|---|---|
| `lg` ≥ 1024px | Two-column. Nav rail fixed 240px, content max-width 720px |
| `md` 768–1023px | Nav rail collapses to icon-only with tooltips, or to a top dropdown. **Pick one and say which** — icon-only settings nav is often unreadable without labels; the dropdown is the safer call |
| `sm` < 768px | Single column. Nav becomes a list; tapping a category pushes to a detail view with a back affordance. Setting rows stack: label + helper above, control below, left-aligned |
| All | Controls remain ≥ 44×44px touch target regardless of visual size |

**Mobile-specific edge case to spec:** the `PreferenceMatrix` (setting × channel grid) cannot survive a 375px viewport as a grid. Spec the mobile form explicitly — recommend collapsing to one expandable row per setting, with channel toggles revealed inside. If you don't spec it, engineering will horizontally scroll it, and horizontally-scrolled settings are unusable.

### 3.7 Permissions matrix

Every setting needs three answers: **who sees it**, **who edits it**, **what non-editors see instead**. The third column is the one designers skip.

| Setting group | Owner | Admin | Member | Non-editor sees |
|---|---|---|---|---|
| Profile (own) | Edit | Edit | Edit | — |
| Account & security (own) | Edit | Edit | Edit | — |
| Notifications (own) | Edit | Edit | Edit | — |
| Team members | Edit | Edit | **View** | Row visible, controls disabled + lock icon |
| Roles & permissions | Edit | View | **Hidden** | Nav item not rendered |
| Billing & plan | Edit | View | **Hidden** | Nav item not rendered |
| Integrations | Edit | Edit | View | Disabled + lock icon |
| Danger zone (delete workspace) | Edit | **Hidden** | **Hidden** | Section not rendered |

**The design rule underneath this:** *disabled for "you could have this permission," hidden for "this isn't your concern."* Showing a member the billing page greyed out advertises a door they can't open. Showing a member a disabled team-role dropdown correctly signals "ask your admin."

**Also spec:** what happens to a user whose role changes *while the page is open*. Minimum answer: on next save attempt, return a permission error with the copy in 4.3 and reload the section.

### 3.8 Edge cases

- **Empty state — no team members:** shouldn't be reachable (you're always a member of your own team), but if the list can be empty, spec it. Copy in 4.2.
- **Empty state — no integrations connected:** illustration + one-line explanation + primary CTA. Copy in 4.2.
- **Long text:** workspace names, email addresses, and connected-account names are the overflow risks. Spec: labels wrap to max two lines then ellipsize with a `title` attribute; email addresses use middle-truncation, not end-truncation, so the domain stays visible.
- **Loading:** skeleton rows matching the final row height, not a centered spinner. Settings loads fast enough that a spinner reads as a flash. Spec skeleton count per section so the page doesn't jump.
- **Slow connection:** if a save exceeds 5s, swap the inline spinner for the "still saving" copy in 4.1. Do not fail silently.
- **Error — section failed to load:** per-section error state with a Retry action. Do **not** fail the whole settings page because billing timed out.
- **i18n:** German and Finnish labels run roughly 30% longer than English. The label/control row must not assume a fixed label width. Flag any right-aligned control that would collide.
- **RTL:** nav rail mirrors to the right; toggle travel direction mirrors; the left accent bar on the active nav item becomes a right bar.
- **Zoom to 200%:** two-column must reflow to single column rather than horizontally scroll (WCAG 1.4.10).
- **Browser autofill:** password managers will inject into account/security fields. Confirm the styling survives autofill's forced background color.
- **Unsaved changes + session expiry:** if the session dies with unsaved text-field changes, the user must not lose them silently. Minimum: preserve field values through the re-auth flow.

### 3.9 Animation

| Element | Trigger | Animation | Duration | Easing |
|---|---|---|---|---|
| Toggle | Change | Knob translate + track color cross-fade | 150ms | `easing-standard` |
| Saved checkmark | Save success | Fade in, hold 2s, fade out | 150 / 2000 / 150ms | `easing-standard` |
| Section expand | Click header | Height auto-expand + content fade | 200ms | `ease-out` |
| Nav item | Hover | Background fade | 100ms | `linear` |
| Error message | Appear | Fade + 4px slide down | 150ms | `ease-out` |
| Mobile category push | Tap | Slide-in from right | 250ms | `ease-out` |

**Required:** everything above respects `prefers-reduced-motion: reduce` — state changes still occur, transitions drop to 0ms. This is a one-line media query for engineering and a WCAG 2.3.3 item; specify it, don't assume it.

### 3.10 Accessibility spec (WCAG 2.1 AA)

Running `[SKILL]` against the described design. I have no screenshots or code, so **I cannot report measured contrast ratios** — reporting numbers I didn't measure would be fabrication. What follows is the required bar, plus the specific places settings redesigns fail, so you can measure the right five things instead of all forty.

**Contrast — measure these five before Thursday:**

| Element | Required ratio | Why it usually fails |
|---|---|---|
| Helper text (`color-text-secondary`) on card surface | 4.5:1 | Muted greys on white land near 4.0:1 and pass a designer's eye |
| **Disabled/locked setting labels** | 4.5:1 | Most systems exempt disabled controls — but a *locked-by-permission* label is informational content the user must read, not a disabled control. Treat it as body text |
| Toggle **off**-state track vs. card background | 3:1 (1.4.11) | The off state is the one that fails. On-state uses brand color and usually passes |
| Input borders and row dividers vs. surface | 3:1 (1.4.11) | Hairline dividers at low opacity fail routinely |
| Focus ring vs. **both** page and card surfaces | 3:1 | A ring tuned against white disappears on the raised card |

**Findings and requirements:**

| # | Requirement | WCAG | Severity | Spec |
|---|---|---|---|---|
| 1 | Every setting control has a programmatic label | 3.3.2 | Critical | Toggles use `<label for>` or `aria-labelledby` pointing at the row label. A visually-adjacent label is not a label |
| 2 | Helper text is associated, not just nearby | 1.3.1 | Major | `aria-describedby` from control → helper text id |
| 3 | Autosave results are announced | 4.1.3 | **Critical** | This is the biggest a11y risk in the whole redesign. Under autosave, a screen-reader user flips a toggle and gets *no feedback*. Requires `aria-live="polite"` region announcing "Email notifications on, saved" / `aria-live="assertive"` for failures |
| 4 | Toggle exposes state | 4.1.2 | Critical | `role="switch"` + `aria-checked`, or a native checkbox. Not a styled `<div>` with a click handler |
| 5 | Nav rail is a landmark with current-page marking | 1.3.1 / 4.1.2 | Major | `<nav aria-label="Settings">`, active item carries `aria-current="page"` |
| 6 | Active nav item is not indicated by color alone | 1.4.1 | Major | Accent bar + weight change, which the spec already has — confirm the bar survives forced-colors mode |
| 7 | Logical focus order | 2.4.3 | Major | Nav rail → page header → sections top-to-bottom → within a row, control after label. No positive `tabindex` |
| 8 | Visible focus on every interactive element | 2.4.7 | Critical | Including the toggle, the nav items, and the danger-zone buttons. Never `outline: none` without a replacement |
| 9 | Error identification is textual | 3.3.1 | Critical | Red border alone fails. Text message, `role="alert"`, and `aria-invalid="true"` on the control |
| 10 | Touch targets ≥ 44×44px | 2.5.5 | Major | A 20×32px visual toggle needs a 44px padded hit area |
| 11 | Confirmation modals trap and restore focus | 2.4.3 / 2.1.2 | Critical | Focus moves to the modal, Escape closes, focus returns to the triggering button |
| 12 | Reflow at 200% zoom / 320px | 1.4.10 | Major | Single column, no horizontal scroll — see the `PreferenceMatrix` note in 3.6 |
| 13 | Reduced motion respected | 2.3.3 | Minor | See 3.9 |
| 14 | Lock icons have accessible names | 1.1.1 | Major | `aria-label="Requires admin permission"`, not a decorative icon with a visual-only tooltip |

**Keyboard map to hand over:**

| Element | Tab | Enter / Space | Arrow keys | Escape |
|---|---|---|---|---|
| Nav rail | One stop for the whole list | Activate item | Move between items | — |
| Toggle | Stop | Toggle + save | — | — |
| Select | Stop | Open | Move options | Close, revert |
| Text input | Stop | Submit section (explicit-save only) | — | Revert field |
| Danger button | Stop | Open modal | — | — |
| Modal | Trapped | Confirm | — | Cancel + restore focus |

---

## 4. UX copy spec

Running `[SKILL]`. Engineering will ship whatever string is in the file, so every string needs to be final. Assumed voice: **plain, calm, second person, no exclamation marks.** Settings is a place people go when something is wrong or they want control — reassurance beats personality.

### 4.1 Save states

| Element | Copy | Note |
|---|---|---|
| Saving (inline) | `Saving…` | Only if it exceeds ~400ms; below that it's a flash |
| Saved (inline) | `Saved` + checkmark | 2s, then fades |
| Slow save (> 5s) | `Still saving…` | Prevents the "is it broken" tab-refresh |
| Save failed (autosave) | `Couldn't save. Check your connection and try again.` | What happened + how to fix. No error codes in the UI |
| Save failed (server error) | `Couldn't save right now. We're looking into it.` + Retry | Don't blame the user for a 500 |
| Explicit save button | `Save changes` | Verb + object. Not "Submit", not "OK" |
| Cancel | `Cancel` | Reverts the section |

### 4.2 Empty states

Pattern: **what this is + why it's empty + how to start.**

| Context | Heading | Body | CTA |
|---|---|---|---|
| No integrations | `No integrations yet` | `Connect the tools your team already uses so data flows automatically.` | `Browse integrations` |
| No API keys | `No API keys` | `Create a key to let your own applications access this workspace.` | `Create key` |
| No team members | `You're the only member` | `Invite teammates to share this workspace.` | `Invite people` |
| Search returned nothing (if settings search exists) | `No settings match "{query}"` | `Try a different word, or browse the categories on the left.` | — |

### 4.3 Permission and plan gates

| Context | Copy | Note |
|---|---|---|
| Locked by role (tooltip on lock icon) | `Only admins can change this.` | Names the role, so the user knows who to ask |
| Locked by role (inline, larger surfaces) | `Only admins can change team roles. Ask an admin if you need this updated.` | Gives the next action |
| Locked by plan | `Available on Pro.` + `Upgrade` link | Short. Don't sell in settings |
| Permission revoked mid-session | `Your permissions changed. Refresh to see the latest settings.` + `Refresh` | See 3.7 |

### 4.4 Confirmations and destructive actions

Rule: **the button says the action, never "OK"** — a user who reads only the buttons should still make the right choice.

| Context | Title | Body | Confirm | Cancel |
|---|---|---|---|---|
| Unsaved changes on navigate | `Leave without saving?` | `Your changes to {section} will be lost.` | `Leave` | `Keep editing` |
| Remove team member | `Remove {name}?` | `They'll lose access to this workspace immediately. Their work stays.` | `Remove member` | `Cancel` |
| Revoke API key | `Revoke this key?` | `Any application using it will stop working right away. This can't be undone.` | `Revoke key` | `Cancel` |
| Delete workspace | `Delete {workspace}?` | `This permanently deletes all data for everyone in this workspace. This can't be undone.` + typed confirmation | `Delete workspace` | `Cancel` |
| Disable 2FA | `Turn off two-factor authentication?` | `Your account will be less secure. You can turn it back on any time.` | `Turn off` | `Cancel` |

### 4.5 Validation errors

Pattern: **what happened + how to fix.** Never "Invalid input."

| Field | Error copy |
|---|---|
| Email, malformed | `Enter a valid email address.` |
| Email, already in use | `That email is already connected to another account.` |
| Name, empty | `Name can't be empty.` |
| Name, too long | `Name must be 50 characters or fewer.` |
| Password, too weak | `Use at least 12 characters, including a number.` |
| URL, malformed | `Enter a full URL, starting with https://` |
| Workspace name, taken | `That name is taken. Try another.` |

### 4.6 Localization notes for translators

- `{name}`, `{workspace}`, `{query}` are variables — do not translate, do not reorder out of grammatical position.
- `Saved` is a status, not a past-tense verb about the user's action. Some languages need a different form.
- `Only admins can change this` — "admin" maps to your product's role name; confirm the role name itself is localized consistently everywhere.
- Toggle labels must read as states, not commands, so they make sense next to an on/off control.
- Allow ~30% expansion on every label. See the i18n note in 3.8.

---

## 5. Migration and rollout — the part redesigns forget

This is why the re-architecture assumption mattered. If settings moved, **every old pointer breaks**, and settings URLs are pointed at from more places than almost any other part of a product.

**Deliver a redirect map.** Old path → new path, one row per removed or moved page:

| Old URL | New URL | Notes |
|---|---|---|
| `/settings/preferences` | `/settings/notifications` | Page split — see next row |
| `/settings/preferences#theme` | `/settings/appearance` | Anchor-level redirect needed, not just path-level |
| `/settings/password` | `/settings/account#password` | Now a section, not a page — deep link must scroll and focus |
| `/settings/team` | `/settings/members` | Rename only |

**Then audit who points at those URLs:**

1. **In-product links** — "Manage notification settings" in email footers, empty-state CTAs, upgrade prompts, error messages. Grep the codebase for `/settings/`.
2. **Transactional emails** — footer unsubscribe and preference links. These live in an email template system, often outside the main repo, and they are the most-clicked settings links you have.
3. **Help docs / support macros** — someone owns these; tell them Thursday, not after launch.
4. **Customer bookmarks** — you can't fix these, which is exactly why the redirects must be permanent, not temporary.

**Rollout:**

| Item | Spec |
|---|---|
| Feature flag | `settings_redesign_v2`, per-workspace |
| Rollout order | Internal → 5% → 25% → 100%, one step per day minimum |
| Rollback | Old settings routes stay live behind the flag for two full weeks after 100% |
| Kill criteria — say these now | Settings-related support tickets up > 2x baseline, or save-failure rate > 1%, or successful-save rate on any single setting drops > 20% vs. baseline |

**Take your own baseline before Thursday.** Current settings page views, saves per setting, and support ticket volume. After launch you cannot reconstruct the "before" number, and without it you'll be arguing about the redesign from vibes.

---

## 6. Analytics events to spec

Ten minutes of your time; otherwise it's a follow-up ticket and you get no read on the redesign.

| Event | Properties | Answers |
|---|---|---|
| `settings_viewed` | `category`, `entry_point` | Which categories matter; how people get here |
| `setting_changed` | `setting_key`, `old_value`, `new_value`, `save_model` | Which settings are actually used |
| `setting_save_failed` | `setting_key`, `error_type` | Kill-criteria metric |
| `settings_search` | `query`, `result_count` | Whether the new structure is findable — a high-volume search for something that has a category is a navigation failure |
| `settings_nav_used` | `from_category`, `to_category` | Whether the grouping matches people's mental model |
| `permission_blocked_view` | `setting_key`, `role` | Whether the disabled-vs-hidden calls in 3.7 are right |

---

## 7. Open decisions — each needs an owner and a date

Do not hand over a spec with these buried in prose. Put them at the top of the doc as a table. **An estimate given on top of unresolved decisions is not an estimate.**

| # | Decision | Recommendation | Owner | Needed by |
|---|---|---|---|---|
| 1 | Save model: autosave, explicit, or hybrid | Hybrid per 3.5 | You + eng lead | **Thursday** |
| 2 | Disabled vs. hidden for each gated setting | Per 3.7 matrix | You | **Thursday** |
| 3 | `md` breakpoint nav: icon-rail or dropdown | Dropdown | You | **Thursday** |
| 4 | Are the 3 "new" components actually new, or composable from existing? | Ask eng | Eng lead | Thursday, in the meeting |
| 5 | Dependent settings: children retained or reset when parent is off | Retained | You + eng | Friday |
| 6 | Concurrent edit handling | Last-write-wins + banner | Eng lead | Friday |
| 7 | Do new tokens get added to the design system, or snap to existing? | Snap to existing where possible | Design system owner | Friday |
| 8 | Who updates help docs and email templates? | — | Support + growth | Thursday (notify), week 2 (done) |

---

## 8. Acceptance criteria / QA checklist

Hand this over so "done" isn't a matter of taste.

- [ ] Every setting in the Section 2 inventory renders, saves, and persists across reload
- [ ] Every role in the 3.7 matrix sees exactly the specified visibility and editability
- [ ] Autosave: optimistic update, revert on failure, inline error, no toast
- [ ] Explicit-save sections: dirty detection, Save disabled when clean, Cancel reverts, navigation guard fires
- [ ] Rapid-toggle debounce sends one request, final value wins
- [ ] Every old URL in the Section 5 map redirects, including anchors
- [ ] Keyboard-only: complete every settings task without a mouse
- [ ] Screen reader: every autosave is announced (the item most likely to be missed)
- [ ] Contrast: the five measurements in 3.10 pass
- [ ] 200% zoom and 320px width: no horizontal scroll
- [ ] `prefers-reduced-motion` honored
- [ ] Longest realistic strings (German + a 60-char workspace name) don't break any row
- [ ] RTL renders correctly
- [ ] All six analytics events fire with correct properties
- [ ] Feature flag off restores old settings with no data loss

---

## Stress Test

**What's weakest here.** This spec is built on assumptions, not on your design file. Every table above is a *shape* that's right for a settings redesign in general; the contents are right only if my five assumptions in Section 0 hold. The re-architecture assumption is the load-bearing one — if this is a visual reskin, Section 5 is wasted effort and I've inflated the Thursday list by a third. **Check assumption 1 first.**

**The assumption most likely to be wrong.** That a design system exists and this reuses it. If the settings redesign was done in isolation — a common pattern, because settings is where designers get free rein — then half the "reused as-is" components in 3.3 are quietly modified, engineering discovers this in week two one component at a time, and the estimate doubles. **Cheap test:** open the file and count how many components are detached from the library. If it's more than two, that's your real Thursday risk, not anything in this document.

**What a smart engineer will say on Thursday.** Three things. (1) *"This is a lot of spec for something we'd have figured out."* Partly fair — items 8–10 on the Thursday list are genuinely nice-to-have if the team is senior and co-located. Items 1–7 are not; every one of them is a decision only you can make. (2) *"Why is settings this complicated?"* Because permissions × states × save-model is a combinatorial space, and settings is the densest instance of it in the product. That's the honest answer. (3) *"Can we cut the PreferenceMatrix?"* You should take this seriously. It's the only genuinely novel component, it has the worst mobile story, and a grouped list of toggles would deliver most of the value. If Thursday's estimate comes back bigger than you want, **that's the cut.**

**What I'd push back on in your own framing.** "What do they need from me?" treats handoff as a one-way delivery. The three highest-value items on that Thursday list — the save model, the component new/reuse split, and the mobile nav decision — are all things you should decide *with* the eng lead in a 45-minute working session, not hand over finished. A spec that arrives fully resolved on decisions engineering has better information about is a spec that gets quietly renegotiated in week two. **Book the 45 minutes.**

**What this document can't tell you.** Whether the redesign is *good*. This is `[SKILL]`, not `[SKILL]` — it assumes the design is settled and the job is transmitting it accurately. If you have any lingering doubt about the information architecture, Thursday is the last cheap moment to test it: five users, ten minutes each, "find where you'd turn off email notifications." After the build starts, that same finding costs a sprint.
