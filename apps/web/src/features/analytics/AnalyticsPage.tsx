"use client";

import { useEffect, useState } from "react";

import { GlassCard } from "@/components/common/GlassCard";
import { JsonBlock } from "@/components/common/JsonBlock";
import { PageHeader } from "@/components/common/PageHeader";
import { Analytics, AnalyticsMapper } from "@/features/analytics/AnalyticsModels";
import { AnalyticsSummary } from "@/features/analytics/AnalyticsSummary";
import { procuatorApi } from "@/infra/api/ApiClient";

const analyticsMapper = new AnalyticsMapper();

export function AnalyticsPage() {
  const [data, setData] = useState<Analytics | null>(null);
  const [raw, setRaw] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isCancelled = false;

    procuatorApi
      .get<Record<string, unknown>>("/analytics")
      .then((response) => {
        if (isCancelled) return;
        setRaw(response);
        setData(analyticsMapper.fromResponse(response));
      })
      .catch((requestError) => {
        if (!isCancelled) {
          setError(
            requestError instanceof Error ? requestError.message : "Failed to load analytics",
          );
        }
      });

    return () => {
      isCancelled = true;
    };
  }, []);

  return (
    <main className="mx-auto max-w-6xl px-5 py-10">
      <PageHeader
        title="Analytics"
        description="Aggregated stats from the backend audit events."
      />

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <GlassCard title="Summary" subtitle="Counts and top flags">
          {error && <div className="text-sm text-red-200">{error}</div>}
          {!data && !error && <div className="text-sm text-white/60">Loading…</div>}
          {data && <AnalyticsSummary data={data} />}
        </GlassCard>

        <GlassCard title="Raw JSON" subtitle="Full response from /analytics">
          {raw ? (
            <JsonBlock value={raw} />
          ) : (
            <div className="text-sm text-white/60">No data yet.</div>
          )}
        </GlassCard>
      </div>
    </main>
  );
}
