import { useState, useEffect, useCallback } from 'react'
import { galleryImages } from '../data/menuData'
import FadeUp from '../animations/FadeUp'

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
    <section id="gallery" className="relative overflow-hidden bg-slate-950 py-24 px-6">

      <div className="absolute -right-24 top-10 h-72 w-72 rounded-full bg-amber-500/15 blur-3xl pointer-events-none" />
      <div className="absolute left-0 bottom-1/4 h-96 w-96 rounded-full bg-sky-500/10 blur-3xl pointer-events-none" />

      <div className="relative max-w-6xl mx-auto">

        <div className="text-center mb-14">
          <FadeUp delay={0}>
            <p className="text-sm uppercase tracking-[0.4em] text-amber-300 font-semibold mb-3">
              Our Gallery
            </p>
          </FadeUp>
          <FadeUp delay={0.1}>
            <h2 className="text-5xl md:text-6xl font-extrabold tracking-[-0.04em] text-white max-w-3xl mx-auto">
              A glimpse into our world.
            </h2>
          </FadeUp>
          <FadeUp delay={0.2}>
            <p className="mt-5 text-slate-300 text-base md:text-lg max-w-2xl mx-auto leading-relaxed">
              From the first roast to the final pour — every corner of Driftwood Café is crafted with intention.
            </p>
          </FadeUp>
        </div>

        {/* Masonry Grid */}
        <div className="columns-1 sm:columns-2 lg:columns-3 gap-4 space-y-4">
          {galleryImages.map((image, index) => (
            <FadeUp key={image.id} delay={index * 0.08}>
              <div
                  onClick={() => setLightbox(image)}
                  className="relative group break-inside-avoid overflow-hidden
                    rounded-2xl border border-white/10 cursor-pointer"
                >
                  <img
                    src={image.src}
                    alt={image.alt}
                    loading="lazy"
                    decoding="async"
                    className={`w-full object-cover transition-transform duration-500
                      group-hover:scale-105
                      ${image.size === 'tall' ? 'h-80' : ''}
                      ${image.size === 'wide' ? 'h-56' : ''}
                      ${image.size === 'normal' ? 'h-64' : ''}
                    `}
                  />
                  <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40
                    transition-all duration-300 flex items-center justify-center">
                    <div className="opacity-0 group-hover:opacity-100 transition-opacity
                      duration-300 bg-white/10 backdrop-blur-sm border border-white/20
                      rounded-full p-3">
                      <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                          d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
                      </svg>
                    </div>
                  </div>
                </div>
            </FadeUp>
          ))}
        </div>
      </div>

      {/* Lightbox — unchanged */}
      {lightbox && (
        <div className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-6"
          onClick={() => setLightbox(null)}>
          <div className="relative max-w-4xl w-full" onClick={(e) => e.stopPropagation()}>
            <img src={lightbox.src} alt={lightbox.alt}
              className="w-full max-h-[80vh] object-contain rounded-2xl" />
            <p className="text-center text-slate-300 mt-4 text-sm">{lightbox.alt}</p>
            <button onClick={() => setLightbox(null)}
              className="absolute -top-4 -right-4 bg-white/10 hover:bg-white/20
                backdrop-blur-sm border border-white/20 rounded-full p-2 transition-colors">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            <div className="flex justify-between mt-6">
              <button onClick={() => navigate(-1)} className="bg-white/10 hover:bg-white/20 backdrop-blur-sm border border-white/20
                rounded-full px-5 py-2 text-white text-sm transition-colors">
                ← Prev
              </button>
              <button onClick={() => navigate(1)} className="bg-white/10 hover:bg-white/20 backdrop-blur-sm border border-white/20
                rounded-full px-5 py-2 text-white text-sm transition-colors">
                Next →
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  )
}