**Skill:** `prd-partner` — PRD Mode, **Stakeholder** output, produced as a **Dev-Team → Stakeholder mode conversion**.

---

## Conversion gap analysis (per the skill's mode-conversion step)

Normally I'd confirm this with you before generating. This run is unattended, so I'm stating it and proceeding.

| | |
|---|---|
| **Carried over** | Problem + evidence, solution concept, scope in/out, success criteria, rollout, both open questions |
| **Added** | Executive summary, business-impact model, why-now, competitive context, deliverability/regulatory risk, resource ask, recommendation with alternatives, risk table |
| **Removed** | Data model (`digest_send_log`, source tables), R1–R6 requirement IDs, HTML/plaintext rendering detail, batching mechanics |
| **Reframed** | Success criteria → outcome metric vs. activity metrics; rollout → measured rollout with a holdout |

**Assumptions I acted on (correct me if any is wrong):**

1. **Audience and slot.** Exec staff — CEO / CPO / CTO / VP Eng / VP CS — in a ~20-minute Thursday agenda item. Written to be read cold in 5 minutes.
2. **What's actually being decided.** The source spec says *"Approved for build."* An exec review of an already-approved build is either a resourcing decision or an FYI. I wrote it as a **decision doc**: the ask is resourcing plus one genuine fork (holdout vs. straight ramp). If Thursday is informational, delete §7 and the alternatives table in §8.
3. **No invented numbers.** I have no access to segment counts, ARPU, churn-by-cohort, or support cost per ticket. Every such figure is flagged `[NEEDS INPUT]` rather than filled in. The arithmetic I *did* do is shown inline so it can be checked.
4. **"Week 1 / 2 / 4"** in the source rollout is relative to build completion, not calendar dates.
5. **Jurisdiction unknown**, so regulatory framing is by mailbox-provider rules (which apply globally and are enforced mechanically) rather than by statute.

---
---

# Weekly Project Digest — Executive Review

**For decision · Thursday** · Owner: Product · Status: approved for build, pending resourcing

---

## 1. Executive Summary

We want to send each customer one email a week telling them what changed across their projects while they were away. It's aimed at our multi-project owners — the segment that logs in **less than half as often** as single-project owners (2.1 vs. 4.4 times per week) and that generates roughly **40 support tickets a month** all saying the same thing: *"I didn't know X changed."*

The data we need already exists in the product; nothing new has to be instrumented. The build is scoped and the rollout is four weeks.

Two things need an exec decision, and neither is a build detail: **the resourcing** (§7), and **whether we ship this as a measured experiment with a holdout or as a straight ramp** (§4). I recommend the holdout.

**Not being decided Thursday:** the feature concept, cadence, or channel. Those are settled.

---

## 2. Problem & Opportunity

### The problem, in business terms

Our most valuable account shape — customers running three or more projects — is the one drifting furthest from the product. They log in 2.1x/week against 4.4x for one- and two-project owners. They come back to a product where too much has changed to reconstruct, so they ask a human instead: ~40 tickets/month, **~480/year**, of pure "what did I miss."

Those tickets are the *visible* version. The invisible version is the customer who doesn't file a ticket and quietly disengages. We are treating the ticket count as the tip, not the total.

**Important caveat, stated up front:** 2.1 vs. 4.4 is a *correlation*. Multi-project owners may log in less because they delegate day-to-day work, not because they're lost. If that's the dominant cause, this feature will produce a well-opened email and a flat login curve. §4 is designed to tell us which world we're in within eight weeks instead of guessing.

### Why now

- **The data is already there.** Project events, membership, and preferences are captured today. This is an assembly job, not a new capability.
- **Parity has arrived.** Scheduled summaries are now table stakes in this category — Asana ships a daily summary plus AI project recaps, and its own customers are publicly asking for *more* digest configurability. Not having one is increasingly a noticed absence.
- **The compliance window is open, not closing.** Mailbox-provider rules (§5) are now fully enforced. Doing this correctly today is cheap. Doing it badly is expensive in a way it wasn't three years ago.

### Market context

TAM/SAM/SOM is the wrong lens here — this is a retention feature inside an existing product, not a new market entry. The sizing that matters is internal:

| Input | Value |
|---|---|
| Customers owning 3+ projects | `[NEEDS INPUT]` |
| Share of ARR they represent | `[NEEDS INPUT]` |
| Their current annual churn vs. 1–2 project owners | `[NEEDS INPUT]` |

Those three numbers convert this from "a nice email" into a sized bet. Without them I can give you the mechanism but not the magnitude. **Ask: CS/Finance to supply before the meeting if possible.**

---

## 3. Proposed Solution

### The narrative

Maya runs delivery at a 40-person agency and owns five client projects. She logs in Tuesday, sees a wall of activity, and can't tell what's new since Thursday. Last month she missed a scope comment on the Northwind project for six days and had to apologise to the client.

Under this feature, Monday 08:00 in Maya's own timezone, she gets one email: five project blocks, each showing items added, items completed, comments received, and who joined. The Northwind comment is line two. She clicks straight into it. Total elapsed time: forty seconds, before she's opened the app.

### Scope

**In:** per-project item deltas, comment counts, membership changes, one call-to-action per project. Weekly, Monday 08:00 local. Opt-out at both the user and the project level.

**Out, and why:**

| Excluded | Why |
|---|---|
| Real-time and daily digests | The segment's problem is week-scale drift, not hour-scale. Higher cadence multiplies complaint risk (§5) for a problem that isn't hourly. |
| Slack / Teams delivery | Real upside, but adds an integration and per-workspace auth surface. Gated on v1 results — see §8. |
| Mobile push | Same reasoning; different plumbing, no new information. |

### Phasing

| Phase | What | When |
|---|---|---|
| 0 | Internal dogfood | Week 1 |
| 1 | 10% of 3+ project owners, **with a matched holdout** | Week 2 |
| 2 | Full rollout to the segment | Week 4 |
| 3 | Extend to 1–2 project owners, or Slack delivery | Gated on §4 outcome |

---

## 4. Success Metrics & Business Impact

### The distinction that matters

Open rate and click-through are **activity** metrics. They tell us the email works as an email. They do not tell us the feature works as a product. Only one metric here is an outcome:

| | Metric | Target | Reads as |
|---|---|---|---|
| **Outcome** | Weekly logins, 3+ project owners | 2.1 → 2.8 in 8 weeks | Did behaviour change |
| Activity | Open rate | ≥35% by week 4 | Is the email wanted |
| Activity | Click-through | ≥8% | Is the content useful |
| Guardrail | Unsubscribe rate | <0.5% per send | Are we annoying people |
| **Guardrail — missing** | **Spam complaint rate** | **<0.10%** | **Are we damaging our domain (§5)** |

For scale: 2.1 → 2.8 closes about **30%** of the gap to single-project owners. That's an honest, non-heroic target.

### Two problems with the metrics as written

**1. The outcome metric can grade its own homework.** One of the open questions in the source spec — *does a digest click-through count as an active session?* — is not a tracking detail. If the answer is yes, the email mechanically produces the logins it's being measured on, and the metric becomes unfalsifiable. **Recommendation: pre-register the answer as "no," and report digest-originated and organic sessions separately.**

**2. A straight ramp gives us no counterfactual.** An 8-week behavioural metric measured across a period in which everything else also changes cannot be attributed. **Recommendation: hold back 10–20% of the segment through week 8.** Cost: a few weeks of delayed value for a fifth of one segment. Benefit: we learn whether digests cause engagement, which decides every subsequent investment in this direction — Slack, daily, mobile, all of it.

### Business impact

I won't fabricate a number. Here is the model, ready to be filled:

- **Support deflection:** 480 tickets/year × `[NEEDS INPUT: fully loaded cost per ticket]`. Deflection is partial, not total — some of those tickets are the user wanting a human.
- **Retention:** `[NEEDS INPUT: # of 3+ project owners]` × ARR × `[NEEDS INPUT: retention delta per unit of login frequency]`. This is the term that dominates the model, and it is also the one we have the least evidence for — which is precisely the argument for the holdout.
- **Cost side:** engineering (§7), plus ESP volume and a dedicated sending subdomain (§5).

---

## 5. Domain & Regulatory Context

**The risk here is not a low open rate. It is breaking our transactional email.**

Once we send weekly bulk mail, we become a "bulk sender" in the eyes of Google, Yahoo, Microsoft, and Apple, and their rules are enforced mechanically — as of 2026, non-compliant bulk mail gets permanent 550 rejections rather than a spam-folder demotion.

| Requirement | Why the exec team should care |
|---|---|
| One-click unsubscribe (RFC 8058), honored within 2 days | Already in the plan. Good. Non-negotiable. |
| Spam complaint rate below 0.3%, target below 0.10% | **This guardrail is absent from the current success criteria.** It is the one that gets mail blocked. |
| Authenticated sending (SPF, DKIM, DMARC) | Table stakes; confirm we are aligned before the first send. |
| Sender reputation is per-domain | **If the digest attracts complaints, password resets, invitations, and receipts on the same domain get throttled or rejected with it.** |

**Recommendation: send the digest from a dedicated subdomain, separate from transactional mail.** This is cheap now and effectively impossible to retrofit after reputation damage. It needs a decision before the first send, not after.

Two design choices already in the plan are, in effect, complaint-rate defences and should be understood as such: suppressing the email when there is nothing to report, and per-project opt-out. A third is still open — whether to send a digest whose only content is the user's own activity. Sending someone a summary of what they themselves did is a reliable way to earn a spam complaint. **Recommendation: suppress.**

---

## 6. Key Risks & Dependencies

| Risk / Dependency | Impact | Mitigation / Status |
|---|---|---|
| Logins are low for structural reasons (delegation), not confusion | Feature succeeds as an email, fails as a retention lever | Holdout (§4) detects this by week 8 rather than after full investment |
| Spam complaints damage domain reputation | Transactional mail degraded — password resets, invites | Dedicated subdomain; complaint-rate guardrail; kill switch with a named owner |
| Unsubscribe attrition compounds | At the 0.5%/send ceiling, **~23% of the list is gone within a year** (0.995⁵² ≈ 0.77). At 0.10%, ~5%. The per-send number looks harmless; the annual number is not. | Treat 0.5% as an emergency ceiling, not a target. Manage to ≤0.10%. |
| Digest becomes a substitute for the product | Opens go up, logins go flat or down | CTA per project; measure logins, not opens, as the outcome |
| Event data quality in `project_events` | Wrong or noisy digests erode trust on first contact | Dogfood week (Phase 0) is the check; hold rollout if it surfaces gaps |
| Deliverability ownership | Nobody watching complaint rate after launch | **Open — needs a named owner. See §9.** |

---

## 7. Resource Ask & Timeline

| Item | Ask |
|---|---|
| Engineering | `[NEEDS INPUT: eng-weeks — eng lead is TBD in the source spec, which is itself a gap]` |
| Design | Email template, HTML + plaintext |
| Lifecycle / deliverability owner | Ongoing, post-launch — small but must be named |
| Infrastructure | Dedicated sending subdomain; ESP volume tier |
| Calendar | 4 weeks to full rollout; 8 weeks to a readable outcome |

**Note:** the source spec lists the eng lead as TBD while marking the work approved for build. Approved-without-an-owner is how things sit still. Worth closing Thursday.

---

## 8. Recommendation

**Ship the weekly email digest to 3+ project owners, with a 10–20% holdout maintained through week 8, a dedicated sending subdomain, and a spam-complaint guardrail added to the success criteria.**

The mechanism is sound, the data cost is near zero, and the category has made this table stakes. The genuine uncertainty is whether digests *cause* engagement or merely correlate with it — and the holdout converts that from an argument into a measurement for a very small price.

| Option | Pros | Cons | Why not recommended |
|---|---|---|---|
| Do nothing | Free | The problem is specifically about people who *aren't* in the product | Doesn't address absence |
| In-app activity feed instead | No deliverability risk, no unsubscribe attrition | Requires the login we're trying to cause | Circular — solves the problem only for users who don't have it |
| **Weekly email digest + holdout** | Reaches the absent user; data exists; learnable | Deliverability risk; 8 weeks to a verdict | **Recommended** |
| Daily or real-time | Faster signal | Multiplies complaint risk; wrong time-scale for the problem | Cadence mismatch |
| Slack/Teams delivery first | Higher engagement where teams already are | Integration + auth surface; narrower reach | Right idea, wrong sequence — revisit as Phase 3 |

---

## 9. Open Questions

**For this exec group:**
1. Does a digest click-through count as an active session? *(Recommendation: no. This determines whether our headline metric is honest.)*
2. Holdout or straight ramp? *(Recommendation: holdout.)*

**For Engineering:**
3. Dedicated sending subdomain — approve before the first send. *(Recommendation: yes.)*
4. Who is the eng lead?

**For Customer Success:**
5. Who owns post-launch complaint-rate monitoring and holds the kill switch?

**For Product (not exec-blocking):**
6. Digest containing only the recipient's own activity — send or suppress? *(Recommendation: suppress.)*

---
---

## Stress Test — what's weakest here

*For Omri, not for the exec deck.*

**Weakest link: the whole business case rests on three numbers I don't have.** Segment size, their share of ARR, and retention-per-login-frequency. Without those, §4's impact model is a shape, not a case, and an exec can legitimately say "come back when you've sized it." If you can get even rough figures from CS or Finance before Thursday, this document roughly doubles in force. That's the single highest-leverage hour before the meeting.

**The assumption most likely to be wrong: that logins are the right outcome metric at all.** I inherited it from the source spec and reframed it, but I didn't challenge it hard enough. Login frequency is itself a proxy — for value received, and ultimately for renewal. A multi-project owner who reads the digest, replies to one comment by email, and never logs in may be *perfectly* served and would score as a failure. If renewal or seat expansion data exists at the cohort level, that's the better outcome metric and logins becomes an intermediate one.

**What a sharp exec will say:**

- *"You're asking for a holdout on a feature you already approved for build. Which is it?"* — Fair. The honest answer is that approval-to-build and approval-to-ramp-blind are different decisions, and the spec conflated them. Be ready to say that plainly rather than defend the framing.
- *"40 tickets a month is a rounding error."* — Probably true on its own. The support number is evidence of a *symptom*, not the size of the *prize*. Don't let the deflection line carry weight it can't bear; the retention argument is the real one, and it's the one currently unsized.
- *"Everyone ships digests and nobody claims they moved retention."* — This is the strongest attack and I don't have a counter. Category parity is an argument for building it; it is not an argument that it works. The holdout is the only honest response.

**What I may have over-engineered:** the deliverability section is the most confident part of this document and also arguably the least exec-relevant — it could be read as an implementation detail dressed up as a risk. I kept it because the failure mode (transactional mail collateral damage) genuinely is a business risk and the subdomain decision is irreversible-in-practice. But if the room is impatient, §5 compresses to two lines and a recommendation.

**One thing I could not verify:** competitor claims. I confirmed Asana ships a daily summary and AI project recaps, and that its customers are requesting more digest configurability. I did *not* verify the equivalent for Linear, Notion, or Basecamp, so I deliberately wrote "table stakes in this category" rather than naming products I hadn't checked. If a competitive slide is expected, that needs a real pass.

---

**Sources consulted for §5 and the competitive claim in §2:**

- [Bulk Email Sender Rules For Google, Yahoo, Microsoft & Apple (2026) — PowerDMARC](https://powerdmarc.com/bulk-email-sender-requirements/)
- [2026 bulk email sender requirements checklist — Red Sift](https://redsift.com/guides/bulk-email-sender-requirements)
- [Gmail and Yahoo sender requirements — Sender.net](https://www.sender.net/help/deliverability-compliance/gmail-and-yahoo-sender-rules/)
- [Asana Smart Summaries: AI project recaps — Asana Help Center](https://help.asana.com/s/article/smart-summaries?language=en_US)
- [New! Daily Summary Inbox Notification — Asana Forum](https://forum.asana.com/t/new-daily-summary-inbox-notification/102655)
- [Feature Request: Customizable Scheduled Digests — Asana Forum](https://forum.asana.com/t/feature-request-customizable-scheduled-digests/1139144)
