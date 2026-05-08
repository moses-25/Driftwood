import { useState, useEffect, useCallback } from 'react'
import { useCart } from '../hooks/useCart'
import { useRouter } from '../hooks/useRouter'
import SearchModal from './SearchModal'

const navLinks = [
  { label: 'Home',     href: '#home' },
  { label: 'About',    href: '#about' },
  { label: 'Menu',     href: '#menu' },
  { label: 'Gallery',  href: '#gallery' },
  { label: 'Reviews',  href: '#reviews' },
  { label: 'Visit Us', href: '#visit' },
]

// Section IDs that live on the main page (not full-page routes)
const SECTION_IDS = new Set(['home', 'about', 'menu', 'gallery', 'reviews', 'visit'])

export default function Navbar({ pendingScroll }) {
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)
  const [searchOpen, setSearchOpen] = useState(false)
  const { totalItems } = useCart()
  const { currentPath, navigate, isFullPage } = useRouter()

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const closeMenu = useCallback(() => setMenuOpen(false), [])

  useEffect(() => {
    if (!menuOpen) return
    const handler = (e) => { if (!e.target.closest('nav')) closeMenu() }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [menuOpen, closeMenu])

  /**
   * Handle a nav link click.
   * - If we're already on the main page: let the browser follow the hash
   *   (Lenis smooth-scroll handles the rest).
   * - If we're on a full-page view (cart/checkout): store the target section
   *   in pendingScroll, then navigate to #home so App unmounts the full-page
   *   view and mounts the main page. App's useEffect will scroll after mount.
   */
  const handleNavClick = useCallback((e, href) => {
    const sectionId = href.replace('#', '')

    if (isFullPage && SECTION_IDS.has(sectionId)) {
      e.preventDefault()
      closeMenu()
      if (pendingScroll) pendingScroll.current = sectionId
      // Navigate to #home to trigger main-page render; App will scroll after mount
      navigate('#home')
    } else {
      closeMenu()
    }
  }, [isFullPage, navigate, closeMenu, pendingScroll])

  return (
    <nav className={`fixed top-0 left-0 w-full z-50 transition-all duration-300 backdrop-blur-xl border-b border-white/10 ${
      scrolled ? 'bg-slate-900/80 shadow-md' : 'bg-slate-900/20'
    }`}>
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

        {/* Logo */}
        <a
          href="#home"
          onClick={(e) => handleNavClick(e, '#home')}
          className="flex items-center gap-3"
        >
          <img src="/Driftwood.png" alt="Driftwood Café" className="h-10 w-auto" />
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
                onClick={(e) => handleNavClick(e, link.href)}
                className="text-base font-bold text-white hover:text-primary transition-colors"
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>

        {/* Right Side */}
        <div className="flex items-center gap-3">
          {/* Cart */}
          <a
            href="#cart"
            className="hidden md:inline-flex items-center gap-3 bg-white/10 text-white text-sm px-4 py-2.5 rounded-full hover:bg-white/20 transition-all duration-200 shadow-sm border border-white/10 font-bold relative"
            aria-label={`Cart${totalItems > 0 ? `, ${totalItems} items` : ''}`}
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
              <span className="absolute -top-2 -right-2 bg-amber-500 text-slate-900 text-xs font-bold rounded-full h-6 w-6 flex items-center justify-center" aria-hidden="true">
                {totalItems}
              </span>
            )}
          </a>

          {/* Search */}
          <button
            onClick={() => setSearchOpen(true)}
            className="hidden md:inline-flex items-center gap-3 bg-white/10 text-white text-sm px-4 py-2.5 rounded-full hover:bg-white/20 transition-all duration-200 shadow-sm border border-white/10 font-bold cursor-pointer"
            aria-label="Open search"
          >
            <span className="inline-flex h-9 w-9 items-center justify-center rounded-full bg-white/10 text-slate-100 ring-1 ring-white/15">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4">
                <circle cx="11" cy="11" r="7" />
                <path d="M21 21l-4.35-4.35" />
              </svg>
            </span>
            Search
          </button>

          {/* Reserve */}
          <a
            href="#visit"
            onClick={(e) => handleNavClick(e, '#visit')}
            className="hidden md:inline-flex items-center justify-center bg-primary text-white text-sm px-6 py-2.5 rounded-full hover:bg-orange-700 transition-all duration-200 font-bold shadow-lg"
          >
            Reserve a Table
          </a>

          {/* Hamburger */}
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="md:hidden flex h-11 w-11 items-center justify-center rounded-full border border-white/15 bg-white/10 p-2 transition-all duration-200 hover:bg-white/20"
            aria-label={menuOpen ? 'Close menu' : 'Open menu'}
            aria-expanded={menuOpen}
          >
            <span className="flex flex-col gap-1.5 w-6">
              <span className={`block h-0.5 rounded-full bg-white transition-all duration-300 ${menuOpen ? 'rotate-45 translate-y-2' : ''}`} />
              <span className={`block h-0.5 rounded-full bg-white transition-all duration-300 ${menuOpen ? 'opacity-0' : ''}`} />
              <span className={`block h-0.5 rounded-full bg-white transition-all duration-300 ${menuOpen ? '-rotate-45 -translate-y-2' : ''}`} />
            </span>
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <div className="md:hidden bg-slate-900 px-6 pb-6 shadow-lg border-t border-white/5">
          <ul className="flex flex-col gap-4 pt-4">
            {navLinks.map((link) => (
              <li key={link.label}>
                <a
                  href={link.href}
                  onClick={(e) => handleNavClick(e, link.href)}
                  className="block text-base font-bold text-white hover:text-primary transition-colors"
                >
                  {link.label}
                </a>
              </li>
            ))}
            <li>
              <button
                onClick={() => { closeMenu(); setSearchOpen(true) }}
                className="w-full text-left text-base font-bold text-white hover:text-primary transition-colors"
              >
                Search
              </button>
            </li>
            <li>
              <a
                href="#cart"
                onClick={closeMenu}
                className="flex items-center justify-between text-base font-bold text-white hover:text-primary transition-colors"
              >
                <span>Cart</span>
                <span className="flex items-center gap-2">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5 text-amber-300">
                    <path d="M6 6h15l-1.5 9h-13z" />
                    <path d="M6 6l-2 0" />
                    <circle cx="9" cy="20" r="1" />
                    <circle cx="18" cy="20" r="1" />
                  </svg>
                  {totalItems > 0 && (
                    <span className="bg-amber-500 text-slate-900 text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
                      {totalItems}
                    </span>
                  )}
                </span>
              </a>
            </li>
            <li>
              <a
                href="#visit"
                onClick={(e) => handleNavClick(e, '#visit')}
                className="block text-center bg-primary text-white px-5 py-2.5 rounded-lg hover:bg-orange-700 transition-colors font-medium"
              >
                Reserve a Table
              </a>
            </li>
          </ul>
        </div>
      )}

      <SearchModal isOpen={searchOpen} onClose={() => setSearchOpen(false)} />
    </nav>
  )
}
