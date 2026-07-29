import { NextRequest, NextResponse } from "next/server";

interface ProxyContext {
  params: Promise<{ path: string[] }>;
}
export class ApiProxy {
  forward = async (request: NextRequest, context: ProxyContext) => {
    const params = await context.params;
    const target = this.buildTargetUrl(request, params.path);
    const init: RequestInit = {
      method: request.method,
      headers: {
        "content-type": request.headers.get("content-type") ?? "application/json",
        accept: request.headers.get("accept") ?? "application/json",
      },
      cache: "no-store",
    };

    if (request.method !== "GET" && request.method !== "HEAD") {
      init.body = await request.text();
    }

    const response = await fetch(target, init);
    return new NextResponse(await response.text(), {
      status: response.status,
      headers: {
        "content-type": response.headers.get("content-type") ?? "application/json",
      },
    });
  };

  private buildTargetUrl(request: NextRequest, pathParts: string[]): URL {
    const incomingUrl = new URL(request.url);
    const baseUrl = (process.env.API_BASE_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");
    const targetUrl = new URL(`${baseUrl}/${pathParts.join("/")}`);
    targetUrl.search = incomingUrl.search;
    return targetUrl;
  }
}
