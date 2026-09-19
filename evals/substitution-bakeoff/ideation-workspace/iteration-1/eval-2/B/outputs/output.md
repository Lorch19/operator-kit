# "Users can't find their old projects" — getting past the search box

## The short version

You're stuck on "add search" because search is the only idea that matches the shape of the complaint. But the complaint is a symptom with at least five different underlying causes, and search only addresses one of them — probably not the largest one.

The specific reason it feels lazy: **search is a query language for people who already remember the answer.** It asks the user to supply a name, at the exact moment when name-recall is what failed. And if a large share of your projects are called "Untitled," "Untitled (2)," and "Copy of Untitled," then search indexes garbage and returns garbage.

The unlock: **the highest-leverage fix is at creation time, not retrieval time.** Auto-name projects from their content, and search becomes worth building. Ship search without it and you'll get a second wave of tickets that say "I searched and nothing came up."

Recommended first three: (1) spend two hours splitting your ticket corpus by root cause, (2) auto-name projects + backfill existing ones, (3) make the home screen recognition-first (resume strip) and make search span archive/trash/other workspaces with explicit "found in Trash" messaging. Search ships inside #3, not as #1.

---

## Part 1 — Why "add search" feels lazy

Three things are true at once:

1. **Search is correct.** You should have it. Every mature product with a project list has one. Not having it is a gap.
2. **Search is not differentiating.** Nobody switches to you because your search box exists. It removes a reason to leave; it doesn't create a reason to stay.
3. **Search is mis-sequenced.** It is a retrieval fix applied to what is mostly a creation-time and identity-time problem.

The instinct that it's lazy is a real signal, and it's pointing at #3. Keep it. Don't ship search alone.

---

## Part 2 — Problem framing before ideating

"Can't find my old projects" is a single sentence covering at least five distinct failures. They need completely different solutions, and only one of them is fixed by a search box.

| # | Root cause | What actually happened | Does search fix it? |
|---|---|---|---|
| **C1** | **Naming failure** | The project was never named. "Untitled (7)" tells the user nothing, so scanning fails *and* search fails. | No — search over unnamed items is useless |
| **C2** | **Recall failure** | The project is named, but the user remembers the *context* (the client, the week, what it looked like), not the string. | Partially — only if they guess a word in the title |
| **C3** | **Scale / architecture failure** | 300 projects in a flat paginated grid with no grouping. The item is visible but undiscoverable. | Partially — helps power users, not browsers |
| **C4** | **Identity / continuity failure** | Created while logged out, on a trial, on a different account, or in a different workspace. The project exists — just not where they're looking. | **No.** Search in the wrong account returns zero results, correctly, forever |
| **C5** | **It isn't there** | Auto-archived, retention-expired, deleted (by them or a collaborator), or a trial downgrade hid it. | **No.** And a blank search result actively makes this worse |

**This is the thing to do before anything else.** Pull the last 100 tickets tagged with this complaint and tag each one with C1–C5 based on how it resolved. It's an afternoon of work and it will change what you build. If C4+C5 are 40% of the corpus, no amount of search design moves your top complaint.

### Questions I'd normally ask you — and the answers I'm assuming

I can't ask, so here is each question with my working assumption and what flips if the assumption is wrong.

| Question | Assumption I'm using | If it's wrong |
|---|---|---|
| What % of projects carry a default/untitled name? | 40–70% | If under 10%, auto-naming drops to a quick win and content-aware retrieval becomes the main bet |
| Median and p90 projects per active user? | Median ~12, p90 ~80 | If p90 is under 10, this isn't a scale problem at all — it's entirely C4/C5, and the answer is account repair, not browsing UX |
| Of tickets, how many end with the project *found* vs. *doesn't exist* vs. *wrong account*? | ~50 / ~20 / ~30 | Drives the entire priority order. This is the number to go get |
| Are projects visually distinctive (thumbnailable)? | Yes | If not, the thumbnail grid loses most of its power — use content-snippet rows instead |
| Can users create a project while logged out or pre-signup? | Yes | If no, the identity cluster shrinks a lot |
| Any retention/auto-delete policy on free or trial tiers? | Yes, some form of cleanup or downgrade-hiding | If yes, a slice of your "top complaint" is a *policy* complaint in a findability costume. That's a comms and lifecycle fix, not a UI one |
| Does "old" mean 2 weeks or 8 months? | Weeks to a few months | If it genuinely means 6+ months, recency-based fixes are near no-ops and content-aware retrieval becomes the real answer |
| Solo users or teams? | Mostly solo and small teams | If teams, "find" also means "find something a colleague made," which adds a permissions and visibility dimension |
| Where do users arrive from? | Direct app open, plus shared links from email/chat | If most arrive via shared links, broken/stale link handling is its own ticket class |
| What does home show today? | Paginated grid sorted by last-modified, no recents emphasis, no grouping | If home already leads with recents, skip the resume strip and go straight to grouping and retrieval |

Everything below is built on these assumptions. Where an idea depends hard on one, I say so.

---

## Part 3 — Twenty angles, twenty candidate ideas

Systematic generation. One idea per angle, forced — including the ones that don't work, because knowing *why* they don't work is half the value.

### Constraint manipulation

**1. Add a constraint — solve it with no search box and no typing.**
→ **Recents-as-home.** The landing screen becomes a reverse-chronological activity stream grouped by day and week ("Today," "Last week," "March"), with large previews. Forces recognition instead of recall. This is the constraint that produces the best idea in the whole set, which tells you something.

**2. Remove all constraints — infinite engineering, no limits.**
→ **Describe it, don't name it.** Semantic index over project *contents* — text on the canvas, layer names, uploaded filenames, prompts, collaborator names — so "the one with the blue pricing table I made for Acme" resolves. Retrieval by description rather than by title.

**3. Make it 100x bigger — 10,000 projects per user.**
→ At that scale, manual naming and folders collapse entirely. You need **auto-collections**: clusters formed without user effort (by client name appearing in content, by time burst, by file type, by collaborator). Also: "find" starts to mean "find across the whole team," not just mine.

**4. Make it much smaller — the absolute minimum that delivers value.**
→ **A "Pick up where you left off" strip.** Three cards, top of home, with a Resume button. One sprint. Probably resolves a meaningful share of tickets on its own because a lot of "can't find my old project" means "can't find the one from yesterday."

### Structural manipulation

**5. Bundle — what separate things should become one?**
→ **One index, faceted.** Today you probably have My Projects, Shared with Me, Templates, Archive, and Trash as separate places. A meaningful number of tickets are "it was in a tab I never open." Unify them into one list with filters — and critically, make search span all of them and *say so*: "3 results here, 1 in Archive, 1 in Trash."

**6. Unbundle — what single thing should split apart?**
→ **Separate the project from its outputs.** Often the user doesn't want the editable project — they want the thing they exported or the link they sent. A **"Links I've shared"** view, findable by recipient and date, is a completely different retrieval path: "I sent it to Dana in March."

**7. Make it the only thing — what if the product were just this?**
→ It would be a **photo library**: large thumbnails, a time scrubber down the side, auto-albums, and the ability to jump to a month instantly. Nobody names their photos and yet everyone finds them. That's the existence proof that naming isn't required for retrieval.

**8. Make it unnecessary — eliminate the need to find.**
→ **Never create an orphan, never lose the thread.** Anonymous/logged-out work gets claimed at signup; session state restores on return; if they arrive from a shared link on a different account, you detect it and offer to switch rather than showing an empty state. This class of fix removes C4 entirely rather than making it easier to work around.

### User psychology

**9. Remove friction — what step can be eliminated?**
→ **Auto-naming.** Derive a name from the project's own content at first meaningful save (the first heading, the dominant text, the source filename, the prompt). Backfill existing untitled projects the same way. This is the dependency that makes every other retrieval idea work.

**10. Add friction — where would deliberate friction help?**
→ **A five-second commit moment at the end of a session,** not the start. "Name this before you go?" with the auto-name pre-filled so it's one keystroke to accept. Naming at creation fails because the user doesn't know what it is yet; naming at the end works because they just finished it.

**11. Reduce anxiety — what are they actually afraid of?**
→ They're not frustrated, they're **scared they lost work.** Address the fear head-on: a permanent, visible "nothing is deleted — see all N projects including archived and deleted" affordance, a generous recovery window, and an end-of-session email with a permalink so there's always a copy of the address outside your app. Also: a self-serve **"Can't find a project?"** recovery flow that walks all five causes, including "check your other account."

**12. Solve an unexpressed need.**
→ They often don't want to *find* the old project — they want to **re-use** it. "Start from my last invoice," "duplicate the Acme deck." Reframing retrieval as "start from" changes the job from archaeology to a creation shortcut, which is a much better product.

### Perspective shifts

**13. Do the opposite — reverse the assumption.**
→ Stop making the user find the project. **Make the project find the user.** Proactive resurfacing: "You were working on Acme three weeks ago," a monthly digest of what they made, deep links back from wherever they shared it.

**14. Reframe — what if the problem is something else entirely?**
→ Three live reframes: (a) it's a **naming problem**, so fix creation, not retrieval; (b) a slice of it is an **authentication problem** wearing a findability costume; (c) it's a **support-deflection problem** — the cheapest measurable win might be an in-product recovery flow that resolves all five causes without a ticket.

**15. Combine unrelated things.**
→ **Time and context as the index, not names.** Anchor the library to things the user actually remembers: the week of a meeting, the day they uploaded a file, the person they shared with. Your browser history works this way and nobody names their browser tabs.

**16. Solve two or three problems at once.**
→ A **monthly "here's what you made" digest** serves findability (permalinks in the inbox, searchable in their email), retention (a re-engagement trigger), and the anxiety problem (proof nothing was lost) — one build, three outcomes. Auto-naming similarly improves findability *and* the recipient experience of shared links *and* the quality of any future search index.

### Experience design

**17. Surprise.**
→ **"On this day" / time machine.** Scrub the library back to how it looked in March. Delightful, and it happens to be a retrieval mechanism.

**18. Make them feel smarter.**
→ A **portfolio view** — projects auto-arranged into a presentable body of work they can show a client or a manager. Finding becomes a side effect of showing off.

**19. Build distribution in.**
→ Shared project links carry a discreet "more from this workspace" path back, so **recipients become a retrieval channel**: the user can find their own work by going to the person they sent it to.

**20. Make it skeuomorphic — what real-world metaphor fits?**
→ Three candidates, and the comparison is instructive:
- **Filing cabinet** (folders, tags, taxonomy) — requires user discipline that your users have already demonstrated they do not have. This is the metaphor most products default to and it is the wrong one here.
- **Workbench** ("what's on your desk right now") — good for the 3 active projects, useless for the 300 old ones.
- **Photo library** (camera roll + auto-albums + time scrub) — designed for exactly this situation: a large, growing, unnamed, visually-distinct corpus. **This is the metaphor to build toward.**

---

## Part 4 — Clustering the twenty into seven real candidates

| | Candidate | Built from | One-line description |
|---|---|---|---|
| **A** | **Fix creation, not retrieval** | 9, 10, 1 | Auto-name from content, backfill existing untitled projects, add a five-second end-of-session naming nudge |
| **B** | **Recognition-first home** | 1, 4, 7, 20 | Resume strip + time-grouped visual library with a month scrubber, replacing the flat grid |
| **C** | **One index, no dead ends** | 5, 11, 14 | Unified faceted list spanning archive/trash/shared/other workspaces, with explicit cross-boundary result messaging and a self-serve recovery flow. **Search lives here.** |
| **D** | **Identity & continuity repair** | 8, 14 | Claim anonymous work at signup, detect wrong-account/wrong-workspace and offer to switch, restore session state, email permalink receipts |
| **E** | **Ambient resurfacing** | 13, 16, 17 | The project finds the user: monthly digest, dormant-project nudges, deep links from shared contexts |
| **F** | **Content-aware retrieval** | 2, 3, 15 | Semantic index over project contents plus auto-collections by client/time/collaborator |
| **G** | **Re-use over retrieve** | 12, 18, 19 | "Start from my last ___", personal templates from own work, portfolio view, share history |

---

## Part 5 — Evaluation

| | Valuable? | Usable? | Feasible? | Viable? |
|---|---|---|---|---|
| **A** Fix creation | **High.** Removes the root cause of C1 and raises the ceiling on every other option | **High** — invisible, zero new UI to learn | **High** for heuristic naming (first heading / filename / dominant text). Medium if generated. Backfill is a batch job | **High** — cheapest path to ticket reduction |
| **B** Recognition-first home | **High** for C2/C3 if "old" means weeks. **Low** if "old" means 8 months | **High** — recognition beats recall for everyone | **High** for the resume strip; medium for the full time-scrubbed library | **High** — also lifts return-session engagement |
| **C** One index + search | **Medium alone, high combined with A.** Converts silent zero-results into "it's in Trash" | **Medium** — facets need restraint or you rebuild the confusion | **High** | **Medium** — necessary, not differentiating |
| **D** Identity repair | **Very high for its slice, zero for everyone else.** Entirely dependent on the C4 share of tickets | **High** — an offer to switch accounts is self-explanatory | **Medium** — touches auth, which is where the sharp edges live | **High** if C4 is real: these are often the users closest to churning or converting |
| **E** Ambient resurfacing | **Medium.** Helps the forgetful, doesn't help someone hunting right now | **Medium** — one notification too many and it's spam | **Medium** — needs a send policy, preferences, unsubscribe | **High** — doubles as a re-engagement lever with its own ROI |
| **F** Content-aware retrieval | **High ceiling, high variance.** Genuinely differentiating if it works | **High** when accurate; **destroys trust** when it isn't | **Low–medium.** Indexing pipeline, cost per project, quality tuning, ongoing spend | **Medium** — real cost, uncertain payoff until the ticket split is known |
| **G** Re-use over retrieve | **Medium–high.** Serves the "I want to make another one like that" job better than any retrieval feature | **High** | **Medium** | **High** — creates value rather than just removing friction |

**Validation moves:** A — count the untitled share, then dry-run the naming heuristic against 200 real projects and read the output yourself before shipping. B — five moderated sessions of "find the project you made about X" on the current build, timed. C — instrument how often a search returns zero results while a match exists in archive/trash. D — comes straight out of the ticket split. E — test as a plain email before building anything in-product. F — before building an index, hand-check whether 20 real ticket descriptions contain enough content-words to have been resolvable. G — a painted door on the empty state: "Start from a previous project."

---

## Part 6 — Classification and the 2x2

| Candidate | Classification |
|---|---|
| A — Fix creation | **Differentiator.** Almost nobody does this well; it compounds into everything else |
| B — Recognition-first home | **Differentiator** in execution, **MMR** in concept |
| C — One index + search | **Neutralizer / MMR.** This is the "add search" instinct, correctly scoped |
| D — Identity repair | **MMR.** Table stakes you're probably failing |
| E — Ambient resurfacing | **Quick Win** as email, **Differentiator** if done with taste |
| F — Content-aware retrieval | **Differentiator** — and the only true Big Bet here |
| G — Re-use over retrieve | **Differentiator.** Reframes the job entirely |

**Risk vs Impact**

- **No Brainers (low risk, high impact) → do first:** A (auto-name + backfill), B-lite (resume strip), C-lite (search spans archive/trash with explicit messaging)
- **Big Bets (high risk, high impact) → only after the ticket split justifies it:** F (semantic retrieval + auto-collections), B-full (time-scrubbed visual library)
- **Quick Wins (low risk, moderate value) → fill gaps:** E as email digest, G as a painted door, the self-serve recovery flow
- **Duds (high risk, low impact) → don't:** folders, tags, and manual taxonomy as the primary answer. They require exactly the organizational discipline your users have already proven they don't have — you'd be shipping a feature that only serves the users who don't have the problem. Also a dud: "favorites/pin," for the same reason (it only helps if you predicted in advance which project you'd need later).

---

## Part 7 — Recommended sequence

**Week 0 — before you build anything.** Tag the last 100 tickets C1–C5. Two hours. If C5 (it isn't there) dominates, stop and go fix the retention policy and the messaging around it; none of this is your problem. If C4 (wrong account) dominates, D jumps to first.

**Release 1 — ship together, not separately.**
- Auto-naming for new projects + backfill of existing untitled ones (A)
- "Pick up where you left off" strip on home (B-lite)
- Search, scoped to span archive, trash, shared, and other workspaces, with explicit "found in Archive" results and a never-blank empty state that links to the recovery flow (C-lite)

The sequencing point is the whole answer to your question: **search ships in the same release as auto-naming, or it indexes "Untitled (14)" and you get a second ticket wave.**

**Release 2.** Time-grouped visual library with a month scrubber (B-full). Unified faceted index (C-full). Identity repair (D), sized by what the ticket split showed.

**Release 3, conditional.** If the split shows C2 (recall-by-context) dominates and users describe projects by contents rather than titles, build F. If it shows they mostly want to make another one like the last one, build G instead. Don't build both.

**Running in parallel, cheap.** Monthly "here's what you made" email (E) — test the plain email version now; it's a week of work and it serves retention independently of whether it moves this metric.

---

## Part 8 — How you'll know it worked

Instrument before Release 1, or you'll be arguing about it later:

- **Primary:** tickets tagged "can't find project" per 1,000 monthly active users (rate, not count — your absolute count will rise with growth regardless)
- **Leading:** % of projects still untitled 7 days after creation. This should fall off a cliff in Release 1 and is your earliest signal
- **Behavioral:** median time from app-open to opening an existing project; % of sessions that open an existing project at all
- **Failure canary:** % of searches returning zero results. If this stays high after Release 1, the naming fix didn't take
- **Counter-metric:** rate at which users rename an auto-generated name within the first session. A little is healthy engagement. A lot means your naming heuristic is wrong and is actively making things worse

---

## Stress Test

**The weakest link is that this whole plan rests on a ticket split I haven't seen.** I've assigned probabilities to C1–C5 from pattern, not from your data. If the real distribution is 70% C5 (free-tier retention deleting work), everything above is elaborate motion in the wrong direction and the actual fix is a policy change plus honest email warnings before deletion. **Do the split first. It's the only step here I'd call non-negotiable.**

**Auto-naming can be worse than "Untitled."** "Untitled" is honest — it tells the user the system doesn't know. A confidently wrong name is a lie, and a list of plausible-but-wrong names is harder to scan than a list of obvious blanks, because every row now demands evaluation. Mitigations: derive names from the user's own content rather than generating descriptions; fall back to "Untitled" when content is thin rather than guessing; show the name inline-editable from the moment it appears; watch the rename-rate counter-metric.

**Recency-first design may not touch "old."** The user's word was *old* projects. A resume strip and a recents-first home serve last-week's project beautifully and do nothing at all for the six-month-old one. If "old" genuinely means months, B is close to a no-op and the real answers are C and F. This is the biggest internal contradiction in my own recommendation, and it resolves the moment you check the age distribution of the projects people are hunting for.

**A smart critic would say:** "You wrote three thousand words to avoid building a search box. Users asked for search. Ship it, measure, then get clever." That critique is substantially fair, and the honest concession is that search is not wrong — it's insufficient and mis-ordered. The plan above ships search in Release 1. It just refuses to ship it alone.

**Survivorship bias in the ticket corpus.** People who file tickets skew toward power users with many projects and high investment. The median user with six projects may have a completely different problem — or no problem — and you'd be designing for the loud tail. Before committing, check whether the complainers are a distinct segment by project count and tenure.

**"Top support complaint" is a weaker signal than it feels.** It may simply be the *easiest* complaint to articulate — "I can't find my stuff" is a sentence anyone can write, while "your export pipeline quietly degrades quality" is not. Volume is not severity and neither is revenue impact. Check whether this complaint correlates with churn or downgrade at all. If it doesn't, it's an annoyance tax, and the cheap fixes (A, B-lite, C-lite) are the entire correct investment — F and B-full would be over-building.

**Ambient resurfacing (E) has a real downside.** If your users are already notification-fatigued, a digest reads as spam and costs you goodwill in exchange for a marginal findability gain. Test as email with a hard opt-out before it ever becomes an in-product notification.

**What I still can't answer:** whether the users filing these tickets are the ones you most want to keep. That determines whether this is a Release-1 problem or a Release-3 problem, and no amount of ideation substitutes for looking.
