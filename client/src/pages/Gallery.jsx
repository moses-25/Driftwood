import { useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { galleryImages } from '../data/menuData'
import FadeUp from '../animations/FadeUp'

const categoryMap = {
  2: 'Interior',
  3: 'Coffee',
  5: 'Food',
  6: 'Coffee',
  7: 'Barista',
  8: 'Coffee',
}

export default function Gallery() {
  const [lightbox, setLightbox] = useState(null)

  const navigate = useCallback((dir) => {
    if (!lightbox) return
    const idx = galleryImages.findIndex(i => i.id === lightbox.id)
    const next = (idx + dir + galleryImages.length) % galleryImages.length
    setLightbox(galleryImages[next])
  }, [lightbox])

  useEffect(() => {
    if (!lightbox) return
    const handler = (e) => {
      if (e.key === 'Escape') setLightbox(null)
      if (e.key === 'ArrowRight') navigate(1)
      if (e.key === 'ArrowLeft') navigate(-1)
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [lightbox, navigate])

  return (
    <section id="gallery" className="relative bg-white py-16 px-6 overflow-hidden">

      <div className="max-w-6xl mx-auto">

        {/* ── Header row ── */}
        <FadeUp delay={0}>
          <div className="mb-8">
            <h2 className="font-display text-3xl md:text-4xl text-espresso font-bold tracking-tight">
              Gallery
            </h2>
          </div>
        </FadeUp>

        {/* ── Thin divider ── */}
        <div className="h-px bg-espresso/10 mb-8" />

        {/* ── Grid ── */}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-x-4 gap-y-10">
          {galleryImages.map((image, i) => (
            <motion.div
              key={image.id}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.3, delay: i * 0.05 }}
              className="group flex flex-col cursor-pointer"
              onClick={() => setLightbox(image)}
              role="button"
              tabIndex={0}
              aria-label={`View ${image.alt}`}
              onKeyDown={(e) => e.key === 'Enter' && setLightbox(image)}
            >
              {/* Image */}
              <div className="relative overflow-hidden aspect-[4/5] bg-warmbeige/30">
                <img
                  src={image.src}
                  alt={image.alt}
                  loading="lazy"
                  decoding="async"
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.03]"
                />

                {/* Hover overlay */}
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-all duration-300 flex items-center justify-center">
                  <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
                    </svg>
                  </div>
                </div>
              </div>

              {/* Label row */}
              <div className="mt-3 flex items-baseline justify-between gap-2">
                <p className="text-[11px] uppercase tracking-[0.12em] text-espresso/80 font-medium">
                  {image.alt}
                </p>
                <p className="text-[11px] uppercase tracking-[0.12em] text-espresso/30 font-medium shrink-0">
                  {categoryMap[image.id]}
                </p>
              </div>
            </motion.div>
          ))}
        </div>

      </div>

      {/* ── Lightbox ── */}
      <AnimatePresence>
        {lightbox && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.25 }}
            className="fixed inset-0 z-50 bg-black/95 backdrop-blur-sm flex items-center justify-center p-6"
            onClick={() => setLightbox(null)}
          >
            <motion.div
              initial={{ scale: 0.96, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.96, opacity: 0 }}
              transition={{ duration: 0.3, ease: [0.25, 0.1, 0.25, 1] }}
              className="relative max-w-4xl w-full"
              onClick={(e) => e.stopPropagation()}
            >
              <img
                src={lightbox.src}
                alt={lightbox.alt}
                className="w-full max-h-[80vh] object-contain"
              />

              {/* Caption */}
              <div className="mt-4 flex items-center justify-between">
                <p className="text-[11px] uppercase tracking-[0.15em] text-white/40 font-mono">
                  {lightbox.alt}
                </p>
                <p className="text-[11px] uppercase tracking-[0.15em] text-white/20 font-mono">
                  {galleryImages.findIndex(i => i.id === lightbox.id) + 1} / {galleryImages.length}
                </p>
              </div>

              {/* Close */}
              <button
                onClick={() => setLightbox(null)}
                className="absolute -top-4 -right-4 h-9 w-9 rounded-full border border-white/15 bg-black flex items-center justify-center text-white/60 hover:text-white hover:border-white/40 transition-colors"
                aria-label="Close"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.75} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>

              {/* Prev / Next */}
              <button
                onClick={() => navigate(-1)}
                className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-14 h-10 w-10 rounded-full border border-white/15 bg-black/80 flex items-center justify-center text-white/60 hover:text-white hover:border-white/40 transition-colors"
                aria-label="Previous"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <button
                onClick={() => navigate(1)}
                className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-14 h-10 w-10 rounded-full border border-white/15 bg-black/80 flex items-center justify-center text-white/60 hover:text-white hover:border-white/40 transition-colors"
                aria-label="Next"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  )
}
