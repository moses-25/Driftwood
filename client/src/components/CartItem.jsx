import { useState } from 'react'
import { useCart } from '../hooks/useCart'
import { parsePrice, formatPrice } from '../utils/price'

const CartItem = ({ item }) => {
  const { addToCart, removeFromCart, removeEntireItem } = useCart()
  const [isRemoving, setIsRemoving] = useState(false)

  const handleRemove = () => {
    setIsRemoving(true)
    setTimeout(() => removeEntireItem(item.cartItemId), 300)
  }

  const handleQuantityChange = (change) => {
    if (change > 0) {
      // Pass the item as-is; addToCart will re-derive the same cartItemId
      // from the same id + customizations, so it merges into this line.
      addToCart(item)
    } else if (item.quantity > 1) {
      removeFromCart(item.cartItemId)
    }
  }

  const itemTotal = parsePrice(item.price) * item.quantity

  return (
    <div
      className={`grid md:grid-cols-[2fr_1fr_1fr_1fr] items-center px-5 py-4 gap-3 md:gap-0 transition-all duration-300 ${
        isRemoving ? 'opacity-0 scale-95' : ''
      }`}
    >
      {/* Product */}
      <div className="flex items-center gap-4">
        {/* Remove button */}
        <button
          onClick={handleRemove}
          className="text-espresso/30 hover:text-red-400 transition-colors flex-shrink-0"
          aria-label="Remove item"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <img
          src={item.image}
          alt={item.name}
          loading="lazy"
          decoding="async"
          className="w-16 h-16 object-cover rounded-lg bg-warmbeige/30 flex-shrink-0"
        />

        <div className="min-w-0">
          <h4
            className="font-semibold text-espresso text-base leading-snug truncate font-tinos"
          >
            {item.name}
          </h4>
          <p
            className="text-espresso/45 text-sm mt-0.5 line-clamp-1 font-tinos"
          >
            {item.description}
          </p>
          {item.customizations && (
            <div className="mt-1 space-y-0.5">
              {item.customizations.size && (
                <p className="text-[10px] text-caramel font-mono">Size: {item.customizations.size}</p>
              )}
              {item.customizations.milk && (
                <p className="text-[10px] text-caramel font-mono">Milk: {item.customizations.milk}</p>
              )}
              {item.customizations.addOns?.length > 0 && (
                <p className="text-[10px] text-caramel font-mono">Add-ons: {item.customizations.addOns.join(', ')}</p>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Mobile: price, quantity, subtotal in a row. Desktop: grid cells */}
      <div className="flex items-center justify-between md:contents">
        {/* Price */}
        <div className="text-espresso/70 text-sm md:text-base font-tinos md:text-center">
          {formatPrice(parsePrice(item.price))}
        </div>

        {/* Quantity */}
        <div className="flex items-center justify-center gap-3">
          <button
            onClick={() => handleQuantityChange(-1)}
            disabled={item.quantity <= 1}
            className="w-7 h-7 rounded-full border border-espresso/20 flex items-center justify-center text-espresso/60 hover:border-caramel hover:text-caramel transition-all disabled:opacity-30 disabled:cursor-not-allowed"
            aria-label="Decrease quantity"
          >
            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M20 12H4" />
            </svg>
          </button>

          <span
            className="w-6 text-center font-semibold text-espresso text-sm font-tinos"
          >
            {item.quantity}
          </span>

          <button
            onClick={() => handleQuantityChange(1)}
            className="w-7 h-7 rounded-full border border-espresso/20 flex items-center justify-center text-espresso/60 hover:border-caramel hover:text-caramel transition-all"
            aria-label="Increase quantity"
          >
            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 4v16m8-8H4" />
            </svg>
          </button>
        </div>

        {/* Subtotal */}
        <div className="font-semibold text-espresso text-sm font-tinos md:text-center">
          {formatPrice(itemTotal)}
        </div>
      </div>
    </div>
  )
}

export default CartItem
