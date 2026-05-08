import { useState } from 'react'
import PrivacyPolicyModal from '../components/PrivacyPolicyModal'
import TermsOfServiceModal from '../components/TermsOfServiceModal'

const quickLinks = [
  { label: 'Home', href: '#home' },
  { label: 'About Us', href: '#about' },
  { label: 'Menu', href: '#menu' },
  { label: 'Gallery', href: '#gallery' },
  { label: 'Reviews', href: '#reviews' },
  { label: 'Contact', href: '#visit' },
]

const contactInfo = [
  {
    icon: (
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    ),
    text: '123 Coffee Street, Brewville, CA 90210',
    href: 'https://maps.google.com/?q=123+Coffee+Street+Brewville+CA+90210',
  },
  {
    icon: (
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
      </svg>
    ),
    text: '(555) 123-4567',
    href: 'tel:+15551234567',
  },
  {
    icon: (
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
      </svg>
    ),
    text: 'hello@driftwoodcafe.com',
    href: 'mailto:hello@driftwoodcafe.com',
  },
]

const socials = [
  {
    label: 'Facebook',
    href: '#',
    icon: (
      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
        <path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z" />
      </svg>
    ),
  },
  {
    label: 'Instagram',
    href: '#',
    icon: (
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <rect x="2" y="2" width="20" height="20" rx="5" ry="5" strokeWidth={2} />
        <circle cx="12" cy="12" r="4" strokeWidth={2} />
        <circle cx="17.5" cy="6.5" r="1" fill="currentColor" strokeWidth={0} />
      </svg>
    ),
  },
  {
    label: 'Twitter',
    href: '#',
    icon: (
      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
        <path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z" />
      </svg>
    ),
  },
  {
    label: 'Pinterest',
    href: '#',
    icon: (
      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
        <path d="M12 0C5.373 0 0 5.373 0 12c0 5.084 3.163 9.426 7.627 11.174-.105-.949-.2-2.405.042-3.441.218-.937 1.407-5.965 1.407-5.965s-.359-.719-.359-1.782c0-1.668.967-2.914 2.171-2.914 1.023 0 1.518.769 1.518 1.69 0 1.029-.655 2.568-.994 3.995-.283 1.194.599 2.169 1.777 2.169 2.133 0 3.772-2.249 3.772-5.495 0-2.873-2.064-4.882-5.012-4.882-3.414 0-5.418 2.561-5.418 5.207 0 1.031.397 2.138.893 2.738a.36.36 0 01.083.345l-.333 1.36c-.053.22-.174.267-.402.161-1.499-.698-2.436-2.889-2.436-4.649 0-3.785 2.75-7.262 7.929-7.262 4.163 0 7.398 2.967 7.398 6.931 0 4.136-2.607 7.464-6.227 7.464-1.216 0-2.359-.632-2.75-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0z" />
      </svg>
    ),
  },
]

export default function Footer() {
  const [email, setEmail] = useState('')
  const [subStatus, setSubStatus] = useState('idle') // idle | loading | success | error
  const [showPrivacy, setShowPrivacy] = useState(false)
  const [showTerms, setShowTerms] = useState(false)

  const handleSubscribe = async () => {
    if (!email) return
    setSubStatus('loading')

    try {
      const res = await fetch('http://localhost:5000/api/newsletter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      })

      if (!res.ok) throw new Error('Failed')

      setSubStatus('success')
      setEmail('')
    } catch {
      setSubStatus('error')
    }
  }

  const scrollToTop = () => window.scrollTo({ top: 0, behavior: 'smooth' })

  return (
    <>
    <footer className="relative bg-slate-900 border-t border-white/10">

      {/* Main Footer Content */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-12">

          {/* Column 1 - Brand */}
          <div className="flex flex-col gap-5">
            <div>
              <span className="text-xl font-bold">
                <span className="text-primary">Driftwood</span>
                <span className="text-white"> Café</span>
              </span>
              <p className="text-slate-400 text-sm mt-3 leading-relaxed">
                Crafting exceptional coffee experiences since 2026. Our
                mission is to create a sanctuary where quality meets comfort.
              </p>
            </div>

            {/* Socials */}
            <div className="flex items-center gap-3">
              {socials.map((social) => (
                <a
                  key={social.label}
                  href={social.href}
                  aria-label={social.label}
                  className="h-9 w-9 rounded-full border border-white/10
                    bg-white/5 flex items-center justify-center text-slate-400
                    hover:text-amber-400 hover:border-amber-500/30
                    hover:bg-amber-500/10 transition-all duration-200"
                >
                  {social.icon}
                </a>
              ))}
            </div>
          </div>

          {/* Column 2 - Quick Links */}
          <div>
            <h4 className="text-white font-semibold text-sm uppercase
              tracking-wider mb-5">
              Quick Links
            </h4>
            <ul className="flex flex-col gap-3">
              {quickLinks.map((link) => (
                <li key={link.label}>
                  <a
                    href={link.href}
                    className="text-slate-400 text-sm hover:text-amber-400
                      transition-colors"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 3 - Contact Info */}
          <div>
            <h4 className="text-white font-semibold text-sm uppercase
              tracking-wider mb-5">
              Contact Info
            </h4>
            <ul className="flex flex-col gap-4">
              {contactInfo.map((item) => (
                <li key={item.text} className="flex items-start gap-3">
                  <span className="text-amber-400 mt-0.5 flex-shrink-0">
                    {item.icon}
                  </span>
                  <a
                    href={item.href}
                    target={item.href.startsWith('http') ? '_blank' : undefined}
                    rel={item.href.startsWith('http') ? 'noopener noreferrer' : undefined}
                    className="text-slate-400 text-sm leading-relaxed hover:text-amber-400 transition-colors"
                  >
                    {item.text}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 4 - Newsletter */}
          <div>
            <h4 className="text-white font-semibold text-sm uppercase
              tracking-wider mb-5">
              Newsletter
            </h4>
            <p className="text-slate-400 text-sm mb-4 leading-relaxed">
              Subscribe to get special offers, free giveaways, and
              once-in-a-lifetime deals.
            </p>

            <div className="flex flex-col gap-3">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Your email address"
                className="w-full bg-slate-800/60 border border-white/10
                  rounded-xl px-4 py-3 text-white text-sm placeholder-slate-500
                  focus:outline-none focus:border-amber-500/50
                  focus:ring-1 focus:ring-amber-500/30 transition-colors"
              />
              <button
                onClick={handleSubscribe}
                disabled={subStatus === 'loading'}
                className="w-full bg-primary hover:bg-orange-700
                  disabled:opacity-50 disabled:cursor-not-allowed
                  text-white font-medium py-3 rounded-xl
                  transition-colors duration-200 text-sm"
              >
                {subStatus === 'loading' ? 'Subscribing...' : 'Subscribe'}
              </button>

              {subStatus === 'success' && (
                <p className="text-green-400 text-xs text-center">
                  ✓ You're subscribed!
                </p>
              )}
              {subStatus === 'error' && (
                <p className="text-red-400 text-xs text-center">
                  Something went wrong. Try again.
                </p>
              )}
            </div>
          </div>

        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-white/5">
        <div className="max-w-6xl mx-auto px-6 py-5 flex flex-col sm:flex-row
          items-center justify-between gap-4">

          <p className="text-slate-500 text-xs">
            © {new Date().getFullYear()} Driftwood Café. All rights reserved.
          </p>

          <div className="flex items-center gap-6">
            <button
              onClick={() => setShowPrivacy(true)}
              className="text-slate-500 text-xs hover:text-slate-300 transition-colors"
            >
              Privacy Policy
            </button>
            <button
              onClick={() => setShowTerms(true)}
              className="text-slate-500 text-xs hover:text-slate-300 transition-colors"
            >
              Terms of Service
            </button>
            <a
              href="#visit"
              className="text-slate-500 text-xs hover:text-slate-300 transition-colors"
            >
              Sitemap
            </a>
          </div>

          {/* Scroll to Top */}
          <button
            onClick={scrollToTop}
            className="h-9 w-9 rounded-full bg-primary hover:bg-orange-700
              flex items-center justify-center transition-colors duration-200"
            aria-label="Scroll to top"
          >
            <svg className="w-4 h-4 text-white" fill="none"
              stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round"
                strokeWidth={2} d="M5 15l7-7 7 7" />
            </svg>
          </button>

        </div>
      </div>

    </footer>

    {/* Modals */}
    {showPrivacy && <PrivacyPolicyModal onClose={() => setShowPrivacy(false)} />}
    {showTerms && <TermsOfServiceModal onClose={() => setShowTerms(false)} />}
    </>
  )
}