// The fetcher as it exists today: one request, no retry.
export type Transport = (url: string, init?: RequestInit) => Promise<Response>;

export interface FetcherDeps {
  transport?: Transport;
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

export interface Fetcher {
  fetchJson<T>(url: string, init?: RequestInit): Promise<T>;
}

export function createFetcher(deps: FetcherDeps = {}): Fetcher {
  const transport: Transport =
    deps.transport ?? ((url, init) => globalThis.fetch(url, init));

  return {
    async fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
      let response = await transport(url, init);
      if (response.status === 503) {
        response = await transport(url, init);
      }
      if (!response.ok) throw new HttpError(response.status, url);
      return (await response.json()) as T;
    },
  };
}
