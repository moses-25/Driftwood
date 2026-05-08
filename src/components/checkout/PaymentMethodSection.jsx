const PAYMENT_METHODS = [
  {
    id: 'pesapal',
    label: 'Pesapal',
    description: 'Cards, mobile money & more',
    badge: 'Recommended',
    icon: (
      <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <rect x="2" y="5" width="20" height="14" rx="3" strokeWidth="2" />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2 10h20" />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 15h4" />
      </svg>
    ),
    color: 'from-violet-500/20 to-purple-500/10',
    borderColor: 'border-violet-500',
    glowColor: 'shadow-[0_0_24px_rgba(139,92,246,0.25)]',
    iconBg: 'bg-violet-500/20 text-violet-300',
    badgeBg: 'bg-violet-500/20 text-violet-300',
  },
  {
    id: 'mpesa',
    label: 'M-Pesa',
    description: 'Pay via Safaricom M-Pesa',
    badge: 'Popular',
    icon: (
      <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
      </svg>
    ),
    color: 'from-green-500/20 to-emerald-500/10',
    borderColor: 'border-green-500',
    glowColor: 'shadow-[0_0_24px_rgba(34,197,94,0.25)]',
    iconBg: 'bg-green-500/20 text-green-300',
    badgeBg: 'bg-green-500/20 text-green-300',
  },
  {
    id: 'cod',
    label: 'Cash on Delivery',
    description: 'Pay when your order arrives',
    badge: null,
    icon: (
      <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
      </svg>
    ),
    color: 'from-amber-500/20 to-orange-500/10',
    borderColor: 'border-amber-500',
    glowColor: 'shadow-[0_0_24px_rgba(251,191,36,0.25)]',
    iconBg: 'bg-amber-500/20 text-amber-300',
    badgeBg: 'bg-amber-500/20 text-amber-300',
  },
]

const PaymentMethodSection = ({ paymentMethod, setPaymentMethod }) => {
  return (
    <div className="bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 p-6 md:p-8 shadow-2xl">
      <div className="flex items-center gap-3 mb-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/15 border border-amber-500/25">
          <svg className="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
          </svg>
        </div>
        <div>
          <h3 className="text-lg font-bold text-white">Payment Method</h3>
          <p className="text-xs text-slate-400">Choose how you'd like to pay</p>
        </div>
      </div>

      <div className="space-y-3">
        {PAYMENT_METHODS.map((method) => {
          const isSelected = paymentMethod === method.id
          return (
            <button
              key={method.id}
              onClick={() => setPaymentMethod(method.id)}
              className={`group w-full relative flex items-center gap-4 p-4 rounded-2xl border-2 text-left transition-all duration-300 overflow-hidden ${
                isSelected
                  ? `border-2 ${method.borderColor} bg-gradient-to-r ${method.color} ${method.glowColor} scale-[1.01]`
                  : 'border-white/15 bg-white/5 hover:bg-white/10 hover:border-white/25'
              }`}
            >
              {/* Icon */}
              <div
                className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl transition-all duration-200 ${
                  isSelected ? method.iconBg : 'bg-white/10 text-slate-400 group-hover:bg-white/15'
                }`}
              >
                {method.icon}
              </div>

              {/* Text */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className={`font-semibold text-sm ${isSelected ? 'text-white' : 'text-slate-200'}`}>
                    {method.label}
                  </span>
                  {method.badge && (
                    <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${isSelected ? method.badgeBg : 'bg-white/10 text-slate-400'}`}>
                      {method.badge}
                    </span>
                  )}
                </div>
                <p className={`text-xs mt-0.5 ${isSelected ? 'text-slate-300' : 'text-slate-500'}`}>
                  {method.description}
                </p>
              </div>

              {/* Radio indicator */}
              <div
                className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full border-2 transition-all duration-200 ${
                  isSelected ? `${method.borderColor} bg-current` : 'border-white/25'
                }`}
              >
                {isSelected && (
                  <div className="h-2 w-2 rounded-full bg-white" />
                )}
              </div>
            </button>
          )
        })}
      </div>

      {/* Pesapal note */}
      {paymentMethod === 'pesapal' && (
        <div className="mt-4 p-3 rounded-xl bg-violet-500/10 border border-violet-500/20 text-xs text-violet-300 flex items-start gap-2">
          <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          You'll be redirected to Pesapal's secure payment gateway to complete your transaction.
        </div>
      )}
      {paymentMethod === 'mpesa' && (
        <div className="mt-4 p-3 rounded-xl bg-green-500/10 border border-green-500/20 text-xs text-green-300 flex items-start gap-2">
          <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          An M-Pesa STK push will be sent to your phone number to complete payment.
        </div>
      )}
      {paymentMethod === 'cod' && (
        <div className="mt-4 p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs text-amber-300 flex items-start gap-2">
          <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Please have the exact amount ready. Our rider will collect payment on arrival.
        </div>
      )}
    </div>
  )
}

export default PaymentMethodSection
