# Retry-with-backoff on the fetcher, written test-first

**Skill run: `engineering-tools/tdd`.** I also read `engineering-tools/diagnosing-bugs`
and did **not** run it — it is a diagnosis loop for a bug that already exists, and nothing
here is broken. One idea from it did carry over: its bar for a feedback loop (*fast,
deterministic, agent-runnable, red-capable*) is the same bar a TDD loop has to clear, and
it is what drove the virtual-clock design below.

Everything in this document was actually run. Code, per-cycle implementation snapshots,
and raw test output are in `work/` (`work/src`, `work/test`, `work/history`, `work/logs`).

- **Stack:** TypeScript on Node 24 (`node --test`, native type stripping). No dependencies,
  no build step — `cd work && npm test`.
- **Result:** 13 tests, 13 passing, 86 ms. 11 red→green cycles, each one run and captured.
- **Suite verified non-vacuous:** 7 deliberate mutations of the retry logic, 7 killed.

---

## Before writing a single test: the seams

The skill is explicit — *"Test only at pre-agreed seams. Before writing any test, write
down the seams under test and confirm them with the user. No test is written at an
unconfirmed seam."* This run is unattended, so here are the questions I would have asked,
and the answers I proceeded on. **Each one is a place where the tests would change shape,
not just detail, if you answer differently.**

| # | Question I could not ask | What I assumed, and why |
|---|---|---|
| 1 | What is the fetcher's public interface today? | `createFetcher({ transport }) → { fetchJson<T>(url, init) }`, throwing `HttpError` on a non-2xx. Written as `work/src/fetcher.ts` **before** any retry work, and pinned by two characterization tests so I could prove retry didn't change it. |
| 2 | Is the retry policy per-fetcher or per-call? | **Per-fetcher** (`createFetcher({ retry: {...} })`). A retry policy is an operational property of the client, not of one request. If it should be per-call, every test's arrange block moves. |
| 3 | Which seam do we test at — `fetchJson`, or a standalone `retry()` helper? | **`fetchJson`.** Retry is not a feature users ask for; "the call succeeds despite a blip" is. Testing a `retry()` helper would test the *shape* of the mechanism and leave the wiring untested. The seam is unchanged by this work, which is why the two cycle-0 tests never needed editing. |
| 4 | Which statuses are retryable? | 429 and 5xx. 4xx other than 429 fail immediately — the request is wrong, retrying it just burns the budget. |
| 5 | Jitter on by default? | **Yes, full jitter.** Backoff without jitter fixes the "one client hammers a sick server" problem and leaves the worse one, "every client retries in lockstep." This assumption had a visible cost in cycle 8 — see below. |
| 6 | Defaults? | 3 attempts, 100 ms base, doubling, 2 s cap. Conservative; every value is injectable. |

**Three things are faked and nothing else** — precisely the boundaries `mocking.md`
sanctions (external API, time, randomness): the `transport`, the `clock`, and `random`.
No internal collaborator is mocked, so the tests survive any rewrite of the loop's insides.
They did: the implementation was restructured three times (ad-hoc `if` → bounded loop →
`try/catch` loop) and not one existing assertion had to change for that reason.

### The design decision that made the tests good

The obvious way to test backoff is to inject a `sleep` spy and assert
`sleep` was called with `100, 200, 400`. That is the **implementation-coupled** anti-pattern
in `tests.md` — asserting on call arguments of an internal collaborator, testing *how*.

Instead I injected a **virtual clock**: `sleep(ms)` advances a counter and returns
immediately. The fake transport stamps each request with `clock.now()`. So the tests assert
on **when each request actually reached the server** — `[0, 100, 300, 700]` — which is the
thing the outage victim cares about, observed at the network boundary. The implementation
can wait however it likes; the test only cares that traffic is spaced out. It also makes the
whole suite run in milliseconds of wall-clock time.

Expected values are **independent literals** taken from the policy in the table above, never
recomputed with the implementation's own arithmetic — that is the **tautological** anti-pattern
(`tests.md`), and it is easy to walk into when the subject is a formula.

---

## The loop, cycle by cycle

One seam, one test, one minimal implementation per cycle — vertical slices, no bulk test
writing. Red output is quoted from `work/logs/NN-red.txt`, green from `NN-green.txt`.

**Cycle 0 — characterization (green, and honestly labelled).** Two tests pinning the
existing contract: success returns the parsed body in one request; failure throws
`HttpError` with the status. These passed immediately. That is not a TDD cycle and I am not
claiming it as one — it is the safety net that proves the next 11 cycles didn't change the
public behaviour.

| # | Behaviour the test names | Red said | Minimal green |
|---|---|---|---|
| 1 | retries after a 503 and returns the body from the retry | `Error [HttpError]: HTTP 503` | one `if (status === 503) retry once` |
| 2 | stops after the default attempt budget and surfaces the last failure | `2 !== 3` | replaced the `if` with a bounded 3-attempt loop |
| 3 | does not retry a 400 — the request is wrong, not the server | `3 !== 1` | `if (status < 500) throw` |
| 4 | retries a 429 because the server is asking us to slow down | `Error [HttpError]: HTTP 429` | `isRetryableStatus = 429 \|\| >= 500` |
| 5 | honours a configured attempt budget | `3 !== 4` | `retry.maxAttempts`, default 3 |
| 6 | **spaces retries out with exponentially growing waits** | `[0, 0, 0, 0]` vs `[0, 100, 300, 700]` | inject `Clock`; `sleep(base * 2 ** (attempt-1))` between attempts |
| 7 | caps how long it will wait between attempts | `700` where `550` was expected | `Math.min(..., maxDelayMs)`, default 2 s |
| 8 | **jitters each wait so retrying clients do not sync up** | `[0, 100, 300, 700]` vs `[0, 25, 75, 175]` | inject `random`; wait is `random() * nominal` |
| 9 | retries when the connection itself fails | `TypeError: fetch failed` escaped | wrap the attempt in `try/catch` |
| 10 | waits as long as a Retry-After header asks, instead of guessing | `25` where `1000` was expected | parse `retry-after` delta-seconds; still capped |
| 11 | stops retrying as soon as the caller aborts | 4 requests, `HttpError` | `if (init?.signal?.aborted) throw init.signal.reason` |

Cycles 3 and 4 are deliberately separate slices. After cycle 3 the rule was the crude
`status < 500`, which is all the 400 test could justify; 429 then demanded its own red.
Bundling them would have been me writing the rule I already had in mind rather than the
rule a test forced — which is the horizontal-slicing habit in miniature.

### What cycle 8 cost, and why that's the interesting part

Turning jitter on made cycles 6 and 7 fail — they had asserted an exact schedule while
silently depending on an un-pinned `Math.random`:

```
✖ spaces retries out with exponentially growing waits
✖ caps how long it will wait between attempts
ℹ pass 8   ℹ fail 2
```

That is the honest cost of slice ordering, and the fix is one line per test:
`random: () => 1, // jitter neutralised: this test is about the schedule`. Now each test
*states* its assumption about the draw instead of depending on one by accident.

The same run surfaced something I had not planned for. Three tests had suddenly become slow:

```
✔ throws HttpError carrying the status when the server keeps failing (195.666666ms)
✔ stops after the default attempt budget and surfaces the last failure (164.629125ms)
✔ honours a configured attempt budget (368.472709ms)
```

Those tests never injected a clock, so they fell through to `setTimeout` and **really slept**.
Suite duration had drifted to **897 ms** and was at the mercy of the OS timer. Injecting the
virtual clock in every test brought it back to **84 ms** and made it deterministic. This is the
`diagnosing-bugs` feedback-loop bar applied to the test suite itself: a slow, timing-dependent
loop is the thing that stops being run.

---

## Is the suite actually load-bearing?

Passing tests prove nothing about whether the tests *can* fail. So I mutated the finished
implementation seven times and re-ran (`work/` restored after each):

| Mutation | Killed by |
|---|---|
| backoff removed (retry immediately) | 3 tests — exponential schedule, cap, jitter |
| cap removed (double forever) | caps how long it will wait |
| jitter removed | jitters each wait |
| everything retryable | does not retry a 400 |
| off-by-one in the budget (`<` for `<=`) | 6 tests |
| Retry-After ignored | waits as long as Retry-After asks |
| abort check removed | stops retrying as soon as the caller aborts |

**7 mutants, 7 killed.** Every guarantee in the policy table has exactly one test that
notices when it disappears.

---

## What it does, in plain English

`fetchJson` now runs a small loop instead of a single request. On each pass it makes the
request; a 2xx returns the parsed body immediately, which is the normal path and costs
nothing. Anything else is sorted into two buckets: *your fault* (a 400 — the request is
malformed, so it throws right away and doesn't waste attempts) and *maybe transient* (a
429, a 5xx, or the connection dying before any status came back).

For a transient failure it waits before trying again, and the wait grows: roughly 100 ms,
then 200, then 400, doubling so a server that is genuinely struggling gets progressively
more room. Two things bound that. A ceiling (2 s by default) stops the doubling turning
into a multi-minute hang, and the attempt budget (3 by default) means it gives up and
raises the last real error rather than retrying forever — a caller waiting on a dead
service gets an error it can act on.

Two refinements matter in production. The wait is multiplied by a random fraction, so a
hundred clients that all failed at the same instant don't all come back at the same
instant and re-flatten the server — backoff without jitter just moves the stampede. And
if the server sends a `Retry-After` header, that instruction wins over our guess: the
server knows when it will be ready and we don't.

Finally, if the caller aborts, the loop stops at once and surfaces the abort. Retrying on
behalf of someone who has navigated away is pure waste, and it is exactly what a naive
retry loop does.

---

## Files

```
work/
├── package.json                  # npm test → node --test test/fetcher.test.ts
├── src/fetcher.ts                # the fetcher (102 lines)
├── test/fetcher.test.ts          # 13 tests (223 lines)
├── test/support/fakes.ts         # virtual clock + scripted transport (53 lines)
├── history/00-before.ts … 12-final.ts   # implementation after each cycle
└── logs/00…12                    # raw red/green output for every cycle
```

### `work/src/fetcher.ts`

```typescript
// JSON fetcher with bounded, jittered exponential backoff.
// Retry policy lives here so every call site gets it without opting in.
export type Transport = (url: string, init?: RequestInit) => Promise<Response>;

export interface Clock {
  now(): number;
  sleep(ms: number): Promise<void>;
}

const systemClock: Clock = {
  now: () => Date.now(),
  sleep: (ms) => new Promise((resolve) => setTimeout(resolve, ms)),
};

export interface RetryOptions {
  /** Total attempts, including the first one. */
  maxAttempts?: number;
  /** Ceiling on the first retry's wait; doubles on each subsequent retry. */
  baseDelayMs?: number;
  /** Ceiling on any single wait. */
  maxDelayMs?: number;
}

export interface FetcherDeps {
  transport?: Transport;
  clock?: Clock;
  /** Source of jitter. Injected so waits are reproducible in tests. */
  random?: () => number;
  retry?: RetryOptions;
}

export class HttpError extends Error {
  status: number;
  url: string;
  constructor(status: number, url: string) {
    super(`HTTP ${status} for ${url}`);
    this.name = "HttpError";
    this.status = status;
    this.url = url;
  }
}

/** `Retry-After: <delta-seconds>`, in ms, or null when absent or unparseable. */
function retryAfterMs(response: Response): number | null {
  const header = response.headers.get("retry-after");
  if (header === null) return null;
  const seconds = Number(header);
  if (!Number.isFinite(seconds) || seconds < 0) return null;
  return seconds * 1000;
}

function isRetryableStatus(status: number): boolean {
  return status === 429 || status >= 500;
}

export interface Fetcher {
  fetchJson<T>(url: string, init?: RequestInit): Promise<T>;
}

export function createFetcher(deps: FetcherDeps = {}): Fetcher {
  const transport: Transport =
    deps.transport ?? ((url, init) => globalThis.fetch(url, init));
  const clock = deps.clock ?? systemClock;
  const maxAttempts = deps.retry?.maxAttempts ?? 3;
  const baseDelayMs = deps.retry?.baseDelayMs ?? 100;
  const maxDelayMs = deps.retry?.maxDelayMs ?? 2000;
  const random = deps.random ?? Math.random;

  return {
    async fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
      let lastError: unknown;

      for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
        let retryable = true;
        let serverAskedForMs: number | null = null;

        try {
          const response = await transport(url, init);
          if (response.ok) return (await response.json()) as T;
          lastError = new HttpError(response.status, url);
          retryable = isRetryableStatus(response.status);
          serverAskedForMs = retryAfterMs(response);
        } catch (err) {
          lastError = err; // the connection failed before any status existed
        }

        if (init?.signal?.aborted) throw init.signal.reason;
        if (!retryable) throw lastError;
        if (attempt < maxAttempts) {
          if (serverAskedForMs !== null) {
            await clock.sleep(Math.min(serverAskedForMs, maxDelayMs));
          } else {
            const nominal = Math.min(baseDelayMs * 2 ** (attempt - 1), maxDelayMs);
            await clock.sleep(random() * nominal);
          }
        }
      }

      throw lastError;
    },
  };
}
```

### `work/test/support/fakes.ts`

```typescript
// Fakes for the three system boundaries the fetcher touches:
// the network, the clock, and randomness. Nothing internal is faked.

export interface VirtualClock {
  now(): number;
  sleep(ms: number): Promise<void>;
}

/** A clock where sleeping is instant but time still moves, so tests stay fast
 *  and deterministic while "when did each request happen?" stays observable. */
export function virtualClock(): VirtualClock {
  let t = 0;
  return {
    now: () => t,
    async sleep(ms: number) {
      t += ms;
    },
  };
}

export type Step =
  | { status: number; body?: unknown; headers?: Record<string, string> }
  | { throws: Error };

export interface RecordedRequest {
  url: string;
  at: number;
}

/** A transport that plays a script of responses and records when each request
 *  arrived on the virtual clock. The last step repeats if asked for more. */
export function scriptedTransport(steps: Step[], clock: { now(): number }) {
  const requests: RecordedRequest[] = [];
  let i = 0;

  const transport = async (url: string, _init?: RequestInit): Promise<Response> => {
    requests.push({ url, at: clock.now() });
    const step = steps[Math.min(i, steps.length - 1)];
    i += 1;
    if ("throws" in step) throw step.throws;
    return new Response(JSON.stringify(step.body ?? null), {
      status: step.status,
      headers: { "content-type": "application/json", ...(step.headers ?? {}) },
    });
  };

  return { transport, requests };
}

/** When each request happened, relative to the first. */
export function offsets(requests: RecordedRequest[]): number[] {
  return requests.map((r) => r.at);
}
```

### `work/test/fetcher.test.ts`

```typescript
import { test } from "node:test";
import assert from "node:assert/strict";
import { createFetcher, HttpError } from "../src/fetcher.ts";
import { offsets, scriptedTransport, virtualClock } from "./support/fakes.ts";

// ── Cycle 0: pin the contract that already exists ────────────────────────────

test("returns the parsed body when the first attempt succeeds", async () => {
  const clock = virtualClock();
  const net = scriptedTransport([{ status: 200, body: { id: 7 } }], clock);
  const fetcher = createFetcher({ transport: net.transport, clock });

  const body = await fetcher.fetchJson<{ id: number }>("https://api.test/thing");

  assert.deepEqual(body, { id: 7 });
  assert.equal(net.requests.length, 1);
});

test("throws HttpError carrying the status when the server keeps failing", async () => {
  const clock = virtualClock();
  const net = scriptedTransport([{ status: 500 }], clock);
  const fetcher = createFetcher({ transport: net.transport, clock });

  await assert.rejects(
    () => fetcher.fetchJson("https://api.test/thing"),
    (err: unknown) => err instanceof HttpError && err.status === 500,
  );
});

// ── Cycle 1: a transient 503 should not reach the caller ────────────────────

test("retries after a 503 and returns the body from the retry", async () => {
  const clock = virtualClock();
  const net = scriptedTransport(
    [{ status: 503 }, { status: 200, body: { id: 7 } }],
    clock,
  );
  const fetcher = createFetcher({ transport: net.transport, clock });

  const body = await fetcher.fetchJson<{ id: number }>("https://api.test/thing");

  assert.deepEqual(body, { id: 7 });
  assert.equal(net.requests.length, 2);
});

// ── Cycle 2: retrying forever is worse than failing ─────────────────────────

test("stops after the default attempt budget and surfaces the last failure", async () => {
  const clock = virtualClock();
  const net = scriptedTransport([{ status: 503 }], clock); // never recovers
  const fetcher = createFetcher({ transport: net.transport, clock });

  await assert.rejects(
    () => fetcher.fetchJson("https://api.test/thing"),
    (err: unknown) => err instanceof HttpError && err.status === 503,
  );
  assert.equal(net.requests.length, 3);
});

// ── Cycle 3: a bad request is our fault; retrying it just wastes time ────────

test("does not retry a 400 — the request is wrong, not the server", async () => {
  const clock = virtualClock();
  const net = scriptedTransport([{ status: 400 }], clock);
  const fetcher = createFetcher({ transport: net.transport, clock });

  await assert.rejects(
    () => fetcher.fetchJson("https://api.test/thing"),
    (err: unknown) => err instanceof HttpError && err.status === 400,
  );
  assert.equal(net.requests.length, 1);
});

// ── Cycle 4: 429 is the one 4xx worth retrying ──────────────────────────────

test("retries a 429 because the server is asking us to slow down", async () => {
  const clock = virtualClock();
  const net = scriptedTransport(
    [{ status: 429 }, { status: 200, body: { ok: true } }],
    clock,
  );
  const fetcher = createFetcher({ transport: net.transport, clock });

  const body = await fetcher.fetchJson<{ ok: boolean }>("https://api.test/thing");

  assert.deepEqual(body, { ok: true });
  assert.equal(net.requests.length, 2);
});

// ── Cycle 5: callers with different tolerance need a different budget ───────

test("honours a configured attempt budget", async () => {
  const clock = virtualClock();
  const net = scriptedTransport([{ status: 503 }], clock);
  const fetcher = createFetcher({
    transport: net.transport,
    clock,
    retry: { maxAttempts: 4 },
  });

  await assert.rejects(() => fetcher.fetchJson("https://api.test/thing"));
  assert.equal(net.requests.length, 4);
});

// ── Cycle 6: hammering a struggling server is what backoff is for ───────────

test("spaces retries out with exponentially growing waits", async () => {
  const clock = virtualClock();
  const net = scriptedTransport([{ status: 503 }], clock);
  const fetcher = createFetcher({
    transport: net.transport,
    clock,
    random: () => 1, // jitter neutralised: this test is about the schedule
    retry: { maxAttempts: 4, baseDelayMs: 100 },
  });

  await assert.rejects(() => fetcher.fetchJson("https://api.test/thing"));

  // Waits of 100, 200, 400 put the four requests at these points on the clock.
  assert.deepEqual(offsets(net.requests), [0, 100, 300, 700]);
  // ...and nothing waits after the final attempt.
  assert.equal(clock.now(), 700);
});

// ── Cycle 7: doubling forever means a 13-minute wait by attempt 10 ──────────

test("caps how long it will wait between attempts", async () => {
  const clock = virtualClock();
  const net = scriptedTransport([{ status: 503 }], clock);
  const fetcher = createFetcher({
    transport: net.transport,
    clock,
    random: () => 1, // jitter neutralised: this test is about the cap
    retry: { maxAttempts: 5, baseDelayMs: 100, maxDelayMs: 250 },
  });

  await assert.rejects(() => fetcher.fetchJson("https://api.test/thing"));

  // Waits of 100, 200, then 250, 250 — the cap bites on the third retry.
  assert.deepEqual(offsets(net.requests), [0, 100, 300, 550, 800]);
});

// ── Cycle 8: 500 clients retrying in lockstep is a second outage ────────────

test("jitters each wait so retrying clients do not sync up", async () => {
  const clock = virtualClock();
  const net = scriptedTransport([{ status: 503 }], clock);
  const fetcher = createFetcher({
    transport: net.transport,
    clock,
    random: () => 0.25, // this client happens to draw a quarter of its window
    retry: { maxAttempts: 4, baseDelayMs: 100 },
  });

  await assert.rejects(() => fetcher.fetchJson("https://api.test/thing"));

  // Full jitter: each wait is a random point in [0, nominal) — 25, 50, 100.
  assert.deepEqual(offsets(net.requests), [0, 25, 75, 175]);
});

// ── Cycle 9: a dropped connection never becomes a status code ───────────────

test("retries when the connection itself fails", async () => {
  const clock = virtualClock();
  const net = scriptedTransport(
    [{ throws: new TypeError("fetch failed") }, { status: 200, body: { id: 7 } }],
    clock,
  );
  const fetcher = createFetcher({ transport: net.transport, clock });

  const body = await fetcher.fetchJson<{ id: number }>("https://api.test/thing");

  assert.deepEqual(body, { id: 7 });
  assert.equal(net.requests.length, 2);
});

// ── Cycle 10: when the server names a wait, guessing is worse ───────────────

test("waits as long as a Retry-After header asks, instead of guessing", async () => {
  const clock = virtualClock();
  const net = scriptedTransport(
    [
      { status: 429, headers: { "retry-after": "1" } },
      { status: 200, body: { ok: true } },
    ],
    clock,
  );
  const fetcher = createFetcher({
    transport: net.transport,
    clock,
    random: () => 0.25, // the computed wait would have been 25ms
    retry: { maxAttempts: 2, baseDelayMs: 100, maxDelayMs: 5000 },
  });

  await fetcher.fetchJson("https://api.test/thing");

  assert.deepEqual(offsets(net.requests), [0, 1000]);
});

// ── Cycle 11: retrying after the caller walked away is work nobody wants ────

test("stops retrying as soon as the caller aborts", async () => {
  const clock = virtualClock();
  const controller = new AbortController();
  const requestsAt: number[] = [];
  const transport = async (_url: string, _init?: RequestInit) => {
    requestsAt.push(clock.now());
    controller.abort(); // the caller gives up while the first attempt is in flight
    return new Response("{}", { status: 503 });
  };
  const fetcher = createFetcher({
    transport,
    clock,
    random: () => 1,
    retry: { maxAttempts: 4, baseDelayMs: 100 },
  });

  await assert.rejects(
    () => fetcher.fetchJson("https://api.test/thing", { signal: controller.signal }),
    (err: unknown) => err instanceof Error && err.name === "AbortError",
  );
  assert.deepEqual(requestsAt, [0]);
});
```

### Final run

```
> node --test test/fetcher.test.ts

✔ returns the parsed body when the first attempt succeeds
✔ throws HttpError carrying the status when the server keeps failing
✔ retries after a 503 and returns the body from the retry
✔ stops after the default attempt budget and surfaces the last failure
✔ does not retry a 400 — the request is wrong, not the server
✔ retries a 429 because the server is asking us to slow down
✔ honours a configured attempt budget
✔ spaces retries out with exponentially growing waits
✔ caps how long it will wait between attempts
✔ jitters each wait so retrying clients do not sync up
✔ retries when the connection itself fails
✔ waits as long as a Retry-After header asks, instead of guessing
✔ stops retrying as soon as the caller aborts
ℹ tests 13   ℹ pass 13   ℹ fail 0   ℹ duration_ms 86.03
```

---

## Deliberately not done

The skill is explicit that refactoring belongs to review, not to the red→green loop, so
two things are left standing as debt rather than fixed mid-cycle:

- **`FetcherDeps` is now misnamed.** It holds boundaries (`transport`, `clock`, `random`)
  *and* policy (`retry`). Splitting it is a rename across the public type — a review-stage
  change, not a green-step change.
- **Nothing was extracted.** The delay calculation could be its own pure function. It is
  three lines and every branch is covered through the seam; extracting it now would be
  refactoring inside the loop.

The only edit I made outside a red→green cycle was fixing the file's header comment, which
still read *"one request, no retry"*. Verified comment-only: a diff of both versions with
comment lines stripped is empty.

---

## Stress Test

**What is weakest here.**

1. **The seams were assumed, not confirmed.** Question 2 in the table (per-fetcher vs
   per-call policy) is the one that would hurt: if retry config belongs per-call, every test's
   arrange block changes and `RetryOptions` moves into `init`. The tests are correct about
   behaviour and possibly wrong about the shape of the API they test it through.
2. **`random: () => 1` is a value `Math.random` can never return** — it returns `[0, 1)`. Two
   tests therefore pin a boundary that is approached but never reached in production. Harmless
   for the schedule they are checking, but it is a fake that is very slightly *more* than the
   real thing.
3. **Types were not checked.** Node 24 strips TypeScript types without verifying them, and no
   `tsc` is available in this offline environment, so `tsc --noEmit` was **not run**. The tests
   prove runtime behaviour; they prove nothing about the types. A real repo must run the
   compiler in CI. I am stating this rather than implying the green suite covers it.
4. **Retrying a non-idempotent request is unguarded.** `fetchJson` will happily replay a
   `POST`. A 503 often means "the request landed and then the response was lost" — this code
   can duplicate a charge. It was not in scope and no test names it, which is exactly why it
   should be flagged loudly rather than left implicit. The right next slice is either
   "retries a GET but not a POST without an idempotency key" or a documented caller contract.
5. **A malformed JSON body is treated as a transient failure.** `response.json()` throws
   inside the `try`, so a 200 with broken JSON gets retried — pointlessly, since it will fail
   the same way. Found by reading the final code, not by a test; that is a gap in my slicing,
   not a gap the suite would catch.
6. **`isRetryableStatus` is too generous at the top end.** 501 and 505 are permanent
   conditions but count as 5xx here. Low blast radius, but three attempts with waits for a
   `501 Not Implemented` is wasted latency on every call.
7. **No test drives real time.** Every test uses the virtual clock, so `systemClock` — the
   code path that actually runs in production — is exercised by exactly nothing. A single
   slow integration test (`baseDelayMs: 1`, real clock, assert it completes) would close that,
   at the cost of the only non-instant test in the suite.

**What a smart critic would say.** "Eleven cycles to add a retry loop is theatre — you knew
the final shape before cycle 1." Partly fair: I did know roughly where it would land. But
three things came out of the loop that would not have come out of writing it in one go —
the jitter default silently breaking two earlier tests (a lurking flake, caught at the moment
it was created), the three tests that were sleeping for real and had pushed the suite to
897 ms, and the `try/catch` restructure in cycle 9 that only became obviously necessary once
cycles 6–8 had fixed the shape of the wait. The mutation check is the honest answer to the
theatre charge: seven mutations, seven caught, so the tests are load-bearing whatever order
they were written in.

**The assumption most likely to be wrong.** That retry belongs inside `fetchJson` at all.
`mocking.md` argues for SDK-style interfaces (`getUser(id)`) over generic fetchers, and
different endpoints deserve different policies — a 30-second report generation and a
100 ms lookup should not share a 3×100 ms budget. Putting the policy in the shared fetcher
makes it invisible at every call site, which is good for consistency and bad the day one
endpoint needs to opt out. The per-fetcher config is the escape hatch, and it only works if
callers actually construct their own fetcher instead of importing one shared singleton.
