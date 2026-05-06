import barista from '../assets/barista.jpg'
import beans from '../assets/beans.jpg'

export default function About() {
  return (
    <section id="about" className="relative overflow-hidden bg-slate-950 py-24 px-6 text-white">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(249,115,22,0.16),_transparent_30%),radial-gradient(circle_at_bottom_right,_rgba(138,163,255,0.12),_transparent_30%)] pointer-events-none" />
      <div className="relative max-w-7xl mx-auto">
        <div className="grid gap-16 lg:grid-cols-[1.2fr_0.8fr] items-center">

          {/* Left - Story Content */}
          <div className="space-y-8">
            <p className="text-sm uppercase tracking-[0.32em] text-orange-300">
              Our Story
            </p>

            <div className="space-y-5">
              <h2 className="text-4xl sm:text-5xl font-semibold tracking-tight text-white">
                From humble beginnings to a coffee destination.
              </h2>
              <p className="max-w-3xl text-slate-300 text-lg leading-8">
                Founded in 2026, Driftwood Café began as a small corner shop with a bold dream: to create a warm, inviting sanctuary where every cup feels handcrafted, every sip feels unforgettable.
              </p>
            </div>

            <div className="rounded-[2rem] border border-white/10 bg-slate-900/80 p-8 shadow-2xl">
              <p className="text-slate-300 leading-8">
                Our journey started with a passion for sourcing the finest beans from sustainable farms around the world. Each cup we serve represents dedication to quality, craftsmanship, and community.
              </p>
              <p className="mt-5 text-slate-300 leading-8">
                Today, we honor the art of coffee making while creating a space where connections grow, ideas spark, and moments are savored one perfect cup at a time.
              </p>
              <p className="mt-8 text-white text-lg font-medium">
                Crafting perfect moments in 2026
              </p>
            </div>
          </div>

          {/* Right - Visuals */}
          <div className="relative">
            <div className="absolute -left-6 top-8 h-32 w-32 rounded-full bg-orange-500/20 blur-3xl" />
            <div className="grid gap-6">
              <div className="overflow-hidden rounded-[2rem] border border-white/10 shadow-2xl">
                <img
                  src={barista}
                  alt="Barista crafting coffee"
                  className="h-[420px] w-full object-cover"
                />
              </div>

              <div className="grid gap-6 sm:grid-cols-[0.9fr_1.1fr]">
                <div className="overflow-hidden rounded-[2rem] border border-white/10 shadow-2xl">
                  <img
                    src={beans}
                    alt="Coffee beans"
                    className="h-[320px] w-full object-cover"
                  />
                </div>
                <div className="relative overflow-hidden rounded-[2rem] border border-white/10 bg-slate-900/80 p-8 shadow-2xl">
                  <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(249,115,22,0.3),_transparent_40%)]" />
                  <div className="relative space-y-4">
                    <p className="text-sm uppercase tracking-[0.3em] text-orange-300">Signature Blend</p>
                    <h3 className="text-3xl font-semibold text-white">House Roast</h3>
                    <p className="text-slate-300 leading-7">
                      Delicate citrus notes, caramel sweetness, and a velvety finish for a truly memorable cup.
                    </p>
                    <div className="rounded-full bg-white/5 px-4 py-2 text-sm text-slate-200">
                      Coastal calm in a cup.
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
  )
}