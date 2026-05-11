const DELIVERY_OPTIONS = [
  {
    id: 'pickup',
    label: 'Pickup',
    description: 'Visit our cozy café',
    time: '15–20 min',
    badge: 'No delivery fee',
    icon: (
      <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
      </svg>
    ),
  },
  {
    id: 'delivery',
    label: 'Delivery',
    description: 'Straight to your door',
    time: '30–45 min',
    badge: 'KES 399 fee',
    icon: (
      <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l2.414 2.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" />
      </svg>
    ),
  },
]

const DeliveryMethodSection = ({ deliveryMethod, setDeliveryMethod }) => {
  return (
    <div className="bg-white/6 rounded-2xl border border-white/10 p-6 md:p-8">
      <div className="flex items-center gap-3 mb-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-caramel/15 border border-caramel/25">
          <svg className="w-5 h-5 text-caramel" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        <div>
          <h3 className="text-lg font-bold text-white" style={{ fontFamily: "'Science Gothic', sans-serif" }}>Delivery Method</h3>
          <p className="text-sm text-white/40" style={{ fontFamily: "'Tinos', serif" }}>How would you like to receive your order?</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {DELIVERY_OPTIONS.map((option) => {
          const isSelected = deliveryMethod === option.id
          return (
            <button
              key={option.id}
              onClick={() => setDeliveryMethod(option.id)}
              className={`group relative p-5 rounded-xl border-2 text-left transition-all duration-250 ${
                isSelected ? 'border-caramel bg-caramel/10' : 'border-white/10 bg-white/4 hover:border-white/20 hover:bg-white/8'
              }`}
            >
              <div className="flex items-start justify-between mb-3">
                <div className={`p-2.5 rounded-xl transition-all duration-200 ${isSelected ? 'bg-caramel/20 text-caramel' : 'bg-white/8 text-white/50'}`}>
                  {option.icon}
                </div>
                {isSelected && (
                  <div className="flex h-5 w-5 items-center justify-center rounded-full bg-caramel">
                    <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                )}
              </div>
              <h4 className={`text-base font-bold mb-0.5 ${isSelected ? 'text-white' : 'text-white/80'}`} style={{ fontFamily: "'Science Gothic', sans-serif" }}>
                {option.label}
              </h4>
              <p className={`text-sm mb-3 ${isSelected ? 'text-white/60' : 'text-white/35'}`} style={{ fontFamily: "'Tinos', serif" }}>
                {option.description}
              </p>
              <div className="flex items-center justify-between">
                <span className={`text-sm ${isSelected ? 'text-white/60' : 'text-white/35'}`} style={{ fontFamily: "'Tinos', serif" }}>
                  {option.time}
                </span>
                <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${isSelected ? 'bg-caramel/20 text-caramel' : 'bg-white/8 text-white/35'}`} style={{ fontFamily: "'Tinos', serif" }}>
                  {option.badge}
                </span>
              </div>
            </button>
          )
        })}
      </div>
    </div>
  )
}

export default DeliveryMethodSection
