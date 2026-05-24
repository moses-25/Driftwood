export default function Hero() {
  return (
    <div id="home" className="relative w-full h-[60vh] md:h-screen md:max-h-[90vh] overflow-hidden pt-16 md:pt-20">

      {/* Background Video - full screen */}
      <div className="absolute inset-0 bg-black">
        <video
          src="/2.mp4"
          autoPlay
          loop
          muted
          playsInline
          preload="metadata"
          poster="/Driftwood.png"
          aria-hidden="true"
          className="w-full h-full object-cover md:scale-90"
          style={{
            maskImage: 'radial-gradient(ellipse at center, black 0%, black 30%, transparent 100%)',
            WebkitMaskImage: 'radial-gradient(ellipse at center, black 0%, black 30%, transparent 100%)'
          }}
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

    </div>
  )
}
