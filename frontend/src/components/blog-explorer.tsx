'use client'

import { useMemo, useState } from 'react'
import type { Post } from '@/lib/content'
import { PostCard } from './post-card'

type Props = {
  posts: Post[]
  tags: string[]
  categories: string[]
}

export function BlogExplorer({ posts, tags, categories }: Props) {
  const [query, setQuery] = useState('')
  const [activeTag, setActiveTag] = useState('all')
  const [activeCategory, setActiveCategory] = useState('all')

  const filteredPosts = useMemo(() => {
    return posts.filter((post) => {
      const byQuery = [post.title, post.excerpt, ...post.tags].join(' ').toLowerCase().includes(query.toLowerCase())
      const byTag = activeTag === 'all' || post.tags.map((tag) => tag.toLowerCase()).includes(activeTag)
      const byCategory = activeCategory === 'all' || post.category.toLowerCase() === activeCategory
      return byQuery && byTag && byCategory
    })
  }, [posts, query, activeTag, activeCategory])

  return (
    <div className="space-y-8">
      <div className="card grid gap-4 md:grid-cols-3">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search posts, tags, ideas..."
          className="rounded-lg border border-border bg-transparent px-4 py-2 text-sm md:col-span-2"
        />
        <div className="grid grid-cols-2 gap-3">
          <select className="rounded-lg border border-border bg-transparent px-2" onChange={(e) => setActiveCategory(e.target.value)}>
            <option value="all">All categories</option>
            {categories.map((category) => (
              <option key={category} value={category.toLowerCase()}>{category}</option>
            ))}
          </select>
          <select className="rounded-lg border border-border bg-transparent px-2" onChange={(e) => setActiveTag(e.target.value)}>
            <option value="all">All tags</option>
            {tags.map((tag) => (
              <option key={tag} value={tag.toLowerCase()}>{tag}</option>
            ))}
          </select>
        </div>
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        {filteredPosts.map((post) => <PostCard key={post.slug} post={post} />)}
      </div>
      {filteredPosts.length === 0 && <p className="text-muted">No posts match your search yet.</p>}
    </div>
  )
}
