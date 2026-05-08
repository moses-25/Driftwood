import { useCart } from '../hooks/useCart'
import { useRouter } from '../hooks/useRouter'
import CartItem from '../components/CartItem'
import OrderSummary from '../components/OrderSummary'
import RecommendedAddOns from '../components/RecommendedAddOns'
import EmptyCart from '../components/EmptyCart'

const Cart = () => {
  const { items, totalItems } = useCart()
  const { navigate } = useRouter()

  if (totalItems === 0) {
    return <EmptyCart />
  }

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 pt-24 pb-12 overflow-hidden">
      <div className="pointer-events-none absolute -left-24 top-32 h-96 w-96 rounded-full bg-amber-500/10 blur-3xl" />
      <div className="pointer-events-none absolute right-0 top-1/3 h-72 w-72 rounded-full bg-orange-500/8 blur-3xl" />

      <div className="relative max-w-7xl mx-auto px-6">
        {/* Breadcrumb */}
        <div className="text-center mb-12">
          <nav className="flex justify-center mb-6" aria-label="Breadcrumb">
            <ol className="flex items-center space-x-2 text-sm text-slate-400">
              <li>
                <button onClick={() => navigate('#home')} className="hover:text-amber-300 transition-colors">
                  Home
                </button>
              </li>
              <li className="text-slate-600" aria-hidden="true">/</li>
              <li>
                <button onClick={() => navigate('#menu')} className="hover:text-amber-300 transition-colors">
                  Menu
                </button>
              </li>
              <li className="text-slate-600" aria-hidden="true">/</li>
              <li className="text-amber-300 font-medium" aria-current="page">Cart</li>
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
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 p-6 shadow-2xl">
              <h3 className="text-xl font-semibold text-white mb-6">Order Items ({totalItems})</h3>
              <div className="space-y-4">
                {items.map((item) => (
                  <CartItem key={`${item.id}-${item.customizations?.size || 'default'}`} item={item} />
                ))}
              </div>
            </div>
            <RecommendedAddOns />
          </div>

          <div className="lg:sticky lg:top-24 lg:self-start">
            <OrderSummary />
          </div>
        </div>
      </div>
    </div>
  )
}

export default Cart