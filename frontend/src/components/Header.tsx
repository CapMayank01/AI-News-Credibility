'use client';
import Link from 'next/link';

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-200/80 bg-[#f7f8f4]/90 backdrop-blur-xl">
      <nav className="container px-5 py-4 lg:px-8">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3 text-lg font-extrabold tracking-tight text-[#142644]">
            <span className="grid h-9 w-9 place-items-center rounded-xl bg-[#142644] text-white shadow-sm">N</span> Verity
          </Link>
          <div className="hidden items-center gap-8 text-sm font-semibold text-slate-600 md:flex">
            <Link href="/" className="transition hover:text-[#142644]">Home</Link>
            <Link href="/analyzer" className="transition hover:text-[#142644]">Analyzer</Link>
            <Link href="/dashboard" className="transition hover:text-[#142644]">Dashboard</Link>
            <Link href="/history" className="transition hover:text-[#142644]">History</Link>
          </div>
          <Link href="/analyzer" className="rounded-full bg-[#142644] px-5 py-2.5 text-sm font-bold text-white transition hover:-translate-y-0.5 hover:bg-[#203b68]">Check an article</Link>
        </div>
      </nav>
    </header>
  );
}
