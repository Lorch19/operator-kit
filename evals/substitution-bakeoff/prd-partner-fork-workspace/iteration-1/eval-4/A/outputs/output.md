# Document Summaries in the Weekly Digest

**Skill:** `prd-partner` · **Mode:** Discovery (compressed, on paper) → PRD Mode, **Dev-Team** output
**Date:** 2026-09-16 · **Version:** v1.0

---

## 0. Mode call, and one piece of pushback before anything else

**Your ask was a solution, not a problem.** "Auto-summarise uploaded documents with an LLM and surface the summary in the digest" specifies a mechanism (LLM), an input (uploads), and a surface (digest) — but not who is hurting, how we know, or what changes if this works. The skill's push-back rule fires here: *problem stated as a solution*, and *no evidence of real user pain*.

Normally this is a Discovery Mode conversation. This run is unattended, so I ran discovery on paper: I picked the strongest reading of the request, wrote every assumption down as a numbered item you can overturn in one line, and continued into the PRD. **Every assumption below is a decision I made on your behalf. Read §2 first — if A1 or A4 is wrong, the PRD in §4 is the wrong PRD.**

**Output mode: Dev-Team.** Not AI-Build — that mode demands stack, data model, component library, and visual direction, none of which I have, and inventing them would hand a coding agent fabricated constraints to obey. Not Stakeholder — you asked to add a feature, not to fund one. §7 lists what a Dev-Team → AI-Build conversion would need to add.

**No TAM/SAM/SOM and no competitor table in this PRD.** Market sizing doesn't shape a single requirement for a feature inside an existing product, and I have no verified data on how specific competitors render digest summaries. Fabricating either would violate the skill's "don't invent" rule. Prior-art *patterns* that do shape requirements are folded into §4.4 and §4.5 instead.

---

## 1. The reframe

The digest is about **change**. A document summary is about **content**. These are different objects, and conflating them is how this feature goes wrong.

Today the digest almost certainly renders uploads as a filename row: *"3 documents added to Northwind Migration."* A filename is a **proxy for content** — it tells the reader something happened without telling them whether it matters. So they open the app to find out, or, far more often, they don't, and the document sits unread until someone asks about it in a meeting.

That gives three candidate problems, and they build three different products:

| | The job | What it implies | Delivery surface |
|---|---|---|---|
| **P-A Triage** | "Is this worth my attention this week?" | 1–2 lines, relevance-oriented, ruthlessly short | Email |
| **P-B Recall** | "What was in that doc again?" | Durable summary stored on the document | In-app, searchable |
| **P-C Comprehension** | "I'm not reading 40 pages" | Structured abstract, sections, key figures | In-app reader |

**The call:** build **P-B, render P-A.** One generation pass produces a durable summary stored as a first-class field on the document; the digest renders a compressed view of it. Not because it's more features — because of a measurement constraint:

> **You cannot learn anything inside an email.** No feedback control, no correction, no iteration, no undo. If the summary only exists in the digest, you ship an unmeasurable quality surface and find out it's bad from churn. The in-app summary is where thumbs-down lives, where you sample for faithfulness, and where a wrong summary can be fixed. The digest is a read-only projection of it.

**Core insight:** the digest's job is not to summarise documents. It is to let someone decide, from the email, whether a document changes their week. Optimise for *decidability*, not for coverage of the document.

---

## 2. Assumptions ledger

Each is a decision I made because the run is unattended. "If wrong" tells you the blast radius.

| # | Assumption | Why I chose it | If wrong |
|---|---|---|---|
| **A1** | The digest today lists uploads by filename/metadata, with no content signal | Only reading under which this feature has a problem to solve | If the digest already shows extracted excerpts, the gain shrinks to formatting — re-scope to a much smaller change |
| **A2** | B2B SaaS, multi-tenant, customer documents may contain personal and confidential data | Standard for "projects + collaborators + weekly digest" | If single-user consumer, §4.4 compresses by roughly half and the launch dependency in §4.6 disappears |
| **A3** | No LLM currently touches customer documents in production | "Add a feature" implies net-new capability | If an LLM is already in the product under an existing DPA and sub-processor notice, the legal lead time drops out of the critical path |
| **A4** | Summaries are per-document, not a per-project weekly narrative roll-up | "the user's uploaded documents" reads as per-document | A roll-up is a **different feature** with a different pipeline — this PRD does not cover it |
| **A5** | "Auto" means every eligible upload is summarised without user action | Your word | If summarisation should be on-demand, cost and consent surfaces change substantially |
| **A6** | Digest volume per user per week is typically single-digit documents, with a long tail of heavy weeks | Typical project-tool shape | If the median week is 30+ documents, the budget rule in §4.5 becomes the primary design problem, not a guardrail |
| **A7** | Document text extraction (PDF/DOCX → text) does not exist yet, or exists only for search indexing | Not implied by the request either way | If a mature extraction service exists, cut roughly a third of the P0 engineering |
| **A8** | Users can adjust digest settings; there is no existing per-feature AI consent surface | Digests almost always have settings | If an AI consent surface exists, reuse it rather than building §4.5 area 5 |

---

## 3. Architecture decision + synthesis checkpoint

### 3.1 Where the summary is generated — alternatives evaluated

| Approach | Risk | Complexity | Time to value | Extensibility | Waste if we pivot |
|---|---|---|---|---|---|
| **(a) On upload, async job, stored on document** ← **chosen** | Low — a week of retry runway before the digest needs it | Medium — needs a queue and a summary store | Medium | High — summary is reusable by search, in-app, notifications, API | Low |
| (b) At digest assembly time, batch | High — one weekly concurrency spike; a failure is unrecoverable, the email has already gone | Low | Fast | Low — summary exists only inside a rendered email | High |
| (c) Lazy, on first digest open | High — latency inside an email client; many clients won't execute it at all | Medium | Fast | Low | High |
| (d) On demand, user clicks "summarise" | Lowest cost and lowest consent risk | Low | Fast | Medium | Low — but **does not satisfy the request**; nothing to put in the digest |

**Chosen: (a).** The decisive argument is not cost, it's **failure timing**. In (b) and (c) a generation failure happens at or after send, when there is no recovery path and the user is already looking at a broken email. In (a) a failure happens days early, gets retried, and if it permanently fails the digest silently renders today's filename row — the user sees the product they already have, not a defect.

*Recorded so nobody "optimises" back toward (b): batching at send looks cheaper and simpler, and it is, right up until the first partial failure ships to every user simultaneously.*

### 3.2 Synthesis Checkpoint

> **Problem:** The digest tells users that documents arrived but not whether they matter, so documents land unread and the email trains people to skim past its most information-dense rows.
> **User:** A project owner triaging their week from a phone on Monday morning, plus the collaborator who wasn't in the room when the document was uploaded.
> **Core insight:** Build a durable, in-app document summary and render a compressed projection of it in the digest — the email is an unmeasurable, uncorrectable surface, so it must never be the only place the summary exists.
> **Scope boundaries:** Per-document summaries of text-bearing uploads, generated at upload, rendered under a hard budget in the digest, with tenant and user off-switches. **Out:** project-level roll-ups, chat/Q&A over documents, summaries of non-upload changes, translation, on-demand re-summarisation.
> **Riskiest assumption:** That a summary changes behaviour at all. The whole feature rests on the belief that people skip documents because they *can't tell* what's in them, rather than because they *don't have time* regardless. If it's time, a better summary changes nothing.
>
> **PRD readiness: 6/10.** The solution shape and the risk surface are solid; the problem evidence is entirely hypothesised, and there are no baselines, so every target in §4.1 is a blank. This is enough to build a bounded v1 against, not enough to justify a roadmap commitment.
>
> **Risks:**
> 1. **No evidence anyone wants this** — *blocks confident investment, not the build.* Resolvable cheaply: see §6.
> 2. **Sub-processor notice is on the critical path** — *blocks launch, not the build.* If customer DPAs use general authorisation with an objection window, that clock starts before the first production call. Start it in week 1. This is the single most likely cause of a slipped launch date.
> 3. **Uploaded documents are untrusted input and the digest is an outbound email from your domain** — *blocks launch.* Treated as P0 in §4.5.
> 4. **The digest may get worse, not better** — *resolvable during build* via the budget rule, but the unsubscribe guardrail in §4.1 is the thing that tells you.
> 5. **Every upload burns tokens forever** — *resolvable during build* via eligibility gating and per-tenant caps, but the unit cost never goes to zero.

---

## 4. PRD — Dev-Team Mode

### 4.1 Context

**TL;DR.** Generate a short, durable summary of each text-bearing document at upload time, store it on the document, and render a compressed, clearly-labelled version of it in the weekly digest under a hard length budget. Goal: let someone decide from the email whether a document changes their week.

**Why now.** The digest already earns weekly attention — a channel you cannot easily re-earn if you spend it — and its highest-value rows are currently the least informative. [NEEDS INPUT: is there a trigger beyond capability being available? If the honest answer is "we can now," say so in the doc — it's a valid reason, but it should be visible, and it lowers the bar for cutting the feature later.]

**The Narrative.**
Maya runs the Northwind migration. Friday afternoon, a vendor emails over a revised SOW; her contractor Dev uploads it to the project and logs off. Nobody @-mentions Maya.

Monday, 7:40am, phone, coffee. The digest lands. Where last week she'd have seen *"Northwind Migration — 1 document added: Northwind_SOW_v4_FINAL_rev2.pdf"* and scrolled past, she now sees:

> **Northwind_SOW_v4_FINAL_rev2.pdf** · added by Dev, Fri
> Revised statement of work. Moves the cutover milestone from March to May and adds a change-request process requiring written approval for scope changes over 40 hours.
> *AI-generated summary · [Open document]*

Maya doesn't need the document. She needs six seconds and the word "May." She forwards the digest to her VP before she's finished the coffee.

**The counter-narrative that shapes the budget rule:** the same Monday, Sam's team uploaded fourteen files — a photo dump from a site visit, three spreadsheets, a scanned invoice. If the digest renders fourteen summaries, Sam's digest is now four screens of gray text and he unsubscribes. The feature has to be as good at *staying quiet* as it is at speaking up. Hence §4.5 area 3.

**Success Metrics.**

| Type | Metric | Target |
|---|---|---|
| Primary (outcome) | Digest-attributed project re-engagement: % of digest opens followed by any project action within 48h | [NEEDS INPUT: current baseline] |
| Guardrail ⚠️ | Digest unsubscribe + mute rate, weekly | **Must not exceed baseline.** Trip-wire → auto-rollback |
| Guardrail | Digest open rate | Must not decline vs. baseline |
| Quality | Summary present for eligible uploads | ≥ 90% within 1h of upload |
| Quality | Faithfulness on a weekly human-rated sample (n≥50): no claim unsupported by source | ≥ 95% pass. Below 90% → pull the digest surface, keep in-app |
| Quality | In-app thumbs-down rate per rendered summary | [NEEDS INPUT: set after 2 weeks of data] |
| Cost | LLM spend per active tenant per week | [NEEDS INPUT: acceptable unit cost] — hard cap enforced regardless |

> **Deliberately not the primary metric: click-through from digest to document.** Success can move it in *either* direction — a good summary that fully answers the question suppresses the click, and that's a win, not a loss. Any framing that treats digest CTR as the north star will reward summaries that withhold information. Track it as a diagnostic only.

### 4.2 Personas

| Persona | Description |
|---|---|
| **Project owner (Maya)** | Reads the digest to triage, usually on mobile, usually under a minute. Primary beneficiary. Cares about *decidability*, not completeness. |
| **Collaborator-at-distance (Dev / the VP)** | Adjacent to the project, not in the working sessions. The digest is their only channel. Most likely to be *harmed* by digest bloat, because they have the least context to skim with. |
| **Tenant admin / privacy owner** | Decides whether customer documents may be sent to a third-party model at all. Not a user of the feature — a gatekeeper of it. Load-bearing here: see §4.4. |

### 4.3 Scope

**Goals**
1. A durable, stored summary for each eligible uploaded document, generated automatically at upload.
2. A compressed rendering of that summary in the weekly digest, under a hard per-digest budget.
3. The summary visible and correctable in-app, with feedback capture.
4. Tenant-level and user-level off switches, honoured at render time per recipient.
5. Failure that degrades to today's digest, never to a visible error.

**Non-Goals (v1)**
- Project-level or week-level narrative roll-ups (**a different feature** — see A4).
- Chat or Q&A over documents; retrieval; citations into page ranges.
- Summarising non-upload changes (comments, tasks, status).
- OCR of scanned documents, or summarising images, video, audio, CAD.
- Translation, or summarising into a language other than the document's.
- User-editable summaries, custom prompts, per-project tone settings.
- On-demand re-summarisation. (v1.1 — see §5.)

### 4.4 Domain & Regulatory Context

Sending customer documents to a third-party model is a data-protection event and a security event, not only an engineering one.

| Area | Requirement / best practice | Impact on this feature |
|---|---|---|
| **GDPR Art. 28 — sub-processors** | An LLM API that receives customer content is a sub-processor: it needs a DPA imposing equivalent obligations, it must appear on the public sub-processor list, and under the common "general written authorisation" model customers get notice and a right to object. | **Launch dependency with legal lead time, not a launch-day task.** Start the notice clock in week 1. Any customer who objects must be servable — which is *why* the tenant off-switch is P0, not P2. |
| **Data residency** | EU tenants frequently contract for EU-only processing. | Model endpoint region must be selectable per tenant, or EU tenants are excluded from v1. Decide explicitly; don't discover it in a renewal call. |
| **Provider retention & training** | Zero-retention, no-training endpoints are table stakes for B2B document content. | Contractual requirement on the model provider before any production call. Also means: no debugging by reading provider-side logs — build your own redacted observability (§4.5 area 6). |
| **EU AI Act Art. 50 (transparency)** | Applied from 2 Aug 2026, so it is live today. The strict marking/disclosure duties target deepfakes and AI text published to inform the public on matters of public interest; a private digest to a document's own project members is **likely outside** that scope. The transitional grace to 2 Dec 2026 covers systems already on the market before 2 Aug 2026 — **a feature launched now does not qualify for it.** | Do not treat the exemption as settled: [NEEDS INPUT: counsel to confirm scope]. **Label the summary as AI-generated regardless** — it's the right product call for a low-trust, uncorrectable surface, and it costs one line of text. |
| **Untrusted input — indirect prompt injection** | A document is attacker-controlled text. Documented attacks hide instructions in body text, metadata, comments, and white-on-white spans; mitigations are layered: delimit and isolate untrusted content, strip non-essential metadata, constrain output, scan output before use. | **This is the highest-severity risk in the feature** and drives P0s in §4.5 area 2. The blast radius is specific: your product sends the model's output, from your domain, into a user's inbox. A successful injection is brand-authenticated phishing. |
| **Summarisation faithfulness** | Faithfulness is the metric that tracks human judgement most closely; measured hallucination *and* omission rates in careful production settings are small but non-zero. Omission is the quieter failure. | Sampling and a rated faithfulness bar are P0 quality gates (§4.1), not a nice-to-have. Budget for the fact that a summary that omits the one material clause is worse than no summary, because it was trusted. |

### 4.5 Requirements

**Area 1 — Generation pipeline**

*P0*
- On upload completion, enqueue a summarisation job. Asynchronous; never blocks the upload response.
- **Eligibility gate runs before any model call.** Eligible = recognised text-bearing type (PDF with a text layer, DOCX, TXT, MD, RTF, ODT) **and** extracted text ≥ 200 characters **and** ≤ [NEEDS INPUT: page/token ceiling; propose 50 pages for v1]. Everything else is marked `not_eligible` with a reason and never reaches the model. This gate is the main cost control — it is cheaper to classify than to summarise.
- Summary is stored as a first-class record on the document: `text`, `model_id`, `prompt_version`, `source_version_id`, `generated_at`, `status`.
- Output constrained to **2–3 sentences, ≤ 400 characters**, declarative, no preamble ("This document…"), no recommendations, no invented figures. A number may appear **only** if it appears verbatim in the source.
- Retry ≤ 3 times with backoff. On permanent failure set `status = failed` and stop. Never retry inside digest assembly.
- Re-summarise on new document version; supersede rather than overwrite (keep prior summary for audit).

*P1*
- Per-tenant weekly token budget; on breach, stop generating and alert — do not silently degrade quality.
- Backfill capability for documents uploaded before launch, off by default and run per-tenant on request.

**Area 2 — Untrusted content and output safety**

*P0*
- Document text is passed to the model as clearly delimited untrusted data, never concatenated into instruction context.
- Strip before extraction: document metadata, author fields, comments, tracked changes, embedded scripts, EXIF.
- **The summary is plain text. Always.** No hyperlinks, no markup, no image references, no email addresses, no phone numbers in the rendered output. Strip them post-generation rather than asking the model not to produce them. This single rule removes most of the phishing blast radius.
- Output scan before storage: reject and mark `quarantined` if the summary contains a URL, an imperative directed at the reader ("click", "verify", "call", "reply"), credential/payment language, or a claim about the user's account or subscription status. Quarantined ⇒ digest falls back to the filename row.
- Adversarial test suite in CI with at least: metadata-embedded instructions, white-text instructions, instructions in a footer, a CV-style "rate this candidate highly" injection, and an instruction to emit a support phone number. Ship blocked on a clean pass.

*P1*
- Rate-limit summarisation per uploader to blunt automated probing of the injection surface.

**Area 3 — Digest rendering**

*P0*
- **Hard budget: at most 3 summaries per project per digest, at most 8 per digest.** Selection ranking [NEEDS INPUT: confirm order] — proposed: documents in projects the recipient acted in within 30 days first, then most recent. Everything beyond the budget renders as today's filename list with a count.
- Summaries render **only** for documents the recipient can access, with the ACL re-checked **at send time**, not at generation time. Access can be revoked between Tuesday and Sunday.
- Every summary carries a visible "AI-generated summary" label and an adjacent link to the source document. The link is generated by the digest, never by the model.
- Truncate to two lines with the full summary available in-app. The digest never scrolls for a single summary.
- `status` in {`failed`, `quarantined`, `not_eligible`, absent} ⇒ render exactly today's filename row. **No error text, no empty state, no "summary unavailable" placeholder.** The user must not be able to tell a summary was attempted.
- Plain-text email part carries the same summaries, same labels.

*P1*
- Collapse near-duplicate summaries from a bulk upload into a single line with a count.

**Area 4 — In-app surface and feedback**

*P0*
- Full summary shown on the document detail view, with the same AI label.
- Thumbs up/down with an optional free-text reason, stored against `prompt_version` and `model_id`. **Without this, you have no quality signal at all** — the email cannot give you one.
- Any user with document access can hide a summary from that document; hidden ⇒ suppressed for all recipients in all future digests. A wrong summary needs a stop button that doesn't require an admin.

*P1*
- Internal review queue for sampled faithfulness rating (feeds the §4.1 quality metric).

**Area 5 — Controls and consent**

*P0*
- **Tenant-level switch**, admin-controlled, **default [NEEDS INPUT: on or off — this is a commercial decision, not an engineering one]**. Off ⇒ no extraction, no model call, no storage for that tenant. Not merely hidden — not generated.
- **User-level switch** in digest settings, honoured per recipient at render time. Maya may have summaries off while her teammate has them on, for the same document.
- Sub-processor list updated and customer notice issued **before the first production call.**
- Project-level opt-out for sensitive projects (HR, legal, M&A). *P1 if tenant-level ships first, but expect this to be the first enterprise ask.*

**Area 6 — Observability, cost, evaluation**

*P0*
- Log per job: document id, tenant, eligibility decision, token counts, latency, status, `prompt_version`, `model_id`. **Never log document text or summary text** — zero-retention at the provider is undone by verbose logging at home.
- Dashboard: summary-present rate, failure rate by reason, quarantine rate, p95 latency, spend by tenant.
- Golden set of ~50 documents with human-written reference summaries; run on every prompt or model change; block the change on regression.
- Alerting on quarantine-rate spike — that is what an attack looks like from the inside.

### 4.6 Dependencies & Risks

| Dependency | Owner | Impact |
|---|---|---|
| LLM provider contract: zero-retention, no-training, region selection | Legal + Eng | **Blocks first production call** |
| Sub-processor list update + customer notice/objection window | Legal + CS | **Blocks launch.** Longest lead time in the plan — start week 1 |
| Text extraction service (see A7) | Eng | Blocks Area 1; may already exist for search |
| Digest template + plain-text part | Eng/Design | Blocks Area 3 |
| Baselines: digest open, unsubscribe, 48h re-engagement | Data | **Blocks evaluation, not the build.** Capture before launch or the guardrails are undefined |

| Risk | Mitigation |
|---|---|
| Injected content reaches a user's inbox from your domain | Area 2 in full: isolation, metadata stripping, plain-text-only output, output scanning, adversarial CI suite, quarantine alerting |
| Summary is plausible but omits the one material clause | Faithfulness sampling with a pass bar; AI label; source link adjacent to every summary; hide control |
| Digest gets noisier and unsubscribes rise | Hard budget; unsubscribe guardrail as an auto-rollback trip-wire; user-level off switch |
| Cost scales with uploads, not with value | Eligibility gate before the model call; per-tenant caps; length ceiling |
| Summary leaks to a recipient without document access | ACL re-check at send time, per recipient |
| We build it and nothing changes | §6 — the cheap probe that should have run first |

### 4.7 Edge Cases

*Non-obvious only. Standard upload/email behaviour is unchanged and unspecified by design.*

| Scenario | Behavior |
|---|---|
| Document deleted after summarising, before the digest sends | Summary deleted with the document; row absent from the digest entirely |
| Document replaced mid-week | Summarise the latest version; digest says "updated," not "added"; prior summary retained for audit, not rendered |
| Document access revoked between generation and send | Not rendered — ACL is evaluated at send time, per recipient |
| Recipient has summaries off, uploader has them on | Summary exists and is stored; simply not rendered for that recipient. Gating is per-recipient, not per-document |
| Tenant switch flipped off after summaries exist | Stop generating immediately; stop rendering immediately; [NEEDS INPUT: purge existing summaries, or retain? Legal call — default to purge] |
| Document exceeds the page ceiling | `not_eligible`, reason `too_long`. Do not chunk-and-reduce in v1 — a partial summary of a long document is the most dangerous output the feature can produce |
| Scanned PDF with no text layer | `not_eligible`, reason `no_text_layer`. No OCR in v1 |
| Password-protected or corrupt file | `not_eligible`. No model call |
| Document not in the recipient's digest language | Summarise in the **document's** language in v1; do not translate. Flagged in §5 |
| 14 documents uploaded in one batch | Budget rule applies; top 3 per project summarised in the digest, remainder as a filename list with a count |
| Zero eligible documents this week | Digest renders exactly as today. No AI section, no empty state |
| Model provider outage all week | All jobs `failed` after retries; digest is byte-identical to today's. **No user-visible signal.** Alert fires internally |

### 4.8 Open Questions

**Legal / Privacy**
1. Does Art. 50 disclosure bind us for a private digest to project members, or is the label purely a product choice? (We label either way.)
2. Do current DPAs use general authorisation with an objection window? How long is the clock?
3. On tenant opt-out after summaries exist: purge or retain?

**Product / Commercial**
4. Tenant default: on or off? On maximises adoption and maximises the number of admins who discover it after the fact.
5. Do EU-residency tenants ship in v1 or wait for a regional endpoint?

**Design**
6. Does the two-line summary replace the filename row or sit beneath it? Mobile width decides this, not desktop.
7. What does the AI label look like such that it's honest but not alarming?

**Data**
8. Current digest open, unsubscribe, and 48h re-engagement baselines — needed *before* launch.
9. Distribution of eligible uploads per user per week, to validate or kill A6 and size the budget rule.

**Engineering**
10. Does text extraction already exist for search? (A7 — worth roughly a third of P0 effort.)
11. Page/token ceiling for eligibility — proposed 50 pages.

### Appendix

- Prompt spec and `prompt_version` history — [link]
- Golden evaluation set and rating rubric — [link]
- Adversarial injection test corpus — [link]
- Tracking plan — [link]
- Digest template designs — [link]

---

## 5. Backlog generated by this PRD

**v1.1 candidates:** project-level opt-out (expect this to be the first enterprise ask); on-demand re-summarisation; summary in the document list view and in search results; summarise-into-recipient-language.

**Deferred, needs its own PRD:** project-level weekly narrative roll-up (A4 — the most likely "obvious next step," and it is a different pipeline with different failure modes); OCR for scanned documents; spreadsheet summarisation, which needs structure-aware handling, not text summarisation.

**Engineering debt to register now:** golden-set maintenance owner; prompt-version rollback path; a documented procedure for mass-purging summaries on a tenant's request.

---

## 6. The probe that should run before, or alongside, the build

Risk 1 is that nobody wants this, and it's the only one the PRD can't retire. Two weeks, no pipeline:

Take 30 real documents from 10 consenting tenants. Write summaries **by hand**. Paste them into next week's digest for those users only. Measure the 48h re-engagement delta and — more importantly — read the replies.

Hand-written summaries are the ceiling: strictly better than anything the model will produce in v1. **If the ceiling doesn't move the metric, the model won't either**, and you've saved a quarter of engineering plus a permanent LLM line item. This costs about a day of someone's writing time and is the highest-leverage thing in this document.

---

## 7. Converting this to AI-Build

Per the skill's conversion table, Dev-Team → AI-Build adds: full acceptance criteria per requirement (Given/When/Then), explicit state and flow logic for the pipeline's happy and error paths, a data model, design direction and per-screen UI description, a comprehensive error-handling matrix, and — if the builder runs autonomously — hold points. For this feature I'd place hold points at: **HP-1** after the eligibility gate and extraction, before any model call is wired; **HP-2** after the adversarial injection suite passes, before the digest surface is enabled; **HP-3** before the first send to real users.

To generate it I'd need what §4.8 Q10 and the A-series don't answer: stack, existing services, and design system.

---

## Stress Test

**Weakest part of this analysis.** The problem statement is a hypothesis dressed in a narrative. Maya is invented. I have no interview, no ticket, no metric showing documents go unread. Every number in §4.1 is a blank or a structural bar, because I refused to fabricate targets — which is correct, and also means this PRD cannot yet justify its own cost. §6 exists because of this.

**Assumptions most likely to be wrong.**
- **A4** (per-document, not roll-up) is a coin flip on your phrasing. If you actually wanted "tell me what happened in my project this week, informed by the documents," this is the wrong PRD and the right one has a different pipeline.
- **A1.** If the digest already shows a first-page excerpt, the marginal gain of an LLM summary over `head(text, 200)` is much smaller than it feels — and an extractive excerpt cannot hallucinate, cannot be injected, and needs no sub-processor.
- **A6.** I designed the budget rule as a guardrail. If heavy weeks are the norm rather than the tail, compression *is* the product and §4.5 area 3 should be the first thing designed, not the third.

**What a smart critic says.**
1. *"You've turned a one-line feature into a legal project."* Partly fair — but the sub-processor clock and the injection surface are real and neither goes away by being ignored. The honest version: **the LLM call is a week of work; the consent surfaces, the off-switches, and the safety scanning are the other eight.** Anyone quoting this at two weeks has not read §4.4 or §4.5 area 2.
2. *"Extractive beats abstractive here."* Strong argument. For a two-line triage blurb, the first substantive sentence of a document is often as decidable as a generated summary, at zero marginal cost and zero hallucination risk. I did not build this comparison into the plan and I should have — **add extractive-baseline as an arm of the §6 probe.** If it ties, the LLM loses on cost, latency, and risk.
3. *"Your primary metric is unfalsifiable."* Also fair. 48h re-engagement will drift for a dozen reasons unrelated to this feature. Absent a holdout, the guardrails are doing more real work than the primary metric — treat the unsubscribe trip-wire as the decision-grade signal and hold out 10% if you can.
4. *"Quarantining on any URL will over-trigger."* Probably true — legitimate summaries of documents about websites will get caught. I accept the false-positive rate because the failure mode is invisible (user sees today's digest) while the false-negative mode is brand-authenticated phishing. Revisit once the quarantine-rate dashboard has data.

**What would change my recommendation.** Evidence that users skip documents for lack of *time* rather than lack of *information*. If that's the case, no summary helps, and the money belongs in notification targeting instead.

---

**Sources**

- [The EU AI Act's Transparency Rules: A Practical Guide to Article 50](https://artificialintelligenceact.eu/transparency-rules-article-50/)
- [EU AI Act: Transparency Obligations Take Effect 2 August 2026 — Cooley](https://www.cooley.com/news/insight/2026/2026-08-03-eu-ai-act-transparency-obligations-take-effect-2-august-2026)
- [Transparency obligations under Article 50 of the AI Act — European Commission](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act)
- [Subprocessors under GDPR: Legal obligations and requirements](https://complydog.com/blog/subprocessors)
- [The SaaS DPA Guide: GDPR Requirements, Subprocessors, and Automation](https://secureprivacy.ai/blog/data-processing-agreements-dpas-for-saas)
- [Prompt-in-Content Attacks: Exploiting Uploaded Inputs to Hijack LLM Behavior (arXiv 2508.19287)](https://arxiv.org/html/2508.19287)
- [Indirect Prompt Injection: The Complete Guide — NeuralTrust](https://neuraltrust.ai/blog/indirect-prompt-injection-complete-guide)
- [What is prompt injection? Example attacks, defenses and testing — Evidently AI](https://www.evidentlyai.com/llm-guide/prompt-injection-llm)
- [A review of faithfulness metrics for hallucination assessment in LLMs (arXiv 2501.00269)](https://arxiv.org/abs/2501.00269)
- [A framework to assess clinical safety and hallucination rates of LLMs for medical text summarisation — npj Digital Medicine](https://www.nature.com/articles/s41746-025-01670-7)

---

*Output format: Markdown. A Word version via the `docx` skill is available on request.*
*Iteration commands: "Go deeper on [section]" · "Challenge [section]" · "Simplify" · "Add alternatives" · "Rate it"*
