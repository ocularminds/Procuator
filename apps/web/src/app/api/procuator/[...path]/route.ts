import { NextRequest, NextResponse } from "next/server";

function getApiBaseUrl() {
  return (process.env.API_BASE_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");
}

function buildTargetUrl(req: NextRequest, pathParts: string[]) {
  const incomingUrl = new URL(req.url);
  const base = getApiBaseUrl();
  const target = new URL(`${base}/${pathParts.join("/")}`);
  target.search = incomingUrl.search;
  return target;
}

async function proxy(req: NextRequest, params: { path: string[] }) {
  const target = buildTargetUrl(req, params.path);

  const contentType = req.headers.get("content-type") ?? "application/json";
  const accept = req.headers.get("accept") ?? "application/json";

  const init: RequestInit = {
    method: req.method,
    headers: {
      "content-type": contentType,
      accept,
    },
    cache: "no-store",
  };

  if (req.method !== "GET" && req.method !== "HEAD") {
    init.body = await req.text();
  }

  const res = await fetch(target, init);
  const body = await res.text();

  return new NextResponse(body, {
    status: res.status,
    headers: {
      "content-type": res.headers.get("content-type") ?? "application/json",
    },
  });
}

export async function GET(req: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const params = await ctx.params;
  return proxy(req, params);
}

export async function POST(req: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const params = await ctx.params;
  return proxy(req, params);
}

export async function PUT(req: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const params = await ctx.params;
  return proxy(req, params);
}

export async function PATCH(req: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const params = await ctx.params;
  return proxy(req, params);
}

export async function DELETE(req: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const params = await ctx.params;
  return proxy(req, params);
}
