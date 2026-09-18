/**
 * A scripted fetch transport. Each entry is played in order:
 *   - a number -> respond with that HTTP status and a JSON body
 *   - an Error -> reject with it (a network-level failure)
 * When the script runs out, the last step repeats.
 *
 * `calls` records how many times the transport was actually invoked.
 * This is a plain closure, not a mocking framework: tests assert on the
 * fetcher's real observable behaviour, never on a mock's bookkeeping API.
 */
export type Step = number | Error;

export interface Transport {
  fetchImpl: typeof fetch;
  readonly calls: number;
}

export function scriptedTransport(steps: Step[], body: unknown = { ok: true }): Transport {
  let calls = 0;
  const fetchImpl = (async () => {
    const step = steps[Math.min(calls, steps.length - 1)];
    calls++;
    if (step instanceof Error) throw step;
    return new Response(JSON.stringify(body), {
      status: step,
      headers: { 'content-type': 'application/json' },
    });
  }) as unknown as typeof fetch;
  return {
    fetchImpl,
    get calls() {
      return calls;
    },
  };
}

/** A sleep that returns immediately: keeps unit tests off the real clock. */
export const instantSleep = async (_ms: number): Promise<void> => {};
