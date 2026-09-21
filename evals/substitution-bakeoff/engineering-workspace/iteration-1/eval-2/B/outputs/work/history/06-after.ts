// The fetcher as it exists today: one request, no retry.
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
  /** Wait before the first retry; doubles on each subsequent retry. */
  baseDelayMs?: number;
}

export interface FetcherDeps {
  transport?: Transport;
  clock?: Clock;
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

  return {
    async fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
      let lastError: unknown;

      for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
        const response = await transport(url, init);
        if (response.ok) return (await response.json()) as T;
        lastError = new HttpError(response.status, url);
        if (!isRetryableStatus(response.status)) throw lastError;
        if (attempt < maxAttempts) {
          await clock.sleep(baseDelayMs * 2 ** (attempt - 1));
        }
      }

      throw lastError;
    },
  };
}
