const DELIVERY_OPTIONS = [
  {
    id: 'pickup',
    label: 'Pickup',
    description: 'Visit our cozy café',
    time: '15–20 min',
    badge: 'No delivery fee',
  },
  {
    id: 'delivery',
    label: 'Delivery',
    description: 'Straight to your door',
    time: '30–45 min',
    badge: 'KES 399 fee',
  },
]

const DeliveryMethodSection = ({ deliveryMethod, setDeliveryMethod }) => {
  return (
    <div className="space-y-4">
      <h3 className="text-base font-semibold text-white/70 uppercase tracking-widest font-tinos">
        Delivery Method
      </h3>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {DELIVERY_OPTIONS.map((option) => {
          const isSelected = deliveryMethod === option.id
          return (
            <button
              key={option.id}
              onClick={() => setDeliveryMethod(option.id)}
              className={`p-5 rounded-xl border-2 text-left transition-all duration-250 ${
                isSelected
                  ? 'border-caramel bg-caramel/10'
                  : 'border-white/10 bg-white/4 hover:border-white/20 hover:bg-white/8'
              }`}
            >
              <div className="flex items-start justify-between mb-2">
                <h4
                  className={`text-base font-bold font-science-gothic ${isSelected ? 'text-white' : 'text-white/80'}`}
                >
                  {option.label}
                </h4>
                {isSelected && (
                  <div className="flex h-5 w-5 items-center justify-center rounded-full bg-caramel shrink-0">
                    <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                )}
              </div>
              <p className={`text-sm mb-3 font-tinos ${isSelected ? 'text-white/60' : 'text-white/35'}`}>
                {option.description}
              </p>
              <div className="flex items-center justify-between">
                <span className={`text-sm font-tinos ${isSelected ? 'text-white/60' : 'text-white/35'}`}>
                  {option.time}
                </span>
                <span
                  className={`text-xs font-medium px-2 py-0.5 rounded-full font-tinos ${
                    isSelected ? 'bg-caramel/20 text-caramel' : 'bg-white/8 text-white/35'
                  }`}
                >
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
