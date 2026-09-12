# Notes

Working notes on how Omri wants to be taught. Update as preferences surface.

## Observed (2026-09-12, first session)

- **Wants evidence, not assertions.** Asked "is it secured?" about a third-party repo and
  expected an actual audit — file-by-file sweeps, not a judgement. Lessons should cite
  the repo file and line, never "as you know".
- **Terse instructions, high trust.** "do all the 3", "push now". Prefers action over
  clarifying questions; ask only when an answer genuinely changes the work.
- **Values caught problems.** Reacted well to the public-repo catch and to being told the
  validator had a real bug. Surfacing a flaw is not received as criticism.
- **Writes in Hebrew and English.** Lessons in English; either is fine in conversation.
- **Retrieval, not coverage.** Explicitly wrote "fluency, not just awareness" — so quiz
  him, don't re-present the routing table.

## Teaching decisions made

- Lessons are built from the kit's *own* text (frontmatter, `DO NOT` clauses,
  `NAVIGATOR.md`), never from my summary of it. This is both more accurate and directly
  demonstrates where the tiebreaker lives.
- Genuine ambiguities in the kit are taught **as ambiguities**, not smoothed into a clean
  answer. Where two skills overlap with no `DO NOT` clause separating them, that is a
  prune signal and the lesson says so.

## Published lessons

Lessons live here as local HTML (linking `assets/lesson.css`, per the `teach` skill).
Because Omri works from remote sessions where local files don't open, each lesson is also
published as a self-contained Artifact with the styles inlined. The local file is the
source; the Artifact is the delivery copy — change the local one first.

| Lesson | Artifact |
|---|---|
| `0001-the-tiebreaker.html` | https://claude.ai/code/artifact/fee27f5f-ee67-4c64-bfb7-7b6b802a7209 |

## To confirm with him

- Is `learning/operator-kit-fluency/` the right home for this workspace? It lives inside
  the repo so it is version-controlled and survives sessions, and it matches the existing
  `sessions/` and `missions/` directories — but it does ship with the plugin marketplace.
- Which skills has he actually run? Blocks both the prune and lesson targeting.
