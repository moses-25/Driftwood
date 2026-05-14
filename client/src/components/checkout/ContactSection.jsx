const inputClass = `w-full rounded-xl border border-white/12 bg-white/6 px-4 py-3 text-white placeholder-white/25 text-base transition-all duration-200 outline-none focus:ring-2 focus:ring-caramel/50 focus:border-caramel/60 hover:border-white/25`

const InputField = ({ label, id, type = 'text', placeholder, value, onChange, error }) => (
  <div className="space-y-1.5">
    <label htmlFor={id} className="block text-sm font-medium text-white/60 font-tinos">
      {label}
    </label>
    <input
      id={id}
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      autoComplete="off"
      className={`${inputClass} font-tinos ${error ? 'border-red-500/60 focus:ring-red-500/30' : ''}`}
    />
    {error && (
      <p className="text-sm text-red-400 mt-1 font-tinos">
        {error}
      </p>
    )}
  </div>
)

const ContactSection = ({ contact, setContact, errors }) => {
  const update = (field) => (e) => setContact((prev) => ({ ...prev, [field]: e.target.value }))

  return (
    <div className="space-y-4">
      <h3 className="text-base font-semibold text-white/70 uppercase tracking-widest font-tinos">
        Contact Information
      </h3>
      <InputField label="Full Name" id="fullName" placeholder="Jane Doe" value={contact.fullName} onChange={update('fullName')} error={errors.fullName} />
      <InputField label="Email Address" id="email" type="email" placeholder="jane@example.com" value={contact.email} onChange={update('email')} error={errors.email} />
      <InputField label="Phone Number" id="phone" type="tel" placeholder="+254 700 000 000" value={contact.phone} onChange={update('phone')} error={errors.phone} />
    </div>
  )
}

export { InputField }
export default ContactSection
