"use client";

import { useEffect, useState } from "react";

import { GlassCard } from "@/components/GlassCard";
import { Button } from "@/components/Field";
import { JsonBlock } from "@/components/JsonBlock";

type Referral = {
  referral_id: string;
  created_at: string;
  status: "PENDING" | "APPROVED" | "DENIED";
  proposed_decision: string;
  request: Record<string, unknown>;
  explanation: string[];
};

export default function ReferralsPage() {
  const [pending, setPending] = useState<Referral[]>([]);
  const [selected, setSelected] = useState<Referral | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function refresh() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/procuator/referrals", { cache: "no-store" });
      const data = await res.json();
      const items = (data.pending ?? []) as Referral[];
      setPending(items);
      setSelected(items[0] ?? null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load referrals");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh().catch(() => undefined);
  }, []);

  async function act(action: "approve" | "deny") {
    if (!selected) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/procuator/referrals/${selected.referral_id}/${action}`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: "{}",
      });
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }
      await refresh();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Action failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-6xl px-5 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-semibold tracking-tight text-white">Referrals</h1>
        <p className="mt-2 text-white/70">Pending human-in-the-loop items created by `REFER` decisions.</p>
      </div>

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <GlassCard title="Pending" subtitle="Select a referral to review">
          <div className="space-y-2">
            {pending.length === 0 && (
              <div className="text-sm text-white/60">No pending referrals. Run a referral scenario first.</div>
            )}
            {pending.map((r) => {
              const active = selected?.referral_id === r.referral_id;
              return (
                <button
                  key={r.referral_id}
                  onClick={() => setSelected(r)}
                  className={
                    "w-full rounded-2xl border p-4 text-left transition " +
                    (active
                      ? "border-white/25 bg-white/10"
                      : "border-white/10 bg-white/5 hover:bg-white/10")
                  }
                >
                  <div className="flex items-center justify-between">
                    <div className="text-sm font-semibold text-white">{r.request?.request_id as string}</div>
                    <div className="text-xs text-white/55">{r.referral_id.slice(0, 8)}…</div>
                  </div>
                  <div className="mt-1 text-sm text-white/70">proposed: {r.proposed_decision}</div>
                  <div className="mt-2 text-xs text-white/55">created: {new Date(r.created_at).toLocaleString()}</div>
                </button>
              );
            })}
          </div>

          <div className="mt-5 flex flex-wrap items-center gap-3">
            <Button onClick={() => refresh()} disabled={loading} className="bg-white/90">
              Refresh
            </Button>
            <Button onClick={() => act("approve")} disabled={loading || !selected}>
              Approve
            </Button>
            <Button onClick={() => act("deny")} disabled={loading || !selected} className="bg-white/85">
              Deny
            </Button>
          </div>

          {error && <div className="mt-4 text-sm text-red-200">{error}</div>}
        </GlassCard>

        <GlassCard title="Details" subtitle="Selected referral payload">
          {selected ? <JsonBlock value={selected} /> : <div className="text-sm text-white/60">Nothing selected.</div>}
        </GlassCard>
      </div>
    </main>
  );
}
