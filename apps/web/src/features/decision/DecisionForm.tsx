"use client";

import { useState } from "react";

import { Button } from "@/components/common/Button";
import { Field } from "@/components/common/Field";
import { Input } from "@/components/common/Input";
import { Select } from "@/components/common/Select";
import {
  DecisionFormValues,
  DecisionPayloadMapper,
  Urgency,
} from "@/features/decision/DecisionModels";

interface DecisionFormProps {
  isLoading: boolean;
  decision?: string;
  onSubmit: (payload: Record<string, unknown>) => Promise<void>;
}
const initialValues: DecisionFormValues = {
  supplierId: "SUP-001",
  industry: "technology",
  amount: 1250,
  budgetRemaining: 50000,
  approvalLimit: 5000,
  urgency: "standard",
  supplierTransactions: 15,
};

const payloadMapper = new DecisionPayloadMapper();

export function DecisionForm({ isLoading, decision, onSubmit }: DecisionFormProps) {
  const [values, setValues] = useState(initialValues);

  function update<Field extends keyof DecisionFormValues>(
    field: Field,
    value: DecisionFormValues[Field],
  ) {
    setValues((current) => ({ ...current, [field]: value }));
  }

  return (
    <>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <Field label="Supplier ID">
          <Input
            value={values.supplierId}
            onChange={(event) => update("supplierId", event.target.value)}
          />
        </Field>

        <Field label="Industry">
          <Select
            value={values.industry}
            onChange={(event) => update("industry", event.target.value)}
          >
            <option value="technology">technology</option>
            <option value="manufacturing">manufacturing</option>
            <option value="healthcare">healthcare</option>
            <option value="retail">retail</option>
            <option value="general">general</option>
          </Select>
        </Field>

        <Field label="Amount (USD)">
          <Input
            type="number"
            value={values.amount}
            onChange={(event) => update("amount", Number(event.target.value))}
            min={0}
            step={50}
          />
        </Field>

        <Field label="Budget remaining">
          <Input
            type="number"
            value={values.budgetRemaining}
            onChange={(event) => update("budgetRemaining", Number(event.target.value))}
            min={0}
            step={100}
          />
        </Field>

        <Field label="Requester approval limit">
          <Input
            type="number"
            value={values.approvalLimit}
            onChange={(event) => update("approvalLimit", Number(event.target.value))}
            min={0}
            step={100}
          />
        </Field>

        <Field
          label="Supplier transactions"
          hint="Used by policy engine for new-supplier referral behavior"
        >
          <Input
            type="number"
            value={values.supplierTransactions}
            onChange={(event) => update("supplierTransactions", Number(event.target.value))}
            min={0}
            step={1}
          />
        </Field>

        <Field label="Urgency">
          <Select
            value={values.urgency}
            onChange={(event) => update("urgency", event.target.value as Urgency)}
          >
            <option value="standard">standard</option>
            <option value="critical">critical</option>
          </Select>
        </Field>
      </div>

      <div className="mt-6 flex items-center gap-3">
        <Button
          onClick={() => onSubmit(payloadMapper.create(values))}
          disabled={isLoading}
        >
          {isLoading ? "Running…" : "Run decision"}
        </Button>
        {decision && (
          <div className="text-sm text-white/80">
            Decision: <span className="font-semibold text-white">{decision}</span>
          </div>
        )}
      </div>
    </>
  );
}
