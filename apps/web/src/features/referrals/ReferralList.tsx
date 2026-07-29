"use client";

import { Referral } from "@/features/referrals/ReferralModels";

interface ReferralListProps {
  referrals: Referral[];
  selected: Referral | null;
  onSelect: (referral: Referral) => void;
}
export function ReferralList({ referrals, selected, onSelect }: ReferralListProps) {
  if (referrals.length === 0) {
    return (
      <div className="text-sm text-white/60">
        No pending referrals. Run a referral scenario first.
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {referrals.map((referral) => {
        const isActive = selected?.referralId === referral.referralId;
        return (
          <button
            key={referral.referralId}
            onClick={() => onSelect(referral)}
            className={
              "w-full rounded-2xl border p-4 text-left transition " +
              (isActive
                ? "border-white/25 bg-white/10"
                : "border-white/10 bg-white/5 hover:bg-white/10")
            }
          >
            <div className="flex items-center justify-between">
              <div className="text-sm font-semibold text-white">{referral.requestId}</div>
              <div className="text-xs text-white/55">
                {referral.referralId.slice(0, 8)}…
              </div>
            </div>
            <div className="mt-1 text-sm text-white/70">
              proposed: {referral.proposedDecision}
            </div>
            <div className="mt-2 text-xs text-white/55">
              created: {new Date(referral.createdAt).toLocaleString()}
            </div>
          </button>
        );
      })}
    </div>
  );
}
