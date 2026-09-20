# Weekly digest email — Discovery session (not a PRD)

**Skill:** `[SKILL]` · **Mode:** Discovery Mode · **Output mode:** not chosen yet, deliberately.

**Why Discovery and not PRD:** *"Not sure yet if it's worth building"* is the entire signal. Writing a PRD now would convert an open question into a settled-looking document — the most expensive mistake available here, because a polished spec gets staffed. We sharpen first. No template until you've seen the risk list.

**One note on format:** this is normally a back-and-forth, one question at a time. It's running unattended, so every question I'd have asked is written out below with my best answer attached and labelled:

- **[ASSUMPTION]** — my default, stated so you can knock it down in one word
- **[YOU HAVE THIS]** — you can answer from data you already hold; I've named where
- **[NEEDS INPUT]** — nobody can answer it from the outside; it's a genuine gap

---

## 0. The pushback, before any questions

**"Weekly digest email" is a solution wearing a problem's clothes.** You've named the artifact, the cadence, and the channel — three decisions — before naming what's broken. The implied problem is roughly *"users lose track of what happened in their projects while they were away."* That's a reasonable guess, but it's mine, not yours.

Two words in the request are doing unexamined work:

- **"Weekly."** Cadence should fall out of how fast projects actually change. If the median project sees activity on 1.2 days a month, a weekly email is mostly an email about nothing. If it changes hourly, weekly is a scrollable archive nobody reads. Cadence is an output of the data, not an input to the design.
- **"Email."** It's the only option in the solution space that delivers the answer *where your product isn't*. Every alternative — in-app feed, unread badge, Slack, on-demand catch-up — keeps the user inside the thing you're trying to make valuable. Email buys reach at the price of engagement happening in Gmail. That's a real trade, and it's currently unmade.

---

## 1. The fork that decides this whole question

Everything downstream depends on one fact I don't have:

> **Are projects single-player or multiplayer?**

| | Solo projects | Shared projects |
|---|---|---|
| What the digest contains | The user's own actions, replayed to them | Things other people did while they were away |
| What it is | A receipt | News |
| Value | Near zero — they were there | Potentially high — this is information they cannot get otherwise |
| Realistic outcome | Opened twice, unsubscribed, mild brand damage | Becomes a habit surface and a re-entry link |

**[ASSUMPTION]** Projects are at least sometimes multi-user, and the digest's real job is *"tell me what other people did."* If projects are overwhelmingly single-user, **my recommendation is don't build it** — build "here's where you left off," which is a different feature with a different trigger (return-to-app, not Monday 9am).

**[YOU HAVE THIS]** Percentage of active projects with ≥2 contributors who made a change in the last 30 days. One query. It decides whether the rest of this document is relevant.

---

## 2. The interrogation

### The problem — what's broken, for whom, and how do we know?

**My answer [ASSUMPTION]:** Collaborators who aren't in the product daily lose the thread on projects they care about. They come back and can't tell what changed since they last looked, so they either ask someone or re-read everything. The cost is felt by the *low-frequency* user, not your power users.

**How we'd know — and this is where it's currently thin [YOU HAVE THIS]:**
- Support tickets or messages containing "what changed", "did anyone", "I missed", "who updated"
- Sessions where a returning user's first action is scrolling history or opening a changelog/activity view
- Churn or dormancy concentrated in *collaborator* seats rather than owner seats

**Push-back:** if none of those show anything, the honest read is that this is a feature you want to exist, not a pain users are having. That's allowed — but it changes the bar from "does it work" to "is it cheap," and the build cost section below says it may not be.

### The trigger — why now?

**My answer [NEEDS INPUT].** I can't find a "why now" in the request, and "we have capacity" is explicitly the weakest form. Legitimate triggers would be: a retention cliff you just measured, a competitor shipping it and prospects asking, a sales objection, or an activity/event log you just built for another reason that makes this nearly free. **If the real answer is "it came up and it sounded obviously good," that is itself an argument for the probe in section 7 rather than a build.**

### The outcome — what does success look like?

**My answer [ASSUMPTION]:** Success is *returning to the product and doing something*, not opening the email. Proposed shape:

| Layer | Metric | Why this one |
|---|---|---|
| Primary | Return-and-act within 48h of send, digest-attributed vs. matched control | The only thing that pays for the build |
| Secondary | Click-to-open ratio (clicks ÷ opens) | Tells you whether the *content* is right, separate from the subject line |
| Guardrail | Unsubscribe + spam-complaint rate | See section 5 — this one can hurt the rest of your email |
| Guardrail | Notification opt-out rate overall | A digest that pushes users to kill *all* email is a net loss |

**The trap to avoid: open rate is a broken metric in 2026.** Apple Mail Privacy Protection and Gmail image proxying fire the tracking pixel without a human involved, inflating reported opens and making the number useless as a success signal ([benchmark aggregators put the inflation at roughly 10–15%](https://owlclaw.com/benchmarks/email-marketing-benchmarks/), and the direction matters more than the figure). If the success metric in the eventual PRD is "40% open rate," the PRD is wrong before it's written.

### The scope — smallest version that delivers value? What's out?

**My answer [ASSUMPTION]:** The smallest honest v1:
- One email, weekly, per user (not per project), covering all projects they're a member of
- Only changes made **by other people**, since the user's last visit — not a fixed 7-day window
- **Suppressed entirely when there is nothing to say.** Non-negotiable; see section 6
- Global on/off plus one-click unsubscribe. No per-project controls, no frequency picker

**Explicitly out of v1:** per-project preferences, frequency selection, daily/monthly variants, digest-of-digests for managers, Slack parity, mobile push parity, AI summarisation of what changed.

### The risks — riskiest assumption, and what could kill this?

**My answer:** Riskiest is that *"what changed" is legible at all.* A digest is only readable if your change events carry enough semantic weight to render as sentences a human wants to read. "Sarah moved 3 tasks to Done and commented on the launch plan" is news. "12 records updated" is noise with a timestamp. **[NEEDS INPUT]:** do your events carry actor, object, and verb, or just table-level mutations? If it's the latter, the digest work is mostly *event modelling*, not email.

### Dependencies — what has to exist first?

**My answer [ASSUMPTION]:** an activity/event log with actor+verb+object, per-user last-seen timestamps, an authenticated transactional email path, an unsubscribe/preference store, and a scheduled job runner with per-timezone send windows. **If the event log doesn't exist, that's the project — the email is the last 20%.** Section 4.

### The market / competition

**My answer:** TAM/SAM/SOM is not a meaningful question for a notification feature inside an existing product — I'm not going to manufacture a market size for it, and I'd push back on anyone who asks for one. The competitive question that *is* real: digests are table stakes in collaboration tools (Asana, Linear, Notion, GitHub all ship some form), which cuts both ways. **[YOU HAVE THIS]** — the useful check is whether prospects or churned accounts have ever cited it, not whether competitors have it. Parity features win no deals; their absence occasionally loses one.

---

## 3. What would have to be true for this to be worth building

This is the section the request was actually asking for. Each row is falsifiable, and three of the five are checkable this week without writing product code.

| # | What must be true | Why it matters | Cheapest check | Status |
|---|---|---|---|---|
| 1 | A meaningful share of projects are **multiplayer** and change while a member is away | Otherwise the digest is a receipt | One query: projects with ≥2 contributors active in 30d | **Unknown — blocking** |
| 2 | There's a population of **low-frequency members** who'd get news, not olds | Daily users already know; they'd get spam | Session-frequency histogram per project member | **Unknown — blocking** |
| 3 | Change events are **semantically legible** (actor, verb, object) | Decides whether this is a 2-week or 8-week build | Read the event schema, or check if one exists | **Unknown — blocking** |
| 4 | A returning-user visit is **worth more than the deliverability risk** you take | Section 5 — the downside isn't zero | Model it: expected returns/week × value vs. complaint-rate exposure | **Resolvable during probe** |
| 5 | Users would **choose** to receive it | Consent is both a legal and a quality gate | Offer it as an opt-in in-product; count take-up | **Resolvable during probe** |

**Read of the table:** three blockers, all answerable from data you already have, none requiring a build. That's the strongest possible argument for not writing a PRD today.

---

## 4. The cost side — what you'd actually be building

"Worth building" is a ratio, and the denominator is usually wrong on this feature because people price the email and forget the substrate.

| Build shape | What it is | Good | Bad | Realistic effort |
|---|---|---|---|---|
| **A. Query-on-send** | At send time, query each domain table for rows changed since `last_seen` | No new infrastructure; fastest to a first send | Query cost scales with users × tables; no history; every new object type means touching the digest; "what changed" is inferred from `updated_at`, so it can't tell an edit from a rename | ~1–2 weeks **if** timestamps exist everywhere |
| **B. Event log** | Emit `actor / verb / object / project / timestamp` events; digest reads the log | Legible sentences, reusable by in-app feed, audit, analytics, webhooks; digest becomes a view over it | You're building a platform primitive to ship an email; backfill gives you no history for existing projects | ~4–8 weeks, mostly not email |
| **C. Hybrid** | Event log for the 3–5 verbs that matter, query-on-send for the rest | Ships a good digest without a full event system | Two code paths; the seam drifts | ~2–3 weeks |

**My recommendation: C, and only after the probe.** Do not let this become "we need an event bus first" — that's a six-month detour justified by an email. Equally, don't pick A and then discover the digest reads like a database changelog.

*This is a discovery-stage sketch, not an architecture decision. If it proceeds, the PRD gets a proper ADR so the builder can't wander back to a rejected approach.*

---

## 5. Constraints that change the maths (flagging early, not as compliance boilerplate)

A recurring digest to your whole user base is a **bulk email**, and bulk email is regulated by the mailbox providers as well as by law. Two of these change the go/no-go calculus, so they belong in discovery rather than an appendix:

1. **A boring digest can damage the email you actually depend on.** Mailbox providers score reputation partly on engagement; sustained low engagement teaches Gmail to distrust your domain, and that distrust doesn't stay in its lane — it reaches password resets, invites, and verification mail ([Mailgun on transactional vs. marketing reputation](https://www.mailgun.com/blog/deliverability/transactional-emails-vs-marketing-emails/)). **Mitigation: send the digest from a separate subdomain** so the two reputations are isolated. Cheap if decided now, painful to retrofit.
2. **Hard thresholds exist.** Google's bulk sender guidance requires authentication (SPF/DKIM/DMARC), one-click unsubscribe honoured within two days, and keeping spam complaints below 0.3% — with 0.1% as the level to actually sit under ([Google sender guidelines](https://support.google.com/a/answer/14229414?hl=en)). Microsoft began *rejecting* non-authenticating bulk mail to Outlook/Hotmail on 5 May 2025 at a 5,000/day threshold it has signalled it may drop entirely ([dmarcian](https://dmarcian.com/microsoft-enforces-spf-dkim-dmarc/)).
3. **Consent.** Under GDPR this is not transactional mail — it's a communication the user didn't individually request, so it needs a lawful basis and a working opt-out; CAN-SPAM requires the unsubscribe path regardless. Practically: **launch opt-in, not opt-out.** Opt-in also doubles as evidence for row 5 of the table above — a feature nobody opts into has answered your question for free.

**What this adds to the build:** a subdomain and its DNS/warm-up, `List-Unsubscribe` with one-click (RFC 8058), a preference store, suppression handling, and complaint-rate monitoring. Perhaps a week, and it is not optional.

---

## 6. The scope creep this feature attracts (pre-emptive)

Nothing has been added yet — but this feature has a known accretion path, and each item arrives individually justified:

> per-project settings → frequency choice (daily/weekly/monthly) → "only notify me about things I follow" → a manager roll-up → Slack parity → mobile push parity → AI summaries of the changes → an in-app version of the same feed → digest analytics

That list is how a two-week feature becomes a quarter. **The discipline: v1 is one email, one global toggle, one cadence.** Everything above goes in a backlog now, at discovery time, so it has a home and doesn't have to fight its way into v1.

**And the one non-negotiable rule, because it's the single most common failure mode:** if there's nothing to report, send nothing. An email that says "no activity this week" trains users that your emails are worthless, and it costs you deliverability to do it.

---

## 7. What I'd do instead of building — the probe that settles it

Three weeks, no product code, answers the question.

**Setup:** pick 30–50 accounts with genuinely multiplayer projects. Hand-assemble the digest — a query plus a human editing the sentences — and send it from a real address. Wizard-of-Oz.

**What you learn that a build wouldn't teach you faster:** whether the events are legible enough to write human sentences from (you'll find out in about twenty minutes of trying), and whether anyone clicks.

**Decision criteria — proposed shapes, calibrate the numbers against your own baselines rather than importing mine:**

| Signal | Go | Kill |
|---|---|---|
| Click-through on the digest | Sustained across all three weeks | Week 3 well below week 1 (novelty, not value) |
| Return-and-act within 48h vs. matched control | Clear lift | Indistinguishable from control |
| Assembly effort | Sentences write themselves from existing events | You keep needing to look things up to make it readable → the real project is the event log |
| Replies / opt-outs | People reply asking for more | Opt-outs during a 50-person opt-in pilot is a strong kill signal |

**A cheaper pre-probe, if even that's too much:** put "Email me a weekly summary" in notification settings as a checkbox that currently does nothing but record intent. Two hours of work. Take-up rate over two weeks tells you whether demand exists before you send a single email. (Be straight with people about it — label it "coming soon" rather than letting it look live.)

---

## 8. Synthesis checkpoint

> **Problem:** Members of shared projects who aren't in the product daily can't tell what changed while they were away — *hypothesised, not yet evidenced.*
> **User:** The low-frequency collaborator, not the daily power user or the project owner.
> **Core insight:** A digest is only worth building where projects are genuinely multiplayer and change events are semantically legible; otherwise it's a receipt for work the user already did, mailed to them.
> **Scope boundaries:** One weekly email per user, other people's changes only, since-last-seen, suppressed when empty, global opt-in. Everything else is backlog.
> **Riskiest assumption:** That your change events carry actor/verb/object richly enough to render as sentences a human wants to read. If they don't, this is an event-modelling project with an email attached, and the cost estimate is wrong by 3–4x.
>
> **PRD readiness: 3/10** — the solution shape is clear enough to spec, but the problem underneath it is unstated and unevidenced, and the one fact that decides the feature's value (multiplayer vs. solo) is unknown. A PRD written today has roughly even odds of specifying the wrong feature competently.
>
> **Risks:**
> 1. **Digest is a receipt, not news** (solo-heavy projects) — feature lands, gets ignored, small trust cost. **Blocks PRD.** One query resolves it.
> 2. **Events aren't legible** — digest reads like a changelog; effort is 3–4x the estimate. **Blocks PRD** — it changes what's being built, not just how well.
> 3. **No evidenced user pain** — risk of building a feature that sounded obviously good. **Blocks PRD** in the sense that success metrics can't be set against a baseline that was never measured.
> 4. **Deliverability contagion** — low engagement degrades the domain reputation your password resets ride on. **Resolvable during build** if the subdomain decision is made up front; expensive to retrofit later.
> 5. **Cadence chosen before data** — "weekly" may be wrong for your actual change frequency. **Resolvable during the probe.**
> 6. **Scope accretion** — the eight-item creep list in section 6. **Resolvable**, by writing the backlog now rather than later.

**The confirm I'd normally be waiting on:** *Does this capture it? Risks 1–3 are the blockers — are any of them already answered on your side?*

---

## 9. What happens next, by branch

| If | Then |
|---|---|
| Projects are mostly multiplayer **and** events are legible | Skip the probe, go to **PRD Mode**. I'd need the audience: AI coding agent, dev team, or stakeholders? **[ASSUMPTION]** given "solo-founder who codes with AI," AI-Build is the likely default — which would also need the build model (supervised vs. hold points) |
| Multiplayer but events are thin | Probe first. The probe's real output is a decision on build shape B vs. C, not a yes/no on the digest |
| Projects are mostly solo | **Don't build this.** Build "here's where you left off," triggered on return rather than on a schedule. Different feature, different PRD, much cheaper |
| You can't get the data this week | Run the two-hour checkbox pre-probe. It's the cheapest signal available |

**What I need from you to move:** three numbers — multiplayer project share, member session-frequency distribution, and whether an actor/verb/object event log exists. Everything else in this document I can carry on assumptions; those three I can't.

---

## Stress Test

**What's weakest here.** The entire analysis rests on the multiplayer/solo fork, and I invented that frame without knowing your product. If "projects" in your product means something else — a client engagement, a build, a document workspace with an external audience — the fork could be the wrong axis entirely and I've organised the whole discovery around a distinction that doesn't carry weight. That's the first thing to check, before any of the numbers.

**Assumptions that could be wrong.**
- *That a digest's value is "news from others."* A counter-case exists: solo users with many projects can genuinely lose track across projects even when they made every change themselves. Breadth can create the same forgetting that absence does. If your users run 10+ projects each, my "receipt, not news" verdict is too strong.
- *That opens are a broken metric.* True in aggregate, but if your audience skews non-Apple and you can measure proxy-open patterns, opens may still be directionally usable — I've dismissed the metric harder than the evidence strictly supports.
- *That the event log is the hidden cost.* If you're on a stack with decent audit logging already (many ORMs and Postgres setups get you most of the way), option A is cheaper than I've priced it and the build could be genuinely small.

**What a smart critic would say.**
1. *"You've made a two-week feature sound like a research programme."* Fair hit. If the build really is two weeks, the probe's three weeks costs more than just shipping it behind a flag to 5% and reading the same signals from a real feature. The probe only wins if the build is genuinely 4+ weeks — which is exactly what section 4's uncertainty is about. **If you can confirm option A is viable, ship the flagged version instead of the probe.**
2. *"Deliverability is overweighted."* At small volume you're nowhere near the thresholds, and the subdomain advice is what high-volume senders do — the search evidence itself says single-domain is usually right below meaningful volume. Counter-argument: the decision is nearly free *now* and expensive later, which is why I'd still take it.
3. *"You told him not to build it without seeing a single user."* Correct, and I haven't — I've said the three facts that decide it are cheap to obtain and currently unobtained. That's a weaker and more defensible claim than "don't build it," and it's the one I'm standing behind.

**The thing I'd most want to be wrong about:** that you already know the multiplayer answer and this whole document is a slow route to a decision you could have made in a sentence. If so, tell me the number and I'll go straight to the PRD.

---

### Sources

- [Email sender guidelines FAQ — Gmail Help (Google)](https://support.google.com/a/answer/14229414?hl=en) — authentication, one-click unsubscribe, spam-rate thresholds
- [Microsoft Enforces SPF, DKIM, DMARC for High-Volume Senders — dmarcian](https://dmarcian.com/microsoft-enforces-spf-dkim-dmarc/) — 5 May 2025 rejection policy, 5,000/day threshold
- [Transactional vs. Marketing Emails — Mailgun](https://www.mailgun.com/blog/deliverability/transactional-emails-vs-marketing-emails/) — engagement-driven reputation and stream separation
- [Email Sender Reputation — Mailgun](https://www.mailgun.com/state-of-email-deliverability/chapter/email-sender-reputation/) — subdomain separation practice by volume
- [Email Marketing Benchmarks — OwlClaw](https://owlclaw.com/benchmarks/email-marketing-benchmarks/) — Apple MPP / proxy-open inflation of reported open rates

*Benchmark figures above are vendor aggregates across mixed industries, not comparable to your product's baseline. I've used them for direction only, and deliberately have not set any target from them — per this skill's rule, invented metrics don't belong in a PRD, and they don't belong in the discovery that precedes one either.*
