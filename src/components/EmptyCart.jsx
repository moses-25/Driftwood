import { useRouter } from '../hooks/useRouter'

const EmptyCart = () => {
  const { navigate } = useRouter()

  const handleExploreMenu = (e) => {
    e.preventDefault()
    navigate('#home')
    setTimeout(() => {
      document.getElementById('menu')?.scrollIntoView({ behavior: 'smooth' })
    }, 80)
  }

  return (
    <div className="min-h-screen bg-black pt-24 pb-16">
      <div className="max-w-6xl mx-auto px-6">

        {/* Header */}
        <div className="text-center mb-12">
          <h1
            className="text-5xl md:text-6xl font-bold text-espresso mb-3"
            style={{ fontFamily: "'Science Gothic', sans-serif" }}
          >
            Shopping Cart
          </h1>
          <nav aria-label="Breadcrumb">
            <ol className="flex items-center justify-center gap-2 text-sm">
              <li>
                <button
                  onClick={() => navigate('#home')}
                  className="text-espresso/50 hover:text-caramel transition-colors"
                  style={{ fontFamily: "'Tinos', serif" }}
                >
                  Home
                </button>
              </li>
              <li className="text-espresso/30" aria-hidden="true">/</li>
              <li
                className="text-espresso/70 font-medium"
                style={{ fontFamily: "'Tinos', serif" }}
              >
                Shopping Cart
              </li>
            </ol>
          </nav>
        </div>

        {/* Empty state */}
        <div className="bg-white rounded-2xl shadow-soft p-16 text-center max-w-xl mx-auto">

          <div className="w-20 h-20 rounded-2xl bg-caramel/10 flex items-center justify-center mx-auto mb-6">
            <span className="text-5xl" aria-hidden="true">🛍️</span>
          </div>

          <h2
            className="text-3xl font-bold text-espresso mb-3"
            style={{ fontFamily: "'Science Gothic', sans-serif" }}
          >
            Your cart is empty
          </h2>

          <p
            className="text-espresso/55 text-base mb-8 leading-relaxed"
            style={{ fontFamily: "'Tinos', serif" }}
          >
            Looks like you haven't added anything yet. Explore our menu and find something you'll love.
          </p>

          <a
            href="#menu"
            onClick={handleExploreMenu}
            className="inline-flex items-center gap-2 bg-espresso hover:bg-caramel text-softwhite font-semibold py-3.5 px-8 rounded-xl transition-all duration-200 text-sm"
            style={{ fontFamily: "'Tinos', serif" }}
          >
            Explore Our Menu
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
            </svg>
          </a>
        </div>

      </div>
    </div>
  )
}

export default EmptyCart
