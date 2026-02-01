import { ReactNode } from "react";

export function GlassCard({
  title,
  subtitle,
  children,
  className,
}: {
  title?: string;
  subtitle?: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section
      className={
        "rounded-2xl border border-white/15 bg-white/10 p-6 shadow-[0_20px_80px_-40px_rgba(0,0,0,0.8)] backdrop-blur-xl " +
        (className ?? "")
      }
    >
      {(title || subtitle) && (
        <header className="mb-4">
          {title && <h2 className="text-lg font-semibold text-white">{title}</h2>}
          {subtitle && <p className="mt-1 text-sm text-white/70">{subtitle}</p>}
        </header>
      )}
      {children}
    </section>
  );
}
