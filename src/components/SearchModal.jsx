import { useState, useEffect, useRef, useMemo } from 'react'
import { menuItems, reviews } from '../data/menuData'
import { formatPrice, parsePrice } from '../utils/price'

const sections = [
  { name: 'Home', href: '#home', description: 'Welcome to Driftwood Café' },
  { name: 'About', href: '#about', description: 'Our story and values' },
  { name: 'Menu', href: '#menu', description: 'Coffee, pastries & specials' },
  { name: 'Gallery', href: '#gallery', description: 'Photos of our café' },
  { name: 'Reviews', href: '#reviews', description: 'What customers say' },
  { name: 'Visit Us', href: '#visit', description: 'Location & hours' },
]

export default function SearchModal({ isOpen, onClose }) {
  const [searchQuery, setSearchQuery] = useState('')
  const inputRef = useRef(null)

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50)
    }
  }, [isOpen])

  const handleClose = () => {
    setSearchQuery('')
    onClose()
  }

  const searchResults = useMemo(() => {
    const query = searchQuery.trim().toLowerCase()
    if (!query) return { menu: [], reviews: [], sections: [] }

    return {
      menu: menuItems.filter(item =>
        item.name.toLowerCase().includes(query) ||
        item.description.toLowerCase().includes(query) ||
        item.category.toLowerCase().includes(query)
      ),
      reviews: reviews.filter(r =>
        r.name.toLowerCase().includes(query) ||
        r.review.toLowerCase().includes(query)
      ),
      sections: sections.filter(s =>
        s.name.toLowerCase().includes(query) ||
        s.description.toLowerCase().includes(query)
      ),
    }
  }, [searchQuery])

  const totalResults = searchResults.sections.length + searchResults.menu.length + searchResults.reviews.length
  const hasResults = totalResults > 0

  const handleResultClick = (href) => {
    handleClose()
    setTimeout(() => {
      document.querySelector(href)?.scrollIntoView({ behavior: 'smooth' })
    }, 100)
  }

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) handleClose()
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') handleClose()
  }

  if (!isOpen) return null

  return (
    <div
      className="fixed inset-0 z-[100] bg-black/70 backdrop-blur-sm flex items-start justify-center pt-16 sm:pt-20 px-3 sm:px-4"
      onClick={handleBackdropClick}
      onKeyDown={handleKeyDown}
      role="dialog"
      aria-modal="true"
      aria-label="Search"
    >
      <div className="w-full max-w-lg bg-slate-900 rounded-xl shadow-2xl border border-white/10 overflow-hidden">

        {/* Search Input */}
        <div className="px-3 py-3 sm:px-4 sm:py-3.5 border-b border-white/10 flex items-center gap-2">
          <div className="relative flex-1">
            <svg
              viewBox="0 0 24 24" fill="none" stroke="currentColor"
              strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
              className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none"
            >
              <circle cx="11" cy="11" r="7" />
              <path d="M21 21l-4.35-4.35" />
            </svg>
            <input
              ref={inputRef}
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search menu, reviews, sections..."
              className="w-full pl-9 pr-8 py-2 bg-slate-800 text-white text-sm rounded-lg border border-white/10 focus:outline-none focus:ring-1 focus:ring-primary placeholder-slate-500"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white transition-colors"
                aria-label="Clear search"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>

          {/* Close button — always visible */}
          <button
            onClick={handleClose}
            aria-label="Close search"
            className="flex-shrink-0 flex items-center justify-center w-9 h-9 rounded-lg bg-slate-800 border border-white/10 text-slate-300 hover:text-white hover:bg-slate-700 active:scale-95 transition-all"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Results */}
        <div className="max-h-[55vh] sm:max-h-[50vh] overflow-y-auto">
          {!searchQuery.trim() ? (
            /* Empty state — quick nav hints */
            <div className="px-3 py-4 sm:px-4">
              <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">Quick navigate</p>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-1.5">
                {sections.map((s) => (
                  <button
                    key={s.name}
                    onClick={() => handleResultClick(s.href)}
                    className="text-left px-3 py-2 rounded-lg bg-slate-800/60 hover:bg-slate-800 border border-white/5 hover:border-primary/30 transition-all group"
                  >
                    <span className="text-sm font-medium text-white group-hover:text-primary transition-colors">{s.name}</span>
                    <p className="text-xs text-slate-500 mt-0.5 leading-tight">{s.description}</p>
                  </button>
                ))}
              </div>
            </div>
          ) : !hasResults ? (
            <div className="text-center py-10 px-4">
              <p className="text-slate-400 text-sm">No results for "<span className="text-white">{searchQuery}</span>"</p>
              <p className="text-slate-500 text-xs mt-1">Try a different keyword</p>
            </div>
          ) : (
            <div className="px-3 py-3 sm:px-4 space-y-4">

              {/* Sections */}
              {searchResults.sections.length > 0 && (
                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Sections</p>
                  <div className="space-y-1">
                    {searchResults.sections.map((s) => (
                      <button
                        key={s.name}
                        onClick={() => handleResultClick(s.href)}
                        className="w-full text-left px-3 py-2 rounded-lg bg-slate-800/50 hover:bg-slate-800 border border-white/5 hover:border-primary/30 transition-all group flex items-center gap-2.5"
                      >
                        <div className="w-7 h-7 flex-shrink-0 rounded-md bg-primary/10 flex items-center justify-center group-hover:bg-primary/20 transition-colors">
                          <svg className="w-3.5 h-3.5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                          </svg>
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-white group-hover:text-primary transition-colors">{s.name}</p>
                          <p className="text-xs text-slate-500 truncate">{s.description}</p>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Menu Items */}
              {searchResults.menu.length > 0 && (
                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Menu Items</p>
                  <div className="space-y-1">
                    {searchResults.menu.map((item) => (
                      <button
                        key={item.id}
                        onClick={() => handleResultClick('#menu')}
                        className="w-full text-left px-3 py-2 rounded-lg bg-slate-800/50 hover:bg-slate-800 border border-white/5 hover:border-primary/30 transition-all group flex items-center gap-3"
                      >
                        <img
                          src={item.image}
                          alt={item.name}
                          className="w-10 h-10 sm:w-12 sm:h-12 flex-shrink-0 object-cover rounded-lg"
                        />
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between gap-2">
                            <p className="text-sm font-medium text-white group-hover:text-primary transition-colors truncate">{item.name}</p>
                            <span className="text-xs font-bold text-primary flex-shrink-0">{formatPrice(parsePrice(item.price))}</span>
                          </div>
                          <p className="text-xs text-slate-500 truncate mt-0.5">{item.description}</p>
                          <span className="text-xs text-slate-600 capitalize">{item.category}</span>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Reviews */}
              {searchResults.reviews.length > 0 && (
                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Reviews</p>
                  <div className="space-y-1">
                    {searchResults.reviews.map((review) => (
                      <button
                        key={review.id}
                        onClick={() => handleResultClick('#reviews')}
                        className="w-full text-left px-3 py-2 rounded-lg bg-slate-800/50 hover:bg-slate-800 border border-white/5 hover:border-primary/30 transition-all group flex items-start gap-2.5"
                      >
                        <div className="w-7 h-7 flex-shrink-0 rounded-full bg-primary/10 flex items-center justify-center text-primary text-xs font-bold">
                          {review.avatar}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between gap-2">
                            <p className="text-sm font-medium text-white group-hover:text-primary transition-colors truncate">{review.name}</p>
                            <div className="flex flex-shrink-0">
                              {[...Array(review.rating)].map((_, i) => (
                                <svg key={i} className="w-3 h-3 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
                                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                </svg>
                              ))}
                            </div>
                          </div>
                          <p className="text-xs text-slate-500 line-clamp-1 mt-0.5">{review.review}</p>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        {hasResults && (
          <div className="px-3 py-2 sm:px-4 border-t border-white/10 bg-slate-800/40 flex items-center justify-between">
            <span className="text-xs text-slate-500">{totalResults} result{totalResults !== 1 ? 's' : ''}</span>
            <span className="text-xs text-slate-600">Click to navigate</span>
          </div>
        )}

        {/* Mobile close strip */}
        <div className="sm:hidden border-t border-white/10">
          <button
            onClick={handleClose}
            className="w-full py-3 text-sm font-semibold text-slate-300 hover:text-white active:bg-slate-800 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}
