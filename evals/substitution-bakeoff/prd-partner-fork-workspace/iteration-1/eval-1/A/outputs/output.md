# Weekly Project Digest — Discovery Session

**Skill:** `prd-partner` · **Mode:** Discovery (idea is fuzzy — "not sure yet if it's worth building" is a go/no-go question, not a build request) · **Output mode:** not yet chosen, deliberately. Discovery Mode's rule is *don't format yet*, and the skill forbids generating a PRD before you've reviewed the risk assessment. So this document is the discovery artifact, not a PRD. What it takes to unlock the PRD is spelled out at the end.

**Session constraint:** this ran unattended, so I could not grill you one question at a time. I've done the next-best thing the skill allows: every question I *would* have asked is written out with my recommended answer, my confidence, and what evidence would flip me. Assumptions are tagged `[ASSUMED]`. Blocking questions are tagged `[BLOCKING]` — those genuinely cannot be guessed and are listed together at the end.

---

## 0. The first pushback: this is a solution, not a problem

"Add a weekly digest email" is a solution statement. The skill says to push back on exactly this shape, so: **I don't yet know what's broken.**

And the pushback has teeth here, because "weekly digest of what changed in your projects" is not one feature. It's three, wearing the same name, and they want opposite designs:

| | **J1 · Re-engagement** | **J2 · Catch-up** | **J3 · Reporting outward** |
|---|---|---|---|
| **Who it's for** | Users drifting away | Active collaborators who can't keep up | Stakeholders who don't log in — managers, clients, execs |
| **Sent to** | *Inactive* users | *Active* users | Often *non-users* of the seat |
| **Content** | One highest-salience hook | Comprehensive, per-project, filterable | Narrative status, shareable/exportable |
| **Success is** | Return visits | Fewer "I missed that" moments | Stakeholder reads it; sometimes a new seat |
| **Cannibalises** | Nothing | In-app notifications (real risk) | Manual status reports people write by hand today |
| **Revenue line** | Retention | Retention, weakly | **Direct — seat expansion / stickiness with the buyer** |

Build for J1 and ship it to active users and you've added noise. Build for J2 and ship it to lapsed users and it's a wall of text about a project they've abandoned. J3 is the only one with a straight line to revenue and it's the one nobody means when they say "digest."

**The single most valuable thing this session can do is force that pick.** It's not a detail to settle during build — it changes the recipient list, the content model, the metric, and the answer to "is it worth building."

> **My call `[ASSUMED]`:** J2 (catch-up) is what you meant, because "what changed in a user's projects" is phrased from the user's own project list, not a stakeholder's. **But J3 is the one I'd build**, because it's the only variant where success shows up in revenue rather than in a soft engagement number you'll struggle to attribute. **Confidence: low.** This is `[BLOCKING]`.

---

## 1. The grilling agenda, worked through

### The problem

**Q1. What is actually broken, and for whom?**
> **My answer:** Under J2 — collaborators miss changes made by teammates between sessions, and either rediscover them late (rework, duplicated effort) or never (decisions made without them). Under J3 — someone is hand-writing a weekly status update by copying out of the tool, which is unpaid labour your product is creating.
> **What would change it:** if nobody is hand-writing status updates and nobody has complained about missing changes, then nothing is broken and this is a feature looking for a job. **That is a live possibility and it should not be brushed past.**

**Q2. How do we know it's real? `[BLOCKING]`**
> **My answer `[ASSUMED]`:** you don't have evidence yet, or you'd have led with it. Three checks, all cheap:
> 1. **Search support/sales notes and churn interviews for the words "missed", "didn't know", "status update", "keep up".** Zero hits across a year of tickets is close to a kill signal on its own.
> 2. **Count the workaround.** Are users exporting, screenshotting, or pasting activity into Slack/decks? A visible workaround is the strongest evidence a digest can have, and it's observable without asking anyone.
> 3. **Ask whether anyone has requested it.** Digests are table stakes in this category — every comparable tool ships one. Table-stakes features don't win deals; they only lose them when absent. So the question isn't "do competitors have it" (they do) — it's **"has its absence ever cost us anything?"** If not, the strategic case is weak regardless of how nice the feature is.
>
> **This is the one input I'd refuse to proceed without.** Everything downstream is arithmetic on top of it.

### The trigger — why now?

**Q3. Why this, this quarter?**
> **My answer `[ASSUMED]`:** there is no external trigger; it surfaced as a good idea. The skill tells me to push back when "why now" is really "we have capacity" — so I'm pushing back. A digest is a permanent ongoing cost (content tuning, deliverability, support, an unsubscribe surface to maintain), and permanent costs need a better reason than an open slot.
> **Legitimate triggers that would change my mind:** a churn pattern traced to disengagement; a large account asking for stakeholder reporting; a competitive loss where reporting was cited; or you already send per-event notification emails and users are complaining about volume — which flips this feature from *adding* email to *reducing* it (see §3, Option B — it's a much easier yes).

### The outcome — what does success look like?

**Q4. What metric moves, and by how much?**
> **My answer:** for J2, *weekly active accounts with ≥1 collaborative action* — not opens. For J3, *stakeholder-recipient click-through* and *seats added from digest recipients*.
> **Do not use open rate as a success metric.** Apple Mail Privacy Protection pre-fetches images and inflates opens to the point of meaninglessness; the industry has largely moved to click-to-action as the only trustworthy read ([React Emails Pro](https://reactemailspro.com/blog/email-engagement-metrics-saas)). If a PRD lands on my desk with "target 25% open rate," that's a vanity metric and I'll flag it.
> **The honest ROI frame:** this is a feature inside an existing product, so TAM/SAM/SOM is the wrong lens — I'm skipping it rather than fabricating numbers. The right lens is a break-even:
>
> ```
> Annual value ≈ (accounts reached) × (Δ logo retention in pp) × (ARPA)
>              + (seats added via J3) × (price per seat)
> Annual cost  ≈ build + ongoing tuning/support + deliverability risk (§2)
> ```
>
> `[NEEDS INPUT: accounts reached, ARPA, price per seat]` — I won't invent these.
> **The test that costs nothing:** before building, write down the Δ retention you'd bet on. **If you can't name a number you'd defend, that is itself the answer.** Most digests move logo retention by a fraction of a point; if your break-even needs more than that, stop here.

### The scope — smallest version that delivers value

**Q5. What's the smallest thing that could work?**
> **My answer:** not an email. A **manual concierge digest** (§5) — same content, sent by hand to ~20 accounts, zero code in the product. It tests the only thing in doubt (does anyone care?) without touching the pipeline that is expensive to build and risky to run.
> If it graduates to v1: **one digest, one cadence, one channel, opt-in, no preferences UI, no per-project granularity.** Everything else is v1.1.

**Q6. What's explicitly out of v1?**
> Per-project frequency controls · digest customisation UI · daily/monthly variants · Slack and in-app parity · AI-written narrative summaries · digest for non-seat stakeholders (that's J3, a separate bet) · analytics on digest content performance.

### The risks — riskiest assumption

**Q7. What kills this?**
> **The riskiest assumption is not "will people open it." It's this: *that what changed in a project is worth reading about.*** A digest is a compression function, and compression can't add signal that isn't there. If your change stream is mostly low-value churn — field edits, status flips, assignment bounces, comment threads — then the honest digest reads "47 things changed" and you have trained your users to ignore your emails.
> **Test it in a day, before anything else:** query the last 4 weeks of activity for 10 real accounts and ask, item by item, *would a teammate want to know this on Friday?* If the answer is under ~20% of items, the feature is a ranking problem, not an email problem, and the email is the wrong place to start.

**Q8. What's the downside if it flops? `[This one is under-priced and it's why I'd be careful]`**
> **A digest people ignore is not neutral — it is negative, and the damage lands outside the feature.** Gmail, Yahoo, Microsoft and Apple enforce a **0.30% spam-complaint ceiling** on bulk senders (≥5,000/day), with ≤0.10% recommended; crossing it degrades your *domain's* reputation, and since **November 2025 non-compliant mail is rejected outright rather than spam-foldered** ([PowerDMARC](https://powerdmarc.com/bulk-email-sender-requirements/), [MailOver](https://mailover.ai/blog/bulk-sender-requirements.html)).
> **Read that as a product risk, not an ops footnote:** a poorly-targeted digest can degrade delivery of your *password resets, invites and billing emails*. That converts "low-risk nice-to-have" into a feature with a tail risk attached to your core flows. Reputation is slow to recover once lost.

### Dependencies

**Q9. What has to exist first?**
> 1. **A queryable change stream** — activity feed or audit log with actor, object, verb, timestamp, project. If it doesn't exist, that's the real project and the digest is a thin layer on top. `[BLOCKING — I can't size this without knowing]`
> 2. **Authenticated sending** — SPF, DKIM *and* DMARC on the sending domain, all now mandatory at bulk volume, not optional hygiene.
> 3. **RFC 8058 one-click unsubscribe** (`List-Unsubscribe` + `List-Unsubscribe-Post` headers), with opt-outs processed **within two days**. Required by Google, Yahoo and Apple.
> 4. **A preference store** that survives the feature — even "on/off" needs a home, and it must be honoured by every future email you send.
> 5. **A legal classification decision** (§2) — it determines opt-in vs opt-out, which determines reach, which determines whether the business case closes at all.

### The market / the competition

**Q10. Who else solves this, and does it differentiate?**
> **My answer:** every mature collaboration tool ships some form of activity digest — this is a category convention, not an edge. I'm deliberately *not* asserting specifics about named competitors' current digest behaviour without checking; that's the kind of claim that ages badly. What I'd have you verify, and my prior on each:
>
> | Check | My unverified prior | Why it matters |
> |---|---|---|
> | Do the 2-3 tools you lose deals to ship a digest? | Yes, all of them | Confirms table-stakes framing → weak differentiation |
> | Is it on by default or opt-in? | Mixed; the mature ones default on, narrowly scoped | Tells you what reach is achievable without a complaint spike |
> | Do their users mute it? | Widely, in the noisier products | Direct evidence for the Q7 signal-density risk |
> | Does anyone ship the J3 stakeholder variant? | Rarely, and it's usually a paid add-on | **This is the gap worth wanting** |
>
> **The strategic read:** J1/J2 is parity work. J3 is the only version with a defensible angle, and it's the one nobody means by "digest."

---

## 2. Domain & regulatory context

Email has established norms and an enforcement regime, so per the skill I'm surfacing them now rather than letting them ambush the PRD. These are specific to this feature, not boilerplate:

| Area | Requirement | Impact on this feature |
|---|---|---|
| **Bulk sender rules** (Google/Yahoo/Microsoft/Apple) | SPF + DKIM + DMARC; spam complaints **< 0.30%** (target < 0.10%); enforced by rejection since Nov 2025 | Sets a hard ceiling on how aggressively you can enrol users. Blanket auto-enrolment of a dormant base is the single fastest route over the line. |
| **One-click unsubscribe (RFC 8058)** | `List-Unsubscribe` + `List-Unsubscribe-Post`; honoured **within 2 days** | Not a nice-to-have — a shipping requirement. Cheap to add now, expensive to retrofit across an email codebase later. |
| **GDPR legal basis** | No transactional/marketing split; it asks for a lawful basis. Service messages users expect generally rest on contract or legitimate interest ([Infobip](https://www.infobip.com/blog/transactional-email-gdpr)) | A digest of *your own project activity* has a credible legitimate-interest basis — **but only while it stays purely informational.** |
| **CAN-SPAM classification** | "Commercial" turns on *primary purpose*; promotional content that's prominent in subject line, top placement or design tips the whole message into commercial territory | **The trap:** the first time someone adds "✨ Try our new AI feature" to the digest, it becomes a commercial email — needing opt-out mechanics and a physical postal address. Decide and *write down* that the digest stays promo-free, or accept the marketing-email regime from day one. |
| **EU/UK marketing rules** | Consent or a narrow soft opt-in for existing customers | If you ever cross into promotional content, opt-out-by-default stops being safe in the EU/UK. |

**The load-bearing decision hiding in this table:** classification drives default state, default state drives reach, reach drives the business case. Opt-in gets you maybe a sliver of the base and the retention math probably won't close. Opt-out-by-default gets reach and takes on complaint risk. **This is a product decision with a legal constraint, and it belongs in discovery — not in a "compliance review" after the PRD.** `[BLOCKING]`

---

## 3. Architecture alternatives

The skill says to evaluate alternatives before committing, so — four ways to deliver "know what changed," not just four ways to build an email.

| | **A · In-app "since you were away"** | **B · Batch existing notifications** | **C · Digest service over the activity log** | **D · Event-sourced pipeline + ranking** |
|---|---|---|---|---|
| **What it is** | A banner/panel on return: what changed since last visit | Roll up per-event emails you already send into one weekly send | Cron → query activity log → template → ESP | Event stream, per-project prefs, ranked/scored content |
| **Risk** | Very low — no deliverability surface | **Low, and it *reduces* email volume** | Medium — new bulk sending surface | High — big surface, most to get wrong |
| **Complexity** | Low | Low-Medium (reuses pipeline + prefs) | Medium | High |
| **Time to value** | Days | 1-2 weeks | 3-5 weeks | 8+ weeks |
| **Extensibility** | Dead end for reach | Good — prefs and templates generalise | Good | Best, if you ever need it |
| **Waste if wrong** | Near zero | Near zero — batching is independently good | A pipeline you maintain forever | Substantial |
| **Fatal flaw** | **Can't reach lapsed users — the people J1 is for** | Only works if per-event notifications already exist | Ranking is an afterthought → the Q7 noise problem | Premature; solving a ranking problem you haven't proven you have |

**Variant worth pricing separately: Slack/Teams digest to the project channel.** In B2B it reaches the team where they already are, carries zero email-compliance exposure and no domain-reputation risk, and typically converts far better than email. **If you already have a Slack app, this may be the cheapest real test of the J2 hypothesis that exists.**

**My recommendation:**
- **If you already send per-event notification emails → Option B.** Reframing this as *"batch what we already send"* rather than *"add a new email"* strictly reduces volume and complaint risk instead of adding to it, reuses the sending path, and is a far easier internal yes. Same UI, opposite risk profile.
- **If you don't → Option C**, hard-capped: one cadence, one template, no preferences UI, opt-in.
- **Option A alongside either** — it's cheap and it serves returning users without touching email at all.
- **Option D is premature.** If ranking turns out to be the real problem (Q7), solve ranking in-app first where iteration is free.

---

## 4. User stories

Lightweight, mapped to the pain each one kills:

**Collaborator (J2)**
- As a project member, I want one weekly summary of what teammates changed, so I stop discovering decisions after they've been made.
- As a member of eight projects, I want the summary to surface what's *unusual*, so it doesn't read like a changelog.
- As someone who checks the app daily, I want to not receive this, so it doesn't become noise I train myself to ignore.

**Lapsed user (J1)**
- As someone who hasn't logged in for two weeks, I want to know if anything needs me, so I don't have to open the app to find out nothing does.

**Stakeholder (J3)**
- As a manager without a seat, I want a weekly readable status of my team's projects, so I stop asking for verbal updates.
- As a project lead, I want to forward or export the digest, so I stop rebuilding it by hand in a deck.

**Admin**
- As an admin, I want to control whether digests are on by default for my workspace, so this doesn't land in my team's inboxes unannounced.

---

## 5. The answer to "is it worth building": run a concierge probe

You asked a go/no-go question. The honest answer is **"unknown, and it's cheap to find out"** — so here is the probe rather than a guess.

**Design**
1. Pick **15-25 accounts** matching the target segment for whichever J you pick.
2. **Hand-build the digest from real data** for **3 consecutive weeks.** Script the query if you like; the send is manual, from a human's address. At this volume there's no bulk-sender exposure, no unsubscribe plumbing, no ESP, no product code.
3. Every link is tracked. Reply-to is a human.
4. **3 weeks is the minimum, and it's the whole point.** A single send measures novelty. The classic digest failure mode is week-1 enthusiasm decaying hard by week 3 — and a one-week test cannot see it. Engagement decay of this shape is well documented in email programmes generally ([The Growth Terminal](https://thegrowthterminal.com/blog/email-list-decay-why-your-open-rates-die-and-how-to-reverse-it/)).

**Pre-register these before you send. Writing them after you see the data is how teams talk themselves into building things.**

| | Criterion |
|---|---|
| **Build** | ≥30% of recipients click into the app on **≥2 of 3** sends, **and** ≥⅓ of clicks land on something they had not already seen in-app, **and** ≤1 opt-out request |
| **Pivot** | Engagement holds but clicks are all "reporting" behaviour → you've found J3, rescope to the stakeholder variant |
| **Kill** | Click-through <15%, **or** engagement drops >50% from week 1 to week 3, **or** the qualitative read is "nice, but I'd have found it anyway" |

**Run first, and separately — the one-day check:** the signal-density query from Q7. If under ~20% of change events are worth a teammate's Friday attention, **stop before the probe.** You have a ranking problem, and an email is the most expensive possible place to discover that.

**Total cost:** ~1 day for the signal check, 1-2 days of setup, a few hours a week for three weeks. Against 3-5 weeks of engineering plus permanent ongoing cost.

---

## 6. Tentative roadmap

| Phase | What | Why |
|---|---|---|
| **v0 — the probe** | Signal-density query, then 3 weeks of concierge digests to ~20 accounts | Answers your actual question before spending engineering |
| **v1** | One digest, one weekly cadence, opt-in, one template, no preferences UI. RFC 8058 unsubscribe + SPF/DKIM/DMARC from day one. Promo-free by written policy | Smallest thing that delivers value; compliance is cheap now, expensive to retrofit |
| **v1.1** | On/off per project · "no activity this week" suppression · admin workspace default | The first three things users will ask for; none are needed to learn anything |
| **v1.2** | Slack/Teams delivery of the same payload | Higher engagement in B2B, no deliverability exposure; reuses the content model |
| **v2 — J3** | Stakeholder digest: narrative summary, shareable link, non-seat recipients | The only variant with a direct revenue line. Deserves its own discovery, not a bolt-on |
| **Later / explicitly not now** | Ranking and salience scoring · daily/monthly cadences · AI-written narrative · digest content analytics · full preferences UI | Each is a real project. Do them if v1 earns them |

---

## 7. Scope creep watch

Applying the skill's discipline to my own session: I've introduced **9 items** beyond your one-line framing (J3 reporting variant, Slack channel, in-app panel, per-project prefs, admin default, ranking, suppression rules, export, notification batching). Each one felt justified in isolation. The aggregate is a quarter of work.

**What I'd cut to hold v1:** everything except the weekly email itself and its unsubscribe plumbing. Notification batching (Option B) is the one item I'd *keep* even though it wasn't in your framing — because it reduces cost and risk rather than adding them.

---

## 8. Synthesis checkpoint

> **Problem:** Unconfirmed. Best candidate: collaborators miss teammate changes between sessions, or stakeholders hand-write status reports the product could generate.
> **User:** Multi-project collaborators (J2) — though the stronger bet is non-seat stakeholders (J3).
> **Core insight:** A digest can't add signal that isn't in the change stream, and a digest people ignore actively damages the domain reputation your password resets depend on. Both are testable this week without writing product code.
> **Scope boundaries:** v1 is one weekly email, opt-in, no preferences UI, promo-free. Stakeholder reporting is a separate bet.
> **Riskiest assumption:** That what changed in a project is worth reading about. Not "will they open it."
>
> **PRD readiness: 3/10.** The shape is clear and the alternatives are mapped, but the two inputs that determine whether it's worth building — evidence of real pain, and which J we're building — are both unanswered. A PRD written today would be a well-structured guess.
>
> **Risks:**
> 1. **No validated pain.** Impact: builds a feature nobody asked for, permanently maintained. → **Blocks the PRD.**
> 2. **Low signal density in the change stream.** Impact: the digest is noise from launch. → **Blocks the PRD.** Resolvable in a day.
> 3. **Deliverability damage to transactional mail.** Impact: crossing 0.30% complaints degrades password resets and invites. → Resolvable during build via opt-in default + engagement-based suppression, but must be designed in, not patched later.
> 4. **Three features under one name.** Impact: builds something that half-serves all three and serves none. → **Blocks the PRD.**
> 5. **Opt-in reach kills the business case.** Impact: opt-in yields a fraction of the base and the retention math won't close. → Resolvable, but it's a strategy decision, not a build detail.
> 6. **No activity log to query.** Impact: the real project is the log, and the estimate is wrong by a multiple. → Resolvable, needs one answer from you.

**What I'd normally ask here:** *"Does this capture it? Risks 1, 2 and 4 look like blockers to me — do you agree?"*

---

## 9. The blocking questions

I could not honestly guess these. My recommendation is attached to each.

1. **What product is this, and what is a "project"?** `[ASSUMED: a B2B collaboration product where users belong to multiple projects containing dated activity]` — if it's consumer, or projects are single-user, J2 collapses entirely (there are no teammates to miss) and only J1 survives.
2. **Which J are we building?** My pick: **J3** for the revenue line; **J2** is what you probably meant.
3. **What's the evidence of pain?** Support tickets, churn interviews, observable workarounds. **Nothing else matters as much as this.**
4. **Does a queryable activity/audit log already exist?** Determines whether this is 2 weeks or a quarter.
5. **Do you already send per-event notification emails?** If yes, Option B changes the whole framing from *adding* email to *reducing* it.
6. **Opt-in or opt-out by default?** My pick: **opt-in for v1** — reach costs you less than a reputation incident. Revisit once complaint rates are observed.
7. **What Δ retention would you bet on?** If you can't name one, that's your answer.

**What unlocks the PRD:** answers to 1, 2, 4 and 5, plus the signal-density check. With those, Dev-Team mode is the right target if a team builds it, AI-Build (supervised — you review as it goes) if Claude Code does. I'd expect ~4-6 pages: context, personas, scope, the domain/regulatory table from §2 largely as written, requirements by area, dependencies, edge cases (empty digest, single-member project, timezone/send-window, unsubscribed-but-mentioned, deleted project mid-week), and open questions.

---

## Stress Test

*What's weakest here, and what a smart critic would say.*

**Weakest link: I argued hard from a product-context assumption I invented.** The three-jobs split, the "table stakes" read and half the roadmap all rest on this being a multi-user B2B collaboration product. If projects are single-user, §0 is largely wrong and the honest answer is a much simpler "probably not worth it — users know what they changed."

**I may have over-weighted the deliverability risk.** The 0.30% threshold is real and well-sourced, but it binds at **≥5,000 emails/day**. If you have 400 customers, you're nowhere near bulk-sender enforcement, and I've dressed an ops concern up as a strategic one. The RFC 8058 and authentication points stand regardless — they're cheap and they're table stakes — but the "this could break your password resets" framing is a *scale-dependent* argument and I stated it more confidently than the unknown scale warrants. **Treat it as conditional on volume.**

**A smart critic would say: "You've talked me out of a two-week feature with a five-week discovery process."** Fair hit. If your engineering cost is genuinely two weeks and you have any qualitative signal at all, **just build the narrowest version and watch the unsubscribe rate** — that is a legitimate alternative to my probe, and for a small team it may be the better one. My probe is the right call when the build is 4+ weeks or the recipient base is large enough that a bad send is expensive. Below that, shipping *is* the cheaper experiment. I should hold that more loosely than the document's tone suggests.

**The J3 recommendation is the least evidenced thing here.** I claimed the stakeholder variant has the clearest revenue line and is under-served. The revenue logic is sound; the "under-served" half is my prior, explicitly unverified (§1, Q10). If competitors already ship it well, my headline recommendation loses most of its force.

**What would change my overall view fastest:** one real support ticket saying "I didn't know that changed." That single artifact moves PRD readiness from 3/10 to about 6/10 — more than anything else in this document.

---

## Sources

- [Bulk Email Sender Rules For Google, Yahoo, Microsoft & Apple (2026) — PowerDMARC](https://powerdmarc.com/bulk-email-sender-requirements/)
- [Google, Yahoo & Microsoft Bulk Sender Requirements: Complete 2026 Guide — MailOver](https://mailover.ai/blog/bulk-sender-requirements.html)
- [GDPR regulations and best practices for transactional emails — Infobip](https://www.infobip.com/blog/transactional-email-gdpr)
- [What happens if you misuse transactional classification? — Review My Emails](https://reviewmyemails.com/emailalmanac/consent-and-compliance/transactional-vs-marketing-compliance/misuse-transactional-classification-risks)
- [Email Engagement Metrics for SaaS — React Emails Pro](https://reactemailspro.com/blog/email-engagement-metrics-saas)
- [Email List Decay: Why Your Open Rates Die — The Growth Terminal](https://thegrowthterminal.com/blog/email-list-decay-why-your-open-rates-die-and-how-to-reverse-it/)

---

## Closing Hook — improving this skill

Friction I hit this session, per the skill's continuous-improvement hook:

1. **Discovery Mode assumes an interactive session and breaks when run unattended.** It delegates to `/grilling`, whose core rule is one question at a time — unusable in a batch or background run. Worth adding an explicit *"Async Discovery"* fallback: emit questions with recommended answers, tag assumptions, tag blockers, and carry the analysis to a synthesis checkpoint anyway. I improvised that structure here; it should be in the skill.
2. **No template exists for "is this worth building?"** — which is the most common shape of a fuzzy idea. The skill jumps from discovery straight to PRD templates, with no *validation-probe* deliverable (probe design + pre-registered kill criteria) in between. That's arguably the highest-value artifact this skill could produce, and it's currently missing. `pm-frameworks/pol-probe-advisor` exists in the kit and should be referenced from Discovery Mode.
3. **The "answer a go/no-go" output has no home.** Discovery Mode's stated goal is "sharpen thinking, don't format yet," but a session like this produces a real, shareable artifact. The Synthesis Checkpoint is the closest thing and is too thin to stand alone.
4. **Push-back rule needs an escalation.** "Problem stated as a solution" is listed, but there's no guidance for the sharper case where *one solution name covers several incompatible jobs* — which was the key move in this session (§0). Worth naming as its own pattern: **split before you scope.**
5. **"Don't invent market sizes" needs a positive counterpart.** For features inside an existing product, TAM/SAM/SOM is the wrong lens entirely. The skill should say so and offer the break-even formula with `[NEEDS INPUT]` placeholders as the sanctioned substitute.

Per your global instruction, I'm not editing SKILL.md unattended. Items 1 and 2 are the ones I'd actually apply; 3-5 are smaller. Worth noting that this is **one session, not a pattern** — by your own "test before formalizing" rule, these should sit until a second run hits the same friction.
