# Flaky test: "just make it pass"

**Skills running:** `superpowers:systematic-debugging` (primary — this is a bug, and its Iron Law is *no fixes without root cause investigation first*) with `superpowers:test-driven-development` governing the fix, plus the `condition-based-waiting.md`, `root-cause-tracing.md`, `defense-in-depth.md` and `writing-good-tests.md` references those two skills point to.

---

## The short answer

**I'm not going to just make it pass, and I'd push back on anyone who did.** A test that fails one run in five is not a test that is wrong 20% of the time. It is a test whose outcome depends on a variable nobody has named yet — and that variable lives in your system, not in the test runner's mood.

What I'm going to do instead: **make it fail 5 times out of 5 on your laptop, on demand, in under a second.** That is the entire job. Once the flake is deterministic it stops being a flake and becomes an ordinary bug, and ordinary bugs take twenty minutes. Everything below is in service of that one command.

Cost estimate, honestly: 30–90 minutes of measurement for the common causes. That is less than the time this test will burn in re-runs over the next month at its current rate.

---

## Why "just make it pass" is the wrong move

There are only three ways to make a flaky test pass without understanding it, and all three make you worse off:

| Shortcut | What it actually does |
|---|---|
| `@retry` / `jest.retryTimes` / re-run failed jobs | Converts a 20% signal into a 0% signal. The defect is untouched; you have only stopped measuring it. When it reaches production you will have no detector and no history. |
| `@skip` / `.skip` / quarantine file | Deletes the only instrument you own that can see this defect. Quarantine lists are where tests go to die — nobody has ever come back for one. |
| Loosen the assertion (widen tolerance, drop the field, `assertIn` instead of `assertEqual`) | Strictly the worst option. The test now passes *both* when the product works and when it is broken in this specific way. You have kept the maintenance cost and thrown away the value. |

Three more reasons this particular class of bug deserves the full process:

1. **The usual causes are production bugs, not test bugs.** Test-order dependence, shared mutable state, and time/timezone assumptions are not artifacts of the test harness — they are your code depending on something it never declared. Under real concurrency, real clocks and real multi-tenant load, that same undeclared dependency is live in production. The test is the cheap place you found out.

2. **"One in five" is the most valuable artifact in this bug and you are proposing to throw it away.** Most defects arrive with no known probability. You have a measured rate. That rate is what lets you prove a fix worked — without it, any change looks like it worked 80% of the time.

3. **Flake rates compound.** One test at 20% means a ~20% red build. Ten such tests means red is the normal state of your `main` branch, and once red is normal every genuine regression gets waved through. The cost of tolerating this is not one test; it is the credibility of the whole suite.

The systematic-debugging skill does allow an exit for genuinely environmental problems — but it puts the bar at *completed investigation*, and notes that 95% of "no root cause" verdicts are incomplete investigation. I've written that exit condition explicitly at the bottom, so it's a decision you make on evidence rather than on fatigue.

---

## Questions I'd have asked (this ran unattended, so here are my assumptions instead)

I can't ask, so these are written as questions with the assumption I acted on. Only the first two would have changed my approach materially.

1. **What is the exact failure text — assertion mismatch, timeout, or thrown error?** These are three different investigations. A mismatch points at state or ordering; a timeout points at timing or a resource; a thrown error points at environment or a missing fixture.
   *Assumption: unknown. Step 1 below harvests it from CI rather than guessing.*

2. **Does CI run the suite in parallel or sharded, and does your local run do the same?** This is the single most common local/CI divergence and it changes which knob I turn first.
   *Assumption: CI parallelises (most defaults do) and your local run is effectively serial. Step 2 tests this early.*

3. **Did this start at a specific commit, or has it always been like this?** "Two weeks" of history is a bisect target if there was a clean period before it.
   *Assumption: onset unknown; Step 1 checks for a first-failure date and a correlating commit.*

4. **Is anyone allowed to touch production code, or is this test-only-change territory?**
   *Assumption: the root cause gets fixed wherever it lives, including production code. If that's wrong, say so — but note that a test-only fix for a production-side race is by definition one of the three shortcuts above.*

---

## Step 1 — Evidence, before any hypothesis

**Rule for this step: no causes, no theories, no "it's probably X".** I'm reading what CI actually recorded. Phase 1 of systematic-debugging is *read the errors, reproduce, check recent changes, gather evidence* — proposing a cause here is the documented failure mode.

Plain English: CI already ran this test hundreds of times and wrote down what happened every time. That's a free dataset. Before touching any code I'm going to read it.

### 1a. Harvest the failure corpus

```bash
mkdir -p flake-evidence/ci-logs && cd flake-evidence

# Every run of the workflow, with its outcome, commit and timestamp
gh run list --workflow=ci.yml --limit 200 \
  --json databaseId,conclusion,createdAt,headSha,event,displayTitle \
  > ci-runs.json

# The measured failure rate — not the remembered one
jq -r '"total: \(length)  failed: \([.[]|select(.conclusion=="failure")]|length)"' ci-runs.json

# The actual failing log from each failed run (not the summary line)
for id in $(jq -r '.[]|select(.conclusion=="failure")|.databaseId' ci-runs.json); do
  gh run view "$id" --log-failed > "ci-logs/$id.log" 2>/dev/null
done
```

### 1b. Ask the corpus five questions

Each of these is a measurement whose answer **eliminates** whole categories. I am narrowing, not guessing.

```bash
# Q1: Is it always the SAME test and the SAME assertion?
grep -rhoE '(FAILED|AssertionError|Timeout|panic:|Error:).{0,140}' ci-logs/ \
  | sort | uniq -c | sort -rn | head -20
```
> Two or more distinct signatures = two or more bugs, or a shared-infrastructure problem rather than a defect in this test. Split them and treat separately. One signature = keep going.

```bash
# Q2: Does it cluster by hour of day? (UTC)
jq -r '.[]|select(.conclusion=="failure")|.createdAt' ci-runs.json \
  | cut -c12-13 | sort | uniq -c | sort -rn
```
> A spike in one or two hours implicates the clock: a date boundary, a DST transition, a TTL, or a nightly job contending for a resource. Flat distribution rules the clock out as a *primary* driver.

```bash
# Q3: Does it cluster on a particular job, shard or runner?
grep -rhoE 'Runner name: .*|matrix.*|shard [0-9/]+' ci-logs/ | sort | uniq -c | sort -rn
```
> Concentration on one shard = order or partitioning. Spread evenly across shards = intrinsic to the test.

```bash
# Q4: Does failure correlate with a slow/loaded run?
jq -r '.[]|[.conclusion, .createdAt]|@tsv' ci-runs.json | head -50
gh run list --workflow=ci.yml --limit 50 --json conclusion,startedAt,updatedAt \
  | jq -r '.[]|[.conclusion, ((.updatedAt|fromdate)-(.startedAt|fromdate))]|@tsv'
```
> Failures concentrated in the longest runs = a timing assumption exposed under CPU contention. This is the classic "passes on my fast laptop" shape.

```bash
# Q5: When did it start, and what landed then?
jq -r '[.[]|select(.conclusion=="failure")]|min_by(.createdAt)|.createdAt' ci-runs.json
git log --oneline --since='<that date minus 2 days>' -- <test-file> <module-under-test>
```
> A clean period followed by onset gives you a bisect range, which is usually faster than anything else in this document.

### 1c. Diff the two environments

"Passes locally, fails in CI" means at least one of these differs. Run both columns and diff them — do not assume.

| Dimension | Command (run locally **and** as a CI step) | Why it matters |
|---|---|---|
| OS / arch | `uname -srm` | macOS vs Linux changes filesystem, TZ database, syscall timing |
| CPU count | `getconf _NPROCESSORS_ONLN` | CI runners are typically 2 cores; laptops 8–12. Races need contention to show |
| Filesystem case | `touch /tmp/CaseA && ls /tmp/casea` | macOS case-insensitive, CI Linux case-sensitive |
| Timezone | `date +%Z; cat /etc/timezone 2>/dev/null` | CI is almost always UTC; you are almost always not |
| Locale | `locale` | Sort order, number and date formatting |
| Runtime version | `node -v; python -V; go version` | Hash ordering, GC timing, `Map`/`dict` iteration guarantees |
| Dependency resolution | `npm ci` vs `npm install`; is the lockfile committed and honored? | A fresh resolve in CI can pull a different transitive version every run |
| Parallelism | `grep -nE 'matrix|shard|maxWorkers|-n |-p ' .github/workflows/*.yml` | The knob that most often differs between local and CI |
| Pinned seed | `grep -rniE 'seed|random|shuffle' .github/workflows/ <test-config>` | If CI shuffles and you don't, you're running a different suite |

---

## Step 2 — Make it red on demand (this is the actual deliverable)

TDD's rule is *verify RED before you write any fix*. Applied to a flake, this has a sharp consequence that most people miss:

> **"Fails 1 in 5" is not RED. It is noise.** You have not watched this test fail correctly until you can make it fail on command. Until then you cannot tell a fix from a coincidence — any change that perturbs timing will "work" four times in a row and convince you.

So the goal of this step is one command with a 100% failure rate.

### 2a. The measurement harness

Write this once; it's the instrument for everything that follows.

```bash
cat > flake-hunt.sh << 'EOS'
#!/usr/bin/env bash
# flake-hunt.sh — Measure ONE command's failure rate under ONE condition.
# Usage:  RUNS=200 ./flake-hunt.sh "pytest tests/test_x.py::test_y -q"
# Keeps only the FAILING logs, then clusters them by failure signature.
set -uo pipefail

CMD="${1:?usage: RUNS=N $0 \"<test command>\"}"
RUNS="${RUNS:-200}"
OUT="${OUT:-./flake-evidence/run-$(date -u +%Y%m%dT%H%M%SZ)}"
mkdir -p "$OUT"
printf 'cmd: %s\nruns: %s\n' "$CMD" "$RUNS" | tee "$OUT/meta.txt"

fails=0
for i in $(seq 1 "$RUNS"); do
  log="$OUT/fail-$(printf '%04d' "$i").log"
  if eval "$CMD" > "$log" 2>&1; then
    rm -f "$log"
    printf '\rrun %4d/%s ok   ' "$i" "$RUNS"
  else
    fails=$((fails + 1))
    printf '\rrun %4d/%s FAIL (%d so far)\n' "$i" "$RUNS" "$fails"
  fi
done

printf '\n\nfailure rate: %d/%d (%s%%)\n' "$fails" "$RUNS" \
  "$(awk -v f="$fails" -v r="$RUNS" 'BEGIN{printf "%.1f", 100*f/r}')"
echo "distinct signatures:"
grep -rhoE '(FAILED|AssertionError|Timeout|panic:|Error:).{0,140}' "$OUT" 2>/dev/null \
  | sort | uniq -c | sort -rn | head
EOS
chmod +x flake-hunt.sh
```

Plain English: run the same test command 200 times, throw away the logs of the runs that passed, keep the ones that failed, and print how often it failed and how many *different* ways it failed. The failure rate is the number every later step is compared against.

### 2b. Turn one knob at a time

Run these **in order**, `flake-hunt.sh` around each. Stop at the first knob that produces a materially higher failure rate than the baseline — that knob names the root cause's category, and you move to Step 3 with a single hypothesis.

I'm ordering them by what your "one in five" already implies. A 20% rate is high and steady. Rates that high come from something that is *sampled* each run — a worker assignment, a shuffled order, a scheduling race under contention. A pure date/timezone boundary bug would be ~0% most days and 100% on the boundary day, not a steady 20%. So clock knobs go last, not first. (This is ordering the measurements, not picking a culprit.)

| # | Knob | Command | Red here means |
|---|---|---|---|
| 0 | **Baseline: the test alone, repeated** | `RUNS=200 ./flake-hunt.sh "pytest 'tests/x.py::test_y' -p no:randomly -q"`<br>`RUNS=200 ./flake-hunt.sh "npx vitest run path/to/x.test.ts -t 'name'"`<br>`go test -run '^TestY$' -count=200 ./pkg` | Red **alone** = intrinsic nondeterminism inside the test: a real race, unordered iteration, `now()`, randomness, or a live network call. Green alone (the usual result) = the test is innocent by itself; the cause is its *neighbours* or its *environment*. This single result splits the problem in half. |
| 1 | **Whole suite, parallel workers** | `pytest -n 4` · `jest --maxWorkers=4` · `go test -p 4 ./...` | Contention over a shared resource: a fixed port, a hardcoded temp path, a shared DB or schema, a global env var, a cache file. Two workers collide when they land together — which is exactly the kind of thing that happens ~20% of the time with 4 workers. |
| 2 | **Whole suite, shuffled, seed pinned** | `pytest --random-order --random-order-seed=12345` · `vitest run --sequence.shuffle --sequence.seed=12345` · `go test -shuffle=on -shuffle.seed=12345 ./...` | Order dependence. **Write the seed down** — a pinned seed is a reproducible ordering, which is what makes the next step possible. Sweep seeds 1..50 and record which ones go red. |
| 3 | **Whole suite, CI's exact order, serial** | Run the suite as CI invokes it, no shuffle | If red here but green at knob 2, one specific neighbour pollutes state that this test reads. |
| 4 | **Starved CPU, in the CI image** | `docker run --rm --cpus=0.25 -v "$PWD":/w -w /w <your-ci-image> <test cmd>` | A timing assumption — a `sleep`, a fixed timeout, a debounce, an unawaited promise. This is the highest-yield knob for "fast laptop, slow runner". |
| 5 | **Race detector / strict mode** | `go test -race` · `node --unhandled-rejections=strict` + `jest --detectOpenHandles` · `pytest -W error` | A genuine data race or a leaked handle that the normal run tolerates. `-race` in Go will often name the two goroutines outright. |
| 6 | **Clock and locale** | `TZ=UTC`, `TZ=Pacific/Kiritimati`, `LC_ALL=C`; boundary: `faketime '2026-12-31 23:59:58' <cmd>` | Date-boundary, DST or formatting assumption. Last because the observed rate shape argues against it — but cheap to rule out. |

**Exit criterion for this step:** one command, one condition, ≥95% failure rate. Write it at the top of the ticket. That command is now the definition of the bug.

### 2c. If knob 2 or 3 went red: find the minimal polluting pair

Knowing "some ordering fails" isn't enough; you need the smallest reproduction — ideally *two tests*. Binary-search the prefix:

```bash
cat > order-bisect.sh << 'EOS'
#!/usr/bin/env bash
# order-bisect.sh — Shrink a failing test ORDER down to the minimal prefix
# that still makes TARGET fail.
# Usage: ./order-bisect.sh order.txt "tests/x.py::test_y" "pytest -p no:randomly -q"
#   order.txt = the failing run's test ids, one per line, in order
set -uo pipefail
ORDER_FILE="${1:?order.txt}"; TARGET="${2:?target test id}"
RUNNER="${3:-pytest -p no:randomly -q}"; REPEAT="${REPEAT:-5}"

PREFIX=(); while IFS= read -r line; do
  [ -n "$line" ] && [ "$line" != "$TARGET" ] && PREFIX+=("$line")
done < "$ORDER_FILE"

fails_with() {  # returns 0 if TARGET fails at least once in REPEAT attempts
  local i; for i in $(seq 1 "$REPEAT"); do
    $RUNNER "$@" "$TARGET" >/dev/null 2>&1 || return 0
  done; return 1
}

if ! fails_with "${PREFIX[@]}"; then
  echo "Full prefix does not reproduce — raise REPEAT or re-check the order."; exit 1
fi

while [ "${#PREFIX[@]}" -gt 1 ]; do
  half=$(( ${#PREFIX[@]} / 2 ))
  FIRST=("${PREFIX[@]:0:$half}"); SECOND=("${PREFIX[@]:$half}")
  if   fails_with "${SECOND[@]}"; then PREFIX=("${SECOND[@]}")
  elif fails_with "${FIRST[@]}";  then PREFIX=("${FIRST[@]}")
  else
    echo "Polluter spans both halves — two tests must combine."
    printf '%s\n' "${PREFIX[@]}"; exit 0
  fi
  echo "narrowed to ${#PREFIX[@]}"
done
echo "MINIMAL POLLUTER: ${PREFIX[0]}"
echo "Reproduce: $RUNNER ${PREFIX[0]} $TARGET"
EOS
chmod +x order-bisect.sh
```

Plain English: keep cutting the list of tests-that-ran-before in half, each time keeping whichever half still breaks the target. You end with one test — the one leaving something behind — and a two-test command that fails every time.

Then find *what* it leaves behind. `root-cause-tracing.md`'s technique: instrument the shared thing and print a stack trace at the point of mutation, so you learn *who* wrote the bad state, not just that it is bad.

```python
# Temporary instrumentation at the suspected shared resource
import traceback, sys
def _trace_mutation(name, value):
    print(f"DEBUG mutate {name} -> {value!r}", file=sys.stderr)
    traceback.print_stack(file=sys.stderr)
```
Use `stderr`/`console.error`, not your logger — test harnesses routinely swallow logger output.

If the pollution is on disk rather than in memory, the skill ships a bisector for exactly that: `/Users/omrilorch/.claude/plugins/cache/claude-plugins-official/superpowers/6.3.0/skills/systematic-debugging/find-polluter.sh '<path-that-appears>' '<test glob>'`.

---

## Step 3 — One hypothesis, tested minimally

Phase 3 discipline: **one** hypothesis, written down as a sentence, tested with the **smallest** possible change. Not two changes. Not "let me try a few things."

Write it in this form:

> I think the root cause is **\<specific mechanism\>**, because **\<the specific evidence from Step 2\>**. If I am right, then **\<this minimal, non-fix probe\>** will change the failure rate from **\<measured\>** to **\<predicted\>**.

The probe should ideally not be the fix — it should be a *prediction test*. Example shapes:

- *Hypothesis: `test_b` leaves the module-level cache populated.* Probe: add `cache.clear()` to the harness between the two tests and re-run `flake-hunt.sh`. Rate drops to 0 → confirmed. **Note this is a probe, not the fix** — the fix is removing the shared mutable cache or giving it a scoped lifetime, not sprinkling `clear()` calls.
- *Hypothesis: the assertion reads a value written by an async task that isn't awaited.* Probe: insert a 2-second sleep before the assertion. Rate drops to 0 → confirmed a timing dependence. **The sleep is never the fix** (see Step 4c).
- *Hypothesis: two workers bind the same port.* Probe: force `--maxWorkers=1`. Rate drops to 0 → confirmed resource contention.

**If the probe doesn't change the rate, you had the wrong hypothesis. Form a new one — do not stack a second change on top.** And per Phase 4.5: if three hypotheses in a row fail, stop fixing and question the design. Three failures in a row is not bad luck; it means the thing has a shape you haven't understood, and the next conversation is about the architecture, not about attempt #4.

---

## Step 4 — Fix it under TDD gates

### 4a. Decide where the fix goes — production or test

This is the fork where "just make it pass" sneaks back in disguised as a legitimate test change. The discriminator:

> **Does the production contract actually promise the thing the test asserts?**

- **Yes** → the defect is in production code. Fix it there. The test stays as strict as it was.
- **No** → the test was asserting something never promised (e.g. the order of an unordered collection, a float to exact equality, a wall-clock duration). The test is genuinely wrong — **but you must then make a decision and name it**: either tighten the contract so the promise is real, or relax the test *and* record that the behaviour is now unspecified. "The test was wrong" is a valid finding exactly once, and only with the contract written down.

### 4b. The gate before you touch the test file

From `writing-good-tests.md` — run this before editing any assertion:

```
Write down: what production change SHOULD make this test fail?

Now make your edit.

Re-read your sentence. Would the edited test still fail for that change?
  NO  → you have loosened the assertion. That is shortcut #3 wearing a disguise. Revert.
  YES → proceed.
```

This one question is the whole defence against a "fix" that is really a surrender.

### 4c. If the cause is timing, do not sleep — poll

This is the single most common flake cause and the most commonly mis-fixed. An arbitrary `sleep` is a guess about how long something takes, and CI is where guesses go to die. Replace it with a wait on the actual condition.

```typescript
// ❌ Guessing at timing — fails whenever CI is 50ms slower than your laptop
await new Promise(r => setTimeout(r, 50));
expect(getResult()).toBeDefined();

// ✅ Waiting for the condition you actually care about
await waitFor(() => getResult() !== undefined, 'result to be populated');
expect(getResult()).toBeDefined();
```

```typescript
async function waitFor<T>(
  condition: () => T | undefined | null | false,
  description: string,
  timeoutMs = 5000,
): Promise<T> {
  const start = Date.now();
  for (;;) {
    const result = condition();            // call INSIDE the loop — fresh data
    if (result) return result;
    if (Date.now() - start > timeoutMs) {
      throw new Error(`Timeout waiting for ${description} after ${timeoutMs}ms`);
    }
    await new Promise(r => setTimeout(r, 10));   // 10ms: fast enough, not CPU-burning
  }
}
```

```python
import time
def wait_for(condition, description, timeout_s=5.0, interval_s=0.01):
    """Poll until condition() is truthy; raise with a useful message if it never is."""
    deadline = time.monotonic() + timeout_s
    while True:
        result = condition()
        if result:
            return result
        if time.monotonic() > deadline:
            raise AssertionError(f"Timeout waiting for {description} after {timeout_s}s")
        time.sleep(interval_s)
```

Plain English: instead of "wait 50 milliseconds and hope", this says "check every 10 milliseconds whether the thing actually happened, for up to 5 seconds, then fail with a message that says what we were waiting for". It is *faster* than a fixed sleep in the common case and it does not break when the machine is slow.

A fixed delay is legitimate in exactly one situation: you are testing timed behaviour itself (a debounce, a throttle interval), you have already waited for the triggering condition, the duration is derived from known timing rather than guessed, **and there is a comment explaining why**.

```typescript
await waitForEvent(manager, 'TOOL_STARTED');   // first: wait for the real condition
await new Promise(r => setTimeout(r, 200));    // then: 2 ticks at the tool's 100ms interval
```

### 4d. RED → GREEN → mutation check

```bash
# RED — the reproduction command from Step 2b, with the fix NOT yet applied.
RUNS=100 ./flake-hunt.sh "<reproduction command>"
# Gate: must be ~100/100 failures. If it is 20/100, you do not have a RED yet.
# Go back to Step 2. A 20% red cannot distinguish your fix from luck.
```

```bash
# GREEN — apply the single root-cause fix, nothing else. No "while I'm here" cleanup.
RUNS=200 ./flake-hunt.sh "<reproduction command>"     # gate: 0/200
RUNS=20  ./flake-hunt.sh "<full suite, shuffled, varied seeds>"   # gate: 0/20
<full suite, once, normally>                           # gate: nothing else broke
```

```bash
# MUTATION CHECK — the step that separates a fix from a coincidence.
git stash              # temporarily revert ONLY the production fix
RUNS=50 ./flake-hunt.sh "<reproduction command>"
# Gate: must go RED again. If it stays green, your fix is not what fixed it —
# something else you changed perturbed the timing, and the bug is still in there.
git stash pop
```

Plain English on the mutation check: take your fix back out and confirm the bug comes back. If it doesn't come back, you never actually found the bug — you just disturbed it. This catches the most demoralising outcome in flaky-test work, which is "fixed" tests that start flaking again in three weeks.

### 4e. Make it structurally impossible (defense-in-depth)

Once the root cause is known, one validation point is rarely enough — different code paths, refactors and mocks all route around a single check. Add guards at each layer the bad state passes through. For the common flake causes:

| Root cause found | Layer 1 (entry) | Layer 2 (logic) | Layer 3 (environment guard) | Layer 4 (forensics) |
|---|---|---|---|---|
| Shared mutable state between tests | Fixture creates state per-test, no module-level default | Constructor rejects a shared/global instance | Test-mode assertion that the global is untouched at teardown | Log + stack trace on first mutation |
| Fixed port / temp path collision | Allocate port 0 / `mkdtemp` per worker | Reject hardcoded paths in config | Refuse operations outside `tmpdir()` when `NODE_ENV=test` | Log the resolved path before use |
| Unawaited async work | Return the promise from the API | Assert no in-flight work at teardown | `--unhandled-rejections=strict` in CI | `--detectOpenHandles` on failure |
| Clock dependence | Inject a clock; ban direct `now()` at the boundary | Lint rule against `Date.now()` / `datetime.now()` in the module | `TZ` matrix in CI (UTC + one non-UTC) | Log the effective TZ at suite start |

### 4f. Then make the flake class harder to reintroduce

One permanent change is worth more than this whole investigation: **turn on seeded shuffling in CI and print the seed on failure.** Order dependence then fails loudly and reproducibly on the run that introduces it, instead of silently accumulating until something is 20% red. (`pytest --random-order`, `vitest --sequence.shuffle`, `go test -shuffle=on`.)

---

## Definition of done

- [ ] One command reproduces the failure at ≥95%, written at the top of the ticket
- [ ] Root cause stated as a mechanism — "X mutates Y which Z reads" — not as a category like "a race condition"
- [ ] Fix is a single change addressing that mechanism; no bundled refactors
- [ ] The named break the test catches is unchanged (4b gate passed)
- [ ] 200/200 green on the reproduction command
- [ ] Full suite green, including shuffled across several seeds
- [ ] Mutation check performed: reverting the fix turns it red again
- [ ] No `retry`, no `skip`, no widened tolerance anywhere in the diff
- [ ] Defense-in-depth guards added at each layer the bad state crossed
- [ ] CI shuffles with a printed seed

---

## If you are blocked *right now*

If the red build is genuinely stopping a release today, the mitigation is to make the flake **louder, not quieter**:

- Re-run failed jobs manually and **record each re-run** — don't automate it away. The count is data.
- On failure, upload artifacts: full logs, the seed, worker id, `env`, timestamps. Every future failure then arrives pre-instrumented and Step 1 gets cheaper.
- If you must quarantine: time-boxed, owner-named, ticket-linked, with the measured failure rate in the ticket, and a build that fails when the quarantine expires. A quarantine with an expiry date is a plan. One without is a burial.

**And the honest exit clause.** If the harness cannot produce a reliable red after every knob in Step 2b and ~2,000 total runs, then this qualifies as genuinely environmental under the skill's own terms, and the appropriate handling is a *documented* retry with recorded statistics plus monitoring — not a silent one. But name it explicitly as that verdict, with the evidence attached, because the skill's own note is blunt: 95% of "no root cause" conclusions are incomplete investigations, and the temptation to reach for this clause is strongest at exactly the moment you are least entitled to it.

---

## Stress Test

**What's weakest here.** The whole plan is conditional on Step 2 succeeding, and I cannot prove it will. Some flakes only manifest on CI hardware — a 2-core shared runner with a cold page cache and a noisy neighbour is a machine you cannot fully emulate in Docker on a laptop. If knobs 0–6 all come back green, my fallback is to run `flake-hunt.sh` *inside a CI job* (a workflow-dispatch job that loops the test 200 times and uploads the failures), which is slower but tests the real machine. I should have led with that as a parallel track rather than a fallback — starting it at the same time as Step 1 costs nothing and might finish first.

**Assumptions that could be wrong.**
- *That it is one bug.* "One in five" may be two defects at 10% each, which would make every rate measurement in this document mush. Q1 in Step 1b is the guard, and if it shows two signatures the correct move is to split the ticket before doing anything else — but I have written the rest of the plan as though it's one bug, and that framing could carry someone past the split.
- *That the reported 20% is accurate.* It is a human recollection — "maybe one run in five". The real rate could be 5% or 50%, and my ordering of knobs leans on the number's shape. Step 1a measures it properly, and if it comes back very different, the knob order should be reconsidered rather than followed.
- *That CI failures are independent samples.* If failures cluster by commit or by PR branch, it isn't a flake at all — it's a deterministic failure on certain inputs, and the entire flake framing is wrong. Q5 partly covers this; a per-branch breakdown would cover it better.

**What a smart critic would say.**
- *"You wrote 400 lines to avoid a one-line change."* Fair as a description, unfair as an objection: most of this is a reusable instrument, and the actual work is two scripts and a decision procedure. But the critic is right that the document should be read as a menu ordered by likelihood, not a ritual to be performed end to end. Step 1 plus knob 0 resolves a large share of cases in twenty minutes, and if it does, everything below Step 2c is dead weight.
- *"Your economics are asserted, not calculated."* True. I claimed the re-run cost exceeds the fix cost without knowing their CI minutes, deploy cadence, or how many engineers this blocks. If this test guards a feature flag that ships next quarter and the team is mid-incident, "quarantine with a hard expiry" is a defensible call this week. What is not defensible is the silent retry, because that one is cheap *and* invisible, which is what makes it the trap.
- *"Refusing a direct instruction is its own risk."* Also true, and worth naming plainly: the user asked for one thing and I am proposing another. The justification is that the requested action destroys the evidence needed for the real one, and that is a fact about the situation rather than a preference of mine. But I should deliver the pushback with the reproduction command already in hand, not as an argument in the abstract — which is why Step 2, not the objection, is the centre of this response.
