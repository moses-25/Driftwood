import { motion } from 'framer-motion'
import { InputField } from './ContactSection'

const DeliveryAddressForm = ({ address, setAddress, errors }) => {
  const update = (field) => (e) => setAddress((prev) => ({ ...prev, [field]: e.target.value }))

  return (
    <motion.div
      initial={{ opacity: 0, y: -12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: [0.25, 0.1, 0.25, 1] }}
      className="space-y-4"
    >
      <h3 className="text-base font-semibold text-white/70 uppercase tracking-widest" style={{ fontFamily: "'Tinos', serif" }}>
        Delivery Address
      </h3>

      <InputField label="County / City" id="county" placeholder="e.g. Nairobi" value={address.county} onChange={update('county')} error={errors.county} />
      <InputField label="Street Address" id="street" placeholder="e.g. Kimathi Street" value={address.street} onChange={update('street')} error={errors.street} />

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <InputField label="Apartment / House No." id="apartment" placeholder="e.g. Apt 4B" value={address.apartment} onChange={update('apartment')} error={errors.apartment} />
        <InputField label="Landmark (optional)" id="landmark" placeholder="e.g. Near Westgate Mall" value={address.landmark} onChange={update('landmark')} error={errors.landmark} />
      </div>

      <div className="space-y-1.5">
        <label htmlFor="notes" className="block text-sm font-medium text-white/60" style={{ fontFamily: "'Tinos', serif" }}>
          Delivery Notes <span className="text-white/30 font-normal">(optional)</span>
        </label>
        <textarea
          id="notes"
          rows={3}
          placeholder="Any special instructions for the delivery rider…"
          value={address.notes}
          onChange={update('notes')}
          style={{ fontFamily: "'Tinos', serif" }}
          className="w-full rounded-xl border border-white/12 bg-white/6 px-4 py-3 text-white placeholder-white/25 text-base outline-none focus:ring-2 focus:ring-caramel/50 focus:border-caramel/60 hover:border-white/25 transition-all duration-200 resize-none"
        />
      </div>
    </motion.div>
  )
}

export default DeliveryAddressForm
