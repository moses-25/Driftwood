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
      <div className="relative z-10 flex flex-col items-center justify-center
        h-full text-center px-6">

        {/* Heading */}
        <h1 className="text-4xl md:text-6xl font-bold text-white mb-4 leading-tight">
          Experience the Perfect Brew
        </h1>

        {/* Subheading */}
        <p className="text-lg text-gray-200 mb-10 max-w-xl">
          A warm sanctuary where every cup tells a story.
          Crafted with care, served with love.
        </p>

        {/* CTA Buttons */}
        <div className="flex items-center gap-4 flex-wrap justify-center">
          <a
            href="#menu"
            className="bg-primary text-white px-8 py-3 rounded-lg
              font-medium hover:bg-orange-700 transition-colors"
          >
            View Menu
          </a>
          <a
            href="#visit"
            className="border-2 border-white text-white px-8 py-3
              rounded-lg font-medium hover:bg-white hover:text-gray-900
              transition-colors"
          >
            Reserve a Table
          </a>
        </div>
      </div>

      {/* Scroll Down Chevron */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 z-10
        animate-bounce">
        <a href="#about" aria-label="Scroll down">
          <svg
            className="w-8 h-8 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </a>
      </div>

    </div>
  )
}