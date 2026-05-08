import { formatPrice, parsePrice } from '../utils/price'

const MenuCard = ({ item, onAddToCart }) => {
  return (
    <div className="group relative overflow-hidden rounded-[2rem] border border-white/10 bg-slate-950/90 shadow-[0_25px_80px_rgba(15,23,42,0.32)] transition-transform duration-300 hover:-translate-y-1">
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-slate-950/20 to-slate-950/95" />

      {/* Image */}
      <div className="relative aspect-[4/3] overflow-hidden rounded-t-[1.75rem] bg-slate-950">
        <img
          src={item.image}
          alt={item.name}
          className="absolute inset-0 h-full w-full object-cover object-center transition-transform duration-700 group-hover:scale-[1.02]"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent" />
        <div className="absolute left-5 bottom-5 rounded-full bg-black/50 px-4 py-2 text-xs uppercase tracking-[0.25em] text-amber-200 font-bold shadow-lg">
          {item.category}
        </div>
      </div>

      {/* Content */}
      <div className="relative p-6 flex flex-col gap-4">
        <div className="flex items-start justify-between gap-3">
          <h3 className="text-xl font-semibold text-white tracking-tight">
            {item.name}
          </h3>
          <span className="rounded-full bg-amber-600/15 px-4 py-2 text-sm font-semibold text-amber-100 ring-1 ring-amber-500/30 whitespace-nowrap">
            {formatPrice(parsePrice(item.price))}
          </span>
        </div>

        <p className="text-slate-300 text-sm leading-7 flex-1">
          {item.description}
        </p>

        <button
          onClick={() => onAddToCart(item)}
          className="mt-2 inline-flex items-center justify-center rounded-full bg-gradient-to-r from-amber-500 to-orange-500 px-5 py-3 text-sm font-semibold text-slate-950 shadow-[0_15px_30px_rgba(251,191,36,0.18)] transition-all duration-200 hover:scale-[1.02]"
        >
          Add to Cart
        </button>
      </div>
    </div>
  )
}

export default MenuCard