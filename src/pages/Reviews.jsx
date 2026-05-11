import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { merchItems } from '../data/menuData'
import { useCart } from '../hooks/useCart'
import FadeUp from '../animations/FadeUp'

const FILTERS = ['All', 'Apparel', 'Drinkware', 'Coffee', 'Accessories']

export default function Merch() {
  const [activeFilter, setActiveFilter] = useState('All')
  const [filterOpen, setFilterOpen] = useState(false)
  const [recentlyAdded, setRecentlyAdded] = useState({})
  const { addToCart } = useCart()

  const filtered = activeFilter === 'All'
    ? merchItems
    : merchItems.filter(i => i.category === activeFilter)

  const handleAdd = (item) => {
    addToCart({ ...item, description: item.category })
    setRecentlyAdded(prev => ({ ...prev, [item.id]: true }))
    setTimeout(() => setRecentlyAdded(prev => ({ ...prev, [item.id]: false })), 1800)
  }

  return (
    <section id="reviews" className="relative bg-black py-16 px-6 overflow-hidden">

      <div className="max-w-6xl mx-auto">

        {/* ── Header row ── */}
        <FadeUp delay={0}>
          <div className="flex items-center justify-between mb-8">
            <h2 className="font-display text-3xl md:text-4xl text-white font-bold tracking-tight">
              {activeFilter === 'All' ? 'Merch' : activeFilter}
            </h2>

            {/* Filter pill */}
            <div className="relative">
              <button
                onClick={() => setFilterOpen(o => !o)}
                className="flex items-center gap-2 border border-white/30 rounded-full px-5 py-2 text-xs font-semibold tracking-[0.15em] uppercase text-white hover:border-white/60 transition-colors duration-200"
              >
                Filter
                <svg
                  className={`w-3 h-3 transition-transform duration-200 ${filterOpen ? 'rotate-180' : ''}`}
                  fill="none" stroke="currentColor" viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              {/* Dropdown */}
              <AnimatePresence>
                {filterOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -8, scale: 0.97 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: -8, scale: 0.97 }}
                    transition={{ duration: 0.18, ease: [0.25, 0.1, 0.25, 1] }}
                    className="absolute right-0 top-full mt-2 bg-[#111] border border-white/10 rounded-2xl overflow-hidden z-20 min-w-[160px] shadow-luxury"
                  >
                    {FILTERS.map(f => (
                      <button
                        key={f}
                        onClick={() => { setActiveFilter(f); setFilterOpen(false) }}
                        className={`w-full text-left px-5 py-3 text-xs font-semibold tracking-wide uppercase transition-colors duration-150 ${
                          activeFilter === f
                            ? 'text-caramel bg-white/5'
                            : 'text-white/50 hover:text-white hover:bg-white/5'
                        }`}
                      >
                        {f}
                      </button>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </FadeUp>

        {/* ── Thin divider ── */}
        <div className="h-px bg-white/10 mb-8" />

        {/* ── Grid ── */}
        <AnimatePresence mode="wait">
          <motion.div
            key={activeFilter}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="grid grid-cols-2 md:grid-cols-3 gap-x-4 gap-y-10"
          >
            {filtered.map((item, i) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3, delay: i * 0.04 }}
                className="group flex flex-col"
              >
                {/* Image — no border, no radius, fills the cell */}
                <div className="relative overflow-hidden aspect-[4/5] bg-[#111]">
                  <img
                    src={item.image}
                    alt={item.name}
                    loading="lazy"
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.03]"
                  />

                  {/* Tag */}
                  {item.tag && (
                    <span className="absolute top-3 left-3 text-[9px] uppercase tracking-widest font-mono font-bold px-2.5 py-1 bg-black text-caramel">
                      {item.tag}
                    </span>
                  )}

                {/* Quick Add — always visible on mobile, slides up on hover for desktop */}
                  <div className="absolute bottom-0 left-0 right-0 md:translate-y-full md:group-hover:translate-y-0 transition-transform duration-300 ease-out">
                    <button
                      onClick={() => handleAdd(item)}
                      className={`w-full py-3 text-xs font-bold tracking-[0.15em] uppercase transition-colors duration-200 ${
                        recentlyAdded[item.id]
                          ? 'bg-white text-black'
                          : 'bg-black/90 text-white hover:bg-caramel hover:text-black'
                      }`}
                    >
                      {recentlyAdded[item.id] ? '✓ Added' : '+ Quick Add'}
                    </button>
                  </div>
                </div>

                {/* Name + Price row — exactly like the reference */}
                <div className="mt-3 flex items-baseline justify-between gap-2">
                  <p className="text-[11px] uppercase tracking-[0.12em] text-white/80 font-medium leading-snug">
                    {item.name}
                  </p>
                  <p className="text-[11px] uppercase tracking-[0.12em] text-white/80 font-medium shrink-0">
                    {item.price}
                  </p>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </AnimatePresence>


      </div>
    </section>
  )
}
