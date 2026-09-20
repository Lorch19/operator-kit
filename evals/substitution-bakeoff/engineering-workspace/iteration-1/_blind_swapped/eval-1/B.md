# Dropped tickers in the nightly run — diagnosis

**Skill: `[SKILL]`** (Phases 1–6), with `[SKILL]`
supplying the Phase 5 regression test.

---

## The short version

You do not have a hypothesis problem. You have a **measurement** problem, and the
measurement you need is already sitting on disk.

"No pattern I can see" is the load-bearing claim in your report, and it is almost
certainly an *eyeball* of a list rather than a computed result. It is also the single
most valuable fact in this bug, because one cheap calculation over it splits the
hypothesis space roughly in half and cannot be argued with:

> **Are the same tickers dropped every night, or different ones each night?**

- **Same tickers** → the cause is an *attribute* of those tickers (symbol format, a null
  required field, listing venue, a corporate action). The bug is deterministic and you can
  read the answer straight off the dropped list.
- **Different tickers** → the cause is in the *run*, not the ticker (concurrency,
  transient vendor errors, retry exhaustion, timeouts, batch boundaries). No amount of
  staring at ticker metadata will ever find it.

At ~1 in 50 over 14 nights you already have on the order of **100–150 drop events**
recorded in your existing nightly outputs. You do not need to wait for tonight. The
harness below reconstructs the whole table from artifacts you already have, in seconds.

**Run this first** (Phase 1, `backfill` mode):

```bash
python3 harness/ticker_audit.py backfill \
  --outputs "data/nightly/*.parquet" \
  --universe data/universe.txt \
  --key ticker
```

Everything after this point is conditioned on what that prints.

---

## Questions I would have asked, and what I assumed instead

This ran unattended, so here are the questions, with the assumption I proceeded on. Each
one that is wrong changes something specific, named below.

| # | Question | Assumed | What changes if I'm wrong |
|---|---|---|---|
| 1 | Are the dropped tickers the *same ones* each night, or different? | **Unknown — this is the first thing to measure.** I have built the measurement rather than guessed the answer. | Nothing; the harness answers it. |
| 2 | How big is the universe? | ~500 names, so ~10 drops/night | Only the arithmetic. At 5,000 names the drop *count* is 100/night and rate-limit hypotheses (H2) rise sharply. |
| 3 | Is there a definitive input universe list the run starts from? | Yes, and it is persisted per night | If the universe is itself computed fresh each night, **the drop may be upstream of the pipeline entirely** — the ticker was never requested. Use `--universe-glob` to audit per-night universes; this is a real and commonly-missed case. |
| 4 | Does the pipeline fan out concurrently (threads / asyncio / Spark / multiprocessing)? | Yes — near-universal for this shape | If it is strictly serial, H1 and H2 drop to the bottom and H4/H5 rise to the top. |
| 5 | Does it hit an external data vendor per ticker? | Yes | If all data is local, H2 (rate limiting) dies outright. |
| 6 | "Two weeks" — was there a deploy, dependency bump, universe expansion, or vendor plan change around then? | Unknown | The `backfill` per-night series shows **step vs ramp**. A step means a change landed; cross-reference `git log --since="3 weeks ago"`. A ramp means growth crossed a limit. This is high-information and free. |
| 7 | "Drops" — missing from the output file, or missing from the downstream dashboard/DB? | Missing from the pipeline's own output | If the row exists in the output but not downstream, the bug is in the **load/read** step and the entire fetch-side hypothesis set is wasted effort. Worth 30 seconds to confirm. |
| 8 | Does the run report *any* errors on a night that drops tickers? | Some, but fewer than the drop count | If error count == drop count, this is a 20-minute fix (the errors name the cause). If errors == 0, the swallow is total and H1 jumps to near-certain. |

**Assumption I am most worried about: #3.** If the universe is regenerated nightly rather
than pinned, "the pipeline dropped a ticker" and "the universe builder never included it"
look identical in the output and have completely disjoint fixes.

---

## Phase 1 — The feedback loop

This is the skill. Everything downstream is mechanical; if the loop is tight, the bug is
90% found. I built three, in increasing cost and decreasing speed-to-answer.

I cannot run these against your repository, so I validated all three against a synthetic
pipeline (`harness/fake_pipeline.py`) that injects six real drop mechanisms transcribed
from production code. Every command and every output below was **actually executed**.

### Loop A — `audit`: the pass/fail signal (51 ms)

Set-difference of the universe against the output. This is the red/green.

```
$ DROP_MODE=none python3 fake_pipeline.py universe.txt out.csv
$ python3 ticker_audit.py audit --universe universe.txt --output out.csv --key ticker
[GREEN] universe=500 produced=500 unique=500 missing=0 (0.00%)
exit=0

$ DROP_MODE=pool_swallow python3 fake_pipeline.py universe.txt out.csv
$ python3 ticker_audit.py audit --universe universe.txt --output out.csv --key ticker
[RED] universe=500 produced=492 unique=492 missing=8 (1.60%)
  dropped  (8): JPM, SMB, KHMN, EEE, ULH, CUNX, QNQ, UIU
exit=1

$ time python3 ticker_audit.py audit ...
0.05s total
```

Against the completion criterion in the skill:

- [x] **Red-capable** — asserts your exact symptom (a ticker present in the input is
      absent from the output), not "ran without erroring".
- [x] **Deterministic** — pure set arithmetic; identical verdict every run.
- [x] **Fast** — 51 ms on 500 rows.
- [x] **Agent-runnable** — exit 0/1, no human in the loop.

It also separates two things that look identical in a row count and have different fixes:

```
$ DROP_MODE=symbol_collision python3 fake_pipeline.py universe.txt out.csv
$ python3 ticker_audit.py audit --universe universe.txt --output out.csv --key ticker
[RED] universe=502 produced=500 unique=500 missing=2 (0.40%)
  MANGLED  (2) - present under another spelling, not dropped: BRK.B, BF.B
```

`BRK.B` was not dropped. It was **renamed to `BRK-B` and then deduplicated against its
own twin.** A row-count check would have told you "2 missing" and sent you hunting in the
fetch layer for a bug that lives in the join key. The harness also counts duplicates,
because a fan-out join and a silent drop can produce the *same* row count.

### Loop B — `backfill`: the answer from artifacts you already have (seconds, no waiting)

The important one. Fourteen nights of existing outputs, audited at once. Below, I seeded a
clean stretch and then "deployed" the bug on night 6:

```
$ python3 ticker_audit.py backfill --outputs "nights/*.csv" --universe universe.txt --key ticker
=== per-night ===
2026-09-01.csv       universe=502  produced=502  missing=  0 (0.00%)
2026-09-02.csv       universe=502  produced=502  missing=  0 (0.00%)
2026-09-03.csv       universe=502  produced=502  missing=  0 (0.00%)
2026-09-04.csv       universe=502  produced=502  missing=  0 (0.00%)
2026-09-05.csv       universe=502  produced=502  missing=  0 (0.00%)
2026-09-06.csv       universe=502  produced=490  missing= 12 (2.39%)
2026-09-07.csv       universe=502  produced=494  missing=  8 (1.59%)
2026-09-08.csv       universe=502  produced=493  missing=  9 (1.79%)  MANGLED=1
2026-09-09.csv       universe=502  produced=495  missing=  7 (1.39%)
2026-09-10.csv       universe=502  produced=491  missing= 11 (2.19%)
2026-09-11.csv       universe=502  produced=495  missing=  7 (1.39%)
2026-09-12.csv       universe=502  produced=492  missing= 10 (1.99%)
2026-09-13.csv       universe=502  produced=488  missing= 14 (2.79%)
2026-09-14.csv       universe=502  produced=490  missing= 12 (2.39%)

=== stability ===
runs=14 (with drops: 9)  mean drops/run=10  drop rate=1.99%
unique tickers ever dropped=80  total drop events=90
pairwise Jaccard: observed=0.0141  expected-if-random=0.0101  repeat-offender share=0.222
VERDICT: RUN-DEPENDENT - different tickers each run, overlap indistinguishable from
chance. The cause is in the RUN, not the ticker: concurrency, transient I/O, retry
exhaustion, timeouts, partial-batch handling.
```

Two findings in one command: the **step change on night 6** (a change landed; go find it
in `git log`) and the **run-dependent verdict**.

**How the verdict is computed, so you can trust or reject it.** It compares the observed
pairwise Jaccard overlap between nightly dropped-sets against the overlap you'd expect if
each night picked its victims uniformly at random. For *k* drops from a universe of *N*,
E|A ∩ B| ≈ k²/N, so E[J] ≈ k / (2N − k). Observed ≫ expected means the victims share an
attribute. Observed ≈ expected means chance. This matters because **a naive eyeball is
badly miscalibrated here**: in the stochastic run above, 22% of drop events landed on a
repeat offender purely by birthday-paradox coincidence. Stare at that list and you *will*
invent a pattern. The null baseline is what stops you.

Proof the discriminator actually discriminates — same harness, two classes of cause:

| `DROP_MODE` | Real mechanism | Observed *J* | Expected if random | Verdict |
|---|---|---|---|---|
| `pool_swallow` | worker future raises, `except: continue` eats it | 0.0106 | 0.0093 | RUN-DEPENDENT ✅ |
| `symbol_collision` | `BRK.B`→`BRK-B`, dedup kills the twin | **1.0** | 0.002 | DETERMINISTIC ✅ |
| `dropna` | required field null, filtered by an inner join | **1.0** | 0.009 | DETERMINISTIC ✅ |
| `tail_batch` | final partial batch discarded | **1.0** | 0.057 | DETERMINISTIC ✅ |

Two orders of magnitude of separation. This is not a judgement call.

### Loop C — `replay`: raise the reproduction rate

A 2% bug is not debuggable one night at a time. `replay` runs the pipeline N times against
a pinned universe and aggregates, converting "1 in 50, once a night" into a signal you can
bisect against in a single sitting:

```
$ python3 ticker_audit.py replay \
    --cmd "python3 fake_pipeline.py universe.txt out.csv" \
    --universe universe.txt --output out.csv --key ticker \
    --runs 30 --env DROP_MODE=pool_swallow
run  27: missing=  9  AB, BAL, CJ, NAM, PP, QRO, RZ, UA
run  28: missing=  8  EV, LC, LML, MEIJ, OEJ, PG, TXVK, YBD
run  29: missing=  9  DGF, EJZE, LZE, MSFT, NSAT, OFDB, QJPA, YDQ
...
runs=30 (with drops: 30)  mean drops/run=9.2  drop rate=1.84%
unique tickers ever dropped=209  total drop events=276
```

30/30 runs red. If your real pipeline is too slow to run 30×, shrink the universe to 50
names and raise `--runs`; the per-item failure probability is what you're sampling, not
the universe. `--env` lets you sweep one variable at a time in Phase 4 (see below).

**Honest limitation:** these runs exercise a synthetic pipeline, so they prove the
*harness* is red-capable and correctly classifies known causes. They do not prove anything
about *your* code. The first genuinely load-bearing run is you pointing `backfill` at your
real `data/nightly/` directory.

---

## Phase 2 — Reproduce and minimise

Once `replay` is red against your pipeline, shrink it. Cut one thing at a time, re-running
after each cut, and keep only what stays red:

1. **Universe** — binary-search it down. 500 → 250 → 125… If the drop rate holds steady as
   the universe shrinks, it is **per-item**. If the drop *count* stays constant while the
   universe halves, it is **per-run** (a fixed tail, a deadline, a boundary) — a very
   different bug, and the cut tells you which for free.
2. **Stages** — run fetch only, then fetch+enrich, then the full chain. First stage that
   goes red owns the bug. (The census in Phase 4 does this without code surgery.)
3. **Concurrency** — `max_workers=1`. If the drop vanishes, H1/H2 are confirmed as a class.
4. **Vendor** — swap live calls for a cached fixture. Still red → the bug is yours, not the
   vendor's. Green → it is I/O-conditional.
5. **Date** — pin the run date. If drops only occur on certain dates, look at corporate
   actions and market holidays.

Done when removing any remaining element makes it go green.

---

## Phase 3 — Ranked hypotheses

Five, ranked, each with the prediction that falsifies it and the one-line probe. Ranking
below assumes the **RUN-DEPENDENT** verdict, which is what "no pattern I can see" weakly
suggests. The re-ranking table follows.

**H1 — A per-item exception is swallowed in the concurrency layer.** *(most likely)*
The classic: `as_completed` inside `try/except Exception: continue`, or
`asyncio.gather(..., return_exceptions=True)` whose exception results are filtered out
instead of raised, or `executor.map` consumed inside a broad `try`.
- **Predicts:** rows_written + errors_logged < universe_size on a dropping night. Setting
  `max_workers=1` makes the drop vanish *or* turns it into a hard crash.
- **Probe:** `grep -rn -B3 -A3 -E "except (Exception|BaseException)" --include=*.py . | grep -E "continue|pass"` and
  `grep -rn "return_exceptions=True" .`
- **Why #1:** it is the only hypothesis that explains *silence*. A vendor error, a timeout,
  and a rate limit all normally leave a log line. Two weeks with no log to point at is
  itself evidence that something is eating the evidence.

**H2 — Retry exhaustion on vendor rate limiting (429 / 503).**
- **Predicts:** drop rate scales with concurrency and with universe size. Halving
  `max_workers` roughly halves it. Drops cluster **late** in the run as the token bucket
  drains, not uniformly.
- **Probe:** log an HTTP status histogram for one night; correlate drop timestamps against
  wall-clock position in the run. Uniform → not H2. Back-loaded → H2.
- **Two-week fit:** a vendor silently tightening a quota, or your universe crossing their
  per-minute limit, both land exactly this way.

**H3 — Per-ticker timeout, or a global deadline truncating the run.**
- **Predicts:** drops correlate with the fetch-latency distribution — the slowest names
  and the tail of the run. Raising the timeout 10× makes them disappear.
- **Probe:** record per-ticker fetch duration for one night; plot dropped vs kept latency.
  If dropped names sit in the p99 of latency, it is H3.
- **Distinguishes from H2:** H3's victims correlate with *latency*; H2's with *position*.

**H4 — A batch / pagination boundary drops a partial group.**
- **Predicts:** **deterministic** — the same tickers every night, and the count is a
  function of `len(universe) % batch_size`. Changing `batch_size` changes both which and
  how many, predictably.
- **Probe:** `replay` with `--env BATCH_SIZE=64` then `=100`. If the dropped set changes
  with batch size, it is H4 and nothing else.
- **Note:** my `tail_batch` fixture produced 54 drops from a 502-name universe at
  batch 64 — 10.8%, far above your 2%. A boundary bug's rate is set by the modulus, so it
  rarely lands near 2% by accident. This is ranked 4th on *rate* grounds, not on plausibility.

**H5 — The rows are produced but not persisted (or not read back).**
Upsert conflict swallowed, non-atomic write, a downstream filter, an `INNER JOIN` against
a reference table that is missing rows.
- **Predicts:** the stage census shows `fetch in == out` but `persist in > out`. Or the
  pipeline's own log claims N rows written while the table holds N−k.
- **Probe:** the Phase 4 census below localises this in one night.
- **Why it stays on the list:** if the answer to my question #7 is "missing from the
  dashboard", this is #1 and H1–H4 are all wasted effort.

### Re-ranking by what Phase 1 prints

| Verdict from `backfill` | New order | Killed outright |
|---|---|---|
| RUN-DEPENDENT | H1 → H2 → H3 → H5 | H4 (deterministic by construction) |
| DETERMINISTIC | H4 → H5 → *new: symbol normalisation* → *new: null required field* | H1, H2, H3 |
| MIXED | Split the repeat offenders out and treat as **two bugs**; the deterministic subset is usually the easy one — fix it first to clear the noise | — |
| MANGLED > 0 | Symbol normalisation, immediately | all others until resolved |

Under DETERMINISTIC, the two hypotheses to add are the ones my fixtures show are most
common in ticker pipelines: **symbol normalisation collisions** (`.`/`-`/`_` conventions
differing between two vendors — the audit's MANGLED counter catches this directly) and a
**null required field** meeting a `dropna()` or an inner join.

---

## Phase 4 — Instrumentation

One probe per prediction, one variable at a time. Not "log everything and grep".

**The highest-yield probe by a wide margin is a stage census** — it localises the drop to a
stage in a single night, killing every hypothesis about the other stages at once. Drop-in
module at `harness/stage_census.py`, every line tagged `[DEBUG-7c31]` so cleanup is one
grep:

```python
from stage_census import census

with census("fetch", universe) as c:
    rows = fetch_all(universe)
    c.out([r.ticker for r in rows])

with census("enrich", [r.ticker for r in rows]) as c:
    enriched = enrich(rows)
    c.out([r.ticker for r in enriched])

with census("persist", [r.ticker for r in enriched]) as c:
    c.out(upsert(enriched))
```

Executed output:

```
[DEBUG-7c31] stage=fetch      in=500   out=498   lost=2   dupes=0   gained=0   LOST=T042,T137
[DEBUG-7c31] stage=enrich     in=498   out=498   lost=0   dupes=0   gained=0
[DEBUG-7c31] stage=persist    in=498   out=499   lost=0   dupes=0   gained=1
[DEBUG-7c31] stage=persist GAINED=['T042']
```

It tracks `gained` and `dupes` as well as `lost`, because a stage that resurrects a stale
row (as `persist` does above) hides a real loss behind a correct-looking total.

Sweeps, one variable at a time, each tied to a prediction:

| Probe | Command | Reading |
|---|---|---|
| H1 | `replay --runs 20 --env MAX_WORKERS=1` | drops → 0, or a crash appears: **H1 confirmed** |
| H2 | `replay --runs 20 --env MAX_WORKERS=4` vs `=16` | rate tracks workers: **H2** |
| H2/H3 | log fetch start-time + duration + status per ticker, one night | dropped cluster late → H2; dropped are slowest → H3 |
| H3 | `replay --env FETCH_TIMEOUT=300` | drops → 0: **H3** |
| H4 | `replay --env BATCH_SIZE=64` vs `=100` | dropped *set* changes with batch size: **H4** |
| H5 | stage census | `persist in > out`: **H5** |

Cleanup at the end: `grep -rn 'DEBUG-7c31' .` — tagged logs die, untagged logs survive.

---

## Phase 5 — Fix and regression test

Written **before** the fix, per the skill.

### The seam

`run_nightly(universe) -> {"rows", "failures"}`.

This is the **correct** seam, and that matters. A unit test on `fetch()` cannot catch this
bug — `fetch()` raises perfectly correctly. The defect lives in the *aggregation boundary*
that decides what to do with that exception, so the test has to observe that boundary. A
test one level lower would pass while the bug shipped: false confidence, which the skill
explicitly warns is worse than no test.

**The tdd skill requires seams be confirmed with you before any test is written.** I could
not ask, so: I am testing at `run_nightly`, and at the per-stage boundary if your stages
are separately callable. If your real entry point is a DAG task rather than a function,
the same invariant goes in a task-level integration test — the seam moves, the assertion
does not.

### Red

```
$ IMPL=pipeline_legacy python3 -m pytest test_no_silent_drops.py -q

        assert "T042" not in {r["ticker"] for r in result["rows"]}
>       assert "T042" in {f["ticker"] for f in result["failures"]}, \
            "T042 failed and was silently dropped instead of reported"
E       AssertionError: T042 failed and was silently dropped instead of reported
E       assert 'T042' in set()

FAILED test_no_silent_drops.py::test_every_ticker_is_either_a_row_or_a_named_failure
FAILED test_no_silent_drops.py::test_a_vendor_error_surfaces_as_a_failure_not_a_missing_row
2 failed, 1 passed in 0.04s
```

The third test — a clean run produces the whole universe — passes in *both* implementations
on purpose. It is the control: it proves the suite can go green, so a green means something.

### The fix

Not "catch that one exception". The bug class is **silent drop**, and patching one
mechanism leaves the other five live. Make a silent drop *structurally impossible* by
enforcing a conservation invariant at every stage boundary:

> **in == out + explicitly-failed.** Every input ticker leaves the stage as either a row or
> a named failure. A stage that cannot say what happened to a ticker refuses to close.

```python
class TickerLedger:
    """in == out + failed, checked at every stage boundary."""
    def close(self):
        seen = set(self.ok) | {f["ticker"] for f in self.failed}
        unaccounted = [t for t in self.expected if t not in seen]
        if unaccounted:
            raise LedgerBreach(
                f"stage {self.stage!r} lost {len(unaccounted)} ticker(s) with no reason "
                f"recorded: {unaccounted[:10]}"
            )
        return self.failed
```

The `except Exception` stays — you do want one bad ticker not to kill the run. What changes
is that it now **records a reason** instead of `continue`. Full implementation in
`harness/pipeline_fixed.py`.

### Green

```
$ IMPL=pipeline_fixed python3 -m pytest test_no_silent_drops.py -q
...                                                                      [100%]
3 passed in 0.02s
```

Then re-run the Phase 1 loop against the original un-minimised nightly run.

### Ship the loop, not just the fix

`ticker_audit.py audit` should run as the **last step of every nightly run**, failing the
job on a non-empty diff. A pipeline that can lose 2% of its universe for two weeks without
anyone being paged does not have a fetch bug; it has a missing invariant. The fix for the
mechanism takes an afternoon. The fix for the *silence* is the audit gate, and that is
what stops the next variant of this bug.

---

## Phase 6 — Cleanup and post-mortem

Before declaring done:

- [ ] Original repro no longer reproduces — re-run `backfill` over post-fix nights
- [ ] Regression test passes at the `run_nightly` seam
- [ ] `grep -rn 'DEBUG-7c31' .` returns nothing
- [ ] Validation fixtures deleted (`fake_pipeline.py`, `pipeline_legacy.py`, `pipeline_fixed.py`,
      `universe.txt`) — keep `ticker_audit.py`, it is now production tooling
- [ ] The hypothesis that turned out correct is named in the commit message

**What would have prevented this?** Not a better `except` block. Three things, in order of
value:

1. **The conservation invariant.** The pipeline had no notion of "I was asked for 500 and
   produced 490". Row counts were tracked; *identities* were not. Every stage boundary that
   moves a set of entities should assert set conservation, not row count.
2. **A reconciliation gate in the nightly job.** Two weeks of silent data loss means the
   only detector in the system was a human noticing. That is the actual incident.
3. **Errors that cannot be swallowed by default.** `except Exception: continue` in a fan-out
   loop is the single highest-yield grep in any batch pipeline.

Item 1 is architectural — the absence of a boundary that could hold the invariant. Per the
skill, that is a `/improve-codebase-architecture` handoff, and it should be made **after**
the fix lands, with the specifics: *the stage boundaries in the nightly pipeline are
implicit (lists passed between functions) rather than explicit objects that can enforce
conservation.* Making them explicit is what turns this from a bug you fix into a bug class
you retire.

---

## Stress Test

**The weakest thing here.** Every number in this document came from a synthetic pipeline I
wrote. I validated the *instrument*, not your system. If your pipeline's shape differs from
my mental model — it's a Spark job, an Airflow DAG with per-ticker tasks, a vendor bulk
endpoint rather than per-ticker calls — then H1–H3 are mis-ranked, though the Phase 1 loop
and the conservation invariant survive intact because they make no assumption about shape.

**Assumptions that could be wrong.**
- *That a stable "universe" exists to diff against.* This is the big one. If the universe is
  computed nightly, my entire Phase 1 measures the wrong boundary and the bug may be
  upstream. Question #3 is the one to resolve before anything else.
- *That "drops" means absent from the output file.* If it means absent downstream, H5 is #1
  and four hypotheses are dead weight.
- *That ~2% is one bug.* At 1-in-50 over 14 nights, a 0.5% deterministic cause hiding under
  a 1.5% stochastic one would produce exactly this report and my MIXED verdict is the only
  thing that would catch it. Do not stop at the first cause found.
- *That two weeks of clean history precedes it.* I assumed a step change. If `backfill`
  shows drops going back months at a lower rate, "it started two weeks ago" is an
  observation about *when someone looked*, not when it began — and the deploy-hunt is a
  dead end.

**What a smart critic would say.** Three things.

*"You built tooling instead of finding the bug."* Fair on its face, and wrong here. With no
repository access, a hypothesis list is worth very little — I'd be guessing at code I can't
read. The Jaccard table above is the defence: a plausible-sounding hypothesis list would
have sent you hunting for a ticker attribute in a bug where 22% of repeat offenders were
pure coincidence. The instrument earns its place precisely because the eyeball is
miscalibrated on this bug.

*"Your stability verdict has a small-sample problem."* Correct, and I'd rather name it than
bury it. At 9 nights with drops and ~10 drops each, the pairwise Jaccard estimate is noisy;
the DETERMINISTIC/RUN-DEPENDENT thresholds (10× and 3× the random baseline) are chosen to
be far outside that noise, which is why the fixtures separated by two orders of magnitude
rather than a few percent. A MIXED verdict genuinely is ambiguous and should be treated as
"collect more nights", not as a finding.

*"The conservation invariant will now crash the nightly run on a single bad ticker."* Yes,
and that is a real trade-off, not a free win. The choice is between a job that fails loudly
on one unaccounted ticker and a job that silently loses 2% for a fortnight. If a hard fail
is wrong for your operations, the invariant should degrade to a loud alert plus a written
failure manifest — but it must not degrade back to silence. That decision is yours and I'd
want to make it explicitly rather than by default.

---

## Files

All paths under `.../eval-1/A/outputs/`:

| File | Keep? | What it is |
|---|---|---|
| `harness/ticker_audit.py` | **Yes — production tooling** | The feedback loop: `audit` / `replay` / `backfill` |
| `harness/stage_census.py` | Until fixed | Phase 4 per-stage census, tagged `[DEBUG-7c31]` |
| `harness/test_no_silent_drops.py` | **Yes — port to your repo** | Phase 5 regression test at the `run_nightly` seam |
| `harness/pipeline_fixed.py` | Reference | `TickerLedger` conservation invariant |
| `harness/pipeline_legacy.py` | Delete | The dropping shape, for the red run |
| `harness/fake_pipeline.py` | Delete | Validation fixture, 6 injectable drop mechanisms |
| `harness/universe.txt` | Delete | 502-name synthetic universe |
