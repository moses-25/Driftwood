import { useCart } from '../hooks/useCart'
import { parsePrice, formatPrice } from '../utils/price'

const OrderSummary = () => {
  const { items } = useCart()

  const subtotal = items.reduce((sum, item) => sum + parsePrice(item.price) * item.quantity, 0)
  const tax = subtotal * 0.16
  const total = subtotal + tax

  const itemCount = items.reduce((s, i) => s + i.quantity, 0)

  // Each row.value is a pre-formatted display string ready to render as-is.
  // Do not store raw numbers here — run them through formatPrice() first so
  // the render site never needs to know whether a value is currency, a count,
  // or a plain label like 'At checkout'.
  const rows = [
    { label: 'Items',           value: `${itemCount} ${itemCount === 1 ? 'item' : 'items'}` },
    { label: 'Sub Total',       value: formatPrice(subtotal) },
    { label: 'Shipping',        value: formatPrice(0) },
    { label: 'Taxes (16% VAT)', value: formatPrice(tax) },
    { label: 'Delivery fee',    value: 'At checkout', muted: true },
  ]

  return (
    <div className="bg-white rounded-2xl shadow-soft p-6">

      <h3
        className="text-lg font-bold text-espresso mb-5 pb-4 border-b border-warmbeige/60 font-science-gothic"
      >
        Order Summary
      </h3>

      <div className="space-y-3 mb-5">
        {rows.map(row => (
          <div key={row.label} className="flex justify-between items-center">
            <span className="text-espresso/60 text-sm font-tinos">
              {row.label}
            </span>
            <span
              className={`text-sm font-medium font-tinos ${row.muted ? 'text-espresso/40 italic text-xs' : 'text-espresso'}`}
            >
            {row.value}
            </span>
          </div>
        ))}
      </div>

      {/* Total */}
      <div className="border-t border-warmbeige/60 pt-4 mb-6">
        <div className="flex justify-between items-center">
          <span className="text-espresso font-semibold font-tinos">
            Total
          </span>
          <span className="text-espresso font-bold text-lg font-science-gothic">
            {formatPrice(total)}
          </span>
        </div>
      </div>

      {/* Checkout button */}
      <a
        href="#checkout"
        className="w-full flex items-center justify-center bg-espresso hover:bg-caramel text-softwhite font-bold py-4 px-6 rounded-xl transition-all duration-200 text-sm tracking-wide font-tinos"
      >
        Proceed to Checkout
      </a>
    </div>
  )
}

export default OrderSummary
