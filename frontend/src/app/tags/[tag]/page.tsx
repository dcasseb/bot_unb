import { notFound } from 'next/navigation'
import { PostCard } from '@/components/post-card'
import { getAllPosts, getAllTags } from '@/lib/content'

export function generateStaticParams() {
  return getAllTags().map((tag) => ({ tag: tag.toLowerCase() }))
}

export default function TagPage({ params }: { params: { tag: string } }) {
  const posts = getAllPosts().filter((post) => post.tags.map((tag) => tag.toLowerCase()).includes(params.tag))
  if (!posts.length) notFound()

  return (
    <section className="space-y-6">
      <h1 className="text-4xl font-semibold">Tag: #{params.tag}</h1>
      <div className="grid gap-6 md:grid-cols-2">{posts.map((post) => <PostCard key={post.slug} post={post} />)}</div>
    </section>
  )
}
