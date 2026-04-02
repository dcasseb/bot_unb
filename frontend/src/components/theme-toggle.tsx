'use client'

import { Moon, Sun } from 'lucide-react'
import { useTheme } from 'next-themes'

export function ThemeToggle() {
  const { setTheme, resolvedTheme } = useTheme()
  const isDark = resolvedTheme === 'dark'

  return (
    <button
      type="button"
      onClick={() => setTheme(isDark ? 'light' : 'dark')}
      className="retro-label transition hover:border-accent hover:text-accent"
      aria-label="Toggle theme"
    >
      {isDark ? <Sun className="inline size-3" /> : <Moon className="inline size-3" />}
    </button>
  )
}
