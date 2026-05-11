import barista from '../assets/barista.jpg'
import beans from '../assets/beans.jpg'
import FadeUp from '../animations/FadeUp'

export default function About() {
  return (
    <section id="about" className="relative overflow-hidden bg-cream py-24 px-6 text-espresso">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(197,138,70,0.10),_transparent_30%),radial-gradient(circle_at_bottom_right,_rgba(164,90,58,0.08),_transparent_30%)] pointer-events-none" />
      <div className="relative max-w-7xl mx-auto">
        <div className="grid gap-16 lg:grid-cols-[1.2fr_0.8fr] items-center">

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
                <div className="space-y-4 pt-2 border-t border-warmbeige/60">
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

                {/* Sign-off */}
                <p className="font-display text-xl font-bold italic text-caramel">
                  — Crafting perfect moments in 2026
                </p>
              </div>
            </FadeUp>
          </div>

          {/* Right - Visuals */}
          <FadeUp delay={0.3} className="relative">
            <div className="absolute -left-6 top-8 h-32 w-32 rounded-full bg-caramel/15 blur-3xl" />
            <div className="grid gap-6">
              <div className="overflow-hidden rounded-[2rem] border border-warmbeige/60 shadow-luxury">
                <img src={barista} alt="Barista crafting coffee"
                  className="h-[420px] w-full object-cover" />
              </div>
              <div className="grid gap-6 sm:grid-cols-[0.9fr_1.1fr]">
                <div className="overflow-hidden rounded-[2rem] border border-warmbeige/60 shadow-card">
                  <img src={beans} alt="Coffee beans"
                    className="h-[320px] w-full object-cover" />
                </div>
                <div className="relative overflow-hidden rounded-[2rem] border border-warmbeige/20 bg-gradient-to-br from-espresso to-darkroast p-8 shadow-luxury">
                  <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(197,138,70,0.25),_transparent_40%)]" />
                  <div className="relative space-y-4">
                    <p className="text-sm uppercase tracking-[0.3em] text-caramel font-mono">Signature Blend</p>
                    <h3 className="font-display text-3xl font-semibold text-softwhite">House Roast</h3>
                    <p className="text-warmbeige/70 leading-7">
                      Delicate citrus notes, caramel sweetness, and a velvety finish.
                    </p>
                    <div className="rounded-full bg-caramel/10 border border-caramel/20 px-4 py-2 text-sm text-caramel">
                      Coastal calm in a cup.
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </FadeUp>

        </div>
      </div>
    </section>
  )
}
