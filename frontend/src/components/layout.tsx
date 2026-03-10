import Link from 'next/link';
import { ReactNode } from 'react';

const links = [
  ['/dashboard', 'Dashboard'],
  ['/monitoramentos', 'Monitoramentos'],
  ['/notificacoes', 'Notificações'],
  ['/configuracoes', 'Configurações'],
] as const;

export function AppLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-200 bg-white/70 p-4 backdrop-blur dark:border-slate-800 dark:bg-slate-900/70">
        <nav className="mx-auto flex max-w-6xl items-center gap-4">
          <span className="font-semibold">Monitor de Vagas UnB</span>
          {links.map(([href, label]) => (
            <Link key={href} href={href} className="text-sm text-slate-600 hover:text-slate-900 dark:text-slate-300">
              {label}
            </Link>
          ))}
        </nav>
      </header>
      <main className="mx-auto max-w-6xl p-6">{children}</main>
    </div>
  );
}
