import { useState, useEffect, useRef } from 'react'
import CheckoutProgress from '../components/checkout/CheckoutProgress'
import ContactSection from '../components/checkout/ContactSection'
import DeliveryMethodSection from '../components/checkout/DeliveryMethodSection'
import DeliveryAddressForm from '../components/checkout/DeliveryAddressForm'
import PaymentMethodSection from '../components/checkout/PaymentMethodSection'
import CheckoutOrderSummary from '../components/checkout/CheckoutOrderSummary'
import { useCart } from '../hooks/useCart'
import { useAuth } from '../hooks/useAuth'
import { useRouter } from '../hooks/useRouter'
import { createOrder } from '../services/api'
import { parsePrice } from '../utils/price'
import EmptyCart from '../components/EmptyCart'

const STEPS = ['Cart', 'Information', 'Payment', 'Confirmation']

const Checkout = () => {
  const { items, totalItems, clearCart } = useCart()
  const { navigate } = useRouter()
  const [currentStep, setCurrentStep] = useState(1)

  const [contact, setContact] = useState({ fullName: '', email: '', phone: '' })
  const [deliveryMethod, setDeliveryMethod] = useState('pickup')
  const [deliveryAddress, setDeliveryAddress] = useState({ county: '', street: '', apartment: '', landmark: '', notes: '' })
  const [paymentMethod, setPaymentMethod] = useState('mpesa')
  const [errors, setErrors] = useState({})
  const [isPlacingOrder, setIsPlacingOrder] = useState(false)
  const [orderResult, setOrderResult] = useState(null)
  const [orderError, setOrderError] = useState('')
  const { user } = useAuth()
  const cancelledRef = useRef(false)

  useEffect(() => {
    return () => { cancelledRef.current = true }
  }, [])

  if (totalItems === 0 && currentStep !== 3 && !orderResult) return <EmptyCart />

  const validateInformation = () => {
    const newErrors = {}
    if (!contact.fullName.trim()) newErrors.fullName = 'Full name is required'
    if (!contact.email.trim()) newErrors.email = 'Email address is required'
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact.email)) newErrors.email = 'Enter a valid email address'
    if (!contact.phone.trim()) newErrors.phone = 'Phone number is required'
    if (deliveryMethod === 'delivery') {
      if (!deliveryAddress.county.trim()) newErrors.county = 'County/City is required'
      if (!deliveryAddress.street.trim()) newErrors.street = 'Street address is required'
    }
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleContinueToPayment = () => { if (validateInformation()) setCurrentStep(2) }

  const handlePlaceOrder = async () => {
    setIsPlacingOrder(true)
    setOrderError('')
    try {
      const orderItems = items.map(item => ({
        product_id: item.id,
        quantity: item.quantity,
        customizations: item.customizations || {},
      }))
      const total = items.reduce((s, i) => s + parsePrice(i.price) * i.quantity, 0)
      const deliveryFee = deliveryMethod === 'delivery' ? 399 : 0
      
      const orderData = {
        items: orderItems,
        order_type: deliveryMethod,
        payment_method: paymentMethod === 'mpesa' ? 'mpesa' : 'cash',
        customer_name: contact.fullName,
        customer_email: contact.email,
        customer_phone: contact.phone,
        delivery_address: deliveryMethod === 'delivery'
          ? `${deliveryAddress.street}${deliveryAddress.apartment ? `, ${deliveryAddress.apartment}` : ''}, ${deliveryAddress.county}`
          : undefined,
        delivery_instructions: deliveryAddress.notes || undefined,
        delivery_fee: deliveryFee || undefined,
      }
      
      const result = await createOrder(orderData)
      if (cancelledRef.current) return
      setOrderResult(result.data)
      clearCart()
      setCurrentStep(3)
    } catch (err) {
      if (cancelledRef.current) return
      setOrderError(err.message || 'Failed to place order')
    } finally {
      if (!cancelledRef.current) setIsPlacingOrder(false)
    }
  }

  const handleBackToMenu = () => {
    navigate('#home')
    setTimeout(() => { document.getElementById('menu')?.scrollIntoView({ behavior: 'smooth' }) }, 80)
  }

  const btnClass = `w-full bg-white hover:bg-caramel text-espresso hover:text-white font-bold py-4 px-6 rounded-xl transition-all duration-200 flex items-center justify-center gap-2 text-base`

  return (
    <div className="min-h-screen bg-black pt-24 pb-16">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">

        {/* Header */}
        <div className="text-center mb-10">
          <nav className="flex justify-center mb-4" aria-label="Breadcrumb">
            <ol className="flex items-center gap-2 text-base font-tinos">
              <li><button onClick={() => navigate('#home')} className="text-white/40 hover:text-caramel transition-colors">Home</button></li>
              <li className="text-white/20">/</li>
              <li><button onClick={() => navigate('#cart')} className="text-white/40 hover:text-caramel transition-colors">Cart</button></li>
              <li className="text-white/20">/</li>
              <li className="text-white/70" aria-current="page">Checkout</li>
            </ol>
          </nav>
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-2 font-science-gothic">
            Checkout
          </h1>
          <p className="text-white/50 text-base max-w-md mx-auto font-tinos">
            Complete your order in just a few steps.
          </p>
        </div>

        {/* Progress */}
        <CheckoutProgress steps={STEPS} currentStep={currentStep} />

        {currentStep === 3 || orderResult ? (
          <ConfirmationScreen contact={contact} deliveryMethod={deliveryMethod} paymentMethod={paymentMethod} orderResult={orderResult} onBackToMenu={handleBackToMenu} />
        ) : (
          <div className="mt-10 grid grid-cols-1 lg:grid-cols-5 gap-8 items-start">
            <div className="lg:col-span-3 space-y-5">
              {currentStep === 1 && (
                <>
                  <ContactSection contact={contact} setContact={setContact} errors={errors} />
                  <DeliveryMethodSection deliveryMethod={deliveryMethod} setDeliveryMethod={setDeliveryMethod} />
                  {deliveryMethod === 'delivery' && (
                    <DeliveryAddressForm address={deliveryAddress} setAddress={setDeliveryAddress} errors={errors} />
                  )}
                  <button onClick={handleContinueToPayment} className={`${btnClass} font-tinos`}>
                    Continue to Payment
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </button>
                </>
              )}
              {currentStep === 2 && (
                <>
                  <InfoReviewCard contact={contact} deliveryMethod={deliveryMethod} deliveryAddress={deliveryAddress} onEdit={() => setCurrentStep(1)} />
                  <PaymentMethodSection paymentMethod={paymentMethod} setPaymentMethod={setPaymentMethod} />
                  {orderError && <p className="text-red-400 text-sm text-center">{orderError}</p>}
                  <button onClick={handlePlaceOrder} disabled={isPlacingOrder} className={`${btnClass} font-tinos disabled:opacity-60 disabled:cursor-not-allowed`}>
                    {isPlacingOrder ? (
                      <><svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" /><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" /></svg>Placing Order…</>
                    ) : (
                      <><svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>Place Order</>
                    )}
                  </button>
                </>
              )}
            </div>
            <div className="lg:col-span-2 lg:sticky lg:top-24 lg:self-start">
              <CheckoutOrderSummary deliveryMethod={deliveryMethod} />
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

const InfoReviewCard = ({ contact, deliveryMethod, deliveryAddress, onEdit }) => (
  <div className="bg-white/6 rounded-2xl border border-white/10 p-6">
    <div className="flex items-center justify-between mb-4">
      <h3 className="text-base font-bold text-white font-science-gothic">Your Information</h3>
      <button onClick={onEdit} className="text-caramel hover:text-white text-sm font-medium transition-colors flex items-center gap-1 font-tinos">
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
        Edit
      </button>
    </div>
    <div className="space-y-2 text-base font-tinos">
      {[['Name', contact.fullName], ['Email', contact.email], ['Phone', contact.phone], ['Method', deliveryMethod]].map(([label, val]) => (
        <div key={label} className="flex gap-3">
          <span className="text-white/35 w-16 shrink-0">{label}</span>
          <span className="text-white font-medium capitalize">{val || '—'}</span>
        </div>
      ))}
      {deliveryMethod === 'delivery' && deliveryAddress.street && (
        <div className="flex gap-3">
          <span className="text-white/35 w-16 shrink-0">Address</span>
          <span className="text-white font-medium">{deliveryAddress.street}{deliveryAddress.apartment ? `, ${deliveryAddress.apartment}` : ''}, {deliveryAddress.county}</span>
        </div>
      )}
    </div>
  </div>
)

const ConfirmationScreen = ({ contact, deliveryMethod, paymentMethod, orderResult, onBackToMenu }) => {
  const paymentLabels = { mpesa: 'M-Pesa', cash: 'Cash on Delivery' }
  const orderNumber = orderResult?.order_number || ''
  const estimatedTime = orderResult?.estimated_ready_time
    ? new Date(orderResult.estimated_ready_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    : deliveryMethod === 'pickup' ? '15–20 min' : '30–45 min'
  return (
    <div className="mt-10 max-w-xl mx-auto text-center">
      <div className="bg-white/6 rounded-2xl border border-white/10 p-10">
        <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-caramel/20 border border-caramel/30">
          <svg className="w-10 h-10 text-caramel" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h2 className="text-4xl font-bold text-white mb-2 font-science-gothic">Order Confirmed!</h2>
        <p className="text-white/60 mb-8 text-base font-tinos">
          Thank you, <span className="text-caramel font-semibold">{contact.fullName || 'friend'}</span>! Your order is being prepared.
        </p>
        {orderNumber && (
          <p className="text-white/40 text-sm font-mono mb-6">
            Order #{orderNumber}
          </p>
        )}
        <div className="space-y-3 text-base text-left bg-white/5 rounded-xl p-5 border border-white/10 mb-8 font-tinos">
          {[
            ['Confirmation sent to', contact.email || '—'],
            ['Delivery method', deliveryMethod],
            ['Payment via', paymentLabels[paymentMethod] || paymentMethod],
            ['Estimated time', estimatedTime],
          ].map(([label, val]) => (
            <div key={label} className="flex justify-between">
              <span className="text-white/40">{label}</span>
              <span className="text-white font-medium capitalize">{val}</span>
            </div>
          ))}
        </div>
        <button onClick={onBackToMenu} className="inline-flex items-center gap-2 bg-white hover:bg-caramel text-espresso hover:text-white font-bold py-3 px-8 rounded-xl transition-all duration-200 text-base font-tinos">
          Back to Menu
        </button>
      </div>
    </div>
  )
}

export default Checkout
