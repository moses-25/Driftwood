import { useCart } from '../hooks/useCart'
import { parsePrice, formatPrice } from '../utils/price'

const OrderSummary = () => {
  const { items } = useCart()

  const subtotal = items.reduce((sum, item) => sum + parsePrice(item.price) * item.quantity, 0)
  const tax = subtotal * 0.16
  const total = subtotal + tax

  const rows = [
    { label: 'Items',           value: items.reduce((s, i) => s + i.quantity, 0), isCount: true },
    { label: 'Sub Total',       value: formatPrice(subtotal) },
    { label: 'Shipping',        value: formatPrice(0) },
    { label: 'Taxes (16% VAT)', value: formatPrice(tax) },
    { label: 'Delivery fee',    value: 'At checkout', muted: true },
  ]

  return (
    <div className="bg-white rounded-2xl shadow-soft p-6">

      <h3
        className="text-lg font-bold text-espresso mb-5 pb-4 border-b border-warmbeige/60"
        style={{ fontFamily: "'Science Gothic', sans-serif" }}
      >
        Order Summary
      </h3>

      <div className="space-y-3 mb-5">
        {rows.map(row => (
          <div key={row.label} className="flex justify-between items-center">
            <span
              className="text-espresso/60 text-sm"
              style={{ fontFamily: "'Tinos', serif" }}
            >
              {row.label}
            </span>
            <span
              className={`text-sm font-medium ${row.muted ? 'text-espresso/40 italic text-xs' : 'text-espresso'}`}
              style={{ fontFamily: "'Tinos', serif" }}
            >
              {row.isCount ? row.value : row.value}
            </span>
          </div>
        ))}
      </div>

      {/* Total */}
      <div className="border-t border-warmbeige/60 pt-4 mb-6">
        <div className="flex justify-between items-center">
          <span
            className="text-espresso font-semibold"
            style={{ fontFamily: "'Tinos', serif" }}
          >
            Total
          </span>
          <span
            className="text-espresso font-bold text-lg"
            style={{ fontFamily: "'Science Gothic', sans-serif" }}
          >
            {formatPrice(total)}
          </span>
        </div>
      </div>

      {/* Checkout button */}
      <a
        href="#checkout"
        className="w-full flex items-center justify-center bg-espresso hover:bg-caramel text-softwhite font-bold py-4 px-6 rounded-xl transition-all duration-200 text-sm tracking-wide"
        style={{ fontFamily: "'Tinos', serif" }}
      >
        Proceed to Checkout
      </a>
    </div>
  )
}

export default OrderSummary
