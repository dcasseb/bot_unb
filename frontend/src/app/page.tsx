import Link from 'next/link'
import { getAllPosts, getAllProjects } from '@/lib/content'
import { siteConfig } from '@/lib/site-config'
import { PostCard } from '@/components/post-card'
import { ProjectCard } from '@/components/project-card'

export default function HomePage() {
  const posts = getAllPosts().slice(0, 6)
  const featuredPosts = posts.filter((post) => post.featured).slice(0, 2)
  const featuredProjects = getAllProjects().filter((project) => project.featured).slice(0, 2)

  return (
    <div className="space-y-16">
      <section className="card relative overflow-hidden p-10">
        <div className="absolute right-0 top-0 h-32 w-32 rounded-bl-full bg-accent/20" />
        <p className="retro-label inline-block">Personal Blog</p>
        <h1 className="mt-4 max-w-3xl text-5xl font-semibold tracking-tight">{siteConfig.name}</h1>
        <p className="mt-4 max-w-2xl text-lg text-muted">{siteConfig.description}</p>
        <p className="mt-3 font-mono text-sm text-accent">{siteConfig.tagline}</p>
        <div className="mt-8 flex gap-3">
          <Link href="/blog" className="rounded-lg bg-accent px-5 py-2.5 text-sm font-medium text-white">
            Read the blog
          </Link>
          <Link href="/projects" className="rounded-lg border border-border px-5 py-2.5 text-sm font-medium">
            Explore projects
          </Link>
        </div>
      </section>

      <section>
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-2xl font-semibold">Featured Posts</h2>
          <Link href="/blog" className="text-sm text-accent">View all</Link>
        </div>
        <div className="grid gap-6 md:grid-cols-2">
          {featuredPosts.map((post) => <PostCard key={post.slug} post={post} />)}
        </div>
      </section>

      <section>
        <h2 className="mb-6 text-2xl font-semibold">Recent Notes & Essays</h2>
        <div className="grid gap-6 md:grid-cols-2">
          {posts.map((post) => <PostCard key={post.slug} post={post} />)}
        </div>
      </section>

      <section>
        <h2 className="mb-6 text-2xl font-semibold">Featured Projects</h2>
        <div className="grid gap-6 md:grid-cols-2">
          {featuredProjects.map((project) => <ProjectCard key={project.slug} project={project} />)}
        </div>
      </section>
    </div>
  )
}
