# Flaky test — diagnosis loop, repro harness, and the honest "make it pass" options

**Skill running: `engineering-tools/diagnosing-bugs`** (primary — a flake is a bug with a
non-deterministic trigger, which is the exact case that skill's Phase 1 is built for),
with **`engineering-tools/tdd`** for Phase 5 (the regression test).

---

## 0. Read this first — one correction before the work

You asked me to make it pass. There are three things that phrase can mean, and only two of
them are things I'll do:

| Option | What it does | Verdict |
|---|---|---|
| **A. Retry / bump the sleep / loosen the assert** | Hides the symptom. If the race is in the *product* code, you have now shipped a known 20% failure and deleted the alarm. | **No.** This is the one I won't do silently. |
| **B. Quarantine — skip it, with an owner, an issue, and a 14-day expiry** | Pipeline goes green in 5 minutes. The signal is preserved as a tracked debt, not deleted. | **Yes, if you need green today.** Exact snippets in §8. |
| **C. Fix the nondeterminism** | The loop below finds *what* varies between local and CI, then removes it. | **Yes — this is the body of the document.** |

The reason A is disqualified isn't purity. A test that fails 1-in-5 in CI is reporting
*something real that varies*. Until you know whether that something lives in the test
(a bad wait) or in the product (a genuine race), retrying is a coin-flip bet on which. The
cheapest way to find out is about 30 minutes of the loop in §2 — and the same 30 minutes
tells you whether B is safe.

The second reason: a single 20%-flaky test makes **1 in 5 pipelines red**. Developers
respond by reflexively clicking re-run, which is the mechanism by which genuine regressions
reach main. Flake rates compound — 20 tests at 1% each gives an 18% red-pipeline rate.
This is a pipeline-integrity problem wearing a one-test costume.

---

## 1. Questions I'd normally ask, and what I'm assuming instead

This runs unattended, so here are the questions, ranked by how much they'd change the plan,
each with the assumption I'm proceeding on.

1. **What does the failure actually say in CI?** Paste the last red run's output.
   *This single answer re-ranks every hypothesis in §5 instantly.* — Assuming unknown;
   §5 gives a prior ranking plus a lookup table keyed to the error text.
2. **Does CI run the whole suite while you run just this test locally?** And is order
   randomized? — Assuming **yes, full suite in CI / single test locally**. This is the
   single most common "passes locally, fails in CI" difference, and it makes order
   pollution (H2) a live suspect.
3. **Does the test touch time, network, a database, concurrency, or generated IDs?** —
   Assuming at least one; the harness varies all of them.
4. **How many cores does the CI runner have vs your laptop, and does the suite run with
   parallel workers/shards?** — Assuming CI is materially slower and more contended
   (2 vCPU GitHub-hosted runner vs a modern laptop is roughly a 4–8× wall-clock gap under
   load). This makes timing races (H1) the prior favourite.
5. **`tdd` requires pre-agreed seams — which seam may the regression test live at?** I
   propose the seam in §7 and mark it **CONFIRM**; do not merge the regression test until
   you've agreed the seam, per the skill.
6. **Is the behaviour under test user-visible?** i.e. could this race hit production? —
   Assuming yes until shown otherwise. This decides whether the fix is test-only or product.
7. **When did it start — first red run's date and SHA?** — Assuming unknown; §2 Step 1
   recovers it from CI history for free.

**Assumed stack:** unknown. Every script below takes the test command as an argument, so
it is framework-agnostic; §3 has the per-framework knobs (pytest / jest / vitest / go /
rspec / junit). CI assumed to be GitHub Actions for the forensics commands — the
equivalents exist in every CI (`buildkite-agent`, `circleci`, `gitlab` API).

---

## 2. Phase 1 — Build the feedback loop

> The `diagnosing-bugs` skill's Phase 1 gate: name **one command you have already run**,
> paste its invocation and output, and show it is red-capable, deterministic (for flakes:
> a pinned, high reproduction rate), fast, and agent-runnable.

### Honest status of that gate

**I cannot meet it — not because the harness is unwritten, but because it has never been
pointed at your test.** There is no repository here. I *have* run the harness against
synthetic fixtures and pasted the output in Step 7, so the tooling works; what's missing is
the only thing that counts — a loop that goes red on **your** bug.

The skill is explicit that you do not proceed to hypotheses without such a loop, so treat
§4 onward as *pre-written* analysis to be executed against the loop's output — not as a
diagnosis. I am handing you the loop, not a verdict.

The corresponding rule for you: **do not accept a fix from anyone — me or a human — that
isn't backed by a rate measurement from this harness.** "It passed a bunch of times" is a
proxy, and §2's confidence arithmetic shows exactly how misleading a proxy it is.

### Step 1 — Mine the CI history you already have (zero new runs, ~2 minutes)

Before building anything, extract what the last 100 CI runs already know.

```bash
#!/usr/bin/env bash
# ci-forensics.sh — what CI history already knows about this flake. Runs nothing new.
#   WF=ci.yml BRANCH=main N=100 ./ci-forensics.sh
set -euo pipefail
WF="${WF:-ci.yml}"; BRANCH="${BRANCH:-main}"; N="${N:-100}"
gh run list --workflow "$WF" --branch "$BRANCH" --limit "$N" \
  --json databaseId,conclusion,createdAt,headSha,event > /tmp/runs.json

python3 - <<'PY'
import json, collections, datetime
runs = json.load(open('/tmp/runs.json'))
red  = [r for r in runs if r['conclusion'] == 'failure']
print(f"red: {len(red)}/{len(runs)} = {len(red)/max(len(runs),1):.0%}")

hrs = collections.Counter(
    datetime.datetime.fromisoformat(r['createdAt'].replace('Z','+00:00')).hour for r in red)
print("red runs by UTC hour:", dict(sorted(hrs.items())))

shas = collections.Counter(r['headSha'][:7] for r in red)
dupes = {k: v for k, v in shas.items() if v > 1}
print("SHAs red more than once:", dupes or "none")

allsha = collections.Counter(r['headSha'][:7] for r in runs)
both = [s for s in shas if allsha[s] > shas[s]]
print("SHAs that went BOTH red and green (flake confirmed, free replay targets):", both[:10])
print("red run ids:", [r['databaseId'] for r in red][:20])
PY
```

Then pull the actual failure text and the order seed from one red run:

```bash
gh run view <RED_RUN_ID> --log-failed | sed -n '1,200p'
gh run view <RED_RUN_ID> --log-failed | grep -inE 'seed|shuffle|random|order|worker|timeout|=== FAILURES'
gh run view <RED_RUN_ID> --json jobs --jq '.jobs[]|{name,conclusion,startedAt,completedAt}'
```

**What each result tells you:**

| Observation | Conclusion |
|---|---|
| A SHA appears both red and green | Flake confirmed, and that SHA is your replay anchor — check it out and hammer it. |
| Red runs cluster in a narrow UTC-hour band | → H3 (clock/date boundary) jumps to rank 1. |
| Red runs cluster on one shard index or one job name | Not a random flake — an **environment-deterministic** failure on one runner config. Far easier: diff that shard's env against a green one. |
| Log prints an order seed | You may already have a deterministic repro. Go straight to §3's "pin the order" and skip most of the hunt. |
| No SHA appears twice at all | Your history is too thin to mine; go to Step 3 and generate samples yourself. |

### Step 2 — The difference table: local-green + CI-red *is* the hypothesis generator

"Passes locally, fails in CI" means the cause is in the **difference set**. Enumerate it
explicitly — this is more productive than a generic flake checklist:

| Axis | Typical laptop | Typical CI runner | Flake it causes |
|---|---|---|---|
| CPU cores / contention | 8–12, idle | 2 vCPU, shared, noisy neighbours | **timing races, timeouts** (H1) |
| What runs | one test, by name | the whole suite | **order pollution** (H2) |
| Test order | file order | randomized per run (or per-shard split) | **order pollution** (H2) |
| Clock / TZ | your local TZ, warm | UTC, and runs at any hour | **date boundaries** (H3) |
| Parallel workers | 1 | `-n auto` → worker count varies with core count | **resource collisions** (H4) |
| State | warm DB, leftover rows/caches, your `.env` | cold container, empty DB, fresh FS | either direction: test may *depend* on your warm state |
| Network | fast, unthrottled | egress-filtered, rate-limited, cold DNS | **external dependency** (H4) |
| Disk | NVMe | network-backed, slow fsync | **timeouts** (H1) |
| Entropy sources | your `PYTHONHASHSEED`/locale | different defaults | **data-order nondeterminism** (H5) |

Each row is a knob. The harness in Step 3 turns all of them at once to raise the local
failure rate; then you turn them **one at a time** to find which one owns the failure.

### Step 3 — `flake-hunt.sh`: measure and raise the rate

The goal for a flake is not a clean repro — it's a **high, replayable** reproduction rate.
Every attempt records everything that varied, so any red run is replayable.

```bash
#!/usr/bin/env bash
# flake-hunt.sh — turn "fails sometimes in CI" into a measured, replayable failure rate.
#
#   ./flake-hunt.sh '<test command>'
#   RUNS=50 JOBS=6 STRESS=8 ./flake-hunt.sh 'pytest tests/test_checkout.py -x -q'
#
# Knobs:
#   RUNS=50    attempts
#   JOBS=4     concurrent attempts (concurrency is itself a stressor)
#   STRESS=0   background CPU burners held for the whole run (simulates a busy CI box)
#   VARY=1     randomise TZ / locale / hash seed per attempt, and record them
#
# Every attempt's log begins with a copy-pasteable replay line.
set -uo pipefail

[ $# -ge 1 ] || { echo "usage: $0 '<test command>'" >&2; exit 2; }
CMD="$*"
RUNS="${RUNS:-50}"; JOBS="${JOBS:-4}"; VARY="${VARY:-1}"; STRESS="${STRESS:-0}"
RUN_DIR="${RUN_DIR:-.flake-hunt/$(date -u +%Y%m%dT%H%M%SZ)}"
mkdir -p "$RUN_DIR"
echo "run,exit_code,seconds,tz,locale,seed" > "$RUN_DIR/results.csv"

TZS=(UTC America/New_York Asia/Kolkata Pacific/Kiritimati Australia/Lord_Howe)
LCS=(C en_US.UTF-8 tr_TR.UTF-8)

rand16 () { od -An -N2 -tu2 < /dev/urandom | tr -d ' '; }

burners=()
if [ "$STRESS" -gt 0 ]; then
  for _ in $(seq 1 "$STRESS"); do
    ( while : ; do : ; done ) & burners+=("$!")
    disown %% 2>/dev/null || true
  done
  trap 'kill "${burners[@]}" 2>/dev/null || true' EXIT
  echo "holding $STRESS CPU burners for the duration"
fi

attempt () {
  local i="$1" tz=UTC lc=C seed=0 r log env_pre t0 rc
  if [ "$VARY" = 1 ]; then
    r=$(rand16); tz="${TZS[$(( r % ${#TZS[@]} ))]}"
    r=$(rand16); lc="${LCS[$(( r % ${#LCS[@]} ))]}"
    seed=$(rand16)
  fi
  log="$RUN_DIR/run-$(printf '%03d' "$i").log"
  env_pre="TZ=$tz LC_ALL=$lc PYTHONHASHSEED=$seed TEST_SEED=$seed"
  printf '### replay: %s %s\n### started: %s\n\n' "$env_pre" "$CMD" "$(date -u +%FT%TZ)" > "$log"
  t0=$SECONDS
  env TZ="$tz" LC_ALL="$lc" PYTHONHASHSEED="$seed" TEST_SEED="$seed" \
      bash -c "$CMD" >> "$log" 2>&1
  rc=$?
  printf '%s,%s,%s,%s,%s,%s\n' "$i" "$rc" "$(( SECONDS - t0 ))" "$tz" "$lc" "$seed" \
    >> "$RUN_DIR/results.csv"
  [ "$rc" -eq 0 ] || printf 'RED  run %s rc=%s -> %s\n     replay: %s %s\n' \
    "$i" "$rc" "$log" "$env_pre" "$CMD"
}

for i in $(seq 1 "$RUNS"); do
  attempt "$i" &
  while [ "$(jobs -rp | wc -l)" -ge "$JOBS" ]; do sleep 0.2; done
done
wait

python3 - "$RUN_DIR/results.csv" <<'PY'
import csv, sys, math, collections
rows = list(csv.DictReader(open(sys.argv[1])))
n = len(rows); red = [r for r in rows if r['exit_code'] != '0']
k = len(red); p = k / n if n else 0.0
z = 1.96
if n:
    d  = 1 + z*z/n
    c  = (p + z*z/(2*n)) / d
    h  = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    lo, hi = max(0.0, c-h), min(1.0, c+h)
else:
    lo = hi = 0.0
print(f"\nruns={n}  red={k}  rate={p:.1%}  95% CI [{lo:.1%}, {hi:.1%}]")
if k:
    need = math.ceil(math.log(0.05)/math.log(1-p)) if 0 < p < 1 else 0
    print(f"at this rate, {need} consecutive GREEN runs are needed to call it fixed (95%)")
    print("red runs by TZ:    ", dict(collections.Counter(r['tz'] for r in red)))
    print("red runs by locale:", dict(collections.Counter(r['locale'] for r in red)))
    slow = sorted(int(r['seconds']) for r in rows)
    print(f"duration p50/p95/max: {slow[n//2]}s / {slow[int(n*0.95)]}s / {slow[-1]}s")
else:
    print(f"0 reds in {n} runs only rules out rates above {hi:.1%} — loop is NOT tight yet")
PY
```

### Step 4 — The stressor ladder: climb until the rate is debuggable

Run in this order; stop as soon as the local rate is **≥50%**. Each rung that works is
itself a diagnosis, because it names the variable that matters.

| # | Command | Raises rate → implicates |
|---|---|---|
| 1 | `RUNS=50 JOBS=1 STRESS=0 ./flake-hunt.sh '<just this test>'` | baseline. If red here, it's self-contained — skip straight to Phase 3. |
| 2 | `RUNS=30 ./flake-hunt.sh '<the WHOLE suite, randomized order>'` | **H2 order pollution** — this is the CI-vs-local difference most often. |
| 3 | `RUNS=40 JOBS=8 STRESS=8 ./flake-hunt.sh '<test>'` | **H1 timing** — CPU starvation reproduces a slow runner. |
| 4 | `docker run --rm --cpus=0.5 --memory=1g -v "$PWD:/w" -w /w <ci-image> bash -c '<test>'` (loop it) | **H1 + environment** — the real CI image, throttled. Highest fidelity. |
| 5 | `RUNS=200 JOBS=1 VARY=1 ./flake-hunt.sh '<test>'` (fast tests only) | **H5 data nondeterminism** — varied seeds/locales, no timing pressure. |
| 6 | `sudo tc qdisc add dev eth0 root netem delay 300ms 100ms` (Linux) or block egress | **H4 network dependency**. |
| 7 | §2 Step 5's "run it in CI" workflow | when local refuses to go red at all — measure where it actually fails. |

If rung 7 is where it first goes red, that is a finding: the cause is environmental, and
the difference table in Step 2 is now your whole hypothesis space.

### Step 5 — Run the loop *in CI*, because that's where it's red

```yaml
# .github/workflows/flake-hunt.yml
# Manual-dispatch flake hunt. 5 shards x 10 runs = 50 samples on real runners.
name: flake-hunt
on:
  workflow_dispatch:
    inputs:
      test:            { description: 'test command to hammer', required: true }
      runs_per_shard:  { description: 'attempts per shard', default: '10' }
jobs:
  hunt:
    runs-on: ubuntu-latest          # must match the real CI job exactly
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4, 5]      # separate runners → samples runner-to-runner variance
    steps:
      - uses: actions/checkout@v4
      - name: setup
        run: ./ci/setup.sh          # <- copy your real CI setup steps verbatim
      - name: hammer
        env:
          TEST_CMD: ${{ inputs.test }}   # via env, NOT inlined into run: (script injection)
          N: ${{ inputs.runs_per_shard }}
        run: |
          mkdir -p flake-logs; fails=0
          for i in $(seq 1 "$N"); do
            log="flake-logs/shard${{ matrix.shard }}-$i.log"
            if bash -c "$TEST_CMD" > "$log" 2>&1; then
              echo "green $i"
            else
              fails=$((fails+1)); echo "::warning::RED attempt $i"; tail -60 "$log"
            fi
          done
          echo "shard ${{ matrix.shard }}: $fails / $N red"
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: flake-logs-${{ matrix.shard }}
          path: flake-logs/
```

Two details that matter: the setup steps must be **byte-identical** to the real job (any
difference and you're measuring a different environment), and run one variant with the
**whole suite** rather than the single test, because order pollution only appears there.

### Step 6 — Phase 1 completion gate, restated for a flake

Do not move to Phase 3 until you can paste **one command plus its output** showing:

- [ ] a measured failure rate **≥50%** (or a pinned seed/order that makes it 100%)
- [ ] the failure is the **same symptom** the CI log shows — same assertion, same error
- [ ] runtime in **seconds**, unattended
- [ ] every red run is **replayable** from its recorded TZ/locale/seed/order line

### Step 7 — What I verified about the harness (and what that does not prove)

I could not run your test, but I did run the tooling, because shipping un-run scripts and
calling them a "loop" would be the same proxy error this document warns about.

**`flake-hunt.sh` vs a synthetic test rigged to fail exactly 30% of the time** — 40 runs,
6-way parallel:

```
runs=40  red=12  rate=30.0%  95% CI [18.1%, 45.4%]
at this rate, 9 consecutive GREEN runs are needed to call it fixed (95%)
red runs by TZ:     {'Australia/Lord_Howe': 4, 'Asia/Kolkata': 2, 'Pacific/Kiritimati': 3, 'America/New_York': 3}
red runs by locale: {'C': 3, 'en_US.UTF-8': 5, 'tr_TR.UTF-8': 4}
```

It recovered the true rate, the interval covers it, the greens-needed figure is right
(`0.7^9 = 0.040`), the TZ/locale spread correctly shows *no* clustering (there is none to
find in this fixture — which is what a null result should look like), and each red log
opened with a replay line.

**`order-bisect.sh` vs a 16-test list, both code paths:**

```
CASE 1 (one polluter at position 11):   MINIMAL POLLUTING SET (1 test): test_polluter   [8 runs]
CASE 2 (needs test_a AND test_b, one in each half, forcing the linear-shrink fallback):
                                        MINIMAL POLLUTING SET (2 tests): test_a, test_b [20 runs]
```

Case 2 is the one worth noting: a naive bisector reports "no single culprit" and gives up
there. The fallback found the pair.

**Also checked:** all four bash blocks pass `bash -n` under **bash 3.2** (macOS default —
the oldest realistic target; that's why the code avoids `mapfile` and `wait -n`); both
embedded Python blocks compile; the `ci-forensics.sh` analysis produces correct output on a
synthetic `gh` payload, including the both-red-and-green SHA detection; the workflow YAML
parses. **The YAML did not parse on the first attempt** — `with: { name: ...${{ }} }` is
invalid YAML in flow style, and GitHub would have rejected it. It is fixed above. That is
the argument for this whole section in one line: three of these artifacts were fine and one
was silently broken, and only running them told me which.

**What this does not prove:** that the harness fits *your* runner, that your flake is
reproducible locally at any stress level, or anything at all about your test's cause.

### The arithmetic that stops you fooling yourself

At a true 20% failure rate, a green run means almost nothing — 4 out of 5 attempts are
green even with the bug fully present.

| True rate | Consecutive greens needed for 95% confidence it's gone |
|---|---|
| 50% | 5 |
| 20% | 14 |
| 10% | 29 |
| 5% | 59 |
| 1% | 299 |

`0.8^14 ≈ 0.044`. So "I ran it 10 times and it passed" is consistent with the bug being
completely untouched. And your own "one run in five" is a small sample: if it's 4 reds in
20 runs, the true rate is somewhere in **[8%, 42%]** at 95% confidence — which is why
Step 1's history mining matters before you trust any before/after comparison.

This is the central trap of flake work: **green-run count is a proxy for "fixed", and it is
a bad one.** The only honest before/after is *measured rate before* vs *measured rate
after*, at a sample size the table above justifies.

---

## 3. Per-framework knobs

| Runtime | Randomize order | Pin the order | Repeat N | Parallelism | Freeze clock | Race detector |
|---|---|---|---|---|---|---|
| **pytest** | `pytest-randomly` (auto once installed) | `-p randomly --randomly-seed=1234`; disable with `-p no:randomly` | `pytest-repeat`: `--count=50 --repeat-scope=session` | `pytest-xdist`: `-n 8` / `-n 0`, `--dist loadfile` | `time-machine`, `freezegun` | `pytest-timeout`, `faulthandler` |
| **jest ≥29.6** | `--randomize` | `--seed=1234` | shell loop; *not* `jest.retryTimes` | `--maxWorkers=1..N`, `--runInBand` | `jest.useFakeTimers()` | — |
| **vitest** | `--sequence.shuffle` | `--sequence.seed=1234` | `--repeats=50` (v1+) or shell loop | `--no-file-parallelism`, `--pool=threads` | `vi.useFakeTimers()` | — |
| **go** | `-shuffle=on` | `-shuffle=1234` | `-count=50` (also busts the cache) | `-parallel=N`, `-cpu=1,4` | inject a `Clock` interface | **`-race` — do this first** |
| **rspec** | `--order random` | `--order random:1234` | shell loop | — | `timecop` | **`rspec --bisect`** (built-in order-bisect; skip my script) |
| **junit5** | `ClassOrderer$Random` / `MethodOrderer$Random` | `junit.jupiter.execution.order.random.seed=1234` | `@RepeatedTest(50)` | `junit.jupiter.execution.parallel.enabled` | inject `Clock.fixed(...)` | jcstress |

Two shortcuts worth knowing: **`go test -race`** finds most Go flakes in one command, and
**`rspec --bisect`** is exactly the order-bisect tool below, already written.

---

## 4. Phase 2 — Reproduce and minimise

Once the loop is red at a workable rate, shrink it. For a flake, "minimise" has a specific
meaning: find the **smallest set of co-running tests / smallest input** that keeps the rate up.

### If the rate is a function of the order/seed → bisect the polluter

This is the highest-yield tool in flake work, because order-dependent failures are
*deterministic given the order* — so a binary search of log₂(n) runs finds the exact
polluting test.

```bash
#!/usr/bin/env bash
# order-bisect.sh — delta-debug a test-order-dependent failure to the polluting test.
#
#   ./order-bisect.sh before.txt 'pytest {} tests/test_checkout.py::test_applies_discount'
#
# before.txt = the test ids that ran BEFORE the victim, in CI's order, one per line.
#   pytest: pytest -p randomly --randomly-seed=<CI_SEED> --collect-only -q
#   go:     grep '^=== RUN' ci.log | awk '{print $3}'
#   jest:   the reporter's order in the CI log
# {} in the template is replaced by the candidate prefix.
set -uo pipefail

LIST="${1:?usage: $0 <ordered-test-id-file> '<cmd template containing {}>'}"; shift
TMPL="$*"

ALL=()
while IFS= read -r line; do [ -n "$line" ] && ALL+=("$line"); done < "$LIST"
[ "${#ALL[@]}" -gt 0 ] || { echo "empty test list" >&2; exit 2; }

runs=0
is_red () {                      # returns 0 when the victim FAILS
  local ids="$*" cmd
  cmd="${TMPL/\{\}/$ids}"
  runs=$(( runs + 1 ))
  if bash -c "$cmd" >/dev/null 2>&1; then return 1; else return 0; fi
}

echo "sanity 1/2: victim alone should be GREEN"
if is_red; then
  echo "  victim fails with no prefix → not order-dependent. Back to Phase 1." >&2; exit 1
fi
echo "sanity 2/2: full prefix should be RED"
if ! is_red "${ALL[@]}"; then
  echo "  full prefix is green → this order does not reproduce. Re-capture CI's order." >&2
  exit 1
fi

CUR=("${ALL[@]}")
while [ "${#CUR[@]}" -gt 1 ]; do
  half=$(( ${#CUR[@]} / 2 ))
  LEFT=("${CUR[@]:0:half}"); RIGHT=("${CUR[@]:half}")
  if   is_red "${LEFT[@]}";  then CUR=("${LEFT[@]}")
  elif is_red "${RIGHT[@]}"; then CUR=("${RIGHT[@]}")
  else
    echo "-> interference needs tests from BOTH halves; switching to linear shrink"
    i=0
    while [ "$i" -lt "${#CUR[@]}" ]; do
      TRY=(); j=0
      for t in "${CUR[@]}"; do [ "$j" -ne "$i" ] && TRY+=("$t"); j=$(( j + 1 )); done
      if [ "${#TRY[@]}" -gt 0 ] && is_red "${TRY[@]}"; then CUR=("${TRY[@]}")
      else i=$(( i + 1 )); fi
    done
    break
  fi
  echo "   still red with ${#CUR[@]} predecessor(s)  [$runs runs so far]"
done

echo
echo "MINIMAL POLLUTING SET (${#CUR[@]} test(s), found in $runs runs):"
printf '  %s\n' "${CUR[@]}"
echo "Now diff what that test leaves behind: globals, env vars, DB rows, module mocks,"
echo "monkeypatches, temp files, open connections, registered signal handlers, caches."
```

### Minimisation rules for the non-order case

Cut **one thing at a time**, re-measuring the rate (not a single run) after each cut:
fixtures → seeded data rows → assertions → setup steps → the other tests in the file.
Done when every remaining element is load-bearing: removing any one drops the rate to zero.

**Do not proceed past this point without a minimised, rate-measured repro.**

---

## 5. Phase 3 — Five ranked, falsifiable hypotheses

Prior ranking for "green locally, ~20% red in CI", each with the prediction that kills it.

**H1 — Timing race against a slower machine (rank 1).**
The test waits a fixed duration, or waits on the wrong signal (a render tick instead of the
data, a `sleep(100)` instead of a condition). CI's 2 contended vCPUs push the operation past
the window.
*Prediction:* rung 3/4 of the ladder (CPU starvation) raises the local rate well above
baseline; and multiplying only the timeout constant by 10 turns it green.
*Falsified if:* the rate is flat from `STRESS=0` to `STRESS=8` and under `--cpus=0.5`.

**H2 — Order dependence / leaked shared state (rank 2).**
CI runs the full suite, possibly in randomized or sharded order; a sibling test leaves
residue — a global singleton, a module-level mock, an env var, an unrolled-back DB row, a
cached config, a monkeypatch, a registered handler.
*Prediction:* replaying CI's exact seed reproduces at ~100%, while the victim alone is
always green; `order-bisect.sh` converges on a specific predecessor.
*Falsified if:* the failing seed replays green, or the rate is identical for
`--randomly-seed` values across the board.

**H3 — Clock, date, or timezone boundary (rank 3).**
Real `now()` in the test: midnight UTC rollover, month/quarter end, DST transition, leap
day, or a "within the last 24h" window computed one way in the code and another in the test.
*Prediction:* red runs cluster in a narrow UTC-hour band in Step 1's histogram; and freezing
the clock to a red run's timestamp makes it red 100% locally.
*Falsified if:* frozen-clock replay at the exact red timestamp is green, and reds are spread
uniformly across the 24 hours.

**H4 — Contended or shared resource: port, path, DB, or network (rank 4).**
A hardcoded port, a fixed `/tmp` filename, a shared table without per-test isolation, a real
outbound HTTP call that CI's egress throttles or rate-limits.
*Prediction:* the rate scales with worker count — `-n 1` green, `-n 8` much redder; and the
error text mentions `EADDRINUSE` / unique-constraint / `file exists` / deadlock / `429` /
`ECONNREFUSED`.
*Falsified if:* the rate is unchanged from 1 to 8 workers, and the test opens no sockets
(`strace -f -e trace=network`, or an assertion that the HTTP mock was used).

**H5 — Nondeterminism in the data, not the timing (rank 5).**
Unseeded RNG/UUID/faker, hash- or set-iteration order, an unstable sort on a non-unique key,
float formatting, locale-dependent collation (`tr_TR` is the classic `I`/`ı` landmine).
*Prediction:* 200 fast in-process iterations with varied seeds (rung 5) go red with **no**
timing pressure at all; and pinning `PYTHONHASHSEED` / the faker seed makes the outcome
perfectly reproducible per-seed.
*Falsified if:* 200 varied-seed iterations are all green.

### Re-rank instantly from the CI error text

| CI log says | Promote to rank 1 |
|---|---|
| `Timeout`, `waitFor exceeded`, `element not found`, `expected ... to eventually` | **H1** |
| An assertion on a *plausible but wrong* value (count off by N, stale record, extra row) | **H2** |
| Off-by-one-hour / one-day, or reds cluster by UTC hour | **H3** |
| `EADDRINUSE`, unique constraint, deadlock, `429`, `ECONNREFUSED`, `file exists` | **H4** |
| Assertion compares an ordered collection, a UUID, or a generated id | **H5** |
| Reds cluster on one shard/runner and the same SHA is reliably red there | **None of the above** — it's deterministic per-environment. Diff that runner's config; this is the easy case. |

Per the skill, this ranked list is a **checkpoint**: show it before testing, since one
sentence of domain knowledge ("we just moved that suite to xdist") re-ranks it instantly.

---

## 6. Phase 4 — Instrument

One probe per prediction. **Change one variable at a time.** Tag everything `[DEBUG-f1a3]`
so cleanup is one grep.

| Hypothesis | The one probe | Reads as |
|---|---|---|
| H1 | Log `[DEBUG-f1a3] waited=<ms> budget=<ms>` at every wait site | reds sit just over budget → confirmed |
| H2 | Snapshot shared state before/after the victim (`globals`, env, `SELECT count(*)` per table, registered mocks) and diff | a non-empty diff names the polluter |
| H3 | Log `[DEBUG-f1a3] now=<iso> tz=<tz> window=[a,b]` at the boundary computation | reds show the timestamp outside the window |
| H4 | `lsof -i -P \| grep <port>` before bind; log the temp path; `SHOW ENGINE INNODB STATUS` on deadlock | collision visible at the moment of failure |
| H5 | Log the full collection **before** the assertion, not just the diff | the ordering varies run to run |

Preference order from the skill: **debugger/REPL breakpoint > targeted logs at the
distinguishing boundary > never "log everything and grep"**. For anything that looks like a
timeout, measure first (`performance.now()` deltas, a timing harness, the query plan) rather
than logging — timeouts are a perf problem in disguise, and logs mislead.

---

## 7. Phase 5 — Fix and regression test (`tdd` skill)

### Fix hierarchy — best to worst

1. **Remove the nondeterminism.** Inject a clock instead of calling `now()`. Seed the RNG.
   Await the *condition* (`waitFor(() => rowExists(), {timeout: 5000, interval: 10})`),
   never a duration. Allocate a random free port / unique temp dir per test. Wrap each test
   in a transaction that rolls back.
2. **Make the implicit ordering explicit.** Proper teardown, per-test fixtures, no
   module-level mutable state.
3. **Bound the wait, don't lengthen the sleep.** A poll-until-condition with a generous
   ceiling is deterministic in *outcome* while tolerant of timing. `sleep(5000)` is not a
   fix; it is the same bug with a bigger number.
4. **Retry.** Legitimate *only* when the nondeterminism is genuinely outside the system
   under test and outside its contract (a third-party sandbox), and then the retry belongs
   in that dependency's client with a documented policy — not as a blanket test-runner flag.

### The regression test — per `tdd`

**Seam: CONFIRM before merging.** `tdd` is explicit that no test is written at an
unconfirmed seam. My proposal, absent your answer to question 5: test at the same public
interface the existing test uses — the flake is evidence that seam is real — and add
*determinism controls* (injected clock / seeded RNG / explicit barrier) rather than moving
to a deeper seam. Moving deeper is tempting and usually wrong: a unit test below the race
cannot express the race.

**The rule that makes a flake regression test worth keeping: it must be red 100%, not 20%.**
You convert the race into a deterministic test by *controlling the thing that varied* —
freeze the clock at the boundary value, force the interleaving with a barrier/fake timer,
run the polluting test explicitly before the victim, pin the seed. A regression test that is
itself flaky has added a second flake, not locked down the first.

Loop, in order:

1. Write the test with the determinism control set to the **failing** value. Run it.
2. **Watch it fail — 20 times out of 20.** If it's 4/20, you have not isolated the cause;
   go back to Phase 3. This gate is the whole value of the exercise.
3. Apply the fix.
4. Watch it pass 20/20.
5. Re-run the **original** un-minimised loop (`flake-hunt.sh` at the rung that first went
   red) and compare *measured rates*, at the sample size §2's table demands.
6. Re-run the CI hammer workflow on the fix branch. Green in CI at n≥30 is the real verdict.

Anti-patterns to avoid here, straight from `tdd`:
- **Tautological** — asserting the timestamp equals the same `now()` expression the code
  uses. The expected value must come from an independent literal (`2026-01-01T00:00:00Z`).
- **Implementation-coupled** — asserting "`retry` was called twice" instead of "the record
  is visible afterwards". Mock only at system boundaries: time, randomness, external APIs.
- **Horizontal slicing** — don't write a battery of "concurrency tests"; one vertical slice
  against the actual observed failure.

**If no correct seam exists** — e.g. the race needs two real processes and your harness
can't express that — the skill says that absence *is the finding*. Write it down, ship the
fix with the Phase 1 loop as the evidence, and flag the architecture gap.

---

## 8. The legitimate "make it pass right now"

If you need green before this work finishes, quarantine — visibly, with an owner and an
expiry. Never a silent retry.

```python
# pytest
@pytest.mark.skip(reason="FLAKE #1234 — 20% red in CI, owner @you, expires 2026-09-30")
```
```js
// jest / vitest
test.skip('applies discount', ... )  // FLAKE #1234 — owner @you, expires 2026-09-30
```
```go
func TestApplyDiscount(t *testing.T) {
    t.Skip("FLAKE #1234 — 20% red in CI, owner @you, expires 2026-09-30")
```
```ruby
# rspec
it 'applies the discount', skip: 'FLAKE #1234 — owner @you, expires 2026-09-30' do
```

Issue body to file alongside it:

```
Title: [FLAKE] <test id> — ~20% red in CI
Observed rate: <k>/<n> from ci-forensics.sh on <date>   (fill in — do not guess)
Red run ids:   <ids>
Quarantined:   <sha>, expires <date + 14d>, owner @<name>
Blast radius:  does this test cover behaviour that can fail in production? <yes/no/unknown>
Next step:     run flake-hunt.sh rungs 1-3; attach results.csv
On expiry:     fixed, or the test is deleted. A permanently-skipped test is worse than
               no test — it is a maintenance cost that asserts nothing.
```

The **Blast radius** line is the one that matters. If the answer is "yes", quarantine buys
you days, not weeks, and the fix is a production bug fix that happens to have a test attached.

---

## 9. Phase 6 — Cleanup and post-mortem

Before declaring done:

- [ ] Original repro no longer reproduces — re-run the Phase 1 loop at the rung that was red
- [ ] Rate measured **before and after**, at a sample size §2's table justifies (not "ran it
      a few times")
- [ ] Regression test red 20/20 pre-fix, green 20/20 post-fix — or the missing seam documented
- [ ] `grep -rn 'DEBUG-f1a3' .` returns nothing
- [ ] `.flake-hunt/` and any throwaway harness removed or moved to `scripts/debug/`
- [ ] The **winning hypothesis named in the commit message**, with the measured rates, so the
      next person debugging a flake here inherits the finding rather than repeating it

**What would have prevented this?** Candidates, in the order I'd actually adopt them —
but note the discipline: *one flake is a hypothesis, not a policy.* Adopt item 1 now; hold
the rest until you've seen the pattern two or three times.

1. **Randomize test order in CI from day one, with the seed printed on every run.** Order
   pollution then surfaces immediately and loudly, at a commit you can bisect, instead of
   silently accumulating until it's a 20% flake with no obvious owner.
2. **Ban wall-clock sleeps in tests** via a lint rule; provide a `waitFor(condition)` helper
   so the right thing is the easy thing.
3. **Inject the clock everywhere.** No production code calls `now()` directly.
4. **A standing flake dashboard** — the red rate per test over the last 200 runs, from the
   same data `ci-forensics.sh` reads. Flakes get fixed when they're visible and ranked.
5. If the cause turns out to be tangled shared state with no clean seam, that's an
   architecture finding — hand it to `/improve-codebase-architecture` **after** the fix
   lands, with the specific coupling named.

---

## 10. In plain English

A flaky test is a test whose result depends on something nobody wrote down — how fast the
machine was that minute, what ran before it, what time it is, which random number came up.
It passes on your laptop because your laptop happens to supply the lucky value every time.

So the work isn't "look at the test and spot the bug". It's: **find the hidden variable.**
The scripts above do that in three moves. First, mine what CI already recorded — if failures
cluster at a particular hour, the hidden variable is the clock; if they cluster on one
machine, it isn't random at all. Second, make the failure happen *on demand locally* by
deliberately turning each suspect knob (starve the CPU, shuffle the order, change the
timezone) — the knob that makes it fail reliably *is* the answer. Third, once it fails
reliably, remove that variable from the test — pin the clock, isolate the state, wait for
the actual thing instead of waiting a fixed number of seconds.

The trap to avoid: with a 1-in-5 failure, running it ten times and seeing green proves
almost nothing — a bug that fails 20% of the time passes ten in a row about 11% of the time.
That's why every step here measures a *rate* rather than counting lucky passes.

---

## Stress Test

**What's weakest here.** The harness is tested; the *diagnosis* is not started. Step 7
shows `flake-hunt.sh` and `order-bisect.sh` working against synthetic fixtures, but a
fixture I wrote to be flaky is a soft target — it has none of the setup cost, shared state,
or environment coupling of a real suite. The scripts also assume `python3` on PATH and
GNU/BSD `od`; expect ten minutes of fitting. Most importantly, the `diagnosing-bugs` Phase 1
gate — *a loop that goes red on **this** bug* — is **not met**, so every hypothesis in §5 is
a prior, not a finding. If you read only one line of this document as a caveat, that's it.

**Assumptions that could be wrong.**
- *That it's actually flaky.* "One run in five" might be one shard, one runner image, or one
  branch failing deterministically. Step 1 checks this first precisely because it would make
  most of this document unnecessary — and that's the good outcome.
- *That H1 deserves rank 1.* That's a base-rate prior from the local-green/CI-red shape, not
  evidence from your code. One line of CI log output should override it; the re-rank table
  exists because my prior is the weakest input in §5.
- *That local stress can reproduce CI.* Some CI-only failures (a proxy, a secret, an image
  difference, a network policy) will never reproduce on a laptop at any stress level. If
  rungs 1–6 all stay green, stop climbing and go to rung 7 — running the hunt *in* CI — rather
  than concluding "not reproducible".
- *That 20% is the true rate.* Four reds in twenty runs gives a 95% interval of roughly
  [8%, 42%]. If the truth is 8%, my "14 green runs proves it" advice is badly optimistic and
  you'd need ~36.

**What a smart critic would say.**
- *"You wrote a thousand words in response to 'just make it pass'."* Fair, and the ordering
  is the answer: §0 gives the 5-minute quarantine up front, so nothing here blocks green.
  But the pushback stands — if the race is in product code, the retry flag ships a known
  bug, and that call is yours to make with the information, not mine to make by default.
- *"`order-bisect.sh` duplicates `rspec --bisect` and `pytest-random-order`'s bisect."* Yes —
  §3 says so and tells you to use theirs. The script is for the runners that lack one.
- *"The linear-shrink fallback is O(n²) test runs."* True; on a 2,000-test suite with a
  30-second suite run it's impractical. Mitigation: bisect at *file* granularity first, then
  at test granularity within the guilty file.
- *"Quarantine-with-expiry is a policy that teams universally ignore."* Also true. The expiry
  is only real if something enforces it — a CI check that fails on a skip marker past its
  date. Worth building only once you've quarantined a third test, not now.
