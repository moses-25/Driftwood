import { useState } from "react";
import { menuItems } from "../data/menuData";
import MenuCard from "../components/MenuCard";

const TABS = [
  { key: "hot",      label: "☕ Hot" },
  { key: "cold",     label: "🧊 Cold" },
  { key: "pastries", label: "🥐 Pastries" },
  { key: "specials", label: "✨ Specials" },
];

const Menu = () => {
  const [activeTab, setActiveTab] = useState("hot");

  const filtered = menuItems.filter((item) => item.category === activeTab);

  const handleAddToCart = (item) => {
    // Placeholder — Phase 7 will wire up global cart state
    console.log("Added to cart:", item.name);
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
              className={`px-6 py-3 rounded-full text-sm font-semibold transition-all duration-200 border ${activeTab === tab.key ?
                "border-amber-500 bg-amber-500/15 text-amber-100 shadow-[0_15px_45px_rgba(251,191,36,0.14)]" :
                "border-white/10 bg-white/5 text-slate-200 hover:bg-white/10 hover:border-white/20"
              }`}
            >
              {tab.label}
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