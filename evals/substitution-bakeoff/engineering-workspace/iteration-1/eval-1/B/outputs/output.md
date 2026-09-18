# Silent ticker drops in the nightly run — root-cause investigation

**Skill:** `superpowers:systematic-debugging`, Phases 1–4, with `superpowers:test-driven-development` for Phase 4's failing test.

---

## What I am deliberately not doing yet

> **The Iron Law:** NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.
> If Phase 1 isn't complete, you cannot propose fixes.

I am not going to hand you a list of likely causes. I could write one — five stories that all fit "about 2% of tickers vanish, no error, every night" — and that would be actively harmful, because **every one of them fits the evidence you currently have equally well.** A ranked guess list at this stage sends you editing code with roughly a 1-in-5 chance of touching the right file, and a 2%-per-night failure rate is exactly slow enough to hand you a false confirmation: change something, watch one clean night, declare victory. At 2% and ~500 tickers, a night with zero drops happens by chance often enough that "it looks fixed" means almost nothing.

The blocker is not that we don't know the cause. **The blocker is that you cannot yet make the bug happen on demand.** Phase 1 of systematic debugging is explicit about this: *"Reproduce consistently. If not reproducible → gather more data, don't guess."* You are in the not-reproducible branch, so the work is gathering data, and that is what everything below is.

Skip to [§5](#5-the-discrimination-table--gated) if you want the cause list; it is written, but it is deliberately placed after the instrument that tells you which row applies, because reading it first is how you end up "fixing" the wrong one.

---

## §0 — The questions I'd have asked first

This runs unattended, so here they are with the assumption I proceeded on. Any answer that differs changes what you should run.

| Question | Why it changes the approach | Assumption I proceeded on |
|---|---|---|
| How do you know a ticker was dropped? | If it's "the output file is short" vs "a named ticker is missing from a diff" vs "a downstream consumer complained", you have three different and differently-blind instruments. | You diff the nightly output against an expected universe list, or noticed absences downstream. |
| Is the universe fixed or does it change nightly? | A moving universe means "missing" may be correct, and your 2% may be partly legitimate. | The universe is roughly fixed night to night (a few hundred names). |
| Does the run exit 0? Any WARN/ERROR lines? | A swallowed exception usually leaves a log line even when it doesn't raise. If the logs are truly clean, that rules out a whole class. | Exit 0, no errors noticed — this is the "silent" in silent drop. |
| What changed ~2 weeks ago? | Phase 1.3. This is the single highest-value question in the whole document. | Unknown. **Please answer it — see the command in §3.0.** |
| Does the pipeline fan out concurrently? | Decides whether the stochastic branch is even reachable. | Assumed yes (typical for a nightly fetch), but not required by anything below. |
| Do you keep the nightly output files? | The entire §3 Move 1 depends on having ~14 nights of artifacts. | Yes — if not, §3 Move 2 still works, it just costs you nights instead of minutes. |

**Also:** "it's been happening for two weeks" is when you *noticed*. Treat the start date as unknown until §3 Move 1 prints the per-night rate. If the rate is flat back through older artifacts, the two-week framing is wrong and you'll waste a day bisecting commits from a window that contains nothing.

---

## §1 — "No pattern I can see" is a measurement gap, not randomness

This is the part I'd push back on hardest, and it is good news.

**The arithmetic.** One in fifty, on a universe of ~500, over fourteen nights, is roughly **140 drop events**. That is not a rare intermittent glitch you have to sit and wait for. That is a dataset — a large one — that has already been generated and is sitting in your output directory right now. A real pattern in 140 observations would be loud. So:

> "No pattern I can see" almost certainly means **no instrument has looked**, not that no pattern exists.

**The proxy trap.** Here is the specific reason you can't see it. You are inferring drops from *absence in the final output*. Absence at the end of a pipeline is a **proxy** for the drop event; it is not the drop event. It tells you a ticker is not in the output. It cannot tell you:

- at which stage it stopped being present,
- whether it was ever fetched at all,
- whether it was excluded on purpose by some rule nobody remembers,
- or whether it was present and then overwritten.

Every one of those is a different bug, and the output diff collapses all of them into one undifferentiated symptom. You are not failing to see a pattern; you are looking at a shadow and trying to read its face.

**Three things "no pattern" could mean.** All three are measurement gaps, and §3 distinguishes them in minutes:

1. **The pattern is in a dimension you haven't plotted.** Not the ticker's name but its *position* in the processing order, its batch index, or the wall-clock second it was fetched. A pagination bug that loses the last item of every 50-item page looks like noise if you only ever look at symbol names.
2. **There are two bugs.** A stable recurring core plus a random tail. Overlay them and each masks the other's signature.
3. **It really is timing-dependent** — and "no pattern in the ticker names" is then the *correct* finding and a strong positive clue, not a dead end.

None of those is "it's random, nothing to be done."

---

## §2 — Define "red" before building anything

Before writing a line, state what success looks like, so I don't build an instrument that measures the wrong thing.

**Target: one command, `make red`, that**

| Property | Why it's non-negotiable |
|---|---|
| **Exits non-zero when a ticker is lost** | An exit code is the only signal CI, a scheduler, and a bisect script can all read. Today the run exits 0 whether it drops 0 or 50. |
| **Names the ticker AND the stage boundary** | "Nine missing" is where you are now. "Nine missing, all at `enrich`" is a solved bug. |
| **Runs in seconds, not overnight** | A feedback loop with a 24-hour cycle time is not a feedback loop. This is the whole reason for the replay path in §3. |
| **Fails for the right reason** | TDD's Verify-RED step. A test that errors on a typo isn't red, it's broken. |
| **Is deterministic, or reproducible-by-seed** | If the loop is itself flaky you cannot tell a fix from a lucky run. |

Everything below exists to produce that command.

---

## §3 — Building the loop, in three moves

### Move 0 — Answer the "what changed" question (2 minutes)

Phase 1.3 of the skill, and the cheapest high-value thing you can do. Run this before anything else:

```bash
# Commits to the pipeline in the window before the drops started.
# Widen to 30 days: "two weeks" is when you noticed, not necessarily when it began.
git log --since='30 days ago' --until='10 days ago' --oneline --stat -- <pipeline-path>

# Dependency changes are the usual silent culprit and are easy to forget.
git log --since='30 days ago' -p -- requirements.txt poetry.lock Pipfile.lock pyproject.toml

# Did anything change that ISN'T in git? Config, a vendor plan, a cron schedule:
git log --since='30 days ago' --oneline -- '*.yaml' '*.yml' '*.toml' '*.ini' '*.env*'
```

**What each result tells you:** a change to the fetch/join/dedupe logic in that window is your prime suspect and gets tested first in §5. **An empty result is equally informative** — it means the trigger was external (a vendor API change, a data volume crossing a threshold, a universe that grew past a page boundary), and you should stop reading the diff and go to Move 1.

### Move 1 — Retro-reproduce from artifacts you already have (minutes, no code change)

You have ~14 nights of output files. That is 140 drop events already recorded. `drop_forensics.py` (delivered, stdlib only) reads them and answers the one question that splits the cause space in half:

> **Do the same tickers drop every night, or a different set each night?**

The statistic it uses: if drops were independent chance events at rate *p*, then across *N* nights you'd expect about `|U| × (1 − (1−p)^N)` **distinct** tickers to have ever dropped. Compare that to the actual number of distinct droppers. Far fewer than expected → the same names keep recurring → the drop is a deterministic property of those tickers. Close to expected → a different set each night → it isn't about the tickers at all.

```bash
python3 drop_forensics.py --nights 'out/*.json' --universe universe.txt
# also accepts .csv / .jsonl / .txt; --symbol-col if the column isn't auto-detected
```

I ran it against fourteen nights generated from each of the two scenarios. **Real output, both correctly classified:**

```
                          deterministic cause          stochastic cause
total drop events                    126                        157
distinct tickers involved              9                        128
expected distinct if chance        112.4                      136.3
concentration ratio                 0.08                       0.94
recurrence histogram     {14 nights: 9}   {1 night:104, 2:20, 3:3, 4:1}

VERDICT             DETERMINISTIC — same          STOCHASTIC — a different
                    tickers drop repeatedly       set drops each night
```

Note how different those are. **Both scenarios produce the identical surface symptom** — ~2% lost, exit code 0, nothing in the logs — and this one command separates them decisively. That is the entire value of building an instrument before theorising.

It also profiles the dropped names against the kept ones (dots, hyphens, length, digits, whitespace, non-ASCII) and tests whether drops cluster at a fixed position within common batch sizes (10/16/25/32/50/64/100/128/250) — which is how a pagination or chunking bug reveals itself. On the stochastic scenario every property lift came back near 1.0, i.e. **the instrument correctly reports "no symbol property explains this"**, which is a real finding rather than a shrug.

> **Caveat, stated because it bit me:** in the deterministic scenario the profiler flagged "contains `-`" at 6.9× lift — but that was 2 of 9 tickers. With only nine droppers, a 6.9× lift is noise. Treat property leads with fewer than ~20 droppers as hypotheses to test, never as findings. The recurrence verdict is the robust number; the property profile is a hint generator.

### Move 2 — Arm the ledger so the *next* run records the event

Move 1 tells you *whether* it's about the tickers. It still can't tell you *where* they're lost, because the artifacts only capture the end state. For that, the pipeline has to account for itself at each boundary — this is Phase 1.4 of the skill, *"gather evidence in multi-component systems: log what enters and what exits each component, run once, then analyse."*

**In plain English:** every stage of the pipeline is made to hand in a receipt. It gets N tickers, it passes on M, and if M < N it must name which ones it dropped and why. A stage may legitimately shed tickers — halted, delisted, no trade — but it has to *declare* them. Anything lost without a declaration is an unaccounted loss and stops the run. That one rule converts "a ticker silently vanished" into "stage `enrich` lost 9 undeclared tickers", which is a different and much smaller problem.

`ledger.py` is delivered and has no dependency on my stand-in — it only needs the set of symbols entering and leaving each stage. **Porting it is four lines per boundary:**

```python
before = {r.symbol for r in rows}
rows = my_stage(rows)                       # your existing, unmodified stage
after  = {r.symbol for r in rows}
led.checkpoint("my_stage", before, after, declared=my_stage_exclusions)
```

Note what this does *not* require: you do not have to guess which stage is guilty first. You wrap all of them and let the run tell you. **Real output from `diagnose.py`, the same universe under two different causes:**

```
   inner-join cause                      swallowed-exception cause
   stage        in   out  delta          stage        in   out  delta
   fetch       506   506      0          fetch       506   494    -12  <-- LOSS
   normalize   506   506      0          normalize   494   494      0
   enrich      506   497     -9  <-LOSS  enrich      494   494      0
   persist     497   497      0          persist     494   494      0

   unaccounted at enrich: 9 (1.78%)      unaccounted at fetch: 12 (2.37%)
   ['BL','BW','C','LEN-A','MDG', ...]    ['BF.A','BF.B','BRK.A','BRK.B', ...]
```

The left column localises the bug to a single function in one run. The right column does more than localise — the dropped set is *entirely dotted symbols*, which names the mechanism outright.

**Finding your boundaries in the repo.** If you're unsure where the stage seams are, these greps find the places rows can silently disappear:

```bash
# Swallowed exceptions inside per-ticker loops — the classic invisible drop
grep -rn -A3 -E 'except (Exception|BaseException)?:?\s*$' --include='*.py' . | grep -B2 -E '(pass|continue)'

# Row-count-changing operations that never raise
grep -rn -E '\.(dropna|drop_duplicates|drop|query|filter)\(' --include='*.py' .
grep -rn -E "how\s*=\s*['\"]inner['\"]|\.join\(|pd\.merge\(" --include='*.py' .

# Concurrency: results that can be discarded rather than collected
grep -rn -E 'ThreadPoolExecutor|ProcessPoolExecutor|as_completed|gather\(|\.map\(' --include='*.py' .
grep -rn -E 'return_exceptions\s*=\s*True|timeout\s*=' --include='*.py' .
```

Every hit is a place where the row count can change without an error. Put a `checkpoint` on each side of the ones on the nightly path.

### Move 3 — `make red`

```bash
make red      # exits non-zero if any ticker fails to reach persisted output
```

For your repo, wire the `red` target to replay a **captured** universe — one night's input, pinned to a file — rather than a live fetch. That is what turns an overnight cycle into a seconds-long one, and it is what makes bisecting feasible. The branch from Move 1 tells you which replay to build:

- **DETERMINISTIC verdict** → replay only the ~9 recurring droppers. Sub-second loop, red every time.
- **STOCHASTIC verdict** → replay the same fixed input repeatedly while varying only concurrency. The delivered harness does this by seeding the race: **same seed → identical drop set every run; different seeds → completely different sets.** Seeding the non-determinism is what makes a timing bug testable at all.

```
innerjoin, seeds 1-5:  identical 9 tickers every time
race,      seed 1:  ['CVDM','LIX','MMMM','WYGP']
           seed 2:  ['DFU','EB','FE','FHPN','HUZD','HXD','JFNA','QCD','SCLN','TLOZ','YDDC']
           seed 3:  ['AANX','EMLB','FHPN','HOL','KIJA','MU','OF','ZWVW']
```

---

## §4 — Phase 4: the failing test, written first

Phase 4.1: *"Create Failing Test Case. Simplest possible reproduction. MUST have before fixing."* Here is that test, actually written and actually run. Full transcripts, not a description.

### RED — before any fix code existed

The first test asserts the conservation invariant: every ticker in the universe appears in the persisted output. Expected value is the universe list itself — **derived by hand, never computed by the code under test**, so it cannot degrade into a mirror assertion (`writing-good-tests.md`, Principle 1).

```
$ python3 -m pytest test_no_silent_drops.py -v

E  AssertionError: 9 of 506 tickers (1.78%) never reached persisted output
   and the run exited 0: ['BL','BW','C','LEN-A','MDG','MMMM','SGWC','UEH','UHAL-B']

FAILED test_every_universe_ticker_reaches_persisted_output[inner-join]
FAILED test_every_universe_ticker_reaches_persisted_output[swallowed-exception]
FAILED test_every_universe_ticker_reaches_persisted_output[concurrency]
FAILED test_every_universe_ticker_reaches_persisted_output[dedupe-collision]
FAILED test_every_universe_ticker_reaches_persisted_output[dropna]
5 failed in 0.04s
```

Verified RED for the right reason: it fails on a *missing ticker*, not an import error or a typo, and the message names the tickers.

### RED again — the attribution tests

Test 1 tells you a ticker is gone. That is exactly where you are today, and it is not enough. Tests 2–5 demand the run name the boundary. They were written against a `ledger` module that did not exist yet:

```
$ python3 -m pytest test_no_silent_drops.py -v
E  ModuleNotFoundError: No module named 'ledger'
```

### GREEN — after writing the minimal ledger

```
$ python3 -m pytest test_no_silent_drops.py -q
5 failed, 7 passed in 0.05s
```

The 7 attribution tests pass — the instrument works. **The 5 conservation tests stay red by design**: they reproduce the bug, and they stay red until the *actual root cause* is fixed. The ledger diagnoses; it does not fix. That is the loop you want: a command that is red now, goes green when and only when the bug is really gone, and would go red again if it regressed.

### What break each test catches

`writing-good-tests.md` requires naming the production change that would make each test fail, *before* writing it:

| Test | The break it catches |
|---|---|
| `test_every_universe_ticker_reaches_persisted_output` | Any silent filter, inner join, swallowed exception, dedupe collision, or dropped future, anywhere in the run. |
| `test_ledger_attributes_each_lost_ticker_to_the_stage_that_lost_it` | A stage that changes row count without accounting for the delta. Remove the accounting from one stage and it goes red naming that stage. |
| `test_run_raises_instead_of_exiting_zero_when_a_ticker_is_lost` | Deletion of the `raise`. This is the single line that converts silent into loud; its removal must never pass CI. |
| `test_declared_exclusions_carry_a_reason_and_do_not_trip_the_gate` | An exclusion path that returns no reason — which would let real drops hide behind legitimate ones. |
| `test_ledger_accounts_correctly_under_the_concurrent_stage` | Non-atomic accounting that undercounts under load, i.e. an instrument that lies in precisely the scenario it was built to diagnose. |

**Mutation check.** Mutating the production code — flipping `how="inner"` to `"left"`, removing a `continue`, deleting the lock, returning an empty list — each produces at least one failing test. No mutation passes everything.

### An honest note on what this proves

The harness proves **the tests and the ledger can catch this class of bug**. It proves **nothing about which mechanism is in your pipeline.** I built five plausible causes into a stand-in and confirmed the instrument catches all five; that is a statement about the instrument. Do not let a green harness become a claim about your code.

**And a demonstration of exactly the failure mode you're in:** while building this I read `make red`'s truncated output, saw a lost-set that didn't match my earlier run, and briefly concluded the harness was non-deterministic. It wasn't. I had read the *last* traceback (the `dropna` parameter) as though it were the `inner-join` one. Five full-suite runs fingerprinted identically — one distinct result. I inferred a pattern from a partial, misattributed view of the output, which is the same mistake the output-diff approach invites at scale. The fix in both cases is the same: make the instrument name what it is measuring.

---

## §5 — The discrimination table — *gated*

**Do not read this as a to-do list.** Run Move 1 and Move 2 first. Then find your row. These are not "likely causes"; they are *what the evidence will mean once you have it*, which is the difference between Phase 3 of the skill and guessing.

| Ledger + forensics signature | What it means | The one next command |
|---|---|---|
| Loss at **fetch**, same tickers nightly, dropped set shares a character property (`.`, `-`, length ≥ 5, digits) | Symbol-format handling: a vendor call or parser rejects a notation, exception swallowed by a per-ticker `except: continue` | Replay just those symbols with the `except` re-raising: `python -c "import p; p.fetch(['BRK.B'], strict=True)"` |
| Loss at **enrich/join**, same tickers nightly, no character pattern | Inner join against a reference table that lags the universe | `SELECT u.sym FROM universe u LEFT JOIN meta m USING(sym) WHERE m.sym IS NULL` — if that set equals the dropped set, confirmed |
| Loss at **normalize**, dropped tickers pair up with a survivor under a punctuation-stripped key | Dedupe key collision (`BRK.B` and `BRK-B` → `BRKB`) | `sort universe.txt \| sed 's/[.-]//g' \| sort \| uniq -d` — nonempty output confirms |
| Loss at **normalize**, droppers are all recently listed / short history | `dropna()` on a trailing field that can't be computed yet | Check `min(history_days)` for the dropped set against the window your trailing field needs |
| Loss at **fetch**, **different** set nightly, count correlates with run duration or worker count | Concurrency: unawaited futures, `return_exceptions=True` never inspected, or a lost update | Re-run the same fixed input with `--workers 1`. Twenty clean serial runs vs. lossy parallel ones is your confirmation |
| Loss at **fetch**, different set nightly, drops **cluster in time** | Upstream rate limiting — a 429 handled as "no data" | `grep -c ' 429\| 5[0-9][0-9] ' <vendor-log>` for the run window |
| Drops align to a fixed position mod a batch size, or cluster at the end of the sorted universe | Pagination / chunking: a lost final partial batch or an off-by-one per page | The batch-alignment section of `drop_forensics.py` already prints the batch size and offset |

Phase 3 discipline applies: **one hypothesis at a time, smallest possible change to test it, verify before moving on.** If three fixes fail, stop and question the architecture rather than attempting a fourth (Phase 4.5) — three failures in a row means the pipeline's shape is the problem, not the line you keep editing.

---

## §6 — After the root cause: make the bug structurally impossible

Once the cause is found and fixed, `defense-in-depth.md` applies. A single check gets bypassed by the next refactor:

1. **Entry** — assert the universe loaded is non-empty and the expected size; a truncated universe file is a silent drop upstream of everything.
2. **Business logic** — the `checkpoint` calls stay in permanently. They are not debug scaffolding to be removed; they are the invariant.
3. **Environment guard** — the nightly job exits non-zero when unaccounted losses exceed zero. Not a threshold — zero. A threshold of "under 1%" is how this bug stayed invisible for two weeks.
4. **Instrumentation** — append `report.to_jsonl()` to the nightly log. The next fourteen nights then produce a dataset instead of an anecdote, which is what §3 Move 1 needed and didn't have.

---

## §7 — What I refused to do, and why

| Tempting move | Why it's wrong here |
|---|---|
| Open with five likely causes | All five fit the evidence equally. Ranking guesses is not investigation, and a 2% failure rate will falsely confirm whichever you try first. |
| Add a retry around the fetch | Treats the symptom. If the ticker is lost at the join, retrying the fetch changes nothing and hides the signal. |
| Backfill missing tickers from the previous night | Makes the output look correct and destroys the evidence. The most expensive possible "fix". |
| Alert when the drop count exceeds a threshold | You already have a threshold — your attention — and it missed this for two weeks. The gate is zero unaccounted losses. |
| Fix the most likely cause and watch tomorrow's run | One night at 2% is not evidence of anything. That is the guess-and-check loop the Iron Law exists to prevent. |

---

## §8 — Files delivered

All under `outputs/harness/`, runnable as-is (Python 3, stdlib + pytest; verified on 3.14.3 / pytest 9.0.2):

| File | What it's for |
|---|---|
| **`drop_forensics.py`** | **Run this against your real data first.** Mines your nightly output files for the deterministic-vs-stochastic verdict, property profile, and batch alignment. Stdlib only. |
| **`ledger.py`** | **Port this into your pipeline.** The stage-boundary accountant. No dependency on the stand-in. |
| `test_no_silent_drops.py` | The conservation + attribution test suite. Copy the invariant; the parametrisation is harness-specific. |
| `diagnose.py` | Prints the per-stage in/out/delta table and attributes each loss. |
| `pipeline.py` | Stand-in pipeline with five real drop mechanisms. Exists so the tests have something to go red against. **Not your pipeline.** |
| `Makefile` | `make red`, `make diagnose`, `make forensics`. |

```bash
cd outputs/harness
make red                                            # the loop: exits non-zero
python3 diagnose.py --bugs innerjoin                # localise to a stage
python3 drop_forensics.py --nights 'demo/det/*.json' --universe demo/universe.txt
```

---

## Stress Test

**Weakest part of this analysis.** §3 Move 1 assumes you retained ~14 nights of output artifacts. If the nightly job overwrites one file, the whole retro-reproduction step evaporates and you're down to Move 2, which costs you nights instead of minutes. I'd have caught this with one question I couldn't ask. **Mitigation:** even 3 nights gives a usable recurrence verdict; the script says so when *n* < 3.

**Assumption most likely to be wrong.** That the drop rate is genuinely ~2% and genuinely started two weeks ago. Both numbers come from noticing, not measuring. If the real rate is 2% on weeknights and 8% on Mondays, that seasonal structure *is* the pattern and it's invisible in an aggregate. §3 Move 1's per-night table is the first thing to read for exactly this reason, and I should have said so more loudly than I did.

**Second assumption.** That the universe is stable. If it grows, some "drops" are new tickers that never had metadata, and the deterministic verdict would be a true reading of a non-bug. The `--universe` flag guards against this only if the universe file is itself versioned per night.

**What a smart critic would say.** *"You've spent the whole document building instruments and haven't fixed anything. Two weeks of bad data is already on the floor."* Fair, and the honest answer is a trade: Move 0 and Move 1 together are under thirty minutes against artifacts you already have, and they cut the cause space roughly in half before a single line changes. If that thirty minutes is genuinely unaffordable tonight, the least-bad shortcut is Move 2 alone — arm the ledger, let one night run, read the stage table in the morning. That still beats guessing, because it produces evidence either way. What I would not accept is skipping straight to §5.

**Where the harness is weakest.** It is a stand-in I wrote, so it only contains bugs I thought of. A sixth mechanism I didn't imagine would sail past every test in it — though notably *not* past the conservation invariant, which is mechanism-agnostic by construction. That is the argument for the invariant over any specific test: it catches the drop without needing to know how it happened.

**One thing I'd want verified before trusting §5.** Every row in that table is reasoning from the signature, not from your code. The first row that seems to match should be confirmed with its named command before any edit — the table's job is to narrow, not to conclude.
