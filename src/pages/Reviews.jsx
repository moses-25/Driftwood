import { useState } from 'react'
import { reviews } from '../data/menuData'

const StarRating = ({ rating }) => (
  <div className="flex gap-1">
    {[1, 2, 3, 4, 5].map((star) => (
      <svg
        key={star}
        className={`w-4 h-4 ${star <= rating ? 'text-amber-400' : 'text-slate-600'}`}
        fill="currentColor"
        viewBox="0 0 24 24"
      >
        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
      </svg>
    ))}
  </div>
)

const ReviewCard = ({ review }) => (
  <div className="relative group rounded-2xl border border-white/10
    bg-slate-900/60 backdrop-blur-sm p-6 flex flex-col gap-4
    hover:border-amber-500/30 hover:bg-slate-900/80
    transition-all duration-300">

    {/* Quote Icon */}
    <div className="absolute top-5 right-5 text-amber-500/20 text-6xl
      font-serif leading-none select-none">
      "
    </div>

    {/* Stars */}
    <StarRating rating={review.rating} />

    {/* Review Text */}
    <p className="text-slate-300 leading-7 text-sm flex-1">
      "{review.review}"
    </p>

    {/* Divider */}
    <div className="h-px bg-white/5" />

    {/* Author */}
    <div className="flex items-center gap-3">
      {/* Avatar */}
      <div className="h-10 w-10 rounded-full bg-amber-500/20 border
        border-amber-500/30 flex items-center justify-center
        text-amber-300 text-xs font-bold flex-shrink-0">
        {review.avatar}
      </div>

      <div>
        <p className="text-white text-sm font-semibold">{review.name}</p>
        <p className="text-slate-500 text-xs">{review.date}</p>
      </div>
    </div>
  </div>
)

export default function Reviews() {
  const [visibleCount, setVisibleCount] = useState(3)

  const visibleReviews = reviews.slice(0, visibleCount)
  const hasMore = visibleCount < reviews.length

  return (
    <section id="reviews" className="relative overflow-hidden bg-slate-950 py-24 px-6">

      {/* Background glows */}
      <div className="absolute left-0 top-1/4 h-72 w-72 rounded-full
        bg-amber-500/10 blur-3xl pointer-events-none" />
      <div className="absolute right-0 bottom-10 h-96 w-96 rounded-full
        bg-sky-500/10 blur-3xl pointer-events-none" />

      <div className="relative max-w-6xl mx-auto">

        {/* Heading */}
        <div className="text-center mb-14">
          <p className="text-sm uppercase tracking-[0.4em] text-amber-300
            font-semibold mb-3">
            Reviews
          </p>
          <h2 className="text-5xl md:text-6xl font-extrabold
            tracking-[-0.04em] text-white max-w-3xl mx-auto">
            What our customers say.
          </h2>
          <p className="mt-5 text-slate-300 text-base md:text-lg max-w-2xl
            mx-auto leading-relaxed">
            Real experiences from the people who make Driftwood Café
            what it is every single day.
          </p>
        </div>

        {/* Review Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {visibleReviews.map((review) => (
            <ReviewCard key={review.id} review={review} />
          ))}
        </div>

        {/* Load More */}
        {hasMore && (
          <div className="text-center mt-12">
            <button
              onClick={() => setVisibleCount((prev) => prev + 3)}
              className="bg-white/5 hover:bg-white/10 border border-white/10
                hover:border-amber-500/30 text-white px-8 py-3 rounded-full
                text-sm font-medium transition-all duration-300"
            >
              Load More Reviews
            </button>
          </div>
        )}

      </div>
    </section>
  )
}