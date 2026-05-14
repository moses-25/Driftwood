/**
 * PremiumButton — luxury CTA button
 *
 * Props:
 *   variant   – 'gold' | 'outline' | 'ghost' (default: 'gold')
 *   size      – 'sm' | 'md' | 'lg' (default: 'md')
 *   as        – 'button' | 'a' (default: 'button')
 *   href      – used when as='a'
 *   onClick   – click handler
 *   disabled  – boolean
 *   className – extra classes
 *   children  – button content
 */
export default function PremiumButton({
  variant = 'gold',
  size = 'md',
  as: Tag = 'button',
  href,
  onClick,
  disabled = false,
  className = '',
  children,
  type = 'button',
  ...rest
}) {
  const sizeClasses = {
    sm: 'px-5 py-2.5 text-xs',
    md: 'px-7 py-3 text-sm',
    lg: 'px-9 py-4 text-base',
  }

  const variantClasses = {
    gold: `
      bg-gradient-to-r from-caramel to-copper text-softwhite
      shadow-gold hover:shadow-gold-lg
      hover:-translate-y-0.5 active:translate-y-0
    `,
    outline: `
      bg-transparent text-caramel border border-caramel/60
      hover:bg-caramel/8 hover:-translate-y-0.5
    `,
    ghost: `
      bg-espresso/5 text-espresso border border-espresso/10
      hover:bg-espresso/10 hover:-translate-y-0.5
    `,
    'gold-dark': `
      bg-gradient-to-r from-caramel to-copper text-softwhite
      shadow-gold hover:shadow-gold-lg
      hover:-translate-y-0.5 active:translate-y-0
    `,
    'outline-light': `
      bg-transparent text-softwhite border border-softwhite/40
      hover:bg-softwhite/10 hover:-translate-y-0.5
    `,
  }

  const base = `
    inline-flex items-center justify-center gap-2
    rounded-full font-sans font-semibold tracking-wide
    transition-all duration-250 cursor-pointer
    disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none
  `

  const props = {
    className: `${base} ${sizeClasses[size] || sizeClasses.md} ${variantClasses[variant] || variantClasses.gold} ${className}`,
    onClick,
    disabled,
    ...(Tag === 'a' ? { href } : { type }),
    ...rest,
  }

  return <Tag {...props}>{children}</Tag>
}
