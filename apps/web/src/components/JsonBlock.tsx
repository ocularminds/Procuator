"use client";

export function JsonBlock({ value }: { value: unknown }) {
  return (
    <pre className="max-h-[520px] overflow-auto rounded-2xl border border-white/10 bg-black/30 p-4 text-xs leading-relaxed text-white/85">
      {JSON.stringify(value, null, 2)}
    </pre>
  );
}
