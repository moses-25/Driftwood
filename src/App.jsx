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
import useSmoothScroll from './hooks/useSmoothScroll'
import { useRouter } from './hooks/useRouter'
import { CartProvider } from './context/CartContext'

function App() {
  useSmoothScroll()
  const { currentPath } = useRouter()

  const isCart = currentPath === '#cart'
  const isCheckout = currentPath === '#checkout'
  const isFullPage = isCart || isCheckout
  
  return (
    <CartProvider>
      <div className="font-sans min-h-full">
        <Navbar />
        
        {isCheckout ? (
          <Checkout />
        ) : isCart ? (
          <Cart />
        ) : (
          <main>
            <section id="home"><Hero /></section>
            <section id="about"><About /></section>
            <section id="menu"><Menu /></section>
            <section id="gallery"><Gallery /></section>
            <section id="reviews"><Reviews /></section>
            <section id="visit"><VisitUs /></section> 
          </main>
        )}
        
        {!isFullPage && <Footer />}
      </div>
    </CartProvider>
  )
}

export default App
