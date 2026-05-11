import { useMemo, useState } from 'react'
import { useCart } from '../hooks/useCart'
import { menuItems } from '../data/menuData'
import { formatPrice, parsePrice } from '../utils/price'

const RecommendedAddOns = () => {
  const { addToCart, items } = useCart()
  const [seed] = useState(() => Math.random())

  const recommendedItems = useMemo(() => {
    const cartItemIds = new Set(items.map(item => item.id))
    const available = menuItems.filter(item => !cartItemIds.has(item.id))
    return [...available]
      .sort((a, b) => (((a.id * seed) % 1) - ((b.id * seed) % 1)))
      .slice(0, 4)
  }, [items, seed])

  if (recommendedItems.length === 0) return null

  return (
    <div className="bg-white rounded-2xl shadow-soft p-6">
      <h3
        className="text-lg font-bold text-espresso mb-1"
        style={{ fontFamily: "'Science Gothic', sans-serif" }}
      >
        You Might Also Like
      </h3>
      <p
        className="text-espresso/50 text-sm mb-6"
        style={{ fontFamily: "'Tinos', serif" }}
      >
        Complete your order with these favourites
      </p>

      <div className="divide-y divide-warmbeige/50">
        {recommendedItems.map((item) => (
          <div key={item.id} className="flex items-center gap-4 py-4 first:pt-0 last:pb-0">
            <img
              src={item.image}
              alt={item.name}
              className="w-14 h-14 object-cover rounded-lg bg-warmbeige/30 flex-shrink-0"
            />
            <div className="flex-1 min-w-0">
              <h4
                className="font-semibold text-espresso text-sm truncate"
                style={{ fontFamily: "'Tinos', serif" }}
              >
                {item.name}
              </h4>
              <p
                className="text-espresso/45 text-xs mt-0.5 line-clamp-1"
                style={{ fontFamily: "'Tinos', serif" }}
              >
                {item.description}
              </p>
            </div>
            <div className="flex items-center gap-3 flex-shrink-0">
              <span
                className="text-espresso font-semibold text-sm"
                style={{ fontFamily: "'Tinos', serif" }}
              >
                {formatPrice(parsePrice(item.price))}
              </span>
              <button
                onClick={() => addToCart(item)}
                className="bg-caramel hover:bg-copper text-softwhite text-xs font-semibold px-3 py-1.5 rounded-lg transition-colors duration-200"
                style={{ fontFamily: "'Tinos', serif" }}
              >
                Add
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default RecommendedAddOns
