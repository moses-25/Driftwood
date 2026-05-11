import { motion } from 'framer-motion'
import { InputField } from './ContactSection'

const DeliveryAddressForm = ({ address, setAddress, errors }) => {
  const update = (field) => (e) => setAddress((prev) => ({ ...prev, [field]: e.target.value }))

  return (
    <motion.div
      initial={{ opacity: 0, y: -12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: [0.25, 0.1, 0.25, 1] }}
    >
      <div className="bg-white/6 rounded-2xl border border-white/10 p-6 md:p-8">
        <div className="flex items-center gap-3 mb-6">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-caramel/15 border border-caramel/25">
            <svg className="w-5 h-5 text-caramel" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
          </div>
          <div>
            <h3 className="text-lg font-bold text-white" style={{ fontFamily: "'Science Gothic', sans-serif" }}>Delivery Address</h3>
            <p className="text-sm text-white/40" style={{ fontFamily: "'Tinos', serif" }}>Where should we bring your order?</p>
          </div>
        </div>
        <div className="space-y-4">
          <InputField label="County / City" id="county" placeholder="e.g. Nairobi" value={address.county} onChange={update('county')} error={errors.county}
            icon={<svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>}
          />
          <InputField label="Street Address" id="street" placeholder="e.g. Kimathi Street" value={address.street} onChange={update('street')} error={errors.street}
            icon={<svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" /></svg>}
          />
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <InputField label="Apartment / House No." id="apartment" placeholder="e.g. Apt 4B" value={address.apartment} onChange={update('apartment')} error={errors.apartment} />
            <InputField label="Landmark (optional)" id="landmark" placeholder="e.g. Near Westgate Mall" value={address.landmark} onChange={update('landmark')} error={errors.landmark} />
          </div>
          <div className="space-y-1.5">
            <label htmlFor="notes" className="block text-sm font-medium text-white/60" style={{ fontFamily: "'Tinos', serif" }}>
              Delivery Notes <span className="text-white/30 font-normal">(optional)</span>
            </label>
            <textarea
              id="notes" rows={3}
              placeholder="Any special instructions for the delivery rider…"
              value={address.notes} onChange={update('notes')}
              style={{ fontFamily: "'Tinos', serif" }}
              className="w-full rounded-xl border border-white/12 bg-white/6 px-4 py-3 text-white placeholder-white/25 text-base outline-none focus:ring-2 focus:ring-caramel/50 focus:border-caramel/60 hover:border-white/25 transition-all duration-200 resize-none"
            />
          </div>
        </div>
      </div>
    </motion.div>
  )
}

export default DeliveryAddressForm
