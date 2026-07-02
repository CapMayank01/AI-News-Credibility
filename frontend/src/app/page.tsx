import Link from 'next/link';

const features = [
  { mark: '01', title: 'Language intelligence', text: 'DistilBERT examines wording, structure, and patterns associated with misleading reporting.' },
  { mark: '02', title: 'Source context', text: 'Known publisher reputation is combined with the model signal for a more grounded assessment.' },
  { mark: '03', title: 'Similarity search', text: 'FAISS compares the article against a trusted reference library of 5,000 real-news articles.' },
];

export default function Home() {
  return (
    <div className="overflow-hidden">
      <section className="relative border-b border-slate-200/80">
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_80%_15%,rgba(85,183,145,0.18),transparent_28%),radial-gradient(circle_at_12%_75%,rgba(44,73,118,0.10),transparent_30%)]" />
        <div className="container grid min-h-[720px] items-center gap-14 px-5 py-20 lg:grid-cols-[1.08fr_.92fr] lg:px-8">
          <div>
            <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-[#35a37c]/30 bg-[#dff5ec] px-4 py-2 text-xs font-bold uppercase tracking-[0.16em] text-[#177052]">
              <span className="h-2 w-2 rounded-full bg-[#35a37c]" /> AI-powered media literacy
            </div>
            <h1 className="max-w-3xl text-5xl font-black leading-[1.03] tracking-[-0.045em] text-[#142644] sm:text-6xl lg:text-7xl">
              Read the news.<br />Question it <span className="text-[#35a37c]">better.</span>
            </h1>
            <p className="mt-7 max-w-xl text-lg leading-8 text-slate-600">
              Verity turns complex credibility signals into a clear, explainable assessment—so you can pause, inspect, and decide with context.
            </p>
            <div className="mt-9 flex flex-col gap-3 sm:flex-row">
              <Link href="/analyzer" className="inline-flex items-center justify-center rounded-full bg-[#142644] px-7 py-4 font-bold text-white shadow-lg shadow-[#142644]/15 transition hover:-translate-y-1 hover:bg-[#203b68]">
                Analyze an article <span className="ml-3">→</span>
              </Link>
              <Link href="/dashboard" className="inline-flex items-center justify-center rounded-full border border-slate-300 bg-white/70 px-7 py-4 font-bold text-[#142644] transition hover:border-[#35a37c] hover:bg-white">
                Explore the dashboard
              </Link>
            </div>
            <div className="mt-11 flex flex-wrap gap-x-8 gap-y-3 text-sm font-semibold text-slate-500">
              <span>✓ Explainable results</span><span>✓ Local ML models</span><span>✓ No account needed</span>
            </div>
          </div>

          <div className="relative mx-auto w-full max-w-lg">
            <div className="absolute -left-12 -top-10 h-28 w-28 rounded-full bg-[#f0c66f]/40 blur-2xl" />
            <div className="relative rotate-[1.5deg] rounded-[2rem] border border-slate-200 bg-white p-5 shadow-2xl shadow-slate-900/10">
              <div className="flex items-center justify-between border-b border-slate-100 pb-4">
                <div className="flex gap-1.5"><span className="h-2.5 w-2.5 rounded-full bg-[#f08b7f]" /><span className="h-2.5 w-2.5 rounded-full bg-[#f0c66f]" /><span className="h-2.5 w-2.5 rounded-full bg-[#35a37c]" /></div>
                <span className="text-xs font-bold uppercase tracking-widest text-slate-400">Credibility report</span>
              </div>
              <div className="mt-5 rounded-2xl bg-[#f4f7f3] p-5">
                <div className="mb-4 h-2.5 w-20 rounded-full bg-slate-200" /><div className="h-4 w-11/12 rounded-full bg-slate-300" /><div className="mt-2 h-4 w-3/4 rounded-full bg-slate-300" />
              </div>
              <div className="mt-5 grid grid-cols-[auto_1fr] items-center gap-5">
                <div className="grid h-28 w-28 place-items-center rounded-full bg-[conic-gradient(#35a37c_0_82%,#e5e9e3_82%)]">
                  <div className="grid h-20 w-20 place-items-center rounded-full bg-white"><div className="text-center"><b className="text-2xl text-[#142644]">82</b><p className="text-[10px] font-bold text-slate-400">SCORE</p></div></div>
                </div>
                <div className="space-y-3">
                  <div><div className="flex justify-between text-xs font-bold"><span>Model confidence</span><span>88%</span></div><div className="mt-1 h-2 rounded-full bg-slate-100"><div className="h-2 w-[88%] rounded-full bg-[#142644]" /></div></div>
                  <div><div className="flex justify-between text-xs font-bold"><span>Source quality</span><span>76%</span></div><div className="mt-1 h-2 rounded-full bg-slate-100"><div className="h-2 w-[76%] rounded-full bg-[#35a37c]" /></div></div>
                  <div className="rounded-xl bg-[#dff5ec] px-3 py-2 text-xs font-bold text-[#177052]">Likely credible</div>
                </div>
              </div>
            </div>
            <div className="absolute -bottom-7 -left-7 rounded-2xl border border-slate-200 bg-white px-5 py-4 shadow-xl"><p className="text-xs font-bold text-slate-400">REFERENCE LIBRARY</p><p className="mt-1 font-black text-[#142644]">5,000 articles</p></div>
          </div>
        </div>
      </section>

      <section className="container px-5 py-24 lg:px-8">
        <div className="mb-12 max-w-2xl"><p className="mb-3 text-sm font-black uppercase tracking-[0.18em] text-[#35a37c]">More than a label</p><h2 className="text-4xl font-black tracking-tight text-[#142644]">Evidence you can inspect.</h2><p className="mt-4 text-lg leading-8 text-slate-600">A credibility score should start your investigation, not end it. Every result breaks down the signals behind the assessment.</p></div>
        <div className="grid gap-5 md:grid-cols-3">
          {features.map((feature) => <article key={feature.mark} className="group rounded-3xl border border-slate-200 bg-white p-7 transition hover:-translate-y-1 hover:border-[#35a37c]/50 hover:shadow-xl hover:shadow-slate-900/5"><span className="text-sm font-black text-[#35a37c]">{feature.mark}</span><h3 className="mt-8 text-xl font-black text-[#142644]">{feature.title}</h3><p className="mt-3 leading-7 text-slate-600">{feature.text}</p></article>)}
        </div>
      </section>

      <section className="container px-5 lg:px-8">
        <div className="grid overflow-hidden rounded-[2rem] bg-[#142644] text-white lg:grid-cols-[1fr_.8fr]">
          <div className="p-9 sm:p-14"><p className="text-sm font-black uppercase tracking-[0.18em] text-[#7bd3b2]">A calmer verification workflow</p><h2 className="mt-4 text-4xl font-black tracking-tight">From article to insight in seconds.</h2><p className="mt-5 max-w-xl text-lg leading-8 text-slate-300">Paste the text or share a URL. Verity cleans the content, runs multiple credibility checks, and returns one readable report.</p><Link href="/analyzer" className="mt-8 inline-block rounded-full bg-[#7bd3b2] px-7 py-4 font-black text-[#142644] transition hover:bg-white">Try the analyzer</Link></div>
          <div className="grid grid-cols-2 gap-px bg-white/10 p-px"><div className="bg-[#1a3155] p-8"><b className="text-4xl text-[#7bd3b2]">98.9%</b><p className="mt-2 text-sm text-slate-300">Baseline test accuracy</p></div><div className="bg-[#1a3155] p-8"><b className="text-4xl text-[#7bd3b2]">4</b><p className="mt-2 text-sm text-slate-300">Analysis signals</p></div><div className="bg-[#1a3155] p-8"><b className="text-4xl text-[#7bd3b2]">384</b><p className="mt-2 text-sm text-slate-300">Embedding dimensions</p></div><div className="bg-[#1a3155] p-8"><b className="text-4xl text-[#7bd3b2]">100%</b><p className="mt-2 text-sm text-slate-300">Explainable output</p></div></div>
        </div>
      </section>
    </div>
  );
}
