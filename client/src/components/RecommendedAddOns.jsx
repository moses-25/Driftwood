import { useMemo, useState } from 'react'
import { useCart } from '../hooks/useCart'
import { useProducts } from '../hooks/useProducts'
import { menuItems as staticMenuItems } from '../data/menuData'
import { formatPrice, parsePrice } from '../utils/price'

/**
 * djb2-inspired hash — converts any ID (number or string) to a stable
 * unsigned 32-bit integer so the seed-based shuffle works regardless of
 * whether IDs are numeric (1, 2 …) or string-based ('m1', 'special-3' …).
 */
function hashId(id) {
  const str = String(id)
  let h = 5381
  for (let i = 0; i < str.length; i++) {
    h = (Math.imul(h, 33) ^ str.charCodeAt(i)) >>> 0
  }
  return h
}

const RecommendedAddOns = () => {
  const { addToCart, items } = useCart()
  const [seed] = useState(() => Math.random())
  
  // Fetch products from backend (same as Menu page)
  const { products: backendProducts, loading, error } = useProducts()
  
  // Use backend products if available, otherwise fall back to static data
  const menuItems = useMemo(() => {
    if (backendProducts && backendProducts.length > 0) {
      return backendProducts
    }
    if (loading || error) {
      return staticMenuItems
    }
    return staticMenuItems
  }, [backendProducts, loading, error])

  const recommendedItems = useMemo(() => {
    const cartItemIds = new Set(items.map(item => item.id))
    const available = menuItems.filter(item => !cartItemIds.has(item.id))
    return [...available]
      .sort((a, b) => ((hashId(a.id) * seed) % 1) - ((hashId(b.id) * seed) % 1))
      .slice(0, 4)
  }, [items, seed, menuItems])

  if (recommendedItems.length === 0) return null

  return (
    <div className="bg-white rounded-2xl shadow-soft p-6">
      <h3
        className="text-lg font-bold text-espresso mb-1 font-science-gothic"
      >
        You Might Also Like
      </h3>
      <p
        className="text-espresso/50 text-sm mb-6 font-tinos"
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
                className="font-semibold text-espresso text-sm truncate font-tinos"
              >
                {item.name}
              </h4>
              <p
                className="text-espresso/45 text-xs mt-0.5 line-clamp-1 font-tinos"
              >
                {item.description}
              </p>
            </div>
            <div className="flex items-center gap-3 flex-shrink-0">
              <span
                className="text-espresso font-semibold text-sm font-tinos"
              >
                {formatPrice(parsePrice(item.price))}
              </span>
              <button
                onClick={() => addToCart(item)}
                className="bg-caramel hover:bg-copper text-softwhite text-xs font-semibold px-3 py-1.5 rounded-lg transition-colors duration-200 font-tinos"
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
