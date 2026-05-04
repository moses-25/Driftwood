import { useState, useEffect } from 'react'
import useDarkMode from '../hooks/useDarkMode'

const navLinks = [
  { label: 'Home', href: '#home' },
  { label: 'About', href: '#about' },
  { label: 'Menu', href: '#menu' },
  { label: 'Gallery', href: '#gallery' },
  { label: 'Reviews', href: '#reviews' },
  { label: 'Visit Us', href: '#visit' },
]

export default function Navbar() {
  const [darkMode, setDarkMode] = useDarkMode()
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)

  // Detect scroll to add solid background
  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <nav className={`fixed top-0 left-0 w-full z-50 transition-all duration-300
      ${scrolled
        ? 'bg-white dark:bg-dark shadow-md'
        : 'bg-transparent'}
    `}>
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

        {/* Logo */}
        <a href="#home" className="flex items-center gap-3">
          <img src="/Driftwood.png" alt="Driftwood Café" className="h-27 w-auto" />
          <span className="text-xl font-bold">
            <span className="text-primary">Driftwood</span>
            <span className="text-gray-900 dark:text-white"> Café</span>
          </span>
        </a>

        {/* Desktop Nav Links */}
        <ul className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => (
            <li key={link.label}>
              <a
                href={link.href}
                className="text-sm font-bold text-gray-700 dark:text-gray-300
                  hover:text-primary dark:hover:text-primary transition-colors"
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>

        {/* Right Side */}
        <div className="flex items-center gap-4">
          {/* Dark Mode Toggle */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="text-gray-700 dark:text-gray-300 hover:text-primary
              dark:hover:text-primary transition-colors text-lg"
            aria-label="Toggle dark mode"
          >
            {darkMode ? '☀️' : '🌙'}
          </button>

          {/* CTA Button - hidden on mobile */}
          <a
            href="#visit"
            className="hidden md:inline-block bg-primary text-white
              text-sm px-5 py-2.5 rounded-lg hover:bg-orange-700
              transition-colors font-medium"
          >
            Reserve a Table
          </a>

          {/* Mobile Hamburger */}
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="md:hidden flex flex-col gap-1.5 p-1"
            aria-label="Toggle menu"
          >
            <span className={`block w-6 h-0.5 bg-gray-700 dark:bg-gray-300
              transition-all duration-300
              ${menuOpen ? 'rotate-45 translate-y-2' : ''}`}
            />
            <span className={`block w-6 h-0.5 bg-gray-700 dark:bg-gray-300
              transition-all duration-300
              ${menuOpen ? 'opacity-0' : ''}`}
            />
            <span className={`block w-6 h-0.5 bg-gray-700 dark:bg-gray-300
              transition-all duration-300
              ${menuOpen ? '-rotate-45 -translate-y-2' : ''}`}
            />
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {menuOpen && (
        <div className="md:hidden bg-white dark:bg-dark px-6 pb-6 shadow-lg">
          <ul className="flex flex-col gap-4">
            {navLinks.map((link) => (
              <li key={link.label}>
                <a
                  href={link.href}
                  onClick={() => setMenuOpen(false)}
                  className="block text-gray-700 dark:text-gray-300
                    hover:text-primary dark:hover:text-primary
                    transition-colors"
                >
                  {link.label}
                </a>
              </li>
            ))}
            <li>
              <a
                href="#visit"
                className="block text-center bg-primary text-white
                  px-5 py-2.5 rounded-lg hover:bg-orange-700
                  transition-colors font-medium"
              >
                Reserve a Table
              </a>
            </li>
          </ul>
        </div>
      )}
    </nav>
  )
}