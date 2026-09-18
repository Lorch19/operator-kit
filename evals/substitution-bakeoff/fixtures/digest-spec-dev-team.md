# PRD — Weekly Project Digest Email (Dev-Team)

**Status:** Approved for build · **Owner:** Product · **Eng lead:** TBD

## Problem
Users with 3+ active projects lose track of changes between logins. Support sees
~40 tickets/month of the form "I didn't know X changed." Weekly active users who
own 3+ projects log in 2.1x/week vs 4.4x for 1-2 project owners.

## Solution
A weekly email summarising what changed across each user's projects: items added,
items completed, comments received, members joined. Sent Monday 08:00 in the
user's local timezone. Opt-out per user; opt-out per project.

## Scope
In: project item deltas, comment counts, membership changes, one CTA per project.
Out: real-time digests, daily cadence, Slack delivery, mobile push.

## Requirements
- R1. Aggregate events per project over trailing 7 days.
- R2. Suppress the email entirely if zero events across all projects.
- R3. Respect per-user and per-project opt-out flags.
- R4. Render in HTML + plaintext; degrade cleanly with images blocked.
- R5. Timezone-aware scheduling, batched to avoid send spikes.
- R6. Unsubscribe link in footer, one-click, no login required.

## Data model
New table `digest_send_log` (user_id, sent_at, projects_included, event_count).
Read from existing `project_events`, `project_members`, `user_preferences`.

## Success criteria
- ≥35% open rate by week 4.
- ≥8% click-through to the product.
- <0.5% unsubscribe rate per send.
- 3+ project owners' weekly logins up from 2.1 to 2.8 within 8 weeks.

## Open questions
- Do we count the digest as an "active session" if the user clicks through?
- What happens for users whose only event is their own activity?

## Rollout
Internal dogfood week 1, 10% of 3+ project owners week 2, full week 4.
