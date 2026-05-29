import { useState } from 'react'
import { submitContactForm } from '../services/api'
import visitBg from '../assets/visit.jpeg'

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
  const [form, setForm] = useState({ name: '', email: '', phone: '', message: '' })
  const [status, setStatus] = useState('idle')
  const open = isCurrentlyOpen()

  const handleChange = (e) => setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setStatus('loading')
    try {
      await submitContactForm(form)
      setStatus('success')
      setForm({ name: '', email: '', phone: '', message: '' })
    } catch {
      setStatus('error')
    }
  }

  const inputClass = `
    w-full bg-white border border-slate-200 rounded-xl px-4 py-3
    text-slate-800 text-sm placeholder-slate-400
    focus:outline-none focus:border-caramel/60 focus:ring-2 focus:ring-caramel/10
    transition-all duration-200
  `

  return (
    <section id="visit" className="bg-white">

      {/* ── Hero Banner ── */}
      <div className="relative h-56 md:h-72 overflow-hidden flex flex-col items-center justify-center text-center px-6">
        <img src={visitBg} alt="" aria-hidden="true" className="absolute inset-0 w-full h-full object-cover" />
        <div className="absolute inset-0 bg-black/35" />
        <div className="relative z-10">
          <h2 className="font-display text-4xl md:text-5xl font-bold text-white mb-3">Visit Us</h2>
        </div>
      </div>

      {/* ── Get In Touch + Form ── */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <div className="grid lg:grid-cols-2 gap-14 items-start">

          {/* ── Left — Info ── */}
          <div>
            <h3
              className="text-3xl md:text-5xl font-black text-espresso mb-2 font-fjalla"
            >
              Get In Touch
            </h3>
            <p className="text-slate-400 text-sm leading-relaxed mb-10 max-w-sm font-instrument">
              Have a question, want to make a reservation, or just want to say hello? We'll get back to you within 24 hours.
            </p>

            {/* Divider */}
            <div className="h-px bg-slate-100 mb-6" />

            {/* Hours */}
            <div>
              <div className="flex items-center gap-2 mb-4">
                <span className="text-espresso font-bold text-sm font-instrument">Opening Hours</span>
                <span className={`ml-auto text-[10px] font-bold font-mono px-2.5 py-1 rounded-full ${open ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'}`}>
                  {open ? 'Open Now' : 'Closed'}
                </span>
              </div>
              <div className="flex flex-col gap-2.5 font-instrument">
                {[
                  { day: 'Mon – Fri', hours: '7:00 AM – 8:00 PM' },
                  { day: 'Saturday', hours: '8:00 AM – 9:00 PM' },
                  { day: 'Sunday',   hours: '8:00 AM – 7:00 PM' },
                ].map(row => (
                  <div key={row.day} className="flex justify-between items-center text-sm max-w-xs">
                    <span className="text-slate-400">{row.day}</span>
                    <span className="font-semibold text-espresso">{row.hours}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* ── Right — Form ── */}
          <div className="bg-slate-50 rounded-3xl p-8 shadow-soft">
            <form onSubmit={handleSubmit} className="flex flex-col gap-5">

              {/* Email + Name */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2" htmlFor="contact-email">Email</label>
                  <input id="contact-email" type="email" name="email" value={form.email} onChange={handleChange} placeholder="Email" required className={inputClass} />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2" htmlFor="contact-name">Name</label>
                  <input id="contact-name" type="text" name="name" value={form.name} onChange={handleChange} placeholder="Name" required className={inputClass} />
                </div>
              </div>

              {/* Phone */}
              <div>
                <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2" htmlFor="contact-phone">Phone</label>
                <input id="contact-phone" type="tel" name="phone" value={form.phone} onChange={handleChange} placeholder="Phone" className={inputClass} />
              </div>

              {/* Message */}
              <div>
                <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2" htmlFor="contact-message">Message</label>
                <textarea id="contact-message" name="message" value={form.message} onChange={handleChange} placeholder="Your message…" rows={5} required className={`${inputClass} resize-none`} />
              </div>

              {/* Submit */}
              <button
                type="submit"
                disabled={status === 'loading'}
                className="w-full bg-espresso hover:bg-caramel text-white font-bold text-sm tracking-[0.12em] uppercase py-4 rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-gold"
              >
                {status === 'loading' ? 'Sending…' : 'Send Message'}
              </button>

              {status === 'success' && <p className="text-green-600 text-sm text-center font-medium">✓ Message sent! We'll get back to you within 24 hours.</p>}
              {status === 'error' && <p className="text-red-500 text-sm text-center">Something went wrong. Please try again.</p>}
            </form>
          </div>

        </div>
      </div>

      {/* ── Full-width Map ── */}
      <div className="w-full h-72 md:h-96 relative overflow-hidden">
        <iframe
          title="Driftwood Café location"
          src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.8!2d36.8219!3d-1.2921!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMcKwMTcnMzEuMiJTIDM2wrA0OScxOC44IkU!5e0!3m2!1sen!2ske!4v1620000000000!5m2!1sen!2ske"
          width="100%" height="100%"
          style={{ border: 0 }}
          allowFullScreen="" loading="lazy" referrerPolicy="no-referrer-when-downgrade"
        />
      </div>

    </section>
  )
}
