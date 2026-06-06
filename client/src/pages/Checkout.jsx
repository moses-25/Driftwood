import { useState, useEffect, useRef, useCallback } from 'react'
import CheckoutProgress from '../components/checkout/CheckoutProgress'
import ContactSection from '../components/checkout/ContactSection'
import DeliveryMethodSection from '../components/checkout/DeliveryMethodSection'
import DeliveryAddressForm from '../components/checkout/DeliveryAddressForm'
import PaymentMethodSection from '../components/checkout/PaymentMethodSection'
import CheckoutOrderSummary from '../components/checkout/CheckoutOrderSummary'
import { useCart } from '../hooks/useCart'
import { useAuth } from '../hooks/useAuth'
import { useRouter } from '../hooks/useRouter'
import { createOrder, queryPaymentStatus } from '../services/api'
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
  const [isProcessingPayment, setIsProcessingPayment] = useState(false)
  const [paymentError, setPaymentError] = useState('')
  const [paymentPolling, setPaymentPolling] = useState(false)
  const [paymentStatus, setPaymentStatus] = useState(null) // 'pending', 'paid', 'failed'
  const [paymentMessage, setPaymentMessage] = useState('')
  const pollingRef = useRef(null)
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
      const orderItems = items
        .filter(item => typeof item.id === 'number')
        .map(item => ({
          product_id: item.id,
          quantity: item.quantity,
          customizations: item.customizations || {},
        }))
      
      const skippedItems = items.filter(item => typeof item.id !== 'number')
      if (skippedItems.length > 0) {
        setOrderError(
          `"${skippedItems.map(i => i.name).join(', ')}" can't be ordered online. They've been skipped.`
        )
      }
      
      if (orderItems.length === 0) {
        throw new Error('None of the items in your cart can be ordered online.')
      }
      
      const deliveryFee = deliveryMethod === 'delivery' ? 399 : 0
      
      const orderData = {
        items: orderItems,
        order_type: deliveryMethod,
        payment_method: paymentMethod,
        // Don't send total_amount - let backend calculate from database prices
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
      setCurrentStep(3) // Go to confirmation screen
    } catch (err) {
      if (cancelledRef.current) return
      setOrderError(err.message || 'Failed to place order')
    } finally {
      if (!cancelledRef.current) setIsPlacingOrder(false)
    }
  }

  const pollMpesaStatus = useCallback(async (checkoutRequestId) => {
    try {
      const result = await queryPaymentStatus(checkoutRequestId)
      if (cancelledRef.current) return

      if (result.success && result.data) {
        const status = result.data.status
        if (status === 'completed') {
          setPaymentStatus('paid')
          setPaymentMessage('Payment completed successfully!')
          setPaymentPolling(false)
          clearInterval(pollingRef.current)
        } else if (result.data.result_code && result.data.result_code !== '0') {
          setPaymentStatus('failed')
          setPaymentMessage(result.data.result_desc || 'Payment failed. Please try again.')
          setPaymentPolling(false)
          clearInterval(pollingRef.current)
        }
      }
    } catch {
      // Ignore polling errors — just retry on next interval
    }
  }, [])

  const handleProcessPayment = async () => {
    if (!orderResult) return
    
    setIsProcessingPayment(true)
    setPaymentError('')
    
    try {
      if (paymentMethod === 'mpesa') {
        const { initiateMpesaPayment } = await import('../services/api')
        
        const paymentData = {
          order_id: orderResult.id,
          phone_number: contact.phone
        }
        
        const result = await initiateMpesaPayment(paymentData)
        
        if (result.success) {
          setPaymentError('')
          setPaymentStatus('pending')
          setPaymentMessage('Payment initiated! Check your phone to complete the M-Pesa STK push.')
          setPaymentPolling(true)
          
          // Start polling for payment status
          const checkoutRequestId = result.data?.checkout_request_id
          if (checkoutRequestId) {
            pollingRef.current = setInterval(() => {
              pollMpesaStatus(checkoutRequestId)
            }, 3000)
            
            // Stop polling after 90 seconds
            setTimeout(() => {
              if (pollingRef.current) {
                clearInterval(pollingRef.current)
                pollingRef.current = null
                setPaymentPolling(false)
                if (paymentStatus !== 'paid' && paymentStatus !== 'failed') {
                  setPaymentMessage('Payment confirmation timed out. Check your M-Pesa messages and contact support if needed.')
                  setPaymentStatus('failed')
                }
              }
            }, 90000)
          }
        } else {
          setPaymentError(result.error || 'Failed to initiate payment')
        }
      } else {
        setPaymentError('')
        setPaymentMessage('Cash payment - Pay on delivery')
      }
    } catch (err) {
      setPaymentError(err.message || 'Failed to process payment')
    } finally {
      setIsProcessingPayment(false)
    }
  }

  // Cleanup polling on unmount
  useEffect(() => {
    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current)
    }
  }, [])

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
          <ConfirmationScreen 
            contact={contact} 
            deliveryMethod={deliveryMethod} 
            paymentMethod={paymentMethod} 
            orderResult={orderResult} 
            onBackToMenu={handleBackToMenu}
            onProcessPayment={handleProcessPayment}
            isProcessingPayment={isProcessingPayment}
            paymentError={paymentError}
            paymentPolling={paymentPolling}
            paymentStatus={paymentStatus}
            paymentMessage={paymentMessage}
          />
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

const ConfirmationScreen = ({ contact, deliveryMethod, paymentMethod, orderResult, onBackToMenu, onProcessPayment, isProcessingPayment, paymentError, paymentPolling, paymentStatus, paymentMessage }) => {
  const paymentLabels = { mpesa: 'M-Pesa', cash: 'Cash on Delivery' }
  const orderNumber = orderResult?.order_number || ''
  const estimatedTime = orderResult?.estimated_ready_time
    ? new Date(orderResult.estimated_ready_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    : deliveryMethod === 'pickup' ? '15–20 min' : '30–45 min'
  
  const isPaid = paymentStatus === 'paid' || orderResult?.payment_status === 'paid'
  const isPending = paymentStatus === 'pending' || orderResult?.payment_status === 'pending'
  
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

        {/* Payment Section */}
        {paymentMethod === 'mpesa' && !isPaid && !paymentPolling && paymentStatus !== 'failed' && (
          <div className="mb-6">
            <div className="bg-caramel/10 border border-caramel/30 rounded-xl p-5 mb-4">
              <div className="flex items-center gap-3 mb-3">
                <svg className="w-5 h-5 text-caramel" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <h3 className="text-white font-bold text-lg font-science-gothic">Complete Payment</h3>
              </div>
              <p className="text-white/60 text-sm mb-4 font-tinos">
                Click below to receive an M-Pesa STK push on your phone ({contact.phone})
              </p>
              <button
                onClick={onProcessPayment}
                disabled={isProcessingPayment}
                className="w-full bg-caramel hover:bg-copper text-white font-bold py-3 px-6 rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 font-tinos"
              >
                {isProcessingPayment ? (
                  <>
                    <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                    </svg>
                    Pay with M-Pesa
                  </>
                )}
              </button>
              {paymentError && (
                <p className="text-red-400 text-sm mt-3">{paymentError}</p>
              )}
            </div>
          </div>
        )}

        {/* M-Pesa polling in progress */}
        {paymentPolling && paymentStatus === 'pending' && (
          <div className="mb-6">
            <div className="bg-caramel/10 border border-caramel/30 rounded-xl p-5">
              <div className="flex items-center gap-3 mb-3">
                <svg className="animate-spin h-5 w-5 text-caramel" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <h3 className="text-white font-bold text-lg font-science-gothic">Waiting for Payment</h3>
              </div>
              <p className="text-white/60 text-sm font-tinos">{paymentMessage}</p>
            </div>
          </div>
        )}

        {/* M-Pesa payment failed */}
        {paymentStatus === 'failed' && !paymentPolling && (
          <div className="mb-6">
            <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-5">
              <div className="flex items-center gap-3 mb-3">
                <svg className="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <h3 className="text-white font-bold text-lg font-science-gothic">Payment Failed</h3>
              </div>
              <p className="text-white/60 text-sm mb-4 font-tinos">{paymentMessage || 'Payment did not go through. Please try again.'}</p>
              <button
                onClick={onProcessPayment}
                disabled={isProcessingPayment}
                className="w-full bg-caramel hover:bg-copper text-white font-bold py-3 px-6 rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 font-tinos"
              >
                {isProcessingPayment ? (
                  <>
                    <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Retrying...
                  </>
                ) : (
                  <>Retry Payment</>
                )}
              </button>
            </div>
          </div>
        )}

        {paymentMethod === 'cash' && (
          <div className="mb-6 bg-green-500/10 border border-green-500/30 rounded-xl p-4">
            <div className="flex items-center gap-2 justify-center text-green-400">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
              </svg>
              <span className="font-semibold font-tinos">Cash payment - Pay on delivery</span>
            </div>
          </div>
        )}

        {isPaid && (
          <div className="mb-6 bg-green-500/10 border border-green-500/30 rounded-xl p-4">
            <div className="flex items-center gap-2 justify-center text-green-400">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
              </svg>
              <span className="font-semibold font-tinos">Payment completed successfully!</span>
            </div>
          </div>
        )}

        <button onClick={onBackToMenu} className="inline-flex items-center gap-2 bg-white hover:bg-caramel text-espresso hover:text-white font-bold py-3 px-8 rounded-xl transition-all duration-200 text-base font-tinos">
          Back to Menu
        </button>
      </div>
    </div>
  )
}

export default Checkout
