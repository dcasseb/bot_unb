import { ProjectCard } from '@/components/project-card'
import { getAllProjects } from '@/lib/content'

export const metadata = {
  title: 'Projects',
  description: 'A living showcase of experiments, systems, and shipped work.',
}

export default function ProjectsPage() {
  const projects = getAllProjects()

  return (
    <section className="space-y-6">
      <div>
        <p className="retro-label inline-block">Build log</p>
        <h1 className="mt-4 text-4xl font-semibold">Projects</h1>
        <p className="mt-2 text-muted">Selected projects, tools, and case-study style notes.</p>
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        {projects.map((project) => <ProjectCard key={project.slug} project={project} />)}
      </div>
    </section>
  )
}
