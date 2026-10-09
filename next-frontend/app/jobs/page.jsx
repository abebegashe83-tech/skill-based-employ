'use client';

import React, { useState, useEffect, Suspense } from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import api from '@/lib/api';
import Header from '@/components/Header';

// Professional SVG Icons
const IconSearch = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>;
const IconMapPin = () => <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>;
const IconDollar = () => <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>;
const IconFilter = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/></svg>;
const IconChevronLeft = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"/></svg>;
const IconChevronRight = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"/></svg>;

function JobsPageContent() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const [searchTerm, setSearchTerm] = useState(searchParams.get('search') || '');
    const [filters, setFilters] = useState({ location: '', skills: '' });
    const [selectedExperience, setSelectedExperience] = useState([]);
    const [jobs, setJobs] = useState([]);
    const [filteredJobs, setFilteredJobs] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [showFilters, setShowFilters] = useState(false);
    const [loading, setLoading] = useState(true);
    const [loadError, setLoadError] = useState('');
    const jobsPerPage = 8;
    const experienceLevels = [
        { label: 'Entry level', value: 'ENTRY' },
        { label: 'Mid level', value: 'MID' },
        { label: 'Senior', value: 'SENIOR' },
        { label: 'Executive', value: 'EXECUTIVE' },
    ];

    useEffect(() => {
        const fetchJobs = async () => {
            try {
                setLoading(true);
                setLoadError('');
                const response = await api.get('jobs/');
                setJobs(response.data);
                setFilteredJobs(response.data);
            } catch (err) {
                console.error('Failed to load jobs:', err);
                setLoadError('We could not load job listings. Please try again.');
            } finally {
                setLoading(false);
            }
        };
        fetchJobs();
    }, []);

    useEffect(() => {
        const searchTerms = searchTerm.trim().toLowerCase().split(/\s+/).filter(Boolean);
        const skillTerms = filters.skills
            .split(',')
            .map((skill) => skill.trim().toLowerCase())
            .filter(Boolean);
        const filtered = jobs
            .filter((job) => {
                const jobSkills = Array.isArray(job.required_skills)
                    ? job.required_skills.map((skill) => String(skill).toLowerCase())
                    : [];
                const searchableText = [
                    job.title,
                    job.description,
                    job.company_name,
                    ...jobSkills,
                ].filter(Boolean).join(' ').toLowerCase();
                const matchesSearch = searchTerms.length === 0 ||
                    searchTerms.every((term) => searchableText.includes(term));
                const matchesLocation = !filters.location.trim() ||
                    (job.location || '').toLowerCase().includes(filters.location.trim().toLowerCase());
                const matchesSkills = skillTerms.length === 0 ||
                    skillTerms.every((term) => jobSkills.some((skill) => skill.includes(term)));
                const matchesExperience = selectedExperience.length === 0 ||
                    selectedExperience.includes((job.experience_level || '').toUpperCase());
                return matchesSearch && matchesLocation && matchesSkills && matchesExperience;
            })
            .sort((left, right) => new Date(right.created_at) - new Date(left.created_at));
        setFilteredJobs(filtered);
        setCurrentPage(1);
    }, [searchTerm, filters, selectedExperience, jobs]);

    const submitSearch = (event) => {
        event.preventDefault();
        const query = new URLSearchParams(searchParams.toString());
        if (searchTerm.trim()) query.set('search', searchTerm.trim());
        else query.delete('search');
        router.replace(`/jobs${query.size ? `?${query.toString()}` : ''}`, { scroll: false });
        document.getElementById('job-results')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };

    const indexOfLastJob = currentPage * jobsPerPage;
    const indexOfFirstJob = indexOfLastJob - jobsPerPage;
    const currentJobs = filteredJobs.slice(indexOfFirstJob, indexOfLastJob);
    const totalPages = Math.ceil(filteredJobs.length / jobsPerPage);

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-all font-sans selection:bg-blue-100">
            <Header />

            <main className="mx-auto max-w-7xl space-y-8 px-4 py-8 sm:space-y-12 sm:px-6 sm:py-12">
                {/* Search Bar Section */}
                <section className="text-center space-y-8 animate-in fade-in duration-700">
                    <h1 className="mx-auto max-w-2xl text-3xl font-black uppercase leading-tight tracking-tighter text-gray-900 dark:text-gray-100 sm:text-5xl sm:leading-none">Find your next defining opportunity.</h1>
                    <form onSubmit={submitSearch} className="mx-auto flex max-w-3xl flex-col gap-2 rounded-3xl border border-gray-200 bg-white p-3 shadow-2xl shadow-blue-500/5 transition-all focus-within:shadow-blue-500/10 dark:border-gray-700 dark:bg-gray-800 sm:rounded-[2rem] md:flex-row">
                        <label className="flex min-h-12 flex-1 items-center gap-3 px-4 sm:px-6">
                            <span className="text-gray-500"><IconSearch /></span>
                            <input 
                                type="text" 
                                aria-label="Search jobs"
                                placeholder="Search by title, company, or tech stack..." 
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="w-full bg-transparent border-none focus:ring-0 text-sm font-bold text-gray-900 dark:text-gray-100 placeholder:text-gray-500"
                            />
                        </label>
                        <div className="w-px bg-gray-200 dark:bg-gray-700 hidden md:block my-3"></div>
                        <label className="flex min-h-12 flex-1 items-center gap-3 px-4 sm:px-6">
                            <span className="text-gray-500"><IconMapPin /></span>
                            <input 
                                type="text" 
                                aria-label="Filter by location"
                                placeholder="Anywhere" 
                                value={filters.location}
                                onChange={(e) => setFilters({...filters, location: e.target.value})}
                                className="w-full bg-transparent border-none focus:ring-0 text-sm font-bold text-gray-900 dark:text-gray-100 placeholder:text-gray-500"
                            />
                        </label>
                        <button type="submit" className="rounded-2xl bg-blue-600 px-6 py-3 font-black uppercase tracking-widest text-white shadow-xl shadow-blue-500/20 transition-colors hover:bg-blue-700 active:scale-95 sm:px-10">Discover jobs</button>
                    </form>
                </section>

                <div className="grid grid-cols-1 lg:grid-cols-4 gap-10">
                    {/* Filters Sidebar */}
                    <div className="lg:hidden">
                        <button
                            type="button"
                            aria-expanded={showFilters}
                            aria-controls="job-filters"
                            onClick={() => setShowFilters((visible) => !visible)}
                            className="flex w-full items-center justify-center gap-2 rounded-xl border border-gray-200 bg-white px-4 py-3 text-sm font-bold text-gray-700 transition-colors hover:border-blue-300 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200"
                        >
                            <IconFilter />
                            {showFilters ? 'Hide filters' : 'Show filters'}
                        </button>
                    </div>
                    <aside id="job-filters" className={`${showFilters ? 'block' : 'hidden'} lg:col-span-1 lg:block animate-in slide-in-from-left-4 duration-700`}>
                        <section className="bg-white dark:bg-gray-800 p-8 rounded-[2.5rem] border border-gray-200 dark:border-gray-700 shadow-sm space-y-8">
                            <div className="flex items-center gap-2 mb-2">
                                <IconFilter />
                                <h2 className="text-xs font-black text-gray-900 dark:text-gray-100 uppercase tracking-widest">Filter results</h2>
                            </div>

                            <div className="space-y-3">
                                <label htmlFor="skills-filter" className="text-[10px] font-black text-gray-500 dark:text-gray-400 uppercase tracking-widest">Skills</label>
                                <input
                                    id="skills-filter"
                                    type="text"
                                    value={filters.skills}
                                    onChange={(event) => setFilters({ ...filters, skills: event.target.value })}
                                    placeholder="e.g. Python, design"
                                    className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-900 placeholder:text-gray-400 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
                                />
                                <p className="text-xs text-gray-500 dark:text-gray-400">Separate multiple skills with commas.</p>
                            </div>
                            
                            <div className="space-y-4">
                                <p className="text-[10px] font-black text-gray-500 dark:text-gray-400 uppercase tracking-widest">Experience</p>
                                {experienceLevels.map(({ label, value }) => (
                                    <label key={value} className="flex items-center gap-3 cursor-pointer group">
                                        <input 
                                            type="checkbox" 
                                            className="w-4 h-4 rounded border-gray-300 dark:border-gray-600 text-blue-600 focus:ring-blue-500"
                                            checked={selectedExperience.includes(value)}
                                            onChange={(e) => {
                                                if (e.target.checked) {
                                                    setSelectedExperience([...selectedExperience, value]);
                                                } else {
                                                    setSelectedExperience(selectedExperience.filter((level) => level !== value));
                                                }
                                            }}
                                        />
                                        <span className="text-xs font-bold text-gray-600 dark:text-gray-400 group-hover:text-blue-600 transition-colors uppercase">{label}</span>
                                    </label>
                                ))}
                            </div>
                        </section>
                    </aside>

                    {/* Jobs Grid */}
                    <div id="job-results" className="min-w-0 scroll-mt-24 space-y-8 lg:col-span-3">
                        <div className="flex flex-wrap items-center justify-between gap-2 px-2 text-[10px] font-black uppercase tracking-widest text-gray-500 dark:text-gray-400">
                            <span>Showing {filteredJobs.length} listings</span>
                            <span>Newest first</span>
                        </div>

                        {loadError ? (
                            <div role="alert" className="rounded-2xl border border-red-200 bg-red-50 p-6 text-sm font-medium text-red-800 dark:border-red-900 dark:bg-red-950/40 dark:text-red-200">
                                <p>{loadError}</p>
                                <button type="button" onClick={() => window.location.reload()} className="mt-3 font-bold underline underline-offset-4">Try again</button>
                            </div>
                        ) : loading ? (
                           <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                             {[...Array(4)].map((_, i) => <div key={i} className="h-64 bg-white dark:bg-gray-800 rounded-[2.5rem] animate-pulse"></div>)}
                           </div>
                        ) : (
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-in fade-in duration-1000">
                            {currentJobs.map(job => (
                                <Link key={job.id} href={`/jobs/${job.id}`} className="bg-white dark:bg-gray-800 p-8 rounded-[2.5rem] border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-2xl hover:-translate-y-2 transition-all duration-500 group flex flex-col justify-between">
                                    <div>
                                        <div className="flex justify-between items-start mb-6">
                                            <div className="w-12 h-12 rounded-2xl bg-gray-100 dark:bg-gray-800 flex items-center justify-center font-black text-gray-400 group-hover:bg-blue-600 group-hover:text-white transition-all shadow-inner uppercase">
                                                {(job.company || job.created_by || 'C').slice(0,1)}
                                            </div>
                                            <span className="text-[9px] font-black px-2 py-1 bg-green-100 text-green-600 rounded-lg border border-green-200 uppercase tracking-widest italic animate-pulse">NEW</span>
                                        </div>
                                        <h3 className="text-lg font-black text-gray-900 dark:text-gray-100 uppercase tracking-tight mb-1 group-hover:text-blue-600 transition-colors line-clamp-1">{job.title}</h3>
                                        <p className="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-widest mb-6">{job.company_name || job.created_by}</p>
                                        
                                        <div className="flex flex-wrap gap-2 mb-8">
                                            {(job.required_skills || []).slice(0, 3).map(s => (
                                              <span key={s} className="text-[8px] font-black px-3 py-1 rounded-full bg-blue-100 text-blue-600 border border-blue-200 uppercase tracking-widest">{s}</span>
                                            ))}
                                        </div>
                                    </div>

                                    <div className="flex justify-between items-center pt-6 border-t border-gray-200 dark:border-gray-700">
                                        <div className="flex items-center gap-3 text-gray-500 dark:text-gray-400 font-bold text-[10px] uppercase">
                                            <span className="flex items-center gap-1"><IconMapPin /> {job.location || 'Remote'}</span>
                                            <span className="flex items-center gap-1"><IconDollar /> {job.salary || 'Comp'}</span>
                                        </div>
                                        <span className="text-blue-600 hover:text-blue-700 font-black text-[10px] uppercase tracking-widest group-hover:translate-x-2 transition-transform">Details →</span>
                                    </div>
                                </Link>
                            ))}
                            {filteredJobs.length === 0 && <div className="col-span-full py-40 text-center text-gray-500 dark:text-gray-400 font-black uppercase tracking-widest italic opacity-50">No opportunities match your search.</div>}
                          </div>
                        )}

                        {/* Pagination */}
                        {totalPages > 1 && (
                            <div className="flex justify-center gap-3 mt-12">
                                <button onClick={() => setCurrentPage(c => Math.max(1, c-1))} className="p-4 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 transition-all"><IconChevronLeft /></button>
                                {[...Array(totalPages)].map((_, i) => (
                                    <button key={i} onClick={() => setCurrentPage(i+1)} className={`w-12 h-12 rounded-2xl font-black text-xs transition-all ${currentPage === i+1 ? 'bg-blue-600 text-white shadow-xl shadow-blue-500/30' : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-500 dark:text-gray-400 hover:text-blue-600 shadow-sm'}`}>{i+1}</button>
                                ))}
                                <button onClick={() => setCurrentPage(c => Math.min(totalPages, c+1))} className="p-4 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 transition-all"><IconChevronRight /></button>
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
}

export default function JobsPage() {
    return (
        <Suspense fallback={<div className="flex min-h-screen items-center justify-center font-black uppercase tracking-widest text-gray-500 dark:text-gray-400 animate-pulse">Initializing Marketplace...</div>}>
            <JobsPageContent />
        </Suspense>
    );
}
