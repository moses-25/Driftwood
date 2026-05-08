import { InputField } from './ContactSection'

const DeliveryAddressForm = ({ address, setAddress, errors }) => {
  const update = (field) => (e) => setAddress((prev) => ({ ...prev, [field]: e.target.value }))

  return (
    <div
      className="overflow-hidden transition-all duration-500"
      style={{ animation: 'slideDown 0.4s ease-out' }}
    >
      <style>{`
        @keyframes slideDown {
          from { opacity: 0; transform: translateY(-12px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `}</style>

      <div className="bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 p-6 md:p-8 shadow-2xl">
        <div className="flex items-center gap-3 mb-6">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/15 border border-amber-500/25">
            <svg className="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">Delivery Address</h3>
            <p className="text-xs text-slate-400">Where should we bring your order?</p>
          </div>
        </div>

        <div className="space-y-4">
          {/* County / City */}
          <InputField
            label="County / City"
            id="county"
            placeholder="e.g. Nairobi"
            value={address.county}
            onChange={update('county')}
            error={errors.county}
            icon={
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            }
          />

          {/* Street Address */}
          <InputField
            label="Street Address"
            id="street"
            placeholder="e.g. Kimathi Street"
            value={address.street}
            onChange={update('street')}
            error={errors.street}
            icon={
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
              </svg>
            }
          />

          {/* Two-column row */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <InputField
              label="Apartment / House No."
              id="apartment"
              placeholder="e.g. Apt 4B"
              value={address.apartment}
              onChange={update('apartment')}
              error={errors.apartment}
            />
            <InputField
              label="Landmark (optional)"
              id="landmark"
              placeholder="e.g. Near Westgate Mall"
              value={address.landmark}
              onChange={update('landmark')}
              error={errors.landmark}
            />
          </div>

          {/* Delivery Notes */}
          <div className="space-y-1.5">
            <label htmlFor="notes" className="block text-sm font-medium text-slate-300">
              Delivery Notes <span className="text-slate-500 font-normal">(optional)</span>
            </label>
            <textarea
              id="notes"
              rows={3}
              placeholder="Any special instructions for the delivery rider…"
              value={address.notes}
              onChange={update('notes')}
              className="w-full rounded-xl border border-white/15 bg-white/5 backdrop-blur-sm px-4 py-3 text-white placeholder-slate-500 text-sm transition-all duration-200 outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-500/60 hover:border-white/25 resize-none"
            />
          </div>
        </div>
      </div>
    </div>
  )
}

export default DeliveryAddressForm
