# "Users can't find their old projects" — options, and why search keeps eating your thinking

**Scope call, said out loud so you can overrule it:** this is not a bounded change to an
existing flow. There is no single "find" flow to patch — the complaint spans naming,
storage, permissions, account identity, and the list UI at once. So I'm treating it as
architectural: clarifying questions, then structurally different approaches, then a design
in sections, then a written spec. **Nothing gets built until you approve the design.** I've
carried this as far as honest reasoning goes without you in the room; every place I had to
guess is labeled.

**What I could and couldn't check:** there's no codebase for this product available to me
here, so I have not read your list view, your data model, or your support queue. Everything
below is reasoned from the complaint itself. That's a real limitation and it's the reason
Question 1 exists.

---

## 1. Why you keep landing on "add search"

Worth naming before the options, because the fixation is doing more damage than the missing
feature.

1. **You're solving the sentence, not the sessions.** "Users can't find their old projects"
   is a support-ticket paraphrase. The verb in it is *find*. Search is the solution that
   rhymes with the verb. But the sentence is already a user's own solution-hypothesis, and
   you inherited their framing wholesale.
2. **Availability.** Every tool you've used has a search box. It is the most retrievable
   exemplar of "helping people locate things," so it arrives first and crowds out the slot.
3. **It converts ambiguity into a ticket.** "Add search" is buildable, estimable, and
   assignable by Friday. The real problem is a mushy multi-cause mess. Reaching for search
   is partly relief from not knowing.
4. **It's the lowest-blame option.** Nobody in a retro says "search was a mistake." An
   option that can't be wrong also can't be evaluated, which is exactly why it stays.

The tell that it's insufficient: **a support ticket means the user already tried.** People
who write in have exhausted the obvious. A search box is the obvious. So search's most
likely effect on your top complaint is to change the ticket from "I can't find it" to "I
searched and it's not there" — which is a worse ticket, because now the absence feels
confirmed and the user is angrier.

Search isn't wrong. It's **mis-sequenced and under-specified**. I'll come back to that.

---

## 2. Questions I'd normally ask one at a time — with my working answer

I can't ask, so each gets my assumption and what flips if I'm wrong.

**Q1. Of the last 50 tickets, how many are "it's in the list and I couldn't spot it" versus
"it isn't in the list at all"?**
*Working answer:* the majority are the second kind — wrong workspace, wrong account, guest
session never claimed, archived, trashed, or hidden by a plan downgrade.
*If I'm wrong* and it's mostly the first kind, Approach A below becomes the recommendation
and search moves much earlier.
*This is the single question whose answer changes the most, and it costs an afternoon.*

**Q2. What fraction of projects are called "Untitled" or a near-duplicate of another name?**
*Working answer:* over a third. Creation tools almost always leak untitled artifacts.
*If I'm wrong* and naming is healthy, drop the auto-naming work and lean on filters.

**Q3. Median and p90 project count per active account?**
*Working answer:* median under 20, p90 in the hundreds. The complaint is concentrated in the
p90 tail and in accounts older than a year.
*If I'm wrong* and even p90 is ~30, this is not a scale problem at all — it's a location or
identity problem, and everything in the "make the list legible" bucket is wasted.

**Q4. Can a person create work before signing in, or under a second email?**
*Working answer:* yes, at least historically. Orphaned-account cases are a steady trickle in
every product that has ever had a guest mode or a Google/email dual-signup path.
*If I'm wrong* and identity is strictly single-account, the recovery surface shrinks a lot.

**Q5. Does anything hide or delete projects without the user's action — retention windows,
plan downgrades, workspace removal, inactivity cleanup?**
*Working answer:* yes, at least one. There usually is, and it is usually undocumented in the
UI.
*If I'm wrong,* good — one whole failure class disappears.

**Q6. What does support actually do to resolve these today?**
*Working answer:* a human runs an internal lookup that the user has no access to. That is a
strong signal, because it means the information exists and is merely withheld from the
person who needs it.

**Q7. What's the success metric?**
*Working answer:* not ticket volume. Ticket volume falls when people give up. Primary metric
should be **dormant-project reopen rate** — accounts per week that open a project untouched
for 30+ days — with time-to-open as the secondary.

**Q8. "Old" — how old?**
*Working answer:* months, not days. The word "old" in your sentence is doing real work: it
says the default view is recency-ordered and the tail is unreachable. If it were "the thing
I made yesterday," you'd have a save/sync bug, not a findability problem.

---

## 3. Generating options properly

Four passes, deliberately chosen so they can't all return search.

### Pass 1 — take the complaint apart word by word

| Word | Hidden assumption | What it opens up |
|---|---|---|
| **Users** | One population with one behavior | Heavy users (scale problem) and returners (identity/memory problem) fail differently |
| **can't find** | The failure is retrieval | Could be recognition, location, access, or existence |
| **their** | Ownership is settled | It may be in a workspace, a teammate's account, or an unclaimed session |
| **old** | Age is incidental | Age *is* the mechanism: recency ordering buries the tail |
| **projects** | The object is well-formed | Objects named "Untitled" are not findable by any means, including search |

### Pass 2 — six distinct ways "can't find" actually happens

| # | Failure mode | Does search fix it? |
|---|---|---|
| 1 | **Retrieval** — it's there, buried in 400 rows | Only if they remember a distinctive word |
| 2 | **Recognition** — it's on screen, they can't tell which one | No. Search over "Untitled (7)" returns nothing useful |
| 3 | **Location** — different workspace, account, or device | No, unless search spans all of them |
| 4 | **Access** — permission or link changed | No. Makes it worse: a zero-result page implies deletion |
| 5 | **Existence** — expired, purged, downgraded away, never saved | No, and actively harmful |
| 6 | **Belief** — they think it's gone and stop looking | No. Nobody searches for what they've mourned |

**Search addresses one and a half of six.** That is the whole diagnosis.

### Pass 3 — intervene at a different point in the lifecycle

Search occupies exactly one cell of six. The other five are unoccupied.

`create → name → store → resurface → retrieve → recover`

### Pass 4 — invert the question

Instead of "how does the user find the project," ask "how does the project find the user,"
and "what if there were no list to search."

### The candidate set

Thirteen candidates, each with a different mechanism. Search is number eight.

**Prevent the loss**
1. **Name-at-birth.** Derive a real title from the first content the moment work starts;
   "Untitled" becomes impossible to create. Attacks recognition at the source.
2. **Claim-your-work.** Bind guest and second-email sessions to an account before they can
   be orphaned; detect same-email-different-provider at login and offer the merge.
3. **Nothing disappears silently.** Downgrades, expiry, and workspace removal show work
   locked and read-only with a stated path, never hidden.

**Make them recognizable**
4. **Visual recall.** Real content thumbnails plus a three-fact line: created, last opened,
   who else touched it. People re-find by picture and by story, not by string.
5. **Episodic grouping.** Group by work session or by month with a visible activity trace,
   so users navigate by "the week I was doing the pitch" rather than by name.

**Make the tail reachable without typing**
6. **Time-bucket browse.** This week / this month / 2025 / older, with counts. Turns 400
   rows into five decisions.
7. **Visible facets.** Owner, shared-with-me, archived, type — narrowing that requires no
   recall at all.
8. **Search — but over content and with typo tolerance,** not a title-prefix match. If you
   build search, this is the only version worth building.

**Remove the finding task**
9. **The project finds the user.** A "pick up where you left off" rail, a dormant-work
   resurface, a monthly "a year ago you made this." The best find is the one never made.
10. **No list at all** — a persistent spatial workspace where old work stays where you left
    it. Genuinely different, genuinely expensive. Listed so it's on the table; I'd kill it.

**Kill the dead end**
11. **One account-wide index plus a "can't find it?" flow.** A single lookup spanning every
    workspace, linked account, archive, trash, and shared item, which tells you *which
    bucket* the hit is in. Empty states and zero-result states route here, never to a help
    article.
12. **Self-serve restore plus a support recovery console.** Give the user the lookup support
    already runs; give support a faster one, instrumented.

**Find out first**
13. **Code the queue and instrument the funnel.** 50 tickets tagged by the six failure
    modes; events for list views, searches, zero results, scroll depth, and dormant reopens.

---

## 4. Three coherent bets, and my recommendation

Not menus — three different theories of the problem.

**Approach A — "Make the list legible"** (candidates 1, 4, 5, 6, 7)
*Theory:* everything is there; the list is a wall of identical grey rows.
*For:* entirely front-end, ships in weeks, helps every user on every visit.
*Against:* fixes modes 1 and 2 only. If your tickets are mode 3-5, it changes nothing about
the complaint you actually named, and you'll have spent a quarter proving it.

**Approach B — "No dead ends"** (11, 12, 2, 3, then 8) — **recommended**
*Theory:* tickets come from absolute dead ends, not slow browsing. People who write in have
already scrolled.
*For:* directly targets the population that generates the complaint; support gets faster
immediately; and the account-wide index it requires is the thing that makes real search cheap
later.
*Against:* the index is back-end work with a genuine security surface — a unified view that
leaks one user's project into another's results is far worse than the bug you're fixing.

**Approach C — "Remove the finding task"** (9, plus 1 and 4)
*Theory:* finding is the wrong verb. Resurface work before it's missed.
*For:* highest ceiling, most differentiated, converts a support cost into a re-engagement
loop.
*Against:* helps the next 90 days of projects, not the ones already lost. It cannot resolve a
single open ticket.

**Recommendation: gate, then B, with pieces of A folded in, then C, and search last.**

1. **Week 1 — candidate 13.** Tag 50 tickets against the six modes and add the funnel
   events. One week, one person. It decides A-versus-B on evidence instead of instinct, and
   without it you're betting a quarter on my Q1 guess.
2. **Weeks 2-6 — Approach B**, plus candidates 1 and 4 from A, because auto-naming and
   thumbnails are cheap, improve every other approach's results, and are the only thing that
   makes any search worth running.
3. **Then — candidate 8, search**, as a filter over the index B already built. At that point
   it's a fraction of the cost, and it finally runs over a corpus with real titles and real
   content instead of a wall of "Untitled."
4. **Fast-follow — C's resurfacing rail**, once you can measure dormant reopens.

Note what happened to your instinct: **search survives, but as the last mile rather than the
first move.** It felt lazy because as a first move it is — it inherits the user's framing,
addresses one failure mode in six, and runs over a corpus too degraded to match against.
Sequenced fourth, over a real index with real titles, it's the correct finish.

---

## 5. Design — Approach B (first section; stop and tell me if this is wrong before I write the rest)

**What we build**
- **Work Index** — one read model per account covering every project the account can
  legitimately reach: all workspaces, all linked identities, archived, trashed-but-
  recoverable, shared-with-me. Each entry carries title, derived title, thumbnail ref,
  timestamps, owner, and **bucket** (active / archived / trashed / locked-by-plan /
  other-workspace / other-linked-account).
- **Identity Resolver** — the linking rules for "accounts that are the same human": same
  verified email across providers, claimed guest sessions, invited-then-registered users.
  Conservative by design; ambiguity produces a prompt, never an automatic merge.
- **Recognition Pipeline** — asynchronous, idempotent derivation of a title and a thumbnail
  from project content, running on create, on meaningful edit, and as a backfill over
  history.
- **Find Surface** — the list, plus the two states that matter most: **empty** and **zero
  results**. Both carry a "looking for something you don't see?" entry that runs the
  cross-bucket lookup and reports the bucket in plain language: *"Found 1 match in your
  archive"* / *"...in the Acme workspace"* / *"...under your other Google login."*
- **Recovery Actions** — restore from trash, unarchive, request access, re-link account. The
  lookup must never be a dead end that only tells you the thing exists.

**Data flow.** Project lifecycle events fan out to the index. The index is a projection, not
a source of truth, and can be rebuilt from scratch — treat that rebuild as a first-class,
tested operation, not an emergency script.

**Failure and edge handling** (the part that decides whether this is a good idea)
- **Permissions are enforced at read time against live authorization, never from the indexed
  copy.** A stale index that leaks another account's project title is a security incident
  that dwarfs the original complaint. This is the one place I'd spend disproportionate
  review.
- **Index lag** is visible, not hidden: a project created 10 seconds ago must appear, so the
  list reads live for the active workspace and the index for everything else.
- **Trashed items** show retention state and remaining time, never a bare absence.
- **Locked-by-plan** items are stated as locked with a path, never silently dropped — one of
  the largest sources of "you deleted my work" tickets in any freemium product.
- **Identity linking is always confirmed by the user.** An incorrect merge is unrecoverable
  and far worse than a missed one.

**How we'd test it**
- A fixture account: 400 projects, 60% untitled, spread over three workspaces, two linked
  logins, with archived and trashed items — the p90 case, not the demo case.
- Authorization tests as the gating suite: every bucket, every revoked-permission path,
  every cross-account case.
- Backfill idempotency and a full index rebuild under load.
- **Five unmoderated find-tasks:** "open the project you made around six months ago." Time
  to success and failure mode recorded. This is the only test that measures the actual
  complaint.

**Metrics**
- *Primary:* dormant-project reopen rate (accounts/week opening a project untouched 30+ days).
- *Secondary:* median time from list entry to opening the intended project.
- *Guardrails:* zero-result rate; ticket volume **and** ticket escalation rate together.
- *Counter-metric:* wrong project opened then immediately closed; accidental restores.

**Explicitly not building** — folders and tags (users don't maintain them, and an unmaintained
folder hides work better than a flat list does); semantic/AI search (a v3 conversation, and
worthless over untitled content); bulk-organize wizards; cross-app federated search; and
candidate 10's spatial workspace.

---

## 6. Stress test

- **Weakest point:** my Q1 answer. The entire recommendation rests on the guess that most
  tickets are dead ends rather than buried rows. That's why week 1 is a gate and not a
  formality — if the tag-up says mode 1 and 2 dominate, switch to Approach A and pull search
  forward. I'd rather be corrected in week 1 than in month 3.
- **Where a critic lands hardest:** "You've turned 'add search' into a quarter of index
  work." Fair. The defense is that the index is the prerequisite for a search worth having,
  and it resolves modes 3, 4, and 5, which search cannot touch at any budget. The rebuttal I
  can't fully dismiss: a crude title search shipped next week would produce *some* signal
  now, and shipping it as a deliberately instrumented probe — measuring the zero-result rate —
  is a legitimate alternative gate to candidate 13. If you want speed, that's the version I'd
  defend.
- **Assumption most likely to be wrong:** that thumbnails are meaningful for your content
  type. If projects are text or config, thumbnails are decorative and candidate 4 collapses
  into candidate 1 alone.
- **What I'd be embarrassed to have missed:** that this is a save-reliability bug wearing a
  findability costume. If any measurable number of these projects genuinely never persisted,
  every option here is cosmetic and the real work is in the write path. The week-1 tag-up
  should be able to see that, and it's the reason I won't skip it.
- **Blast radius of being wrong:** low for the gate, moderate for B. The index is additive
  and removable; the identity linking is not. If we get merging wrong, we create a worse
  complaint than the one we started with.

---

## 7. Before anything gets built

I need three things from you:

1. **Does the scope call hold** — architectural, not a quick add?
2. **Does the recommended sequence hold** — one week of evidence, then "no dead ends," then
   search last? Or do you want the crude-search-as-probe variant instead?
3. **Section 5 is the first design section only.** Tell me it's right and I'll write the
   remaining sections, then the full written spec for your review. The implementation plan
   comes after you've approved that spec — not before.

If the answers to Q1 and Q5 in section 2 are already known to you, send them first. They
would change this document more than anything else could.
