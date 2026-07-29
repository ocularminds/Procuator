export interface Scenario {
  testId: string;
  name: string;
  description: string;
  supplierId: string;
  amount: number;
  payload: Record<string, unknown>;
}
interface ScenarioResponse {
  scenarios?: Record<string, unknown>[];
}

export class ScenarioMapper {
  fromResponse(response: ScenarioResponse): Scenario[] {
    return (response.scenarios ?? []).map((payload) => ({
      testId: String(payload.test_id),
      name: String(payload.scenario_name),
      description: String(payload.scenario_description),
      supplierId: String(payload.supplier_id),
      amount: Number(payload.amount),
      payload,
    }));
  }
}
