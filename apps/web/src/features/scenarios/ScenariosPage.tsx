"use client";

import { useEffect, useState } from "react";

import { Button } from "@/components/common/Button";
import { GlassCard } from "@/components/common/GlassCard";
import { JsonBlock } from "@/components/common/JsonBlock";
import { PageHeader } from "@/components/common/PageHeader";
import { ScenarioList } from "@/features/scenarios/ScenarioList";
import { Scenario, ScenarioMapper } from "@/features/scenarios/ScenarioModels";
import { procuatorApi } from "@/infra/api/ApiClient";

const scenarioMapper = new ScenarioMapper();

export function ScenariosPage() {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [selected, setSelected] = useState<Scenario | null>(null);
  const [result, setResult] = useState<unknown>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isCancelled = false;

    procuatorApi
      .get<{ scenarios?: Record<string, unknown>[] }>("/demo/scenarios")
      .then((response) => {
        if (isCancelled) return;
        const loadedScenarios = scenarioMapper.fromResponse(response);
        setScenarios(loadedScenarios);
        setSelected(loadedScenarios[0] ?? null);
      })
      .catch((requestError) => {
        if (!isCancelled) {
          setError(
            requestError instanceof Error ? requestError.message : "Failed to load scenarios",
          );
        }
      });

    return () => {
      isCancelled = true;
    };
  }, []);

  async function runScenario() {
    if (!selected) return;
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      setResult(await procuatorApi.post("/decision", selected.payload));
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Run failed");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-6xl px-5 py-10">
      <PageHeader
        title="Demo scenarios"
        description="Pick a scenario and run it against the decision endpoint."
      />

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <GlassCard title="Scenarios" subtitle="Server-provided demo cases">
          <ScenarioList scenarios={scenarios} selected={selected} onSelect={setSelected} />

          <div className="mt-5 flex items-center gap-3">
            <Button onClick={runScenario} disabled={!selected || isLoading}>
              {isLoading ? "Running…" : "Run selected"}
            </Button>
            {selected && (
              <div className="text-xs text-white/60">
                Selected: <span className="text-white/85">{selected.name}</span>
              </div>
            )}
          </div>

          {error && <div className="mt-4 text-sm text-red-200">{error}</div>}
        </GlassCard>

        <GlassCard title="Result" subtitle="Raw JSON from /decision">
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
