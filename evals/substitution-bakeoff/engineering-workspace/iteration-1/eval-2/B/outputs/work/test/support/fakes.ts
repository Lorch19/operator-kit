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
