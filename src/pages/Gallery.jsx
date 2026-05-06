import { useState } from 'react'
import { galleryImages } from '../data/menuData'

export default function Gallery() {
  const [lightbox, setLightbox] = useState(null)

  return (
    <section id="gallery" className="relative overflow-hidden bg-slate-950 py-24 px-6">

      {/* Background glows - consistent with your other sections */}
      <div className="absolute -right-24 top-10 h-72 w-72 rounded-full bg-amber-500/15 blur-3xl pointer-events-none" />
      <div className="absolute left-0 bottom-1/4 h-96 w-96 rounded-full bg-sky-500/10 blur-3xl pointer-events-none" />

      <div className="relative max-w-6xl mx-auto">

        {/* Heading */}
        <div className="text-center mb-14 animate-fadeIn">
          <p className="text-sm uppercase tracking-[0.4em] text-amber-300 font-semibold mb-3">
            Our Gallery
          </p>
          <h2 className="text-5xl md:text-6xl font-extrabold tracking-[-0.04em] text-white max-w-3xl mx-auto">
            A glimpse into our world.
          </h2>
          <p className="mt-5 text-slate-300 text-base md:text-lg max-w-2xl mx-auto leading-relaxed">
            From the first roast to the final pour — every corner of Driftwood
            Café is crafted with intention.
          </p>
        </div>

        {/* Masonry Grid */}
        <div className="columns-1 sm:columns-2 lg:columns-3 gap-4 space-y-4">
          {galleryImages.map((image, index) => (
            <div
              key={image.id}
              onClick={() => setLightbox(image)}
              className={`relative group break-inside-avoid overflow-hidden
                rounded-2xl border border-white/10 cursor-pointer
                animate-fadeInUp`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <img
                src={image.src}
                alt={image.alt}
                className={`w-full object-cover transition-transform duration-500
                  group-hover:scale-105
                  ${image.size === 'tall' ? 'h-80' : ''}
                  ${image.size === 'wide' ? 'h-56' : ''}
                  ${image.size === 'normal' ? 'h-64' : ''}
                `}
              />

              {/* Hover Overlay */}
              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40
                transition-all duration-300 flex items-center justify-center">
                <div className="opacity-0 group-hover:opacity-100 transition-opacity
                  duration-300 bg-white/10 backdrop-blur-sm border border-white/20
                  rounded-full p-3">
                  <svg
                    className="w-6 h-6 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"
                    />
                  </svg>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Lightbox */}
      {lightbox && (
        <div
          className="fixed inset-0 z-50 bg-black/90 flex items-center
            justify-center p-6 animate-fadeIn"
          onClick={() => setLightbox(null)}
        >
          <div
            className="relative max-w-4xl w-full animate-scaleIn"
            onClick={(e) => e.stopPropagation()}
          >
            <img
              src={lightbox.src}
              alt={lightbox.alt}
              className="w-full max-h-[80vh] object-contain rounded-2xl"
            />

            {/* Caption */}
            <p className="text-center text-slate-300 mt-4 text-sm">
              {lightbox.alt}
            </p>

            {/* Close Button */}
            <button
              onClick={() => setLightbox(null)}
              className="absolute -top-4 -right-4 bg-white/10 hover:bg-white/20
                backdrop-blur-sm border border-white/20 rounded-full p-2
                transition-colors"
            >
              <svg
                className="w-5 h-5 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>

            {/* Prev / Next */}
            <div className="flex justify-between mt-6">
              <button
                onClick={() => {
                  const idx = galleryImages.findIndex(i => i.id === lightbox.id)
                  const prev = galleryImages[(idx - 1 + galleryImages.length) % galleryImages.length]
                  setLightbox(prev)
                }}
                className="bg-white/10 hover:bg-white/20 backdrop-blur-sm
                  border border-white/20 rounded-full px-5 py-2 text-white
                  text-sm transition-colors"
              >
                ← Prev
              </button>
              <button
                onClick={() => {
                  const idx = galleryImages.findIndex(i => i.id === lightbox.id)
                  const next = galleryImages[(idx + 1) % galleryImages.length]
                  setLightbox(next)
                }}
                className="bg-white/10 hover:bg-white/20 backdrop-blur-sm
                  border border-white/20 rounded-full px-5 py-2 text-white
                  text-sm transition-colors"
              >
                Next →
              </button>
            </div>
          </div>
        </div>
      )}

    </section>
  )
}