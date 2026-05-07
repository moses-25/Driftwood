import { useState, useEffect } from 'react'

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

  return { currentPath, navigate }
}