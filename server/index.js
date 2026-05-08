import 'dotenv/config'
import express from 'express'
import cors from 'cors'
import { Resend } from 'resend'

const app = express()
const resend = new Resend(process.env.RESEND_API_KEY)

app.use(cors({ origin: process.env.CLIENT_ORIGIN || 'http://localhost:5173' }))
app.use(express.json())

app.post('/api/contact', async (req, res) => {
  const { name, email, message } = req.body

  if (!name || !email || !message) {
    return res.status(400).json({ error: 'All fields are required.' })
  }

  try {
    // 1. Notify the café owner
    await resend.emails.send({
      from: 'Driftwood Contact Form <onboarding@resend.dev>',
      to: process.env.OWNER_EMAIL,
      subject: `New message from ${name}`,
      html: `
        <div style="font-family:sans-serif;max-width:600px;margin:auto">
          <h2 style="color:#f97316">New Contact Form Submission</h2>
          <p><strong>Name:</strong> ${name}</p>
          <p><strong>Email:</strong> ${email}</p>
          <p><strong>Message:</strong></p>
          <blockquote style="border-left:3px solid #f97316;padding-left:12px;color:#555">
            ${message.replace(/\n/g, '<br/>')}
          </blockquote>
          <hr/>
          <p style="color:#999;font-size:12px">Sent via Driftwood Café contact form</p>
        </div>
      `,
    })

    // 2. Auto-reply to the sender
    await resend.emails.send({
      from: 'Driftwood Café <onboarding@resend.dev>',
      to: email,
      subject: 'We got your message ☕',
      html: `
        <div style="font-family:sans-serif;max-width:600px;margin:auto">
          <h2 style="color:#f97316">Thanks, ${name}!</h2>
          <p>We received your message and will get back to you within 24 hours.</p>
          <p style="color:#555;font-style:italic">"${message.replace(/\n/g, '<br/>')}"</p>
          <hr/>
          <p style="color:#999;font-size:12px">
            Driftwood Café · 123 Coffee Street, Brewville, CA 90210
          </p>
        </div>
      `,
    })

    res.json({ ok: true })
  } catch (err) {
    console.error('Resend error:', err)
    res.status(500).json({ error: 'Failed to send email.' })
  }
})

const PORT = process.env.PORT || 5000
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`))
