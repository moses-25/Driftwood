import { useMemo, useRef } from 'react'
import { useCart } from '../hooks/useCart'
import { menuItems } from '../data/menuData'
import { formatPrice, parsePrice } from '../utils/price'

const RecommendedAddOns = () => {
  const { addToCart, items } = useCart()
  // Stable shuffle seed — only randomise once per mount, not on every render
  const shuffleSeed = useRef(Math.random())

  const recommendedItems = useMemo(() => {
    const cartItemIds = new Set(items.map(item => item.id))
    const available = menuItems.filter(item => !cartItemIds.has(item.id))
    // Deterministic-ish shuffle using the stable seed
    return [...available]
      .sort((a, b) => (((a.id * shuffleSeed.current) % 1) - ((b.id * shuffleSeed.current) % 1)))
      .slice(0, 4)
  }, [items])

  if (recommendedItems.length === 0) return null

  return (
    <div className="bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 p-6 md:p-8 shadow-2xl">
      <h3 className="text-xl md:text-2xl font-bold text-white mb-2 md:mb-3">Perfect With Your Order</h3>
      <p className="text-slate-300 text-sm md:text-base mb-6 md:mb-8">Complete your coffee moment with these customer favorites</p>
      
      <div className="grid grid-cols-1 gap-4 md:gap-6">
        {recommendedItems.map((item) => (
          <div key={item.id} className="group bg-white/8 rounded-2xl border border-white/15 p-4 md:p-6 hover:bg-white/12 transition-all duration-200 hover:scale-[1.02] hover:shadow-xl">
            <div className="flex gap-3 md:gap-4">
              <img
                src={item.image}
                alt={item.name}
                className="w-16 h-16 md:w-20 md:h-20 object-cover rounded-xl bg-slate-800 flex-shrink-0 group-hover:scale-105 transition-transform duration-200"
              />
              
              <div className="flex-1 min-w-0">
                <h4 className="font-bold text-white text-sm md:text-base mb-1 md:mb-2 truncate">{item.name}</h4>
                <p className="text-slate-300 text-xs md:text-sm mb-3 md:mb-4 line-clamp-2 leading-relaxed">{item.description}</p>
                
                <div className="flex items-center justify-between gap-2">
                  <span className="text-amber-300 font-bold text-base md:text-lg">{formatPrice(parsePrice(item.price))}</span>
                  <button
                    onClick={() => addToCart(item)}
                    className="bg-gradient-to-r from-amber-500/30 to-orange-500/30 hover:from-amber-500/40 hover:to-orange-500/40 text-amber-200 text-xs md:text-sm font-semibold px-3 py-2 md:px-4 md:py-2.5 rounded-xl transition-all duration-200 hover:scale-105 border border-amber-500/40 shadow-lg hover:shadow-amber-500/25 whitespace-nowrap"
                  >
                    Add to Cart
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default RecommendedAddOns