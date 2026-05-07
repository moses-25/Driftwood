import { useCart } from '../hooks/useCart'

const OrderSummary = ({ deliveryOption }) => {
  const { items } = useCart()

  // Calculate totals
  const subtotal = items.reduce((sum, item) => {
    return sum + (parseFloat(item.price.replace('$', '')) * item.quantity)
  }, 0)

  const deliveryFee = deliveryOption === 'delivery' ? 3.99 : 0
  const tax = subtotal * 0.08875 // 8.875% tax
  const total = subtotal + deliveryFee + tax

  return (
    <div className="bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 p-6 shadow-2xl">
      <h3 className="text-xl font-semibold text-white mb-6">Order Summary</h3>
      
      <div className="space-y-4 mb-6">
        <div className="flex justify-between text-slate-300">
          <span>Subtotal</span>
          <span>${subtotal.toFixed(2)}</span>
        </div>
        
        {deliveryFee > 0 && (
          <div className="flex justify-between text-slate-300">
            <span>Delivery Fee</span>
            <span>${deliveryFee.toFixed(2)}</span>
          </div>
        )}
        
        <div className="flex justify-between text-slate-300">
          <span>Tax</span>
          <span>${tax.toFixed(2)}</span>
        </div>
        
        <div className="border-t border-white/10 pt-4">
          <div className="flex justify-between text-white font-semibold text-lg">
            <span>Total</span>
            <span className="text-amber-300">${total.toFixed(2)}</span>
          </div>
        </div>
      </div>

      {/* Checkout Button */}
      <button className="w-full bg-gradient-to-r from-amber-500 to-orange-500 text-slate-900 font-bold py-4 px-6 rounded-2xl hover:from-amber-600 hover:to-orange-600 transition-all duration-200 transform hover:scale-[1.02] hover:shadow-2xl shadow-[0_15px_35px_rgba(251,191,36,0.25)] mb-4">
        <div className="flex items-center justify-center gap-2">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          Secure Checkout
        </div>
      </button>

    </div>
  )
}

export default OrderSummary