import { useMemo } from 'react'
import { useCart } from '../hooks/useCart'
import { menuItems } from '../data/menuData'

const RecommendedAddOns = () => {
  const { addToCart, items } = useCart()

  // Get random items from menu, excluding items already in cart
  const recommendedItems = useMemo(() => {
    const cartItemIds = items.map(item => item.id)
    const availableItems = menuItems.filter(item => !cartItemIds.includes(item.id))
    
    // Shuffle array and take first 4 items
    const shuffled = [...availableItems].sort(() => 0.5 - Math.random())
    return shuffled.slice(0, 4)
  }, [items])

  const handleAddToCart = (item) => {
    addToCart(item)
  }

  if (recommendedItems.length === 0) {
    return null // Don't show section if no recommendations available
  }

  return (
    <div className="bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 p-6 shadow-2xl">
      <h3 className="text-xl font-semibold text-white mb-2">Perfect With Your Order</h3>
      <p className="text-slate-400 text-sm mb-6">Complete your coffee moment with these customer favorites</p>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {recommendedItems.map((item) => (
          <div key={item.id} className="group bg-white/5 rounded-2xl border border-white/10 p-4 hover:bg-white/10 transition-all duration-200">
            <div className="flex gap-3">
              <img
                src={item.image}
                alt={item.name}
                className="w-16 h-16 object-cover rounded-xl bg-slate-800 flex-shrink-0"
              />
              
              <div className="flex-1 min-w-0">
                <h4 className="font-semibold text-white text-sm mb-1 truncate">{item.name}</h4>
                <p className="text-slate-400 text-xs mb-2 line-clamp-2">{item.description}</p>
                
                <div className="flex items-center justify-between">
                  <span className="text-amber-300 font-semibold text-sm">{item.price}</span>
                  <button
                    onClick={() => handleAddToCart(item)}
                    className="bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 text-xs font-medium px-3 py-1.5 rounded-lg transition-all duration-200 hover:scale-105 border border-amber-500/30"
                  >
                    Add
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