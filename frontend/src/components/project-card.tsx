import type { Project } from '@/lib/content'

export function ProjectCard({ project }: { project: Project }) {
  return (
    <article className="card">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-xl font-semibold">{project.title}</h3>
        <span className="retro-label">{project.status}</span>
      </div>
      <p className="text-muted">{project.description}</p>
      <div className="mt-4 flex flex-wrap gap-2">
        {project.technologies.map((tech) => (
          <span key={tech} className="retro-label">{tech}</span>
        ))}
      </div>
      {project.links && project.links.length > 0 && (
        <div className="mt-5 flex gap-4 text-sm text-accent">
          {project.links.map((link) => (
            <a key={link.url} href={link.url} target="_blank" rel="noreferrer">
              {link.label}
            </a>
          ))}
        </div>
      )}
    </article>
  )
}
