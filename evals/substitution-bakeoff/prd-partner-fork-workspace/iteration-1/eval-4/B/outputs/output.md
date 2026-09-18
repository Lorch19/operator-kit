# Document Auto-Summary in the Weekly Digest

**Skill:** `prd-partner` · **Mode:** PRD Mode → **Dev-Team** output
**Date:** 2026-09-16 · **Status:** Draft v1.0, unreviewed

---

## How I ran this (read once, then skip)

The request — *"Add a feature where we auto-summarise the user's uploaded documents with an LLM and surface the summary in the digest"* — is one sentence, and by `prd-partner`'s own mode-detection rules it is **fuzzy**, which routes to Discovery Mode. Discovery Mode is defined as a live `grilling` session: one question at a time, waiting for each answer. That is impossible unattended.

So I did the next-best faithful thing rather than skipping the step: I ran a **written discovery pass** — the problem fork, the architecture tradeoff, the assumption register, and the Synthesis Checkpoint in the skill's own format — and then generated the PRD against those stated assumptions. Sections 1–4 are that discovery pass. Section 5 onward is the PRD proper.

**Why Dev-Team and not AI-Build or Stakeholder:** no audience was named. AI-Build demands a stack, data model, auth model and design direction; with zero repo context I would be *inventing* those, which the skill forbids. Stakeholder mode demands business impact and a resource ask, which I would also be inventing. Dev-Team is the mode I can fill with real content and no fabrication. Converting Dev-Team → AI-Build later costs one pass and is listed in the skill's conversion table.

---

## 1. Read this first: the request is a solution, not a problem

`prd-partner` says to push back when a problem is stated as a solution. This one is — twice over. It names a mechanism ("summarise with an LLM") and a surface ("in the digest") without naming what is broken. Three different problems produce this same sentence, and they do **not** converge on the same v1:

| # | Underlying problem | What v1 should then be | Primary metric |
|---|---|---|---|
| **A** | The digest reports *that* things changed but not *what* changed, so recipients skim and bounce. | Make the digest's document rows self-explanatory. Summary is one of several fixes (others: better diffs, better subject lines, activity grouping). | Action taken after digest |
| **B** | Uploaded documents go unread; knowledge sits idle in projects. | Document discovery. The digest is one surface and probably the *weakest* one — in-app preview-on-hover and search would beat a weekly email. | Documents read per upload |
| **C** | Competitors ship AI summaries; we need an AI story. | A visible, brandable AI surface. Design optimises for perception and demo-ability, not for weekly utility. | Perception / win-rate in deals |

**I am proceeding on Problem A**, because the request explicitly anchors the value to the digest ("surface the summary in the digest"). If the real driver is B, this PRD builds the right pipeline on the wrong surface — the summarisation half survives, the digest half is wasted. If it is C, the whole measurement plan in §8 is wrong and should be replaced.

**This is the single highest-leverage thing to correct before any engineer starts.** It costs one sentence from whoever asked.

### The core insight that shapes everything below

Document summarisation is commoditised. Every document tool ships it; a competent implementation is a weekend of work, and the model does the hard part.

**The hard part is selection, not summarisation** — deciding which three to five documents out of this week's twelve matter *to this particular recipient*, and leaving the rest out. A digest that pastes forty summaries into an email is strictly worse than today's digest. So the ranking-and-capping requirement (§9-D1) is P0, not polish, and it is where the product differentiation actually lives.

---

## 2. Assumption register

Every assumption I am building on, and what breaks if it is wrong. These are assumptions, not findings.

| # | Assumption | Why | If wrong |
|---|---|---|---|
| 1 | The digest is a weekly email, per-recipient, summarising changes in projects that recipient belongs to. | Given in the brief. | — |
| 2 | Documents are uploaded into projects and carry per-document or per-project access control. | Standard for any multi-user project tool. | If documents are world-readable within a workspace, §10-C1 (render-time ACL check) simplifies to nothing — but verify, don't assume. |
| 3 | The product is multi-tenant B2B SaaS with at least some EU customers. | "Projects" + "digest" + "uploaded documents" is a team-collaboration shape. | If single-tenant or consumer-only, the sub-processor and admin-toggle requirements (§9-C) shrink sharply. |
| 4 | No LLM vendor is in production yet for this product. | Nothing in the brief suggests one. | If one is already a named sub-processor with a signed DPA, §9-C5 and the 30-day notice dependency largely disappear — the biggest schedule risk goes away. |
| 5 | There is no existing text-extraction pipeline (PDF/DOCX → text). | Not mentioned. | If one exists, cut ~40% of pipeline build. If not, this is the real engineering cost — extraction is messier than the LLM call. |
| 6 | Digest send is a batch job; there is a feature-flag system capable of tenant-level holdouts. | Standard. | If no flagging exists, §9-E1/E2 become dependencies, not requirements, and the measurement plan is not executable. |
| 7 | Upload volume per tenant per week is in the single-to-low-double digits, with a long tail of automated bulk uploaders. | The shape of every file-upload product I have seen. | The cost model (§11-R1) is entirely driven by this. If a tenant syncs a Drive folder of 10,000 files, per-document summarisation at ingest is financially unviable without the caps in §9-A8. |

Nothing in this document contains an invented baseline, market size, price, or conversion rate. Where a number is needed and I do not have it, it is marked **[NEEDS INPUT]**.

---

## 3. Architecture decision: where does summarisation happen?

The skill says to evaluate alternatives before committing when the idea involves system design. This one does, and the choice is load-bearing — it determines cost profile, failure behaviour, and whether the summary is reusable beyond the digest.

| Approach | Risk | Complexity | Time to value | Extensibility | Waste if we pivot |
|---|---|---|---|---|---|
| **1. Summarise at digest-send time**, per document, inline in the batch job | **High** — the whole tenant base summarises in one Sunday-night window; one vendor outage kills the week's digest entirely | Low | Fastest | **Poor** — summary exists only inside the email | High — nothing survives a surface pivot |
| **2. Summarise at digest-send time, at digest level** (one synthesis across the week's documents) | High — same spike, plus attribution is hard ("which doc said that?") and the output is hard to test | High | Slow | Poor | High |
| **3. ✅ Summarise at ingest time**, store per document version; digest renders the top N | Low — failures surface days before send, retryable; spend spread across the week | Medium | Medium | **Strong** — same summary powers search, hover-preview, document list, in-app feed | **Low** — the asset survives even if the digest idea dies |
| **4. Summarise lazily on first read** | Medium — introduces latency into a read path that is currently fast | Medium | Medium | Medium | Medium |

**Chosen: Approach 3 — summarise at ingest, render at digest.** Four reasons, in order of weight:

1. **The summary becomes a reusable asset.** The digest is its first consumer, not its only one. If Problem B (§1) turns out to be the real problem, the work is already done.
2. **Failures become visible and fixable before the email goes out.** In Approach 1, a vendor outage on Sunday means a broken digest with no recovery window. In Approach 3, a failure on Tuesday gets retried on Wednesday.
3. **Cost and rate-limit pressure spread across the week** instead of every tenant hitting the vendor in the same hour.
4. **Idempotency is natural.** One summary per document version, keyed by content hash — no duplicate spend, no non-deterministic drift between two renderings of the same document.

The cost of Approach 3: we pay to summarise documents that never appear in any digest. Given §2-7, that is acceptable and bounded by the caps in §9-A8. **Record this as decided** — it is the kind of thing an engineer will otherwise "simplify" back into Approach 1.

Digest-level synthesis (Approach 2) is a real v1.1 idea layered *on top of* stored per-document summaries. It is not a v1.

---

## 4. Synthesis Checkpoint

> **Problem:** The weekly digest reports that documents changed but not what they say, so recipients cannot tell whether any of it needs them.
> **User:** A project member who reads the digest on a phone, on a Sunday evening, with thirty seconds of attention.
> **Core insight:** Summarising is commoditised; *choosing which three documents matter to this recipient* is the product.
> **Scope boundaries:** Text-bearing documents only, summarised at ingest, ranked and capped at five per digest, plain-text output, additive to today's digest and independently kill-switchable.
> **Riskiest assumption:** That the digest — a weekly, one-way email — is the right surface at all (see §1, Problem B).
>
> **PRD readiness: 5/10.** The mechanism, safety model and edge cases are solid and buildable as written. The *justification* is not: there is no evidence of user pain, no baseline for any metric, and the underlying problem was chosen by me rather than stated. That is a 5, and it should stay a 5 until someone answers §13-Q1.
>
> **Risks:**
> 1. **Wrong problem** (§1) — *blocks PRD.* One sentence from the requester resolves it.
> 2. **Untrusted content reaching an LLM whose output is emailed from our domain** — *resolvable during build*, but only if §9-B is treated as P0. This is the failure mode most likely to become an incident.
> 3. **Cost scales with upload volume, not with seats** — *resolvable during build* via §9-A8.
> 4. **New AI sub-processor triggers enterprise procurement friction and a contractual notice window** — *blocks launch, not build.* Start the clock now (§11-D1).
> 5. **No baseline means no way to tell if it worked** — *resolvable*, but only with a holdout (§9-E1). Without one, seasonal email drift will be read as a win.

---
---

# PRD — Dev-Team Mode

## 5. Context

**TL;DR.** The weekly digest currently tells recipients *that* documents were added; it does not tell them what is in those documents, so a row like "4 documents added" carries almost no decision value. We will generate a short summary for each text-bearing document at upload time, and render the three-to-five most relevant ones in each recipient's digest, ranked per recipient and access-checked at send.

**Why now.** Weak — and this should be said plainly. The honest "why now" is that document summarisation has become cheap and reliable enough to be table stakes, not that we have evidence this specific pain is costing us specific users. **[NEEDS INPUT: is there a digest engagement decline, a support theme, a churn signal, or a lost deal behind this request?]** If the answer is "we have capacity and AI is available," the skill's own guidance is to push back, and I am pushing back.

**Market & competitive context.** TAM/SAM/SOM omitted deliberately — I have no revenue, pricing or market data for this product, and inventing three numbers to fill a table would be worse than an empty one.

Competitive context does shape requirements, so:

| Competitor class | How they handle this | Gap / our angle |
|---|---|---|
| All-in-one workspaces (Notion, Coda) | AI summarisation of a page, invoked in-app by the user, on demand | Pull, not push. The user must already be looking at the document — which is exactly the moment our user is *not* in. |
| Chat platforms (Slack, Teams) | AI recaps of channels and threads on a schedule | Closest analogue, and the one to learn from: their hard-won lesson is that recap quality collapses without aggressive relevance filtering. Confirms §1's core insight. |
| Cloud storage (Google Drive/Gemini, Dropbox Dash) | Per-file summary in the file browser and in search | Same pull-shaped pattern; strong at file-level, absent at "what changed this week." |

The read: **per-document summarisation is table stakes and not defensible.** Per-recipient selection inside a change digest is the part nobody has made good. Build accordingly — spend the engineering on ranking, not on prompt tuning.

**The narrative.**

> Maya runs ops at a 30-person logistics company. Sunday, 8pm, on her phone. The digest for *Q4 Carrier Renegotiation* says "4 documents added." She has no idea whether any of them need her before Monday's 9am call, and she is not going to open four PDFs on a phone, so she archives the email and finds out at 9:04am that the Nordic Freight counter-offer landed on Thursday.
>
> With this feature, the same email says: **"Nordic Freight — counter-offer. 6% increase over 18 months; rejects our volume-tier request; response requested by Sept 22."** Maya taps through, reads the actual document for four minutes, and walks into Monday having already decided.

The value is delivered in the moment she decides whether to tap. That is a one-line, thirty-word job — which is why the output contract in §9-A7 is deliberately tight.

**Success metrics.**

| Type | Metric | Definition | Target |
|---|---|---|---|
| **Primary** | Post-digest action rate | % of digest recipients who take any in-app action within 48h of send, treatment vs. holdout | **[NEEDS INPUT: baseline]** — ship gate is a pre-registered relative lift over holdout, agreed *before* the test starts |
| Secondary | Document open rate from digest | Unique doc opens attributed to digest links / recipients | Directional only — see note |
| **Quality gate** | Materially-misleading rate | Weekly human audit, n=100 sampled summaries, rated accurate / minor error / materially misleading | Proposed: **≤2% materially misleading**, sustained, or roll back. *Threshold is my proposal and needs sign-off.* |
| Guardrail | Digest open rate | Must not decline vs. holdout | No statistically significant decline |
| Guardrail | Unsubscribe + spam-complaint rate | Per send | No increase vs. holdout |
| Guardrail | LLM cost per active tenant per week | Vendor spend / tenants with ≥1 upload | **[NEEDS INPUT: acceptable ceiling]** — circuit breaker wired to it (§9-A8) |
| Guardrail | Summary report rate | "This summary is wrong" clicks / summaries rendered | Trend watch; spike = investigate, not auto-rollback |

*Note on the secondary metric:* document opens is a **flawed** success signal and should not be a gate. A genuinely good summary may *reduce* opens, because the reader got what they needed from the email. Reading a drop in opens as failure would kill a working feature.

**Explicitly rejected as vanity metrics:** number of summaries generated, % of documents summarised, "AI feature adoption." All three go up if we ship something useless, and up further if we ship something harmful. They measure our activity, not the user's outcome.

---

## 6. Personas

| Persona | Description | What they need from this |
|---|---|---|
| **Digest recipient** (primary) | Project member, reads the digest on mobile, thirty seconds of attention, low tolerance for noise | Enough signal to decide "does this need me before Monday?" — and not one line more |
| **Document owner** | The person who uploaded the file, often mid-draft | Confidence that a half-finished draft is not being broadcast, and a way to say "that summary is wrong" |
| **Workspace admin** | Buyer or IT owner; answers to security review | Control over whether we process their documents with a third-party model at all, and separately over whether content leaves the app in email |

Merged: support/CS is not a persona here, but is a stakeholder in §13.

**User stories.**

- As a **digest recipient**, I want each document row to tell me what the document actually says, so that I can decide in seconds whether to open it.
- As a **digest recipient**, I want no more than a handful of summaries, so that the email stays readable in a week with heavy uploads.
- As a **document owner**, I want to know a summary will be generated and shown, so that I am not surprised by a draft being characterised to my team.
- As a **document owner**, I want to flag a wrong summary in one tap, so that I do not have to email support about it.
- As a **workspace admin**, I want to turn off third-party AI processing entirely, so that I can answer my security questionnaire honestly.
- As a **workspace admin**, I want to allow summarisation but keep summary text out of outbound email, so that confidential content stays inside the access-controlled app.

---

## 7. Scope

**Goals**
- Generate a short, structured summary for each text-bearing document at upload time, stored per document version.
- Render a ranked, capped set of those summaries in each recipient's weekly digest, gated by that recipient's current access.
- Keep the feature strictly additive: if any part of it fails, the recipient gets today's digest, not an error.
- Give admins real control over third-party processing and over content leaving the app.

**Non-goals (v1)** — each with the reason, so nobody re-litigates them mid-build:
- **Digest-level synthesis across documents** ("three contracts landed, all renewing in Q1"). Better product; much harder to attribute and test. v1.1, built on top of v1's stored summaries.
- **Spreadsheets, slide decks, images, audio, video, archives.** Spreadsheets in particular summarise badly and confidently — a wrong summary of a financial model is the worst failure mode available to us.
- **OCR for scanned documents.** Adds a second vendor, a second cost line and a second accuracy problem. v1.1.
- **Q&A / chat over documents.** Different product.
- **Translation.** v1 summarises in the document's own language. See §13-Q4.
- **User-configurable summary length, tone or prompt.** Every configurable surface is a surface we must test and defend against injection.
- **Retroactive summarisation of the existing document backlog.** Unbounded cost against documents nobody is currently asking about. Ingest-forward only; backfill is a separate, costed decision.

---

## 8. Domain & regulatory context

Specific to this feature. Generic compliance boilerplate omitted.

| Area | Requirement / best practice | Impact on this feature |
|---|---|---|
| **GDPR Art. 28(2) — sub-processors** | A processor must give controllers prior notice of intended sub-processor changes, with a right to object. Standard practice is general written authorisation + a public sub-processor list + ~30 days' notice. | Adding an LLM vendor **is** adding a sub-processor. The notice window is a hard gate on *launch date*, not on build. Start it now. Enterprise customers may object — hence the default-off recommendation in §9-C3. |
| **GDPR Art. 5 — purpose limitation & minimisation** | Documents were uploaded for storage and collaboration; summarisation is a new processing purpose. | Needs an admin-level control and an in-product notice, not a silent rollout. Minimisation also argues for the truncation policy (§9-A4) — send the model less text, not more. |
| **GDPR Art. 17 / Art. 20 — erasure & portability** | Summaries are derived personal data. | Deletion of a document must cascade to its summaries within the standard deletion SLA; summaries must appear in data exports. §9-C2. |
| **GDPR Art. 9 — special categories** | Tenants will upload HR files, medical notes, legal correspondence. We do not know which. | Per-folder exclusion (P1) and a working admin kill switch (P0) are the only honest answers at our layer. |
| **International transfers** | If the inference endpoint sits outside the EEA, a transfer mechanism is required. | Prefer an EU-resident inference endpoint for EU tenants. Cheaper to choose at vendor-selection time than to retrofit. §9-C5. |
| **Vendor terms** | Zero data retention, no training on our data, contractually. | This is the first question in every security review. Make it a vendor-selection gate, not a negotiation. §9-C5. |
| **EU AI Act Art. 50 — transparency** | In force since **2 Aug 2026**. Art. 50(2) machine-readable marking of synthetic output binds **providers** of the generative system, not us as deployer. Art. 50(4) deployer labelling binds only text *published to inform the public on matters of public interest*. | **A private weekly work digest does not trigger Art. 50(4).** We should label summaries as AI-generated anyway (§9-D2) — for trust and for the reader's calibration, not because the AI Act compels it here. Saying this precisely matters: overstating the obligation invites the wrong design. |
| **OWASP Top 10 for LLM Applications (2025)** | LLM01 Prompt Injection (incl. indirect), LLM02 Sensitive Information Disclosure, LLM05 Improper Output Handling, LLM10 Unbounded Consumption. | All four apply directly. Uploaded documents are attacker-controllable input, and our output lands in an email from our sending domain. §9-B is written against these. |
| **Indirect prompt injection — established mitigations** | Defence in depth: sanitise before the context window (strip HTML/CSS/JS, zero-width and bidi characters, document metadata); "spotlighting" via randomised delimiters marking untrusted regions; restrict ingestible formats; filter output. Demonstrated attacks exist where hidden text in a Word document manipulates a summarising assistant. | Directly implemented as §9-B1 through B4. |

---

## 9. Requirements

Grouped by area. P0 = v1 cannot ship without it.

### A. Summarisation pipeline

- **P0-A1** Summarisation runs asynchronously on document ingest (upload and new-version events), never on the digest-send path. *(Decided in §3.)*
- **P0-A2** Idempotency key = `(tenant_id, document_id, version_id, content_hash, prompt_version, model_id)`. Re-summarise only when that tuple changes. Prevents duplicate spend and prevents two renderings of the same document disagreeing.
- **P0-A3** MIME allowlist. **In:** PDF with an extractable text layer, DOCX, TXT, MD, RTF, and native-editor documents. **Out:** everything else, silently (no summary, no error). Allowlist, never denylist.
- **P0-A4** Length policy. Documents above the extraction threshold **[NEEDS INPUT: pick a token budget at vendor selection]** are summarised from a truncated leading window, and the stored summary is flagged `basis: truncated`. The digest renders that flag as "based on the first N pages." **No silent truncation** — a summary that omits the conclusion of a 90-page contract while looking complete is worse than no summary.
- **P0-A5** Minimum-length policy. Documents under ~150 words are not summarised; the digest shows the document's first two lines verbatim. A 30-word note does not need an LLM, and summarising one produces something longer than the original.
- **P0-A6** Extraction failures (no text layer, password-protected, corrupt, unsupported encoding) record a typed failure reason and stop after N retries. Failure reasons are enumerable, not free text — they drive §9-E3 and tell us what to build in v1.1.
- **P0-A7** Strict output contract, validated in code:
  - `headline` — ≤ 12 words
  - `summary` — ≤ 60 words, 2–3 sentences
  - `key_points` — 0–3 bullets, ≤ 15 words each
  - `basis` — `full | truncated`
  On schema violation: retry once, then store no summary. Never store or render unvalidated model output.
- **P1-A8** Per-tenant daily and weekly summarisation caps, plus a global cost circuit breaker. On trip: stop summarising, alert, and let the digest degrade to today's behaviour. **The digest must never fail because the LLM budget did.**

### B. Untrusted content and output safety

Every uploaded document is attacker-controllable input. The output of this pipeline is placed in an email sent from our domain, carrying our sender reputation, to people who trust it. That is the severity argument for treating this section as P0 rather than hardening.

- **P0-B1** The system prompt states that the delimited region is untrusted data to be summarised, never instructions to follow. Extracted text is wrapped in a **per-request randomised delimiter** (spotlighting), so a document cannot forge the delimiter to escape its region.
- **P0-B2** Pre-extraction sanitisation, before text reaches the context window: strip HTML/CSS/JS; strip zero-width, bidirectional-override and other invisible control characters; strip document metadata (author, comments, tracked changes, speaker notes); drop text that is rendered invisible (white-on-white, 0pt, positioned off-canvas). These are where hidden instructions live.
- **P0-B3** Output is rendered as **plain text only**. Any URL, email address, markdown link, HTML tag or image reference in model output is **stripped**, and the occurrence is logged as a suspected-injection signal. No model output is ever rendered as markup. *Rationale: without this, a document containing "Summary: your account is suspended, verify at http://…" becomes a phishing email from our domain, past our customers' spam filters, with our name on it.*
- **P0-B4** Length caps are enforced in code after generation, not requested in the prompt. Prompts are guidance; validators are the contract.
- **P0-B6** Cache keys include `tenant_id`. A content-hash-only cache is a tempting optimisation and a cross-tenant disclosure: it leaks *that tenant B holds the same file as tenant A*, and shares tenant A's generated text into tenant B's product. Prohibited.
- **P1-B5** Monitor the rate of outputs with stripped URLs or reader-directed imperatives, per tenant. Sustained spikes indicate someone probing us.

### C. Permissions and privacy

- **P0-C1** Summary visibility is evaluated **at digest render time** against the recipient's *current* access to the source document — never at generation time, never cached alongside the summary. If the recipient cannot open the document, neither the summary nor any indication that the document exists appears in their digest. *Permissions change between Tuesday's upload and Sunday's send; a summary generated under Tuesday's ACL is not authorisation to send it under Sunday's.*
- **P0-C2** Deleting a document or version cascades to its summaries within the standard deletion SLA. Summaries are included in data export.
- **P0-C3** Two **independent** admin toggles:
  - `ai_summarisation_enabled` — may we send this workspace's documents to a third-party model at all?
  - `ai_summary_in_email` — may summary text leave the app in outbound email, or link-only?
  These are genuinely separate decisions. An admin can reasonably accept in-app AI processing and still refuse to have document content sitting in employees' inboxes, forwardable, in mail backups, outside the audit log. Collapsing them into one switch forces an all-or-nothing that loses the second group.
  Default for existing tenants: **[NEEDS INPUT — legal + commercial call.]** My recommendation: **off** for enterprise-tier tenants until the sub-processor notice window has run; **on with prominent in-product notice** for self-serve.
- **P0-C5** Vendor selection gates: contractual zero-retention, no training on customer data, and an EU-resident inference option.
- **P1-C4** Per-folder / per-label exclusion, for HR, legal and finance areas.

### D. Digest rendering

- **P0-D1 (the differentiating requirement)** The summaries section is **ranked and capped at five documents**, ranked per recipient. v1 ranking signal, kept deliberately simple and explainable: recency × the recipient's relationship to the document (uploaded by someone they work with / in a project they are active in / they are named in the document's sharing). Overflow renders as "+7 more documents" linking to a filtered list. *A forty-summary email is worse than today's digest. The cap is the feature.*
- **P0-D2** Every summary is labelled as AI-generated, with one line of standing caveat ("summaries can be wrong — open the document to check") and a one-tap "this is wrong" affordance that links to a short web form. Not a reply-to-email mechanism.
- **P0-D3** Graceful degradation per row. If a document has no summary — failed, excluded, too short, unsupported type, admin-disabled, budget-tripped — the digest renders that row exactly as it does today. The absence of a summary is never a visible error.
- **P0-D4** Zero summarisable documents that week → the section is omitted entirely. No "no documents this week" empty state; the digest is already long enough.
- **P0-D6** **No summary text in the subject line or the email preview text.** Preview text renders in inbox lists, on lock screens and on smartwatches — visible to anyone near the device, and in contexts the recipient did not choose. Leaking a confidential document's content there is a materially larger exposure than leaking it inside the body, which at least requires opening the mail.
- **P1-D5** The `text/plain` MIME part carries the same content as the HTML part.

### E. Observability and rollout

- **P0-E1** **Tenant-level holdout**, 10% minimum, held for at least four weekly sends. Tenant-level rather than recipient-level so that colleagues do not receive visibly different digests and compare them.
- **P0-E2** Kill switch that reverts every tenant to the current digest without a deploy, testable in staging before launch.
- **P0-E3** Per-summary telemetry: model, prompt version, input/output tokens, latency, cost, failure reason, `basis`, injection-signal flags. **Source document text must not be written to logs** beyond a short, access-controlled debug window — the pipeline's most likely accidental privacy hole is its own debug logging.

---

## 10. Dependencies

| Dependency | Owner | Impact |
|---|---|---|
| **D1.** LLM vendor selection + DPA / zero-retention / EU endpoint | Legal + Eng | Gates launch. Start immediately — see D2. |
| **D2.** Sub-processor notice to customers, ~30-day window + objection handling | Legal + CS | **Gates launch date, not build.** This runs in parallel with development or it becomes the critical path by default. |
| **D3.** Text extraction for PDF/DOCX (build or buy) | Eng | Likely the largest engineering item, and the one most often underestimated. See §2-5. |
| **D4.** Digest template + rendering changes, including plain-text part | Eng | Moderate. |
| **D5.** Feature flag + tenant-level holdout capability | Eng | Gates the measurement plan (§9-E1). If absent, we cannot know if this worked. |
| **D6.** Admin settings surface for the two toggles | Eng + Design | Gates §9-C3. |
| **D7.** Weekly human summary audit — who does it, on what sample | Product + CS | Gates the quality metric. Unowned, this quietly stops happening in week 3. |

## 11. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| **R1. Cost scales with upload volume, not with seats.** One tenant syncing a bulk folder can dominate total spend. | High, financial | Per-tenant caps + global circuit breaker (§9-A8); exclude bulk/automated upload sources from v1; publish cost per tenant weekly from day one. |
| **R2. Indirect prompt injection turns our digest into a phishing vector** from our own sending domain. | High, security + brand | §9-B1–B4 as P0, not as hardening. Red-team with hostile documents before launch, not after. |
| **R3. A confidently wrong summary of something consequential** — a contract term, an incident report, a legal notice. | High, trust | The summary never replaces the document link; explicit AI labelling and caveat (§9-D2); `basis: truncated` disclosure (§9-A4); weekly audit with a rollback threshold. |
| **R4. New AI sub-processor triggers enterprise procurement friction or objection.** | Medium-high, commercial | Default-off for enterprise pending notice (§9-C3); the two-toggle model gives objecting admins a middle option instead of a "no". |
| **R5. Measurement fails and we cannot tell whether it worked.** Email engagement drifts seasonally; a before/after read will show a "win" either way. | Medium, strategic | Holdout (§9-E1) and a pre-registered ship threshold agreed before the first send. |
| **R6. We built the right pipeline on the wrong surface** (§1, Problem B). | Medium | Approach 3 (§3) is the hedge: summaries are stored as first-class data, so a pivot to in-app discovery loses the digest work only, not the pipeline. |

---

## 12. Edge cases

Non-obvious scenarios only. Obvious ones are omitted per the skill's guidance.

| Scenario | Behaviour |
|---|---|
| Scanned PDF with no text layer | Typed failure `no_text_layer`. No summary, row renders as today. Counted — it sizes the v1.1 OCR decision. |
| Password-protected or encrypted file | Typed failure `encrypted`. Never attempt to crack or prompt for a password. |
| 500-page document | Truncated window, `basis: truncated`, digest says "based on the first N pages." |
| 40-word meeting note | Not summarised; first two lines shown verbatim (§9-A5). |
| Document uploaded, then replaced twice in the same week | Summarise each version; the digest renders **only the latest**, with "updated 3 times this week." Never three rows for one document. |
| Document deleted after summary generation, before digest send | Suppressed at render; summary cascade-deleted (§9-C2). |
| Recipient's access revoked between upload and send | Suppressed — render-time ACL check (§9-C1). |
| Recipient's access *granted* between upload and send | Included. Same check, same direction. |
| Document in a language the recipient does not read | v1: summarise in the document's language. Known gap — §13-Q4. |
| Model returns a refusal, an empty response, or fails validation twice | No summary stored. Row renders as today. **A refusal string must never appear in an email.** |
| 40 documents uploaded in one week | Top 5 ranked and rendered; "+35 more" links to the filtered list (§9-D1). |
| Document contains hidden text instructing the summariser | Sanitised pre-extraction (§9-B2); any surviving URL/imperative stripped from output (§9-B3); occurrence logged and counted (§9-B5). |
| Tenant disables `ai_summarisation_enabled` after summaries exist | Stop generating; stop rendering immediately. **[NEEDS INPUT: does disabling also delete existing summaries? My recommendation: yes — an admin turning this off means "you do not hold this."]** |
| Two tenants upload byte-identical files | Two independent summaries, two cache entries (§9-B6). Deliberate; do not "optimise." |
| Summary generation succeeds but costs 40× the median (pathological document) | Cap enforced at request level; over-cap documents are skipped and logged, not retried. |

---

## 13. Open questions

**For the requester / Product** *(Q1 is the one that matters)*
- **Q1.** Which problem is this solving — A, B or C in §1? **This changes v1.** Everything else here is downstream of the answer.
- **Q2.** What is the current digest engagement baseline, and what lift would make this worth the ongoing cost? Needed before the first send, not after.
- **Q3.** Should the v1 ranking signal be different from the recency × relationship heuristic in §9-D1? This is the differentiating requirement and it is the one I had least basis to specify.
- **Q4.** Cross-language: summarise in the document's language, or the recipient's? v1 assumes the document's.

**For Legal / Privacy**
- **Q5.** Default state of `ai_summarisation_enabled` for existing tenants, by tier. My recommendation is in §9-C3; the call is not mine.
- **Q6.** Does our current DPA's general authorisation cover adding this sub-processor with notice, or do enterprise contracts require affirmative consent?
- **Q7.** Does disabling summarisation require deleting existing summaries?

**For Engineering**
- **Q8.** Does a text-extraction pipeline already exist (§2-5)? This is the largest single unknown in the estimate.
- **Q9.** Does tenant-level feature flagging with a stable holdout exist (§2-6)? Without it, §9-E1 is a dependency, not a requirement.

**For CS / Support**
- **Q10.** Who owns the weekly summary audit (D7), and what is the escalation path when a customer reports a materially wrong summary?

---

## 14. Tentative roadmap

| Phase | What | Why |
|---|---|---|
| **v1** | Ingest-time summarisation for text-bearing documents; ranked, capped, access-checked rendering in the digest; two admin toggles; holdout + kill switch | Prove that a summary in the digest changes what recipients do, without betting the digest on it |
| **v1.1** | Digest-level synthesis across the week's documents ("three carrier contracts landed, all renewing in Q1") | Strictly better reading experience; needs v1's stored summaries and a working accuracy baseline first |
| **v1.1** | Reuse summaries in-app: document list, hover preview, search result snippets | The asset already exists; near-zero marginal cost; directly tests Problem B |
| **v1.2** | OCR for scanned documents; per-folder exclusions; recipient-language summaries | Sized by v1's failure-reason telemetry — build what actually failed, not what we guessed would |
| **Later** | Personalised ranking learned from click behaviour; spreadsheet and deck handling; per-recipient "why you are seeing this" | Only once selection quality is measurable |

**Backlog items generated by this PRD:** retroactive backfill decision (costed separately); bulk/automated upload source detection; the digest's plain-text parity gap if D5 is deferred; red-team corpus of hostile documents as a reusable test asset.

---

## 15. Stress test

*What is weakest here, and what a smart critic would say.*

1. **The whole document rests on an assumption I made, not a fact I was given.** §1 picks Problem A. If the requester meant B or C, this PRD is a well-built answer to a question nobody asked. The readiness score of 5/10 reflects exactly this, and no amount of detail in §9 fixes it. The strongest critique of this document is that it is too specific for how little it knows.

2. **"Selection is the product" is an argument, not a finding.** I reasoned it from the shape of the competitive landscape and from the failure mode of chat recaps. It is not validated. If recipients only ever have two or three documents a week, the cap in §9-D1 never binds, and the requirement I called the differentiator is dead weight — the feature reduces to commodity summarisation, and the competitive case in §5 evaporates. **The cheapest possible test: query the current distribution of documents-per-project-per-week before writing any code.** If the p90 is 3, cut §9-D1 to a simple recency sort and ship in a fraction of the time.

3. **The safety section may be over-engineered for the actual threat.** If the product is used exclusively by small internal teams uploading their own documents, indirect prompt injection requires an attacker who already has upload access to your workspace — and such an attacker has better options than a digest email. The counter, which I find more persuasive: the mitigations in §9-B are cheap and static, the blast radius if wrong is a phishing email carrying our sending domain to our customers, and any product with external sharing or email-to-upload has a genuinely untrusted input path. I would not cut them, but a critic arguing "you have priced this risk at enterprise levels for an SMB product" is not being unreasonable.

4. **The primary metric is soft, and I said so but did not solve it.** "Post-digest action within 48h" is attribution-fragile — someone who would have opened the app on Monday regardless gets counted. The holdout is what makes it interpretable, which means the measurement plan is entirely dependent on D5 existing. If it does not, we ship blind, and every number in §5 becomes decoration.

5. **Ingest-time summarisation (§3) pays for documents nobody reads.** In a product where 80% of uploads are never opened by anyone, Approach 1 — summarise only the handful that reach a digest — is genuinely cheaper, and my "reusable asset" argument is a bet on a v1.1 that may never ship. I stand by Approach 3 on operational grounds (failure recovery window, no Sunday-night spike), but the cost argument against it is real, and §2-7 is the assumption holding it up.

6. **Nothing here is validated with a user.** No quotes, no support tickets, no usage data. The honest status of this document is *a well-specified hypothesis*, and it should be labelled that way in any room it enters.

---

## 16. Skill improvement notes (`prd-partner` closing hook)

The skill's closing hook asks me to surface improvements and ask whether to apply them. I cannot ask, so here is the list — nothing applied.

1. **No unattended path.** A one-line, solution-shaped request correctly routes to Discovery Mode, but Discovery Mode is defined *only* as a live grilling session. When conversation is impossible, the skill offers nothing and the natural failure is to silently skip discovery and emit a confident PRD. **Suggest:** add a "Written Discovery" fallback — candidate-problem fork, assumption register, Synthesis Checkpoint, readiness score capped at 6/10 when no human confirmed the problem.
2. **Mode Detection has no defaults.** All three questions assume an answer arrives. **Suggest:** "If unanswerable: default to Dev-Team, state the inference, and note the conversion cost." AI-Build in particular is unsafe as an unattended default — it demands a stack and data model that must then be invented, which the skill elsewhere forbids.
3. **The ADR block exists only in AI-Build mode**, yet Discovery Mode instructs evaluating architecture alternatives for any system-design idea. In Dev-Team mode the resulting tradeoff table has nowhere to live, so it gets dropped — and the anti-regression value ("stops the builder improving back toward the rejected approach") applies just as much to a human engineer. **Suggest:** make the ADR block available in Dev-Team mode.
4. **"Don't invent metrics" collides with the Success Metrics table's mandatory Target column.** The resolution I used — express the target as a pre-registered decision rule against a holdout — is better than both inventing a number and leaving the column blank. **Suggest:** write that resolution into the skill.
5. **Industry Best Practices triggers on regulated domains, but the highest-value material in this run was security.** "Untrusted user content enters an LLM whose output reaches other users" is not in the trigger list, and it produced the sharpest requirements in the document. **Suggest:** add that trigger, pointing at the OWASP LLM Top 10.
6. **No guidance on rejecting vanity metrics visibly.** The skill says push back on them in Discovery; it does not suggest listing the rejected ones in the PRD. Naming them ("we are deliberately not counting summaries generated, and here is why") is cheap and prevents them reappearing in the first dashboard someone builds.

---

## Sources

- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/)
- [Transparency obligations under Article 50 of the AI Act — European Commission FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act)
- [EU AI Act — Transparency Obligations for AI-Generated Content (Article 50), Orrick](https://www.orrick.com/en/Insights/2026/08/EU-AI-Act-Transparency-Obligations-for-AI-Generated-Content-Article-50)
- [The AI Act's Transparency Obligations: Rules, Scope and Timeline, Stibbe](https://www.stibbe.com/publications-and-insights/the-ai-acts-transparency-obligations-rules-scope-and-timeline)
- [Sub-Processor (AI Vendors), GDPR Article 28(2) Obligations](https://www.knowlee.ai/glossary/sub-processor-ai)
- [AI Sub-Processor Disclosures in SaaS: A Reviewer's Guide](https://vensider.io/blog/ai-subprocessor-disclosures-saas)
- [Defending Against Indirect Prompt Injection Attacks With Spotlighting](https://ceur-ws.org/Vol-3920/paper03.pdf)
- [Indirect Prompt Injection: The Complete Guide, NeuralTrust](https://neuraltrust.ai/blog/indirect-prompt-injection-complete-guide)
- [How Microsoft defends against indirect prompt injection attacks, MSRC](https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks)

---

## Output format

Per the skill: this is the Markdown version. A `.docx` via the `document-tools/docx` skill is available on request — recommended if §5 and §15 are going to a stakeholder audience, since the Stress Test reads better as a standalone appendix in that format.
