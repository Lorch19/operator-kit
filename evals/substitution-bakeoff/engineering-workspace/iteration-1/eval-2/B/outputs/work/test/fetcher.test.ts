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
