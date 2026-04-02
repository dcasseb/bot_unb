# Signal & Grain — Personal Blog (Next.js + MDX)

A production-ready, open-access personal blog designed with a modern-retro visual language.

## Repository

- GitHub: https://github.com/dcasseb/personal-blog.git

## Environment target

- Target environment: `personal-blog`
- Copy `.env.example` to `.env.local` and keep `NEXT_PUBLIC_ENVIRONMENT=personal-blog`.

## Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS + Typography
- MDX content files with frontmatter (`gray-matter`)
- Static generation for posts/projects

## Project Architecture

- `src/app/*`: Route pages (home, blog, post, projects, about, archive, tag/category pages)
- `src/components/*`: Reusable UI primitives and page components
- `src/lib/content.ts`: Content model, frontmatter parsing, tag/category/archive helpers
- `src/lib/mdx.tsx`: MDX compilation and heading extraction
- `src/content/posts/*.mdx`: Blog posts
- `src/content/projects/*.mdx`: Projects
- `src/app/rss.xml/route.ts`: RSS feed endpoint
- `src/app/sitemap.ts` and `src/app/robots.ts`: SEO essentials

## Content Model

### Post frontmatter

```yaml
title: string
date: YYYY-MM-DD
updated: YYYY-MM-DD (optional)
tags: [string]
category: string
excerpt: string
coverImage: string (optional)
draft: boolean
featured: boolean
relatedProject: string (optional)
```

### Project frontmatter

```yaml
title: string
description: string
technologies: [string]
status: Active | Completed | Paused
date: YYYY-MM-DD
featured: boolean
links:
  - label: string
    url: string
```

## Writing Workflow

1. Create a new `.mdx` file inside `src/content/posts`.
2. Add frontmatter fields.
3. Write content using Markdown/MDX.
4. Set `draft: true` to keep unpublished locally.
5. Build and deploy.

## Local Development

```bash
cp .env.example .env.local
npm install
npm run dev
```

## Build & Quality Checks

```bash
npm run lint
npm run build
```

## Deployment

### Vercel (recommended)

1. Push repository to GitHub.
2. Import project in Vercel.
3. Set root directory to `frontend`.
4. Build command: `npm run build`
5. Output: `.next`

### Netlify

1. Connect repository.
2. Base directory: `frontend`
3. Build command: `npm run build`
4. Publish directory: `.next`
5. Use Netlify Next.js runtime.

## Branding Assets

Place favicon, OG image, and custom artwork in:

- `public/favicon.ico`
- `public/branding/*`

