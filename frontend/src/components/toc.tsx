export function TableOfContents({ headings }: { headings: { title: string; slug: string }[] }) {
  if (!headings.length) return null

  return (
    <aside className="card sticky top-24 hidden h-fit lg:block">
      <p className="mb-3 text-sm font-semibold">On this page</p>
      <ul className="space-y-2 text-sm text-muted">
        {headings.map((heading) => (
          <li key={heading.slug}>
            <a href={`#${heading.slug}`} className="hover:text-accent">{heading.title}</a>
          </li>
        ))}
      </ul>
    </aside>
  )
}
