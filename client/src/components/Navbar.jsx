import { useState, useEffect, useCallback } from 'react'
import { useCart } from '../hooks/useCart'
import { useRouter } from '../hooks/useRouter'
import SearchModal from './SearchModal'
import logo from '../assets/logo.png'

const navLinks = [
  { label: 'Home',     href: '#home' },
  { label: 'About',    href: '#about' },
  { label: 'Menu',     href: '#menu' },
  { label: 'Gallery',  href: '#gallery' },
  { label: 'Merch',    href: '#reviews' },
  { label: 'Visit Us', href: '#visit' },
]

const SECTION_IDS = new Set(['home', 'about', 'menu', 'gallery', 'reviews', 'visit'])

export default function Navbar({ pendingScrollRef }) {
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)
  const [searchOpen, setSearchOpen] = useState(false)
  const { totalItems } = useCart()
  const { navigate, isFullPage } = useRouter()

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 40)
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

  const handleNavClick = useCallback((e, href) => {
    const sectionId = href.replace('#', '')
    if (isFullPage && SECTION_IDS.has(sectionId)) {
      e.preventDefault()
      closeMenu()
      if (pendingScrollRef) pendingScrollRef.current = sectionId
      navigate('#home')
    } else {
      closeMenu()
    }
  }, [isFullPage, navigate, closeMenu, pendingScrollRef])

  return (
    <nav
      className={`fixed top-0 left-0 w-full z-50 transition-all duration-500 ${
        scrolled
          ? 'bg-softwhite/95 backdrop-blur-xl shadow-soft border-b border-warmbeige/60'
          : 'bg-transparent'
      }`}
      role="navigation"
      aria-label="Main navigation"
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

        {/* Logo */}
        <a
          href="#home"
          onClick={(e) => handleNavClick(e, '#home')}
          className="flex items-center gap-3 group"
          aria-label="Driftwood Café — Home"
        >
          <img
            src={logo}
            alt="Driftwood Café logo"
            className="h-10 w-auto transition-transform duration-300 group-hover:scale-105"
          />
          <span className="font-display text-xl font-bold tracking-tight">
            <span className={`transition-colors duration-300 ${scrolled ? 'text-caramel' : 'text-caramel'}`}>
              Driftwood
            </span>
            <span className={`transition-colors duration-300 ${scrolled ? 'text-espresso' : 'text-softwhite'}`}>
              {' '}Café
            </span>
          </span>
        </a>

        {/* Desktop Nav Links */}
        <ul className="hidden md:flex items-center gap-8" role="list">
          {navLinks.map((link) => (
            <li key={link.label}>
              <a
                href={link.href}
                onClick={(e) => handleNavClick(e, link.href)}
                className={`relative text-base font-bold tracking-wide transition-colors duration-200 group font-fjalla ${
                  scrolled ? 'text-espresso hover:text-caramel' : 'text-softwhite hover:text-caramel'
                }`}
              >
                {link.label}
                <span className="absolute -bottom-0.5 left-0 w-0 h-px bg-caramel transition-all duration-300 group-hover:w-full" />
              </a>
            </li>
          ))}
        </ul>

        {/* Right Side Actions */}
        <div className="flex items-center gap-2">

          {/* Search */}
          <button
            onClick={() => setSearchOpen(true)}
            className={`hidden md:flex h-10 w-10 items-center justify-center rounded-full transition-all duration-200 ${
              scrolled
                ? 'text-espresso/60 hover:text-espresso hover:bg-warmbeige'
                : 'text-softwhite/70 hover:text-softwhite hover:bg-softwhite/10'
            }`}
            aria-label="Open search"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" className="w-4.5 h-4.5">
              <circle cx="11" cy="11" r="7" />
              <path d="M21 21l-4.35-4.35" />
            </svg>
          </button>

          {/* Cart */}
          <a
            href="#cart"
            className={`hidden md:flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 relative ${
              scrolled
                ? 'text-espresso/70 hover:text-espresso hover:bg-warmbeige border border-warmbeige'
                : 'text-softwhite/80 hover:text-softwhite hover:bg-softwhite/10 border border-softwhite/20'
            }`}
            aria-label={`Cart${totalItems > 0 ? `, ${totalItems} items` : ''}`}
          >
            <span className="text-lg" aria-hidden="true">🛒

            </span>
            <span>Cart</span>
            {totalItems > 0 && (
              <span className="absolute -top-1.5 -right-1.5 bg-caramel text-softwhite text-[10px] font-bold rounded-full h-5 w-5 flex items-center justify-center shadow-gold" aria-hidden="true">
                {totalItems}
              </span>
            )}
          </a>

          {/* Reserve CTA */}
          <a
            href="#visit"
            onClick={(e) => handleNavClick(e, '#visit')}
            className="hidden md:inline-flex items-center justify-center bg-black text-softwhite text-sm font-semibold px-6 py-2.5 rounded-full shadow-gold hover:shadow-gold-lg hover:-translate-y-0.5 transition-all duration-250"
          >
            Reserve a Table
          </a>

          {/* Hamburger */}
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className={`md:hidden flex h-10 w-10 items-center justify-center rounded-full border transition-all duration-200 ${
              scrolled
                ? 'border-warmbeige bg-cream hover:bg-warmbeige text-espresso'
                : 'border-softwhite/20 bg-softwhite/10 hover:bg-softwhite/20 text-softwhite'
            }`}
            aria-label={menuOpen ? 'Close menu' : 'Open menu'}
            aria-expanded={menuOpen}
          >
            <span className="flex flex-col gap-1.5 w-5">
              <span className={`block h-0.5 rounded-full transition-all duration-300 ${menuOpen ? 'rotate-45 translate-y-2 bg-espresso' : scrolled ? 'bg-espresso' : 'bg-softwhite'}`} />
              <span className={`block h-0.5 rounded-full transition-all duration-300 ${menuOpen ? 'opacity-0' : scrolled ? 'bg-espresso' : 'bg-softwhite'}`} />
              <span className={`block h-0.5 rounded-full transition-all duration-300 ${menuOpen ? '-rotate-45 -translate-y-2 bg-espresso' : scrolled ? 'bg-espresso' : 'bg-softwhite'}`} />
            </span>
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {menuOpen && (
        <div className="md:hidden bg-softwhite/98 backdrop-blur-xl border-t border-warmbeige/60 shadow-luxury">
          <div className="px-6 py-6 flex flex-col gap-1">
            {navLinks.map((link) => (
              <a
                key={link.label}
                href={link.href}
                onClick={(e) => handleNavClick(e, link.href)}
                className="block py-3 text-lg font-bold text-espresso hover:text-caramel border-b border-warmbeige/40 last:border-0 transition-colors font-fjalla"
              >
                {link.label}
              </a>
            ))}
            <button
              onClick={() => { closeMenu(); setSearchOpen(true) }}
              className="text-left py-3 text-lg font-bold text-espresso hover:text-caramel border-b border-warmbeige/40 transition-colors font-fjalla"
            >
              Search
            </button>
            <a
              href="#cart"
              onClick={closeMenu}
              className="flex items-center justify-between py-3 text-lg font-bold text-espresso hover:text-caramel border-b border-warmbeige/40 transition-colors font-fjalla"
            >
              <span>Cart</span>
              {totalItems > 0 && (
                <span className="bg-caramel text-softwhite text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
                  {totalItems}
                </span>
              )}
            </a>
            <div className="pt-4">
              <a
                href="#visit"
                onClick={(e) => handleNavClick(e, '#visit')}
                className="block text-center bg-black text-softwhite font-semibold px-6 py-3 rounded-full shadow-gold transition-all duration-200"
              >
                Reserve a Table
              </a>
            </div>
          </div>
        </div>
      )}

      <SearchModal isOpen={searchOpen} onClose={() => setSearchOpen(false)} />
    </nav>
  )
}
