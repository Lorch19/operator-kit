**Skill:** `[SKILL]` — PRD Mode, **Stakeholder** output. Converted from the existing Dev-Team PRD.

---

### Conversion note (what I did and what I assumed)

This ran unattended, so I made the calls below rather than asking. Each is a real assumption, not a detail — challenge any of them.

| Assumption | Why | If wrong |
|---|---|---|
| "Exec review" = decision forum, not an FYI | You said Thursday, with a named audience. Info updates don't need a resource ask; decision docs do | Section 7 and the Recommendation are wasted space — cut them |
| The build is still approved, not up for reversal | Source spec says "Approved for build" | Section 8 should lead with a build/don't-build call, not a how-to-proceed call |
| Exec audience is non-technical on email infrastructure | Standard | Section 5 can compress to two lines |
| Thursday = 17 Sep 2026 (tomorrow) | Today is Wed 16 Sep 2026 | Timeline in §7 shifts |

**Gap analysis, Dev-Team → Stakeholder.**
*Carried over:* problem evidence, scope, success criteria, rollout, open questions.
*Added:* executive summary, cost of the status quo, business-impact model, deliverability/regulatory exposure, resource ask, explicit recommendation with alternatives.
*Removed:* R1–R6 requirement list, `digest_send_log` schema and table reads, HTML/plaintext rendering, batching mechanics. None of it is decidable by this audience.

I did **not** invent the numbers the source spec doesn't contain — user counts, ARPU, support cost per ticket, eng weeks, TAM. Those appear as `[NEEDS INPUT]`. A stakeholder doc with fabricated business math is worse than one with honest blanks, because the fabrication is what gets quoted afterwards.

---

# Weekly Project Digest
## Executive Review — Thursday 17 Sep 2026

**Owner:** Product · **Eng lead:** unassigned · **Status:** approved for build, pre-kickoff
**Decision requested today:** (1) confirm the engagement thesis is worth testing, (2) name an eng lead, (3) approve the deliverability guardrail in §5.

| Version | Date | What changed | Why |
|---|---|---|---|
| v2.0 | 16 Sep 2026 | Stakeholder cut of the Dev-Team PRD | Exec review; implementation detail replaced with impact, risk, and the ask |

---

### 1. Executive summary

Our highest-value cohort is our least engaged. Users who own three or more projects log in **2.1 times a week** — less than half the **4.4** of users with one or two projects. They also generate roughly **40 support tickets a month** that are all a version of *"I didn't know X changed."* The more someone commits to the product, the more they lose track of it.

We propose a weekly email that tells each user what actually moved across their projects — items added and completed, comments, new members — with one way back in per project. Four-week rollout: internal dogfood, 10%, then everyone.

The bet is that **visibility, not capability, is what's suppressing engagement in this cohort.** That bet is currently untested, which is why §8 recommends proceeding with a decision gate rather than a straight ship. One thing needs an explicit decision today: at our volume this becomes regulated bulk email, and mishandling it degrades deliverability for *every* email we send — password resets and invoices included — not just this one.

---

### 2. Problem and opportunity

**The problem, in business terms.** Commitment to the product is currently punished. A user with six projects has six times the surface area to track and no more ability to track it than a user with one. They fall behind, they stop checking, and the ones who do come back arrive through a support ticket rather than the product.

**What the status quo costs.**

| Cost | Evidence | Annualised |
|---|---|---|
| Support load | ~40 tickets/month, "I didn't know X changed" | ~480 tickets/yr × `[NEEDS INPUT: fully-loaded cost per ticket]` |
| Engagement gap | 2.1 vs 4.4 weekly logins | `[NEEDS INPUT: # of 3+ project owners]` × the retention delta below |
| Reputational | Unknown — no churn analysis links this cohort's login rate to cancellation | `[NEEDS INPUT: churn rate by project-count cohort]` |

**Read the engagement number carefully.** It points the opposite way from intuition — more projects should mean *more* engagement. Two explanations fit the same data, and they lead to different decisions:

- **Overload.** These users are drowning and disengaging. A digest helps, and the cohort is a retention risk. *This is the spec's implicit theory.*
- **Selection.** Multi-project owners are delegators and overseers who were never going to log in daily. 2.1 is their healthy baseline, not a symptom. A digest is a pleasant nicety with no retention effect.

Nothing in the current evidence base separates these. §8 proposes the cheapest way to find out.

**Why now.** `[NEEDS INPUT]` — the source spec doesn't state a trigger, and this is the first question a good exec asks. If the honest answer is "we had capacity," say that; it's defensible for a four-week build and indefensible for anything larger.

**Market context.** Deliberately omitted. This is a retention feature for existing users, not a market-entry bet — TAM/SAM/SOM would be theatre here. The one competitive fact that *would* matter is whether digests are table stakes in our category (I believe they are; `[NEEDS INPUT: competitive audit]` to state it as fact rather than impression). If they are table stakes, the framing shifts from "growth bet" to "closing a gap," and the bar for shipping drops.

---

### 3. Proposed solution

**The narrative.** *(Illustrative, not a researched persona.)* Maya runs four client projects. Monday 8am, before her first call, she gets one email: the API migration project has three items closed and two new comments on the spec she wrote; the onboarding revamp gained a member; the other two are quiet. Twenty seconds of reading tells her the one place she needs to be. She clicks through to the spec thread. Previously she'd have found that comment on Thursday, or in a support ticket asking why nobody told her.

**In scope.** Per-project deltas (items added, items completed, comments, membership changes), one call-to-action per project, Monday 08:00 in the user's local time, opt-out at both user and project level, and no email at all when nothing happened.

**Explicitly out, and why.**

| Out | Why |
|---|---|
| Real-time and daily digests | Defeats the purpose — the problem is noise, and more frequency recreates it |
| Slack delivery | Real demand, different build; revisit after the email thesis is proven |
| Mobile push | Same |

**Phasing.**

| Phase | What | Timing |
|---|---|---|
| 1 | Internal dogfood | Week 1 |
| 2 | 10% of 3+ project owners | Week 2 |
| 3 | Full rollout | Week 4 |

The gap between weeks 2 and 4 exists to read results. §8 proposes we actually use it as a gate.

---

### 4. Success metrics and business impact

| Metric | Target | How measured | What it tells us |
|---|---|---|---|
| **Weekly logins, 3+ project owners** | 2.1 → 2.8 in 8 weeks | Cohort analysis vs. holdout | **The only metric that matters.** Everything else is a health check |
| Open rate | ≥35% by week 4 | ESP | The email is wanted |
| Click-through | ≥8% | ESP | The content is useful, not just the subject line |
| Unsubscribe rate | <0.5% per send | ESP | We're not annoying people |
| **Spam complaint rate** | **<0.10%; never 0.30%** | ESP / postmaster tools | **Missing from the original spec.** See §5 |

**Two measurement problems worth an exec decision:**

1. **The primary metric can fake itself.** If a click from the digest counts as an active session, we will hit 2.8 logins by sending the email, regardless of whether anyone's behaviour changed. The number would go up and mean nothing. **Digest-originated sessions must be excluded from the success metric, and the comparison must be against a held-back control group.** The original spec listed this as an open question; at exec level it's a precondition.
2. **The target closes only about 30% of the gap** (0.7 of the 2.3-login difference). That's a reasonable ambition for one email — but if the board-level goal is "make multi-project owners as engaged as single-project owners," this feature is roughly a third of the answer and shouldn't be sold as the whole one.

**Business impact model.** Structure is real; the inputs are not ours to invent:

> Annual value ≈ `[# of 3+ project owners]` × `[retention lift, pp]` × `[ARPU]`
> plus `480 tickets/yr` × `[cost per ticket]` × `[% deflected]`

Whoever owns the revenue model should fill this before Thursday. If the top line can't clear a four-week build, that's a finding, not a failure — and it's better found now.

---

### 5. Deliverability and regulatory context — *the one item needing a decision*

A weekly email to the whole user base almost certainly puts us over **5,000 messages per day**, the threshold at which Google, Yahoo and Microsoft apply bulk-sender rules. These are enforced automatically, at the domain level.

| Requirement | What it means | Consequence of missing it |
|---|---|---|
| One-click unsubscribe (RFC 8058 headers, not just a footer link) | Machine-readable unsubscribe the mail client honours itself | Filtering and throttling by Gmail |
| Spam complaint rate below 0.10%, never 0.30% | Complaints, not unsubscribes — different number, different meaning | At 0.30% Gmail treats the sending domain as a spam source |
| SPF, DKIM and DMARC with domain alignment | Proof the mail is really from us | Since 5 May 2025 Microsoft **rejects** non-compliant bulk mail outright (`550 5.7.15`) — not junk-foldered, rejected |

**Why this belongs in front of an exec rather than in the engineering spec.** The blast radius isn't the digest. Domain reputation is shared: if this email tips us over a complaint threshold, the mail that gets throttled includes password resets, invoices, and security notifications. A retention feature would have created a support and trust incident.

Two concrete gaps in the current plan:

- The spec's guardrail is **unsubscribe rate <0.5%**. Mailbox providers police **spam complaint rate**, a different and much less forgiving metric. An unsubscribe is a user politely leaving; a complaint is a user telling Google we're a spammer. We are currently not tracking the one that can hurt us.
- The spec says "unsubscribe link in footer, one-click, no login required," which reads as satisfying the requirement but describes a *link*. The requirement is a *header*. Worth ten seconds of confirmation with the eng lead.

**Decision requested:** approve spam complaint rate as a hard rollout gate — if 10% exceeds 0.10%, we hold rather than expand. This costs nothing if we're right about the email being welcome.

---

### 6. Key risks and dependencies

| Risk / dependency | Impact | Mitigation / status |
|---|---|---|
| **Causality untested** — the login gap may be selection, not overload | The feature ships, metric doesn't move, 8 weeks gone | Holdout group from week 2; explicit read at the week-2 gate |
| **Domain reputation** (§5) | Company-wide email deliverability | Complaint-rate gate; verify RFC 8058 headers pre-launch |
| **Metric contamination** (§4) | We "succeed" without changing behaviour | Exclude digest-originated sessions; require control comparison |
| **Self-activity noise** — users whose only events are their own | Digest reads as a robot reciting your own week back to you; drives complaints | Product decision needed before build — see §9 |
| **No eng lead assigned** | Nothing starts | **Needs a name on Thursday** |
| Send-volume infrastructure at full rollout | Send spikes, throttling | Batched scheduling in the build plan; confirm ESP capacity `[NEEDS INPUT]` |

---

### 7. Resource ask and timeline

| | |
|---|---|
| Engineering | `[NEEDS INPUT: eng weeks]` — sized against a 4-week rollout |
| Design | Email template `[NEEDS INPUT]` |
| Analytics | Holdout cohort setup + week-2 read — **new**, not in the original plan |
| Dependencies | ESP configuration; DMARC/DKIM verification with whoever owns the sending domain |
| Start | Blocked on eng lead assignment |

Sizing is unfilled because the source spec doesn't contain it. It should be filled before the meeting rather than estimated live.

---

### 8. Recommendation

**Proceed to the 10% pilot with a genuine gate at week 2 — don't pre-approve full rollout.** The build is cheap, the problem is evidenced, and the category likely expects this feature. What isn't established is that a digest moves the login number, so buy that information for the cost of one extra analytics setup instead of assuming it.

Three changes to the approved plan: a holdout group, spam complaint rate as a hard gate, and digest-originated sessions excluded from the success metric. None of them change the build meaningfully; all three change whether we can believe the result.

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| **Pilot with a week-2 gate** | Cheap; tests the thesis before full exposure; contains deliverability risk | Two extra weeks to full rollout | **Recommended** |
| Ship straight to 100% | Fastest; simplest | Unbounded deliverability exposure; no way to attribute the result | Not recommended — speed buys nothing when the outcome is unmeasurable |
| In-app "what changed since you were here" instead | Zero deliverability risk; no consent burden | Only reaches users who already log in — the exact people who aren't the problem | Not recommended *as a replacement*; strong as a fast follow |
| Instrument first, build later | Cheapest way to test the causal claim | Burns weeks; the build is small enough that the pilot answers the same question while delivering value | Not recommended |

---

### 9. Open questions

**For this room, Thursday:**
1. Who is the eng lead?
2. Do we accept spam complaint rate as a hard rollout gate? *(Recommend yes.)*
3. Does the week-2 gate have teeth — can this be held, or is full rollout already committed?

**For Product, before build:**
4. What does a user see when their only activity is their own? Suppress, or show "you were the only one active"? *(Leaning suppress — a digest of your own actions is the fastest route to a spam complaint.)*

**For Analytics, before week 2:**
5. Holdout group construction and size.
6. Formal definition of "active session" excluding digest-originated traffic.

---

## Stress Test

**Weakest part of this document.** The business impact section is a shape with no numbers in it. Everything else here could be right and the doc still fails Thursday if someone asks "what's this worth?" and the answer is a formula. That is a genuine gap, and I'd rather name it than paper over it — but it needs filling before the meeting, not during.

**Assumptions most likely to be wrong.**
- *That this is a decision meeting.* If it's an FYI, §7 and §8 are noise and the doc should be one page.
- *That send volume crosses 5,000/day.* I inferred it from "weekly email to all users." If the user base is small, §5 is over-weighted — though the practices remain correct and the headers cost nothing.
- *That the login gap is the right problem at all.* I've flagged the selection-effect reading, but I've still organised the whole document around the spec's engagement thesis. A genuinely independent analysis might conclude the 40 support tickets are the real, measurable problem and the login number is a distraction — 480 tickets a year is a fact; the retention story is a hypothesis.

**What a sharp exec says in response.**
- *"You've turned an approved build into a pilot with conditions. Is this Product hedging?"* Fair challenge. The honest answer: the gate costs two weeks and buys the ability to know whether it worked. If the org's appetite is "ship it, it's an email, stop over-thinking" — that's a legitimate call, and the only non-negotiable is the deliverability guardrail, because that one has blast radius beyond the feature.
- *"A third of the gap is unambitious."* Correct. One email won't make a six-project owner behave like a one-project owner. If that's the actual goal, this is the first of several things, and the roadmap should say so rather than letting this feature absorb the expectation.
- *"Why is a PM telling me about DKIM?"* Because the failure mode is a company-wide email outage caused by a retention feature, and nobody else in the approval chain was looking at it.

**Where I'd push back on the original spec.** The `<0.5% unsubscribe rate` success criterion looks like a safety guardrail and isn't one — it monitors the polite exit while ignoring the complaint that actually triggers enforcement. That's the kind of gap that survives a dev review because it looks like it's already covered.

---

**Sources** (for the §5 claims — these are grounded, not recalled):
- [Google — Email sender guidelines](https://support.google.com/a/answer/81126) (5,000/day threshold, RFC 8058 one-click unsubscribe, 0.10% target / 0.30% hard limit, SPF/DKIM/DMARC alignment)
- [Microsoft — Strengthening the email ecosystem: Outlook's new requirements for high-volume senders](https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730) (enforcement from 5 May 2025, `550 5.7.15` rejection)
- [dmarcian — Microsoft enforces SPF, DKIM, DMARC](https://dmarcian.com/microsoft-enforces-spf-dkim-dmarc/) (corroborating)

*Note: Google's guidelines also specify a maximum time to process unsubscribe requests. I did not confirm the exact figure from the primary source, so I've left it out rather than state a number from memory — worth a check with the eng lead.*
