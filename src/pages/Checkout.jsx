import { useState } from 'react'
import CheckoutProgress from '../components/checkout/CheckoutProgress'
import ContactSection from '../components/checkout/ContactSection'
import DeliveryMethodSection from '../components/checkout/DeliveryMethodSection'
import DeliveryAddressForm from '../components/checkout/DeliveryAddressForm'
import PaymentMethodSection from '../components/checkout/PaymentMethodSection'
import CheckoutOrderSummary from '../components/checkout/CheckoutOrderSummary'
import { useCart } from '../hooks/useCart'
import { useRouter } from '../hooks/useRouter'
import EmptyCart from '../components/EmptyCart'

const STEPS = ['Cart', 'Information', 'Payment', 'Confirmation']

const Checkout = () => {
  const { totalItems, clearCart } = useCart()
  const { navigate } = useRouter()
  const [currentStep, setCurrentStep] = useState(1) // 1=Information, 2=Payment, 3=Confirmation

  const [contact, setContact] = useState({ fullName: '', email: '', phone: '' })
  const [deliveryMethod, setDeliveryMethod] = useState('pickup')
  const [deliveryAddress, setDeliveryAddress] = useState({
    county: '',
    street: '',
    apartment: '',
    landmark: '',
    notes: '',
  })
  const [paymentMethod, setPaymentMethod] = useState('pesapal')
  const [errors, setErrors] = useState({})
  const [isPlacingOrder, setIsPlacingOrder] = useState(false)

  if (totalItems === 0 && currentStep !== 3) {
    return <EmptyCart />
  }

  const validateInformation = () => {
    const newErrors = {}
    if (!contact.fullName.trim()) newErrors.fullName = 'Full name is required'
    if (!contact.email.trim()) newErrors.email = 'Email address is required'
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact.email))
      newErrors.email = 'Enter a valid email address'
    if (!contact.phone.trim()) newErrors.phone = 'Phone number is required'
    if (deliveryMethod === 'delivery') {
      if (!deliveryAddress.county.trim()) newErrors.county = 'County/City is required'
      if (!deliveryAddress.street.trim()) newErrors.street = 'Street address is required'
    }
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleContinueToPayment = () => {
    if (validateInformation()) setCurrentStep(2)
  }

  const handlePlaceOrder = () => {
    setIsPlacingOrder(true)
    // Simulate async order placement — replace with real API call
    setTimeout(() => {
      setIsPlacingOrder(false)
      clearCart()
      setCurrentStep(3)
    }, 2000)
  }

  const handleBackToMenu = () => {
    navigate('#home')
    setTimeout(() => {
      document.getElementById('menu')?.scrollIntoView({ behavior: 'smooth' })
    }, 80)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 pt-24 pb-16 relative overflow-hidden">
      {/* Ambient background blobs */}
      <div className="pointer-events-none absolute -left-32 top-24 h-[500px] w-[500px] rounded-full bg-amber-500/8 blur-3xl" />
      <div className="pointer-events-none absolute right-0 top-1/2 h-80 w-80 rounded-full bg-orange-500/6 blur-3xl" />
      <div className="pointer-events-none absolute left-1/2 bottom-0 h-64 w-64 -translate-x-1/2 rounded-full bg-amber-600/5 blur-3xl" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6">
        {/* Page header */}
        <div className="text-center mb-10">
          <nav className="flex justify-center mb-5" aria-label="Breadcrumb">
            <ol className="flex items-center space-x-2 text-sm text-slate-400">
              <li>
                <button onClick={() => navigate('#home')} className="hover:text-amber-300 transition-colors">
                  Home
                </button>
              </li>
              <li className="text-slate-600" aria-hidden="true">/</li>
              <li>
                <button onClick={() => navigate('#cart')} className="hover:text-amber-300 transition-colors">
                  Cart
                </button>
              </li>
              <li className="text-slate-600" aria-hidden="true">/</li>
              <li className="text-amber-300 font-medium" aria-current="page">Checkout</li>
            </ol>
          </nav>
          <h1 className="text-4xl md:text-5xl font-extrabold text-white tracking-tight">
            Checkout
          </h1>
          <p className="mt-3 text-slate-400 text-base max-w-xl mx-auto">
            Complete your order in just a few steps. Your coffee is almost on its way.
          </p>
        </div>

        {/* Progress bar */}
        <CheckoutProgress steps={STEPS} currentStep={currentStep} />

        {currentStep === 3 ? (
          <ConfirmationScreen
            contact={contact}
            deliveryMethod={deliveryMethod}
            paymentMethod={paymentMethod}
            onBackToMenu={handleBackToMenu}
          />
        ) : (
          <div className="mt-10 grid grid-cols-1 lg:grid-cols-5 gap-8 items-start">
            {/* LEFT — Form */}
            <div className="lg:col-span-3 space-y-6">
              {currentStep === 1 && (
                <>
                  <ContactSection
                    contact={contact}
                    setContact={setContact}
                    errors={errors}
                  />
                  <DeliveryMethodSection
                    deliveryMethod={deliveryMethod}
                    setDeliveryMethod={setDeliveryMethod}
                  />
                  {deliveryMethod === 'delivery' && (
                    <DeliveryAddressForm
                      address={deliveryAddress}
                      setAddress={setDeliveryAddress}
                      errors={errors}
                    />
                  )}
                  <button
                    onClick={handleContinueToPayment}
                    className="w-full bg-gradient-to-r from-amber-500 to-orange-500 text-slate-900 font-bold py-4 px-6 rounded-2xl hover:from-amber-400 hover:to-orange-400 transition-all duration-200 hover:scale-[1.01] shadow-[0_10px_30px_rgba(251,191,36,0.25)] flex items-center justify-center gap-2 text-base"
                  >
                    Continue to Payment
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </button>
                </>
              )}

              {currentStep === 2 && (
                <>
                  <InfoReviewCard
                    contact={contact}
                    deliveryMethod={deliveryMethod}
                    deliveryAddress={deliveryAddress}
                    onEdit={() => setCurrentStep(1)}
                  />
                  <PaymentMethodSection
                    paymentMethod={paymentMethod}
                    setPaymentMethod={setPaymentMethod}
                  />
                  <button
                    onClick={handlePlaceOrder}
                    disabled={isPlacingOrder}
                    className="w-full bg-gradient-to-r from-amber-500 to-orange-500 text-slate-900 font-bold py-4 px-6 rounded-2xl hover:from-amber-400 hover:to-orange-400 transition-all duration-200 hover:scale-[1.01] shadow-[0_10px_30px_rgba(251,191,36,0.25)] flex items-center justify-center gap-2 text-base disabled:opacity-70 disabled:cursor-not-allowed disabled:scale-100"
                  >
                    {isPlacingOrder ? (
                      <>
                        <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                        </svg>
                        Placing Order…
                      </>
                    ) : (
                      <>
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                        </svg>
                        Place Order
                      </>
                    )}
                  </button>
                </>
              )}
            </div>

            {/* RIGHT — Sticky order summary */}
            <div className="lg:col-span-2 lg:sticky lg:top-24 lg:self-start">
              <CheckoutOrderSummary deliveryMethod={deliveryMethod} />
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

/* ── Inline sub-components ─────────────────────────────────────────── */

const InfoReviewCard = ({ contact, deliveryMethod, deliveryAddress, onEdit }) => (
  <div className="bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 p-6 shadow-2xl">
    <div className="flex items-center justify-between mb-4">
      <h3 className="text-lg font-semibold text-white">Your Information</h3>
      <button
        onClick={onEdit}
        className="text-amber-400 hover:text-amber-300 text-sm font-medium transition-colors flex items-center gap-1"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
        </svg>
        Edit
      </button>
    </div>
    <div className="space-y-2 text-sm text-slate-300">
      <div className="flex gap-2">
        <span className="text-slate-500 w-20 shrink-0">Name</span>
        <span className="text-white font-medium">{contact.fullName || '—'}</span>
      </div>
      <div className="flex gap-2">
        <span className="text-slate-500 w-20 shrink-0">Email</span>
        <span className="text-white font-medium">{contact.email || '—'}</span>
      </div>
      <div className="flex gap-2">
        <span className="text-slate-500 w-20 shrink-0">Phone</span>
        <span className="text-white font-medium">{contact.phone || '—'}</span>
      </div>
      <div className="flex gap-2">
        <span className="text-slate-500 w-20 shrink-0">Method</span>
        <span className="text-amber-300 font-medium capitalize">{deliveryMethod}</span>
      </div>
      {deliveryMethod === 'delivery' && deliveryAddress.street && (
        <div className="flex gap-2">
          <span className="text-slate-500 w-20 shrink-0">Address</span>
          <span className="text-white font-medium">
            {deliveryAddress.street}
            {deliveryAddress.apartment ? `, ${deliveryAddress.apartment}` : ''}, {deliveryAddress.county}
          </span>
        </div>
      )}
    </div>
  </div>
)

const ConfirmationScreen = ({ contact, deliveryMethod, paymentMethod, onBackToMenu }) => {
  const paymentLabels = { pesapal: 'Pesapal', mpesa: 'M-Pesa', cod: 'Cash on Delivery' }
  return (
    <div className="mt-10 max-w-xl mx-auto text-center">
      <div className="bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 p-10 shadow-2xl">
        <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br from-amber-500/20 to-orange-500/20 border border-amber-500/30">
          <svg className="w-10 h-10 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h2 className="text-3xl font-extrabold text-white mb-2">Order Confirmed!</h2>
        <p className="text-slate-400 mb-8">
          Thank you,{' '}
          <span className="text-amber-300 font-semibold">{contact.fullName || 'friend'}</span>!
          Your order has been received and is being prepared.
        </p>
        <div className="space-y-3 text-sm text-left bg-white/5 rounded-2xl p-5 border border-white/10 mb-8">
          <div className="flex justify-between">
            <span className="text-slate-400">Confirmation sent to</span>
            <span className="text-white font-medium">{contact.email || '—'}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Delivery method</span>
            <span className="text-amber-300 font-medium capitalize">{deliveryMethod}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Payment via</span>
            <span className="text-white font-medium">{paymentLabels[paymentMethod]}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Estimated time</span>
            <span className="text-white font-medium">
              {deliveryMethod === 'pickup' ? '15–20 min' : '30–45 min'}
            </span>
          </div>
        </div>
        <button
          onClick={onBackToMenu}
          className="inline-flex items-center gap-2 bg-gradient-to-r from-amber-500 to-orange-500 text-slate-900 font-bold py-3 px-8 rounded-2xl hover:from-amber-400 hover:to-orange-400 transition-all duration-200 hover:scale-[1.02] shadow-[0_10px_30px_rgba(251,191,36,0.25)]"
        >
          Back to Menu
        </button>
      </div>
    </div>
  )
}

export default Checkout
