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
      <h3 className="text-lg font-bold text-white mb-5" style={{ fontFamily: "'Science Gothic', sans-serif" }}>
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
              <p className="text-base font-medium text-white truncate" style={{ fontFamily: "'Tinos', serif" }}>{item.name}</p>
              {item.customizations?.size && (
                <p className="text-sm text-white/35" style={{ fontFamily: "'Tinos', serif" }}>{item.customizations.size}</p>
              )}
            </div>
            <span className="text-base font-semibold text-white shrink-0" style={{ fontFamily: "'Tinos', serif" }}>
              {formatPrice(parsePrice(item.price) * item.quantity)}
            </span>
          </div>
        ))}
      </div>

      <div className="border-t border-white/10 mb-4" />

      {/* Totals */}
      <div className="space-y-2.5 mb-5" style={{ fontFamily: "'Tinos', serif" }}>
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
          <span className="text-base font-bold text-white" style={{ fontFamily: "'Tinos', serif" }}>Total</span>
          <span className="text-xl font-bold text-caramel" style={{ fontFamily: "'Science Gothic', sans-serif" }}>{formatPrice(total)}</span>
        </div>
      </div>

      {/* Estimated time */}
      <div className="flex items-center gap-3 p-3 rounded-xl bg-white/5 border border-white/10 mb-5">
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-caramel/15 text-caramel">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" strokeWidth="2" />
            <polyline points="12,6 12,12 16,14" strokeWidth="2" strokeLinecap="round" />
          </svg>
        </div>
        <div>
          <p className="text-sm text-white/35" style={{ fontFamily: "'Tinos', serif" }}>
            Estimated {deliveryMethod === 'pickup' ? 'pickup' : 'delivery'} time
          </p>
          <p className="text-base font-semibold text-white" style={{ fontFamily: "'Tinos', serif" }}>{estimatedTime}</p>
        </div>
      </div>

      {/* Trust badges */}
      <div className="flex items-center justify-center gap-5 text-sm text-white/30" style={{ fontFamily: "'Tinos', serif" }}>
        {[['Secure', 'M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z'], ['Protected', 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z'], ['Trusted', 'M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z']].map(([label, path]) => (
          <div key={label} className="flex items-center gap-1">
            <svg className="w-3.5 h-3.5 text-caramel" fill={label === 'Secure' ? 'currentColor' : 'none'} stroke={label === 'Secure' ? 'none' : 'currentColor'} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={path} />
            </svg>
            {label}
          </div>
        ))}
      </div>
    </div>
  )
}

export default CheckoutOrderSummary
