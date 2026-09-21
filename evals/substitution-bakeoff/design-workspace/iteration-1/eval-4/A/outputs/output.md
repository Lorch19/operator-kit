# Accessibility Audit: Dark Theme — Grey-on-Grey + Blue Primary Button

**Skill:** `design-tools/accessibility-review` (primary), with the remediation spec in `design-tools/design-handoff` format
**Standard:** WCAG 2.1 AA
**Date:** 2026-09-16

---

## Verdict first

**No — not as described. But the thing you're worried about is probably not the thing that blocks you.**

You flagged the mid-blue button. That's the *least* likely failure in what you described. A mid-blue on near-black almost always clears the 3:1 non-text threshold — `#2563EB` on `#0A0A0A` measures **3.83:1**, `#0D6EFD` measures **4.40:1**. The blue fill is fine.

The ship blocker is the part you mentioned in passing: **"lots of grey-on-grey."** That phrase describes the single highest-volume WCAG failure mode in dark themes, and it fails in a way that standard spot-checking misses — I'll show exactly how below.

There is also a *second* risk hiding inside the blue button that you didn't ask about: the white **label on** the blue is squeezed between two competing requirements, and if your blue is on the lighter end of "mid," the label fails even though the fill passes.

Ship gate at the bottom. Read the "10-minute self-check" first — it converts this from my guesswork into your measured answer.

---

## Questions I would have asked (and the assumptions I'm proceeding under)

This ran unattended with no hexes, no screenshots, no code. Here is what I would have asked and what I assumed instead. Every number below is traceable to these assumptions — swap your real values into the thresholds and the verdict recomputes.

| # | Question I'd ask | Assumption I proceeded under | Does the answer change the verdict? |
|---|---|---|---|
| 1 | What are the actual hex values — page bg, each surface tier, each grey text token, the blue? | Page `#0A0A0A`–`#121212`; surfaces `#1E1E1E` / `#27272A`; greys in the `#666`–`#A1A1AA` band; blue in the `#2563EB`–`#3B82F6` band | **Yes — decisively.** This is the one question that matters. |
| 2 | Is the near-black behind the button the *page*, or an elevated card? | Both — I audit against both, because the answer differs | **Yes.** A card surface shrinks every ratio. |
| 3 | Is the grey-on-grey *text on surface*, or *border/divider on surface*? | Both — they have different thresholds (4.5:1 vs 3:1) | Yes — borders get a lower bar. |
| 4 | Does one blue token serve both the button fill *and* inline links? | Assumed yes — this is the common setup | **Yes.** One token cannot do both jobs. See F-04. |
| 5 | Is dark theme the only theme, or is there a light theme users can switch to? | Assumed dark-only | Yes — a compliant light theme is a mitigation, not a fix. |
| 6 | Is this consumer-facing in the EU/UK, or sold to enterprise/public sector? | Assumed yes to at least one | Changes the *cost* of shipping non-compliant, not the finding. |
| 7 | What's the body font weight? | Assumed 400; flagging if 300 | Yes — see T-01, the math is weight-blind. |

**Proceeding under those assumptions, the audit below is what I'd hand an engineer.**

---

## 10-minute self-check (do this before you read the rest)

You do not need an audit tool to resolve this. Three measurements answer the ship question.

**Step 1 — Find your darkest *surface* that carries body text.** Not the page background. The card, the input field, the dropdown, the table row. Call it `S`.

**Step 2 — Look up the cheat sheet.** The darkest grey that still passes 4.5:1 for body text:

| Your surface `S` | Darkest passing body grey | Ratio at that point |
|---|---|---|
| `#0A0A0A` (near-black page) | `#797979` | 4.55:1 |
| `#121212` (Material dark) | `#7D7D7D` | 4.55:1 |
| `#1E1E1E` (card / elevated) | `#858585` | 4.52:1 |
| `#27272A` (input / higher tier) | `#8E8E8E` | 4.55:1 |

**If any grey text token is darker than the value in row `S`, you have a WCAG 1.4.3 failure and you should not ship it.** Most dark themes I'd expect to see land their secondary text around `#71717A` or `#6B7280` — both of which measure **3.45:1 on `#1E1E1E`**. That is a fail.

**Step 3 — Check your blue twice, not once.**
- Blue fill vs. the surface directly behind it → needs **≥ 3:1**
- Your button label vs. the blue fill → needs **≥ 4.5:1** (or 3:1 if the label is ≥18.66px bold / ≥24px regular)

If both pass, the button ships. If only the first passes, your label is the problem, not the button.

---

## Summary

**Issues:** 9 | **Critical:** 3 | **Major:** 4 | **Minor:** 2

Severity here means: *Critical* = blocks ship, is a defensible legal claim, and degrades the product for sighted users too. *Major* = fix before the next release. *Minor* = backlog.

---

## Findings

| # | Issue | WCAG | Severity | Fix |
|---|---|---|---|---|
| **F-01** | **Grey text validated against the page background, then reused on elevated surfaces.** A grey chosen to clear 4.5:1 on `#121212` silently drops below threshold on a `#1E1E1E` card and further on a `#27272A` input. `#8A8A8A` measures 5.43:1 on the page but **4.31:1 on `#27272A`** — passes, then fails, same token. | 1.4.3 | **Critical** | Validate every text token against the *lightest* surface it can land on, not the page. Ship a per-tier text token (see remediation spec). |
| **F-02** | **Secondary / tertiary / meta text below 4.5:1.** The typical dark-theme "muted" greys: `#71717A` on `#1E1E1E` = **3.45:1**; `#6B7280` on `#1F2937` = **3.04:1**; `#666666` on `#222222` = **2.77:1**. All fail body-text threshold. This is almost certainly what "lots of grey-on-grey" means. | 1.4.3 | **Critical** | Lift muted text to ≥ the Step-2 cheat-sheet value for its surface. `#949494` clears 4.5:1 on every tier up to `#27272A` (4.91:1). |
| **F-03** | **Placeholder text.** Dark themes routinely set placeholders around `#5A5A5A`, which on a `#1E1E1E` input measures **2.42:1**. Placeholders are *not* exempt from 1.4.3 (only *disabled* controls are), and placeholder-as-label is already a 3.3.2 failure. | 1.4.3, 3.3.2 | **Critical** | Raise placeholder to ≥4.5:1 **and** add a persistent visible label above the field. Never use placeholder as the only label. |
| **F-04** | **One blue token serving both button fill and inline link text.** These have opposite requirements on dark. `#2563EB` works as a fill (3.83:1 vs page) but **fails as link text at 3.62:1 on `#121212`**. A blue light enough to be readable *as text* (`#3B82F6` = 5.09:1) is too light to carry a white label at 4.5:1 (**3.68:1** — fail). | 1.4.3 | **Major** | Split into two tokens: `accent-fill` (darker, carries white label) and `accent-text` (lighter, ≥4.5:1 as text). Do not reuse one for both. |
| **F-05** | **White label on the blue fill — the squeeze.** On a `#0A0A0A` page the fill luminance must be **≥0.109** to clear 3:1 against the page, and **≤0.183** for a white label to clear 4.5:1. That window exists but is narrow. `#0D6EFD` sits at 0.1833 — exactly on the edge, label at **4.50:1**. One nudge lighter and the label fails. | 1.4.3 | **Major** | Target luminance **0.15–0.17**. `#2F6FE4` (fill 4.26:1 vs page, white label 4.65:1) sits comfortably inside with margin on both sides. |
| **F-06** | **Input and control borders below 3:1.** The default dark-theme border `#3F3F46` measures **1.79:1 on `#121212`** and **1.43:1 on `#27272A`**. A form field's boundary is what identifies it as a field — 1.4.11 applies. | 1.4.11 | **Major** | Borders that identify a control need ≥3:1: `#6B7280` (3.88:1 on `#121212`) minimum, `#8A8A8A` preferred. Purely decorative dividers are exempt — keep those subtle, but don't let one token serve both roles. |
| **F-07** | **Focus ring likely tinted with the brand accent.** A blue ring against a blue button is nearly invisible: `#60A5FA` ring on a `#2563EB` fill = **2.03:1**. The ring must clear 3:1 against *both* the component it surrounds *and* the background behind it. | 2.4.7, 1.4.11 | **Major** | Use a neutral high-contrast ring: `#FFFFFF` measures **4.65:1 vs the `#2F6FE4` fill** and **19.80:1 vs the page** — clears both. Add a 2px dark offset so it also survives on light surfaces. |
| **F-08** | **State changes signalled by fill alone.** Hover/selected/active on near-black often shift by 3–5% luminance, which is imperceptible and fails the state-identification clause of 1.4.11. | 1.4.11, 1.4.1 | Minor | Ensure any two states differ by ≥3:1 *or* add a non-colour cue (border weight, icon, underline, checkmark). |
| **F-09** | **Error/success states carried by colour tint on near-black.** Desaturated reds and greens lose most of their differentiation against a near-black ground, and a red-tinted border at low contrast conveys nothing to a low-vision or colourblind user. | 1.4.1, 3.3.1 | Minor | Pair every status colour with an icon **and** text. Error text itself must clear 4.5:1 — a red that reads on white will not read on near-black. |

---

## Color Contrast

### Grey text on dark surfaces — where the failures actually are

`*` = passes 4.5:1 (body text) · `~` = 3:1 only, large text (≥18.66px bold / ≥24px) · `X` = fails both

| Foreground | on `#0A0A0A` | on `#121212` | on `#18181B` | on `#1E1E1E` | on `#27272A` |
|---|---|---|---|---|---|
| `#FFFFFF` | 19.80 `*` | 18.73 `*` | 17.72 `*` | 16.67 `*` | 14.89 `*` |
| `#EDEDED` | 16.91 `*` | 16.00 `*` | 15.13 `*` | 14.24 `*` | 12.72 `*` |
| `#D4D4D8` | 13.40 `*` | 12.67 `*` | 11.99 `*` | 11.28 `*` | 10.08 `*` |
| `#B4B4B8` | 9.58 `*` | 9.06 `*` | 8.57 `*` | 8.07 `*` | 7.21 `*` |
| `#A1A1AA` | 7.72 `*` | 7.31 `*` | 6.91 `*` | 6.50 `*` | 5.81 `*` |
| `#949494` | 6.53 `*` | 6.18 `*` | 5.84 `*` | 5.50 `*` | 4.91 `*` |
| `#8A8A8A` | 5.73 `*` | 5.43 `*` | 5.13 `*` | 4.83 `*` | **4.31 `~`** |
| `#7F7F7F` | 4.94 `*` | 4.68 `*` | **4.42 `~`** | **4.16 `~`** | 3.72 `~` |
| `#71717A` | 4.10 `~` | 3.88 `~` | 3.67 `~` | 3.45 `~` | 3.08 `~` |
| `#6B7280` | 4.10 `~` | 3.88 `~` | 3.66 `~` | 3.45 `~` | 3.08 `~` |
| `#666666` | 3.45 `~` | 3.26 `~` | 3.09 `~` | **2.90 `X`** | **2.59 `X`** |
| `#52525B` | 2.56 `X` | 2.42 `X` | 2.29 `X` | 2.16 `X` | 1.93 `X` |

**Read the bold cells.** `#8A8A8A` and `#7F7F7F` are the trap: they pass on the page background and fail one surface tier up. That is F-01, and it is why a spot-check against the page background gives a false green.

### The blue button — both checks

| Blue | Luminance | Fill vs `#0A0A0A` (need 3:1) | `#FFF` label (need 4.5:1) | Verdict |
|---|---|---|---|---|
| `#1E40AF` blue-800 | 0.0704 | **2.27 ✗** | 8.72 ✓ | Fill too dark |
| `#1D4ED8` blue-700 | 0.1067 | **2.95 ✗** | 6.70 ✓ | Fill just misses |
| `#2E67D8` | 0.1524 | 3.82 ✓ | 5.19 ✓ | **Passes both** |
| `#2563EB` blue-600 | 0.1532 | 3.83 ✓ | 5.17 ✓ | **Passes both** |
| `#2A6FDB` | 0.1698 | 4.14 ✓ | 4.78 ✓ | **Passes both** |
| `#2F6FE4` | 0.1757 | 4.26 ✓ | 4.65 ✓ | **Passes both — best margin** |
| `#0D6EFD` Bootstrap | 0.1833 | 4.40 ✓ | **4.50 ⚠** | On the knife edge |
| `#007AFF` iOS | 0.2114 | 4.93 ✓ | **4.02 ✗** | Label fails |
| `#3B82F6` blue-500 | 0.2355 | 5.38 ✓ | **3.68 ✗** | Label fails |
| `#60A5FA` blue-400 | 0.3630 | 7.79 ✓ | **2.54 ✗** | Label fails badly |

**The squeeze, stated precisely.** On a `#0A0A0A` page:
- fill luminance must be **≥ 0.1091** → 3:1 against the page (1.4.11)
- fill luminance must be **≤ 0.1833** → white label at 4.5:1 (1.4.3, normal text)
- relaxing the label to ≥18.66px bold raises the ceiling to **0.30**

The window is real but only ~0.07 luminance wide. Aim for the middle of it, not an edge.

### The blue as *text* (links) — different answer

| Blue | as text on `#121212` | Verdict |
|---|---|---|
| `#2563EB` | **3.62** | ✗ Fails |
| `#3B82F6` | 5.09 | ✓ |
| `#0A84FF` | 5.14 | ✓ |
| `#409CFF` | 6.62 | ✓ |
| `#60A5FA` | 7.37 | ✓ |

Note `#2563EB` appears as a pass in the button table and a fail here. **That is F-04.** Same colour, two jobs, one of them impossible.

### Borders, dividers, focus rings

| Colour | vs `#0A0A0A` | vs `#121212` | vs `#1E1E1E` | vs `#27272A` |
|---|---|---|---|---|
| `#3F3F46` | 1.90 ✗ | 1.79 ✗ | 1.60 ✗ | 1.43 ✗ |
| `#52525B` | 2.56 ✗ | 2.42 ✗ | 2.16 ✗ | 1.93 ✗ |
| `#6B7280` | 4.10 ✓ | 3.88 ✓ | 3.45 ✓ | 3.08 ✓ |
| `#8A8A8A` | 5.73 ✓ | 5.43 ✓ | 4.83 ✓ | 4.31 ✓ |

Focus ring, checked against **both** neighbours:

| Ring | vs `#2563EB` fill | vs `#0A0A0A` page | Verdict |
|---|---|---|---|
| `#FFFFFF` | 5.17 ✓ | 19.80 ✓ | **Use this** |
| `#EDEDED` | 4.41 ✓ | 16.91 ✓ | Also fine |
| `#93C5FD` | **2.87 ✗** | 10.98 ✓ | Fails against the button |
| `#60A5FA` | **2.03 ✗** | 7.79 ✓ | Fails badly |
| `#A1A1AA` | **2.02 ✗** | 7.72 ✓ | Fails badly |

---

## Three dark-theme failure modes the contrast math does not catch

These are why "it passes the checker" and "it ships" are not the same sentence in a dark theme.

**T-01 — Contrast math is font-weight-blind, and light-on-dark blooms.**
On a dark ground, light text optically spreads into the background (halation), thinning perceived stroke weight. A 4.6:1 grey at weight 300 is *measurably compliant* and *functionally worse* than the same ratio at weight 400 in a light theme — and it is materially worse for readers with astigmatism, who are ~30–40% of the adult population. **Rule: no font weight below 400 in dark mode for body text; prefer 450–500 for anything below 16px.** If your greys pass and the theme still feels mushy, this is why.

**T-02 — Pure black is a worse background than near-black.**
`#FFFFFF` on `#000000` is 21:1 — the maximum possible, and one of the *worst* choices available. Maximum contrast maximises halation, and on OLED, pure black pixels have a different response time to lit ones, producing visible smearing during scroll. **Use `#121212`–`#1A1A1A` as the page, and `#EDEDED` rather than `#FFFFFF` as primary text (16.00:1 — still enormous headroom).** You described "near-black," which suggests you already avoided this; confirm it isn't `#000` anywhere.

**T-03 — Elevation-by-lightness is the root cause of the grey-on-grey problem.**
In a light theme you show elevation with a shadow. On near-black, shadows are invisible, so every dark design system signals elevation by making the surface *lighter*. Each elevation tier therefore *subtracts* contrast from every text and border token sitting on it. This is not a palette mistake — it is structural, and it is exactly why F-01 happens to careful teams. **The fix is architectural: text tokens must be indexed by surface tier, not global.** A single `text-secondary` token cannot be correct on four surfaces.

---

## Keyboard Navigation

Not inspectable without a build. This is the checklist to run before ship — a dark theme makes focus visibility harder specifically because low-contrast rings disappear into low-contrast surfaces.

| Element | Tab order | Enter/Space | Escape | Focus ring visible on every surface tier? |
|---|---|---|---|---|
| Primary button | Must match visual order | Both activate | n/a | Check against page **and** card |
| Secondary / ghost button | | Both activate | n/a | Ghost buttons are the worst case — no fill to contrast against |
| Text inputs | | n/a | Clears or exits, not both | Check against input fill, not page |
| Dropdown / select | | Opens | Closes, returns focus to trigger | Check ring on the open menu surface |
| Modal | Focus trapped inside | | Closes, returns focus to opener | |
| Links in body copy | | Enter activates | n/a | Underline, not colour alone (1.4.1) |
| Skip-to-content | First tab stop | | | Must be visible when focused |

**Specific dark-theme keyboard risk:** teams frequently remove the browser default `:focus` outline (because it looks wrong on dark) and replace it with a *subtle* custom ring. Subtle plus dark equals invisible. If `outline: none` appears anywhere in the stylesheet without a compliant replacement on the same selector, that is a 2.4.7 failure and it is a blocker.

---

## Remediation Spec
*(`design-handoff` format — hand this to engineering as-is)*

### Design Tokens

| Token | Value | Usage | Verified against |
|---|---|---|---|
| `surface-base` | `#121212` | Page background | — |
| `surface-raised` | `#1E1E1E` | Cards, panels | — |
| `surface-overlay` | `#27272A` | Inputs, menus, tooltips | — |
| `text-primary` | `#EDEDED` | Headings, body | 16.00 / 14.24 / 12.72 ✓ |
| `text-secondary` | `#B4B4B8` | Supporting copy | 9.06 / 8.07 / 7.21 ✓ |
| `text-tertiary` | `#949494` | Meta, timestamps, captions | 6.18 / 5.50 / 4.91 ✓ |
| `border-control` | `#8A8A8A` | Input/control boundaries (1.4.11) | 5.43 / 4.83 / 4.31 ✓ |
| `border-decorative` | `#3F3F46` | Dividers only — never a control boundary | Exempt (decorative) |
| `accent-fill` | `#2F6FE4` | Primary button background | 4.03 vs base, 3.58 vs raised ✓ |
| `accent-on-fill` | `#FFFFFF` | Label on `accent-fill` | 4.65 ✓ |
| `accent-text` | `#60A5FA` | Inline links, text-only buttons | 7.37 on base ✓ |
| `focus-ring` | `#FFFFFF` | 2px ring + 2px offset | 4.65 vs fill, 19.80 vs base ✓ |

**Note on `text-tertiary`:** `#949494` clears 4.5:1 on every surface tier including `#27272A` (4.91:1). It has the smallest margin in the set — do not darken it, and do not introduce a fourth, lighter surface tier without re-validating it.

### Components

| Component | Variant | Change | Notes |
|---|---|---|---|
| Button | Primary | `accent-fill` + `accent-on-fill` label | Do not use `accent-text` here — it fails as a fill |
| Button | Secondary/ghost | `border-control` 1px + `text-primary` label | Ghost buttons need the border to satisfy 1.4.11 |
| Button | Disabled | Reduce opacity, **keep ≥3:1** | Technically exempt from 1.4.3, but users must read what they cannot yet click |
| Input | Default | `border-control`, `text-primary` value | |
| Input | Placeholder | ≥`#949494` on `surface-overlay` | Plus a persistent visible `<label>` — placeholder is never the label |
| Input | Error | `border` + icon + text, not colour alone | 1.4.1 + 3.3.1 |
| Link | Inline | `accent-text` + underline | Underline satisfies 1.4.1 independent of hue |

### States and Interactions

| Element | State | Required behaviour |
|---|---|---|
| Any focusable | `:focus-visible` | 2px `focus-ring`, 2px offset, ≥3:1 vs both neighbours |
| Any focusable | `outline: none` | **Forbidden** without a compliant replacement on the same selector |
| Primary button | hover / active | ≥3:1 difference from default, or add a non-colour cue |
| Status messages | all | Icon + text, never hue alone |

### Edge Cases

- **Long text:** truncation must not hide required info; provide full text on focus/hover *and* to screen readers
- **Zoom to 200%:** verify no horizontal scroll and no clipped controls (1.4.4 / 1.4.10)
- **Forced-colors / Windows High Contrast:** verify the theme does not break — dark themes commonly do
- **OS `prefers-contrast: more`:** if you can, offer a higher-contrast dark variant

### Accessibility Notes

- Every text token is validated against the **lightest** surface it can appear on, not the page background
- `accent-fill` and `accent-text` are permanently separate tokens — do not let anyone consolidate them
- Body font weight ≥400 in dark mode; no 300 (T-01)

---

## Ship Gate

**Blocks ship (fix before release):**
1. **F-02 / F-01** — every body-text grey below the Step-2 cheat-sheet threshold for its surface. This is the answer to your question. High-volume, affects the most users, easiest to prove in a complaint.
2. **F-03** — placeholder contrast *and* placeholder-as-label. Two failures in one control, on forms, where the cost of failure is highest.
3. **Focus visibility** — if `outline: none` exists without a compliant replacement, keyboard users cannot operate the product at all. Check this today; it takes one grep.

**Fix in the next release (do not block on, do not forget):**
4. **F-04 / F-05** — split the blue token; move the fill to luminance 0.15–0.17.
5. **F-06** — control borders to ≥3:1.
6. **F-07** — neutral focus ring.

**Backlog:**
7. F-08, F-09, T-01 weight audit, forced-colors verification.

**Effort estimate:** items 1–3 are a token-table change plus a stylesheet grep. If your theme is properly tokenised this is under a day of engineering and a half-day of QA. If greys are hardcoded at call sites, it's a week and you've just found a second problem worth fixing.

**On the cost of shipping anyway:** as of 2026 both the European Accessibility Act (in force since June 2025) and long-standing ADA Title III case law make low contrast one of the most commonly cited and most easily evidenced claims — an automated crawler proves it in seconds, with no expert testimony needed. Colour contrast is the single most-cited issue in automated accessibility scans of the top million sites, year after year. I'm flagging commercial risk, not giving legal advice; if this is consumer-facing in the EU or UK, route it past whoever owns that. But the engineering argument stands on its own: this is a cheap fix now and an expensive one after a complaint.

---

## Stress Test

**What's weakest here.** Every number in this audit is computed from *assumed* hex values, because none were provided. The contrast math is exact and the thresholds are correct, but the mapping from "lots of grey-on-grey" to `#71717A` on `#1E1E1E` is my inference. If your greys are actually `#A1A1AA` and up, F-01 and F-02 evaporate and you're close to shippable. **The 10-minute self-check exists precisely to replace my inference with your measurement — do it before you act on the ship gate.**

**The assumption most likely to be wrong.** I assumed one blue token does double duty as fill and link (F-04). Plenty of mature design systems already split these. If yours does, F-04 and half of F-05 drop out and the blue button is entirely fine — which would make your opening instinct exactly backwards, and the greys the whole story.

**Where I may be over-strict.** WCAG 1.4.11 does not unambiguously require a filled button's *fill* to hit 3:1 against the page. If the button carries a text label that itself passes 1.4.3, the label is arguably sufficient to identify the component, and several auditors read it that way. I've treated the fill as in-scope because (a) low-vision users scan for affordance shapes before reading labels, (b) any *state* communicated by fill change unambiguously does require 3:1, and (c) procurement checklists and VPAT reviewers flag it regardless of the spec's ambiguity. If you're optimising purely for letter-of-the-standard compliance rather than usability, F-05's fill requirement is the finding most open to challenge.

**Where I may be under-strict.** WCAG 2.x contrast math is known to model light-on-dark poorly — it systematically *over*-rates dark-mode readability relative to perceptual models like APCA (the candidate successor used in WCAG 3 drafts). Several of the values I marked as passing at 4.5–5.5:1 on dark would likely be marked borderline under APCA. **Shipping is gated on WCAG 2.1 AA, so that's what I audited — but treat 4.5:1 as your floor in dark mode, not your target.** Aim for 7:1 on body text where the design allows; you have the headroom, since `#EDEDED` on `#121212` is 16:1.

**What a smart critic would say.** *"You've turned 'is this good enough to ship' into a 9-finding audit with a token rewrite. That's scope creep on a yes/no question."* Fair. The honest compressed answer: **the blue button is fine, the greys are probably not, and three of the nine findings actually block you.** Everything else is the spec for fixing it properly once, instead of three times. If you need to ship this week, do ship-gate items 1–3 and defer the rest — that gets you to defensible, if not excellent.

**What would change my mind entirely.** A screenshot, or the hex values. Either one turns this from a well-reasoned conditional into a verdict. Send them and this recomputes in a minute.
