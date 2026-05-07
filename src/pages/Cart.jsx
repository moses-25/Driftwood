import { useState } from 'react'
import { useCart } from '../hooks/useCart'
import CartItem from '../components/CartItem'
import OrderSummary from '../components/OrderSummary'
import RecommendedAddOns from '../components/RecommendedAddOns'
import EmptyCart from '../components/EmptyCart'

const Cart = () => {
  const { items, totalItems } = useCart()
  const [promoCode] = useState('')
  const [deliveryOption, setDeliveryOption] = useState('pickup')

  if (totalItems === 0) {
    return <EmptyCart />
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 pt-24 pb-12">
      {/* Background Elements */}
      <div className="absolute -left-24 top-32 h-96 w-96 rounded-full bg-amber-500/10 blur-3xl" />
      <div className="absolute right-0 top-1/3 h-72 w-72 rounded-full bg-orange-500/8 blur-3xl" />
      
      <div className="relative max-w-7xl mx-auto px-6">
        {/* Cart Hero */}
        <div className="text-center mb-12">
          <nav className="flex justify-center mb-6">
            <ol className="flex items-center space-x-2 text-sm text-slate-400">
              <li><a href="#home" className="hover:text-amber-300 transition-colors">Home</a></li>
              <li className="text-slate-600">/</li>
              <li><a href="#menu" className="hover:text-amber-300 transition-colors">Menu</a></li>
              <li className="text-slate-600">/</li>
              <li className="text-amber-300 font-medium">Cart</li>
            </ol>
          </nav>
          
          <h1 className="text-5xl md:text-6xl font-extrabold text-white mb-4 tracking-tight">
            Your <span className="text-amber-400">Cart</span>
          </h1>
          <p className="text-slate-300 text-lg max-w-2xl mx-auto leading-relaxed">
            Review your carefully curated coffee experience before we begin crafting your perfect order.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Cart Items Section */}
          <div className="lg:col-span-2 space-y-6">
            {/* Delivery Options */}
            <div className="bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 p-6 md:p-8 shadow-2xl">
              <h3 className="text-xl md:text-2xl font-bold text-white mb-2">Choose Your Experience</h3>
              <p className="text-slate-300 text-sm md:text-base mb-6">How would you like to enjoy your handcrafted order?</p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
                {[
                  { 
                    id: 'pickup', 
                    label: 'Pickup', 
                    time: '15-20 min', 
                    description: 'Visit our cozy café',
                    benefit: 'Skip delivery fees',
                    icon: (
                      <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                      </svg>
                    )
                  },
                  { 
                    id: 'delivery', 
                    label: 'Delivery', 
                    time: '30-45 min', 
                    description: 'Straight to your door',
                    benefit: 'Contactless & convenient',
                    icon: (
                      <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l2.414 2.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" />
                      </svg>
                    )
                  }
                ].map((option) => (
                  <button
                    key={option.id}
                    onClick={() => setDeliveryOption(option.id)}
                    className={`group relative p-6 rounded-2xl border-2 transition-all duration-300 text-left overflow-hidden ${
                      deliveryOption === option.id
                        ? 'border-amber-500 bg-gradient-to-br from-amber-500/15 to-orange-500/10 text-amber-100 shadow-[0_15px_35px_rgba(251,191,36,0.15)] scale-[1.02]'
                        : 'border-white/15 bg-white/5 text-slate-300 hover:bg-white/10 hover:border-white/25 hover:scale-[1.01]'
                    }`}
                  >
                    {/* Background gradient for selected state */}
                    {deliveryOption === option.id && (
                      <div className="absolute inset-0 bg-gradient-to-br from-amber-500/5 to-orange-500/5 rounded-2xl" />
                    )}
                    
                    <div className="relative z-10">
                      {/* Icon and Badge */}
                      <div className="flex items-start justify-between mb-4">
                        <div className={`p-3 rounded-xl transition-all duration-200 ${
                          deliveryOption === option.id 
                            ? 'bg-amber-500/20 text-amber-300' 
                            : 'bg-white/10 text-slate-400 group-hover:bg-white/15'
                        }`}>
                          {option.icon}
                        </div>
                        
                        {deliveryOption === option.id && (
                          <div className="bg-amber-500 text-slate-900 text-xs font-bold px-2 py-1 rounded-full">
                            Selected
                          </div>
                        )}
                      </div>

                      {/* Content */}
                      <div className="space-y-2">
                        <h4 className="text-xl font-bold">{option.label}</h4>
                        <p className="text-sm opacity-90">{option.description}</p>
                        
                        <div className="flex items-center justify-between pt-2">
                          <div className="flex items-center gap-2">
                            <svg className="w-4 h-4 opacity-75" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <circle cx="12" cy="12" r="10" />
                              <polyline points="12,6 12,12 16,14" />
                            </svg>
                            <span className="text-sm font-medium">{option.time}</span>
                          </div>
                          
                          <div className={`text-xs font-medium px-2 py-1 rounded-full ${
                            deliveryOption === option.id 
                              ? 'bg-amber-500/20 text-amber-300' 
                              : 'bg-white/10 text-slate-400'
                          }`}>
                            {option.benefit}
                          </div>
                        </div>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
              
              {/* Additional Info */}
              <div className="mt-6 p-4 bg-white/5 rounded-xl border border-white/10">
                <div className="flex items-center gap-2 text-slate-300">
                  <svg className="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="text-sm">
                    {deliveryOption === 'pickup' && 'We\'ll text you when your order is ready for pickup'}
                    {deliveryOption === 'delivery' && 'Free delivery on orders over $25 • $3.99 delivery fee applies'}
                  </span>
                </div>
              </div>
            </div>

            {/* Cart Items */}
            <div className="bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 p-6 shadow-2xl">
              <h3 className="text-xl font-semibold text-white mb-6">Order Items ({totalItems})</h3>
              <div className="space-y-4">
                {items.map((item) => (
                  <CartItem key={`${item.id}-${item.customizations?.size || 'default'}`} item={item} />
                ))}
              </div>
            </div>

            {/* Recommended Add-ons */}
            <RecommendedAddOns />
          </div>

          {/* Order Summary - Sticky on desktop */}
          <div className="lg:sticky lg:top-24 lg:self-start">
            <OrderSummary deliveryOption={deliveryOption} />
          </div>
        </div>

      </div>
    </div>
  )
}

export default Cart