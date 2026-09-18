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
