import { ApiProxy } from "@/infra/api/ApiProxy";

const apiProxy = new ApiProxy();

export const GET = apiProxy.forward;
export const POST = apiProxy.forward;
export const PUT = apiProxy.forward;
export const PATCH = apiProxy.forward;
export const DELETE = apiProxy.forward;
