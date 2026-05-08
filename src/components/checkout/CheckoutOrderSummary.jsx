import { useCart } from '../../hooks/useCart'

const DELIVERY_FEE = 399   // KES
const TAX_RATE = 0.16      // 16% VAT (Kenya standard)

const CheckoutOrderSummary = ({ deliveryMethod }) => {
  const { items } = useCart()

  const subtotal = items.reduce((sum, item) => {
    const price = parseFloat(item.price.replace(/[^0-9.]/g, ''))
    return sum + price * item.quantity
  }, 0)

  const deliveryFee = deliveryMethod === 'delivery' ? DELIVERY_FEE / 100 : 0
  const tax = subtotal * TAX_RATE
  const total = subtotal + deliveryFee + tax

  const estimatedTime = deliveryMethod === 'pickup' ? '15–20 min' : '30–45 min'

  return (
    <div className="bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 p-6 shadow-2xl">
      <h3 className="text-lg font-bold text-white mb-5">Order Summary</h3>

      {/* Items list */}
      <div className="space-y-3 mb-5">
        {items.map((item) => {
          const price = parseFloat(item.price.replace(/[^0-9.]/g, ''))
          return (
            <div key={`${item.id}-${item.customizations?.size || 'default'}`} className="flex items-center gap-3">
              {/* Thumbnail */}
              <div className="relative shrink-0">
                <img
                  src={item.image}
                  alt={item.name}
                  className="h-12 w-12 rounded-xl object-cover bg-slate-800"
                />
                {/* Quantity badge */}
                <span className="absolute -top-1.5 -right-1.5 flex h-5 w-5 items-center justify-center rounded-full bg-amber-500 text-slate-900 text-xs font-bold">
                  {item.quantity}
                </span>
              </div>

              {/* Name + price */}
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white truncate">{item.name}</p>
                {item.customizations?.size && (
                  <p className="text-xs text-slate-500">{item.customizations.size}</p>
                )}
              </div>
              <span className="text-sm font-semibold text-amber-300 shrink-0">
                ${(price * item.quantity).toFixed(2)}
              </span>
            </div>
          )
        })}
      </div>

      {/* Divider */}
      <div className="border-t border-white/10 mb-4" />

      {/* Totals */}
      <div className="space-y-2.5 text-sm mb-5">
        <div className="flex justify-between text-slate-400">
          <span>Subtotal</span>
          <span className="text-slate-200">${subtotal.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-slate-400">
          <span>Delivery fee</span>
          <span className={deliveryFee === 0 ? 'text-green-400 font-medium' : 'text-slate-200'}>
            {deliveryFee === 0 ? 'Free' : `$${deliveryFee.toFixed(2)}`}
          </span>
        </div>
        <div className="flex justify-between text-slate-400">
          <span>Tax (16% VAT)</span>
          <span className="text-slate-200">${tax.toFixed(2)}</span>
        </div>
      </div>

      {/* Total */}
      <div className="border-t border-white/10 pt-4 mb-5">
        <div className="flex justify-between items-center">
          <span className="text-base font-bold text-white">Total</span>
          <span className="text-xl font-extrabold text-amber-300">${total.toFixed(2)}</span>
        </div>
      </div>

      {/* Estimated delivery */}
      <div className="flex items-center gap-2.5 p-3 rounded-xl bg-white/5 border border-white/10 mb-5">
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-amber-500/15 text-amber-400">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" strokeWidth="2" />
            <polyline points="12,6 12,12 16,14" strokeWidth="2" strokeLinecap="round" />
          </svg>
        </div>
        <div>
          <p className="text-xs text-slate-400">Estimated {deliveryMethod === 'pickup' ? 'pickup' : 'delivery'} time</p>
          <p className="text-sm font-semibold text-white">{estimatedTime}</p>
        </div>
      </div>

      {/* Trust badges */}
      <div className="flex items-center justify-center gap-4 text-xs text-slate-500">
        <div className="flex items-center gap-1">
          <svg className="w-3.5 h-3.5 text-amber-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
          </svg>
          Secure
        </div>
        <div className="flex items-center gap-1">
          <svg className="w-3.5 h-3.5 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
          Protected
        </div>
        <div className="flex items-center gap-1">
          <svg className="w-3.5 h-3.5 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
          Trusted
        </div>
      </div>
    </div>
  )
}

export default CheckoutOrderSummary
