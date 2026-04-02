import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import readingTime from 'reading-time'

const postsDirectory = path.join(process.cwd(), 'src/content/posts')
const projectsDirectory = path.join(process.cwd(), 'src/content/projects')

export type Post = {
  slug: string
  title: string
  excerpt: string
  date: string
  updated?: string
  tags: string[]
  category: string
  coverImage?: string
  draft?: boolean
  featured?: boolean
  relatedProject?: string
  content: string
  readingTime: string
}

export type Project = {
  slug: string
  title: string
  description: string
  technologies: string[]
  status: 'Active' | 'Completed' | 'Paused'
  links?: { label: string; url: string }[]
  screenshot?: string
  featured?: boolean
  date: string
  content: string
}

const readMarkdown = (directory: string) =>
  fs.readdirSync(directory).filter((file) => file.endsWith('.mdx'))

const readFile = (directory: string, file: string) => {
  const fullPath = path.join(directory, file)
  const source = fs.readFileSync(fullPath, 'utf8')
  const { data, content } = matter(source)
  const slug = file.replace(/\.mdx$/, '')
  return { data, content, slug }
}

export const getAllPosts = (includeDrafts = false): Post[] => {
  return readMarkdown(postsDirectory)
    .map((file) => {
      const { data, content, slug } = readFile(postsDirectory, file)
      return {
        slug,
        title: data.title,
        excerpt: data.excerpt,
        date: data.date,
        updated: data.updated,
        tags: data.tags ?? [],
        category: data.category ?? 'General',
        coverImage: data.coverImage,
        draft: data.draft ?? false,
        featured: data.featured ?? false,
        relatedProject: data.relatedProject,
        content,
        readingTime: readingTime(content).text,
      } as Post
    })
    .filter((post) => (includeDrafts ? true : !post.draft))
    .sort((a, b) => +new Date(b.date) - +new Date(a.date))
}

export const getPostBySlug = (slug: string) => getAllPosts(true).find((post) => post.slug === slug)

export const getAllProjects = (): Project[] => {
  return readMarkdown(projectsDirectory)
    .map((file) => {
      const { data, content, slug } = readFile(projectsDirectory, file)
      return {
        slug,
        title: data.title,
        description: data.description,
        technologies: data.technologies ?? [],
        status: data.status ?? 'Active',
        links: data.links ?? [],
        screenshot: data.screenshot,
        featured: data.featured ?? false,
        date: data.date,
        content,
      } as Project
    })
    .sort((a, b) => +new Date(b.date) - +new Date(a.date))
}

export const getProjectBySlug = (slug: string) => getAllProjects().find((project) => project.slug === slug)

export const getAllTags = () => [...new Set(getAllPosts().flatMap((post) => post.tags))].sort()

export const getAllCategories = () => [...new Set(getAllPosts().map((post) => post.category))].sort()

export const getArchive = () => {
  return getAllPosts().reduce<Record<string, Post[]>>((acc, post) => {
    const key = new Date(post.date).toLocaleString('en-US', { month: 'long', year: 'numeric' })
    acc[key] = [...(acc[key] ?? []), post]
    return acc
  }, {})
}
