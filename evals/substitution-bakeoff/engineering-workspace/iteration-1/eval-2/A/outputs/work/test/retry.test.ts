import { test } from 'node:test';
import assert from 'node:assert/strict';
import { fetchJson, HttpError } from '../src/fetcher.ts';
import { instantSleep, scriptedTransport } from '../test-support/transport.ts';

test('retries after a transient network failure and returns the body', async () => {
  const transport = scriptedTransport([new Error('ECONNRESET'), 200], { id: 7 });

  const result = await fetchJson<{ id: number }>('https://api.test/thing', {
    fetchImpl: transport.fetchImpl,
    retry: { sleep: instantSleep },
  });

  assert.deepEqual(result, { id: 7 });
  assert.equal(transport.calls, 2);
});

test('makes 3 attempts by default before giving up', async () => {
  const transport = scriptedTransport([new Error('ECONNRESET')]);

  await assert.rejects(() =>
    fetchJson('https://api.test/thing', {
      fetchImpl: transport.fetchImpl,
      retry: { sleep: instantSleep },
    }),
  );

  assert.equal(transport.calls, 3);
});

test('honours a configured maxAttempts', async () => {
  const transport = scriptedTransport([new Error('ECONNRESET')]);

  await assert.rejects(() =>
    fetchJson('https://api.test/thing', {
      fetchImpl: transport.fetchImpl,
      retry: { maxAttempts: 5, sleep: instantSleep },
    }),
  );

  assert.equal(transport.calls, 5);
});

test('waits with exponential backoff between attempts', async () => {
  const transport = scriptedTransport([new Error('ECONNRESET')]);
  const waits: number[] = [];

  await assert.rejects(() =>
    fetchJson('https://api.test/thing', {
      fetchImpl: transport.fetchImpl,
      retry: {
        maxAttempts: 4,
        baseDelayMs: 100,
        jitter: false,
        sleep: async (ms: number) => {
          waits.push(ms);
        },
      },
    }),
  );

  assert.deepEqual(waits, [100, 200, 400]);
});

// Regression: a delay must only occur BETWEEN attempts. Sleeping after the final
// failed attempt makes every exhausted retry pay a pointless extra wait.
test('does not wait after the final attempt', async () => {
  const transport = scriptedTransport([new Error('ECONNRESET')]);
  const waits: number[] = [];

  await assert.rejects(() =>
    fetchJson('https://api.test/thing', {
      fetchImpl: transport.fetchImpl,
      retry: {
        maxAttempts: 3,
        jitter: false,
        sleep: async (ms: number) => {
          waits.push(ms);
        },
      },
    }),
  );

  assert.equal(waits.length, 2, '3 attempts should be separated by exactly 2 waits');
});

test('caps the backoff delay at maxDelayMs', async () => {
  const transport = scriptedTransport([new Error('ECONNRESET')]);
  const waits: number[] = [];

  await assert.rejects(() =>
    fetchJson('https://api.test/thing', {
      fetchImpl: transport.fetchImpl,
      retry: {
        maxAttempts: 6,
        baseDelayMs: 100,
        maxDelayMs: 500,
        jitter: false,
        sleep: async (ms: number) => {
          waits.push(ms);
        },
      },
    }),
  );

  assert.deepEqual(waits, [100, 200, 400, 500, 500]);
});

test('does not retry a 400 client error', async () => {
  const transport = scriptedTransport([400]);

  await assert.rejects(
    () =>
      fetchJson('https://api.test/thing', {
        fetchImpl: transport.fetchImpl,
        retry: { sleep: instantSleep },
      }),
    (error: unknown) => error instanceof HttpError && error.status === 400,
  );

  assert.equal(transport.calls, 1, 'a malformed request will never succeed on retry');
});

test('retries a 429 rate-limit response', async () => {
  const transport = scriptedTransport([429, 429, 200], { id: 7 });

  const result = await fetchJson<{ id: number }>('https://api.test/thing', {
    fetchImpl: transport.fetchImpl,
    retry: { sleep: instantSleep },
  });

  assert.deepEqual(result, { id: 7 });
  assert.equal(transport.calls, 3, '429 is a 4xx, but backing off is exactly the fix');
});

test('retries a 408 request-timeout response', async () => {
  const transport = scriptedTransport([408, 200], { id: 7 });

  const result = await fetchJson<{ id: number }>('https://api.test/thing', {
    fetchImpl: transport.fetchImpl,
    retry: { sleep: instantSleep },
  });

  assert.deepEqual(result, { id: 7 });
  assert.equal(transport.calls, 2);
});

// When many clients fail at the same instant, identical backoff schedules make them
// all retry at the same instant too, re-creating the load that caused the failure.
test('spreads retries with jitter by default so clients do not retry in lockstep', async () => {
  const transport = scriptedTransport([new Error('ECONNRESET')]);
  const waits: number[] = [];

  await assert.rejects(() =>
    fetchJson('https://api.test/thing', {
      fetchImpl: transport.fetchImpl,
      retry: {
        maxAttempts: 4,
        baseDelayMs: 100,
        random: () => 0.5,
        sleep: async (ms: number) => {
          waits.push(ms);
        },
      },
    }),
  );

  assert.deepEqual(waits, [50, 100, 200]);
});
