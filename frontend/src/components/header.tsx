import Link from 'next/link'
import { ThemeToggle } from './theme-toggle'

const navItems = [
  { href: '/', label: 'Home' },
  { href: '/blog', label: 'Blog' },
  { href: '/projects', label: 'Projects' },
  { href: '/about', label: 'About' },
  { href: '/archive', label: 'Archive' },
]

export function Header() {
  return (
    <header className="sticky top-0 z-40 border-b border-border/70 bg-bg/90 backdrop-blur">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/" className="font-mono text-sm uppercase tracking-[0.2em] text-accent">
          Signal & Grain
        </Link>
        <nav className="flex items-center gap-5 text-sm">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href} className="text-muted transition hover:text-fg">
              {item.label}
            </Link>
          ))}
          <ThemeToggle />
        </nav>
      </div>
    </header>
  )
}
