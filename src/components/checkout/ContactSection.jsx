const InputField = ({ label, id, type = 'text', placeholder, value, onChange, error, icon }) => (
  <div className="space-y-1.5">
    <label htmlFor={id} className="block text-sm font-medium text-slate-300">
      {label}
    </label>
    <div className="relative">
      {icon && (
        <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4 text-slate-500">
          {icon}
        </div>
      )}
      <input
        id={id}
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        autoComplete="off"
        className={`w-full rounded-xl border bg-white/5 backdrop-blur-sm px-4 py-3 text-white placeholder-slate-500 text-sm transition-all duration-200 outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-500/60 hover:border-white/25 ${
          icon ? 'pl-11' : ''
        } ${
          error
            ? 'border-red-500/60 focus:ring-red-500/30'
            : 'border-white/15'
        }`}
      />
    </div>
    {error && (
      <p className="text-xs text-red-400 flex items-center gap-1 mt-1">
        <svg className="w-3.5 h-3.5 shrink-0" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
        </svg>
        {error}
      </p>
    )}
  </div>
)

const ContactSection = ({ contact, setContact, errors }) => {
  const update = (field) => (e) => setContact((prev) => ({ ...prev, [field]: e.target.value }))

  return (
    <div className="bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 p-6 md:p-8 shadow-2xl">
      <div className="flex items-center gap-3 mb-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/15 border border-amber-500/25">
          <svg className="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <div>
          <h3 className="text-lg font-bold text-white">Contact Information</h3>
          <p className="text-xs text-slate-400">We'll use this to confirm your order</p>
        </div>
      </div>

      <div className="space-y-4">
        <InputField
          label="Full Name"
          id="fullName"
          placeholder="Jane Doe"
          value={contact.fullName}
          onChange={update('fullName')}
          error={errors.fullName}
          icon={
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          }
        />
        <InputField
          label="Email Address"
          id="email"
          type="email"
          placeholder="jane@example.com"
          value={contact.email}
          onChange={update('email')}
          error={errors.email}
          icon={
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          }
        />
        <InputField
          label="Phone Number"
          id="phone"
          type="tel"
          placeholder="+254 700 000 000"
          value={contact.phone}
          onChange={update('phone')}
          error={errors.phone}
          icon={
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
          }
        />
      </div>
    </div>
  )
}

export { InputField }
export default ContactSection
