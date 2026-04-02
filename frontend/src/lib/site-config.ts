export const siteConfig = {
  name: 'Signal & Grain',
  description:
    'Thoughts, essays, and project notes from a creative technologist exploring software, writing, and systems.',
  url: process.env.NEXT_PUBLIC_SITE_URL ?? 'https://example.com',
  author: 'Your Name',
  tagline: 'Modern craft, retro soul.',
  environment: process.env.NEXT_PUBLIC_ENVIRONMENT ?? 'personal-blog',
  social: {
    github: 'https://github.com/yourhandle',
    x: 'https://x.com/yourhandle',
    linkedin: 'https://linkedin.com/in/yourhandle',
  },
}
