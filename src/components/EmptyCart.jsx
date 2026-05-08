import { useRouter } from '../hooks/useRouter'

const EmptyCart = () => {
  const { navigate } = useRouter()

  const handleExploreMenu = (e) => {
    e.preventDefault()
    // Navigate to home first so the main page mounts, then scroll to menu
    navigate('#home')
    setTimeout(() => {
      document.getElementById('menu')?.scrollIntoView({ behavior: 'smooth' })
    }, 80)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 pt-24 pb-12">
      {/* Enhanced Background Elements */}
      <div className="absolute -left-24 top-32 h-96 w-96 rounded-full bg-amber-500/15 blur-3xl animate-pulse" />
      <div className="absolute right-0 top-1/3 h-72 w-72 rounded-full bg-orange-500/12 blur-3xl animate-pulse delay-1000" />
      <div className="absolute left-1/2 bottom-32 h-64 w-64 rounded-full bg-amber-400/8 blur-3xl animate-pulse delay-500" />
      
      <div className="relative max-w-5xl mx-auto px-6 text-center">
        {/* Breadcrumb */}
        <nav className="flex justify-center mb-12" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-2 text-sm text-slate-400">
            <li>
              <button onClick={() => navigate('#home')} className="hover:text-amber-300 transition-colors">
                Home
              </button>
            </li>
            <li className="text-slate-600" aria-hidden="true">/</li>
            <li>
              <button onClick={handleExploreMenu} className="hover:text-amber-300 transition-colors">
                Menu
              </button>
            </li>
            <li className="text-slate-600" aria-hidden="true">/</li>
            <li className="text-amber-300 font-medium" aria-current="page">Cart</li>
          </ol>
        </nav>

        {/* Main Empty Cart Section */}
        <div className="bg-gradient-to-br from-white/8 to-white/4 backdrop-blur-xl rounded-3xl border border-white/15 p-12 md:p-16 shadow-2xl mb-8 relative overflow-hidden">
          {/* Decorative elements */}
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-amber-500 to-orange-500" />
          
          <div className="max-w-2xl mx-auto">
            {/* Enhanced Coffee Cup Illustration */}
            <div className="w-40 h-40 mx-auto mb-12 relative group">
              <div className="w-full h-full bg-gradient-to-br from-amber-500/25 to-orange-500/25 rounded-3xl border-2 border-dashed border-amber-400/40 flex items-center justify-center group-hover:scale-105 transition-transform duration-300">
                <svg className="w-20 h-20 text-amber-400/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M8 6h8M9 3h6a2 2 0 0 1 2 2v0a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4v0a2 2 0 0 1 2-2z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M6 12h12v4a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2v-4z" />
                </svg>
              </div>
              {/* Enhanced floating elements */}
              <div className="absolute -top-3 -right-3 w-8 h-8 bg-gradient-to-br from-amber-400 to-orange-400 rounded-full animate-bounce opacity-60" />
              <div className="absolute -bottom-3 -left-3 w-6 h-6 bg-gradient-to-br from-orange-400 to-amber-400 rounded-full animate-bounce delay-300 opacity-60" />
              <div className="absolute top-1/2 -right-6 w-4 h-4 bg-amber-300 rounded-full animate-pulse delay-700 opacity-40" />
            </div>

            <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-6 tracking-tight">
              Your Cart is <span className="bg-gradient-to-r from-amber-400 to-orange-400 bg-clip-text text-transparent">Empty</span>
            </h1>
            
            <p className="text-slate-200 text-xl md:text-2xl mb-4 leading-relaxed font-light">
              Looks like you haven't added any <span className="text-amber-300 font-medium">handcrafted delights</span> yet.
            </p>
            
            <p className="text-slate-300 text-lg mb-12 leading-relaxed">
              Let's find something perfect for your taste and start your coffee journey.
            </p>

            {/* Enhanced CTA Buttons */}
            <div className="space-y-6">
              <a
                href="#menu"
                onClick={handleExploreMenu}
                className="group inline-flex items-center justify-center gap-4 bg-gradient-to-r from-amber-500 to-orange-500 text-slate-900 font-bold py-5 px-10 rounded-2xl hover:from-amber-600 hover:to-orange-600 transition-all duration-300 transform hover:scale-105 shadow-[0_20px_40px_rgba(251,191,36,0.3)] hover:shadow-[0_25px_50px_rgba(251,191,36,0.4)] text-lg"
              >
                <svg className="w-6 h-6 group-hover:rotate-12 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
                Explore Our Menu
                <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default EmptyCart