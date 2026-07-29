"use client";

import type { ReactNode } from "react";

interface FieldProps {
  label: string;
  children: ReactNode;
  hint?: string;
}
export function Field({ label, children, hint }: FieldProps) {
  return (
    <label className="block">
      <div className="mb-1 text-sm font-medium text-white/85">{label}</div>
      {children}
      {hint && <div className="mt-1 text-xs text-white/55">{hint}</div>}
    </label>
  );
}
