import Link from 'next/link'
import { getArchive } from '@/lib/content'

export default function ArchivePage() {
  const archive = getArchive()

  return (
    <section className="space-y-8">
      <h1 className="text-4xl font-semibold">Archive</h1>
      {Object.entries(archive).map(([month, posts]) => (
        <div key={month} className="card">
          <h2 className="mb-4 text-xl font-semibold">{month}</h2>
          <ul className="space-y-3">
            {posts.map((post) => (
              <li key={post.slug}>
                <Link href={`/blog/${post.slug}`} className="text-accent hover:underline">{post.title}</Link>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </section>
  )
}
