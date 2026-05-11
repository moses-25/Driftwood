const PAYMENT_METHODS = [
  {
    id: 'pesapal',
    label: 'Pesapal',
    description: 'Cards, mobile money & more',
    badge: 'Recommended',
    note: "You'll be redirected to Pesapal's secure payment gateway.",
    icon: (
      <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <rect x="2" y="5" width="20" height="14" rx="3" strokeWidth="2" />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2 10h20M6 15h4" />
      </svg>
    ),
  },
  {
    id: 'mpesa',
    label: 'M-Pesa',
    description: 'Pay via Safaricom M-Pesa',
    badge: 'Popular',
    note: 'An M-Pesa STK push will be sent to your phone number.',
    icon: (
      <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
      </svg>
    ),
  },
  {
    id: 'cod',
    label: 'Cash on Delivery',
    description: 'Pay when your order arrives',
    badge: null,
    note: 'Please have the exact amount ready for the rider.',
    icon: (
      <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
      </svg>
    ),
  },
]

const PaymentMethodSection = ({ paymentMethod, setPaymentMethod }) => {
  const active = PAYMENT_METHODS.find(m => m.id === paymentMethod)

  return (
    <div className="bg-white/6 rounded-2xl border border-white/10 p-6 md:p-8">
      <div className="flex items-center gap-3 mb-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-caramel/15 border border-caramel/25">
          <svg className="w-5 h-5 text-caramel" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
          </svg>
        </div>
        <div>
          <h3 className="text-lg font-bold text-white font-science-gothic">Payment Method</h3>
          <p className="text-sm text-white/40 font-tinos">Choose how you'd like to pay</p>
        </div>
      </div>

      <div className="space-y-3">
        {PAYMENT_METHODS.map((method) => {
          const isSelected = paymentMethod === method.id
          return (
            <button
              key={method.id}
              onClick={() => setPaymentMethod(method.id)}
              className={`group w-full flex items-center gap-4 p-4 rounded-xl border-2 text-left transition-all duration-250 ${
                isSelected ? 'border-caramel bg-caramel/10' : 'border-white/10 bg-white/4 hover:border-white/20 hover:bg-white/8'
              }`}
            >
              <div className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl transition-all duration-200 ${isSelected ? 'bg-caramel/20 text-caramel' : 'bg-white/8 text-white/40'}`}>
                {method.icon}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className={`font-semibold text-base font-science-gothic ${isSelected ? 'text-white' : 'text-white/70'}`}>
                    {method.label}
                  </span>
                  {method.badge && (
                    <span className={`text-xs font-medium px-2 py-0.5 rounded-full font-tinos ${isSelected ? 'bg-caramel/20 text-caramel' : 'bg-white/8 text-white/35'}`}>
                      {method.badge}
                    </span>
                  )}
                </div>
                <p className={`text-sm mt-0.5 font-tinos ${isSelected ? 'text-white/55' : 'text-white/30'}`}>
                  {method.description}
                </p>
              </div>
              <div className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full border-2 transition-all duration-200 ${isSelected ? 'border-caramel' : 'border-white/20'}`}>
                {isSelected && <div className="h-2 w-2 rounded-full bg-caramel" />}
              </div>
            </button>
          )
        })}
      </div>

      {active?.note && (
        <div className="mt-4 p-3 rounded-xl bg-white/5 border border-white/10 text-sm text-white/50 flex items-start gap-2 font-tinos">
          <svg className="w-4 h-4 shrink-0 mt-0.5 text-caramel" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {active.note}
        </div>
      )}
    </div>
  )
}

export default PaymentMethodSection
