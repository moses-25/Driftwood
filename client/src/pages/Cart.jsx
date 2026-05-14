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
    <div className="min-h-screen bg-black pt-24 pb-16">

      <div className="max-w-6xl mx-auto px-6">

        {/* ── Header ── */}
        <div className="text-center mb-10">
          <h1
            className="text-5xl md:text-6xl font-bold text-white mb-3 font-science-gothic"
          >
            Shopping Cart
          </h1>

          {/* Breadcrumb */}
          <nav aria-label="Breadcrumb">
            <ol className="flex items-center justify-center gap-2 text-base">
              <li>
                <button
                  onClick={() => navigate('#home')}
                  className="text-white/50 hover:text-caramel transition-colors font-tinos"
                >
                  Home
                </button>
              </li>
              <li className="text-white/30" aria-hidden="true">/</li>
              <li
                className="text-white/70 font-medium font-tinos"
                aria-current="page"
              >
                Shopping Cart
              </li>
            </ol>
          </nav>
        </div>

        {/* ── Main grid ── */}
        <div className="grid grid-cols-1 lg:grid-cols-[1fr_320px] gap-8 items-start">

          {/* Left — items table */}
          <div>
            {/* Table header */}
            <div className="grid grid-cols-[2fr_1fr_1fr_1fr] bg-caramel rounded-xl px-5 py-3 mb-1">
              {['Product', 'Price', 'Quantity', 'Subtotal'].map(h => (
                <span
                  key={h}
                  className="text-softwhite text-sm font-semibold text-center first:text-left font-tinos"
                >
                  {h}
                </span>
              ))}
            </div>

            {/* Items */}
            <div className="bg-white rounded-xl shadow-soft divide-y divide-warmbeige/60">
              {items.map((item) => (
                <CartItem key={item.cartItemId} item={item} />
              ))}
            </div>

            {/* Recommended */}
            <div className="mt-8">
              <RecommendedAddOns />
            </div>
          </div>

          {/* Right — order summary */}
          <div className="lg:sticky lg:top-24 lg:self-start">
            <OrderSummary />
          </div>

        </div>
      </div>
    </div>
  )
}

export default Cart
