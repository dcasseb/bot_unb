import Link from 'next/link'
import type { Post } from '@/lib/content'

export function PostCard({ post }: { post: Post }) {
  return (
    <article className="card transition hover:-translate-y-0.5 hover:shadow-glow">
      <div className="mb-4 flex items-center gap-3 text-xs text-muted">
        <span>{new Date(post.date).toLocaleDateString()}</span>
        <span>•</span>
        <span>{post.readingTime}</span>
        <span className="retro-label">{post.category}</span>
      </div>
      <h3 className="text-2xl font-semibold leading-tight">
        <Link href={`/blog/${post.slug}`} className="hover:text-accent">
          {post.title}
        </Link>
      </h3>
      <p className="mt-3 text-muted">{post.excerpt}</p>
      <div className="mt-4 flex flex-wrap gap-2">
        {post.tags.map((tag) => (
          <Link key={tag} href={`/tags/${tag.toLowerCase()}`} className="retro-label hover:border-accent hover:text-accent">
            #{tag}
          </Link>
        ))}
      </div>
    </article>
  )
}
