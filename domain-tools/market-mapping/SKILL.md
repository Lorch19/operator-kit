---
name: market-mapping
disable-model-invocation: true
description: >-
  Map a problem space or market as one objective, sourced, scored report: problem size, segments, unmet needs, alternatives, players, economics, risks, open questions. No recommendations.
  Use for "analyze the market for X", partnership or investment diligence, or "is there a business here".
  DO NOT use for a single competitor deep-dive — use competitive-teardown.
---

# Market Mapping

The output is **one report** in 8 sections. Each section opens with a one- or two-sentence finding and then gives one main table. Calculations sit in folded `<details>` blocks. The reader should be able to get the picture in two minutes and check any number in ten.

## Hard rules

1. **Map, don't recommend.** Don't write "we should", don't pick a focus segment, and don't add a mitigation column. Give an opinion only if the user asks, and give it in chat, not in the report.
2. **Problem space, not the solution under review.** The product that prompted the research is not the subject.
3. **Status quo first** (April Dunford). The strongest alternative is usually WhatsApp, Excel, a person, or doing less. Score it like any vendor.
4. **Every number has a source link, or an `הערכה` / estimate badge plus a visible formula.** Flag vendor self-reported claims as such.
5. **Every score is transparent.** Show the formula, the raw 1–5 inputs, and the weights in a folded table.
6. **Tables, not cards.** Use heat cells, pills and badges instead of paragraphs. Methodology goes in the folds, never in the body.
7. **One version.** When asked to sharpen, rewrite the report. Don't add a separate summary.
8. **Look before publishing.** Run `assets/screenshot.py` and view the images. Phone and desktop must both pass the overflow check.

## Phase 0 — Scope (at most 3 questions)

- Boundary: which problem or market, and what is excluded.
- Geography: players and trends globally, with segments in depth for the target countries.
- Reader: who receives it. This sets the language and the level of detail.

## Phase 1 — Research

Run searches in parallel. Use standard mode first and extended mode for niche or recent facts. Collect, with dates:

| Bucket | What to get |
|---|---|
| Size inputs | Units (rooms, firms, seats) × usage × unit cost, per country |
| Trends | 5–6 dated, sourced rows: labour, regulation, tech, money (a light PESTEL) |
| Segments | Counts per segment and what they use today |
| Players | 10–20 players in 4–5 groups, with funding, customer counts and recent moves |
| Pricing | Anchors per unit and per seat, setup fees, revenue share |
| Switching | What pushes customers to switch, what pulls them, and what stops them (survey data where available) |

If a source is unreachable, say so and use the next best one. Never invent a number.

## Phase 2 — Score

- **Problem size:** use a bottom-up annual spend formula. Skip TAM/SAM/SOM while the problem is still undefined.
- **Segment opportunity** (Ulwick): pain = average of 3–5 named drivers (each 1–5); opportunity = pain + max(pain − coverage, 0).
  For a replacement market such as a core system: openness = dissatisfaction + trigger − switching cost.
- **Unmet needs:** importance + max(importance − satisfaction, 0), scored 0–20, for each need × segment. Show this early, in section 3.
- **Alternatives:** 6–8 options, including the status quo and "do less".
  - Use 8 buying criteria, and always include impact on the outcome, daily adoption, cost and vendor risk.
  - Weights sum to 100 for each segment. Raw scores are 1–5.
  - Show a weighted score per segment in **one** table, and badge what each segment uses today.
- **Players:** for each, what it is strong at, weak at, and how relevant it is (now / watch / far).

## Phase 3 — Report

Copy `assets/report-template.html`. Replace the header, the prose and the data arrays in the script. Keep the CSS: it already has theme tokens, dark mode, heat classes and RTL number fixes.

| # | Section | Main table |
|---|---|---|
| 1 | Bottom line | One sentence plus 4 number tiles |
| 2 | Problem / market | Size by country with formulas; trends with sources |
| 3 | Customers | Segments sorted by score (calculation folded); unmet-needs heat table |
| 4 | Competition | Alternatives × segments (weights and raw scores folded); players grouped; moves timeline folded |
| 5 | The domain's key question | For example "does it work without X?" or "what makes them switch?" |
| 6 | Economics | Price anchors; what a revenue target (e.g. ₪1M/yr) means in units and market share |
| 7 | Risks | Impact and likelihood pills; no mitigations |
| 8 | What to check | Interview plan box; confidence table; methods and sources folded |

Footer: numbers marked as estimates are the author's calculation, not interview data.

## Phase 4 — Verify

1. Run `node --check` on the extracted `<script>`.
2. Recompute every derived number in a scratch script (shares, multiples, unit counts).
3. Run `python3 assets/screenshot.py report.html out`. Both widths must print OK. Then view the PNGs.
4. Check bidirectional text: in RTL pages, wrap mixed numbers in `.num`, which uses an LTR isolate, or put them in their own column.

## Phase 5 — Deliver

Publish the report as an artifact. Reply in two or three lines: what the report covers, that sharing happens through the Share menu, and the next step if there is one.

## Failure modes seen in practice

- Published without looking. The page was ugly and broke on mobile.
- Recommendations crept in through words like "focus" or "best bet", or through a mitigation column.
- TAM/SAM/SOM was used before the problem was defined.
- The criteria left out "impact on the outcome", so the status quo won on convenience alone.
- One chart was repeated per segment instead of one unified table.
- Unmet needs were buried at the end instead of shown upfront.
- Methodology paragraphs sat in the body instead of in the folds.
- Long, convoluted sentences. The bar is a crisp chat answer: short claims, numbers, sources.
