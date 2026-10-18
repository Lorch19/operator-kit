# Linx Claude Code Brief
**Version:** 1.0 | **Last updated:** 2026-10-18  
**Purpose:** Paste this entire file into Claude Code running on your Linx account (where Notion MCP connectors are available). Claude Code will build 3 skills in sequence, stopping for your validation at each checkpoint before continuing.

---

## Context: Who You Are & What Linx Does

You are working for **Omri Lorch**, PM at **Linx Security** — an AI-native identity security & governance platform. Series A ($33M), ~60 people, founded by Israel Duanis (CEO) and Niv Goldenberg (CPO). Customers include Peloton, Wiz, Aramark, Discount Tire.

**Linx's platform** covers: Risk Visibility (ISPM), AI-Powered Remediation (Autopilot, launched March 2026), Governance & Policy, Access Approvals, JIT Access (roadmap), Compliance & Reporting (roadmap), Identity Lifecycle (roadmap), NHI + Agentic Identity Governance (live, key differentiator).

**Strategic narrative:** AI-native from core (not bolted on). Graph-based, agentless. Unified coverage across human identities, non-human identities (service accounts, API keys, bots), and agentic AI identities. The bet: move from periodic access reviews to continuous autonomous governance.

**Omri's background:** 6 years at Payoneer (KYC/Risk/Compliance/Account Security), Head of Product at Cedar Money (fintech), MBA Tel Aviv. Identity security is a newer domain for him — bridge IAM jargon when needed.

---

## What You Will Build

Three skills, in this exact order:

1. **`linx-security-domain-context`** — Foundation skill. Loaded at session start to give Claude Code Linx-specific context: glossary, product positioning, competitive landscape, buyer personas, market data, compliance frameworks. Other Linx skills depend on this one.

2. **`prd-partner` overlay** (`linx-prd-partner`) — Extends the generic `prd-partner` skill with Linx-specific additions: security/compliance PRD sections, identity security domain terminology, CISO/Security Architect/SOC Analyst/GRC Manager personas.

3. **`competitive-teardown` overlay** (`linx-competitive-teardown`) — Extends the generic `competitive-teardown` skill with identity security scoring dimensions, pre-built competitor stubs for all 8 major competitors, and Linx-specific positioning analysis.

---

## Execution Instructions

**Work sequentially.** Build Skill 1 → checkpoint → Skill 2 → checkpoint → Skill 3 → checkpoint. Do not skip ahead.

**File locations:** All skills go in a `/skills/` directory relative to wherever this brief is opened. If a `/skills/` directory doesn't exist, create it.

**Notion MCP:** Use Notion MCP connectors to pull any available Linx documentation, product wiki pages, or competitive intel before writing each skill. Prefer Notion data over training knowledge for anything company-specific. If Notion data is unavailable for a section, write `[NEEDS NOTION: <what to pull>]` as a placeholder.

**Quality bar:** Each skill should be 150–300 lines. Well-structured sections with headers. Actionable enough that Claude Code can execute without asking clarifying questions. Specific enough to Linx that a generic PM framework wouldn't produce equivalent output.

**Do not ask questions during execution.** Make judgment calls. Flag uncertainties inline with `[NEEDS INPUT: <question>]`. Keep moving.

---

## Checkpoint Protocol

At each checkpoint:
1. Print a summary of what was built (skill name, line count, sections included, Notion pages consulted)
2. Print the 3 test scenarios below and your expected outputs for each
3. Print: `**CHECKPOINT [N] COMPLETE. Review above and type CONTINUE to proceed or REVISE [section] to fix.**`
4. Wait for Omri's response before starting the next skill

---

## Skill 1: `linx-security-domain-context`

**File:** `/skills/linx-security-domain-context/SKILL.md`

**Purpose:** Foundation context layer. Loaded at session start. Gives Claude Code everything it needs to reason about Linx's domain, market, and competitive position without asking background questions.

**Frontmatter:**
```yaml
---
name: linx-security-domain-context
description: >-
  Foundation context for all Linx product work. Loads domain knowledge, 
  glossary, competitive landscape, buyer personas, and market data.
  Load this first at the start of every Linx Claude Code session.
  Updated: 2026-10-18
type: context
depends_on: []
---
```

**Sections to include:**

### 1. Identity Security Glossary
Define these terms precisely as Linx uses them (check Notion for Linx-specific definitions; fall back to industry standard if not found):
- IGA (Identity Governance & Administration)
- ISPM (Identity Security Posture Management)
- NHI (Non-Human Identity)
- PAM (Privileged Access Management)
- JIT (Just-in-Time) Access
- Agentic Identity
- Joiner/Mover/Leaver (JML) lifecycle
- Access Review / Certification
- Entitlement
- RBAC / ABAC
- SOD (Segregation of Duties)
- Service Account
- Kill Switch (in Linx's Autopilot context)
- Continuous Governance (vs. periodic)
- Graph-based identity (what this means architecturally)
- Agentless (what this means for Linx's deployment model)

### 2. Product Platform (Current State)

Build a table with these columns: Capability | Status | Market Gap | Linx's Approach

Capabilities to cover:
- Risk Visibility (ISPM)
- AI-Powered Remediation (Autopilot)
- Governance & Policy
- Access Approvals & Workflows
- JIT Access
- Compliance & Reporting
- Identity Lifecycle (Joiner/Mover/Leaver)
- NHI + Agentic Identity Governance

Pull current status from Notion. If unavailable, use: Live = confirmed in onboarding, Roadmap = planned, Building = in progress.

### 3. Strategic Narrative (Internalize)

Three core narratives Claude must internalize and use when reasoning about Linx's strategy:

**Narrative 1: Agentic identity as a first-class governance problem**
Three specific risks: sequential risk (benign actions form dangerous chains), compound access (agents autonomously expand permissions), delegation context loss (IAM sees fragments, misses the orchestrator). Linx's answer: treat decision sequences as first-class security objects.

**Narrative 2: JIT access from humans to agents**
4-layer model: visibility → policy/decision → intelligence → fulfillment/audit. Agents are distinct identities (not service account wrappers). Agents cannot self-escalate. Kill-switch tied to anomaly detection.

**Narrative 3: Autopilot = autonomous but guardrailed**
Continuous monitoring + contextual risk evaluation + autonomous action OR human escalation. The trust barrier: CISOs are skeptical of "autonomous" — guardrails are the answer (confidence × risk matrix, progressive autonomy, full audit trails).

### 4. Buyer Personas

Build detailed profiles for each persona. Pull from Notion if available:

**CISO**
- Title variations: CISO, VP Security, Head of Information Security
- Company stage: Series B+ / 200+ employees (typically)
- Primary pain: Risk accumulation outpaces governance capacity. Quarterly certifications = rubber stamps. NHI blind spots.
- Buying trigger: Audit finding, security incident, board pressure post-breach in similar company, compliance mandate
- What they measure success by: Risk reduction (quantified), audit pass rate, MTTR for access anomalies
- Language they use: "Attack surface," "blast radius," "zero trust," "compliance posture"
- Skepticism to address: AI autonomy ("we can't have a machine making security decisions without oversight")
- Linx angle: Autopilot with guardrails. Progressive autonomy. Full audit trail. Kill switch.

**Security Architect**
- Primary pain: Can't enforce policy across the sprawl. Every new tool = new identity silo.
- Buying trigger: Cloud migration, M&A integration, new compliance requirement
- What they measure success by: Policy coverage, integration breadth, time-to-enforce
- Language they use: "Posture," "policy enforcement," "identity fabric," "graph"
- Linx angle: Agentless, graph-based. Unified across human + NHI + agentic.

**SOC Analyst**
- Primary pain: Alert fatigue. Can't tell signal from noise on identity events. No context to investigate.
- Buying trigger: Too many tickets, SLA misses on access reviews, incident where identity was the vector
- What they measure success by: Alert fidelity, investigation time, false positive rate
- Language they use: "Noise," "context," "enrichment," "SIEM correlation"
- Linx angle: Graph context enriches every alert. Autopilot handles low-confidence remediations. Analyst focuses on real escalations.

**GRC Manager**
- Primary pain: Manual evidence collection for audits. Can't demonstrate continuous compliance.
- Buying trigger: Upcoming SOC 2 / ISO 27001 / FedRAMP audit, failed audit, new compliance requirement
- What they measure success by: Audit pass rate, evidence collection time, control coverage
- Language they use: "Controls," "evidence," "continuous compliance," "frameworks"
- Linx angle: Continuous governance = continuous compliance. Evidence auto-generated from audit trail.

### 5. Competitive Landscape

Full table with: Competitor | Position | Recent Moves | Linx's Edge | Threat Level (Low/Med/High/Critical)

Competitors (pull latest intel from Notion; fall back to onboarding data):
- SailPoint
- ServiceNow/Veza ($1B acquisition, March 2026)
- CyberArk (acquired Zilla $175M + Venafi $1.54B)
- ConductorOne ($111M raised)
- Lumos ($35M Series B, "Albus" multi-agent IGA)
- Opal Security ($32M Series B)
- Zluri (Identity Security Platform launch, March 2026)
- Saviynt (IGA+PAM, regulated industries)

### 6. Market Data

Pull from Notion. If unavailable, use:
- IGA market: ~$8.6B (2024) → $24B+ by 2032 (13.8% CAGR)
- NHI market: $11.3B standalone
- Machine-to-human identity ratio: 17:1, up 44% YoY
- RSA 2026 dominant theme: agentic AI governance
- 85% of orgs adopting AI agents, only 5% at production scale — blocked by identity/access questions
- Enterprise IGA integration rate: 89% of orgs integrated <50% of apps
- Traditional IGA deployment time: 12-18 months

### 7. Compliance Frameworks Relevant to Linx Customers

For each framework, explain: what it requires in identity/access terms + how Linx's capabilities map to it.

Frameworks:
- SOC 2 (Type I/II) — access controls, user provisioning, periodic reviews
- ISO 27001 — access management, user provisioning, monitoring
- FedRAMP — identity and access management, continuous monitoring
- HIPAA — minimum necessary access, audit controls
- PCI-DSS — privileged access, least privilege, access reviews
- GDPR — data access governance, right to erasure (identity lifecycle)
- NIST CSF — identity management, access control, detection

### 8. Staleness Indicators

```
## When to Refresh This Skill

last_updated: 2026-10-18

Check these signals monthly:
- New Linx product launch or capability status change
- Competitor funding round, acquisition, or major product announcement
- New analyst report mentioning Linx (Forrester, Gartner, IDC)
- New compliance requirement affecting Linx's ICP
- M&A activity in the identity security space

Refresh protocol:
1. Open Notion → pull latest from [product wiki, competitive intel pages]
2. Update sections 2 (Platform), 5 (Competitive Landscape), 6 (Market Data)
3. Update last_updated date
4. Commit with message: "chore: refresh linx-security-domain-context [date]"
```

---

### Checkpoint 1 Test Scenarios

After building Skill 1, validate it against these scenarios:

**Test 1:** Ask Claude Code: *"What's the difference between NHI governance and PAM, and where does Linx play?"*
- **Expected:** Precise definition of both terms, clear articulation of the overlap and distinction, Linx's specific positioning in NHI+agentic governance vs. CyberArk's PAM heritage.

**Test 2:** Ask Claude Code: *"A CISO at a 500-person SaaS company is skeptical of Autopilot. What's Linx's answer?"*
- **Expected:** Surfaces the "autonomous but guardrailed" narrative, mentions progressive autonomy model, confidence × risk matrix, full audit trail, kill switch. Speaks CISO language (blast radius, audit trail, escalation).

**Test 3:** Ask Claude Code: *"What compliance frameworks should drive Linx's roadmap for Compliance & Reporting?"*
- **Expected:** Identifies SOC 2, ISO 27001, FedRAMP as highest-impact targets, maps specific Linx capabilities to each framework's identity access requirements, flags GRC Manager as the persona most driven by compliance timelines.

---

## Skill 2: `linx-prd-partner`

**File:** `/skills/linx-prd-partner/SKILL.md`

**Purpose:** Extends the generic `prd-partner` skill with Linx-specific additions. Does NOT replace prd-partner — it overlays it. When writing PRDs for Linx, load both: `prd-partner` for the base workflow + `linx-prd-partner` for domain additions.

**Depends on:** `linx-security-domain-context` (load first)

**Frontmatter:**
```yaml
---
name: linx-prd-partner
description: >-
  Linx-specific overlay for prd-partner. Adds identity security domain 
  sections, Linx buyer personas, and security/compliance PRD requirements.
  Load alongside prd-partner for any Linx product work.
  Updated: 2026-10-18
type: overlay
depends_on: [linx-security-domain-context, prd-partner]
---
```

**Sections to include:**

### 1. When This Overlay Activates

Load `linx-prd-partner` alongside `prd-partner` whenever:
- Writing a PRD for any Linx feature or capability
- The feature touches identity, access, governance, compliance, or NHI
- Omri mentions Linx, Autopilot, IGA, ISPM, NHI, or any Linx customer

### 2. Linx Persona Additions

Replace the generic prd-partner personas with these Linx-specific ones:

| Persona | Role | Primary Goal | Key Metric |
|---------|------|-------------|------------|
| CISO | Economic buyer + security champion | Reduce identity risk surface, pass audits | Risk reduction %, audit findings |
| Security Architect | Technical evaluator + implementer | Enforce policy across all identity types | Policy coverage, integration count |
| SOC Analyst | Daily user | Investigate and remediate identity threats faster | Alert fidelity, MTTR |
| GRC Manager | Compliance champion | Continuous compliance evidence | Audit pass rate, evidence collection time |
| IT Admin | Daily operator | Provision/deprovision without manual process | Provisioning time, error rate |
| Developer | End user (access consumer) | Get the access I need fast, without friction | Time to access, approval latency |

### 3. Linx PRD — Additional Required Sections

Add these sections to every Linx PRD, after the standard `prd-partner` sections:

#### Identity Security Context
```
| Dimension | Details |
|-----------|---------|
| Identity types affected | Human / NHI / Agentic / All |
| Lifecycle stage | Discovery / Provisioning / Access Review / Deprovisioning |
| Governance mode | Continuous / Periodic / Triggered |
| Autonomy level | Manual / Recommended / Supervised / Trusted Auto |
| Compliance frameworks impacted | SOC 2 / ISO 27001 / FedRAMP / Other |
```

#### Risk & Guardrails
```
For any feature involving autonomous action:
- Confidence threshold required before autonomous action
- Human escalation trigger conditions
- Kill switch behavior
- Audit trail: what is logged, in what format, for how long
- Rollback capability: can Autopilot's action be reversed?
```

#### Competitive Differentiation
```
For each competing approach:
| How [Competitor] handles this | Linx's angle | Why it matters to [persona] |
```
Pull competitor data from `linx-security-domain-context`.

#### Integration Requirements
```
| System | Integration type | Priority | Notes |
|--------|-----------------|----------|-------|
| Identity providers (Okta, Azure AD, etc.) | | | |
| HRIS (Workday, BambooHR) | | | |
| Cloud (AWS IAM, Azure RBAC, GCP) | | | |
| SaaS apps (Salesforce, GitHub, etc.) | | | |
| SIEM/SOAR | | | |
```

### 4. Linx Discovery Mode Additions

When in Discovery Mode, add these questions to the standard prd-partner discovery set:

- **Identity scope:** Does this touch human identities, NHIs, agentic identities, or all three?
- **Governance trigger:** Is governance periodic (review cycles) or continuous (real-time)?
- **Autonomy question:** Where does this fall on the manual → autonomous spectrum? What guardrails are needed?
- **Compliance driver:** Is there a specific audit requirement driving this feature?
- **Customer evidence:** Which Linx customers are asking for this? What did they say exactly?
- **Competitive pressure:** Is a competitor shipping this? How does it differ from what we'd build?

### 5. Linx-Specific PRD Anti-Patterns

Flag and push back if a Linx PRD includes:
- **"AI will figure it out"** — Every autonomous decision needs a defined confidence threshold and escalation path. Ask: what's the kill switch?
- **"We'll add NHI support later"** — NHI is a core differentiator. If the feature scope excludes NHI, that's a deliberate strategic choice that needs to be stated explicitly.
- **"SOC 2 is just checkboxes"** — GRC Managers are a primary buyer. Compliance isn't a feature request, it's a buying criterion.
- **"Just build it like Okta does"** — Linx's position is AI-native and autonomous. Features that replicate legacy IGA behavior don't advance the platform thesis.
- **Personas without CISO alignment** — If the feature doesn't address CISO-level risk metrics, flag the missing economic buyer story.

### 6. Linx Metrics Framework

Standard success metrics for Linx features:

| Feature Area | Metric | Definition |
|-------------|--------|------------|
| Risk Visibility | Identity risk score reduction | % change in high-risk identity count post-deployment |
| Autopilot | Autonomous remediation rate | % of flagged issues resolved without human action |
| Access Reviews | Rubber-stamp rate | % of reviews completed with 0 revocations (should decrease) |
| JIT Access | Time to access | Minutes from request to provisioned access |
| NHI Governance | NHI coverage | % of NHIs with active governance policies |
| Compliance | Evidence collection time | Hours to compile audit evidence package |
| Integration | Time to integrate | Days from contract to first governance data flowing |

---

### Checkpoint 2 Test Scenarios

**Test 1:** Ask Claude Code: *"Write a 1-paragraph PRD context section for a feature that lets Autopilot automatically revoke stale service accounts."*
- **Expected:** Uses identity security context table (NHI, Deprovisioning, Continuous, Trusted Auto), includes Risk & Guardrails section (confidence threshold, kill switch, audit trail), references GRC Manager and SOC Analyst personas.

**Test 2:** Ask Claude Code: *"Omri says 'we need a dashboard showing all our identities.' What Discovery Mode questions should I ask?"*
- **Expected:** Runs standard prd-partner discovery + Linx additions: which identity types (human/NHI/agentic), governance mode (continuous or periodic), which persona is the primary user, what compliance frameworks need to be visible, is this replacing a manual spreadsheet process.

**Test 3:** Ask Claude Code: *"Our PRD for the new Compliance Reporting feature doesn't mention NHI. Is that okay?"*
- **Expected:** Flags this as a Linx anti-pattern, asks whether NHI exclusion is a deliberate strategic choice or an oversight, suggests adding explicit "NHI governance data not included in v1 because [reason]" to the Non-Goals section.

---

## Skill 3: `linx-competitive-teardown`

**File:** `/skills/linx-competitive-teardown/SKILL.md`

**Purpose:** Extends the generic `competitive-teardown` skill with identity security scoring dimensions and pre-built competitor stubs. When running competitive analysis for Linx, load both: `competitive-teardown` for the base workflow + `linx-competitive-teardown` for Linx-specific dimensions.

**Depends on:** `linx-security-domain-context` (load first)

**Frontmatter:**
```yaml
---
name: linx-competitive-teardown
description: >-
  Linx-specific overlay for competitive-teardown. Adds identity security 
  scoring dimensions, pre-built competitor stubs, and Linx positioning analysis.
  Load alongside competitive-teardown for any Linx competitive work.
  Updated: 2026-10-18
type: overlay
depends_on: [linx-security-domain-context, competitive-teardown]
---
```

**Sections to include:**

### 1. Identity Security Scoring Dimensions

Replace the generic 12-dimension rubric with these identity-security-specific dimensions when analyzing Linx competitors:

| # | Dimension | 1 (Weak) | 3 (Average) | 5 (Best-in-class) | Linx weight |
|---|-----------|----------|-------------|-------------------|-------------|
| 1 | **Human Identity Coverage** | Basic provisioning only | Full IGA lifecycle | JML + access reviews + certification | High |
| 2 | **NHI Governance** | Not supported | Service accounts only | Full NHI: service accounts + API keys + bots + AI agents | Critical |
| 3 | **Agentic Identity** | Not on roadmap | Partial agent coverage | Agentic identity as first-class governance object | Critical |
| 4 | **AI-Powered Remediation** | Manual only | Recommendations only | Autonomous action with guardrails (progressive autonomy) | Critical |
| 5 | **Graph Depth** | Flat access lists | Basic relationship mapping | Full graph: entitlements + relationships + risk context | High |
| 6 | **Deployment Speed** | 12-18 months | 3-6 months | Days to weeks (agentless) | High |
| 7 | **Integration Breadth** | <50 connectors | 50-200 connectors | 200+ with deep identity-aware connectors | Medium |
| 8 | **Compliance Coverage** | 1-2 frameworks | SOC 2 + ISO | SOC 2 + ISO + FedRAMP + HIPAA + PCI | Medium |
| 9 | **Access Review Quality** | Periodic rubber stamps | Configurable certifications | Continuous + AI-contextualized + anomaly detection | High |
| 10 | **Audit Trail** | Basic logs | Structured audit log | Immutable, searchable, evidence-package-ready | Medium |
| 11 | **Protocol Support** | SCIM only | SCIM + SAML | SCIM + SAML + OAuth + proprietary APIs | Medium |
| 12 | **SIEM Integration** | None | Basic syslog/SIEM | Bidirectional: ingest + enrich + send enriched alerts | Low |

### 2. Competitor Stubs

Pre-built profiles for all 8 major competitors. Pull latest intel from Notion before using; update `[NEEDS NOTION]` placeholders with live data.

---

#### SailPoint
**Position:** Dominant incumbent, re-IPO'd. The "safe choice" for enterprise IGA.  
**Funding/Stage:** Public (re-IPO'd)  
**ICP:** Large enterprise (5,000+ employees), regulated industries (FSI, healthcare, government)  
**Core strength:** Market leadership, partner ecosystem, compliance depth, brand recognition  
**Core weakness:** Legacy architecture, 12-18 month deployment, expensive, not AI-native  
**Recent moves:** AI-powered adaptive identity, Harbor Pilot agents, machine identity lifecycle  
**NHI coverage:** Machine identity lifecycle announced; depth of native NHI governance unverified [NEEDS NOTION]  
**Agentic identity:** Emerging — agents as extensions of existing identity fabric, not first-class objects  
**Autonomous remediation:** Workflow automation, not AI-autonomous action  
**Linx's edge vs. SailPoint:** Speed to value (days vs. months), AI-native vs. bolted-on AI, true agentic identity governance  
**Linx's vulnerability vs. SailPoint:** SailPoint's incumbent advantage in large enterprise; displacement from entrenched IGA is a long sales cycle  
**Threat level:** High (in enterprise IGA deals); Low (in mid-market, NHI-first deals)  
**[NEEDS NOTION: latest pricing data, recent customer wins/losses]**

---

#### ServiceNow/Veza
**Position:** $1B acquisition (March 2026). Graph-based identity + ITSM distribution powerhouse.  
**Funding/Stage:** Acquired by ServiceNow  
**ICP:** Enterprise already on ServiceNow ITSM; IT-driven identity governance  
**Core strength:** Distribution (ServiceNow install base is massive), graph-based authorization, workflow integration  
**Core weakness:** Authorization-focused (who can access what), not governance-focused (who should have what). ITSM-centric = IT team buyer, not security buyer  
**Recent moves:** Veza's graph + ServiceNow's ITSM → identity governance embedded in ITSM workflows  
**NHI coverage:** Limited — Veza had some NHI support, roadmap unclear post-acquisition  
**Agentic identity:** Not a focus  
**Autonomous remediation:** Workflow-based (ServiceNow tickets), not AI-autonomous  
**Linx's edge vs. ServiceNow/Veza:** Security-buyer focus vs. IT-buyer focus. Unified human+NHI+agentic vs. authorization-only. Autonomous action vs. ticket workflows.  
**Linx's vulnerability vs. ServiceNow/Veza:** Organizations deeply committed to ServiceNow ITSM may prefer keeping identity governance in-platform  
**Threat level:** Medium (strong distribution advantage, but different buyer and different capability focus)  
**[NEEDS NOTION: latest Veza product post-acquisition, any Linx competitive losses to ServiceNow/Veza]**

---

#### CyberArk
**Position:** PAM leader expanding aggressively to IGA and machine identity.  
**Funding/Stage:** Public (CYBR)  
**ICP:** Large enterprise with PAM program already in place; security-first orgs  
**Core strength:** Deep PAM expertise, regulatory compliance, brand trust in security teams  
**Core weakness:** Acquisition-assembled stack (PAM + Zilla IGA + Venafi machine identity) = integration complexity. Legacy at core.  
**Recent moves:** Acquired Zilla Security ($175M, IGA), Venafi ($1.54B, machine identity). Building convergence story.  
**NHI coverage:** Venafi for PKI/machine identity + CyberArk's own secrets management. Strong but fragmented.  
**Agentic identity:** Not yet. Focus on traditional PAM for AI access.  
**Autonomous remediation:** Policy enforcement in PAM context; limited IGA autonomy  
**Linx's edge vs. CyberArk:** AI-native vs. acquisition-assembled. True agentic identity governance vs. traditional PAM adapted for AI. Speed of deployment vs. CyberArk's complexity.  
**Linx's vulnerability vs. CyberArk:** CyberArk's brand is very strong with CISOs who have bought PAM; displacement is hard.  
**Threat level:** High (they are building toward the same platform vision via acquisitions)  
**[NEEDS NOTION: latest Zilla integration status, any Linx deals lost to CyberArk]**

---

#### ConductorOne
**Position:** Modern IGA challenger. Strong content marketing.  
**Funding/Stage:** $111M raised  
**ICP:** Mid-market to enterprise (500-5,000 employees), developer-forward orgs  
**Core strength:** Modern UX, strong developer experience, unified human+NHI governance messaging  
**Core weakness:** Workflow-based remediation (creates tickets, doesn't act autonomously)  
**Recent moves:** Unified human+NHI governance, strong content marketing, community building  
**NHI coverage:** Yes — ConductorOne has NHI messaging and coverage  
**Agentic identity:** Limited — not a focus  
**Autonomous remediation:** No — ticket and workflow based  
**Linx's edge vs. ConductorOne:** Autonomous remediation vs. ticket workflows. Graph depth. Agentic identity as differentiator.  
**Linx's vulnerability vs. ConductorOne:** ConductorOne has developer-friendly positioning that resonates with DevSecOps buyers. Also has more marketing momentum.  
**Threat level:** High (closest to Linx in ICP and messaging; direct competitor in mid-market deals)  
**[NEEDS NOTION: any head-to-head deals with ConductorOne; current positioning]**

---

#### Lumos
**Position:** AI-first IGA. Pinterest, MongoDB, GitHub as customers.  
**Funding/Stage:** $35M Series B  
**ICP:** Mid-market, SaaS-heavy organizations, developer culture  
**Core strength:** Modern UX, "Albus" multi-agent IGA launch, strong in SaaS access governance  
**Core weakness:** SaaS-focused = lighter on cloud infrastructure (IAM roles, service accounts). NHI coverage limited beyond SaaS.  
**Recent moves:** Launched "Albus" (first AI multi-agent IGA system, 2026)  
**NHI coverage:** Limited — SaaS-oriented tool coverage  
**Agentic identity:** Albus is multi-agent IGA (agents running governance workflows) — different from governing agentic identities  
**Autonomous remediation:** Albus has autonomous workflow capabilities  
**Linx's edge vs. Lumos:** Graph depth + NHI coverage vs. SaaS-only. Cloud + on-prem identity vs. SaaS-only. True agentic identity governance vs. agents running governance workflows (different thing).  
**Linx's vulnerability vs. Lumos:** Lumos has modern UX and developer experience advantage in SaaS-heavy mid-market  
**Threat level:** Medium (different buyer, different coverage depth; could converge)  
**[NEEDS NOTION: Albus feature details post-launch; Linx vs. Lumos win/loss]**

---

#### Opal Security
**Position:** Developer-friendly JIT access. Cloud-native.  
**Funding/Stage:** $32M Series B  
**ICP:** Developer-forward orgs, cloud-native companies, DevOps/DevSecOps teams  
**Core strength:** Best-in-class JIT access UX, Terraform/Slack/Jira integrations, developer love  
**Core weakness:** JIT-only focus. No broader IGA, no NHI governance, no compliance reporting.  
**Recent moves:** Cloud-native JIT, strong developer community  
**NHI coverage:** None meaningful  
**Agentic identity:** None  
**Autonomous remediation:** None — JIT is request-based  
**Linx's edge vs. Opal:** Platform breadth (JIT is one capability in Linx; it's Opal's entire product). NHI + agentic governance.  
**Linx's vulnerability vs. Opal:** Opal's JIT UX is best-in-class. If Linx's JIT isn't as polished, Opal wins JIT-only deals.  
**Threat level:** Low (point solution; different buyer journey; JIT is a feature in Linx's platform)  
**[NEEDS NOTION: Linx JIT roadmap status vs. Opal capabilities]**

---

#### Zluri
**Position:** NHI expansion play. 200+ customers. Launched Identity Security Platform March 2026.  
**Funding/Stage:** [NEEDS NOTION: latest funding]  
**ICP:** Mid-market, SaaS-heavy  
**Core strength:** SaaS discovery and governance, 200+ customer base to upsell  
**Core weakness:** Discovery-focused historically; remediation is newer and less proven  
**Recent moves:** Launched "Identity Security Platform" (March 2026) — added NHI and posture management  
**NHI coverage:** Yes — added as part of March 2026 launch  
**Agentic identity:** Not a stated focus  
**Autonomous remediation:** Limited — primarily discovery + recommendations  
**Linx's edge vs. Zluri:** AI autonomy + true remediation vs. discovery-focused. Depth of governance vs. breadth of SaaS discovery.  
**Threat level:** Low-Medium (entering same space but from different origin; less proven in governance)  
**[NEEDS NOTION: Zluri platform launch details; any head-to-head deals]**

---

#### Saviynt
**Position:** Converged IGA+PAM, strong in regulated industries.  
**Funding/Stage:** Private, significant revenue  
**ICP:** Regulated industries (FSI, healthcare, government), large enterprise with complex SAP/Workday environments  
**Core strength:** SAP/Workday fine-grained controls, regulatory compliance depth, IGA+PAM convergence  
**Core weakness:** Complexity equals long implementation. Not AI-native. Expensive.  
**Recent moves:** Converged IGA+PAM platform messaging, cloud-native delivery  
**NHI coverage:** Limited  
**Agentic identity:** Not a focus  
**Autonomous remediation:** Workflow-based  
**Linx's edge vs. Saviynt:** Speed-to-value + AI-native vs. complexity. Agentic identity governance (Saviynt has none).  
**Linx's vulnerability vs. Saviynt:** Saviynt's SAP/Workday depth is extremely hard to replicate; regulated industries with these systems won't consider Linx as a Saviynt replacement  
**Threat level:** Low (different ICP; compete primarily on greenfield deals in tech/SaaS vertical)  
**[NEEDS NOTION: any recent Linx vs. Saviynt competitive situations]**

---

### 3. Linx Positioning Analysis

#### Where Linx Wins Today
- NHI-first or agentic identity deals (only credible option)
- Greenfield IGA at Series B–D companies (no legacy debt, modern stack)
- Organizations where Autopilot's autonomous remediation is the differentiator
- Speed-to-value deals where incumbent IGA deployment time is the problem

#### Where Linx Is Vulnerable Today
- Deals requiring deep SAP/Workday controls (Saviynt territory)
- CyberArk replacement in PAM-centric organizations (brand, incumbency)
- SailPoint displacement in large enterprise (long sales cycle, committee buying)
- JIT-only deals where Opal's UX wins

#### Linx's "Only We" Statement
*"Linx is the only platform that governs human identities, non-human identities, and agentic AI identities in a unified graph — with AI-powered autonomous remediation, not just detection."*

Challengers to this claim:
- ConductorOne: also claims unified human+NHI (but no autonomous remediation)
- ServiceNow/Veza: graph-based (but authorization-focused, IT buyer, no agentic identity)
- Lumos/Albus: agents running governance (different from governing agentic identities)

#### Competitive Positioning Map

```
                    AI-NATIVE (autonomous action)
                            |
             Linx ●         |
                            |
PLATFORM ───────────────────┼─────────────────── POINT SOLUTION
(human+NHI+agentic)         |                    (one capability)
                            |
   ConductorOne ●           |              ● Opal (JIT only)
   ServiceNow/Veza ●        |
   Lumos ●                  |
                            |
                    WORKFLOW-BASED (ticket creation)

Axes:
  X = Platform breadth (point solution ↔ platform)
  Y = Remediation approach (workflow-based ↔ AI-autonomous)
  
Not plotted (different quadrant):
  SailPoint, Saviynt, CyberArk — Legacy platform, manual governance
```

### 4. Competitive Intel Refresh Protocol

```
last_updated: 2026-10-18

Monthly refresh checklist:
□ Check Notion competitive intel pages for updates
□ Review competitor LinkedIn / press releases for new features/funding
□ Search "SailPoint|CyberArk|ConductorOne|Lumos|Veza site:techcrunch.com OR site:businesswire.com" (last 30 days)
□ Check G2/Gartner Peer Insights for new reviews mentioning NHI or agentic identity
□ Update competitor stubs with [date] inline for any changed data
□ Update last_updated date in frontmatter
```

---

### Checkpoint 3 Test Scenarios

**Test 1:** Ask Claude Code: *"Linx is in a competitive deal against ConductorOne. What's our pitch?"*
- **Expected:** Surfaces Linx's edge on autonomous remediation vs. ticket workflows, highlights agentic identity as Linx differentiator, acknowledges ConductorOne's modern UX and developer experience, suggests leading with Autopilot demo and NHI coverage.

**Test 2:** Ask Claude Code: *"Score Lumos on our identity security rubric."*
- **Expected:** Runs through the 12 identity-security-specific dimensions, gives Lumos strong scores on Human Identity Coverage + modern UX, weak scores on NHI Governance + Agentic Identity + Autonomous Remediation, provides total score with commentary.

**Test 3:** Ask Claude Code: *"Where does Linx have whitespace that no competitor owns today?"*
- **Expected:** Identifies agentic identity governance + autonomous remediation as the whitespace, notes no competitor credibly offers both in a unified platform, calls out the convergence risk (CyberArk buying their way there, ConductorOne potentially building autonomy).

---

## Final Deliverable Checklist

After completing all 3 skills and passing all checkpoints:

- [ ] `/skills/linx-security-domain-context/SKILL.md` created, 150-300 lines, all 8 sections present
- [ ] `/skills/linx-prd-partner/SKILL.md` created, 150-300 lines, Linx persona table + 4 additional PRD sections present
- [ ] `/skills/linx-competitive-teardown/SKILL.md` created, 200-400 lines, all 8 competitor stubs + positioning analysis present
- [ ] All `[NEEDS NOTION: ...]` placeholders documented (these are follow-up items, not blockers)
- [ ] All `[NEEDS INPUT: ...]` placeholders documented
- [ ] Omri has reviewed and approved each checkpoint

When done, print this message:

```
ALL 3 SKILLS COMPLETE.

Summary:
- linx-security-domain-context: [X] lines, [N] Notion pages consulted
- linx-prd-partner: [X] lines
- linx-competitive-teardown: [X] lines

Needs Notion (complete these to fill placeholders):
[list all [NEEDS NOTION] items]

Needs Input:
[list all [NEEDS INPUT] items]

Next step: Copy the /skills/ directory to Lorch19/Linx-Operator-Kit repo.
```
