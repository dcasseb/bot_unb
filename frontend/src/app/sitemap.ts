import type { MetadataRoute } from 'next'
import { getAllPosts, getAllProjects } from '@/lib/content'
import { siteConfig } from '@/lib/site-config'

export default function sitemap(): MetadataRoute.Sitemap {
  const staticRoutes = ['', '/blog', '/projects', '/about', '/archive'].map((route) => ({
    url: `${siteConfig.url}${route}`,
    lastModified: new Date(),
  }))

  const postRoutes = getAllPosts().map((post) => ({
    url: `${siteConfig.url}/blog/${post.slug}`,
    lastModified: new Date(post.updated ?? post.date),
  }))

  const projectRoutes = getAllProjects().map((project) => ({
    url: `${siteConfig.url}/projects#${project.slug}`,
    lastModified: new Date(project.date),
  }))

  return [...staticRoutes, ...postRoutes, ...projectRoutes]
}
