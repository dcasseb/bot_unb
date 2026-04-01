import Image from 'next/image'
import { siteConfig } from '@/lib/site-config'

export default function AboutPage() {
  return (
    <section className="grid gap-10 md:grid-cols-[220px_1fr]">
      <Image
        src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&q=80"
        alt="Profile"
        width={220}
        height={220}
        className="rounded-2xl border border-border object-cover"
      />
      <div className="space-y-4">
        <p className="retro-label inline-block">About</p>
        <h1 className="text-4xl font-semibold">Hi, I’m {siteConfig.author}</h1>
        <p className="text-muted">
          I write about software design, digital craft, and the systems behind meaningful products. This site is my
          open notebook—essays, learning notes, and project retrospectives.
        </p>
        <h2 className="text-xl font-semibold">Interests</h2>
        <p className="text-muted">Developer experience, thoughtful interface design, resilient systems, and writing.</p>
        <h2 className="text-xl font-semibold">Skills</h2>
        <p className="text-muted">TypeScript, Next.js, Python, product strategy, technical writing, and design systems.</p>
        <div className="flex gap-4 text-accent">
          <a href={siteConfig.social.github}>GitHub</a>
          <a href={siteConfig.social.linkedin}>LinkedIn</a>
          <a href={siteConfig.social.x}>X</a>
        </div>
      </div>
    </section>
  )
}
