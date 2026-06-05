import { useCart } from '../../hooks/useCart'
import { parsePrice, formatPrice } from '../../utils/price'

const DELIVERY_FEE = 399
const TAX_RATE = 0.16

const CheckoutOrderSummary = ({ deliveryMethod }) => {
  const { items } = useCart()

  const subtotal = items.reduce((sum, item) => sum + parsePrice(item.price) * item.quantity, 0)
  const deliveryFee = deliveryMethod === 'delivery' ? DELIVERY_FEE : 0
  const tax = subtotal * TAX_RATE
  const total = subtotal + deliveryFee + tax
  const estimatedTime = deliveryMethod === 'pickup' ? '15–20 min' : '30–45 min'

  return (
    <div className="bg-white/6 rounded-2xl border border-white/10 p-6">
      <h3 className="text-lg font-bold text-white mb-5 font-science-gothic">
        Order Summary
      </h3>

      {/* Items */}
      <div className="space-y-3 mb-5">
        {items.map((item) => (
          <div key={`${item.id}-${item.customizations?.size || 'default'}`} className="flex items-center gap-3">
            <div className="relative shrink-0">
              <img src={item.image} alt={item.name} className="h-12 w-12 rounded-xl object-cover bg-white/10" />
              <span className="absolute -top-1.5 -right-1.5 flex h-5 w-5 items-center justify-center rounded-full bg-caramel text-white text-xs font-bold">
                {item.quantity}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-base font-medium text-white truncate font-tinos">{item.name}</p>
              {item.customizations?.size && (
                <p className="text-sm text-white/35 font-tinos">{item.customizations.size}</p>
              )}
            </div>
            <span className="text-base font-semibold text-white shrink-0 font-tinos">
              {formatPrice(parsePrice(item.price) * item.quantity)}
            </span>
          </div>
        ))}
      </div>

      <div className="border-t border-white/10 mb-4" />

      {/* Totals */}
      <div className="space-y-2.5 mb-5 font-tinos">
        {[
          { label: 'Subtotal', value: formatPrice(subtotal) },
          { label: 'Delivery fee', value: deliveryFee === 0 ? 'Free' : formatPrice(deliveryFee), green: deliveryFee === 0 },
          { label: 'Tax (16% VAT)', value: formatPrice(tax) },
        ].map(row => (
          <div key={row.label} className="flex justify-between text-base">
            <span className="text-white/40">{row.label}</span>
            <span className={row.green ? 'text-green-400 font-medium' : 'text-white/80'}>{row.value}</span>
          </div>
        ))}
      </div>

      <div className="border-t border-white/10 pt-4 mb-5">
        <div className="flex justify-between items-center">
          <span className="text-base font-bold text-white font-tinos">Total</span>
          <span className="text-xl font-bold text-caramel font-science-gothic">{formatPrice(total)}</span>
        </div>
      </div>

    </div>
  )
}

export default CheckoutOrderSummary
