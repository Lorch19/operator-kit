**Skill:** `[SKILL]` — **PRD Mode**, **Dev-Team** output.

You said engineering needs it Monday and that the build decision is made, so I skipped Discovery and went straight to the document. Two things I'd normally have asked and instead decided in the draft, flagged loudly in §0 so you can overturn them in one line: **suppress empty digests** and **no LLM-generated summary prose in v1**. Genuinely open items I did *not* invent answers to are marked `[NEEDS INPUT]` and collected in §9.

One piece of pushback before the doc: *"weekly digest email"* is a solution, not a problem. I've accepted the call and written the PRD, but I reconstructed the problem in §1 and made the riskiest assumption explicit — that **passive awareness converts into return visits**. §5.F gates the full rollout on a holdout that actually tests it. If you only take one thing from this draft into Monday, take the holdout.

---

# PRD: Weekly Project Digest Email

| | |
|-|-|
| **Version** | v1.0 (initial draft) |
| **Date** | 2026-09-16 |
| **Author** | Omri |
| **Audience** | Engineering (build), Design, Legal (§4 review) |
| **Status** | Draft for Monday kickoff — §0 assumptions need a yes/no before sprint planning |

---

## 0. Assumptions & Decisions Log

This draft was written without a discovery round. Everything below is a **decision I made on your behalf** to keep the document buildable. Each is cheap to reverse *now* and expensive to reverse after sprint 1. Read this section first.

| # | Decision | Rationale | Cost to reverse later |
|---|----------|-----------|----------------------|
| D1 | **Suppress the send when nothing qualifying happened.** No "quiet week" emails. | An empty digest is the fastest way to train a user that this sender is ignorable, and it inflates the denominator on every metric below. | Low — flag flip |
| D2 | **One email per user, covering all their projects** — not one email per project. | Per-project fan-out reproduces the notification fatigue the digest is supposed to solve. | **High** — changes the aggregation unit, the template, and the unsubscribe model |
| D3 | **No LLM-generated summary prose in v1.** Templated aggregation only. | Non-determinism inside a permission-scoped surface means a hallucinated line could imply activity the recipient can't verify, or leak a phrasing of content they shouldn't see. Also: cost and latency at full-list fan-out. Revisit in v1.1 once the deterministic pipeline is trustworthy. | Medium |
| D4 | **Exclude the recipient's own actions** from the digest. | The product promise is "what changed while you were away." | Low |
| D5 | **Send Monday 08:00 in the recipient's local timezone**; window = previous Mon 00:00 → Sun 23:59:59 local. | Makes the subject line honest ("Last week in your projects") and the window trivially explainable. Friday-afternoon is the credible alternative — worth an A/B in v1.1, not a v1 debate. | Low |
| D6 | **Digest gets its own sending subdomain and stream**, separate from transactional email. | A digest earns spam complaints. Password resets must not inherit that reputation. See §4. | **High** — DNS, warmup, and ESP config are painful to retrofit |
| D7 | **Digest opt-out is independent** of all other notification settings. | Unsubscribing from a weekly summary must never silently disable a security or mention alert. | Medium |
| D8 | **Default state is ON (opt-out) for eligible existing users**, with a pre-launch heads-up email. | Opt-in defaults typically collect too few recipients to measure anything in a quarter. **This is the one decision most likely to be wrong** — it is a legal and trust question as much as a product one. See §4 and Q-L1. | Low technically, **high in trust terms once sent** |

Assumed product shape, since it wasn't specified: a multi-tenant workspace product where a **user belongs to one or more projects**, and a project contains **items** (tasks), **comments**, **documents/files**, and **members**. If the underlying object model differs, §5.B (event taxonomy) is the section that needs rewriting — the rest holds.

---

## 1. Context

**TL;DR.** Ship a weekly email that tells each user what actually changed in their projects last week, so people who aren't in the product daily stop losing the thread. We build it deterministically, send it only when there's something to say, and gate the full rollout on a measured lift in return visits against a holdout.

**Why now.** The decision to build is made. The thing worth protecting is *why* it's worth building: as a user's project count grows, per-event notifications get muted or filtered, and there is currently no low-effort surface that answers "what did I miss?" The digest is a bet that a single weekly, permission-correct summary re-establishes that thread. `[NEEDS INPUT: the actual trigger — a retention drop, a support theme, a customer ask? The PRD is stronger if §1 cites the real signal instead of this reconstruction.]`

**Market & competitive context — deliberately skipped.** TAM/SAM/SOM is not meaningful for a retention feature inside an existing product, and I won't fabricate competitor implementation details. What *does* shape requirements is industry-established email practice, and that's in §4 with sources.

### The Narrative

Maya is a designer on four projects. She's heads-down in Figma most of the week and muted the product's per-event emails in month two because they arrived at twenty a day. On Monday at 08:00 she gets one email: **"Last week in your 4 projects."** Three project blocks. Under *Website Refresh*: 6 items completed, 2 new items, and a comment thread on "Nav IA" where Dan asked her a direct question on Thursday. Under *Brand System*: a new document, *Type Scale v2*. The fourth project had nothing and isn't shown. She taps the Nav IA thread, lands in the item, and replies — 40 seconds, one tap in. The project she was removed from on Wednesday does not appear at all, and neither does the item she created herself on Tuesday.

### Success Metrics

The whole point of §5.F's instrumentation is that this table can be filled in with evidence rather than opinion.

| Type | Metric | Definition | Target |
|------|--------|------------|--------|
| **Primary** | **7-day return-visit lift** | % of recipients with ≥1 authenticated session within 7 days of send, **minus** the same % in the holdout | `[NEEDS INPUT: baseline weekly return rate]` — ship gate is *positive and statistically significant*, not a round number invented here |
| Secondary | Unique click rate | unique clickers ÷ delivered | `[NEEDS INPUT: no comparable in-product baseline]` |
| Secondary | Actions taken post-click | % of clickers who comment, complete, or create within the session | Directional in v1; no gate |
| **Guardrail** | Digest unsubscribe rate | cumulative unsubscribes ÷ delivered | Proposed: **< 0.5% cumulative by week 4.** Above 1% = stop and redesign |
| **Guardrail** | Spam complaint rate | per Gmail bulk-sender policy | **< 0.1%; hard stop at 0.3%** (verified, §4) |
| **Guardrail** | Cross-stream unsubscribe rate | all-email opt-outs, all streams | Must not rise vs pre-launch |
| **Guardrail** | Transactional deliverability | inbox placement of password reset / invite | No degradation (this is what D6 protects) |
| **Explicitly NOT a metric** | **Open rate** | — | Apple Mail Privacy Protection pre-fetches tracking pixels, inflating reported opens by an estimated 15–20 points. Do not put open rate on a dashboard anyone makes decisions from. |

---

## 2. Personas

| Persona | Description | What the digest must do for them |
|---------|-------------|----------------------------------|
| **The drifting member** (primary) | On 3+ projects, opens the product weekly or less, has muted or filtered most notification email | Re-establish the thread in one scan; make the single most relevant item tappable |
| **The project lead** | Owns 1–2 projects, in the product daily, wants confidence the work is moving | Accurate counts they'd defend in a status meeting. A wrong number here destroys trust in the whole email |
| **The over-notified power user** | High volume, already receives in-app + per-event email, likely to treat a new stream as spam | Never feel like *more* mail. Must be able to turn off the digest **alone**, in one click, without touching anything else (D7) |

---

## 3. Scope

**Goals**
1. One weekly email per eligible user summarising changes across all their projects.
2. Deterministic, permission-correct content that is provably a subset of what the recipient can see in-product.
3. Send only when there is something worth saying (D1).
4. One-click unsubscribe scoped to the digest alone (D7), plus in-product preference control.
5. Instrumentation and a holdout sufficient to answer "did this work?" within 8 weeks.
6. Bulk-sender compliance from the first send, not retrofitted (§4).

**Non-Goals (v1)** — each of these is a real request that will surface in the kickoff; the answer is "v1.1, tracked in §8."
- Configurable cadence (daily / biweekly / monthly).
- Per-project emails or per-project cadence.
- User-configurable content filters ("only show me comments").
- LLM-written narrative summaries (D3).
- Digest delivery in Slack, in-app inbox, or push.
- Inline replies from the email body.
- Attachment or file-content previews.
- Digests for users with zero projects, or for org-external guests `[see Q-P2]`.
- Localized copy beyond the product's existing supported locales.

---

## 4. Domain & Regulatory Context

Not boilerplate — each row changes a specific requirement in §5. **§4 needs Legal sign-off before the first production send**, which is the only hard external dependency in this PRD.

| Area | Requirement / best practice | Impact on this feature |
|------|----------------------------|------------------------|
| **CAN-SPAM (US) — "primary purpose" test** | Transactional/relationship content is exempt from opt-out requirements; a message becomes **commercial** if the subject line reads commercial, or if the relationship content doesn't appear at the top. Significant promotional content flips the whole email to commercial. | **The digest is a relationship message today and must stay one.** Requirement: **no promotional modules, upsells, feature announcements, or plan nudges in the digest template — ever.** The first time Marketing asks for a banner, the email's legal classification changes. Bake this into the template as a hard constraint, not a guideline. We ship the unsubscribe anyway (below), so the practical risk is low — but the subject line and top-of-body rule still bind. |
| **CASL (Canada)** | The three baseline obligations for a commercial electronic message are consent, sender identification, and an unsubscribe mechanism; a withdrawal must be honoured **within 10 business days**. | Every digest carries full sender identification and a working unsubscribe regardless of classification, and unsubscribes take effect **immediately** (§5.E), which clears both the 10-business-day and 48-hour bars. |
| **GDPR / ePrivacy (EU/UK)** | Service-related messaging about an existing relationship generally rests on legitimate interest; marketing requires consent. Data minimisation applies to the email body itself. | Supports the opt-out default (D8) **only while the email stays purely service-related** — which is the same constraint the CAN-SPAM row imposes. `[Q-L1]` |
| **Gmail bulk-sender requirements** (≥5,000 msgs/day) | SPF **and** DKIM required; the From-header organizational domain must **align** with SPF or DKIM. `List-Unsubscribe` per **RFC 8058** (one-click) — mailto or landing-page links alone are insufficient. Unsubscribes fulfilled within **48 hours**. Spam rate **below 0.1%**, and **never at or above 0.3%** (at 0.3%+ a sender loses eligibility for delivery mitigation until it stays under for 7 consecutive days). | Direct P0 requirements in §5.C and §5.E. These are pass/fail at the mailbox provider, not preferences. |
| **Deliverability hygiene** | Bulk and transactional streams should be reputation-isolated. | D6: dedicated subdomain + separate ESP stream/IP pool, warmed before full rollout (§5.D). |
| **Content confidentiality** | The email body leaves our security boundary and persists in the recipient's mailbox, forwardable and indefinitely retained. | Digest shows **titles, actor names, counts, and links** — never comment bodies in full, never document contents, never file attachments. Depth of content in the body is a security decision, not a design one. `[Q-L2: any customer segment where even titles in email are contractually disallowed?]` |
| **Accessibility** | Semantic structure, ≥4.5:1 contrast, meaningful link text, dark-mode rendering, plain-text alternative. | P0 in §5.C. "View 12 items" beats "click here"; the plain-text part must be genuinely readable, not a stripped-tag artifact. |

---

## 5. Requirements

### A. Eligibility & Subscription

**P0**
- A user is eligible if: account is active and not suspended; email is **verified**; they are a current member of ≥1 non-archived project; they have not opted out of the digest; and the org has not disabled digests org-wide.
- Unverified email addresses are **never** sent to. This is a deliverability requirement as much as a correctness one.
- Org admins can disable the digest for their entire org (single setting, applies to all members).
- Per-user preference `digest.weekly.enabled`, default `true` for eligible users (D8), stored independently of every other notification preference.

**P1**
- Pre-launch heads-up email to existing users, sent ≥72h before the first digest, with a one-click "not for me" that sets the preference without sending a digest first.

### B. Content Selection & Aggregation

This is the section that decides whether the email is trusted or ignored. Two rules govern it:

> **Rule 1 — Render net state, not the event stream.** If an item was renamed six times, the digest shows the item once, with its current name. Replaying raw events is the single most common way digests become unreadable.
>
> **Rule 2 — Authorize at render time against current ACLs.** Never against the ACL as it stood when the event fired. A user removed from a project on Wednesday sees nothing from that project, including Monday's events.

**P0 — event taxonomy.** v1 includes only these. Anything not listed is excluded by default; adding an event type is a deliberate change, not an oversight fix.

| Event | In v1? | Collapse rule |
|-------|--------|---------------|
| `item.created` | ✅ | One row per item, current title |
| `item.completed` (terminal state) | ✅ | One row per item; only the final state at cutoff counts |
| `item.status_changed` (non-terminal) | ❌ | High volume, low signal |
| `item.field_updated` / renamed | ❌ | Reflected in current title only |
| `item.assigned` | ❌ | Recipient already gets a direct notification |
| `comment.created` | ✅ | Collapse per thread: count + most recent comment's author and **title/first line only** (§4) |
| `document.created` / `published` | ✅ | One row per document |
| `document.edited` | ✅ | Collapse per document: "edited by Ana and 2 others" |
| `member.joined` / `member.removed` | ✅ | Collapse per project into one line |
| `project.created` / `archived` | ✅ | One row |
| `item.deleted` | ❌ | **And it suppresses that item's `created` row if both fall in the same window** |

**P0 — filters and caps**
- Exclude every event where `actor_id == recipient_id` (D4).
- Exclude events in archived projects and in projects the recipient cannot currently read.
- Cap at **5 projects** per email, ordered by qualifying-event count descending, then most recent activity. Overflow renders as "+N other projects with activity" linking to the in-product activity view.
- Cap at **6 rows** per project block, ordered by recency. Overflow renders as "+N more" deep-linking into that project.
- **Bulk-activity collapse:** if a single actor produces >20 events of one type in one project in the window, collapse to a single line ("Ana added 340 items") rather than paginating an import.
- **Suppression (D1):** if zero qualifying rows survive all filters, **do not send, and do not enqueue.** Record a `digest.suppressed` event with the reason.

**P0 — window definition**
- Window is a **half-open interval** `[window_start, cutoff)` — closed at the start, exclusive at the cutoff — so that consecutive weeks can neither double-count nor drop an event at the boundary.
- `window_start` and `cutoff` are computed in UTC from a **timezone offset snapshotted at scheduling time**, so a user who changes timezone mid-week does not get a shifted or duplicated window (§7).

### C. Rendering & Email Build

**P0**
- Responsive HTML, tested against Gmail (web/iOS/Android), Apple Mail, and Outlook (web/desktop). `[NEEDS INPUT: client mix from current email analytics — it should reorder this list]`
- A genuine plain-text alternative part — authored, not tag-stripped.
- Dark-mode safe: no white-background-dependent logos, no hardcoded near-black text on transparent.
- Accessibility per §4: semantic headings, ≥4.5:1 contrast, descriptive link text, `alt` on every image, `lang` set.
- Subject line: `Last week in your {N} projects` (N ≥ 2) / `Last week in {Project Name}` (N = 1). Relationship-framed, never promotional (§4).
- Preheader summarises volume: "6 items completed, 3 new comments."
- Every deep link carries the target's canonical URL plus digest attribution params (§5.F) and lands on the **item**, not the project root.
- **No promotional content of any kind** in the template (§4). Enforce in code review; a lint on the template directory is cheap and worth it.
- All images served from a stable CDN host with absolute HTTPS URLs; the email must be fully comprehensible with images blocked.

**P0 — required headers**
- `List-Unsubscribe` **and** `List-Unsubscribe-Post: List-Unsubscribe=One-Click` per RFC 8058.
- SPF and DKIM on the sending subdomain, with From-header domain **aligned** to at least one of them; DMARC policy published.
- Stable `Message-ID`; `List-Id` identifying the digest stream.

### D. Scheduling & Delivery

**P0**
- Weekly job, per-user target **Monday 08:00 recipient-local** (D5). Timezone resolution order: user setting → org setting → **UTC**.
- **Idempotency key `(user_id, digest_period_id)`.** A given user receives at most one digest per period regardless of retries, redeploys, or timezone changes. This is the requirement that prevents the worst possible launch-day outcome.
- **Failure isolation:** one user's render or send failure must not abort the batch. Log, skip, continue, and surface the count.
- Retries: exponential backoff on transient ESP failures, max 3 attempts, **abandoned after the period's cutoff + 24h** — a Wednesday digest about last week is worse than no digest.
- **Kill switch:** a feature flag that halts generation *and* drains an in-flight batch, operable without a deploy. Named, documented, and **tested in staging before the first production send.**
- Dedicated sending subdomain and ESP stream, isolated from transactional (D6), IP-warmed against a ramped rollout.
- Rollout ramp: internal → 1% → 10% → 50% → 100%, with a minimum of one full send cycle at each step and a spam-rate check at each gate (§4).

**P0 — bounce and complaint handling**
- Hard bounce → suppress the address across all streams, mark email unverified.
- **Spam complaint → immediately and permanently unsubscribe that user from the digest.** Non-negotiable: complaints are what threaten the 0.1%/0.3% thresholds.
- Soft bounce → 3 consecutive periods, then suppress the digest for that user.

**P1**
- Per-minute send rate cap, configurable without deploy.

### E. Preferences & Unsubscribe

**P0**
- One-click unsubscribe (RFC 8058 POST) takes effect **immediately** — inside both the 48-hour Gmail bar and the 10-business-day CASL bar (§4).
- The unsubscribe link in the body requires **no login** and disables **only** the weekly digest (D7). It must be a signed, single-purpose, expiring token — not a raw user ID in a query string.
- The confirmation page states plainly what was turned off and what was left on, and offers one-click re-subscribe.
- In-product notification settings expose the digest as its own toggle, with copy stating the cadence and that it is separate from other notifications.
- Unsubscribing from the digest **must not** alter any other notification preference. Cover this with an explicit regression test.

### F. Instrumentation & Measurement

**P0**
- **10% holdout**, randomised by stable user hash, held for the first 8 weeks. Holdout users are eligible in every respect and simply receive nothing. They are not told. The holdout is the only thing that can answer §1's riskiest assumption, and it is what §1's primary metric is measured against.
- Events: `digest.generated`, `digest.suppressed{reason}`, `digest.sent`, `digest.delivered`, `digest.clicked{link_type, position}`, `digest.unsubscribed{source}`, `digest.bounced{type}`, `digest.complained`.
- Every event carries `digest_period_id`, `user_id`, `project_count`, `row_count`, `holdout: bool`.
- Click attribution params on every link, joinable to in-product sessions.
- **Do not instrument open-pixel rate as a decision metric** (§1). If it's collected at all, label it in the warehouse as MPP-contaminated so nobody builds on it six months from now.
- Dashboard covering the full §1 metrics table, with the guardrails visible on the same screen as the primary metric.

### G. Operational Safety

**P0**
- **Permission regression test as a release gate:** a fixture user removed from a project mid-window must produce a digest containing zero rows from that project. This test failing blocks the release.
- Generation runs against **read replicas**; a weekly full-list fan-out must not contend with production write traffic.
- Structured logs with `digest_period_id` for reconstructing any individual send.
- Alerts: send volume deviating >30% week-over-week; suppression rate >`[NEEDS INPUT: expected baseline]`; spam rate crossing 0.1%.

---

## 6. Dependencies & Risks

| Dependency | Owner | Impact if late |
|-----------|-------|----------------|
| Legal review of §4 (esp. D8 default-on and the EU cohort) | Legal | **Blocks first production send.** Start Monday |
| Sending subdomain, DNS, SPF/DKIM/DMARC, IP warmup | Infra | Blocks any send at volume; multi-week lead time — start in parallel with build, not after |
| Queryable event/activity log covering §5.B's taxonomy | Backend | **Blocks everything.** If no such log exists, this PRD understates the effort by a lot `[NEEDS INPUT: does it exist and is it queryable by time window and project?]` |
| Reliable per-user timezone | Backend | Degrades D5 to UTC for affected users |
| Email template system + client testing tooling | Frontend | Blocks §5.C |
| Notification preferences surface | Frontend | Blocks §5.E |
| Warehouse join between email events and product sessions | Data | Blocks the §5.F holdout readout — the feature ships unmeasurable |

| Risk | Severity | Mitigation |
|------|----------|------------|
| **The core bet is wrong** — awareness doesn't convert to return visits | High | The §5.F holdout. Agree the kill criterion *before* launch, while it's cheap to say "we'd stop" |
| **Permission leak** — recipient sees a project they no longer belong to | **Critical** | Render-time ACL check (§5.B Rule 2) + the §5.G release-gate test. Treat any occurrence as a security incident, not a bug |
| **Transactional deliverability contaminated** by digest complaints | High | D6 stream separation; spam-rate gates at every rollout step |
| Digest cannibalises an existing higher-value email stream | Medium | Cross-stream unsubscribe guardrail (§1) |
| **Wrong counts destroy trust** — one visibly incorrect number and the project lead persona never opens it again | High | Net-state rendering (Rule 1); reconcile digest counts against the in-product activity view in staging on real data |
| Default-on (D8) reads as a land grab | Medium | 72h heads-up email with pre-emptive opt-out (§5.A P1); immediate, frictionless unsubscribe |
| Weekly fan-out degrades production DB | Medium | Read replicas, batching, rate cap (§5.G) |
| Scope pressure to add LLM summaries mid-build | Medium | D3 is written down with its reason; it's in the §8 backlog with a home |

---

## 7. Edge Cases

Non-obvious only. Standard states (loading, 404, offline) follow existing conventions.

| Scenario | Expected behavior |
|----------|-------------------|
| User belongs to 40 projects | Top 5 by qualifying-event count; "+35 other projects with activity" |
| User removed from a project mid-window | **Zero rows from that project**, including events from before removal (Rule 2) |
| User *added* to a project mid-window | Include only events from `max(window_start, membership_start)` — no retroactive visibility |
| Item created and deleted inside the same window | Both suppressed; the item never appears |
| Project renamed mid-window | Current name only (Rule 1) |
| Bulk import of 5,000 items | Collapses to one line per actor per type (§5.B) |
| User's only activity is their own | Suppressed by D4, then suppressed entirely by D1 |
| User changes timezone mid-window | Offset snapshotted at scheduling time; the idempotency key guarantees exactly one send |
| Recipient in a locale with no translated template | Fall back to English `[Q-D2: or suppress? Suppressing loses a user; a wrong-language email may lose them harder]` |
| Email unverified at send time | Do not send. Record `digest.suppressed{reason: unverified_email}` |
| User deactivated between generation and send | Do not send; drop from the in-flight batch |
| Org disables digests between generation and send | Do not send; honour at send time, not generation time |
| Trial expired / account in read-only | `[Q-P3: still eligible? A digest is arguably a good re-activation surface, but it may also read as pressure]` |
| Job fails halfway through the batch | Resume via idempotency key; already-sent users are never re-sent |
| Job misses its window entirely (outage) | Send late **only within 24h of cutoff**, otherwise skip the period and alert |

---

## 8. Backlog & Roadmap

Everything §3 declared out of scope needs a home, or it comes back as scope creep in week 2.

| Item | Priority | Trigger to revisit |
|------|----------|--------------------|
| Cadence options (daily / biweekly / monthly) | P1 | Unsubscribe reasons citing frequency |
| Send-day/time A/B (Monday vs Friday) | P1 | After the §5.F holdout readout, not before |
| LLM-generated summary prose (D3) | P2 | Once the deterministic pipeline is trusted and a permission-safe evaluation exists |
| Per-project digest preferences | P2 | Demand from users with >10 projects |
| Slack / in-app digest delivery | P2 | If email engagement is weak but the *content* tests well — that result would mean the channel is wrong, not the feature |
| User-configurable content filters | P2 | Feature requests |
| Expanded event taxonomy (§5.B exclusions) | P2 | Click data showing which row types actually get tapped |
| "Catch up" digest after long absence | P3 | — |

---

## 9. Open Questions

**Product (you) — needed before sprint planning**
- **Q-P1:** What was the actual trigger (§1)? A real signal changes the metric targets and possibly the taxonomy.
- **Q-P2:** Are external guests / client-seat users eligible?
- **Q-P3:** Expired-trial and read-only accounts — eligible?
- **Q-P4:** **What result would make us turn this off?** Decide now, while it's cheap.
- **Q-P5:** Confirm or overturn D1, D3, and D8 — these three drive the most build time.

**Legal — start Monday, blocks first send**
- **Q-L1:** Is default-on (D8) acceptable for EU/UK recipients under legitimate interest given the digest is purely service-related?
- **Q-L2:** Any customer contracts (enterprise, regulated verticals) where project titles in outbound email are disallowed?
- **Q-L3:** Confirm the CAN-SPAM relationship-message classification and the hard "no promotional content" template rule (§4).

**Engineering**
- **Q-E1:** Does a queryable activity/event log covering §5.B exist today, with time-window and project filters? Largest single unknown in this document.
- **Q-E2:** Feasible read-replica capacity for a full-list weekly fan-out?
- **Q-E3:** Current per-user timezone coverage — what % would fall back to UTC?

**Design**
- **Q-D1:** Project-block hierarchy — grouped by project (assumed) or by event type across projects?
- **Q-D2:** Untranslated-locale behaviour (§7).

**Data**
- **Q-DA1:** Can email events be joined to authenticated product sessions today? Without this, §1's primary metric is uncomputable and the holdout is wasted.

---

## Appendix

**To be linked before kickoff:** email template designs (Figma), full tracking plan, event taxonomy mapped to actual schema names, ESP configuration runbook, rollout gate checklist.

**Sources used in §1 and §4**
- [CAN-SPAM Act: A Compliance Guide for Business — FTC](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business)
- [When sending commercial email, businesses can't unsubscribe from CAN-SPAM compliance — FTC](https://www.ftc.gov/business-guidance/blog/2023/08/when-sending-commercial-email-businesses-cant-unsubscribe-can-spam-compliance)
- [Email sender guidelines FAQ — Gmail Help](https://support.google.com/a/answer/14229414?hl=en)
- [Frequently Asked Questions about Canada's Anti-Spam Legislation — CRTC](https://crtc.gc.ca/eng/com500/faq500.htm)
- [Canada's Anti-Spam Legislation (CASL) Guidance on Implied Consent — CRTC](https://crtc.gc.ca/eng/com500/guide.htm)
- [Apple Mail Privacy Protection: The 2026 Guide to MPP, iOS 18, and the Metrics That Actually Matter — Sender](https://www.sender.net/blog/apple-mail-privacy-protection/)
- [How Apple Mail Privacy Protection inflates email open rates — Paubox](https://www.paubox.com/blog/how-apple-mail-privacy-protection-inflates-email-open-rates)

---
---

# Stress Test

Per the skill's "challenge the output" rule — this is **not** part of the document you hand engineering.

**Weakest part of this PRD: §1's problem statement is reconstructed, not evidenced.** I was told the build decision is made and I accepted it, but that means every metric target in §1 is `[NEEDS INPUT]` because there's no baseline behind them. A PRD that can't say what success looks like in numbers is a build spec, not a product decision. Q-P1 and Q-P4 are the two questions that would fix this, and both take you about ten minutes.

**Assumptions most likely to be wrong**

1. **D8 (default-on).** I chose it for measurement power, but it's the decision with the worst downside: if the digest lands badly, you've degraded trust with your entire user base simultaneously, and the guardrails only tell you *after* the send. A defensible alternative is default-on for users with ≥2 projects and default-off for single-project users, who get the least value from aggregation and are the most likely to read it as noise.
2. **That "what changed" is what people want.** The digest as specified is an *activity log*. The drifting member may not want to know that six items were completed — she may want to know **what needs her**. A "3 things waiting on you" email is a different, probably better, and roughly equally expensive product. §5.B's taxonomy is built for the first framing; switching to the second is a near-total rewrite of that section. **This is the highest-leverage thing to reconsider before Monday.**
3. **That weekly is the right cadence.** Chosen because you specified it. It's untested, and §8 parks it rather than resolving it.
4. **Q-E1.** If no queryable activity log exists, this PRD is a 2-week spec sitting on top of an 8-week platform project, and the timeline conversation on Monday is the wrong one.

**What a smart critic would say**

- *"Your holdout measures the wrong thing."* Fair hit. 7-day return rate after a Monday email captures people who were coming back anyway. A cleaner design is a persistent holdout measured on 4-week retention, not a single-cycle return visit. Weekly return is cheaper to read and noisier; be honest with the team that it's a proxy.
- *"You banned LLM summaries and then wrote a taxonomy that makes the email boring."* Also fair. D3 is a v1 risk-management call, not a permanent position — but if the deterministic version tests flat, the honest reading is "this content isn't compelling," not "we need better prose."
- *"Suppressing empty digests will suppress most digests."* Plausible and untested. If a large share of users have quiet weeks, D1 means low volume and an underpowered holdout. **Estimate the suppression rate from historical activity data before sprint planning** — it's a single query and it could change the rollout plan.
- *"Six guardrails and no agreed kill criterion is not a measurement plan."* Correct, and Q-P4 exists precisely because I couldn't ask you.

**Cheapest thing that would most improve this PRD:** run the suppression-rate query and answer Q-E1. Both are queries, not meetings, and either one could change the shape of Monday's conversation.
