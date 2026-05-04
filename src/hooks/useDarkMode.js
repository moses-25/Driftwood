import { useState, useEffect } from 'react'

export default function useDarkMode() {
  const [darkMode, setDarkMode] = useState(false)

  useEffect(() => {
    const root = document.documentElement
    if (darkMode) {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
  }, [darkMode])

  return [darkMode, setDarkMode]
}