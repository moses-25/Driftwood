import Cursor from './components/Cursor'
import Navbar from './components/Navbar'
import Hero from './pages/Hero'
import About from './pages/About'
import Menu from './pages/Menu'
import Gallery from './pages/Gallery'
import Reviews from './pages/Reviews'
import VisitUs from './pages/VisitUs'
import Footer from './pages/Footer'
import useSmoothScroll from './hooks/useSmoothScroll'

function App() {
  useSmoothScroll()
  
  return (
    <div className="font-sans min-h-full" style={{ cursor: 'none' }}>
      <Cursor />
      <Navbar />
      <main>
        <section id="home"><Hero /></section>
        <section id="about"><About /></section>
        <section id="menu"><Menu /></section>
        <section id="gallery"><Gallery /></section>
        <section id="reviews"><Reviews /></section>
        <section id="visit"><VisitUs /></section> 
      </main>
      <Footer />
    </div>
  )
}

export default App
