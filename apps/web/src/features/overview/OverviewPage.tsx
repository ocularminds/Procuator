import Link from "next/link";

import { GlassCard } from "@/components/common/GlassCard";

interface OverviewItem {
  title: string;
  subtitle: string;
  description: string;
  href: string;
  action: string;
  primary?: boolean;
}
const overviewItems: OverviewItem[] = [
  {
    title: "Make a decision",
    subtitle: "Fill a request, get APPROVE / REFER / DENY",
    description: "Runs risk + policy and creates a referral when needed.",
    href: "/decision",
    action: "Open decision form",
    primary: true,
  },
  {
    title: "Demo scenarios",
    subtitle: "Three curated cases for a quick walkthrough",
    description: "Load server-provided scenarios and run them against the backend.",
    href: "/scenarios",
    action: "View scenarios",
  },
  {
    title: "Human-in-the-loop",
    subtitle: "Review and resolve pending referrals",
    description: "Any `REFER` decision creates a referral that can be approved or denied.",
    href: "/referrals",
    action: "Open referrals",
  },
  {
    title: "Analytics",
    subtitle: "Aggregated decision stats",
    description: "View counts by decision and top flags from the audit log.",
    href: "/analytics",
    action: "View analytics",
  },
];

export function OverviewPage() {
  return (
    <main className="mx-auto max-w-6xl px-5 py-10">
      <div className="mb-10">
        <h1 className="text-4xl font-semibold tracking-tight text-white">
          Procurement decisions, explained.
        </h1>
        <p className="mt-3 max-w-2xl text-base text-white/70">
          A simple frontend for the Procuator FastAPI backend: risk checks, policy evaluation,
          human-in-the-loop referrals, and decision analytics.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
        {overviewItems.map((item) => (
          <GlassCard key={item.href} title={item.title} subtitle={item.subtitle}>
            <p className="text-sm text-white/70">{item.description}</p>
            <div className="mt-5">
              <Link
                className={
                  item.primary
                    ? "inline-flex items-center rounded-xl bg-white px-4 py-2 text-sm font-semibold text-black hover:bg-white/90"
                    : "inline-flex items-center rounded-xl border border-white/15 bg-white/5 px-4 py-2 text-sm font-semibold text-white hover:bg-white/10"
                }
                href={item.href}
              >
                {item.action}
              </Link>
            </div>
          </GlassCard>
        ))}
      </div>
    </main>
  );
}
