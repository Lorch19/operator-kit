# Figma shipped a design agent. What that actually changes for us.

**How I'm treating this.** Not a quick take. "Riff" is how you opened it, but the thing under the riff is a positioning question — if the answer is what I think it is, it changes what the product is for, not just what we ship next quarter. So I'm running the heavy version: context, the questions that matter, two or three real directions with trade-offs, a design, and then a hard stop. Nothing gets built off this document until you say yes to a specific direction. If you wanted a five-minute reaction instead, say so and I'll collapse it.

---

## 0. What I checked, and what I'm taking on faith

There's no repo, brief, or metrics file for me to read here, so the company context below is your one sentence plus my assumptions. Flag anything I got wrong — three of the assumptions carry real weight.

What I did verify, because the whole argument turns on it:

- Figma's agent is native to the canvas and generates real artboards from a prompt, not images. Confirmed.
- **The agent's quality is a function of an existing design system.** Figma's own positioning is that it knows your components, colors, tokens and variables; independent testing reports it is *strongest at flows built on a real, component-based design system*. This is the single most important fact in this document.
- Figma is already at the destination. Figma Sites publishes live responsive sites with a CMS; Figma Make goes prompt → interactive web app. So they are not stuck upstream of a developer handoff.

That last one matters because it kills the first argument I was going to make to you. My instinct was "their output is a design file, ours is a live thing, we're safe." That's false. Do not let anyone in the building make that argument in a strategy meeting; it will get checked and it will fall over.

---

## 1. The questions I'd be asking you one at a time

I can't ask, so here's each one with the answer I'm running on and what breaks if I'm wrong. Two of these change the recommendation outright.

**Q1. Which non-designer?** "People who aren't designers" spans a solo founder mocking an app, a PM specing a feature, a marketer building a landing page, and a teacher making a worksheet. These are four different companies.
*Assumption:* founders, PMs and marketers at companies under ~50 people, making product and marketing surfaces.
*If wrong:* if you're actually in the teacher/small-business/social-graphics lane, Figma's announcement is close to irrelevant to you and this entire document is over-reacting. **This is the biggest branch point.**

**Q2. What does a user physically leave with today?** A file they hand to someone, a screenshot they paste into Slack, or a live thing with a URL?
*Assumption:* a mockup that gets handed off or screenshotted — the work stops short of being real.
*If wrong:* if you already publish live artifacts, you're further along than I'm assuming and Section 4 is mostly a sharpening exercise rather than a pivot.

**Q3. Is our generation quality at parity with theirs today?**
*Assumption:* no, and it won't be. They'll look better on day one and the gap will persist.
*If wrong:* if you genuinely out-render them, some of the "don't compete on generation" logic loosens — but not much, because parity on a commodity isn't a business.

**Q4. Where does retention come from today?**
*Assumption:* weak and project-shaped — people show up for a burst, finish a thing, leave for six weeks.
*If wrong:* if there's a daily-use surface I don't know about, that surface is the asset to defend and I'd build around it instead.

**Q5. What do we own that Figma structurally can't copy?**
*Assumption:* right now, nothing. That's the actual problem, and it predates the Figma news.

**Q6. What's the response budget?**
*Assumption:* one quarter to put something visible in market, not a year of rebuild.

**Q7. Do our users arrive with a brand system, or nothing?**
*Assumption:* nothing. A logo, maybe two colors, an existing website they didn't design.
*If wrong:* if your users do arrive with design systems, you are competing with Figma head-on on their strongest ground, and I'd tell you to sell the company or pick a different segment.

---

## 2. The read

**The barrier we removed was never the moat we thought it was.** The pitch for a design tool aimed at non-designers has always been: professional tools are too hard, we make the output achievable without the craft. That located the barrier in the *interface* — canvases, layers, constraints, the pen tool. Prompt-to-screen dissolves the interface barrier for everyone at once, including for the incumbent whose interface was the hardest. "You don't have to learn the tool" just stopped being a differentiator; it's now a feature every tool has by Tuesday.

**But generation was never the hard part of the job.** The non-designer's actual job is not "produce a screen." It's "ship something that works and doesn't embarrass me, without a designer to tell me if it's right." Generation delivers a draft. It does not deliver a decision. When anyone can produce twenty screens in ten seconds, the bottleneck moves from *making* to *choosing and trusting* — and our user is precisely the person with no ability to choose and no one to ask.

**Here's the asymmetry that's actually defensible.** Figma's agent is good because it sits on a design system. Components, tokens, variables, prior art — that's what turns a prompt into something coherent rather than something generic. Our users do not have that and never will. So the constraint layer that makes generation good is, for our segment, *missing*. Whoever manufactures that missing layer controls output quality. Not the model. The model is the same model.

That reframes the product. **We are not a design tool with an AI feature. We are a brief-and-constraint engine with a rendering backend.** The scarce input in our segment isn't design skill and isn't compute — it's the specification. Ask a non-designer to describe a screen and you get "a dashboard, make it look nice." Prompt-to-screen assumes the user can specify. Ours can't. That's the gap, and it's the one Figma's product is least motivated to close, because their user *is* the specification.

**Second asymmetry: the sign-off.** Figma will never make "is this safe to ship?" a headline feature, because saying that to a professional designer is an insult. For our user it's the whole anxiety. Nobody is going to tell them the contrast fails, the mobile layout breaks, the CTA is buried, the tone is off-brand. There is no reviewer. Selling the reviewer is a product Figma's own customer would resent.

**Third, and this is the one I'd argue hardest for: Figma is probably not the attacker.** They're the *signal*. The faster threat to a design tool for non-designers is the prompt-to-app tools coming up from underneath — a founder who can type "a pricing page for my SaaS" and get a deployed, working page has no reason to stop at a design step at all. Figma moving down-market is slowed by org gravity, seat-based pricing built for design teams, and an onboarding path that assumes a file and a team. The tools coming up have none of that friction. If we spend the quarter building a defensive answer to Figma specifically, we will fight the wrong war.

**And the commercial consequence:** a screen just stopped being a scarce artifact. Any pricing tied to making screens — per seat, per project, per export — is repricing toward zero on a schedule we don't control. Monetization has to move off generation and onto something that stays scarce: confidence, publication, volume, consistency over time.

---

## 3. Three directions

**A. Own the destination.** Stop shipping mockups; ship the live thing. Unit of work becomes a published page, a deployed surface, a sent email — real, addressable, measurable.
*For:* closes the loop the user actually cares about; pricing moves to published artifacts.
*Against:* Figma already does this via Sites and Make, and a dozen prompt-to-app tools do it better. Alone, this is a race to a crowded finish line.

**B. Own the sign-off.** Be the reviewer the user doesn't have: brand fidelity, accessibility, mobile, hierarchy, copy, conversion patterns. Works on our output *and* on imports — including things made in Figma.
*For:* structurally hard for Figma to prioritize; creates a surface even when the user generates elsewhere; genuinely unserved.
*Against:* a checker is a feature, not a company. Weak standalone retention, weak pricing power, and easy to bolt onto any rival in a quarter.

**C. Own the constraints.** Become the place where a non-design company's visual and verbal truth lives — derived, not authored. Ingest their live site, their existing app, their deck, their logo; synthesize the design system they never built; then expose it everywhere: our editor, their code tool, an MCP endpoint, a Figma plugin.
*For:* attacks the exact dependency Figma's agent runs on, in the segment where that dependency is unmet. Models commoditize; a company's derived context doesn't. Gets better with use.
*Against:* invisible. Nobody wakes up wanting a design system. It must be sold as an outcome, never as the thing it is.

**Recommendation: C is the engine, A is the surface it's sold as, B is the ritual that makes both legible.**

Concretely: the user arrives, we derive their constraints from what already exists in their business in under a minute, we generate against those constraints into a destination-native artifact, and every generation ends with a named, specific sign-off. C without A is an invisible infrastructure product nobody buys. A without C is a me-too generator that loses on render quality. B alone is a browser extension.

**What I'd refuse to do:** ship a "prompt to screen" button as the headline response to this news. If we add it, it's plumbing, mentioned nowhere in the positioning. Matching a competitor's announcement is how you spend a quarter arriving second.

---

## 4. The design

Four parts, each with a checkpoint. Tell me where it stops holding.

**4.1 What the product becomes.** Positioning: *the design tool that already knows your company.* The unit of work stops being a file and becomes a shipped artifact with a sign-off attached.
*Does this hold?*

**4.2 Three components, cleanly separated.**

- **Deriver** — in: a URL, an app screenshot, a PDF, a logo. Out: a constraint set (palette with roles, type scale, spacing rhythm, component inventory, tone-of-voice sample, real content strings). Knows nothing about rendering. Testable on its own: feed it 50 real small-company sites, score the constraint sets by hand.
- **Composer** — in: constraint set + a goal (not a design prompt — "get more demo bookings," "explain the pricing tiers"). Out: candidate artifacts. This is the commodity layer; treat it as swappable and never build identity on it.
- **Ship-check** — in: artifact + constraint set. Out: a named list of specific risks with one-click fixes ("body text is 3.1:1 against your background, fails at AA — raise to #1F2937"). Runs on imported work too, which is how it becomes a wedge rather than a postscript.

Each is independently testable and independently replaceable. If the Composer needs to know how derivation works, the boundary is wrong.
*Does this hold?*

**4.3 First run.** Paste your URL. Sixty seconds later you're looking at a page that already uses your colors, your type, your words, and your product's real screenshots — before you've typed a prompt. The demo is the moat: a competitor's blank prompt box next to our pre-loaded one is the entire sales pitch, and it can't be copied without building the Deriver.

**4.4 When it fails.** Derivation will fail — brandless sites, JS-heavy apps, one-page Squarespace templates. Failure must degrade to a three-question fallback (what's your primary color, formal or casual, who's it for), never to a blank canvas. And the ship-check must under-claim: it says "three things I'd fix" and lists them, never "this is good." A false clean bill of health on something that then flops in public is the one failure that destroys the entire value proposition. Every check names the standard it's applying.

**4.5 Pricing.** Off seats and off generation. Price on published artifacts and on the persistence of the constraint set — the brand memory is the subscription, the generation is free. This is also the defense against per-seat incumbents: our buyer has one or two people, not twenty.

*Does 4.3 through 4.5 hold?*

---

## 5. Sequencing, and what would make me abandon this

**Two weeks, before any product work.** Build the Deriver as a throwaway script against 30 real customer URLs and have a designer grade the constraint sets blind. If derived constraints aren't materially better than defaults, direction C is dead and I'd rather know in two weeks than two quarters. Run in parallel: five calls with users who've already tried Figma's agent — did they even notice, did they switch, what stopped them.

**Quarter one.** Deriver plus ship-check, shipped against the existing editor. Do not rebuild the editor.

**Quarter two.** Destination-native output and the pricing move — only if the quarter-one retention change is real.

**Kill criteria, stated now so we can't rationalize later:** derived constraints don't beat defaults in blind grading; users don't come back for the ship-check within 30 days; or Figma ships derive-from-URL themselves, at which point the wedge is gone and the answer is segment, not feature.

---

## 6. Stress test

**Weakest link:** the whole thing rests on derived constraints being meaningfully better than good defaults. They might not be. A tasteful default template plus the user's logo and two colors may get 85% of the way, in which case the Deriver is engineering effort for a marginal gain and C collapses into "nice onboarding."

**A smart critic says:** "You've described an onboarding improvement and a linter, and called it a strategy." That's a fair hit. The counter is that the Deriver is the only component here that compounds and that a competitor can't ship in a sprint — but it's a counter, not a proof.

**What I might have wrong:** that non-designers want a sign-off at all. They may want *permission to stop thinking*. A product that says "three things are wrong with this" might be experienced as the nagging they came here to escape. The ship-check may need to fix silently and report afterward, which is a materially different product.

**The move that beats us:** Figma ships derive-from-URL for teams without design systems. It's an obvious feature, they have the distribution, and it would erase the wedge in one release. The bet is that their org gravity, their pricing, and their customer's self-image make it a low priority for four to six quarters. That is a timing bet, not a moat. Say it out loud every time this gets presented.

**The thing nobody will want to hear:** if Q1's answer is that our users are making one-off graphics rather than product and marketing surfaces, none of the above applies and we should ignore the Figma news entirely.

---

## 7. What I need from you

Nothing gets built off this. Two answers change the plan:

1. **Which non-designer** (Q1) — this flips the whole document.
2. **Is a two-week throwaway derivation test worth burning before anything else** — that's the cheapest place to be wrong.

Give me those and I'll turn this into an actual sequenced plan. Push back on the read first if it's off; I'd rather rewrite Section 2 than plan against a wrong premise.

---

**Sources for the verified claims:**
- [The Figma Design Agent is Here | Figma Blog](https://www.figma.com/blog/the-figma-agent-is-here/)
- [Figma AI Design Agent — Native to Your Canvas | Figma](https://www.figma.com/solutions/ai-design-agent/)
- [Work with the Figma agent in design files – Figma Help Center](https://help.figma.com/hc/en-us/articles/37998629035799-Work-with-the-Figma-agent-in-design-files)
- [Figma AI Agents: Review, Pricing & How to Use (2026)](https://sanjaytarani.com/blog/figma-ai-agents-an-honest-review-after-testing-every-prompt)
- [Introducing Figma Sites | Figma Blog](https://www.figma.com/blog/introducing-figma-sites/)
- [Figma Make FAQs – Figma Help Center](https://help.figma.com/hc/en-us/articles/31722591905559-Figma-Make-FAQs)
