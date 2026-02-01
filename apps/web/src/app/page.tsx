import Link from "next/link";

import { GlassCard } from "@/components/GlassCard";

export default function Home() {
  return (
    <main className="mx-auto max-w-6xl px-5 py-10">
      <div className="mb-10">
        <h1 className="text-4xl font-semibold tracking-tight text-white">
          Procurement decisions, explained.
        </h1>
        <p className="mt-3 max-w-2xl text-base text-white/70">
          A simple frontend for the Procuator FastAPI backend: risk checks, policy evaluation, human-in-the-loop
          referrals, and decision analytics.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
        <GlassCard
          title="Make a decision"
          subtitle="Fill a request, get APPROVE / REFER / DENY"
        >
          <p className="text-sm text-white/70">
            Runs risk + policy and creates a referral when needed.
          </p>
          <div className="mt-5">
            <Link
              className="inline-flex items-center rounded-xl bg-white px-4 py-2 text-sm font-semibold text-black hover:bg-white/90"
              href="/decision"
            >
              Open decision form
            </Link>
          </div>
        </GlassCard>

        <GlassCard
          title="Demo scenarios"
          subtitle="Three curated cases for a quick walkthrough"
        >
          <p className="text-sm text-white/70">
            Load server-provided scenarios and run them against the backend.
          </p>
          <div className="mt-5">
            <Link
              className="inline-flex items-center rounded-xl border border-white/15 bg-white/5 px-4 py-2 text-sm font-semibold text-white hover:bg-white/10"
              href="/scenarios"
            >
              View scenarios
            </Link>
          </div>
        </GlassCard>

        <GlassCard
          title="Human-in-the-loop"
          subtitle="Review and resolve pending referrals"
        >
          <p className="text-sm text-white/70">
            Any `REFER` decision creates a referral that can be approved or denied.
          </p>
          <div className="mt-5">
            <Link
              className="inline-flex items-center rounded-xl border border-white/15 bg-white/5 px-4 py-2 text-sm font-semibold text-white hover:bg-white/10"
              href="/referrals"
            >
              Open referrals
            </Link>
          </div>
        </GlassCard>

        <GlassCard
          title="Analytics"
          subtitle="Aggregated decision stats"
        >
          <p className="text-sm text-white/70">
            View counts by decision and top flags from the audit log.
          </p>
          <div className="mt-5">
            <Link
              className="inline-flex items-center rounded-xl border border-white/15 bg-white/5 px-4 py-2 text-sm font-semibold text-white hover:bg-white/10"
              href="/analytics"
            >
              View analytics
            </Link>
          </div>
        </GlassCard>
      </div>
    </main>
  );
}
