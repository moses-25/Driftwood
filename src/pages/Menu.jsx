import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { menuItems } from "../data/menuData";
import MenuCard from "../components/MenuCard";
import { useCart } from "../hooks/useCart";
import SectionTitle from "../components/SectionTitle";

const TABS = [
  { key: "cold",     label: "Cold" },
  { key: "pastries", label: "Pastries" },
  { key: "hot",      label: "Hot" },
  { key: "specials", label: "Specials" },
];

const getTabIcon = (key) => {
  switch (key) {
    case "hot":
      return (
        <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M8 6h8M9 3h6a2 2 0 0 1 2 2v0a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4v0a2 2 0 0 1 2-2z" />
          <path d="M6 12h12v4a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2v-4z" />
        </svg>
      )
    case "cold":
      return (
        <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M12 3v18" />
          <path d="M8 15h8" />
          <path d="M10 7h4" />
          <path d="M9 20h6" />
        </svg>
      )
    case "pastries":
      return (
        <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M4 12c0-4 4.5-8 8-8s8 4 8 8-3.58 7-7 7H8c-2.5 0-4-2-4-4z" />
          <path d="M8 12c0 3 2 5 4 5s4-2 4-5" />
        </svg>
      )
    case "specials":
      return (
        <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M12 3l2.5 6.5L21 10l-5 4.5L17 21l-5-3.5L7 21l1-6.5L3 10l6.5-0.5L12 3z" />
        </svg>
      )
    default:
      return null
  }
}

const Menu = () => {
  const [activeTab, setActiveTab] = useState("cold");
  const { addToCart } = useCart();

  const filtered = menuItems.filter((item) => item.category === activeTab);

  const handleAddToCart = (item) => {
    addToCart(item);
  };

  return (
    <section id="menu" className="relative overflow-hidden py-28 bg-darkroast">

      {/* Subtle warm glow */}
      <div className="absolute -left-32 top-20 h-80 w-80 rounded-full bg-caramel/10 blur-3xl pointer-events-none" />
      <div className="absolute right-0 bottom-20 h-96 w-96 rounded-full bg-copper/8 blur-3xl pointer-events-none" />

      {/* Grain texture */}
      <div
        className="absolute inset-0 opacity-[0.03] pointer-events-none"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
        }}
      />

      <div className="relative max-w-7xl mx-auto px-6">

        <SectionTitle
          eyebrow="Our Menu"
          heading={<>Something for every <em className="italic text-caramel">mood</em> and moment.</>}
          subtext="Explore our signature coffees, handcrafted cold pours, fresh pastries, and seasonal specials designed to inspire your day."
          light
        />

        {/* Tab Bar */}
        <div className="flex justify-center flex-wrap gap-3 mb-12">
          {TABS.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex items-center gap-2 px-5 py-3 rounded-full text-sm font-semibold transition-all duration-200 border ${activeTab === tab.key ?
                "border-caramel bg-caramel/15 text-softwhite shadow-gold" :
                "border-white/10 bg-white/5 text-warmbeige/70 hover:bg-white/10 hover:border-white/20"
              }`}
              aria-pressed={activeTab === tab.key}
            >
              <span className="inline-flex h-9 w-9 items-center justify-center rounded-full bg-white/10 text-caramel">
                {getTabIcon(tab.key)}
              </span>
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Card Grid */}
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.3, ease: [0.25, 0.1, 0.25, 1] }}
            className="grid grid-cols-1 gap-6 sm:grid-cols-2 xl:grid-cols-3"
          >
            {filtered.map((item, i) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, y: 24 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: i * 0.07, ease: [0.25, 0.1, 0.25, 1] }}
              >
                <MenuCard item={item} onAddToCart={handleAddToCart} />
              </motion.div>
            ))}
          </motion.div>
        </AnimatePresence>

      </div>
    </section>
  );
};

export default Menu;
