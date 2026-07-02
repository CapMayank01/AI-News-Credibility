'use client';
import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="mt-24 border-t border-slate-200 bg-[#eef1eb] py-10 text-slate-600">
      <div className="container flex flex-col gap-6 px-5 md:flex-row md:items-center md:justify-between lg:px-8">
        <div className="flex items-center gap-3 font-extrabold text-[#142644]"><span className="grid h-8 w-8 place-items-center rounded-lg bg-[#142644] text-white">N</span> Verity</div>
        <div className="flex gap-6 text-sm font-medium"><Link href="/analyzer">Analyzer</Link><Link href="/dashboard">Dashboard</Link><Link href="/history">History</Link></div>
        <p className="text-sm">AI guidance, not a substitute for primary sources.</p>
      </div>
    </footer>
  );
}
