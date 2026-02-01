import Link from "next/link";

const links: Array<{ href: string; label: string }> = [
  { href: "/", label: "Overview" },
  { href: "/decision", label: "Decision" },
  { href: "/scenarios", label: "Scenarios" },
  { href: "/referrals", label: "Referrals" },
  { href: "/analytics", label: "Analytics" },
];

export function Nav() {
  return (
    <div className="sticky top-0 z-20 border-b border-white/10 bg-black/20 backdrop-blur-xl">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-xl bg-gradient-to-br from-indigo-400/90 via-fuchsia-400/70 to-cyan-300/70 shadow-lg" />
          <div>
            <div className="text-sm font-semibold tracking-wide text-white">Procuator</div>
            <div className="text-xs text-white/60">Procurement decisioning demo</div>
          </div>
        </div>

        <nav className="hidden items-center gap-2 md:flex">
          {links.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className="rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-sm text-white/80 hover:bg-white/10 hover:text-white"
            >
              {l.label}
            </Link>
          ))}
        </nav>

        <div className="text-xs text-white/60">
          <span className="hidden sm:inline">Backend: </span>
          <code className="rounded-lg border border-white/10 bg-white/5 px-2 py-1">API_BASE_URL</code>
        </div>
      </div>
    </div>
  );
}
