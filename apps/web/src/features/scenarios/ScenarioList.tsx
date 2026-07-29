"use client";

import { Scenario } from "@/features/scenarios/ScenarioModels";

interface ScenarioListProps {
  scenarios: Scenario[];
  selected: Scenario | null;
  onSelect: (scenario: Scenario) => void;
}
export function ScenarioList({ scenarios, selected, onSelect }: ScenarioListProps) {
  return (
    <div className="space-y-2">
      {scenarios.map((scenario) => {
        const isActive = selected?.testId === scenario.testId;
        return (
          <button
            key={scenario.testId}
            onClick={() => onSelect(scenario)}
            className={
              "w-full rounded-2xl border p-4 text-left transition " +
              (isActive
                ? "border-white/25 bg-white/10"
                : "border-white/10 bg-white/5 hover:bg-white/10")
            }
          >
            <div className="flex items-center justify-between">
              <div className="text-sm font-semibold text-white">{scenario.name}</div>
              <div className="text-xs text-white/55">{scenario.testId}</div>
            </div>
            <div className="mt-1 text-sm text-white/70">{scenario.description}</div>
            <div className="mt-2 text-xs text-white/55">
              supplier={scenario.supplierId} • amount={scenario.amount}
            </div>
          </button>
        );
      })}
    </div>
  );
}
