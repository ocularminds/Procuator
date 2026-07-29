import { Analytics } from "@/features/analytics/AnalyticsModels";

interface AnalyticsSummaryProps {
  data: Analytics;
}
export function AnalyticsSummary({ data }: AnalyticsSummaryProps) {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-3">
        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <div className="text-xs text-white/60">Total events</div>
          <div className="mt-1 text-2xl font-semibold text-white">{data.total}</div>
        </div>
        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <div className="text-xs text-white/60">Avg risk score</div>
          <div className="mt-1 text-2xl font-semibold text-white">
            {data.averageRiskScore == null ? "—" : data.averageRiskScore}
          </div>
        </div>
      </div>

      <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
        <div className="text-sm font-semibold text-white">Counts by decision</div>
        <div className="mt-3 grid grid-cols-3 gap-2">
          {Object.entries(data.decisionCounts).map(([decision, count]) => (
            <div
              key={decision}
              className="rounded-xl border border-white/10 bg-black/20 p-3"
            >
              <div className="text-xs text-white/60">{decision}</div>
              <div className="mt-1 text-lg font-semibold text-white">{count}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
        <div className="text-sm font-semibold text-white">Top flags</div>
        <div className="mt-3 space-y-2">
          {data.topFlags.slice(0, 8).map((item) => (
            <div
              key={item.flag}
              className="flex items-center justify-between rounded-xl border border-white/10 bg-black/20 px-3 py-2"
            >
              <div className="text-sm text-white/80">{item.flag}</div>
              <div className="text-sm font-semibold text-white">{item.count}</div>
            </div>
          ))}
          {data.topFlags.length === 0 && (
            <div className="text-sm text-white/60">No flags yet.</div>
          )}
        </div>
      </div>
    </div>
  );
}
