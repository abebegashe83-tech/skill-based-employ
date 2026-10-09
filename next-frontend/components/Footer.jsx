'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Footer() {
  const pathname = usePathname();

  const isActive = (path) => pathname === path;

  const linkClass = (path) =>
    `transition-colors ${isActive(path) ? 'text-blue-400 font-semibold' : 'hover:text-white'}`;

  return (
    <footer className="bg-gray-100 dark:bg-gray-900 text-gray-600 dark:text-gray-300 py-12 transition-colors">
      <div className="max-w-7xl mx-auto px-6">
        <div className="mb-8 grid grid-cols-1 gap-8 md:grid-cols-3">
          {/* Brand Section */}
          <div className="col-span-1 md:col-span-1">
            <div className="flex items-center gap-2 text-blue-600 dark:text-blue-400 font-bold text-xl mb-4">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-black text-lg">S</div>
              <span>SkillMatch</span>
            </div>
            <p className="text-sm">
              AI-powered job matching platform connecting talent with opportunities based on skills, not degrees.
            </p>
          </div>

          {/* Links Section */}
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/" className={linkClass('/')}>Home</Link></li>
              <li><Link href="/jobs" className={linkClass('/jobs')}>Jobs</Link></li>
              <li><Link href="/about" className={linkClass('/about')}>About</Link></li>
              <li><Link href="/contact" className={linkClass('/contact')}>Contact</Link></li>
            </ul>
          </div>

          {/* Legal Section */}
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Legal</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/privacy" className={linkClass('/privacy')}>Privacy Policy</Link></li>
              <li><Link href="/terms" className={linkClass('/terms')}>Terms of Service</Link></li>
            </ul>
          </div>

        </div>

        <div className="pt-8 border-t border-gray-200 dark:border-gray-800 text-center text-sm">
          © {new Date().getFullYear()} SkillMatch. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
