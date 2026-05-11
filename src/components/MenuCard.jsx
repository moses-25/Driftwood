import { motion } from 'framer-motion'
import { formatPrice, parsePrice } from '../utils/price'

const MenuCard = ({ item, onAddToCart }) => {
  return (
    <motion.div
      layout
      whileHover={{ y: -6 }}
      transition={{ duration: 0.3, ease: [0.25, 0.1, 0.25, 1] }}
      className="group relative overflow-hidden rounded-4xl bg-gradient-to-b from-espresso to-darkroast shadow-card border border-white/5 flex flex-col"
    >
      {/* Image */}
      <div className="relative aspect-[4/3] overflow-hidden rounded-t-4xl bg-darkroast flex-shrink-0">
        <img
          src={item.image}
          alt={item.name}
          className="absolute inset-0 h-full w-full object-cover object-center transition-transform duration-700 scale-75 group-hover:scale-[0.85]"
        />
        {/* Gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-espresso/90 via-espresso/20 to-transparent" />

        {/* Category badge */}
        <div className="absolute top-4 left-4">
          <span className="inline-block rounded-full bg-darkroast/70 backdrop-blur-sm border border-caramel/20 px-3 py-1 text-[10px] uppercase tracking-[0.25em] text-caramel font-mono font-medium">
            {item.category}
          </span>
        </div>

        {/* Price badge */}
        <div className="absolute top-4 right-4">
          <span className="inline-block rounded-full bg-caramel/90 backdrop-blur-sm px-3 py-1 text-xs font-bold text-darkroast shadow-gold">
            {formatPrice(parsePrice(item.price))}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="relative p-6 flex flex-col gap-3 flex-1">
        {/* Decorative line */}
        <div className="h-px w-8 bg-caramel/40 mb-1" />

        <h3 className="font-display text-xl text-softwhite font-semibold leading-tight tracking-tight">
          {item.name}
        </h3>

        <p className="text-warmbeige/60 text-sm leading-relaxed flex-1">
          {item.description}
        </p>

        <button
          onClick={() => onAddToCart(item)}
          className="mt-3 w-full inline-flex items-center justify-center gap-2 rounded-full bg-gradient-to-r from-caramel to-copper text-softwhite text-sm font-semibold py-3 px-5 shadow-gold hover:shadow-gold-lg hover:brightness-110 transition-all duration-250 group/btn"
          aria-label={`Add ${item.name} to cart`}
        >
          <svg className="w-4 h-4 transition-transform duration-200 group-hover/btn:scale-110" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
          </svg>
          Add to Cart
        </button>
      </div>
    </motion.div>
  )
}

export default MenuCard
