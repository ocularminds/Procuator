export interface Referral {
  referralId: string;
  createdAt: string;
  status: "PENDING" | "APPROVED" | "DENIED";
  proposedDecision: string;
  requestId: string;
  raw: Record<string, unknown>;
}
interface ReferralListResponse {
  pending?: Record<string, unknown>[];
}

export class ReferralMapper {
  fromResponse(response: ReferralListResponse): Referral[] {
    return (response.pending ?? []).map((raw) => {
      const request = (raw.request ?? {}) as Record<string, unknown>;
      return {
        referralId: String(raw.referral_id),
        createdAt: String(raw.created_at),
        status: String(raw.status) as Referral["status"],
        proposedDecision: String(raw.proposed_decision),
        requestId: String(request.request_id),
        raw,
      };
    });
  }
}
