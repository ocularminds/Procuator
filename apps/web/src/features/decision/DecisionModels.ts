export type Urgency = "standard" | "critical";

export interface DecisionFormValues {
  supplierId: string;
  industry: string;
  amount: number;
  budgetRemaining: number;
  approvalLimit: number;
  urgency: Urgency;
  supplierTransactions: number;
}
export interface DecisionResponse {
  decision: "APPROVE" | "REFER" | "DENY";
}

export class DecisionPayloadMapper {
  create(values: DecisionFormValues): Record<string, unknown> {
    return {
      supplier_id: values.supplierId,
      industry: values.industry,
      amount: values.amount,
      currency: "USD",
      budget_remaining: values.budgetRemaining,
      requester_approval_limit: values.approvalLimit,
      urgency: values.urgency,
      supplier_history: {
        total_transactions: values.supplierTransactions,
      },
    };
  }
}
