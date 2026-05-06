import heroVideo from '../assets/wood.mp4'
import heroVideo2 from '../assets/2.mp4'

export default function Hero() {
  return (
    <div className="relative w-full h-screen overflow-hidden">

      {/* Background Video - two side by side to fill landscape screen */}
      <div className="absolute inset-0 flex flex-col md:flex-row bg-black">
        <video src={heroVideo} autoPlay loop muted playsInline className="w-full h-1/2 md:h-full md:w-1/2 object-cover" />
        <video src={heroVideo2} autoPlay loop muted playsInline className="w-full h-1/2 md:h-full md:w-1/2 object-cover" />
      </div>

      {/* Dark Overlay */}
      <div className="absolute inset-0 bg-black/40" />

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center justify-center h-full text-center px-6">
        
        {/* Overline */}
        <p className="text-sm md:text-base uppercase tracking-[0.3em] text-orange-400 mb-6 font-semibold" style={{ fontFamily: 'Oswald, sans-serif' }}>
          Premium Coffee Experience
        </p>

        {/* Main Heading */}
        <h1 
          className="text-6xl md:text-8xl text-white mb-6 leading-[0.95] max-w-5xl drop-shadow-xl"
          style={{
            fontFamily: 'Bebas Neue, sans-serif',
            letterSpacing: '0.02em',
            textShadow: `
              -2px -2px 0 rgba(0, 0, 0, 0.4),
              2px -2px 0 rgba(0, 0, 0, 0.4),
              -2px 2px 0 rgba(0, 0, 0, 0.4),
              2px 2px 0 rgba(0, 0, 0, 0.4),
              -3px 0 2px rgba(249, 115, 22, 0.15),
              3px 0 2px rgba(249, 115, 22, 0.15)
            `,
            fontWeight: '400'
          }}
        >
          Experience the Perfect Brew
        </h1>

        {/* Subheading */}
        <p className="text-lg md:text-xl text-slate-200 max-w-2xl leading-relaxed" style={{ fontFamily: 'Oswald, sans-serif', fontWeight: '400' }}>
          A warm sanctuary where every cup tells a story.<br />
          <span className="text-white font-bold">Crafted with care, served with love.</span>
        </p>
      </div>

    </div>
  )
}