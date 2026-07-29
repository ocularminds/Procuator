"use client";

import { useState } from "react";

import { GlassCard } from "@/components/common/GlassCard";
import { JsonBlock } from "@/components/common/JsonBlock";
import { PageHeader } from "@/components/common/PageHeader";
import { DecisionForm } from "@/features/decision/DecisionForm";
import { DecisionResponse } from "@/features/decision/DecisionModels";
import { procuatorApi } from "@/infra/api/ApiClient";

export function DecisionPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<unknown>(null);

  async function submit(payload: Record<string, unknown>) {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      setResult(await procuatorApi.post("/decision", payload));
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unknown error");
    } finally {
      setIsLoading(false);
    }
  }

  const decision = (result as DecisionResponse | null)?.decision;

  return (
    <main className="mx-auto max-w-6xl px-5 py-10">
      <PageHeader
        title="Decision"
        description="Submit a request to the backend. The backend combines policy + risk and may create a human referral."
      />

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <GlassCard title="Request" subtitle="A small set of fields for the demo">
          <DecisionForm isLoading={isLoading} decision={decision} onSubmit={submit} />
          {error && <div className="mt-4 text-sm text-red-200">{error}</div>}
        </GlassCard>

        <GlassCard title="Result" subtitle="Raw JSON returned by the API">
          {result ? (
            <JsonBlock value={result} />
          ) : (
            <div className="text-sm text-white/60">No result yet.</div>
          )}
        </GlassCard>
      </div>
    </main>
  );
}
