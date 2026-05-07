import { useState } from 'react'
import { motion } from 'framer-motion'
import { reviews } from '../data/menuData'
import FadeUp from '../animations/FadeUp'
import StaggerContainer from '../animations/StaggerContainer'
import { childVariants } from '../animations/animationVariants'

const StarRating = ({ rating, interactive = false, onRatingChange }) => (
  <div className="flex gap-1">
    {[1, 2, 3, 4, 5].map((star) => (
      <svg key={star}
        className={`w-4 h-4 ${star <= rating ? 'text-amber-400' : 'text-slate-600'} ${interactive ? 'cursor-pointer hover:text-amber-300 transition-colors' : ''}`}
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
  const [formData, setFormData] = useState({
    name: '',
    review: '',
    rating: 0
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (formData.name.trim() && formData.review.trim() && formData.rating > 0) {
      const newReview = {
        id: Date.now(), // Simple ID generation
        name: formData.name.trim(),
        date: new Date().toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        }),
        rating: formData.rating,
        review: formData.review.trim(),
        avatar: formData.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
      }
      onSubmit(newReview)
      setFormData({ name: '', review: '', rating: 0 })
    }
  }

  return (
    <motion.div
      variants={childVariants}
      className="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur-sm p-6"
    >
      <h3 className="text-xl font-bold text-white mb-4">Share Your Experience</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">Your Name</label>
          <input
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
            interactive={true}
            onRatingChange={(rating) => setFormData(prev => ({ ...prev, rating }))}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">Your Review</label>
          <textarea
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
    </motion.div>
  )
}

const ReviewCard = ({ review }) => (
  <motion.div
    variants={childVariants}
    className="relative group rounded-2xl border border-white/10
      bg-slate-900/60 backdrop-blur-sm p-6 flex flex-col gap-4
      hover:border-amber-500/30 hover:bg-slate-900/80 transition-all duration-300"
  >
    <div className="absolute top-5 right-5 text-amber-500/20 text-6xl font-serif leading-none select-none">"</div>
    <StarRating rating={review.rating} />
    <p className="text-slate-300 leading-7 text-sm flex-1">"{review.review}"</p>
    <div className="h-px bg-white/5" />
    <div className="flex items-center gap-3">
      <div className="h-10 w-10 rounded-full bg-amber-500/20 border border-amber-500/30
        flex items-center justify-center text-amber-300 text-xs font-bold flex-shrink-0">
        {review.avatar}
      </div>
      <div>
        <p className="text-white text-sm font-semibold">{review.name}</p>
        <p className="text-slate-500 text-xs">{review.date}</p>
      </div>
    </div>
  </motion.div>
)

export default function Reviews() {
  const [visibleCount, setVisibleCount] = useState(3)
  const [userReviews, setUserReviews] = useState([])

  const allReviews = [...userReviews, ...reviews]
  const visibleReviews = allReviews.slice(0, visibleCount)
  const hasMore = visibleCount < allReviews.length

  const handleNewReview = (newReview) => {
    setUserReviews(prev => [newReview, ...prev])
  }

  return (
    <section id="reviews" className="relative overflow-hidden bg-slate-950 py-24 px-6">
      <div className="absolute left-0 top-1/4 h-72 w-72 rounded-full bg-amber-500/10 blur-3xl pointer-events-none" />
      <div className="absolute right-0 bottom-10 h-96 w-96 rounded-full bg-sky-500/10 blur-3xl pointer-events-none" />

      <div className="relative max-w-6xl mx-auto">

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

        <StaggerContainer className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-12">
          <ReviewForm onSubmit={handleNewReview} />
          <div className="flex items-center justify-center">
            <div className="text-center">
              <h3 className="text-2xl font-bold text-white mb-2">Join the Conversation</h3>
              <p className="text-slate-300 text-sm">
                Share your thoughts about Driftwood Café and help others discover their next favorite spot.
              </p>
            </div>
          </div>
        </StaggerContainer>

        <StaggerContainer className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {visibleReviews.map((review) => (
            <ReviewCard key={review.id} review={review} />
          ))}
        </StaggerContainer>

        {hasMore && (
          <FadeUp delay={0} className="text-center mt-12">
            <button onClick={() => setVisibleCount((prev) => prev + 3)}
              className="bg-white/5 hover:bg-white/10 border border-white/10
                hover:border-amber-500/30 text-white px-8 py-3 rounded-full
                text-sm font-medium transition-all duration-300">
              Load More Reviews
            </button>
          </FadeUp>
        )}
      </div>
    </section>
  )
}