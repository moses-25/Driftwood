import { useEffect, useRef } from 'react'
import Navbar from './components/Navbar'
import Hero from './pages/Hero'
import About from './pages/About'
import Menu from './pages/Menu'
import Gallery from './pages/Gallery'
import Reviews from './pages/Reviews'
import VisitUs from './pages/VisitUs'
import Footer from './pages/Footer'
import Cart from './pages/Cart'
import Checkout from './pages/Checkout'
import Cursor from './components/Cursor'
import useSmoothScroll from './hooks/useSmoothScroll'
import { useRouter } from './hooks/useRouter'
import { CartProvider } from './context/CartContext'

function AppContent() {
  useSmoothScroll()
  const { currentPath, isFullPage } = useRouter()

  const isCart = currentPath === '#cart'
  const isCheckout = currentPath === '#checkout'

  // When the main page mounts (after navigating away from cart/checkout),
  // scroll to the section that was requested via the hash.
  const pendingScrollRef = useRef(null)

  useEffect(() => {
    if (!isFullPage && pendingScrollRef.current) {
      const target = pendingScrollRef.current
      pendingScrollRef.current = null
      // Small delay so the sections have time to paint
      setTimeout(() => {
        const el = document.getElementById(target)
        if (el) el.scrollIntoView({ behavior: 'smooth' })
      }, 80)
    }
  }, [isFullPage])

  return (
    <div className="font-sans min-h-full bg-cream">
      <Cursor />
      <Navbar pendingScrollRef={pendingScrollRef} />

      {isCheckout ? (
        <Checkout />
      ) : isCart ? (
        <Cart />
      ) : (
        <main>
          <Hero />
          <About />
          <Menu />
          <Gallery />
          <Reviews />
          <VisitUs />
        </main>
      )}

      {!isCart && !isCheckout && <Footer />}
    </div>
  )
}

function App() {
  return (
    <CartProvider>
      <AppContent />
    </CartProvider>
  )
}

export default App
