import { useState, useEffect } from 'react'

// Hashes that render a full-page view (not a section on the main page)
const FULL_PAGE_HASHES = new Set(['#cart', '#checkout'])

export const useRouter = () => {
  const [currentPath, setCurrentPath] = useState(window.location.hash || '#home')

  useEffect(() => {
    const handleHashChange = () => {
      setCurrentPath(window.location.hash || '#home')
    }
    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [])

  const navigate = (path) => {
    window.location.hash = path
    setCurrentPath(path)
  }

  return { currentPath, navigate, isFullPage: FULL_PAGE_HASHES.has(currentPath) }
}
