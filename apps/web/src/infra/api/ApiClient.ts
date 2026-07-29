export interface ApiClient {
  get<Result>(path: string): Promise<Result>;
  post<Result>(path: string, payload?: unknown): Promise<Result>;
}

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export class ProcuatorApiClient implements ApiClient {
  constructor(private readonly basePath = "/api/procuator") {}

  async get<Result>(path: string): Promise<Result> {
    return this.request<Result>(path, { cache: "no-store" });
  }

  async post<Result>(path: string, payload: unknown = {}): Promise<Result> {
    return this.request<Result>(path, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload),
    });
  }

  private async request<Result>(path: string, init: RequestInit): Promise<Result> {
    const response = await fetch(`${this.basePath}${path}`, init);
    const text = await response.text();
    const data = text ? JSON.parse(text) : null;

    if (!response.ok) {
      const detail = data?.detail ? JSON.stringify(data.detail) : `HTTP ${response.status}`;
      throw new ApiError(detail, response.status);
    }

    return data as Result;
  }
}

export const procuatorApi = new ProcuatorApiClient();
