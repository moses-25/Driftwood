const EmptyCart = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 pt-24 pb-12">
      {/* Background Elements */}
      <div className="absolute -left-24 top-32 h-96 w-96 rounded-full bg-amber-500/10 blur-3xl" />
      <div className="absolute right-0 top-1/3 h-72 w-72 rounded-full bg-orange-500/8 blur-3xl" />
      
      <div className="relative max-w-4xl mx-auto px-6 text-center">
        {/* Breadcrumb */}
        <nav className="flex justify-center mb-8">
          <ol className="flex items-center space-x-2 text-sm text-slate-400">
            <li><a href="#home" className="hover:text-amber-300 transition-colors">Home</a></li>
            <li className="text-slate-600">/</li>
            <li><a href="#menu" className="hover:text-amber-300 transition-colors">Menu</a></li>
            <li className="text-slate-600">/</li>
            <li className="text-amber-300 font-medium">Cart</li>
          </ol>
        </nav>

        {/* Empty Cart Illustration */}
        <div className="bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 p-12 shadow-2xl mb-8">
          <div className="max-w-md mx-auto">
            {/* Coffee Cup Illustration */}
            <div className="w-32 h-32 mx-auto mb-8 relative">
              <div className="w-full h-full bg-gradient-to-br from-amber-500/20 to-orange-500/20 rounded-2xl border-2 border-dashed border-amber-500/30 flex items-center justify-center">
                <svg className="w-16 h-16 text-amber-500/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M8 6h8M9 3h6a2 2 0 0 1 2 2v0a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4v0a2 2 0 0 1 2-2z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M6 12h12v4a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2v-4z" />
                </svg>
              </div>
              {/* Floating elements */}
              <div className="absolute -top-2 -right-2 w-6 h-6 bg-amber-500/20 rounded-full animate-pulse" />
              <div className="absolute -bottom-2 -left-2 w-4 h-4 bg-orange-500/20 rounded-full animate-pulse delay-300" />
            </div>

            <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4 tracking-tight">
              Your Cart is <span className="text-amber-400">Empty</span>
            </h1>
            
            <p className="text-slate-300 text-lg mb-8 leading-relaxed">
              Looks like you haven't added any handcrafted delights yet. 
              Let's find something perfect for your taste.
            </p>

            {/* CTA Buttons */}
            <div className="space-y-4">
              <a
                href="#menu"
                className="inline-flex items-center justify-center gap-3 bg-gradient-to-r from-amber-500 to-orange-500 text-slate-900 font-bold py-4 px-8 rounded-2xl hover:from-amber-600 hover:to-orange-600 transition-all duration-200 transform hover:scale-105 shadow-[0_15px_35px_rgba(251,191,36,0.25)]"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
                Explore Our Menu
              </a>
              
              <div className="text-slate-400 text-sm">or</div>
              
              <a
                href="#specials"
                className="inline-flex items-center justify-center gap-2 bg-white/10 text-white font-semibold py-3 px-6 rounded-xl hover:bg-white/20 transition-all duration-200 border border-white/20"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 3l2.5 6.5L21 10l-5 4.5L17 21l-5-3.5L7 21l1-6.5L3 10l6.5-0.5L12 3z" />
                </svg>
                View Today's Specials
              </a>
            </div>
          </div>
        </div>

        {/* Popular Items Preview */}
        <div className="bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 p-8 shadow-2xl">
          <h3 className="text-2xl font-bold text-white mb-6">Popular Choices</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { name: 'Signature Latte', price: '$5.50', emoji: '☕' },
              { name: 'Iced Americano', price: '$4.25', emoji: '🧊' },
              { name: 'Chocolate Croissant', price: '$3.75', emoji: '🥐' }
            ].map((item, index) => (
              <div key={index} className="text-center p-4 bg-white/5 rounded-2xl border border-white/10 hover:bg-white/10 transition-all duration-200 group cursor-pointer">
                <div className="text-4xl mb-3 group-hover:scale-110 transition-transform duration-200">{item.emoji}</div>
                <h4 className="font-semibold text-white mb-1">{item.name}</h4>
                <p className="text-amber-300 font-medium">{item.price}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default EmptyCart