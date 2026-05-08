import { useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { reviews } from '../data/menuData'
import FadeUp from '../animations/FadeUp'

const StarRating = ({ rating, interactive = false, onRatingChange }) => (
  <div className="flex gap-1">
    {[1, 2, 3, 4, 5].map((star) => (
      <svg
        key={star}
        className={`w-4 h-4 ${star <= rating ? 'text-amber-400' : 'text-slate-600'} ${
          interactive ? 'cursor-pointer hover:text-amber-300 transition-colors' : ''
        }`}
        fill="currentColor"
        viewBox="0 0 24 24"
        onClick={interactive ? () => onRatingChange(star) : undefined}
      >
        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
      </svg>
    ))}
  </div>
)

const ReviewForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({ name: '', review: '', rating: 0 })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (formData.name.trim() && formData.review.trim() && formData.rating > 0) {
      onSubmit({
        id: Date.now(),
        name: formData.name.trim(),
        date: new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }),
        rating: formData.rating,
        review: formData.review.trim(),
        avatar: formData.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2),
      })
      setFormData({ name: '', review: '', rating: 0 })
    }
  }

  return (
    <div className="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur-sm p-6">
      <h3 className="text-xl font-bold text-white mb-4">Share Your Experience</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="review-name" className="block text-sm font-medium text-slate-300 mb-2">Your Name</label>
          <input
            id="review-name"
            type="text"
            value={formData.name}
            onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
            className="w-full px-3 py-2 bg-slate-800/50 border border-white/10 rounded-lg text-white placeholder-slate-500 focus:border-amber-500/50 focus:outline-none transition-colors"
            placeholder="Enter your name"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">Rating</label>
          <StarRating
            rating={formData.rating}
            interactive
            onRatingChange={(rating) => setFormData(prev => ({ ...prev, rating }))}
          />
        </div>
        <div>
          <label htmlFor="review-text" className="block text-sm font-medium text-slate-300 mb-2">Your Review</label>
          <textarea
            id="review-text"
            value={formData.review}
            onChange={(e) => setFormData(prev => ({ ...prev, review: e.target.value }))}
            className="w-full px-3 py-2 bg-slate-800/50 border border-white/10 rounded-lg text-white placeholder-slate-500 focus:border-amber-500/50 focus:outline-none transition-colors resize-none"
            rows={4}
            placeholder="Tell us about your experience..."
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-amber-500 hover:bg-amber-600 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200"
        >
          Submit Review
        </button>
      </form>
    </div>
  )
}

export default function Reviews() {
  const [userReviews, setUserReviews] = useState([])
  const [current, setCurrent] = useState(0)
  const [direction, setDirection] = useState(1)

  const allReviews = [...userReviews, ...reviews]
  const total = allReviews.length

  const go = useCallback((dir) => {
    setDirection(dir)
    setCurrent(prev => (prev + dir + total) % total)
  }, [total])

  const handleNewReview = (newReview) => {
    setUserReviews(prev => [newReview, ...prev])
    // Jump to the new review (it lands at index 0)
    setDirection(-1)
    setCurrent(0)
  }

  const review = allReviews[current]

  const variants = {
    enter: (dir) => ({ opacity: 0, x: dir > 0 ? 60 : -60 }),
    center: { opacity: 1, x: 0 },
    exit: (dir) => ({ opacity: 0, x: dir > 0 ? -60 : 60 }),
  }

  return (
    <section id="reviews" className="relative overflow-hidden bg-slate-950 py-24 px-6">
      <div className="absolute left-0 top-1/4 h-72 w-72 rounded-full bg-amber-500/10 blur-3xl pointer-events-none" />
      <div className="absolute right-0 bottom-10 h-96 w-96 rounded-full bg-sky-500/10 blur-3xl pointer-events-none" />

      <div className="relative max-w-6xl mx-auto">

        {/* Heading */}
        <div className="text-center mb-14">
          <FadeUp delay={0}>
            <p className="text-sm uppercase tracking-[0.4em] text-amber-300 font-semibold mb-3">Reviews</p>
          </FadeUp>
          <FadeUp delay={0.1}>
            <h2 className="text-5xl md:text-6xl font-extrabold tracking-[-0.04em] text-white max-w-3xl mx-auto">
              What our customers say.
            </h2>
          </FadeUp>
          <FadeUp delay={0.2}>
            <p className="mt-5 text-slate-300 text-base md:text-lg max-w-2xl mx-auto leading-relaxed">
              Real experiences from the people who make Driftwood Café what it is every single day.
            </p>
          </FadeUp>
        </div>

        {/* Two-column layout: form left, carousel right */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-start">

          {/* Review form */}
          <FadeUp delay={0.1}>
            <ReviewForm onSubmit={handleNewReview} />
          </FadeUp>

          {/* Carousel */}
          <FadeUp delay={0.2}>
            <div className="flex flex-col gap-6">

              {/* Card */}
              <div className="relative overflow-hidden rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur-sm min-h-[260px]">
                <AnimatePresence mode="wait" custom={direction}>
                  <motion.div
                    key={review.id}
                    custom={direction}
                    variants={variants}
                    initial="enter"
                    animate="center"
                    exit="exit"
                    transition={{ duration: 0.3, ease: [0.25, 0.1, 0.25, 1] }}
                    className="p-6 flex flex-col gap-4"
                  >
                    {/* Decorative quote */}
                    <div className="absolute top-5 right-5 text-amber-500/20 text-6xl font-serif leading-none select-none" aria-hidden="true">"</div>

                    <StarRating rating={review.rating} />

                    <p className="text-slate-300 leading-7 text-sm flex-1">
                      "{review.review}"
                    </p>

                    <div className="h-px bg-white/5" />

                    <div className="flex items-center gap-3">
                      <div className="h-10 w-10 rounded-full bg-amber-500/20 border border-amber-500/30 flex items-center justify-center text-amber-300 text-xs font-bold flex-shrink-0">
                        {review.avatar}
                      </div>
                      <div>
                        <p className="text-white text-sm font-semibold">{review.name}</p>
                        <p className="text-slate-500 text-xs">{review.date}</p>
                      </div>
                    </div>
                  </motion.div>
                </AnimatePresence>
              </div>

              {/* Navigation row */}
              <div className="flex items-center justify-between">

                {/* Dot indicators */}
                <div className="flex items-center gap-2">
                  {allReviews.map((_, i) => (
                    <button
                      key={i}
                      onClick={() => { setDirection(i > current ? 1 : -1); setCurrent(i) }}
                      aria-label={`Go to review ${i + 1}`}
                      className={`rounded-full transition-all duration-200 ${
                        i === current
                          ? 'w-6 h-2 bg-amber-400'
                          : 'w-2 h-2 bg-white/20 hover:bg-white/40'
                      }`}
                    />
                  ))}
                </div>

                {/* Prev / Next buttons */}
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => go(-1)}
                    aria-label="Previous review"
                    className="h-10 w-10 rounded-full border border-white/15 bg-white/5 hover:bg-white/15 hover:border-amber-500/40 flex items-center justify-center text-white transition-all duration-200"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7" />
                    </svg>
                  </button>
                  <span className="text-slate-500 text-sm tabular-nums">
                    {current + 1} / {total}
                  </span>
                  <button
                    onClick={() => go(1)}
                    aria-label="Next review"
                    className="h-10 w-10 rounded-full border border-white/15 bg-white/5 hover:bg-white/15 hover:border-amber-500/40 flex items-center justify-center text-white transition-all duration-200"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </button>
                </div>

              </div>
            </div>
          </FadeUp>

        </div>
      </div>
    </section>
  )
}
