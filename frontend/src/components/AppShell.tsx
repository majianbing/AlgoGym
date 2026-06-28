import {
  BarChart3,
  BookOpen,
  CalendarDays,
  Dumbbell,
  FileUp,
  RotateCcw,
  Settings,
} from "lucide-react";
import Link from "next/link";
import type { ReactNode } from "react";

const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: BarChart3 },
  { label: "Knowledge Base", href: "/knowledge-base", icon: FileUp },
  { label: "Plan", href: "/plan", icon: CalendarDays },
  { label: "Session", href: "/session", icon: Dumbbell },
  { label: "Review", href: "/review", icon: RotateCcw },
  { label: "Settings", href: "/settings", icon: Settings },
];

type AppShellProps = {
  eyebrow: string;
  title: string;
  children: ReactNode;
};

export function AppShell({ eyebrow, title, children }: AppShellProps) {
  return (
    <main className="min-h-screen bg-ink text-slate-100">
      <div className="grid min-h-screen grid-cols-1 lg:grid-cols-[260px_1fr]">
        <aside className="border-b border-line bg-panel/80 p-5 lg:border-b-0 lg:border-r">
          <Link href="/dashboard" className="mb-8 flex items-center gap-3 text-xl font-bold">
            <BookOpen className="text-mint" size={26} />
            AlgoGym
          </Link>
          <nav className="grid grid-cols-2 gap-2 lg:grid-cols-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  href={item.href}
                  className="flex items-center gap-2 rounded-md px-3 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white"
                  key={item.href}
                >
                  <Icon size={18} />
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </aside>
        <section className="p-5 lg:p-8">
          <header className="mb-8">
            <p className="mb-2 text-xs font-bold uppercase tracking-wide text-mint">{eyebrow}</p>
            <h1 className="max-w-4xl text-3xl font-bold leading-tight text-white lg:text-4xl">
              {title}
            </h1>
          </header>
          {children}
        </section>
      </div>
    </main>
  );
}
