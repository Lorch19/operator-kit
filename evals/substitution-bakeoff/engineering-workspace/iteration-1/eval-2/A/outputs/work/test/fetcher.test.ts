import { test } from 'node:test';
import assert from 'node:assert/strict';
import { fetchJson, HttpError } from '../src/fetcher.ts';
import { instantSleep, scriptedTransport } from '../test-support/transport.ts';

// Characterisation tests: these pin the fetcher's PRE-EXISTING behaviour so the
// retry work cannot silently change it.

test('returns the parsed JSON body on success', async () => {
  const transport = scriptedTransport([200], { id: 7 });
  const result = await fetchJson<{ id: number }>('https://api.test/thing', {
    fetchImpl: transport.fetchImpl,
  });
  assert.deepEqual(result, { id: 7 });
});

test('throws HttpError carrying the status on a non-2xx response', async () => {
  const transport = scriptedTransport([500]);
  await assert.rejects(
    () =>
      fetchJson('https://api.test/thing', {
        fetchImpl: transport.fetchImpl,
        retry: { sleep: instantSleep },
      }),
    (error: unknown) => error instanceof HttpError && error.status === 500,
  );
});
