import { useState } from 'react'

const HOURS = [
  { day: 'Monday - Friday', hours: '7:00 AM - 8:00 PM' },
  { day: 'Saturday', hours: '8:00 AM - 9:00 PM' },
  { day: 'Sunday', hours: '8:00 AM - 7:00 PM' },
]

const INFO = [
  {
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
      </svg>
    ),
    text: '(555) 123-4567',
  },
  {
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
      </svg>
    ),
    text: 'hello@driftwoodcafe.com',
  },
  {
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    ),
    text: '123 Coffee Street, Brewville, CA 90210',
  },
]

const isCurrentlyOpen = () => {
  const now = new Date()
  const day = now.getDay()
  const hour = now.getHours()
  if (day >= 1 && day <= 5) return hour >= 7 && hour < 20
  if (day === 6) return hour >= 8 && hour < 21
  if (day === 0) return hour >= 8 && hour < 19
  return false
}

export default function VisitUs() {
  const [form, setForm] = useState({ name: '', email: '', message: '' })
  const [status, setStatus] = useState('idle') // idle | loading | success | error

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setStatus('loading')

    try {
      const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:5000'
      const res = await fetch(`${apiBase}/api/contact`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })

      if (!res.ok) throw new Error('Failed')

      setStatus('success')
      setForm({ name: '', email: '', message: '' })
    } catch {
      setStatus('error')
    }
  }

  const open = isCurrentlyOpen()

  return (
    <section id="visit" className="relative overflow-hidden bg-slate-950 py-24 px-6">

      {/* Background glows */}
      <div className="absolute -left-24 top-10 h-72 w-72 rounded-full
        bg-amber-500/15 blur-3xl pointer-events-none" />
      <div className="absolute right-0 bottom-10 h-96 w-96 rounded-full
        bg-sky-500/10 blur-3xl pointer-events-none" />

      <div className="relative max-w-6xl mx-auto">

        {/* Heading */}
        <div className="text-center mb-14">
          <p className="text-sm uppercase tracking-[0.4em] text-amber-300
            font-semibold mb-3">
            Find Us
          </p>
          <h2 className="text-5xl md:text-6xl font-extrabold
            tracking-[-0.04em] text-white max-w-3xl mx-auto">
            Come visit us.
          </h2>
          <p className="mt-5 text-slate-300 text-base md:text-lg max-w-2xl
            mx-auto leading-relaxed">
            We'd love to see you in person. Find us, reach out, or
            reserve your spot.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">

          {/* Left Column */}
          <div className="flex flex-col gap-6">

            {/* Map Placeholder */}
            <div className="rounded-2xl border border-white/10 bg-slate-900/60
              overflow-hidden h-64 flex items-center justify-center relative">
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(249,115,22,0.08),_transparent_70%)]" />
              <div className="text-center relative z-10">
                <svg className="w-10 h-10 text-amber-500 mx-auto mb-3"
                  fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round"
                    strokeWidth={1.5} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <p className="text-slate-400 text-sm">Interactive Map</p>
                <p className="text-slate-500 text-xs mt-1">
                  DROPPING SOON <br />
                  we're brewing up something special to help you find us with ease.
                </p>
              </div>
            </div>

            {/* Opening Hours */}
            <div className="rounded-2xl border border-white/10 bg-slate-900/60
              backdrop-blur-sm p-6">
              <h3 className="text-white font-semibold text-lg mb-5">
                Opening Hours
              </h3>
              <div className="flex flex-col gap-4">
                {HOURS.map((item) => (
                  <div key={item.day}
                    className="flex justify-between items-center">
                    <span className="text-amber-400 text-sm">{item.day}</span>
                    <span className="text-slate-300 text-sm">{item.hours}</span>
                  </div>
                ))}
              </div>

              {/* Open/Closed Status */}
              <div className="mt-6 flex items-center gap-2">
                <span className={`h-2 w-2 rounded-full ${open ? 'bg-green-400' : 'bg-red-400'}`} />
                <span className="text-slate-400 text-sm">
                  {open ? 'Currently Open' : 'Currently Closed'}
                </span>
              </div>
            </div>

            {/* Contact Info */}
            <div className="rounded-2xl border border-white/10 bg-slate-900/60
              backdrop-blur-sm p-6 flex flex-col gap-4">
              {INFO.map((item) => (
                <div key={item.text} className="flex items-center gap-3">
                  <div className="text-amber-400 flex-shrink-0">{item.icon}</div>
                  <span className="text-slate-300 text-sm">{item.text}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Right Column - Contact Form */}
          <div className="rounded-2xl border border-white/10 bg-slate-900/60
            backdrop-blur-sm p-8">
            <h3 className="text-white font-semibold text-lg mb-2">
              Contact Us
            </h3>
            <p className="text-slate-400 text-sm mb-8">
              Have a question or want to make a reservation? We'll get
              back to you within 24 hours.
            </p>

            <form onSubmit={handleSubmit} className="flex flex-col gap-5">

              {/* Name */}
              <div>
                <label className="block text-slate-400 text-xs font-medium
                  uppercase tracking-wider mb-2" htmlFor="contact-name">
                  Name
                </label>
                <input
                  id="contact-name"
                  type="text"
                  name="name"
                  value={form.name}
                  onChange={handleChange}
                  placeholder="Your name"
                  required
                  className="w-full bg-slate-800/60 border border-white/10
                    rounded-xl px-4 py-3 text-white text-sm placeholder-slate-500
                    focus:outline-none focus:border-amber-500/50
                    focus:ring-1 focus:ring-amber-500/30 transition-colors"
                />
              </div>

              {/* Email */}
              <div>
                <label className="block text-slate-400 text-xs font-medium
                  uppercase tracking-wider mb-2" htmlFor="contact-email">
                  Email
                </label>
                <input
                  id="contact-email"
                  type="email"
                  name="email"
                  value={form.email}
                  onChange={handleChange}
                  placeholder="your.email@example.com"
                  required
                  className="w-full bg-slate-800/60 border border-white/10
                    rounded-xl px-4 py-3 text-white text-sm placeholder-slate-500
                    focus:outline-none focus:border-amber-500/50
                    focus:ring-1 focus:ring-amber-500/30 transition-colors"
                />
              </div>

              {/* Message */}
              <div>
                <label className="block text-slate-400 text-xs font-medium
                  uppercase tracking-wider mb-2" htmlFor="contact-message">
                  Message
                </label>
                <textarea
                  id="contact-message"
                  name="message"
                  value={form.message}
                  onChange={handleChange}
                  placeholder="Your message..."
                  rows={5}
                  required
                  className="w-full bg-slate-800/60 border border-white/10
                    rounded-xl px-4 py-3 text-white text-sm placeholder-slate-500
                    focus:outline-none focus:border-amber-500/50
                    focus:ring-1 focus:ring-amber-500/30 transition-colors resize-none"
                />
              </div>

              {/* Submit */}
              <button
                type="submit"
                disabled={status === 'loading'}
                className="w-full bg-primary hover:bg-orange-700 disabled:opacity-50
                  disabled:cursor-not-allowed text-white font-medium py-3
                  rounded-xl transition-colors duration-200"
              >
                {status === 'loading' ? 'Sending...' : 'Send Message'}
              </button>

              {/* Feedback */}
              {status === 'success' && (
                <p className="text-green-400 text-sm text-center">
                  ✓ Message sent! We'll get back to you within 24 hours.
                </p>
              )}
              {status === 'error' && (
                <p className="text-red-400 text-sm text-center">
                  Something went wrong. Please try again.
                </p>
              )}

            </form>
          </div>
        </div>
      </div>
    </section>
  )
}