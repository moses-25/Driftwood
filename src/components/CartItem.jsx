import { useState } from 'react'
import { useCart } from '../hooks/useCart'

const CartItem = ({ item }) => {
  const { addToCart, removeFromCart, removeEntireItem } = useCart()
  const [isRemoving, setIsRemoving] = useState(false)

  const handleRemove = () => {
    setIsRemoving(true)
    setTimeout(() => {
      removeEntireItem(item.id)
    }, 300)
  }

  const handleQuantityChange = (change) => {
    if (change > 0) {
      addToCart(item)
    } else if (item.quantity > 1) {
      removeFromCart(item.id)
    }
  }

  // Calculate item total
  const itemTotal = parseFloat(item.price.replace('$', '')) * item.quantity

  return (
    <div className={`group bg-white/5 rounded-2xl border border-white/10 p-4 transition-all duration-300 ${
      isRemoving ? 'opacity-0 scale-95 translate-x-4' : 'hover:bg-white/10'
    }`}>
      <div className="flex gap-4">
        {/* Product Image */}
        <div className="flex-shrink-0">
          <img
            src={item.image}
            alt={item.name}
            className="w-20 h-20 object-cover rounded-xl bg-slate-800"
          />
        </div>

        {/* Product Details */}
        <div className="flex-1 min-w-0">
          <div className="flex justify-between items-start mb-2">
            <h4 className="font-semibold text-white text-lg truncate pr-2">{item.name}</h4>
            <button
              onClick={handleRemove}
              className="text-slate-400 hover:text-red-400 transition-colors p-1 rounded-lg hover:bg-red-500/10"
              aria-label="Remove item"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <p className="text-slate-300 text-sm mb-3 line-clamp-2">{item.description}</p>

          {/* Customizations */}
          {item.customizations && (
            <div className="mb-3 space-y-1">
              {item.customizations.size && (
                <div className="text-xs text-amber-300">Size: {item.customizations.size}</div>
              )}
              {item.customizations.milk && (
                <div className="text-xs text-amber-300">Milk: {item.customizations.milk}</div>
              )}
              {item.customizations.sugar && (
                <div className="text-xs text-amber-300">Sugar: {item.customizations.sugar}</div>
              )}
              {item.customizations.addOns && item.customizations.addOns.length > 0 && (
                <div className="text-xs text-amber-300">
                  Add-ons: {item.customizations.addOns.join(', ')}
                </div>
              )}
            </div>
          )}

          {/* Quantity and Price */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <button
                onClick={() => handleQuantityChange(-1)}
                disabled={item.quantity <= 1}
                className="w-8 h-8 rounded-full bg-white/10 border border-white/20 flex items-center justify-center text-white hover:bg-white/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed hover:scale-105"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20 12H4" />
                </svg>
              </button>
              
              <span className="w-8 text-center font-semibold text-white">{item.quantity}</span>
              
              <button
                onClick={() => handleQuantityChange(1)}
                className="w-8 h-8 rounded-full bg-white/10 border border-white/20 flex items-center justify-center text-white hover:bg-white/20 transition-all hover:scale-105"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                </svg>
              </button>
            </div>

            <div className="text-right">
              <div className="text-sm text-slate-400">{item.price} each</div>
              <div className="font-semibold text-amber-300 text-lg">${itemTotal.toFixed(2)}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CartItem