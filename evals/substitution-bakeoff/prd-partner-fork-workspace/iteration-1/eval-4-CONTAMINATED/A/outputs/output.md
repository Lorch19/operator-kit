# Document Summaries in the Weekly Digest

**Skill running:** `prd-partner`
**Mode:** Discovery Mode → PRD Mode · **Output mode:** Dev-Team
**Date:** 2026-09-16 · **Version:** v1.0

---

## 0. Mode detection, and how this was run unattended

**Idea clarity → Fuzzy → Discovery Mode.** The ask names a mechanism ("auto-summarise with an LLM") and a surface ("in the digest"). It does not name a problem, a user, a trigger, or a definition of success. The skill's *When to Push Back* list opens with exactly this case — a problem stated as a solution — so Discovery runs first, and the PRD is generated from the reframed problem, not from the literal ask.

**Output mode → Dev-Team.** The context describes a feature inside a shipped product with an existing digest pipeline. Nothing signals a coding agent will build it (no repo, no stack, no build-model question) and nothing signals a leadership funding decision. Dev-Team is the correct default. Conversion notes are in §5 if the audience is actually different.

**Unattended handling.** This skill has three conversational gates: mode confirmation, the Synthesis Checkpoint sign-off, and the "deeper or tighter?" question before generating. I cannot ask, so I closed each gate myself and recorded the answer as a numbered, falsifiable assumption. Anything I could not responsibly invent — baselines, market sizes, specific compliance posture — is flagged **[NEEDS INPUT: …]** rather than filled in. Per the skill's Flags rule, no invented metrics, market sizes, or compliance requirements.

---

## 1. Assumptions register

Every assumption below would normally have been a question. Read this table first; if any row is wrong, the PRD section it points at is the one to re-open.

| ID | Assumption | Why this one | If wrong, what breaks |
|----|-----------|--------------|----------------------|
| A1 | The digest is a **weekly, per-user, per-project email** rendered by a batch job with a send window, not a live page. | Stated in the brief. | If it is an in-app feed, the latency, degradation, and no-recall constraints in §6 relax a lot. |
| A2 | "Uploaded documents" means **user-supplied files attached to a project** (PDF/DOCX/TXT/MD and similar), not the product's own native docs. | "Uploaded" implies ingest of foreign files. | If they are native collaborative docs, diff-based change summaries beat whole-document summaries, and §Requirements A changes shape. |
| A3 | Documents carry **per-document or per-project access control**, and digest recipients are not guaranteed to have access to every document in a project. | True of essentially every multi-user project tool. | If every project member can read every document, edge case E3 and requirement C1 become trivial. |
| A4 | There is **no LLM in production today** for this data. This feature introduces a new processor/sub-processor and a new outbound data flow. | Framing is "add a feature where we auto-summarise… with an LLM". | If a model vendor is already contracted for this data class, §4 shrinks to a DPA amendment and the consent work in D mostly disappears. |
| A5 | The business goal behind the ask is **digest engagement and reduced context-recovery cost**, not a new revenue line. | Digests are retention surfaces. Nobody prices a digest. | If this is a paid-tier upsell, Success Metrics and §Personas need a buyer persona and a packaging decision. |
| A6 | Some customers are **EU-established or process EU personal data**, so GDPR and (from 2 Aug 2026) EU AI Act Art. 50 transparency are live constraints, not theoretical. | Default-safe for a document product with any European footprint. | If the product is strictly US-only single-tenant, §4 compresses to contractual no-training terms and internal policy. |
| A7 | Cost per digest matters — this is an **always-on background cost across the whole base**, not a user-triggered action. | Weekly × every project × every document is the worst cost shape in AI features. | If volume is small (low thousands of docs/week), requirement F can be deferred to v1.1. |
| A8 | Ship target is **one quarter, one squad**, no dedicated ML team. | Default for a feature-sized ask with no stated constraint. | A longer runway would make the per-project synthesis (Option C in §2.4) viable for v1. |

---

## 2. Discovery Mode

### 2.1 Pushback: the ask is a solution wearing a problem's clothes

Three things are wrong with the request as written, and they compound.

**First, "summarise documents" and "the digest" are two different jobs glued together.** The digest today answers *what changed in my projects this week*. A document summary answers *what is in this file*. Those are different objects with different shelf lives. A document uploaded eight months ago has a summary, but it is not news, and the digest is a news product. Shipping the literal ask means the digest starts carrying content that did not change — which is the one thing a change digest is supposed to filter out.

**Second, the digest's scarcest resource is length, and this feature spends it.** A weekly email gets a few seconds of skim. The dominant failure mode of digests is not "insufficiently informative" — it is "too long, unsubscribed." A paragraph of LLM prose per document is the single fastest way to double the email. Any version of this feature that does not come with a hard word budget makes the digest worse while looking like it made it better.

**Third, there is no evidence in the ask.** No complaint, no support theme, no usage signal that says people are failing to keep up with documents. The skill's rule is to push back when there is only assumption. I am pushing back — and then proceeding under A5, because the run is unattended and a flagged assumption beats a stalled deliverable. **The single highest-value thing to do before building is to check whether document-related context loss is a real reported pain or a plausible-sounding one.** That is Open Question Q1, and it is the one that could kill the feature.

*Where I accept and move on:* auto-summarisation of changed documents is a well-established pattern across adjacent products, the technical risk is low, and the reversibility is high (it is a block in an email that can be removed in one deploy). This does not need a research quarter before a build. It needs a defined problem and a guardrail.

### 2.2 The reframe

> Not: *"Summarise uploaded documents with an LLM and put the summaries in the digest."*
>
> But: **"When a document in my project changes, tell me in one line what that means for the project — so I can decide whether to open it, without opening it."**

Three consequences fall straight out of the reframe, and they define v1:

1. **Change-scoped, not corpus-scoped.** Only documents created or modified inside the digest window appear. No backfill of the archive. This removes the "not news" problem, and it cuts cost by roughly the ratio of weekly-active documents to total documents.
2. **A decision aid, not a replacement artifact.** The summary exists to support one decision — open it or don't. That justifies one or two sentences, not an abstract. Length discipline stops being a nag and becomes the spec.
3. **Project-relative, not document-absolute.** "Q3 pricing model, replaces last week's draft — three tiers instead of two" is useful. "This document discusses pricing strategy" is not. The prompt must be given the surrounding project context and the prior version, or it will produce the second kind.

### 2.3 Discovery questions, self-answered

**The problem.** Project members lose the thread on documents. Files arrive from teammates, clients, and vendors; the notification that they arrived carries a filename and nothing else. A filename is a terrible summary — `Final_v3_updated.pdf` tells you nothing about whether it matters to you. So documents go unread, or get read late, or get read by the wrong person. The cost is invisible because nobody files a ticket saying "I did not read a document." **[NEEDS INPUT: Q1 — is this visible anywhere in support tickets, NPS verbatims, or the gap between document-upload and first-open-by-another-user?]**

**The trigger — why now.** Two reasons that are actually true rather than convenient. (a) The cost and latency of competent summarisation have collapsed; a per-document summary is now a fraction of a cent, which was not true when this digest was designed. (b) Summarised digests are becoming a baseline expectation in this software category — arriving late is not a differentiator problem, it is a "feels dated" problem.

**The outcome.** The digest gets more useful without getting longer: readers click through to more of the documents that matter to them, skip the ones that don't, and unsubscribe at the same rate or lower. Note the trap in §Success Metrics — raw document-open rate is the wrong metric, and it may correctly go *down*.

**The scope.** Smallest version that delivers value: one sentence per document that changed this week, for documents with extractable text, inside the existing digest layout, capped per project. **Out:** chat with your documents, cross-document synthesis, search, action-item extraction, meeting notes, summaries on the document page itself, and a separate "AI" tab. Each of those is a real product; none of them is this one.

**The riskiest assumption.** Not "can the model summarise" — it can. It is: **a one-line summary changes what the reader does.** If people already knew which documents mattered from the filename and the uploader's name, the summary is decoration and the metrics will not move.

**Dependencies.** Text extraction for the document formats in scope (the boring half of this feature, and the half most likely to slip); a model vendor with acceptable data terms; digest template capacity; admin-level settings plumbing.

**The market.** Skipping TAM/SAM/SOM deliberately: this is a retention feature inside an existing product, not a market entry, so market sizing does not shape a single requirement. Fabricating a number here would violate the skill's Flags rule and change nothing about what gets built.

**The competition.** Document-and-activity summarisation now ships as a default in the large collaboration suites — the pattern is table stakes, not an edge. What is still genuinely contested, and where this can be better than the incumbents: incumbents summarise the *document*; almost none of them summarise the *change relative to the project*. **[NEEDS INPUT: Q7 — confirm against the actual named competitor set before this claim goes in a customer-facing deck.]**

### 2.4 Architecture decision

This is system design, not just a feature, so alternatives get evaluated before committing — per the skill's Architecture Decisions step. The decision that matters: **when is the summary computed?**

| | Approach | Risk | Complexity | Time to value | Extensibility | Waste |
|---|---|---|---|---|---|---|
| **A** | **Generate on upload/change (async), store keyed by content hash, digest reads stored text** | **Low** — digest job does zero model calls; a vendor outage degrades to no-summary, never to no-digest | **Medium** — needs a job queue, a store, a versioning key | **Fast** | **High** — the stored summary is immediately reusable on the document page, in search, in notifications | **Low** — recomputed only when content changes; same file in two projects computed once |
| B | Generate during the digest build, per document | **High** — the weekly send now depends on N×M model calls inside a deadline; one rate-limit event delays or drops the whole batch | Low | Fast | Low — summary exists nowhere else | High — recomputed every run |
| C | Generate one synthesised paragraph per project per week (all changed docs in a single call) | Medium — better reading experience, but a single hallucinated clause taints the whole block and is un-attributable to a source | High — harder to evaluate, harder to cite, harder to permission-filter per recipient | Slow | Medium | Medium |
| D | No LLM — extractive heuristics (title, first paragraph, headings) | Very low | Very low | Immediate | Low | None |

**Chosen: A.** The decisive argument is not quality, it is blast radius. The weekly digest is an existing, working product that people rely on; B makes its delivery dependent on a third-party model's availability inside a batch deadline, which trades a solid asset for a new feature. A keeps the model call on the upload path, where a failure is invisible and retryable, and the digest simply renders what exists.

**On D:** worth saying out loud that extractive heuristics are not embarrassing — for well-structured documents they are competitive, and they cost nothing. They are rejected because they fail exactly where the need is greatest (scanned contracts, slide decks, anything where the first paragraph is boilerplate). D survives as the fallback path when the model is unavailable — see requirement A6.

**On C:** the better long-term reading experience, kept as the v1.1 candidate once per-document faithfulness evaluation is in place and trusted. Building C first means shipping the hardest-to-evaluate output with no evaluation history behind it.

*Recorded so it is not quietly re-litigated during the build: a future implementer who moves generation into the digest job to "simplify" has re-chosen B and reintroduced the blast-radius problem.*

### 2.5 Scope creep watch

Items that surfaced during discovery and were deliberately pushed out of v1. Each was individually defensible; the aggregate is a different product.

| Deferred | Why not v1 |
|---|---|
| Per-project synthesis paragraph (Option C) | Needs a faithfulness track record first |
| Action-item / owner / deadline extraction | Different failure mode — a missed action item is worse than a vague summary, and it needs its own evaluation |
| Summary shown on the document page | Cheap once summaries are stored, but it widens QA surface and the store is designed for it anyway |
| Ask-a-question-about-this-document | A separate product |
| User-tunable summary length or tone | Settings surface with no evidence anyone wants it |
| Non-text documents (images, video, audio) | Different pipeline entirely |

### 2.6 Synthesis checkpoint

> **Problem:** Project members cannot tell from a filename whether a newly added or changed document matters to them, so relevant documents go unread or are read too late.
> **User:** Project members who receive the weekly digest and are not the person who uploaded the file.
> **Core insight:** The digest's job is *what changed*, so the summary must describe the change in project terms — not abstract the document — and must cost almost no additional email length.
> **Scope boundaries:** Documents with extractable text, changed inside the digest window, one to two sentences each, capped per project, rendered inside the existing digest layout. No chat, no cross-document synthesis, no new surfaces.
> **Riskiest assumption:** That a one-line summary changes reader behaviour at all, rather than being pleasant decoration on an email people already skim.
>
> **PRD readiness: 7/10.** The problem, the mechanism, and the failure modes are specific enough to build against, and the architecture question is settled. It is not a 9 because the pain is assumed rather than evidenced (Q1) and every success target lacks a baseline (Q2).
>
> **Risks:**
> 1. **Unevidenced pain** — the whole feature could be decoration. *Resolvable before build, cheaply: one query on upload-to-first-external-open latency, plus a support-ticket search. Does not block starting the pipeline work, which is reusable regardless.*
> 2. **Trust cliff in an un-editable channel** — a wrong or embarrassing summary lands in an inbox and cannot be recalled. One bad summary about a sensitive document costs more trust than fifty good ones earn. *Blocks launch, not build: requires the quality gate (E) and the injection defences (C) to be in place before the first real send.*
> 3. **New sub-processor for customer document content** — enterprise customers who accepted "we store your files" did not accept "we send your files to a model vendor." *Blocks launch. Needs DPA/sub-processor notice and a workspace-level off switch — see §4.*
> 4. **Digest length inflation → unsubscribes** — the feature can damage the surface it is improving. *Resolvable during build via a hard word budget and the unsubscribe guardrail metric.*
> 5. **Always-on cost across the whole base** — scales with documents × recipients, forever, whether or not anyone reads it. *Resolvable during build: content-hash dedupe, change-window scoping, per-project caps.*

*Gate normally requiring sign-off here. Proceeding under the unattended constraint; risks 2 and 3 are launch blockers and are carried into §6 so they cannot be lost.*

---

## 3. PRD — Dev-Team Mode

### 1. Context

**TL;DR.** When a document in a project is added or changed, we generate a one-to-two-sentence summary of what changed and show it beside that document in the weekly digest, so readers can decide what to open without opening anything. We build it now because the per-document cost is negligible, summarised digests have become a category expectation, and the digest is currently the only surface that tells people about documents while telling them nothing about the documents.

**Why now.** Summarisation quality at acceptable cost and latency crossed the usable threshold since the digest was designed, and competitors in adjacent collaboration suites now ship this by default — the gap is starting to read as staleness rather than restraint.

**Market & competitive context.** *TAM/SAM/SOM intentionally omitted — this is a retention feature in an existing product; market sizing shapes none of the requirements below.*

| Competitor pattern | How they handle it | Gap / our angle |
|---|---|---|
| Large collaboration suites (doc/drive products with built-in AI) | Summarise the document on demand, on the document's own page | Nobody has to ask for ours; it arrives where attention already is |
| Workspace AI recaps | Summarise *activity* (messages, events), documents only shallowly | We summarise the document's change in project terms |
| Search/knowledge assistants | Summarise on query — user must already know what to look for | Ours serves the person who does not yet know a document exists |

*Pattern-level observation, not a verified audit of a named competitor set — see Q7.*

**The narrative.** Maya runs implementation projects for three client accounts. Monday, 8:40am, on the train. Her digest arrives. Under **Northwind Rollout** she sees: *"Security review response — Northwind's InfoSec answered our questionnaire; two items marked non-compliant (data residency, SSO enforcement)."* She has never opened a security questionnaire response in her life without being asked twice. She opens this one, and by 9:15 she has pulled the SSO question into the standup agenda — four days before the client would have raised it. Below it, three more documents she scrolls past in a second and a half, because now she can tell they are the vendor's standard onboarding packet.

**Success metrics.** Targets are relative movements against baselines we do not currently have; those are flagged rather than invented.

| Type | Metric | Target |
|---|---|---|
| Primary | **Qualified click-through**: digest recipients who open at least one document *from* the digest, per weekly send | **[NEEDS INPUT: baseline]** — propose +20% relative, measured against the holdout, not against last quarter |
| Primary | **Time from document upload to first open by a non-uploader** (median) | **[NEEDS INPUT: baseline]** — propose −25% for documents that appear in a digest |
| Secondary | **Summary helpfulness**: thumbs-down rate on rendered summaries | Under 3% of rendered summaries, and no single project above 10% |
| Guardrail | **Digest unsubscribe + mark-as-spam rate** | Must not increase vs. holdout. **A statistically detectable increase is a rollback trigger, not a discussion.** |
| Guardrail | **Faithfulness pass rate** of generated summaries (see requirement E1) | Above 95% before any general rollout |
| Quality | **Digest length** (rendered word count, p90) | No more than +15% vs. pre-launch |
| Cost | Cost per digest send | **[NEEDS INPUT: acceptable ceiling]** |

**A metric trap, stated explicitly because it will otherwise be measured wrong.** "Document opens went up" is *not* unambiguously success, and "document opens went down" is *not* unambiguously failure. A summary that correctly tells Maya she can skip the vendor's standard onboarding packet has done its job by *preventing* an open. This is why the primary metric is *click-through from the digest* — an action the summary caused — rather than total document opens, and why helpfulness feedback is collected directly. Anyone reporting total opens as the headline number is reporting a proxy that points both ways.

### 2. Personas

| Persona | Description |
|---|---|
| **Digest reader (primary)** | Project member, not the uploader. Skims the digest on a phone in under 30 seconds. Optimises for "is there anything here I need to act on." Will not read a paragraph. |
| **Document author / uploader** | Uploaded the file. Never sees a useful summary of their own work — but *does* care that the summary sent to their colleagues represents it accurately and does not expose something they considered incidental. |
| **Workspace admin / security reviewer** | Approves what happens to company documents. Did not sign up for a model vendor. Has a veto, and will use it if they learn about the feature from the digest rather than from us. |

### 3. Scope

**Goals**
- Summarise documents created or modified inside the digest window, per project.
- Render one to two sentences per document inside the existing digest layout, within a hard word budget.
- Describe the change in project-relative terms where a prior version exists.
- Degrade invisibly: no summary is always acceptable; a delayed or missing digest is not.
- Ship a workspace-level off switch and the disclosures required to turn the feature on for everyone else.

**Non-goals**
- Backfilling summaries for the existing document archive.
- Cross-document or per-project synthesis (v1.1 — see §2.4 Option C).
- Action-item, owner, or deadline extraction.
- Any conversational or query interface over documents.
- Summaries on the document page, in search, or in real-time notifications (the store is built to support these; the surfaces are not in v1).
- Non-text-bearing media: images, audio, video.
- User-configurable length, tone, or language preferences.

### 4. Domain & Regulatory Context

Three regimes bind this feature specifically. None of this is generic compliance boilerplate — each row changes a requirement.

| Area | Requirement / best practice | Impact on this feature |
|---|---|---|
| **GDPR Art. 28 — sub-processors** | A sub-processor must be authorised by the controller and bound by GDPR-equivalent terms. SaaS DPAs typically run on *general authorisation*: a right to be notified of sub-processor changes with a defined objection window (commonly 10–30 days). Annexes naming the details of processing, security measures, and the sub-processor list must actually be completed. | The model vendor must be added to the published sub-processor list and customers notified **before first processing**, with the objection window elapsed. Drives requirement D1 (workspace off switch) — an objecting customer needs an answer other than "terminate your contract." |
| **GDPR Chapter V — transfers** | Transfers outside the EEA need an adequacy decision or SCCs. | Constrains vendor and region choice; EU-resident workspaces should pin inference to an EU region. Drives D4. |
| **EU AI Act Art. 50 — transparency** | Transparency obligations apply from **2 August 2026**. AI-generated or AI-modified content, explicitly including **summaries**, falls in scope where it materially affects meaning; generative outputs must be marked in a machine-readable form as artificially generated. Penalties reach €15m or 3% of worldwide turnover. | This feature is squarely in scope and the date has already passed. Drives B4 (visible labelling) and B5 (machine-readable marking in the email payload). This is not a nice-to-have disclosure. |
| **OWASP LLM01 — prompt injection** | For untrusted input, OWASP's named mitigations include *"Segregate and identify external content"* (separate and clearly denote untrusted content), *"Implement input and output filtering"*, *"Define and validate expected output formats"*, and *"Constrain model behavior"*. | Uploaded documents are untrusted by definition — anyone can email a client a PDF. Drives requirements C2–C4. |
| **Summarisation faithfulness evaluation** | Established practice runs cheap deterministic checks first (length, schema), then classifier-based faithfulness scoring, with LLM-as-judge last, using a pinned judge model and a versioned rubric. Rubrics that force per-claim verdicts with quoted supporting spans agree with humans far better than a single "is this faithful?" score. | Drives requirement E1 — a layered gate, not a single vibe check, with the rubric under version control. |

**The non-obvious one.** The digest is a **sender-authenticated email from us**. Content that originates in an attacker-supplied document and is rendered inside that email inherits our sender reputation. An uploaded PDF containing text crafted to be repeated by a summariser becomes a phishing message wearing our brand. This is why C3 (no URLs, no contact details, no imperatives sourced from document content) and C4 (plain-text rendering, no HTML passthrough) are P0 and not polish.

### 5. Requirements

#### A. Summary generation pipeline

**P0**
- **A1** — On document create or content change, enqueue a summarisation job asynchronously. The upload response must not wait on it.
- **A2** — Key stored summaries by `(content_hash, prompt_version, model_version)`. Identical content across two projects is generated once. A prompt or model change invalidates the cache without a data migration.
- **A3** — Extract text for the v1 format set: PDF (text layer), DOCX, TXT, MD, RTF. **[NEEDS INPUT: confirm against actual upload-volume-by-mimetype — build for the real top five, not the assumed one.]** Documents with no extractable text produce no summary and no error surface.
- **A4** — Pass project context into the prompt: project name, document title, uploader, and — where a prior version exists — a representation of the previous version, so the model can describe the change rather than the document.
- **A5** — Enforce the output contract in code, not in the prompt alone: a structured object with a `summary` field of at most **[NEEDS INPUT: word cap, propose 30]** words, no URLs, no markup. Violations are rejected and retried once, then dropped.
- **A6** — On model failure, timeout, or rejected output after retry, fall back to the extractive heuristic (title plus leading substantive sentence) **only if** it passes the same output contract; otherwise render the document with no summary, exactly as today.
- **A7** — Truncate oversized documents to a bounded context with a deterministic, documented strategy (head plus structural headings), and record that truncation occurred on the stored summary.

**P1**
- **A8** — Re-summarise on content change only, not on metadata change (rename, move, re-share).
- **A9** — Coalesce repeated edits: if a document changes N times inside the window, summarise the final state once and record the change count.

**P2**
- **A10** — Summarise in the document's dominant detected language. Cross-language handling is Q5.

#### B. Digest rendering

**P0**
- **B1** — Render summaries only for documents created or modified inside the digest window. No archive backfill.
- **B2** — Cap summaries per project per digest at **[NEEDS INPUT: propose 5]**, ordered by recency of change, with a plain "+N more documents" line. The cap is a product decision about email length, not a performance workaround.
- **B3** — The digest build **never blocks on summary generation**. Missing summary renders the document row exactly as it renders today. Send time is unchanged.
- **B4** — Label summaries as AI-generated in visible copy, once per block rather than once per summary.
- **B5** — Mark summary content as machine-readably AI-generated in the email payload, per §4. **[NEEDS INPUT: legal to confirm the specific marking convention we adopt.]**
- **B6** — Per-summary feedback control (helpful / not helpful) that works without a login round-trip, feeding the secondary metric.

**P1**
- **B7** — Hold out a randomised **[NEEDS INPUT: propose 10%]** of recipients with summaries suppressed, for the duration of the measurement period. Without this, every primary metric is uninterpretable — seasonality and concurrent releases will move them.

#### C. Trust, safety, and permissions

**P0**
- **C1** — Re-check document access **at digest render time, per recipient** — never at generation time. Generation is per document; visibility is per reader. A summary must not render for a recipient who cannot open the document.
- **C2** — Delimit and label document text in the prompt as untrusted data, per OWASP *"Segregate and identify external content"*. Instructions live in the system prompt only.
- **C3** — Strip from summary output: URLs, email addresses, phone numbers, and second-person imperatives. A summary that tells the reader to do something is a rejected summary.
- **C4** — Render summaries as plain text. No HTML, no markup, no links originating in document content.
- **C5** — Redact or suppress before send when the summary contains detected credentials or secrets.
- **C6** — Log every generation with document id, prompt version, model version, and output, retained long enough to investigate a complaint about a sent email. **[NEEDS INPUT: retention period — must satisfy both investigation needs and data-minimisation.]**

**P1**
- **C7** — Adversarial test suite of documents crafted to manipulate the summariser, run in CI against the prompt, per OWASP *"Conduct adversarial testing and attack simulations"*. The prompt is code and regresses like code.
- **C8** — Suppress summaries for documents whose sensitivity classification exceeds a threshold, where such classification exists. **[NEEDS INPUT: do we have document sensitivity labels today?]**

#### D. Controls and consent

**P0**
- **D1** — Workspace-level off switch, admin-controlled, honoured by both generation and rendering. Off means documents are not sent to the vendor at all, not merely hidden.
- **D2** — Model vendor added to the published sub-processor list, with customer notification and the DPA objection window elapsed before first processing.
- **D3** — Contractual terms with the vendor prohibiting training on our customers' content and bounding retention. **[NEEDS INPUT: vendor and terms — commercial decision.]**

**P1**
- **D4** — Region-pinned inference for workspaces with a data-residency commitment.
- **D5** — Per-user opt-out of seeing summaries in their own digest, distinct from the workspace switch.

**P2**
- **D6** — Per-project suppression, for projects handling sensitive material inside a workspace that is otherwise opted in.

#### E. Quality evaluation and observability

**P0**
- **E1** — Layered pre-send quality gate: (1) deterministic checks — length, schema, no-URL contract; (2) a faithfulness check scoring the summary against the source text; (3) LLM-as-judge on a versioned rubric, pinned judge model, run on a sample rather than every item. The rubric demands per-claim verdicts with quoted supporting spans, not a single holistic score. Below threshold, the summary is dropped — **an email cannot be recalled, so the gate fails closed.**
- **E2** — A frozen golden set of representative documents with human-reviewed reference summaries, run before any prompt or model change reaches production.
- **E3** — Dashboards for generation success rate, gate rejection rate by reason, p50/p95 generation latency, thumbs-down rate, and cost per digest.

**P1**
- **E4** — Sample human review of rendered summaries weekly for the first **[NEEDS INPUT: propose 6]** weeks post-launch. Automated faithfulness scoring does not catch tone, awkwardness, or the summary that is technically true and socially disastrous.

#### F. Cost and rate control

**P1**
- **F1** — Per-workspace generation rate limits and a global circuit breaker that disables generation (never the digest) on cost or error-rate breach.
- **F2** — Skip documents below a minimum length threshold — see edge case E6.
- **F3** — Cost attribution per workspace, so the cost-per-digest metric can be read by segment rather than as one blended number.

---

### Mid-generation quality check

Per the skill's checkpoint, I paused after §4 and re-read §1–4 before writing the requirements. Two things were below standard and were fixed rather than left:

- **Success metrics were vanity on the first pass.** They read "summaries generated" and "document opens." Both are proxies that move for reasons unrelated to the feature working. Replaced with a caused-action primary metric, an explicit unsubscribe guardrail with a rollback trigger, and a written warning that total opens points both ways.
- **Access control was buried in edge cases.** Re-checking permissions per recipient at render time is not an edge case, it is the difference between a feature and an incident. Promoted to requirement C1, P0.

Self-assessment after the fix: **8/10** on specificity. The residual gap is that seven values are genuinely unknown to me and are flagged rather than guessed.

---

### 6. Dependencies & Risks

| Dependency | Owner | Impact |
|---|---|---|
| Text extraction for the v1 format set | Backend | Blocks A3. Historically the most underestimated part of this kind of feature — PDFs with no text layer, DOCX with tracked changes, encrypted files |
| Model vendor selection and contract | Legal + Eng leadership | Blocks D2/D3, therefore blocks launch, not build |
| Sub-processor notice and objection window | Legal | **Calendar dependency with a fixed minimum duration — start it in week 1 or it becomes the critical path** |
| Art. 50 marking convention | Legal | Blocks B5 |
| Digest template capacity and holdout infrastructure | Growth / lifecycle | Blocks B2 and B7 |
| Admin settings surface | Frontend | Blocks D1 |

| Risk | Mitigation |
|---|---|
| **A wrong summary lands in an inbox and cannot be recalled** | E1 fails closed; C3/C4 constrain the output; staged rollout starting with internal workspaces |
| **Prompt injection from an uploaded document becomes a phishing email under our sender identity** | C2–C4 plus the CI adversarial suite (C7). Treat as a security review item, not a quality item |
| **Sub-processor objection from an enterprise customer** | D1 gives them a real answer; D2 makes the notice arrive from us rather than from a surprised end user |
| **Digest gets longer, unsubscribes rise** | B2 cap, A5 word cap, unsubscribe guardrail with a pre-agreed rollback trigger |
| **Cross-ACL content leak via summary** | C1 render-time per-recipient check |
| **Cost grows with the base indefinitely** | A2 content-hash dedupe, B1 change-window scoping, F1 circuit breaker |
| **The feature is decoration — metrics do not move** | B7 holdout makes this *detectable*. Without it we would ship and assume. Pre-commit to the decision rule: no detectable movement after the measurement period means remove the block, keep the pipeline (which is reusable for the document page and search) |

### 7. Edge Cases

Non-obvious only. Standard loading and empty states are not specified here.

| Scenario | Behaviour |
|---|---|
| **E1** Document deleted after summarisation but before send | Suppress. Existence-check at render, alongside the C1 access check |
| **E2** Access revoked between generation and send | Suppress for that recipient. Same render-time check |
| **E3** Document visible to the uploader but not to other project members | Renders for those with access, omitted for those without — the same digest differs per recipient, by design |
| **E4** Document contains text engineered to manipulate the summariser | Output contract (A5) and filters (C3) reject it; the attempt is logged and alerted on. Alerting matters: repeated attempts are a signal about the uploader |
| **E5** Scanned PDF or image-only file — no text layer | No summary, no error message. "Could not summarise" lines are noise multiplied by every such document |
| **E6** Document shorter than the summary would be (a two-line note) | Skip summarisation; render the document's own opening text |
| **E7** Password-protected or encrypted file | No extraction, no summary, no error surface |
| **E8** Document changed 14 times during the window | One summary of the final state, plus "updated 14 times" from A9 |
| **E9** Same file uploaded to two projects | Generated once (A2), rendered in both, permission-checked independently |
| **E10** Document contains a third party's personal data — a CV, a medical note, a signed contract | The summary can surface into an email what was previously behind a click. Mitigated by C1 and C8; **the residual case is Q4 and is a genuine open question, not a solved one** |
| **E11** Document restored from trash inside the window | Treat as a change; re-summarise if the content hash is absent from the store |
| **E12** Document written in a language the recipient does not read | v1 summarises in the document's language (A10). Known-imperfect — Q5 |
| **E13** Model vendor outage across the entire window | Digest sends on time with no summaries. The user-visible outcome is last quarter's digest, which is acceptable; a late digest is not |

### 8. Open Questions

**For Product / Research**
- **Q1** — *Blocking-if-negative.* Is document context loss a real, observable pain? Check: support tickets mentioning missed or unread documents; median upload-to-first-external-open latency; whether that latency correlates with anything we can act on. **If this comes back empty, the honest answer is that this feature is a category-expectation play, and it should be scoped and funded as one.**
- **Q2** — Current baselines for digest click-through, unsubscribe rate, and rendered length. Every target in §Success Metrics is unset until these exist.
- **Q3** — Per-project summary cap and word cap: 5 and 30 are proposals, not decisions. Worth one round of rendered mockups at realistic volumes.

**For Legal / Privacy**
- **Q4** — Where a document contains a third party's personal data, does surfacing a summary in an email to a wider project audience constitute a new processing purpose requiring its own basis? (E10.)
- **Q5** — Language handling: summarise in the document's language, or the recipient's? The second is a translation, which is separately in scope for Art. 50 marking.
- **Q6** — Art. 50 machine-readable marking convention for email-delivered AI text, and generation-log retention period (C6).

**For Engineering / Data**
- **Q7** — Verify the competitive claim in §1 against the actual named competitor set before it is used externally.
- **Q8** — Real upload-volume-by-mimetype distribution, to size A3 against reality rather than assumption.
- **Q9** — Do document sensitivity labels exist today? C8 depends on it.
- **Q10** — Acceptable cost-per-digest ceiling, and who owns that budget line.

### Appendix

- **[NEEDS INPUT]** Prompt specification and versioning policy — link
- **[NEEDS INPUT]** Faithfulness rubric v1 (versioned, pinned judge model) — link
- **[NEEDS INPUT]** Golden evaluation set — link
- **[NEEDS INPUT]** Digest template mockups at 1, 5, and 5+ document volumes — link
- **[NEEDS INPUT]** Tracking plan for the metrics in §1 — link
- **[NEEDS INPUT]** Sub-processor notice and DPA amendment — link

---

## 4. Stress Test

*What is weakest here, what could be wrong, what a smart critic would say.*

**The weakest part is the evidence base, and no amount of structure fixes it.** This PRD is well-formed reasoning on top of an assumed problem. A1–A8 carry the whole thing. The most likely way this ships and fails is not a technical failure — it is that summaries render correctly, look good in the demo, and change nobody's behaviour, because people were already deciding from the filename and the uploader's name. Q1 and the B7 holdout exist precisely because I cannot rule this out from here.

**The strongest counter-argument to the core reframe.** I argued the digest is a *change* product and therefore summaries should be change-scoped. A critic would say: the real reason people do not read documents is not that they missed the notification, it is that they do not have time — and for them, a summary of an *old, important* document is more valuable than a summary of a *new, trivial* one. That critic may be right. Change-scoping is a cost and simplicity decision as much as a product one, and I should own that. If Q1 shows the pain is about the archive rather than the flow, Option C (per-project synthesis, maybe even relevance-ranked across the archive) is the better product and this v1 is the wrong shape.

**Where the architecture decision could be wrong.** I chose generate-on-upload primarily on blast radius. The cost of that choice is staleness: a summary generated at upload reflects the document at upload, and A8's change-detection is the only thing keeping it honest. If change detection is unreliable — and for some formats it will be, because a trivial re-save can alter a content hash while a meaningful edit inside a PDF may not — summaries will drift from their documents in ways nobody notices until a customer does. Option B has no staleness problem at all. I still think A is right; the honest framing is that I traded a *visible* failure mode (late digest) for an *invisible* one (stale summary), and invisible failures are the ones that survive longest.

**Where the metrics could still be wrong.** The paired-metric design is better than raw opens, but qualified click-through is itself gameable by making summaries *intriguing* rather than *informative* — a summary that withholds the punchline drives clicks and degrades the product. If click-through rises while thumbs-down also rises, that is the signature of this failure, and it should be read as a failure rather than a mixed result.

**What a smart competitor would say.** "You spent a quarter putting one sentence next to a filename. We shipped a summary on every document page, in search results, and in notifications from the same pipeline in the same quarter." They would have a point — and the architecture here is deliberately built so that becomes a rendering exercise rather than a rebuild. But the v1 surface list is narrow on purpose: one surface means one evaluation loop and one blast radius while the faithfulness track record is being established. That is a defensible trade for the first release and an indefensible one for the third.

**What would change my mind entirely.** If Q1 returns evidence that people *do* open documents promptly and the complaint is instead "I open it and still cannot find the part that matters," then summarisation is the wrong intervention and in-document highlighting is the right one. Same technology, different product, different PRD.

---

## 5. Self-assessment and conversion notes

**Rate it: 8/10 for a Dev-Team PRD.**

| Section | Rating | Note |
|---|---|---|
| Context & narrative | 8 | Specific and concrete; the metric trap is the most useful paragraph in the document |
| Success metrics | 6 | Well-designed shapes, no baselines. Cannot exceed 6 until Q2 is answered |
| Domain & regulatory | 9 | Sourced, specific, and each row drives a requirement rather than decorating the doc |
| Requirements | 8 | Buildable. Seven bracketed values are real unknowns, not laziness |
| Edge cases | 9 | E3, E4, and E10 are the non-obvious ones and they are the ones that cause incidents |
| Risks | 8 | Launch blockers separated from build risks; rollback trigger pre-agreed |
| Evidence base | 5 | The honest weak point. Flagged rather than papered over |

**If the audience is actually different.** To **Stakeholder** mode: add an executive summary, business impact, and a resource ask; cut §5 Requirements and §7 Edge Cases entirely; lead with the recommendation. To **AI-Build** mode: keep everything, then add acceptance criteria per requirement in given/when/then form, explicit state and flow logic for the generation pipeline, UI description for the digest block and admin setting, design direction, an Architecture Decision Record capturing §2.4 so a builder does not "simplify" back to Option B, and — if autonomous — hold points at (HP-1) text extraction working across the real mimetype distribution, (HP-2) first summaries passing the E1 gate on the golden set, and (HP-3) before the first send to any non-internal recipient.

---

## Sources

- [Article 50: Transparency Obligations for Providers and Deployers of Certain AI Systems — EU Artificial Intelligence Act](https://artificialintelligenceact.eu/article/50/)
- [EU AI Act — Transparency Obligations for AI-Generated Content (Article 50) — Orrick](https://www.orrick.com/en/Insights/2026/08/EU-AI-Act-Transparency-Obligations-for-AI-Generated-Content-Article-50)
- [EU AI Act: Transparency Obligations Take Effect 2 August 2026 — Cooley](https://www.cooley.com/news/insight/2026/2026-08-03-eu-ai-act-transparency-obligations-take-effect-2-august-2026)
- [Transparency obligations under Article 50 of the AI Act — European Commission](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act)
- [The SaaS DPA Guide: GDPR Requirements, Subprocessors, and Automation — Secure Privacy](https://secureprivacy.ai/blog/data-processing-agreements-dpas-for-saas)
- [GDPR and third-party risk: Article 28, sub-processors, and transfers — Rescana](https://www.rescana.com/learn/compliance/gdpr-third-party-risk/)
- [Third-Party Sub-Processor Management Under GDPR — ComplyOne](https://www.complyone.io/guides/gdpr/sub-processor-management-gdpr)
- [LLM01:2025 Prompt Injection — OWASP Gen AI Security Project](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [LLM Prompt Injection Prevention Cheat Sheet — OWASP](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [How to evaluate RAG faithfulness with LLM-as-a-judge — Langfuse](https://langfuse.com/resources/engineering/rag-faithfulness-evaluation)
- [LLM Summarization Evaluation: A 2026 Architectural Deep Dive — Future AGI](https://futureagi.com/blog/llm-summarization-evaluation-deep-dive-2026/)
- [LLM-as-a-judge: a complete guide to using LLMs for evaluations — Evidently AI](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)
