import Link from 'next/link'
import { notFound } from 'next/navigation'
import { getAllPosts, getPostBySlug } from '@/lib/content'
import { renderMDX, extractHeadings } from '@/lib/mdx'
import { TableOfContents } from '@/components/toc'

export async function generateStaticParams() {
  return getAllPosts(true).map((post) => ({ slug: post.slug }))
}

export async function generateMetadata({ params }: { params: { slug: string } }) {
  const post = getPostBySlug(params.slug)
  if (!post || post.draft) return {}
  return { title: post.title, description: post.excerpt }
}

export default async function PostPage({ params }: { params: { slug: string } }) {
  const post = getPostBySlug(params.slug)
  if (!post || post.draft) notFound()

  const content = await renderMDX(post.content)
  const headings = extractHeadings(post.content)

  const posts = getAllPosts()
  const index = posts.findIndex((p) => p.slug === post.slug)
  const previous = posts[index + 1]
  const next = posts[index - 1]
  const related = posts.filter((p) => p.slug !== post.slug && p.tags.some((tag) => post.tags.includes(tag))).slice(0, 3)

  return (
    <div className="grid gap-10 lg:grid-cols-[1fr_280px]">
      <article className="space-y-8">
        <header className="card">
          <p className="retro-label inline-block">{post.category}</p>
          <h1 className="mt-4 text-4xl font-semibold leading-tight">{post.title}</h1>
          <p className="mt-3 text-muted">{post.excerpt}</p>
          <div className="mt-4 flex flex-wrap gap-3 text-sm text-muted">
            <span>Published {new Date(post.date).toLocaleDateString()}</span>
            {post.updated && <span>Updated {new Date(post.updated).toLocaleDateString()}</span>}
            <span>{post.readingTime}</span>
          </div>
        </header>

        <div className="prose prose-neutral max-w-none rounded-xl border border-border/70 bg-bg/80 p-8 dark:prose-invert">
          {content}
        </div>

        <section className="card">
          <p className="mb-3 text-sm font-semibold">Share</p>
          <div className="flex flex-wrap gap-4 text-sm text-accent">
            <a href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(post.title)}`}>Share on X</a>
            <a href={`https://www.linkedin.com/sharing/share-offsite/?url=/blog/${post.slug}`}>Share on LinkedIn</a>
          </div>
        </section>

        <nav className="grid gap-4 md:grid-cols-2">
          {previous ? <Link href={`/blog/${previous.slug}`} className="card">← {previous.title}</Link> : <div />}
          {next ? <Link href={`/blog/${next.slug}`} className="card text-right">{next.title} →</Link> : <div />}
        </nav>

        {related.length > 0 && (
          <section>
            <h2 className="mb-4 text-2xl font-semibold">Related posts</h2>
            <div className="grid gap-4 md:grid-cols-3">
              {related.map((item) => (
                <Link key={item.slug} href={`/blog/${item.slug}`} className="card">
                  <h3 className="font-medium">{item.title}</h3>
                  <p className="mt-2 text-sm text-muted">{item.excerpt}</p>
                </Link>
              ))}
            </div>
          </section>
        )}
      </article>

      <TableOfContents headings={headings} />
    </div>
  )
}
