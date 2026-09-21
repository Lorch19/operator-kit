# "We should build a mobile app"

## Before anything: what kind of request this is

This is a new system, not a change to something that already exists here. That means it gets the full treatment — questions, approaches, a written design, then an implementation plan — not a quick sketch and a scaffold. I'm saying that out loud so you can override it.

But I can't even start the questions honestly, because the request as stated isn't a project yet. It's a solution wearing a project's clothes.

**"We should build a mobile app" bundles three separate claims, and only the last one is stated:**

1. There's a problem worth spending months on. *(unstated)*
2. Software is the right response to it. *(unstated)*
3. That software should be a phone app distributed through app stores. *(stated)*

The one you stated is the least reversible and the least important. Claims 1 and 2 decide whether any of this pays off. Claim 3 is a delivery-surface decision that should fall out of them — and it's the one that buys you two runtimes, store review cycles, a device matrix, signing and release trains, crash/analytics plumbing, and users stranded on old versions you can't force to upgrade.

So I'm not going to generate app ideas yet. That would be filling in claims 1 and 2 with my guesses and calling it your strategy.

## What I checked first

Before assuming the app has nothing to attach to, I looked:

```
$ find . -name package.json -o -name "*.swift" -o -name "*.kt" -o -name pubspec.yaml -o -name Podfile
  (only two package.json files, both inside evals/ test fixtures)

$ find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -5
  405 md   119 json   117 xsd   92 py   58 txt
```

This repo is a documentation-and-scripts toolkit: 405 markdown files, 92 Python scripts, zero client code, no backend service, no API. `BACKLOG.md` has no mobile item anywhere in it. The last 15 commits are all internal documentation and routing maintenance.

Two things follow. First, there's no existing flow to extend, which confirms this is greenfield — the heavier process, not the lighter one. Second, and more usefully: **this repo gives no candidate for what "the app" is.** So the app is either for a different product entirely, or it doesn't exist yet even as a concept. Either way, the missing information isn't technical.

## The seven things I'd need to know

In a live session I'd ask these one at a time and stop after the first, because the answer to Q1 changes which of the others are even worth asking. Since this is running unattended, here they all are with my working answer and — the part that matters — what each answer actually changes.

**Q1. Who has the problem, and what do they do today instead?**
*Why it forks the work:* A named person with a painful workaround means the build is a fast follow. A hypothetical user means the next step is five conversations, not a repository.
*My assumption:* No named user yet. The phrase "we should build" is a hunch in search of evidence.
*If I'm wrong:* If you can name three people and what they currently do with a spreadsheet, texts, or paper, skip most of what follows and go straight to specifying that one flow.

**Q2. What does a phone give you that a browser tab doesn't?**
*Why it forks the work:* This is the entire justification for the word "mobile." Test below.
*My assumption:* Nothing proven yet — so the default is mobile web, not an app.
*If I'm wrong:* Name the capability and it becomes the spine of the design, and the first thing the prototype has to prove works.

**Q3. What has to be true in 90 days for this to have been worth it?**
*Why it forks the work:* Without a number, there's no way to stop, and no way to tell a working version from a failed one. "People use it" isn't a criterion.
*My assumption:* Undefined. I'd force one before any build: a count of people doing a specific thing a specific number of times.
*If I'm wrong:* If there's already a target, it constrains scope hard and most feature debates resolve themselves.

**Q4. Is this a new product, or a mobile surface on something you already have?**
*Why it forks the work:* A surface on an existing product inherits users, auth, data, and a backend — the app is a client. A new product must earn distribution from zero, which is a marketing problem, not an engineering one, and it's usually the thing that kills these.
*My assumption:* New product, since nothing here suggests an existing service.
*If I'm wrong:* If there's an existing backend, the design starts at its API and the scope drops by more than half.

**Q5. Who builds it, and who maintains it in month seven?**
*Why it forks the work:* Maintenance, not construction, is the real cost. App stores force you to keep shipping — OS updates, SDK deprecations, signing certificates, policy changes — whether or not the product is growing.
*My assumption:* One part-time builder working with AI assistance. That alone eliminates two separate native codebases as an option.
*If I'm wrong:* A team of three-plus changes what's affordable, but not the sequencing.

**Q6. What's the budget, and what's the kill criterion?**
*Why it forks the work:* A stated kill criterion is what makes a cheap probe rational instead of a delay tactic.
*My assumption:* Unbudgeted. I'd propose one week of exploration with a written go/no-go before anything longer.
*If I'm wrong:* A hard budget mostly sets how much scope gets cut, not what gets built first.

**Q7. Is there a non-negotiable constraint driving this — a customer who requires an app, regulated data, a date?**
*Why it forks the work:* This is the question most likely to make everything above irrelevant. If a buyer's checklist says "mobile app" or there's a demo on a fixed date, the goal isn't a product, it's an artifact for a meeting — and the cheapest honest answer might be a clickable prototype, not a shipped binary.
*My assumption:* No such constraint. If there is one, say so and I'll redesign around it rather than around users.

## The test that decides the "mobile" part

If none of these is the mechanism by which the product creates value, a responsive web app beats an app on cost, iteration speed, and distribution — and you can reverse the decision later:

| Capability | Load-bearing when... |
|---|---|
| Push notifications while the app is closed | Re-engagement *is* the product mechanic (reminders, alerts, time-sensitive matching) |
| Offline operation with local writes that sync later | Users work in warehouses, planes, basements, fields, or bad coverage |
| Camera / scanner / sensors, low friction | Continuous capture, barcodes, AR, motion — not "upload a photo occasionally" |
| Background execution | Location tracking, geofencing, periodic sync without the user opening anything |
| Pocket immediacy | The job happens standing up, in under ten seconds, away from a desk |
| Platform trust surfaces | Biometrics, secure enclave, Apple/Google Pay, HealthKit, contacts |
| Store presence as a channel | You genuinely expect store search to be an acquisition source — the weakest reason on this list, and the most over-claimed |

**Scoring:** zero load-bearing → build mobile web, revisit in six months. Exactly one → check whether an installable web app or a thin wrapper covers it before committing. Two or more → a real app is justified, and those two capabilities are the first thing the first version must prove.

## What "a mobile app" actually contains

Worth naming, because the scope question isn't "which features" — it's how much of this you're signing up for:

Account and identity · the one core flow · server, data model, hosting · offline sync and conflict policy · notification infrastructure · payments and store-billing rules · release pipeline (signing, beta tracks, crash reporting, forced upgrade) · privacy disclosures, consent, and in-app account deletion.

Only the second item is your product. The other seven are the toll you pay to ship it. A first version should carry exactly one core flow, one platform, and — if you can possibly avoid it — no accounts.

## Three ways forward, with my recommendation

**A. One-week problem probe — recommended.**
Five conversations with people you believe have the problem, plus a clickable one-screen prototype of the single core flow. No repository, no stack decision. Ask them what they did the last time this came up, what it cost them, and what they tried instead — past behavior, never "would you use this." Pass condition, written before you start: at least three of five describe the problem unprompted *and* show you a workaround they built themselves. Output is a decision, not code.
*Why this one:* Every other path is cheaper and better-aimed after it, and if it fails you've spent a week instead of a quarter.

**B. Mobile web first.**
Build the core flow as a responsive web app, installable to the home screen. Ship in days, change in hours, no review queue. Escalate to a real app the first time a specific missing capability blocks a behavior you have actually watched someone need.
*Cost:* Notifications are weak, offline is work, and you give up store presence.

**C. Commit to the app now.** One cross-platform codebase, one platform released first, one flow.
*Only if* the capability test already returns a hard yes and a fixed date forces it. Two separate native codebases is off the table at the team size I'm assuming.

Ruled out regardless of answers: both platforms at launch, accounts-before-value, and any backend built before the flow is known.

## What I'd do next, on the assumptions as stated

Taking my own answers at face value — no named user, no proven device need, no deadline, small team — the honest plan is path A, and it takes a week:

1. **Days 1–2.** Write the problem down as one sentence: *who*, *in what situation*, *fails to do what*, *and what it costs them.* If that sentence can't be written without inventing details, that's the finding.
2. **Days 2–4.** Five conversations. Four questions each, all about the last time it happened.
3. **Day 5.** Score against the capability test. Score against the pass condition from path A.
4. **Day 5.** Go / no-go in writing. Go means I write the design to `docs/specs/<date>-<topic>-design.md`, you review it, and only then does it become an implementation plan.

Nothing gets scaffolded, no stack gets chosen, and no repository gets created before that document exists and you've said yes to it.

## Stress test

**Weakest part of this.** My repository evidence may be beside the point. Nothing in your sentence says the app belongs to this codebase — if it's for a different product with real users and a backend, I've anchored on the wrong ground and Q4 is already answered in a way that makes half of this moot.

**Assumption most likely to be wrong.** That the sentence is exploratory. If it came out of a decision already made with your team, or a customer conversation, then interrogating the premise reads as obstruction, and the useful contribution would have been scope-cutting instead. Tell me it's decided and I'll switch to arguing about what to cut.

**What a smart critic would say.** "This is discovery theater. Some teams learn more from shipping a rough version in three weeks than from five interviews, and your week of talking produces opinions while a build produces behavior." That argument is strongest when the build is cheap and reversible — which is exactly what store distribution is not. But if you can genuinely reach a usable version in three weeks, path C is defensible and I'd stop arguing.

**Where my own test is weak.** The capability table under-weights distribution. For some consumer products, being in the App Store *is* the acquisition channel, and that alone can justify an app with zero device-capability need. I flagged it as the weakest line in the table because it's the reason people reach for when the other six come up empty — but occasionally it's the true one.
