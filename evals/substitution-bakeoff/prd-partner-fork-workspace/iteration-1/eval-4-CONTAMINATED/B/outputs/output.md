# PRD — Document Summaries in the Weekly Digest

**Skill:** `prd-partner` · **Mode:** PRD Mode → **Dev-Team** output
**Extends:** *PRD — Weekly Project Digest Email (Dev-Team)*, status Approved for build
**Date:** 2026-09-16 · **Owner:** Product · **Eng lead:** TBD

---

## 0. How I ran this, and the one thing I'd change about the request

The skill routes a solution-shaped, under-specified request to **Discovery Mode** first. This
session is unattended, so I ran the discovery agenda on paper against the approved parent
spec rather than through conversation, recorded the synthesis and the assumptions below, and
then generated the PRD. Every place I would have asked a question is either an explicit
assumption (**[A-n]**) or a flag (**[NEEDS INPUT]**). Nothing is invented silently.

**Push-back, before the PRD.** The request names a mechanism ("auto-summarise with an LLM"),
not a problem. The parent spec already has the problem: *~40 tickets/month of "I didn't know X
changed," and 3+ project owners log in 2.1x/week vs 4.4x.* Read against that, the digest's job
is **triage** — helping someone decide *whether to open the thing* — not comprehension. That
reframe is load-bearing and it changes the build:

- A faithful abstract of a 40-page document is the wrong artefact. Three lines answering
  "what is this and is there anything I should react to" is the right one.
- It sets the quality bar: a summary is good when the click-or-skip decision it produces
  matches the one the user would make after opening the document. Not when it is complete.
- It caps length. The parent spec's guardrail is `<0.5% unsubscribe per send`. Summaries make
  the email longer, which is the most plausible way this feature makes the digest *worse*.

I have written the PRD to that framing. If the real goal was "let users read documents without
opening them," this is the wrong spec and the scope roughly triples.

---

## 1. Discovery Synthesis

> **Problem:** Multi-project owners can't tell from the digest whether a newly added document
> matters to them, so the line "4 items added" gets skipped and the change is missed.
> **User:** Owners and members of 3+ active projects who already receive the weekly digest.
> **Core insight:** The summary's job is triage, not comprehension — three lines that support
> a click-or-skip decision, not an abstract.
> **Scope boundaries:** Uploaded documents only; summary generated at upload, not at send;
> read-only surface in an existing email; no chat, no diffing, no translation.
> **Riskiest assumption:** That summary quality is the binding constraint on click-through —
> rather than the digest simply not being read, or documents being a small share of events.
>
> **PRD readiness: 7/10.** The parent spec supplies the problem, the audience, the baselines,
> the data model and the rollout pattern, which is unusually strong footing. Held back from 8+
> by two unknowns that only instrumentation answers: the document share of digest events, and
> whether our DPA permits an LLM sub-processor without a customer notice cycle.
>
> **Risks:**
> 1. **Sub-processor notice is on the critical path** (blocks launch, not build). Adding an LLM
>    that processes customer documents is a sub-processor change. GDPR Art. 28(2) requires the
>    controller be informed and given a genuine opportunity to object *before* processing
>    starts; the Regulation sets no number of days — the DPA does, market-standard ~15 days,
>    with AI sub-processors trending to 30-day cycles. This is weeks of calendar time that no
>    amount of engineering compresses. **Start it in week 1, not at launch.**
> 2. **Length hurts the guardrail** (resolvable during build). Longer email, `<0.5%` unsubscribe
>    ceiling. Mitigated by hard caps (DS-5) and a control arm in rollout.
> 3. **Wrong summary is uncorrectable in email** (resolvable during build). Sent mail can't be
>    edited. Mitigated by a pre-rollout accuracy gate (DS-9) and an in-app correction path.
> 4. **Documents may be a small share of "items added"** (blocks the business case, not the
>    build). If documents are 5% of events, the ceiling on this feature is 5% of the digest's
>    click-through. **[NEEDS INPUT: document share of `project_events` over a trailing quarter.]**
>    This is one query and it should be run before engineering starts.

**Assumption register**

| ID | Assumption | If wrong |
|----|-----------|----------|
| A-1 | Audience is the same engineering team that owns the parent Dev-Team spec, so this is a Dev-Team extension. | Convert per the delta in Appendix C. |
| A-2 | Uploaded documents are a kind of project item and an upload already emits a `project_events` row. | Eng must add the event type; +1 sprint, changes DS-1. |
| A-3 | Text extraction (PDF/DOCX → text) does not exist today. | If it exists, drop that dependency and OCR scope. |
| A-4 | A document is visible to every member of its project (no per-document ACL). | DS-7 becomes a hard blocker, not a safeguard. |
| A-5 | We can commit to a no-training, short-retention LLM provider under our existing security posture. | Feature may require self-hosted inference; cost and timeline change materially. |

---

## 2. Context

**TL;DR.** The weekly digest tells users a document was added but not whether it matters, so
they skip it. We generate a short triage summary when a document is uploaded and render it
beneath that project's line in the digest.

**Why now.** The digest is approved and about to establish its engagement baselines. Adding
summaries after those baselines are set means we can measure the lift against a control arm
instead of guessing — and the summary store we build is reusable by search and the document
list later.

**The narrative.** Maya owns five projects and logs in twice a week. Monday 08:00 her digest
shows *Acme Rebrand — 4 items added.* Today she skims past it. After this ships, one of those
four carries a line: *"Vendor_MSA_v3.pdf — Master services agreement with Kinetic Logistics.
24-month term, $2M liability cap, 60-day termination clause. Signature block is unsigned."*
She clicks through, because now she knows it is the contract she has been waiting on.

**Success metrics**

| Type | Metric | Target |
|------|--------|--------|
| Primary | Digest → product click-through, summarised arm vs. control | **≥2pp absolute lift** over the control arm's rate at the same point in rollout |
| Primary | Click-through on document items specifically | Baseline **[NEEDS INPUT: document-item CTR from the first 4 weeks of digest sends]**; target set from the 10% arm |
| Secondary | "I didn't know X changed" tickets attributable to documents | Down from **[NEEDS INPUT: document share of the ~40/month]** |
| Guardrail (inherited) | Unsubscribe rate per send | Stays `<0.5%` — a breach in the summarised arm rolls the feature back |
| Guardrail (inherited) | Open rate | Stays `≥35%` |
| Quality gate | Material inaccuracy rate, human-rated, n=100 sample | `≤5%` before the 10% arm opens |
| Cost | LLM spend per 1,000 summarised documents | Under **[NEEDS INPUT: monthly budget ceiling from Finance]** |

I have deliberately not invented a click-through target. The parent spec's `≥8%` is a
whole-digest figure; the honest bar for this feature is "beats its own control arm," and the
absolute number comes from the 10% cohort.

## 3. Personas

| Persona | Description |
|---------|-------------|
| **Multi-project owner** | Owns 3+ active projects, logs in ~2.1x/week, is the digest's existing target. Reads the digest on a phone, in the first ten minutes of Monday. Wants to know what to open. |
| **Project member** | Belongs to projects they don't own; often the person who uploaded the document. Their interest is the inverse: that colleagues notice what they added. |

## 4. Scope

**Goals**
- A short triage summary for each newly uploaded document, generated at upload.
- That summary rendered under its project in the weekly digest, in HTML and plaintext.
- A correction path, so a wrong summary can be reported and the quality metric has a source.

**Non-goals** *(and why)*
- Summarising non-document events (comments, membership) — different problem, different prompt.
- Version diffing ("what changed since v2") — the highest-value follow-on, but it needs a
  version model we don't have. v1.1.
- Chat or Q&A over documents — a product, not a digest line.
- Translation and non-English summarisation — v1 detects and skips; see DS-8.
- Re-summarising a document the uploader already described in a title or comment.
- Real-time or per-upload notification — explicitly out of the parent spec's scope.

## 5. Domain & Regulatory Context

| Area | Requirement / best practice | Impact on this feature |
|------|------------------------------|------------------------|
| Sub-processor change (GDPR Art. 28(2)) | Controller must be informed of the intended change and given a genuine opportunity to object *before* the new sub-processor begins processing. No statutory period; the DPA sets it. Market standard ~15 days; AI sub-processors trending to 30-day cycles. | **Launch blocker.** Publish the notice and run the objection window before the first production document is sent to the provider. Owner: Legal. Start week 1. |
| Purpose limitation / provider terms | Provider must be contractually barred from training on our customers' content, with defined (ideally zero) retention. | Gate on A-5. Record the commitment in the sub-processor entry. |
| International transfer | If the provider processes outside the EEA, a valid transfer mechanism is required. | **[VERIFY WITH COUNSEL]** — do not assert a position in the PRD. |
| Special-category data | Uploaded documents may contain health, HR or financial data the user never intended to route through a third party. | Drives DS-6 (per-project summary opt-out) and DS-11 (no summary content in logs). |
| Content-in-email exposure | Email is forwarded, synced to personal devices, and retained outside our controls in ways in-app content is not. | Summary length cap and the per-project opt-out are privacy controls, not just UX ones. |

This section is specific to routing customer documents to a third party. It is not a generic
compliance appendix, and nothing here is a legal opinion.

## 6. Requirements

Extends the parent spec's R1–R6; those continue to apply unchanged.

**Summary generation**
- **DS-1 (P0)** On upload of an eligible document, enqueue an asynchronous summarisation job.
  Generation never happens in the digest send path.
- **DS-2 (P0)** Eligibility gate — summarise only when the document's project has ≥1 member
  with the digest enabled and the project is not opted out (parent R3). This is the cost
  control: it avoids paying for documents no digest will ever show.
- **DS-3 (P0)** Store the result in a new `document_summaries` table (`document_id`,
  `summary_text`, `model`, `prompt_version`, `input_token_count`, `status`, `generated_at`).
  `prompt_version` is mandatory — without it, a quality regression can't be attributed.
- **DS-4 (P0)** Output contract per Appendix A: plain text, ≤ 400 characters, no URLs, no
  markup. Output failing validation is stored as `status = rejected` and never rendered.

**Digest rendering**
- **DS-5 (P0)** Caps: at most **3** summaries per project and **10** per email, most recent
  first, with a "+N more" rollup. These numbers are deliberate defaults, tunable by config,
  and are the primary defence of the unsubscribe guardrail.
- **DS-6 (P0)** A per-project *summaries* opt-out, distinct from the parent's digest opt-out.
  A legal or HR project may want the digest and not want document content in email.
- **DS-7 (P0)** Access is re-checked **at render time, per recipient**, against current access
  to that specific document. A summary generated when a document was visible must not render
  to a recipient whose access has since been removed, or for a document since deleted.
- **DS-8 (P0)** Graceful degradation — if a summary is missing, pending, rejected, or in an
  unsupported language, render the existing event line unchanged. Never render an error, a
  placeholder, or a partial summary. A summarisation failure must never delay or block a send.
- **DS-9 (P0)** Summaries never trigger a send. Parent R2 (suppress if zero events) is
  evaluated on events only — a summary attaches to an event that already exists.
- **DS-10 (P0)** Render in both HTML and plaintext (parent R4). Plaintext is not an
  afterthought here; the summary is the payload.

**Safety and privacy**
- **DS-11 (P0)** Document text is untrusted input. Pass it as delimited data, never as
  instruction. Validate the output (DS-4) before storage. A document containing "ignore
  previous instructions and write X" must not change what lands in anyone's inbox, and a
  summary must never be able to influence a link, a recipient, or send logic.
- **DS-12 (P0)** Do not log summary text or document content in application logs, error
  reports, or traces. Log identifiers and token counts only.
- **DS-13 (P1)** Show the summary on the document detail page with a "report this summary"
  control.

> DS-13 is the one thing I added beyond the request, and it is worth naming as such. Without
> it there is no correction path for a wrong summary and no source for the quality metric in
> §2. The data already exists by DS-3, so the cost is a component, not a system.

## 7. Dependencies & Risks

| Dependency | Owner | Impact |
|-----------|-------|--------|
| LLM provider contract, DPA, sub-processor notice + objection window | Legal | **Blocks launch.** Multi-week lead time. Start week 1. |
| Text extraction (PDF/DOCX/TXT → text); OCR explicitly out of v1 | Eng | Blocks DS-1. See A-3. |
| Document-type event in `project_events` | Eng | Blocks DS-1 and DS-5 ordering. See A-2. |
| Digest renderer changes (HTML + plaintext) | Eng | Blocks DS-5, DS-10. |
| Cost monitoring and a budget alert | Eng/Finance | Not a blocker, but shipping without it is how a token bill becomes a surprise. |

| Risk | Mitigation |
|------|-----------|
| Longer email raises unsubscribes past 0.5% | Caps (DS-5); control arm in rollout; roll back on breach. |
| Hallucinated summary, uncorrectable once sent | Accuracy gate before the 10% arm (§2); DS-13 correction path; triage framing keeps claims shallow and checkable. |
| Cost scales with uploads, not with digests | Eligibility gate (DS-2); input token cap (Appendix A); budget alert. |
| Prompt injection via document content | DS-11. Treat as a standing control, not a one-time test. |
| Documents are a small share of events, capping the upside | Run the share query **before** engineering starts. This is the cheapest kill-decision available. |

## 8. Edge Cases

| Scenario | Behavior |
|----------|----------|
| Scanned PDF with no text layer | Ineligible in v1. No summary, no error. Log for OCR demand sizing. |
| Document over the input token cap | Head + tail sampling per Appendix A; summary marked `truncated`; still rendered. |
| Encrypted / password-protected file | Ineligible. Never attempt to open. |
| Document deleted between upload and Monday send | DS-7 drops it at render time. |
| Document replaced with a new version before send | Summarise the version current at render time; if its summary is not ready, DS-8 applies. |
| Same file uploaded to two projects | Summarise once, keyed by content hash; render in both. |
| Non-English document | v1 detects and skips (DS-8). Do not emit an English summary of a German contract. |
| Provider outage on Monday | No effect — generation is decoupled from send (DS-1). This is the main reason for that choice. |
| Zero-byte or corrupt file | `status = failed`, no render, no retry loop beyond 3 attempts. |
| User opted out of summaries mid-week | DS-6 is evaluated at render time, so the opt-out takes effect on the next send. |

## 9. Rollout

Mirror the parent spec, with a control arm added: internal dogfood week 1; accuracy gate
(n=100, ≤5% material inaccuracy) before opening the 10% arm; week 2 the 10% cohort splits
summarised vs. control so the lift in §2 is measurable; full rollout week 4 only if the
unsubscribe and open-rate guardrails hold in the summarised arm.

## 10. Open Questions

**Legal** — What notice period does our current DPA set for sub-processor additions, and does
it distinguish AI sub-processors? Does the shortlisted provider process outside the EEA?

**Eng** — Does text extraction exist (A-3)? Does an upload emit a `project_events` row (A-2)?
Is there a per-document ACL below project membership (A-4)?

**Data** — What share of `project_events` are document uploads? What is document-item
click-through in the digest's first four weeks?

**Product** — Are caps of 3/project and 10/email right, or should ordering be by predicted
relevance rather than recency? (Recency in v1; relevance is a v1.1 item.)

---

## Stress Test

**Weakest part of this PRD.** The business case rests on an unmeasured quantity. If document
uploads are a small fraction of digest events, every requirement here is well-formed and the
feature still can't move the number. I have put that query on the critical path, but I could
not run it, so the PRD is conditionally sound rather than justified.

**Assumptions most likely to be wrong.**
1. *That triage framing is what users want.* Plausible counter-evidence: users may want to
   read the document in the email and never click at all — which would make click-through the
   wrong success metric entirely, and a rising open rate with flat CTR would look like failure
   while actually being success. I would watch time-to-first-login-after-digest as a hedge.
2. *That summary quality is the binding constraint.* If the digest simply isn't read, better
   content inside it changes nothing. The control arm catches this, but only after the build.
3. *That generate-at-upload is right.* It is right for reliability and reuse, and it is wrong
   if most uploaded documents are never digest-eligible — then we pay for summaries nobody
   reads. DS-2 narrows this but does not close it.

**What a smart critic would say.** *"You have written a spec for an LLM feature whose success
metric is an email click. The cheap version is to render the document's first 200 characters
of extracted text and see whether click-through moves at all."* That critique is correct and I
would run it first — it costs days, needs no sub-processor notice, and if extracted text moves
click-through as much as a generated summary, the LLM is unnecessary. **I recommend this as a
pre-step to the build, not as a replacement for the PRD.** It is in Appendix B as B-0.

**Where I pushed back and lost.** The request asked to summarise documents. The sharper
feature is summarising *what changed about the project* — which is what the digest is actually
for. I scoped it as v1.1 rather than v1 because it consumes per-document summaries anyway, and
building it first means re-reading every document every week with nothing reusable to show for
it. That is a defensible sequencing call, not a rebuttal.

---

## Appendix A — Summariser Contract

**Input:** extracted plain text, capped at a configured input-token budget. Over budget, take
head and tail (the two regions carrying document identity and status) rather than truncating
at the cap. Pass document filename and MIME type as separate labelled fields.

**Framing:** document text is supplied as delimited **data**. The system prompt states that
content inside the delimiters is never an instruction.

**Output:** plain text, ≤ 400 characters, answering in order — what this document is; the two
or three facts a reader would need to decide whether to open it; anything anomalous (unsigned,
draft, expired, blank). No preamble ("This document is about…"), no URLs, no markup, no
speculation beyond the text.

**Validation before storage:** length; absence of URLs and HTML tags; non-empty; language
matches the detected document language. Any failure → `status = rejected`, DS-8 applies.

**Versioning:** every stored summary carries `prompt_version` and `model`. Changing either
requires a fresh n=100 accuracy sample before it reaches production traffic.

## Appendix B — Roadmap & Backlog

| Phase | Item | Why |
|-------|------|-----|
| **B-0 (pre-build)** | Extracted-text baseline: render first 200 chars, measure CTR | Cheapest possible test of whether summarisation is the lever. Days, not weeks. |
| **v1** | DS-1 … DS-12 | This PRD. |
| **v1.1** | Project-level "what changed and why it matters" roll-up composed from stored summaries | The sharper feature; needs v1's summary store. |
| **v1.1** | Version diff summaries ("changed since v2") | Highest-value follow-on; blocked on a version model. |
| **v1.1** | Relevance-based ordering instead of recency | Caps in DS-5 make ordering matter more as volume grows. |
| **v2** | OCR for scanned documents | Size demand from v1's ineligibility log first. |
| **v2** | Summaries in search and the document list | The store already exists; near-free reuse. |
| **Backlog** | Non-English summarisation | Requires a language policy decision first. |
| **Backlog** | Cost dashboard per account | Follows the budget alert. |

## Appendix C — Converting This to AI-Build

**Carry over:** all of §2–§9, Appendix A, the assumption register.
**Add:** per-requirement Given/When/Then acceptance criteria; state and flow logic for the
generate → validate → store → render path with every error branch; the `document_summaries`
migration written out; design direction for the email block in HTML and plaintext; an ADR
recording that generate-at-upload and per-document (not per-project) summaries were chosen
deliberately, so a builder does not "improve" back toward the rejected shapes; hold points at
schema, first generated summary, and pre-send render.
**Remove:** nothing — AI-Build expands rather than cuts.

## Appendix D — Sources

- [GDPR Subprocessor Change Notices: The Article 28 requirements](https://www.orbiqhq.com/trust-center/gdpr-subprocessor-change-notices)
- [Subprocessor Management Under GDPR Article 28](https://www.orbiqhq.com/eu-regulations/subprocessor-management-gdpr-article-28)
- [Microsoft's DPA update cuts AI subprocessor notice to 30 days](https://ppc.land/microsofts-dpa-update-cuts-ai-subprocessor-notice-to-30-days/)

Notice periods are contractual, not statutory. The figures above are market context for
sizing the timeline — our own DPA governs, which is why it is the first open question.

---

## Closing Hook — Skill Improvement Notes

Accumulated while running `prd-partner` on this task:

1. **No unattended path.** Discovery Mode ends at "do not proceed until Omri has reviewed the
   risk assessment," which has no defined behaviour when the session cannot ask. Worth adding
   an explicit rule: when input is unavailable, convert every question into a numbered
   assumption, put the register directly above the PRD, and proceed.
2. **Mode detection ignores existing artifacts.** The strongest signal for output mode here was
   that the parent spec is labelled Dev-Team. The skill infers audience from the conversation;
   it should check for a predecessor document first.
3. **"Don't invent metrics" needs a positive instruction.** The skill says don't invent
   targets, but the template has a Targets column. The useful rule is: state the metric, the
   baseline source, and the ship bar — and let the absolute target come from the first rollout
   cohort.
4. **Guardrail metrics have no home in the Dev-Team template.** Success Metrics is
   single-directional. Inherited guardrails like `<0.5% unsubscribe` are what actually kill
   features; the table should have a type column that includes them. (Used one here.)

Apply any of these to `prd-partner/SKILL.md`? Larger items (1 and 2) are skill-structure
changes worth logging to the backlog rather than patching inline.
