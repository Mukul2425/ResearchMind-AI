import Link from "next/link";

const nav = [
  { href: "/", label: "Dashboard" },
  { href: "/upload", label: "Upload" },
  { href: "/library", label: "Library" },
  { href: "/chat", label: "Chat" },
  { href: "/compare", label: "Compare" },
];

export function Sidebar() {
  return (
    <aside className="rounded-xl2 border border-ink/10 bg-canvas/85 p-5 shadow-panel backdrop-blur">
      <p className="mb-5 text-xs font-semibold uppercase tracking-[0.2em] text-moss">ResearchMind AI</p>
      <nav className="space-y-2">
        {nav.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="block rounded-lg px-3 py-2 text-sm font-medium text-ink transition hover:bg-moss hover:text-canvas"
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
