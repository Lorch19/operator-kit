Running **`[SKILL]`** — PRD Mode, **Dev-Team** output. Audience cue is "engineering needs it"; "assume we've decided to build it" closes the build/don't-build question, so no discovery detour. I've taken the build decision as made and noted the one residual risk at the end rather than re-opening it here.

**This draft runs on assumptions I could not check with you.** They are listed once, up front, so you can correct them in one pass instead of hunting through the doc. Everything I could not assume responsibly is in §8 Open Questions with the requirement it blocks — so engineering knows exactly what they can start Monday and what they cannot.

**Assumptions:**
1. "Project" is a container multiple users belong to, with an activity/audit stream already persisted (comments, file changes, status changes, membership changes). If no such stream exists, R-A1 becomes a much larger build and the Monday date is at risk — this is the single assumption most likely to be wrong.
2. Users can belong to many projects; the digest is one email per user covering all their projects, not one per project.
3. There is an existing transactional email provider and an existing notification-preferences surface to extend. Not building either from scratch.
4. Weekly cadence is fixed for v1 (the request says "each week"); cadence configurability is a non-goal.
5. No LLM/AI summarisation in v1 — see §3 Non-Goals and the roadmap.

---

# PRD: Weekly Project Digest Email

**Status:** Draft for engineering · **Output mode:** Dev-Team · **Date:** 2026-09-16

---

## 1. Context

### TL;DR

A weekly email that tells each user what changed in the projects they belong to but were not personally in. It exists to close the awareness gap that makes people either miss things that needed them or open the app daily "just to check."

### Why Now

The build decision is made. The timing constraint that actually shapes this spec is external, not internal: Google, Yahoo, Microsoft and Apple now enforce bulk-sender rules with hard rejection rather than spam-foldering, so the compliance and authentication work in §5C is a precondition for the first send, not a follow-up.

### Market & Competitive Context

**Skipped deliberately.** The competitive landscape does not shape any requirement here — every collaboration tool ships a digest, the patterns are converged and well understood, and nothing about a competitor's version changes what we build. I have no TAM/SAM/SOM data for this and will not invent it. If this doc later has to travel to an exec audience, that section gets built from real numbers, not from this one.

### The Narrative

Maya is a designer on four projects. Three are ambient — she is on them because her work touches them occasionally. On Monday at 8am she gets one email. It does not tell her what she did; it tells her that on *Nordic Rebrand*, someone replaced the two logo files she'd commented on and the launch date moved to 14 Oct; that *Atlas* had a decision logged she is named in; and that the other two had nothing worth her attention, so they are not mentioned at all. Three items, not thirty. She clicks the logo change, lands directly on that file already signed in, and leaves. Total elapsed time: forty seconds. The week she is on holiday and nothing happens in her projects, she gets no email at all.

That last sentence is the product. Most digests fail by sending every week regardless, which trains the recipient to delete on sight.

### Success Metrics

**Open rate is explicitly rejected as a success metric.** Apple Mail Privacy Protection pre-fetches tracking pixels for a large share of recipients, so opens measure Apple's proxy, not human attention. Do not instrument a goal against it. Track it only as a deliverability diagnostic.

The design requirement that makes all of this measurable: **hold out 5–10% of eligible users from the start.** Without a holdout, "digest recipients return more often" is unfalsifiable — the people who read digests are the engaged people already. A holdout is nearly free to build on day one and expensive to retrofit. R-F3 covers it.

| Type | Metric | Definition (instrument exactly this) | Target |
|------|--------|--------------------------------------|--------|
| **Primary (outcome)** | Incremental return rate | % of the eligible population with ≥1 product session in the 72h after send, digest arm minus holdout arm | **[NEEDS INPUT: pre-register a minimum detectable lift before the first send. Suggested decision rule: ship to 100% if the digest arm beats holdout by the pre-registered margin at p<0.05 sustained over 6 consecutive sends — 6 because weekly cadence means 6 exposures is the first honest read.]** |
| **Leading** | Item click-through | Clicks per sent digest, broken down by item type (comment / file / status / membership / date change) | No target. This is the input that ranks content in v1.1 — the item types nobody clicks get demoted or cut. |
| **Leading** | Suppression rate | % of eligible users suppressed for having nothing to report | No target — but if this is near 0%, the relevance filter (R-A3) is too loose and we are sending noise. |
| **Guardrail** | Spam complaint rate | Complaints ÷ delivered, per mailbox provider, rolling 7 days | **< 0.10%.** Not invented: the platform hard limit is 0.30% and 0.10% is the standard operating margin. Breaching 0.30% at any provider triggers the §5C kill switch. |
| **Guardrail** | Unsubscribe rate | Digest opt-outs ÷ delivered, per send | **[NEEDS INPUT: alert threshold.]** Trend matters more than level — a rising curve means content relevance is degrading. |
| **Counter-metric** | All-email opt-out | Users who disable *every* email notification type, not just the digest | Must not rise vs. pre-launch baseline. A bad digest poisons the whole email channel, because annoyed users reach for the global switch rather than the granular one. This is the metric that catches the real damage. |
| **Health** | Hard bounce rate | Hard bounces ÷ attempted | **[NEEDS INPUT: threshold.]** Must auto-suppress the address on first hard bounce regardless (R-C5). |

---

## 2. Personas

| Persona | Description | What the digest does for them |
|---------|-------------|-------------------------------|
| **Ambient member** *(primary)* | Belongs to 3–10 projects, actively works in 1–2. Misses things in the rest and finds out late. | The core case. Replaces "open the app and scan everything" with one scannable email. |
| **Lead / owner** | Accountable across several projects. Needs to spot where to intervene, not to read everything. | A cross-project sweep that surfaces movement and stalls without opening five project views. |
| **Dormant user** | No session in 30+ days. Still a member of projects. | Re-engagement — and the highest-risk segment. This is where spam complaints concentrate, because the email arrives with no remembered context. Handled explicitly in R-B4. |

*Merged deliberately: "admin" and "lead" behave identically for this feature.*

---

## 3. Scope

### Goals
- One weekly email per user, aggregating changes across all projects they can currently see.
- Send nothing when there is nothing worth sending.
- Get the user from email to the exact changed object in one click, signed in.
- Meet bulk-sender authentication and unsubscribe requirements before the first production send.
- Ship with the measurement apparatus (holdout + per-item attribution) in place from send one.

### Non-Goals
| Not in v1 | Why |
|-----------|-----|
| Digest of the user's own activity | Nobody wants a report of what they already did. Excluded at the query level (R-A2), not filtered in the template. |
| Configurable cadence (daily/monthly) | Multiplies the batch, aggregation window and preference surface. Weekly is the hypothesis; earn the rest. |
| Per-project digest subscriptions | Turns one preference into N. Revisit once R-F2 shows which projects people actually click. |
| Real-time or instant notifications | Different product with a different failure mode. Unrelated build. |
| In-app or Slack digest surface | The email is the test. Adding surfaces before knowing the email works multiplies cost against an unvalidated premise. |
| **LLM summarisation of digest content** | Deliberately excluded. It carries data-handling, accuracy-recourse, cost and latency questions that would each need their own treatment and would hold up the Monday handoff. Parked on the roadmap, not forgotten. |
| Digest for external/guest collaborators | Permission model differs and the leak blast radius is larger. Explicitly excluded in R-B5. |

---

## 4. Domain & Regulatory Context

Specific to this feature — engineering cannot ship the first send without C1 and C2.

| Area | Requirement | Impact on this feature |
|------|-------------|------------------------|
| **Bulk sender rules** (Google, Yahoo, Microsoft, Apple) | At 5,000+ messages/day per domain: SPF **and** DKIM **and** aligned DMARC; one-click unsubscribe per RFC 8058; spam complaints kept below 0.30%. Enforcement is rejection, not spam-foldering. | A weekly digest crosses 5,000/day the moment the eligible base does. Authentication must be verified before send one, not after. Drives R-C1, R-C2, R-C6. |
| **RFC 8058 one-click unsubscribe** | `List-Unsubscribe` (HTTPS) **plus** `List-Unsubscribe-Post: List-Unsubscribe=One-Click`. Both headers must be covered by the DKIM signature, and the URI must self-identify recipient and list. The POST must unsubscribe with no confirmation page and no login. | Common implementation bug: the header is added after signing, so DKIM does not cover it and providers ignore it. Call it out in R-C2. |
| **Message classification: commercial vs. transactional/relationship** | Under CAN-SPAM the test is *primary purpose*. A summary of activity in the user's own account reads as a relationship message; the moment it carries feature promotion, upsells or recommendations, it becomes commercial and the full commercial rule set attaches. | **Do not let marketing add a promo block later without re-running this analysis.** Engineering-safe default: build it to the commercial standard from day one — one-click unsubscribe, physical postal address in the footer, honest From and Subject. That is cheap now and near-impossible to retrofit under pressure. |
| **GDPR / ePrivacy** | Lawful basis and the user's ability to stop receiving it. | Granular per-type opt-out in existing notification settings (R-E1), honoured within 48h to meet platform expectations regardless of the statutory window. Do **not** hard-code a legal conclusion — see OQ-1. |
| **Content sensitivity** | The digest reproduces project content into an inbox we do not control, where it persists indefinitely and may be forwarded or sit on a personal device. | Argues for titles and counts over full content bodies (R-D3). Combined with the authorisation timing problem in R-B1, this is the highest-severity risk in the doc. |

I have **not** concluded what is legally required of us — that is OQ-1 for Legal. What is above is the platform requirement (hard, factual, non-negotiable) plus the engineering-safe default.

---

## 5. Requirements

### A. Content selection & aggregation

**P0**
- **R-A1** — Source digest content from the persisted project activity stream for the digest window. Single bounded query across the user's projects; no N+1 per project. *(Depends on the stream existing — Assumption 1.)*
- **R-A2** — Exclude activity where the actor is the recipient. Excluded in the query, not in the template.
- **R-A3** — **Collapse before ranking.** N edits to the same object by the same actor within the window render as one item ("Dana updated the brief") with a change count, never N rows. Membership churn collapses to a single line per project. Un-collapsed streams are the main reason digests feel like noise.
- **R-A4** — Cap at **[NEEDS INPUT: max items per digest and max projects listed — Design owns this]**. A cap is required regardless of the number: Gmail clips messages over ~102KB and hides the remainder behind "View entire message," so an uncapped digest silently truncates for the heaviest users, who are exactly the users it matters most to.
- **R-A5** — Projects with zero qualifying activity are omitted entirely. No "nothing happened" rows.
- **R-A6** — Digest window is a fixed 7-day period ending at generation. Boundary is timezone-dependent — see OQ-3.

**P1**
- **R-A7** — Rank items by relevance to the recipient, not recency: objects they authored or commented on, threads they are @-mentioned in, then everything else. A flat reverse-chronological list is the fallback if ranking slips — ship the fallback rather than the date.

### B. Send eligibility & suppression

**P0**
- **R-B1** — **Authorise at send time, per recipient.** Re-check project membership and object-level visibility immediately before dispatch, not at batch generation. A user removed from a project between generation and send must not receive its content. This is the defect class that turns a digest feature into a security incident; it is not an edge case and does not belong in §7.
- **R-B2** — **Suppress empty digests.** Zero qualifying items after R-A2/A3/A5 ⇒ send nothing. No "quiet week" email.
- **R-B3** — **Idempotent sends.** A send ledger keyed on `(user_id, period_start)` with a uniqueness constraint. A retried or re-run batch must never double-send — this is the failure that generates complaints fastest.
- **R-B4** — Dormant users (no session in **[NEEDS INPUT: threshold days]**) are eligible but monitored as a separate cohort in the R-F metrics. If their complaint rate breaches the R-C6 threshold, the cohort is suppressed independently rather than killing the whole send.
- **R-B5** — External/guest collaborators are ineligible in v1.
- **R-B6** — Suppress users with a prior hard bounce, a spam complaint, or a digest opt-out. Checked at send time against the ledger, not cached in the batch.

### C. Delivery & compliance infrastructure

**P0**
- **R-C1** — SPF, DKIM and DMARC alignment verified on the sending domain before the first production send. Verification is a gating checklist item with a named owner, not an assumption.
- **R-C2** — `List-Unsubscribe` (HTTPS) and `List-Unsubscribe-Post: List-Unsubscribe=One-Click` headers, **added before DKIM signing so the signature covers them.** The endpoint must accept an unauthenticated POST, act immediately, and never present a confirmation page or login wall.
- **R-C3** — Visible unsubscribe link plus a physical postal address in the footer. Cheap, and it is what makes the OQ-1 classification question non-blocking.
- **R-C4** — Honour every opt-out (header or link) within **48 hours**; realistically, immediately.
- **R-C5** — Bounce and complaint webhooks wired to the suppression ledger. Hard bounce ⇒ permanent suppression on first occurrence. Complaint ⇒ permanent suppression plus cohort attribution.
- **R-C6** — **Kill switch.** A single flag that halts all digest sends without a deploy. Triggered automatically when the rolling 7-day complaint rate at any provider exceeds **0.30%**, and available manually. Deliverability damage compounds across *all* company email, so the blast radius of a bad digest is not limited to the digest.
- **R-C7** — Ramp the first production send: **[NEEDS INPUT: ramp schedule]**. A cold sending domain going from zero to full volume in one batch is itself a spam signal. Do not skip this to make a date.

### D. Rendering

**P0**
- **R-D1** — HTML plus a genuine plaintext alternative. The plaintext part must be readable, not a link dump.
- **R-D2** — Table-based layout. Flexbox and grid are not reliable across email clients; Outlook in particular.
- **R-D3** — Items show object title, actor, change type and timestamp. **Not** full comment or document bodies — see §4 content sensitivity. Exceptions require the OQ-1 outcome.
- **R-D4** — Every item links to the specific object. A user arriving signed-out must land on that object after auth, not be dumped on a dashboard. Preserve the destination through the auth redirect.
- **R-D5** — Links carry attribution parameters sufficient to satisfy R-F2 without exposing user identifiers in a way that leaks through referrers.
- **R-D6** — Subject line states the actual content, not a fixed string. Accurate subject lines are both a compliance point and the largest single lever on whether it gets opened. Copy: **[NEEDS INPUT — Design/Content owns; needs the item-count and project-name variables from R-A3/A4]**.

**P1**
- **R-D7** — Dark-mode-safe colours. Several clients force-invert, which reliably destroys logos and light-text-on-light-background blocks.

### E. Preferences & unsubscribe

**P0**
- **R-E1** — Digest appears as its own toggle in existing notification settings, independent of other email types. Users who only want the digest gone must not have to disable everything — this is what protects the §1 counter-metric.
- **R-E2** — One-click unsubscribe (R-C2) sets the same preference as the settings toggle. One state, two entry points; no divergent flags.
- **R-E3** — Default state for existing and new users: **[NEEDS INPUT — depends on OQ-1. Engineering should build the default as a config value, not a constant, so the answer lands as a config change rather than a release.]**

### F. Instrumentation

**P0**
- **R-F1** — Emit `digest_generated`, `digest_suppressed` (with reason), `digest_sent`, `digest_bounced`, `digest_complained`, `digest_unsubscribed`.
- **R-F2** — Emit `digest_link_clicked` with item type and position, so R-A7 ranking has an input and the leading metric is computable.
- **R-F3** — **Holdout assignment from send one.** Deterministic, stable per user, 5–10%. Holdout users are generated-and-logged but not sent, so the counterfactual is measurable rather than assumed. Retrofitting this after launch loses the clean baseline permanently.
- **R-F4** — Do not instrument a goal against open rate (Apple MPP). Collect it as a deliverability diagnostic only, labelled as such in the dashboard so nobody reports it upward as engagement.

---

## 6. Dependencies & Risks

| Dependency | Owner | Impact |
|------------|-------|--------|
| Project activity stream with actor, object, type, timestamp | Backend | **Blocks R-A1 and the whole feature.** If absent, re-scope before Monday — this is the schedule risk. |
| Email provider supporting custom headers pre-signing + bounce/complaint webhooks | Platform/Infra | Blocks R-C2, R-C5. Some providers strip or append headers post-signing — verify, don't assume. |
| SPF/DKIM/DMARC on the sending domain | Infra/IT | **Blocks the first production send.** Often the longest-lead item because it needs DNS access someone else owns. Start it Monday. |
| Notification preferences surface | Frontend | Blocks R-E1. |
| Legal review of message classification | Legal | Blocks R-E3 default only. Everything else proceeds. |
| Email template/design | Design | Blocks R-D6, R-A4 caps. |

| Risk | Mitigation |
|------|------------|
| **Content leaks to a user who lost access between generation and send** | R-B1 send-time authorisation. Highest severity in the doc. Needs an explicit test, including the removed-mid-window case. |
| **Digest complaints damage deliverability for all company email** | R-C6 kill switch + 0.10% operating margin + R-C7 ramp + R-B4 cohort-level suppression. |
| **Digest is noise; users mute all email rather than just this** | R-A3 collapsing, R-A5/R-B2 suppression, R-E1 granular toggle, and the counter-metric that catches it. |
| **Batch double-sends on retry** | R-B3 ledger with a uniqueness constraint. |
| **Success is unmeasurable because everyone got it** | R-F3 holdout from send one. |
| **Monday date pressure drops compliance work as "infra polish"** | R-C1/C2 are gating checklist items, not a workstream. A send without them can get the domain rejected outright, which costs far more than the slip. |

---

## 7. Edge Cases

*Non-obvious only. Standard states (loading, empty inbox) are not specified.*

| Scenario | Behavior |
|----------|----------|
| User's only project is deleted mid-window | Activity from a deleted project is excluded. If that empties the digest, R-B2 suppresses it. |
| User joins a project mid-window | Include only activity from their join timestamp forward. Joining a project does not grant a retroactive feed of what happened before they arrived. |
| Actor is deactivated or deleted between event and send | Item still renders with the historical display name. Do not resolve actor identity at render time or the row breaks. |
| Object renamed several times in the window | Show the current title with the original as context; count as one change (R-A3). |
| All activity in the window is the user's own | Zero qualifying items ⇒ suppressed (R-A2 + R-B2). |
| User changes email address mid-window | Send to the address current at send time; never to a cached one from generation. |
| Batch fails halfway | Ledger (R-B3) makes resume safe — resume, never restart. |
| User unsubscribes while the batch is running | R-B6 is evaluated at send time, so the in-flight message is not sent. |
| Very heavy week (hundreds of items) | R-A4 cap applies with an explicit "and N more" link. Never rely on Gmail's clipping to do the truncation. |
| Same user, two accounts, same inbox | Two digests. Accepted for v1; noted as a complaint-risk source. |

---

## 8. Open Questions

Ordered by what they block, so Monday's work can start against the unblocked majority.

**Legal**
- **OQ-1** — Is the digest a transactional/relationship message or a commercial one, and what is our lawful basis? *Blocks R-E3 (default on/off) only.* Everything else is built to the stricter standard regardless, so this does not gate the build. **Needed before the first production send, not before development starts.**

**Design / Content**
- **OQ-2** — Max items per digest and max projects listed (R-A4), and subject-line copy (R-D6). *Blocks final template only; engineering can build against a config-driven placeholder.*

**Product / Eng**
- **OQ-3** — Is the "week" boundary and 8am send time in the user's local timezone or a single global UTC batch? *Blocks R-A6 and the batch architecture.* **Highest-cost question here** — local time turns one batch into a rolling 24-hour send window, which changes scheduling, capacity and idempotency handling. **Answer this before Monday.** My assumption if no answer arrives: single global batch for v1, local-time sends on the roadmap.
- **OQ-4** — Dormancy threshold for R-B4.
- **OQ-5** — Ramp schedule for the first sends (R-C7).

**Data / Analytics**
- **OQ-6** — Minimum detectable lift to pre-register for the primary metric, and the holdout percentage within the 5–10% band. *Blocks the launch decision rule, not the build.* Must be fixed **before** the first send — choosing a threshold after seeing results is how a feature gets declared a success for free.

---

## 9. Roadmap — where the non-goals live

| Phase | What | Why |
|-------|------|-----|
| v1 | Everything above | Test the premise that a weekly summary changes behaviour, measurably. |
| v1.1 | Relevance ranking tuned from R-F2 click data; per-project mute | The first real data on which change types anyone cares about. Cheap once instrumented. |
| v1.2 | Cadence choice (daily/weekly/monthly) | Only once the weekly hypothesis is confirmed, and only if opt-out reasons point at frequency. |
| v2 | LLM summarisation of project activity and uploaded documents | Deliberately deferred from v1 (§3). Carries its own data-handling, accuracy-recourse, cost and latency questions and needs a treatment of its own rather than a paragraph in this one. |
| v2 | Additional surfaces (in-app, Slack) | Only after the email proves the underlying need. |

---

## Appendix

- Field-level event schema for R-F1/R-F2 — **[to be linked: tracking plan]**
- Email template and responsive/dark-mode specs — **[to be linked: Figma]**
- Bulk sender authentication checklist (SPF/DKIM/DMARC verification steps) — **[to be linked: infra runbook]**

---

## Stress Test

**What is weakest here.** The doc rests hardest on Assumption 1 — that a usable activity stream already exists. If activity is scattered across per-feature tables with no common shape, R-A1 alone is a multi-sprint build and the Monday handoff is a handoff of a spec whose foundation is missing. That is the assumption I would check first, before any of the open questions.

**What could be wrong in the framing.** I accepted "we've decided to build it," as instructed. But the doc quietly assumes the digest's job is *awareness*, and awareness might not be the real problem — if people miss things because notification volume is already too high, a weekly digest adds to the pile rather than replacing anything. The design leans on a holdout precisely so this can fail visibly instead of quietly, but a holdout only tells you *whether* it worked, never *why not*. Worth one look at existing notification volume per user before building.

**Where a critic would push hardest.** Three places. (1) "Suppress empty digests" is the right call but makes the send volume unpredictable, which complicates both capacity planning and the statistics — users who receive four digests and users who receive one are not comparable, so the primary metric needs exposure-adjusting rather than a naive arm comparison. (2) The 6-send evaluation window means roughly six weeks before a real read, which sits badly with a Monday-deadline culture; expect pressure to call it early on open rate, which is exactly what R-F4 exists to prevent. (3) Ranking (R-A7) is P1 and the fallback is reverse-chronological — but reverse-chronological is also the version most likely to feel like noise, which risks the whole test failing on presentation rather than on premise. If the schedule forces a cut, cutting ranking may cost more than slipping a week.

**What I chose not to invent.** No TAM/SAM/SOM, no target numbers for return rate or unsubscribe rate, no legal conclusion on message classification. The two numeric thresholds that *are* stated (0.30% platform limit, 0.10% operating margin) are external platform requirements, not targets I made up. Everything else is flagged.

**Sources for §4:** [Gmail sender guidelines FAQ](https://support.google.com/mail/answer/14229414?hl=en) · [2026 bulk email sender requirements (Red Sift)](https://redsift.com/guides/bulk-email-sender-requirements) · [Bulk email sender rules for Google, Yahoo, Microsoft & Apple (PowerDMARC)](https://powerdmarc.com/bulk-email-sender-requirements/) · [What is RFC 8058 (Mailgun)](https://www.mailgun.com/blog/deliverability/what-is-rfc-8058/) · [One-click List-Unsubscribe header (EmailLabs)](https://emaillabs.io/en/one-click-list-unsubscribe-header-rfc-80581/) · [GDPR and transactional emails (TermsFeed)](https://www.termsfeed.com/blog/gdpr-transactional-emails/)
