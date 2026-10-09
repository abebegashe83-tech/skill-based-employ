'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import ThemeToggle from './ThemeToggle';
import { getSession } from '@/lib/auth';

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    setUser(getSession());
  }, []);

  const navLinkClass =
    'block rounded-lg px-3 py-2 text-sm font-medium text-gray-600 transition-colors hover:bg-gray-50 hover:text-blue-600 dark:text-gray-300 dark:hover:bg-gray-800 dark:hover:text-blue-400';

  return (
    <header className="sticky top-0 z-50 border-b border-gray-100 bg-white/90 shadow-sm backdrop-blur-md transition-colors dark:border-gray-800 dark:bg-gray-950/90">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">
        <Link href="/" className="flex items-center gap-3" onClick={() => setMenuOpen(false)}>
          <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-2xl font-black text-white shadow-lg shadow-blue-500/20">S</span>
          <span className="text-xl font-bold tracking-tight text-gray-900 dark:text-white">SkillMatch</span>
        </Link>

        <nav aria-label="Main navigation" className="hidden items-center gap-2 md:flex">
          <Link href="/" className={navLinkClass}>Home</Link>
          <Link href="/jobs" className={navLinkClass}>Jobs</Link>
          <ThemeToggle shorthand />
          {user ? (
            <Link href="/dashboard" className={navLinkClass}>Dashboard</Link>
          ) : (
            <>
              <Link href="/login" className={navLinkClass}>Login</Link>
              <Link href="/signup" className="rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-colors hover:bg-blue-700">Register</Link>
            </>
          )}
        </nav>

        <div className="flex items-center gap-2 md:hidden">
          <ThemeToggle shorthand />
          <button
            type="button"
            className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-gray-200 text-gray-700 transition-colors hover:bg-gray-50 dark:border-gray-700 dark:text-gray-200 dark:hover:bg-gray-800"
            aria-label={menuOpen ? 'Close navigation menu' : 'Open navigation menu'}
            aria-expanded={menuOpen}
            aria-controls="mobile-main-navigation"
            onClick={() => setMenuOpen((open) => !open)}
          >
            <span aria-hidden="true" className="text-xl leading-none">{menuOpen ? '×' : '☰'}</span>
          </button>
        </div>
      </div>

      {menuOpen && (
        <nav
          id="mobile-main-navigation"
          aria-label="Mobile navigation"
          className="space-y-1 border-t border-gray-100 bg-white px-4 py-3 dark:border-gray-800 dark:bg-gray-950 md:hidden"
        >
          <Link href="/" className={navLinkClass} onClick={() => setMenuOpen(false)}>Home</Link>
          <Link href="/jobs" className={navLinkClass} onClick={() => setMenuOpen(false)}>Jobs</Link>
          {user ? (
            <Link href="/dashboard" className={navLinkClass} onClick={() => setMenuOpen(false)}>Dashboard</Link>
          ) : (
            <>
              <Link href="/login" className={navLinkClass} onClick={() => setMenuOpen(false)}>Login</Link>
              <Link href="/signup" className={navLinkClass} onClick={() => setMenuOpen(false)}>Register</Link>
            </>
          )}
        </nav>
      )}
    </header>
  );
}
