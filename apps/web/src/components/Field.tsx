"use client";

import { ReactNode } from "react";

export function Field({
  label,
  children,
  hint,
}: {
  label: string;
  children: ReactNode;
  hint?: string;
}) {
  return (
    <label className="block">
      <div className="mb-1 text-sm font-medium text-white/85">{label}</div>
      {children}
      {hint && <div className="mt-1 text-xs text-white/55">{hint}</div>}
    </label>
  );
}

export function Input(props: React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      {...props}
      className={
        "w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-white/40 outline-none focus:border-white/25 focus:bg-white/10 " +
        (props.className ?? "")
      }
    />
  );
}

export function Select(props: React.SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <select
      {...props}
      className={
        "w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white outline-none focus:border-white/25 focus:bg-white/10 " +
        (props.className ?? "")
      }
    />
  );
}

export function Button(props: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      {...props}
      className={
        "rounded-xl bg-white px-4 py-2 text-sm font-semibold text-black shadow-lg shadow-white/10 hover:bg-white/90 disabled:cursor-not-allowed disabled:opacity-50 " +
        (props.className ?? "")
      }
    />
  );
}
