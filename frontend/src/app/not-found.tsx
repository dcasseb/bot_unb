import Link from 'next/link'

export default function NotFound() {
  return (
    <section className="card mx-auto mt-20 max-w-2xl text-center">
      <p className="retro-label inline-block">404</p>
      <h1 className="mt-4 text-4xl font-semibold">Signal lost.</h1>
      <p className="mt-3 text-muted">The page drifted into the static. Let’s get you back on track.</p>
      <Link href="/" className="mt-6 inline-block rounded-lg bg-accent px-5 py-2 text-white">Back home</Link>
    </section>
  )
}
