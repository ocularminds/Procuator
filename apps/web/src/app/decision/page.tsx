"use client";

import { useMemo, useState } from "react";

import { GlassCard } from "@/components/GlassCard";
import { Button, Field, Input, Select } from "@/components/Field";
import { JsonBlock } from "@/components/JsonBlock";

type DecisionResponse = {
  request_id: string;
  supplier_id: string;
  decision: "APPROVE" | "REFER" | "DENY";
  explanation: string[];
  human_in_the_loop?: { required: boolean; referral_id?: string };
};

export default function DecisionPage() {
  const [supplierId, setSupplierId] = useState("SUP-001");
  const [industry, setIndustry] = useState("technology");
  const [amount, setAmount] = useState(1250);
  const [budgetRemaining, setBudgetRemaining] = useState(50000);
  const [approvalLimit, setApprovalLimit] = useState(5000);
  const [urgency, setUrgency] = useState<"standard" | "critical">("standard");
  const [supplierTransactions, setSupplierTransactions] = useState(15);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<unknown>(null);

  const payload = useMemo(
    () => ({
      supplier_id: supplierId,
      industry,
      amount,
      currency: "USD",
      budget_remaining: budgetRemaining,
      requester_approval_limit: approvalLimit,
      urgency,
      supplier_history: {
        total_transactions: supplierTransactions,
      },
    }),
    [supplierId, industry, amount, budgetRemaining, approvalLimit, urgency, supplierTransactions],
  );

  async function submit() {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch("/api/procuator/decision", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(payload),
      });

      const text = await res.text();
      const data = text ? JSON.parse(text) : null;

      if (!res.ok) {
        throw new Error(data?.detail ? JSON.stringify(data.detail) : `HTTP ${res.status}`);
      }

      setResult(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  const summary = (result as DecisionResponse | null)?.decision;

  return (
    <main className="mx-auto max-w-6xl px-5 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-semibold tracking-tight text-white">Decision</h1>
        <p className="mt-2 text-white/70">
          Submit a request to the backend. The backend combines policy + risk and may create a human referral.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <GlassCard title="Request" subtitle="A small set of fields for the demo">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Supplier ID">
              <Input value={supplierId} onChange={(e) => setSupplierId(e.target.value)} />
            </Field>

            <Field label="Industry">
              <Select value={industry} onChange={(e) => setIndustry(e.target.value)}>
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
                value={amount}
                onChange={(e) => setAmount(Number(e.target.value))}
                min={0}
                step={50}
              />
            </Field>

            <Field label="Budget remaining">
              <Input
                type="number"
                value={budgetRemaining}
                onChange={(e) => setBudgetRemaining(Number(e.target.value))}
                min={0}
                step={100}
              />
            </Field>

            <Field label="Requester approval limit">
              <Input
                type="number"
                value={approvalLimit}
                onChange={(e) => setApprovalLimit(Number(e.target.value))}
                min={0}
                step={100}
              />
            </Field>

            <Field label="Supplier transactions" hint="Used by policy engine for new-supplier referral behavior">
              <Input
                type="number"
                value={supplierTransactions}
                onChange={(e) => setSupplierTransactions(Number(e.target.value))}
                min={0}
                step={1}
              />
            </Field>

            <Field label="Urgency">
              <Select value={urgency} onChange={(e) => setUrgency(e.target.value as "standard" | "critical")}>
                <option value="standard">standard</option>
                <option value="critical">critical</option>
              </Select>
            </Field>
          </div>

          <div className="mt-6 flex items-center gap-3">
            <Button onClick={submit} disabled={loading}>
              {loading ? "Running…" : "Run decision"}
            </Button>
            {summary && (
              <div className="text-sm text-white/80">
                Decision: <span className="font-semibold text-white">{summary}</span>
              </div>
            )}
          </div>

          {error && <div className="mt-4 text-sm text-red-200">{error}</div>}
        </GlassCard>

        <GlassCard title="Result" subtitle="Raw JSON returned by the API">
          {result ? <JsonBlock value={result} /> : <div className="text-sm text-white/60">No result yet.</div>}
        </GlassCard>
      </div>
    </main>
  );
}
