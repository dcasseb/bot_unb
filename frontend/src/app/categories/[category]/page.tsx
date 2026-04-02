import { notFound } from 'next/navigation'
import { PostCard } from '@/components/post-card'
import { getAllCategories, getAllPosts } from '@/lib/content'

export function generateStaticParams() {
  return getAllCategories().map((category) => ({ category: category.toLowerCase() }))
}

export default function CategoryPage({ params }: { params: { category: string } }) {
  const posts = getAllPosts().filter((post) => post.category.toLowerCase() === params.category)
  if (!posts.length) notFound()

  return (
    <section className="space-y-6">
      <h1 className="text-4xl font-semibold">Category: {params.category}</h1>
      <div className="grid gap-6 md:grid-cols-2">{posts.map((post) => <PostCard key={post.slug} post={post} />)}</div>
    </section>
  )
}
