import { useState, useRef, useMemo, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { menuItems as staticMenuItems } from "../data/menuData";
import MenuCard from "../components/MenuCard";
import { useCart } from "../hooks/useCart";
import { useProducts } from "../hooks/useProducts";

const TABS = [
  { key: "cold",     label: "Cold Brews" },
  { key: "hot",      label: "Hot Drinks" },
  { key: "pastries", label: "Pastries"   },
  { key: "specials", label: "Specials"   },
];

const CoffeeBeanDeco = ({ style, size = 28 }) => (
  <svg
    width={size}
    height={size * 0.65}
    viewBox="0 0 28 18"
    style={style}
    aria-hidden="true"
  >
    <ellipse cx="14" cy="9" rx="13" ry="8.5" fill="#C58A46" />
    <path
      d="M14 1.5 Q7 9 14 16.5"
      stroke="#1E1A17"
      strokeWidth="2"
      fill="none"
      strokeLinecap="round"
    />
  </svg>
);

const CoffeeCupDeco = ({ style, size = 56 }) => (
  <svg width={size} height={size} viewBox="0 0 56 56" style={style} fill="none" aria-hidden="true">
    <path d="M8 18h34l-5 26H13L8 18z" stroke="#C58A46" strokeWidth="1.2" strokeLinejoin="round" />
    <path d="M42 22h5a5 5 0 010 10h-5" stroke="#C58A46" strokeWidth="1.2" strokeLinecap="round" />
    <ellipse cx="25" cy="17" rx="11" ry="2.5" stroke="#C58A46" strokeWidth="0.8" />
    <path d="M20 11 Q23 7 20 4" stroke="#C58A46" strokeWidth="1" strokeLinecap="round" />
    <path d="M25 10 Q28 6 25 3" stroke="#C58A46" strokeWidth="1" strokeLinecap="round" />
    <path d="M30 11 Q33 7 30 4" stroke="#C58A46" strokeWidth="1" strokeLinecap="round" />
  </svg>
);

const BEANS = [
  { top: "4%",   left:  "2%",   size: 40, rotate:  30, opacity: 0.14 },
  { top: "8%",   left:  "18%",  size: 22, rotate:  70, opacity: 0.10 },
  { top: "12%",  left:  "42%",  size: 28, rotate: -15, opacity: 0.08 },
  { top: "16%",  right: "3%",   size: 32, rotate: -30, opacity: 0.13 },
  { top: "28%",  left:  "1%",   size: 18, rotate:  55, opacity: 0.09 },
  { top: "35%",  right: "8%",   size: 26, rotate:  45, opacity: 0.11 },
  { top: "48%",  left:  "8%",   size: 34, rotate: -50, opacity: 0.12 },
  { top: "52%",  right: "2%",   size: 20, rotate:  20, opacity: 0.09 },
  { top: "60%",  left:  "30%",  size: 16, rotate:  80, opacity: 0.07 },
  { top: "65%",  right: "18%",  size: 30, rotate: -60, opacity: 0.10 },
  { bottom: "28%", right: "4%", size: 36, rotate: -45, opacity: 0.13 },
  { bottom: "22%", left: "14%", size: 24, rotate:  35, opacity: 0.09 },
  { bottom: "14%", left: "40%", size: 20, rotate: -25, opacity: 0.08 },
  { bottom: "10%", left: "22%", size: 28, rotate:  15, opacity: 0.10 },
  { bottom: "6%",  right:"10%", size: 22, rotate:  60, opacity: 0.09 },
  { bottom: "4%",  left: "5%",  size: 18, rotate: -10, opacity: 0.07 },
];

const CUPS = [
  { top: "10%",   right: "28%", size: 64, rotate:  12, opacity: 0.07 },
  { top: "42%",   left:  "20%", size: 48, rotate: -20, opacity: 0.06 },
  { bottom: "18%",right: "32%", size: 56, rotate:  30, opacity: 0.07 },
  { bottom: "35%",left:  "2%",  size: 44, rotate: -15, opacity: 0.05 },
  { top: "72%",   left:  "48%", size: 52, rotate:  40, opacity: 0.06 },
];

const WATERMARKS = [
  { text: "DRIFTWOOD", top:    "8%",  left:   "-4%", size: 130, rotate: -35, opacity: 0.04 },
  { text: "COFFEE",    top:    "38%", right:  "-6%", size: 110, rotate:  22, opacity: 0.05 },
  { text: "CRAFT",     bottom: "22%", left:   "8%",  size: 100, rotate: -18, opacity: 0.04 },
  { text: "EST. 2024", top:    "68%", right:  "12%", size:  60, rotate:  50, opacity: 0.06 },
  { text: "BREWED",    top:    "28%", left:   "30%", size:  90, rotate: -48, opacity: 0.03 },
  { text: "DRIFTWOOD", bottom: "4%",  right:  "-8%", size: 120, rotate:  18, opacity: 0.04 },
  { text: "CAFE",      top:    "55%", left:   "-2%", size:  80, rotate: -25, opacity: 0.05 },
  { text: "ROASTED",   top:    "18%", right:  "20%", size:  70, rotate:  55, opacity: 0.04 },
];

const Menu = () => {
  const [activeTab, setActiveTab] = useState("cold");
  const [quantity, setQuantity] = useState(1);
  const { addToCart } = useCart();
  const carouselRef = useRef(null);
  
  // Fetch products from backend
  const { products: backendProducts, loading, error } = useProducts();
  
  // Use backend products if available, otherwise fall back to static data
  const menuItems = useMemo(() => {
    if (loading || error || backendProducts.length === 0) {
      return staticMenuItems;
    }
    return backendProducts;
  }, [backendProducts, loading, error]);

  const filtered = menuItems.filter((item) => item.category === activeTab);
  
  const selectedItem = useMemo(() => {
    return menuItems.find((i) => i.category === activeTab) || null;
  }, [activeTab, menuItems]);

  const handleTabChange = (newTab) => {
    setActiveTab(newTab);
    setQuantity(1);
  };

  const handleAddToCart = () => {
    if (!selectedItem) return;
    for (let i = 0; i < quantity; i++) addToCart(selectedItem);
    setQuantity(1);
  };

  const scrollCarousel = (dir) => {
    carouselRef.current?.scrollBy({ left: dir * 220, behavior: "smooth" });
  };

  const handleSelectItem = (item) => {
    // For manual selection, we need to update the activeTab to match the item's category
    if (item.category !== activeTab) {
      handleTabChange(item.category);
    } else {
      setQuantity(1);
    }
  };

  return (
    <section id="menu" className="relative overflow-hidden bg-darkroast min-h-screen py-24">

      {/* Background glows */}
      <div className="absolute -left-40 top-10 h-96 w-96 rounded-full bg-caramel/8 blur-3xl pointer-events-none" />
      <div className="absolute right-0 bottom-10 h-96 w-96 rounded-full bg-copper/6 blur-3xl pointer-events-none" />
      <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 h-64 w-64 rounded-full bg-caramel/5 blur-3xl pointer-events-none" />

      {/* ── Decorative watermark layer ── */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden select-none">

        {/* Text watermarks */}
        {WATERMARKS.map((w, i) => (
          <span
            key={i}
            className="absolute font-display font-bold tracking-widest text-caramel whitespace-nowrap"
            style={{
              top: w.top, left: w.left, right: w.right, bottom: w.bottom,
              fontSize: w.size,
              opacity: w.opacity,
              transform: `rotate(${w.rotate}deg)`,
              transformOrigin: "center center",
              lineHeight: 1,
            }}
            aria-hidden="true"
          >
            {w.text}
          </span>
        ))}

        {/* Coffee cup outlines */}
        {CUPS.map((c, i) => (
          <CoffeeCupDeco
            key={i}
            size={c.size}
            style={{
              position: "absolute",
              top: c.top, left: c.left, right: c.right, bottom: c.bottom,
              opacity: c.opacity,
              transform: `rotate(${c.rotate}deg)`,
            }}
          />
        ))}

        {/* Coffee beans */}
        {BEANS.map((b, i) => (
          <CoffeeBeanDeco
            key={i}
            size={b.size}
            style={{
              position: "absolute",
              top: b.top, left: b.left, right: b.right, bottom: b.bottom,
              opacity: b.opacity,
              transform: `rotate(${b.rotate}deg)`,
            }}
          />
        ))}
      </div>

      <div className="relative max-w-7xl mx-auto px-6">

        {/* ── Header: eyebrow + tabs + signage ── */}
        <div className="relative flex flex-col items-center gap-6 mb-12">

          {/* Driftwood Cafe signage – top right */}
          <div className="absolute right-0 top-0 hidden lg:block">
            <motion.div
              initial={{ opacity: 0, y: -12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              {/* Hanging wires */}
              <div className="flex justify-center gap-8 mb-1">
                <div className="w-px h-6 bg-caramel/40" />
                <div className="w-px h-6 bg-caramel/40" />
              </div>
              <div
                className="border-2 border-caramel/50 rounded-xl px-5 py-3 bg-darkroast/80 backdrop-blur-sm"
                style={{
                  boxShadow:
                    "0 0 24px rgba(197,138,70,0.25), 0 0 8px rgba(197,138,70,0.15), inset 0 0 16px rgba(197,138,70,0.05)",
                }}
              >
                <p
                  className="font-display text-3xl italic text-caramel leading-none tracking-wide"
                  style={{ textShadow: "0 0 16px rgba(197,138,70,0.7)" }}
                >
                  Driftwood
                </p>
                <p
                  className="font-display text-xl italic text-caramel/75 text-right leading-none mt-0.5"
                  style={{ textShadow: "0 0 12px rgba(197,138,70,0.5)" }}
                >
                  cafe&apos;
                </p>
              </div>
            </motion.div>
          </div>

          {/* Eyebrow */}
          <div className="flex items-center gap-3">
            <span className="section-divider" />
            <p className="text-xs uppercase tracking-[0.35em] font-semibold font-mono text-caramel">
              Our Menu
            </p>
            <span className="section-divider rotate-180" />
          </div>

          {/* Category tabs */}
          <div className="flex gap-2 flex-wrap justify-center">
            {TABS.map((tab) => (
              <button
                key={tab.key}
                onClick={() => handleTabChange(tab.key)}
                aria-pressed={activeTab === tab.key}
                className={`px-5 py-2.5 rounded-full text-sm font-semibold border transition-all duration-200 ${
                  activeTab === tab.key
                    ? "bg-caramel text-darkroast border-caramel shadow-gold"
                    : "border-white/15 text-warmbeige/60 bg-white/5 hover:bg-white/10 hover:border-white/25 hover:text-warmbeige/80"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* ── Featured Item ── */}
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.25 }}
            className="grid grid-cols-1 lg:grid-cols-2 items-center gap-10 lg:gap-6 mb-16"
          >
            {/* Left: large image */}
            <div className="flex items-center justify-center">
              <AnimatePresence mode="wait">
                {selectedItem && (
                  <motion.div
                    key={selectedItem.id}
                    initial={{ opacity: 0, scale: 0.88, x: -24 }}
                    animate={{ opacity: 1, scale: 1,    x: 0   }}
                    exit={{   opacity: 0, scale: 0.88, x: -24 }}
                    transition={{ duration: 0.45, ease: [0.25, 0.1, 0.25, 1] }}
                    className="relative w-full max-w-[480px]"
                  >
                    <div className="w-full aspect-[4/3] rounded-3xl bg-espresso/40 overflow-hidden flex items-center justify-center">
                      <img
                        src={selectedItem.image}
                        alt={selectedItem.name}
                        className="w-full h-full object-contain object-center transition-transform duration-500"
                        style={{
                          filter:
                            "drop-shadow(0 20px 40px rgba(0,0,0,0.7)) drop-shadow(0 0 30px rgba(197,138,70,0.18))",
                        }}
                      />
                    </div>
                    {/* Ground glow */}
                    <div className="absolute -bottom-4 left-1/2 -translate-x-1/2 w-3/4 h-6 rounded-full bg-caramel/25 blur-xl pointer-events-none" />
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Right: details */}
            <div className="lg:pl-8">
              <AnimatePresence mode="wait">
                {selectedItem && (
                  <motion.div
                    key={selectedItem.id}
                    initial={{ opacity: 0, x: 24 }}
                    animate={{ opacity: 1, x: 0  }}
                    exit={{   opacity: 0, x: 24  }}
                    transition={{ duration: 0.35, ease: [0.25, 0.1, 0.25, 1] }}
                    className="flex flex-col gap-5"
                  >
                    {/* Price */}
                    <p className="text-softwhite font-bold text-5xl tracking-tight">
                      {selectedItem.price}
                    </p>

                    {/* Name */}
                    <div>
                      <h2 className="font-display text-2xl text-softwhite font-bold uppercase tracking-wider leading-tight">
                        {selectedItem.name}
                      </h2>
                      <div className="h-0.5 w-12 bg-caramel mt-2 rounded-full" />
                    </div>

                    {/* Description */}
                    <p className="text-warmbeige/60 text-sm leading-relaxed max-w-sm">
                      {selectedItem.description}
                    </p>

                    {/* Quantity + Add to cart */}
                    <div className="flex items-center gap-4 flex-wrap mt-1">
                      {/* Stepper */}
                      <div className="flex items-center border border-white/20 rounded-full overflow-hidden bg-white/5">
                        <button
                          onClick={() => setQuantity((q) => Math.max(1, q - 1))}
                          className="w-10 h-10 flex items-center justify-center text-softwhite text-lg hover:bg-white/10 transition-colors"
                          aria-label="Decrease quantity"
                        >
                          −
                        </button>
                        <span className="w-10 text-center text-softwhite font-semibold text-sm border-x border-white/15">
                          {quantity}
                        </span>
                        <button
                          onClick={() => setQuantity((q) => q + 1)}
                          className="w-10 h-10 flex items-center justify-center text-softwhite text-lg hover:bg-white/10 transition-colors"
                          aria-label="Increase quantity"
                        >
                          +
                        </button>
                      </div>

                      {/* Add to cart */}
                      <motion.button
                        whileHover={{ scale: 1.03 }}
                        whileTap={{ scale: 0.97 }}
                        onClick={handleAddToCart}
                        className="btn-gold flex-1 min-w-[140px] max-w-[200px]"
                        aria-label={`Add ${selectedItem.name} to cart`}
                      >
                        <svg
                          className="w-4 h-4 flex-shrink-0"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                          strokeWidth="2"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
                          />
                        </svg>
                        Add to Cart
                      </motion.button>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        </AnimatePresence>

        {/* ── Carousel ── */}
        <div className="relative">
          {/* Left arrow */}
          <button
            onClick={() => scrollCarousel(-1)}
            className="lg:hidden absolute -left-5 top-1/2 -translate-y-1/2 z-10 w-10 h-10 rounded-full bg-caramel flex items-center justify-center text-darkroast text-2xl font-bold shadow-gold hover:brightness-110 active:scale-95 transition-all"
            aria-label="Scroll carousel left"
          >
            ‹
          </button>

          {/* Cards */}
          <div
            ref={carouselRef}
            className="flex gap-4 overflow-x-auto scrollbar-hidden px-8 pb-3"
          >
            {filtered.map((item, i) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0  }}
                transition={{ duration: 0.4, delay: i * 0.07, ease: [0.25, 0.1, 0.25, 1] }}
                className="flex-shrink-0"
              >
                <MenuCard
                  item={item}
                  isSelected={selectedItem?.id === item.id}
                  onSelect={() => handleSelectItem(item)}
                  onAddToCart={() => addToCart(item)}
                />
              </motion.div>
            ))}
          </div>

          {/* Right arrow */}
          <button
            onClick={() => scrollCarousel(1)}
            className="lg:hidden absolute -right-5 top-1/2 -translate-y-1/2 z-10 w-10 h-10 rounded-full bg-caramel flex items-center justify-center text-darkroast text-2xl font-bold shadow-gold hover:brightness-110 active:scale-95 transition-all"
            aria-label="Scroll carousel right"
          >
            ›
          </button>
        </div>

      </div>
    </section>
  );
};

export default Menu;
