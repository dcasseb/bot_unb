import { BlogExplorer } from '@/components/blog-explorer'
import { getAllCategories, getAllPosts, getAllTags } from '@/lib/content'

export const metadata = {
  title: 'Blog',
  description: 'Essays, notes, and reflections.',
}

export default function BlogPage() {
  const posts = getAllPosts()
  const tags = getAllTags()
  const categories = getAllCategories()

  return (
    <section className="space-y-6">
      <div>
        <p className="retro-label inline-block">Open access writing</p>
        <h1 className="mt-4 text-4xl font-semibold">Blog</h1>
        <p className="mt-2 text-muted">All essays and notes are free to read—no login, no paywall.</p>
      </div>
      <BlogExplorer posts={posts} tags={tags} categories={categories} />
    </section>
  )
}
