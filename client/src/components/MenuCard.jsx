import { motion } from 'framer-motion'

const MenuCard = ({ item, isSelected, onSelect, onAddToCart }) => {
  const handleImageError = (e) => {
    // If image fails to load, use a placeholder
    e.target.src = `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'%3E%3Crect fill='%238B4513' width='200' height='200' opacity='0.2'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='16' fill='%238B4513' opacity='0.6'%3ENo Image%3C/text%3E%3C/svg%3E`;
  };

  return (
    <motion.div
      whileHover={{ y: -5 }}
      transition={{ duration: 0.25, ease: [0.25, 0.1, 0.25, 1] }}
      onClick={onSelect}
      className={`cursor-pointer w-[185px] rounded-2xl overflow-hidden flex flex-col border transition-all duration-300 ${
        isSelected
          ? 'border-caramel shadow-gold bg-gradient-to-b from-espresso to-darkroast scale-[1.03]'
          : 'border-white/10 bg-gradient-to-b from-espresso/60 to-darkroast hover:border-white/25'
      }`}
    >
      {/* Image */}
      <div className="relative h-[115px] overflow-hidden flex-shrink-0 bg-espresso/40 flex items-center justify-center">
        <img
          src={item.image}
          alt={item.name}
          onError={handleImageError}
          className="w-[95%] h-[95%] object-contain object-center transition-transform duration-500 hover:scale-110"
          style={{ filter: "drop-shadow(0 8px 16px rgba(0,0,0,0.6))" }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-darkroast/55 to-transparent pointer-events-none" />

        {/* Price badge */}
        <div className="absolute bottom-2 right-2">
          <span className="text-[10px] font-bold bg-caramel/90 text-darkroast rounded-full px-2 py-0.5 leading-none">
            {item.price}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="p-3 flex flex-col gap-1.5 flex-1">
        <h3 className="text-softwhite text-xs font-semibold leading-snug line-clamp-2">
          {item.name}
        </h3>
        <p className="text-warmbeige/50 text-[10px] leading-relaxed line-clamp-3 flex-1">
          {item.description}
        </p>

        {/* Cart button */}
        <button
          onClick={(e) => { e.stopPropagation(); onAddToCart(); }}
          className="mt-2 w-full flex items-center justify-center bg-caramel hover:brightness-110 active:scale-95 text-darkroast rounded-lg py-2 transition-all duration-200"
          aria-label={`Add ${item.name} to cart`}
        >
          <svg
            className="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            strokeWidth="2.5"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
            />
          </svg>
        </button>
      </div>
    </motion.div>
  )
}

export default MenuCard
