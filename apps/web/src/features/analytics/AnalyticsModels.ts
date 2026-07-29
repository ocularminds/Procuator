export interface FlagCount {
  flag: string;
  count: number;
}
export interface Analytics {
  total: number;
  averageRiskScore: number | null;
  decisionCounts: Record<string, number>;
  topFlags: FlagCount[];
}

export class AnalyticsMapper {
  fromResponse(raw: Record<string, unknown>): Analytics {
    return {
      total: Number(raw.total),
      averageRiskScore:
        raw.avg_risk_score == null ? null : Number(raw.avg_risk_score),
      decisionCounts: (raw.counts_by_decision ?? {}) as Record<string, number>,
      topFlags: (raw.top_flags ?? []) as FlagCount[],
    };
  }
}
