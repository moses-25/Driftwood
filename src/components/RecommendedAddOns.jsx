import { useCart } from '../hooks/useCart'

const recommendedItems = [
  {
    id: 'croissant-1',
    name: 'Butter Croissant',
    price: '$3.50',
    image: '/api/placeholder/120/120',
    category: 'pastries',
    description: 'Flaky, buttery perfection'
  },
  {
    id: 'muffin-1',
    name: 'Blueberry Muffin',
    price: '$4.25',
    image: '/api/placeholder/120/120',
    category: 'pastries',
    description: 'Fresh blueberries in every bite'
  },
  {
    id: 'cookie-1',
    name: 'Chocolate Chip Cookie',
    price: '$2.75',
    image: '/api/placeholder/120/120',
    category: 'pastries',
    description: 'Warm, gooey, and irresistible'
  },
  {
    id: 'sandwich-1',
    name: 'Avocado Toast',
    price: '$8.50',
    image: '/api/placeholder/120/120',
    category: 'specials',
    description: 'Smashed avocado on artisan bread'
  }
]

const RecommendedAddOns = () => {
  const { addToCart } = useCart()

  const handleAddToCart = (item) => {
    addToCart(item)
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