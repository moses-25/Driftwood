import { useEffect } from 'react'

export default function PrivacyPolicyModal({ onClose }) {
  // Close on Escape key
  useEffect(() => {
    const handler = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [onClose])

  // Prevent body scroll while open
  useEffect(() => {
    document.body.style.overflow = 'hidden'
    return () => { document.body.style.overflow = '' }
  }, [])

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="privacy-title"
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
          <h2 id="privacy-title" className="text-white font-bold text-xl">
            Privacy Policy
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
            <h3 className="text-amber-400 font-semibold mb-2">1. Information We Collect</h3>
            <p>
              When you use our contact form or subscribe to our newsletter, we collect
              your name and email address. We do not collect payment information, and
              we do not use cookies for tracking purposes.
            </p>
          </section>

          <section>
            <h3 className="text-amber-400 font-semibold mb-2">2. How We Use Your Information</h3>
            <p>
              We use the information you provide solely to respond to your inquiries,
              process reservations, and send you our newsletter if you have opted in.
              We will never sell, rent, or share your personal data with third parties
              for marketing purposes.
            </p>
          </section>

          <section>
            <h3 className="text-amber-400 font-semibold mb-2">3. Email Communications</h3>
            <p>
              If you subscribe to our newsletter, you may unsubscribe at any time by
              clicking the unsubscribe link in any email we send. We use Resend to
              deliver emails, and your email address is stored securely on their
              platform in accordance with their privacy policy.
            </p>
          </section>

          <section>
            <h3 className="text-amber-400 font-semibold mb-2">4. Data Retention</h3>
            <p>
              We retain your contact information only as long as necessary to fulfill
              the purpose for which it was collected, or as required by law. You may
              request deletion of your data at any time by contacting us at{' '}
              <a href="mailto:hello@driftwoodcafe.com"
                className="text-amber-400 hover:underline">
                hello@driftwoodcafe.com
              </a>.
            </p>
          </section>

          <section>
            <h3 className="text-amber-400 font-semibold mb-2">5. Security</h3>
            <p>
              We take reasonable measures to protect your personal information from
              unauthorized access, disclosure, or misuse. However, no method of
              transmission over the internet is 100% secure.
            </p>
          </section>

          <section>
            <h3 className="text-amber-400 font-semibold mb-2">6. Changes to This Policy</h3>
            <p>
              We may update this Privacy Policy from time to time. Any changes will
              be posted on this page with an updated revision date.
            </p>
          </section>

          <section>
            <h3 className="text-amber-400 font-semibold mb-2">7. Contact Us</h3>
            <p>
              If you have any questions about this Privacy Policy, please reach out
              at{' '}
              <a href="mailto:hello@driftwoodcafe.com"
                className="text-amber-400 hover:underline">
                hello@driftwoodcafe.com
              </a>{' '}
              or call us at (555) 123-4567.
            </p>
          </section>

        </div>
      </div>
    </div>
  )
}
