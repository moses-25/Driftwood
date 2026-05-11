export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Driftwood Luxury Palette
        espresso:    '#3B2416',
        darkroast:   '#1E1A17',
        caramel:     '#C58A46',
        warmbeige:   '#E8D8C8',
        cream:       '#F8F3EE',
        copper:      '#A45A3A',
        softwhite:   '#FFFDF9',
        // Legacy aliases
        primary:     '#C58A46',
      },
      fontFamily: {
        serif:   ['Cormorant Garamond', 'Playfair Display', 'Georgia', 'serif'],
        display: ['Playfair Display', 'Cormorant Garamond', 'Georgia', 'serif'],
        sans:    ['Inter', 'Poppins', 'system-ui', 'sans-serif'],
        mono:    ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
        '6xl': '3rem',
      },
      boxShadow: {
        'luxury':    '0 25px 80px rgba(59,36,22,0.18), 0 8px 24px rgba(59,36,22,0.10)',
        'card':      '0 20px 60px rgba(30,26,23,0.22), 0 4px 16px rgba(30,26,23,0.12)',
        'gold':      '0 8px 32px rgba(197,138,70,0.28)',
        'gold-lg':   '0 16px 48px rgba(197,138,70,0.32)',
        'soft':      '0 4px 24px rgba(59,36,22,0.08)',
        'inner-top': 'inset 0 2px 8px rgba(59,36,22,0.12)',
      },
      backgroundImage: {
        'grain':         "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E\")",
        'cream-gradient': 'linear-gradient(135deg, #FFFDF9 0%, #F8F3EE 50%, #E8D8C8 100%)',
        'dark-gradient':  'linear-gradient(135deg, #1E1A17 0%, #3B2416 100%)',
        'gold-gradient':  'linear-gradient(135deg, #C58A46 0%, #A45A3A 100%)',
      },
      keyframes: {
        fadeIn: {
          '0%':   { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        shimmer: {
          '0%':   { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        floatY: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%':      { transform: 'translateY(-8px)' },
        },
      },
      animation: {
        fadeIn:  'fadeIn 0.5s ease-out',
        shimmer: 'shimmer 2.5s linear infinite',
        floatY:  'floatY 4s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
