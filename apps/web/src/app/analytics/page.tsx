"use client";

import { useEffect, useState } from "react";

import { GlassCard } from "@/components/GlassCard";
import { JsonBlock } from "@/components/JsonBlock";

type Analytics = {
  total: number;
  avg_risk_score: number | null;
  counts_by_decision: Record<string, number>;
  top_flags: Array<{ flag: string; count: number }>;
};

export default function AnalyticsPage() {
  const [data, setData] = useState<Analytics | null>(null);
  const [raw, setRaw] = useState<unknown>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setError(null);
      const res = await fetch("/api/procuator/analytics", { cache: "no-store" });
      const json = await res.json();
      if (cancelled) return;
      setRaw(json);
      setData(json as Analytics);
    })().catch((e) => {
      setError(e instanceof Error ? e.message : "Failed to load analytics");
    });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <main className="mx-auto max-w-6xl px-5 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-semibold tracking-tight text-white">Analytics</h1>
        <p className="mt-2 text-white/70">Aggregated stats from the backend audit events.</p>
      </div>

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <GlassCard title="Summary" subtitle="Counts and top flags">
          {error && <div className="text-sm text-red-200">{error}</div>}
          {!data && !error && <div className="text-sm text-white/60">Loading…</div>}
          {data && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                  <div className="text-xs text-white/60">Total events</div>
                  <div className="mt-1 text-2xl font-semibold text-white">{data.total}</div>
                </div>
                <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                  <div className="text-xs text-white/60">Avg risk score</div>
                  <div className="mt-1 text-2xl font-semibold text-white">
                    {data.avg_risk_score == null ? "—" : data.avg_risk_score}
                  </div>
                </div>
              </div>

              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="text-sm font-semibold text-white">Counts by decision</div>
                <div className="mt-3 grid grid-cols-3 gap-2">
                  {Object.entries(data.counts_by_decision ?? {}).map(([k, v]) => (
                    <div key={k} className="rounded-xl border border-white/10 bg-black/20 p-3">
                      <div className="text-xs text-white/60">{k}</div>
                      <div className="mt-1 text-lg font-semibold text-white">{v}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="text-sm font-semibold text-white">Top flags</div>
                <div className="mt-3 space-y-2">
                  {(data.top_flags ?? []).slice(0, 8).map((f) => (
                    <div
                      key={f.flag}
                      className="flex items-center justify-between rounded-xl border border-white/10 bg-black/20 px-3 py-2"
                    >
                      <div className="text-sm text-white/80">{f.flag}</div>
                      <div className="text-sm font-semibold text-white">{f.count}</div>
                    </div>
                  ))}
                  {(data.top_flags ?? []).length === 0 && <div className="text-sm text-white/60">No flags yet.</div>}
                </div>
              </div>
            </div>
          )}
        </GlassCard>

        <GlassCard title="Raw JSON" subtitle="Full response from /analytics">
          {raw ? <JsonBlock value={raw} /> : <div className="text-sm text-white/60">No data yet.</div>}
        </GlassCard>
      </div>
    </main>
  );
}
