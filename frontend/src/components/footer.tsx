import Link from 'next/link'
import { siteConfig } from '@/lib/site-config'

export function Footer() {
  return (
    <footer className="mt-20 border-t border-border/70">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-6 py-8 text-sm text-muted md:flex-row md:justify-between">
        <p>© {new Date().getFullYear()} {siteConfig.author}. Built with Next.js + MDX.</p>
        <div className="flex gap-4">
          <Link href={siteConfig.social.github}>GitHub</Link>
          <Link href={siteConfig.social.x}>X</Link>
          <Link href={siteConfig.social.linkedin}>LinkedIn</Link>
          <Link href="/rss.xml">RSS</Link>
        </div>
      </div>
    </footer>
  )
}
