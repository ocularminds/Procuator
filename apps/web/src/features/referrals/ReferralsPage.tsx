"use client";

import { useCallback, useEffect, useState } from "react";

import { Button } from "@/components/common/Button";
import { GlassCard } from "@/components/common/GlassCard";
import { JsonBlock } from "@/components/common/JsonBlock";
import { PageHeader } from "@/components/common/PageHeader";
import { ReferralList } from "@/features/referrals/ReferralList";
import { Referral, ReferralMapper } from "@/features/referrals/ReferralModels";
import { procuatorApi } from "@/infra/api/ApiClient";

const referralMapper = new ReferralMapper();

export function ReferralsPage() {
  const [pending, setPending] = useState<Referral[]>([]);
  const [selected, setSelected] = useState<Referral | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await procuatorApi.get<{ pending?: Record<string, unknown>[] }>(
        "/referrals",
      );
      const referrals = referralMapper.fromResponse(response);
      setPending(referrals);
      setSelected(referrals[0] ?? null);
    } catch (requestError) {
      setError(
        requestError instanceof Error ? requestError.message : "Failed to load referrals",
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  async function resolve(action: "approve" | "deny") {
    if (!selected) return;
    setIsLoading(true);
    setError(null);

    try {
      await procuatorApi.post(`/referrals/${selected.referralId}/${action}`);
      await refresh();
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Action failed");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-6xl px-5 py-10">
      <PageHeader
        title="Referrals"
        description="Pending human-in-the-loop items created by `REFER` decisions."
      />

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <GlassCard title="Pending" subtitle="Select a referral to review">
          <ReferralList referrals={pending} selected={selected} onSelect={setSelected} />

          <div className="mt-5 flex flex-wrap items-center gap-3">
            <Button onClick={refresh} disabled={isLoading} className="bg-white/90">
              Refresh
            </Button>
            <Button onClick={() => resolve("approve")} disabled={isLoading || !selected}>
              Approve
            </Button>
            <Button
              onClick={() => resolve("deny")}
              disabled={isLoading || !selected}
              className="bg-white/85"
            >
              Deny
            </Button>
          </div>

          {error && <div className="mt-4 text-sm text-red-200">{error}</div>}
        </GlassCard>

        <GlassCard title="Details" subtitle="Selected referral payload">
          {selected ? (
            <JsonBlock value={selected.raw} />
          ) : (
            <div className="text-sm text-white/60">Nothing selected.</div>
          )}
        </GlassCard>
      </div>
    </main>
  );
}
