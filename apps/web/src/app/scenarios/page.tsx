"use client";

import { useEffect, useMemo, useState } from "react";

import { GlassCard } from "@/components/GlassCard";
import { Button } from "@/components/Field";
import { JsonBlock } from "@/components/JsonBlock";

type Scenario = {
  test_id: string;
  scenario_name: string;
  scenario_description: string;
  supplier_id: string;
  industry?: string;
  amount: number;
  budget_remaining?: number;
  requester_approval_limit?: number;
  [k: string]: unknown;
};

export default function ScenariosPage() {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [selected, setSelected] = useState<Scenario | null>(null);
  const [result, setResult] = useState<unknown>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setError(null);
      const res = await fetch("/api/procuator/demo/scenarios");
      const data = await res.json();
      if (cancelled) return;
      setScenarios(data.scenarios ?? []);
      setSelected((data.scenarios ?? [])[0] ?? null);
    })().catch((e) => {
      setError(e instanceof Error ? e.message : "Failed to load scenarios");
    });
    return () => {
      cancelled = true;
    };
  }, []);

  const canRun = useMemo(() => !!selected && !loading, [selected, loading]);

  async function runScenario() {
    if (!selected) return;
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch("/api/procuator/decision", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(selected),
      });
      const text = await res.text();
      const parsed = text ? JSON.parse(text) : null;
      if (!res.ok) {
        throw new Error(parsed?.detail ? JSON.stringify(parsed.detail) : `HTTP ${res.status}`);
      }
      setResult(parsed);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Run failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-6xl px-5 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-semibold tracking-tight text-white">Demo scenarios</h1>
        <p className="mt-2 text-white/70">Pick a scenario and run it against the decision endpoint.</p>
      </div>

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <GlassCard title="Scenarios" subtitle="Server-provided demo cases">
          <div className="space-y-2">
            {scenarios.map((s) => {
              const active = selected?.test_id === s.test_id;
              return (
                <button
                  key={s.test_id}
                  onClick={() => setSelected(s)}
                  className={
                    "w-full rounded-2xl border p-4 text-left transition " +
                    (active
                      ? "border-white/25 bg-white/10"
                      : "border-white/10 bg-white/5 hover:bg-white/10")
                  }
                >
                  <div className="flex items-center justify-between">
                    <div className="text-sm font-semibold text-white">{s.scenario_name}</div>
                    <div className="text-xs text-white/55">{s.test_id}</div>
                  </div>
                  <div className="mt-1 text-sm text-white/70">{s.scenario_description}</div>
                  <div className="mt-2 text-xs text-white/55">
                    supplier={s.supplier_id} • amount={s.amount}
                  </div>
                </button>
              );
            })}
          </div>

          <div className="mt-5 flex items-center gap-3">
            <Button onClick={runScenario} disabled={!canRun}>
              {loading ? "Running…" : "Run selected"}
            </Button>
            {selected && (
              <div className="text-xs text-white/60">
                Selected: <span className="text-white/85">{selected.scenario_name}</span>
              </div>
            )}
          </div>

          {error && <div className="mt-4 text-sm text-red-200">{error}</div>}
        </GlassCard>

        <GlassCard title="Result" subtitle="Raw JSON from /decision">
          {result ? <JsonBlock value={result} /> : <div className="text-sm text-white/60">No result yet.</div>}
        </GlassCard>
      </div>
    </main>
  );
}
