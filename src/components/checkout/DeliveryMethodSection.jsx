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
    <div className="bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 p-6 md:p-8 shadow-2xl">
      <div className="flex items-center gap-3 mb-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/15 border border-amber-500/25">
          <svg className="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        <div>
          <h3 className="text-lg font-bold text-white">Delivery Method</h3>
          <p className="text-xs text-slate-400">How would you like to receive your order?</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {DELIVERY_OPTIONS.map((option) => {
          const isSelected = deliveryMethod === option.id
          return (
            <button
              key={option.id}
              onClick={() => setDeliveryMethod(option.id)}
              className={`group relative p-5 rounded-2xl border-2 text-left transition-all duration-300 overflow-hidden ${
                isSelected
                  ? 'border-amber-500 bg-gradient-to-br from-amber-500/15 to-orange-500/10 shadow-[0_0_24px_rgba(251,191,36,0.18)] scale-[1.02]'
                  : 'border-white/15 bg-white/5 hover:bg-white/10 hover:border-white/25 hover:scale-[1.01]'
              }`}
            >
              {/* Glow overlay */}
              {isSelected && (
                <div className="pointer-events-none absolute inset-0 rounded-2xl bg-gradient-to-br from-amber-500/5 to-transparent" />
              )}

              <div className="relative z-10">
                <div className="flex items-start justify-between mb-3">
                  <div
                    className={`p-2.5 rounded-xl transition-all duration-200 ${
                      isSelected ? 'bg-amber-500/20 text-amber-300' : 'bg-white/10 text-slate-400 group-hover:bg-white/15'
                    }`}
                  >
                    {option.icon}
                  </div>
                  {isSelected && (
                    <div className="flex h-5 w-5 items-center justify-center rounded-full bg-amber-500">
                      <svg className="w-3 h-3 text-slate-900" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  )}
                </div>

                <h4 className={`text-base font-bold mb-0.5 ${isSelected ? 'text-amber-100' : 'text-white'}`}>
                  {option.label}
                </h4>
                <p className={`text-xs mb-3 ${isSelected ? 'text-amber-200/70' : 'text-slate-400'}`}>
                  {option.description}
                </p>

                <div className="flex items-center justify-between">
                  <div className={`flex items-center gap-1.5 text-xs ${isSelected ? 'text-amber-200' : 'text-slate-400'}`}>
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <circle cx="12" cy="12" r="10" />
                      <polyline points="12,6 12,12 16,14" />
                    </svg>
                    {option.time}
                  </div>
                  <span
                    className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                      isSelected ? 'bg-amber-500/20 text-amber-300' : 'bg-white/10 text-slate-400'
                    }`}
                  >
                    {option.badge}
                  </span>
                </div>
              </div>
            </button>
          )
        })}
      </div>
    </div>
  )
}

export default DeliveryMethodSection
