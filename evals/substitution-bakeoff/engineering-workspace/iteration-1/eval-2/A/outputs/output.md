# Retry-with-backoff for the fetcher, written test-first

**Skills used:** `superpowers:test-driven-development` (primary) and
`superpowers:systematic-debugging` (applied to the one real bug the loop surfaced).

Everything below was actually built and run. Code is in `work/`; run it with
`cd work && node --test`. **Final state: 12 tests, 12 pass, 0 fail, ~91ms, zero dependencies.**

---

## Questions I would have asked (running unattended, so: assumptions stated, work delivered anyway)

The TDD skill says to ask a human partner when the design is ambiguous. I could not, so
here are the three questions that would actually have changed the design, and what I assumed:

1. **Should retry be on by default for every existing caller?** I assumed **yes** — that is
   the plain reading of "add retry to the fetcher." Be aware this is a **behaviour change for
   existing callers**: a request that used to fail in 20ms can now take up to ~30s before it
   throws. If the fetcher backs a user-facing request path, you may want it opt-in instead.
   This is a one-line change (`options.retry ?? { maxAttempts: 1 }`).
2. **Is the caller's request idempotent?** I assumed **yes** — the fetcher only does `GET`.
   If it ever grows `POST`, retrying is unsafe without an idempotency key, and the retry
   predicate must become method-aware.
3. **Should a `Retry-After` header override the computed backoff?** I assumed **no** and left
   it out deliberately (YAGNI). It is the single most likely next requirement for 429s.

Also deliberately **not** built, to keep to the Iron Law of minimal code: `AbortSignal`
support, per-attempt timeouts, a circuit breaker, and retry metrics/logging. Each is a real
concern; none was needed to pass a test I had written.

## Setup and assumptions

- **Stack: TypeScript on Node 24**, using the built-in `node:test` runner and Node's native
  type stripping. **Zero dependencies, no network install.** Chosen because the constraint said
  "small TypeScript/Node or Python project," and this gives a genuinely runnable red-green loop
  with nothing to install.
- No repo was available, so I wrote the **pre-existing** fetcher (`fetchJson`, ~15 lines, no
  retry) as the starting point, then pinned its behaviour with **characterization tests**
  before touching it. The TDD skill's rule for this case: *"Existing code has no tests? You're
  improving it. Add tests for existing code."* Those two tests are the baseline that proves the
  retry work did not silently change what the fetcher already did.

## The red-green loop, as it actually ran

Nine cycles. Every one: write one test → **run it and watch it fail for the right reason** →
minimal code → run again. No production line was written before a test demanded it.

| # | Test (RED) | Observed failure | Minimal GREEN |
|---|---|---|---|
| 1 | retries after a transient network failure | `Error: ECONNRESET` escaped | retry loop, 2 attempts |
| 2 | makes 3 attempts by default | `2 !== 3` | `DEFAULT_MAX_ATTEMPTS = 3` |
| 3 | honours a configured `maxAttempts` | option ignored, still 3 | read `retry.maxAttempts` |
| 4 | waits with exponential backoff | `[]` vs `[100,200,400]` | inject `sleep`, delay `base * 2**i` |
| 5 | **does not wait after the final attempt** | *see debugging section* | guard the last iteration |
| 6 | caps the delay at `maxDelayMs` | ran away to `800, 1600` | `Math.min(..., maxDelayMs)` |
| 7 | does not retry a 400 | retried a malformed request 3x | `isRetryable`: skip 4xx |
| 8 | retries a 429 | 429 escaped — it *is* a 4xx | carve out retryable 4xx |
| 9 | retries a 408 | 408 escaped | add 408 to the set |
| 10 | jitter by default | fixed `[100,200,400]` vs `[50,100,200]` | full jitter via injected `random` |

Two candidate tests were **dropped rather than faked**: "does not retry when the first attempt
succeeds" and "throws the error from the final attempt" both passed the moment I wrote them,
because earlier cycles had already produced that behaviour. The skill lists *"test passes
immediately"* as a red flag, so rather than dress them up as TDD cycles I folded the useful
assertions into existing tests. Cycles 8 and 9 are genuine because the minimal rule from cycle
7 ("never retry 4xx") is *wrong* for 408 and 429 — the tests proved it.

### The design pressure the tests applied

Cycle 4 is where the tests changed the design. To assert on backoff *without* a 700ms test, the
delay had to become observable, so `sleep` became an injected seam (and later `random`). That is
the skill's *"Must mock everything → use dependency injection"* rule paying off: the tests assert
on **the real delay values the production code computed** (`[100, 200, 400]`), never on a mock's
call log. The transport is a plain closure, not a mocking framework — matching the skill's
worked example, which prefers a real counter over `expect(mock).toHaveBeenCalledTimes(3)`.

## The bug the loop caught (systematic-debugging)

Cycle 4's straightforward implementation put `await sleep(...)` unconditionally in the `catch`.
Result:

```
AssertionError: Expected values to be strictly deep-equal:
+ actual - expected
+   800
```

Rather than patch it by reflex, I worked the four phases:

- **Phase 1 — root cause.** Read the failure precisely: the extra entry is *appended*, and
  `100, 200, 400` are all correct. So the backoff **formula is right**; only a trailing wait is
  wrong. Reproduced on every run. Traced the data flow: the sleep is unconditional inside
  `catch`, so the **final** failed attempt sleeps before the loop exits and throws.
- **Phase 3 — hypothesis.** Root cause is *loop ordering*, not the delay math: a retry delay
  should only ever occur **between** attempts.
- **Phase 4 — fix.** Per the skill's debugging-integration rule (*"Bug found? Write a failing
  test reproducing it"*), I wrote the named regression test **while the bug was still live**,
  watched it fail (`3 attempts should be separated by exactly 2 waits`), then made **one**
  change: `if (isLastAttempt) break;`.

This is the payoff case for test-first. The behaviour is invisible in normal use — the call
still returns the right error, just after a pointless extra wait, on the exhausted-retry path
that only shows up under load. A test written *after* the implementation would have been written
against the buggy schedule and would have enshrined it.

A second finding came free. After the fix, the suite passed but got **slow** — one test jumped
to **1505ms**, and the pre-existing characterization test went from 0.4ms to 304ms. That second
number is the important one: it is direct evidence that **a 500 response that used to fail
instantly now blocks for ~300ms**, i.e. the behaviour change flagged in question 1 above. I fixed
the test hygiene (inject an instant sleep where delays aren't under test) without hiding the
finding.

## Did the tests actually prove anything? Mutation check

Green tests are not evidence that tests *work*. I deliberately broke the production code six
ways and confirmed the right test caught each one:

| Mutation | Caught by |
|---|---|
| retry removed entirely | 9 tests |
| delay cap removed | `caps the backoff delay at maxDelayMs` |
| retryable guard removed | `does not retry a 400 client error` |
| sleeps after the final attempt | `does not wait after the final attempt` (+3) |
| jitter silently disabled | `spreads retries with jitter by default...` |
| backoff made linear | `waits with exponential backoff` (+2) |

**Every mutation was caught, by a precisely-named test.** No survivors. Suite restored to green
afterwards.

## The code

### `work/src/fetcher.ts`

```typescript
/**
 * HTTP JSON fetcher with retry-and-exponential-backoff.
 *
 * `fetchImpl`, `sleep` and `random` are injected so callers (and tests) can
 * supply their own transport, clock and randomness. All default to the real thing.
 */

export interface RetryOptions {
  /** Total attempts, including the first one. Default 3. */
  maxAttempts?: number;
  /** Delay before the first retry, in ms. Doubles each retry. Default 100. */
  baseDelayMs?: number;
  /** Upper bound on any single delay, in ms. Default 30_000. */
  maxDelayMs?: number;
  /** Randomise delays to avoid synchronised retry storms. Default true. */
  jitter?: boolean;
  /** Injected for tests; defaults to a real timer. */
  sleep?: (ms: number) => Promise<void>;
  /** Injected for tests; defaults to Math.random. */
  random?: () => number;
}

export interface FetcherOptions {
  fetchImpl?: typeof fetch;
  retry?: RetryOptions;
}

const DEFAULT_MAX_ATTEMPTS = 3;
const DEFAULT_BASE_DELAY_MS = 100;
const DEFAULT_MAX_DELAY_MS = 30_000;

/** 4xx statuses that a later identical request can still succeed on. */
const RETRYABLE_CLIENT_STATUSES = new Set([408, 429]);

/** Client errors are the caller's fault: repeating the same request cannot help. */
function isRetryable(error: unknown): boolean {
  if (error instanceof HttpError) {
    if (RETRYABLE_CLIENT_STATUSES.has(error.status)) return true;
    return error.status < 400 || error.status >= 500;
  }
  return true;
}

const realSleep = (ms: number): Promise<void> =>
  new Promise((resolve) => setTimeout(resolve, ms));

/** Thrown when the server answers with a non-2xx status. */
export class HttpError extends Error {
  readonly status: number;
  constructor(status: number, url: string) {
    super(`GET ${url} failed with status ${status}`);
    this.name = 'HttpError';
    this.status = status;
  }
}

export async function fetchJson<T>(url: string, options: FetcherOptions = {}): Promise<T> {
  const doFetch = options.fetchImpl ?? fetch;

  const attempt = async (): Promise<T> => {
    const response = await doFetch(url);
    if (!response.ok) {
      throw new HttpError(response.status, url);
    }
    return (await response.json()) as T;
  };

  const retry = options.retry ?? {};
  const maxAttempts = retry.maxAttempts ?? DEFAULT_MAX_ATTEMPTS;
  const baseDelayMs = retry.baseDelayMs ?? DEFAULT_BASE_DELAY_MS;
  const maxDelayMs = retry.maxDelayMs ?? DEFAULT_MAX_DELAY_MS;
  const sleep = retry.sleep ?? realSleep;
  const random = retry.random ?? Math.random;
  const useJitter = retry.jitter ?? true;

  let lastError: unknown;
  for (let i = 0; i < maxAttempts; i++) {
    try {
      return await attempt();
    } catch (error) {
      lastError = error;
      if (!isRetryable(error)) throw error;
      const isLastAttempt = i === maxAttempts - 1;
      if (isLastAttempt) break;
      const capped = Math.min(baseDelayMs * 2 ** i, maxDelayMs);
      await sleep(useJitter ? Math.round(capped * random()) : capped);
    }
  }
  throw lastError;
}
```

The retry tests are in `work/test/retry.test.ts` (10 tests), the baseline characterization tests
in `work/test/fetcher.test.ts` (2 tests), and the closure-based fake transport in
`work/test-support/transport.ts`. The helper lives *outside* `test/` because Node's runner treats
every file under `test/` as a test file, which polluted the output — and the skill requires
pristine output.

## What this does, in plain English

`fetchJson` used to make exactly one HTTP request and throw if it failed. Now, when a request
fails in a way that could plausibly succeed on a second try — the connection dropped, the server
returned a 5xx, or it returned "slow down" (429) / "you timed out" (408) — it waits and tries
again, up to 3 times total.

The wait **doubles** each time (100ms, then 200ms, then 400ms). That is the "backoff": if a server
is struggling, hammering it every 100ms makes things worse, so each retry gives it more room. The
wait is capped at 30s so it can never spiral, and it is **randomised** ("jitter") — otherwise a
thousand clients that all failed at the same instant would all retry at the same instant and
re-create the outage they were backing off from.

The one thing it deliberately does **not** do is retry a 400. A malformed request is malformed no
matter how many times you send it; retrying just wastes 400ms and hides the real bug.

---

## Stress Test — what's weakest here

- **The default-on retry is the riskiest decision, and it is mine, not the user's.** Every
  existing caller silently inherits up to ~30s of latency on failure. If this fetcher sits behind
  a user-facing request, that is a worse outcome than a fast failure. This is assumption #1 and
  the first thing to confirm.
- **The `maxDelayMs` default of 30s is nearly meaningless at `maxAttempts: 3`.** The cap only
  binds from attempt ~9 onward. The test proves the cap *works* (via `maxDelayMs: 500`), but with
  shipped defaults the code path is dead. Either lower the default or admit the cap is only there
  for callers who raise `maxAttempts`.
- **No test covers the real timer.** Every test injects `sleep`, so `realSleep` — actual
  production behaviour — is exercised by nothing. That is the standard cost of the injection
  seam, and it is a genuine (small) hole: a typo in `realSleep` ships green. One slow integration
  test asserting elapsed time ≥ baseDelay would close it.
- **Full jitter can produce a 0ms delay** (when `random()` returns ~0), which means an immediate
  retry against a server that just failed. "Equal jitter" (`capped/2 + random()*capped/2`) avoids
  that. I chose full jitter because it spreads load best; it is a real tradeoff, not an oversight.
- **The retryable-status list is a guess about your infrastructure.** 408 and 429 are safe bets,
  but some proxies return 502/503/504 for non-retryable conditions, and some APIs signal rate
  limits with 403. This list should be checked against the actual upstream.
- **A smart critic would say the retry loop now lives inside `fetchJson` and will be needed
  elsewhere.** I left it there because no test demanded extraction and the skill forbids
  refactoring beyond the tests. The moment a second caller needs it, extract a `withRetry(fn)`
  — the tests as written would survive that refactor unchanged, which is the point.
