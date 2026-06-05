import barista from '../assets/barista.jpg'
import beans from '../assets/beans.jpg'
import FadeUp from '../animations/FadeUp'

export default function About() {
  return (
    <section id="about" className="relative overflow-hidden bg-cream py-24 px-6 text-espresso">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(197,138,70,0.10),_transparent_30%),radial-gradient(circle_at_bottom_right,_rgba(164,90,58,0.08),_transparent_30%)] pointer-events-none" />
      <div className="relative max-w-7xl mx-auto">
        {/* Main Story Section */}
        <div className="grid gap-12 lg:grid-cols-[1.2fr_0.8fr] items-start mb-20">

          {/* Left - Story Content */}
          <div className="space-y-8">
            <FadeUp delay={0}>
              <p className="text-2xl text-copper font-luckiest">
                Our Story
              </p>
            </FadeUp>

            <FadeUp delay={0.1}>
              <div className="space-y-6">
                <h2 className="font-display text-5xl sm:text-6xl font-bold tracking-tight text-espresso leading-[1.1]">
                  From humble beginnings to a coffee destination.
                </h2>

                {/* Intro paragraph — larger, acts as a lead */}
                <p className="font-serif-body text-2xl sm:text-3xl text-espresso/85 leading-10 font-semibold">
                  Founded in 2026, Driftwood Café began as a small corner shop with a bold dream:
                  to create a warm, inviting sanctuary where every cup feels handcrafted,
                  every sip feels unforgettable.
                </p>

                {/* Body paragraphs */}
                <div className="space-y-4 pt-6 border-t border-warmbeige/60">
                  <p className="text-lg text-espresso/70 leading-8 font-medium">
                    Our journey started with a passion for sourcing the finest beans from
                    sustainable farms around the world. Each cup we serve represents dedication
                    to quality, craftsmanship, and community.
                  </p>
                  <p className="text-lg text-espresso/70 leading-8 font-medium">
                    Today, we honor the art of coffee making while creating a space where
                    connections grow, ideas spark, and moments are savored one perfect cup at a time.
                  </p>
                </div>
              </div>
            </FadeUp>
          </div>

          {/* Right - Visuals (Desktop only) */}
          <FadeUp delay={0.3} className="relative hidden lg:block">
            <div className="absolute -left-6 top-8 h-32 w-32 rounded-full bg-caramel/15 blur-3xl" />
            <div className="grid gap-6">
              <div className="overflow-hidden rounded-lg md:rounded-2xl border-4 md:border-8 border-yellow-900/40 shadow-lg md:shadow-2xl bg-yellow-50/50" style={{boxShadow: '0 10px 25px rgba(0,0,0,0.1), inset 0 1px 0 rgba(255,255,255,0.5)'}}>
                <img src={barista} alt="Barista crafting coffee"
                  className="h-48 md:h-[420px] w-full object-cover" style={{filter: 'sepia(0.15)'}} />
              </div>
              <div className="grid gap-6 grid-cols-[0.9fr_1.1fr]">
                <div className="overflow-hidden rounded-lg md:rounded-2xl border-4 md:border-8 border-yellow-900/40 shadow-lg md:shadow-xl bg-yellow-50/50" style={{boxShadow: '0 10px 25px rgba(0,0,0,0.1), inset 0 1px 0 rgba(255,255,255,0.5)'}}>
                  <img src={beans} alt="Coffee beans"
                    className="h-40 md:h-[320px] w-full object-cover" style={{filter: 'sepia(0.15)'}} />
                </div>
                <div className="relative overflow-hidden rounded-lg border-4 border-caramel/80 bg-gradient-to-b from-amber-100 via-amber-50 to-yellow-50 p-8 shadow-2xl" style={{backgroundImage: 'repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(139,69,19,.05) 2px, rgba(139,69,19,.05) 4px)'}}>
                  <div className="absolute top-4 right-4 w-16 h-16 border-3 border-caramel/40 rounded-full" />
                  <div className="relative space-y-5">
                    <div className="space-y-1">
                      <p className="text-xs uppercase tracking-widest text-amber-900 font-serif font-bold" style={{letterSpacing: '0.15em'}}>~ Established 2026 ~</p>
                      <p className="text-xs uppercase tracking-[0.4em] text-amber-800 font-mono font-bold">Premium Blend</p>
                    </div>
                    <h3 className="font-serif text-4xl font-bold text-amber-950 leading-tight">House Roast</h3>
                    <p className="text-amber-900 leading-7 text-sm font-serif italic">
                      Delicate citrus notes, caramel sweetness, and a velvety finish.
                    </p>
                    <div className="pt-2 border-t-2 border-caramel/60">
                      <p className="text-xs text-amber-900 font-serif italic font-semibold">✦ Coastal calm in a cup. ✦</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </FadeUp>
        </div>

        {/* Mobile Images - 2 Column Grid (visible only on mobile) */}
        <FadeUp delay={0.3} className="lg:hidden">
          <div className="grid grid-cols-2 gap-4 mb-12">
            <div className="overflow-hidden rounded-lg border-4 border-yellow-900/40 shadow-lg bg-yellow-50/50" style={{boxShadow: '0 10px 25px rgba(0,0,0,0.1), inset 0 1px 0 rgba(255,255,255,0.5)'}}>
              <img src={barista} alt="Barista crafting coffee"
                className="h-56 w-full object-cover" style={{filter: 'sepia(0.15)'}} />
            </div>
            <div className="overflow-hidden rounded-lg border-4 border-yellow-900/40 shadow-lg bg-yellow-50/50" style={{boxShadow: '0 10px 25px rgba(0,0,0,0.1), inset 0 1px 0 rgba(255,255,255,0.5)'}}>
              <img src={beans} alt="Coffee beans"
                className="h-56 w-full object-cover" style={{filter: 'sepia(0.15)'}} />
            </div>
          </div>
          
          {/* House Roast Card Below Images on Mobile */}
          <div className="relative overflow-hidden rounded-lg border-4 border-caramel/80 bg-gradient-to-b from-amber-100 via-amber-50 to-yellow-50 p-8 shadow-2xl" style={{backgroundImage: 'repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(139,69,19,.05) 2px, rgba(139,69,19,.05) 4px)'}}>
            <div className="absolute top-4 right-4 w-12 h-12 border-3 border-caramel/40 rounded-full" />
            <div className="relative space-y-5">
              <div className="space-y-1">
                <p className="text-xs uppercase tracking-widest text-amber-900 font-serif font-bold" style={{letterSpacing: '0.15em'}}>~ Established 2026 ~</p>
                <p className="text-xs uppercase tracking-[0.4em] text-amber-800 font-mono font-bold">Premium Blend</p>
              </div>
              <h3 className="font-serif text-3xl font-bold text-amber-950 leading-tight">House Roast</h3>
              <p className="text-amber-900 leading-7 text-sm font-serif italic">
                Delicate citrus notes, caramel sweetness, and a velvety finish.
              </p>
              <div className="pt-2 border-t-2 border-caramel/60">
                <p className="text-xs text-amber-900 font-serif italic font-semibold">✦ Coastal calm in a cup. ✦</p>
              </div>
            </div>
          </div>
        </FadeUp>


      </div>
    </section>
  )
}
