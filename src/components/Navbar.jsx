import { useState, useEffect } from 'react'
import { useCart } from '../hooks/useCart'

const navLinks = [
  { label: 'Home', href: '#home' },
  { label: 'About', href: '#about' },
  { label: 'Menu', href: '#menu' },
  { label: 'Gallery', href: '#gallery' },
  { label: 'Reviews', href: '#reviews' },
  { label: 'Visit Us', href: '#visit' },
]

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)
  const { totalItems } = useCart()

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const handleNavClick = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <nav className={`fixed top-0 left-0 w-full z-50 transition-all duration-300 backdrop-blur-xl border-b border-white/10 ${
      scrolled ? 'bg-slate-900/80 shadow-md' : 'bg-slate-900/20'
    }`}>
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

        {/* Logo */}
        <a href="#home" onClick={handleNavClick} className="flex items-center gap-3">
          <img src="/Driftwood.png" alt="Driftwood Café" className="h-27 w-auto" />
          <span className="text-xl font-bold text-white">
            <span className="text-primary">Driftwood</span>
            <span className="text-white font-bold text-lg"> Café</span>
          </span>
        </a>

        {/* Desktop Nav Links */}
        <ul className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => (
            <li key={link.label}>
              <a
                href={link.href}
                onClick={handleNavClick}
                className="text-base font-bold text-white hover:text-primary transition-colors"
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>

        {/* Right Side */}
        <div className="flex items-center gap-3">
          <a
            href="#cart"
            className="hidden md:inline-flex items-center gap-3 bg-white/10 text-white text-sm px-4 py-2.5 rounded-full hover:bg-white/20 transition-all duration-200 shadow-sm border border-white/10 font-bold relative"
            aria-label="Add to cart"
          >
            <span className="inline-flex h-9 w-9 items-center justify-center rounded-full bg-white/10 text-amber-300 ring-1 ring-white/15">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4">
                <path d="M6 6h15l-1.5 9h-13z" />
                <path d="M6 6l-2 0" />
                <circle cx="9" cy="20" r="1" />
                <circle cx="18" cy="20" r="1" />
              </svg>
            </span>
            Cart {totalItems > 0 && `(${totalItems})`}
            {totalItems > 0 && (
              <span className="absolute -top-2 -right-2 bg-amber-500 text-slate-900 text-xs font-bold rounded-full h-6 w-6 flex items-center justify-center">
                {totalItems}
              </span>
            )}
          </a>
          <a
            href="#search"
            className="hidden md:inline-flex items-center gap-3 bg-white/10 text-white text-sm px-4 py-2.5 rounded-full hover:bg-white/20 transition-all duration-200 shadow-sm border border-white/10 font-bold"
            aria-label="Search"
          >
            <span className="inline-flex h-9 w-9 items-center justify-center rounded-full bg-white/10 text-slate-100 ring-1 ring-white/15">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4">
                <circle cx="11" cy="11" r="7" />
                <path d="M21 21l-4.35-4.35" />
              </svg>
            </span>
            Search
          </a>
          <a
            href="#visit"
            className="hidden md:inline-flex items-center justify-center bg-primary text-white text-sm px-6 py-2.5 rounded-full hover:bg-orange-700 transition-all duration-200 font-bold shadow-lg"
            aria-label="Reserve a table"
          >
            Reserve a Table
          </a>

          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="md:hidden flex h-11 w-11 items-center justify-center rounded-full border border-white/15 bg-white/10 p-2 transition-all duration-200 hover:bg-white/20"
            aria-label="Toggle menu"
          >
            <span
              className={`block w-6 h-0.5 rounded-full bg-white transition-all duration-300 ${
                menuOpen ? 'rotate-45 translate-y-1.5' : ''
              }`}
            />
            <span
              className={`block w-6 h-0.5 rounded-full bg-white transition-all duration-300 ${
                menuOpen ? 'opacity-0' : ''
              }`}
            />
            <span
              className={`block w-6 h-0.5 rounded-full bg-white transition-all duration-300 ${
                menuOpen ? '-rotate-45 -translate-y-1.5' : ''
              }`}
            />
          </button>
        </div>
      </div>

      {menuOpen && (
        <div className="md:hidden bg-slate-900 px-6 pb-6 shadow-lg">
          <ul className="flex flex-col gap-4">
            {navLinks.map((link) => (
              <li key={link.label}>
                <a
                  href={link.href}
                  onClick={() => {
                    setMenuOpen(false)
                    handleNavClick()
                  }}
                  className="block text-base font-bold text-white hover:text-primary transition-colors"
                >
                  {link.label}
                </a>
              </li>
            ))}
            <li>
              <a
                href="#visit"
                className="block text-center bg-primary text-white px-5 py-2.5 rounded-lg hover:bg-orange-700 transition-colors font-medium"
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
