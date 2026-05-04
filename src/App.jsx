import { BrowserRouter as Router } from 'react-router-dom'
import Navbar from './components/Navbar'
import Hero from './pages/Hero'
import About from './pages/About'
import Menu from './pages/Menu'
import Gallery from './pages/Gallery'
import Reviews from './pages/Reviews'
import VisitUs from './pages/VisitUs'
import Footer from './pages/Footer'

function App() {
  return (
    <Router>
      <div className="font-sans">
        <Navbar />
        <main>
          <Hero />
          <About />
          <Menu />
          <Gallery />
          <Reviews />
          <VisitUs />
        </main>
        <Footer />
      </div>
    </Router>
  )
}

export default App