import { useEffect } from 'react'

export default function TermsOfServiceModal({ onClose }) {
  useEffect(() => {
    const handler = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [onClose])

  useEffect(() => {
    document.body.style.overflow = 'hidden'
    return () => { document.body.style.overflow = '' }
  }, [])

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="terms-title"
    >
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/70 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Panel */}
      <div className="relative z-10 w-full max-w-2xl max-h-[85vh] flex flex-col
        bg-slate-900 border border-white/10 rounded-2xl shadow-2xl overflow-hidden">

        {/* Header */}
        <div className="flex items-center justify-between px-8 py-5
          border-b border-white/10 flex-shrink-0">
          <h2 id="terms-title" className="text-white font-bold text-xl">
            Terms of Service
          </h2>
          <button
            onClick={onClose}
            aria-label="Close"
            className="h-8 w-8 rounded-full bg-white/5 hover:bg-white/10
              flex items-center justify-center text-slate-400
              hover:text-white transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Scrollable body */}
        <div className="overflow-y-auto px-8 py-6 text-slate-300 text-sm
          leading-relaxed flex flex-col gap-6">

          <p className="text-slate-400 text-xs">Last updated: January 1, 2026</p>

          <section>
            <h3 className="text-amber-400 font-semibold mb-2">1. Acceptance of Terms</h3>
            <p>
              By accessing or using the Driftwood Café website, you agree to be
              bound by these Terms of Service. If you do not agree to these terms,
              please do not use our website.
            </p>
          </section>

          <section>
            <h3 className="text-amber-400 font-semibold mb-2">2. Use of the Website</h3>
            <p>
              This website is provided for informational purposes — to share our
              menu, story, and contact details. You agree not to misuse the site,
              attempt to gain unauthorized access, or use it for any unlawful purpose.
            </p>
          </section>

          <section>
            <h3 className="text-amber-400 font-semibold mb-2">3. Contact Form & Reservations</h3>
            <p>
              Submitting our contact form does not guarantee a reservation. All
              reservation requests are subject to availability and confirmation by
              our team. We will respond within 24 hours during business hours.
            </p>
          </section>

          <section>
            <h3 className="text-amber-400 font-semibold mb-2">4. Intellectual Property</h3>
            <p>
              All content on this website — including text, images, logos, and
              design — is the property of Driftwood Café and may not be reproduced,
              distributed, or used without our express written permission.
            </p>
          </section>

          <section>
            <h3 className="text-amber-400 font-semibold mb-2">5. Disclaimer of Warranties</h3>
            <p>
              This website is provided "as is" without warranties of any kind.
              We do not guarantee that the site will be error-free, uninterrupted,
              or free of viruses or other harmful components.
            </p>
          </section>

          <section>
            <h3 className="text-amber-400 font-semibold mb-2">6. Limitation of Liability</h3>
            <p>
              Driftwood Café shall not be liable for any indirect, incidental, or
              consequential damages arising from your use of this website or our
              services.
            </p>
          </section>

          <section>
            <h3 className="text-amber-400 font-semibold mb-2">7. Changes to Terms</h3>
            <p>
              We reserve the right to update these Terms of Service at any time.
              Continued use of the website after changes are posted constitutes
              your acceptance of the revised terms.
            </p>
          </section>

          <section>
            <h3 className="text-amber-400 font-semibold mb-2">8. Contact</h3>
            <p>
              Questions about these terms? Email us at{' '}
              <a href="mailto:hello@driftwoodcafe.com"
                className="text-amber-400 hover:underline">
                hello@driftwoodcafe.com
              </a>.
            </p>
          </section>

        </div>
      </div>
    </div>
  )
}
