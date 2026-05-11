import FadeUp from '../animations/FadeUp'

/**
 * SectionTitle — reusable editorial heading block
 *
 * Props:
 *   eyebrow   – small uppercase label above the heading
 *   heading   – main heading text (can include JSX for italic/script words)
 *   subtext   – optional paragraph below the heading
 *   align     – 'center' | 'left' (default: 'center')
 *   light     – if true, renders on dark backgrounds (inverts colors)
 */
export default function SectionTitle({
  eyebrow,
  heading,
  subtext,
  align = 'center',
  light = false,
}) {
  const isCenter = align === 'center'

  return (
    <div className={`mb-14 ${isCenter ? 'text-center' : 'text-left'}`}>
      {eyebrow && (
        <FadeUp delay={0}>
          <div className={`flex items-center gap-3 mb-4 ${isCenter ? 'justify-center' : ''}`}>
            <span className="section-divider" />
            <p
              className={`text-xs uppercase tracking-[0.35em] font-semibold font-mono ${
                light ? 'text-caramel' : 'text-copper'
              }`}
            >
              {eyebrow}
            </p>
            <span className="section-divider rotate-180" />
          </div>
        </FadeUp>
      )}

      <FadeUp delay={0.1}>
        <h2
          className={`font-display text-4xl sm:text-5xl md:text-6xl leading-[1.1] tracking-tight max-w-3xl ${
            isCenter ? 'mx-auto' : ''
          } ${light ? 'text-softwhite' : 'text-espresso'}`}
        >
          {heading}
        </h2>
      </FadeUp>

      {subtext && (
        <FadeUp delay={0.2}>
          <pCF2E-A6A5
            className={`mt-5 text-base md:text-lg leading-relaxed max-w-2xl ${
              isCenter ? 'mx-auto' : ''
            } ${light ? 'text-warmbeige/80' : 'text-espresso/60'}`}
          >
            {subtext}
          </p>
        </FadeUp>
      )}
    </div>
  )
}
