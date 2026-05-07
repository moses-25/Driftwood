import { useState } from "react";
import { menuItems } from "../data/menuData";
import MenuCard from "../components/MenuCard";
import { useCart } from "../hooks/useCart";

const TABS = [
  { key: "hot",      label: "Hot" },
  { key: "cold",     label: "Cold" },
  { key: "pastries", label: "Pastries" },
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
  const [activeTab, setActiveTab] = useState("hot");
  const { addToCart } = useCart();

  const filtered = menuItems.filter((item) => item.category === activeTab);

  const handleAddToCart = (item) => {
    addToCart(item);
  };

  return (
    <section id="menu" className="relative overflow-hidden py-24 bg-slate-950 text-white">
      <div className="absolute -left-24 top-10 h-72 w-72 rounded-full bg-amber-500/20 blur-3xl" />
      <div className="absolute right-0 top-1/4 h-96 w-96 rounded-full bg-sky-500/10 blur-3xl" />
      <div className="relative max-w-6xl mx-auto px-6">

        {/* Heading */}
        <div className="text-center mb-12 relative z-10">
          <p className="text-sm uppercase tracking-[0.4em] text-amber-300 font-semibold mb-3">
            Our Menu
          </p>
          <h2 className="text-5xl md:text-6xl font-extrabold tracking-[-0.04em] text-white max-w-3xl mx-auto">
            Something for every mood and moment.
          </h2>
          <p className="mt-5 text-slate-300 text-base md:text-lg max-w-2xl mx-auto leading-relaxed">
            Explore our signature coffees, handcrafted cold pours, fresh pastries, and seasonal specials designed to inspire your day.
          </p>
        </div>

        {/* Tab Bar */}
        <div className="relative z-10 flex justify-center flex-wrap gap-3 mb-12">
          {TABS.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex items-center gap-2 px-5 py-3 rounded-full text-sm font-semibold transition-all duration-200 border ${activeTab === tab.key ?
                "border-amber-500 bg-amber-500/15 text-amber-100 shadow-[0_15px_45px_rgba(251,191,36,0.14)]" :
                "border-white/10 bg-white/5 text-slate-200 hover:bg-white/10 hover:border-white/20"
              }`}
            >
              <span className="inline-flex h-9 w-9 items-center justify-center rounded-full bg-white/10 text-amber-200">
                {getTabIcon(tab.key)}
              </span>
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Card Grid */}
        <div
          key={activeTab}
          className="grid grid-cols-1 gap-6 sm:grid-cols-2 xl:grid-cols-3" 
        >
          {filtered.map((item) => (
            <MenuCard key={item.id} item={item} onAddToCart={handleAddToCart} />
          ))}
        </div>

      </div>
    </section>
  );
};

export default Menu;