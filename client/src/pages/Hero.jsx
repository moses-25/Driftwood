export default function Hero() {
  return (
    <div id="home" className="relative w-full h-screen overflow-hidden">

      {/* Background Video - two side by side to fill landscape screen */}
      <div className="absolute inset-0 flex flex-col md:flex-row bg-black">
        <video
          src="/wood.mp4"
          autoPlay
          loop
          muted
          playsInline
          preload="metadata"
          poster="/Driftwood.png"
          aria-hidden="true"
          className="w-full h-[60vh] md:h-full md:w-1/2 object-contain"
        />
        <video
          src="/2.mp4"
          autoPlay
          loop
          muted
          playsInline
          preload="metadata"
          poster="/Driftwood.png"
          aria-hidden="true"
          className="w-full h-[60vh] md:h-full md:w-1/2 object-contain"
        />
      </div>

      {/* Dark Overlay */}
      <div className="absolute inset-0 bg-black/45" />

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center justify-center h-full text-center px-6">
        
        {/* Overline */}
        <p className="text-sm md:text-base uppercase tracking-[0.3em] text-orange-400 mb-6 font-semibold font-oswald">
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
        <p className="text-lg md:text-xl text-slate-200 max-w-2xl leading-relaxed font-oswald font-normal">
          A warm sanctuary where every cup tells a story.<br />
          <span className="text-white font-bold">Crafted with care, served with love.</span>
        </p>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 z-10 flex flex-col items-center gap-2 animate-bounce">
        <span className="text-xs text-white/50 uppercase tracking-widest">Scroll</span>
        <svg className="w-5 h-5 text-white/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
        </svg>
      </div>

    </div>
  )
}
