import { useState, useMemo } from 'react';
import type { Tool } from '../lib/tools';

interface Props {
  tools: Tool[];
  categories: string[];
  languages: string[];
}

export default function ToolSearch({ tools, categories, languages }: Props) {
  const [query, setQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedLang, setSelectedLang] = useState<string | null>(null);
  const [selectedRisk, setSelectedRisk] = useState<string | null>(null);

  const risks = ['low', 'medium', 'high', 'critical'];

  const filtered = useMemo(() => {
    return tools.filter((tool) => {
      if (query) {
        const q = query.toLowerCase();
        const match =
          tool.name.toLowerCase().includes(q) ||
          tool.binary.toLowerCase().includes(q) ||
          tool.description.toLowerCase().includes(q) ||
          tool.category.some((c) => c.toLowerCase().includes(q)) ||
          (tool.aliases?.some((a) => a.toLowerCase().includes(q)) ?? false);
        if (!match) return false;
      }
      if (selectedCategory && !tool.category.includes(selectedCategory)) return false;
      if (selectedLang && !tool.lang.includes(selectedLang) && !tool.lang.includes('all')) return false;
      if (selectedRisk && tool.risk !== selectedRisk) return false;
      return true;
    });
  }, [tools, query, selectedCategory, selectedLang, selectedRisk]);

  return (
    <div>
      {/* Search */}
      <div className="relative mb-6">
        <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          type="text"
          placeholder="Search tools, categories, commands..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full pl-10 pr-4 py-3 rounded-xl border bg-white/80 dark:bg-white/[0.03] border-gray-200 dark:border-white/10 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500/40 backdrop-blur-sm transition-all"
        />
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2 mb-6">
        <FilterGroup
          label="Category"
          options={categories}
          selected={selectedCategory}
          onSelect={setSelectedCategory}
        />
        <FilterGroup
          label="Language"
          options={languages}
          selected={selectedLang}
          onSelect={setSelectedLang}
        />
        <FilterGroup
          label="Risk"
          options={risks}
          selected={selectedRisk}
          onSelect={setSelectedRisk}
          colorMap={{
            low: 'text-emerald-600 dark:text-emerald-400',
            medium: 'text-amber-600 dark:text-amber-400',
            high: 'text-orange-600 dark:text-orange-400',
            critical: 'text-red-600 dark:text-red-400',
          }}
        />
      </div>

      {/* Results count */}
      <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
        {filtered.length} tool{filtered.length !== 1 ? 's' : ''}
        {query || selectedCategory || selectedLang || selectedRisk ? ' matched' : ' total'}
      </p>

      {/* Tool grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((tool) => (
          <ToolCard key={tool.slug} tool={tool} />
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-16 text-gray-400 dark:text-gray-500">
          <p className="text-lg">No tools found</p>
          <p className="text-sm mt-1">Try adjusting your filters</p>
        </div>
      )}
    </div>
  );
}

function FilterGroup({
  label,
  options,
  selected,
  onSelect,
  colorMap,
}: {
  label: string;
  options: string[];
  selected: string | null;
  onSelect: (value: string | null) => void;
  colorMap?: Record<string, string>;
}) {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm border transition-all ${
          selected
            ? 'border-blue-500/40 bg-blue-500/10 text-blue-600 dark:text-blue-400'
            : 'border-gray-200 dark:border-white/10 text-gray-600 dark:text-gray-400 hover:border-gray-300 dark:hover:border-white/20'
        }`}
      >
        {label}
        {selected && <span className="font-medium">: {selected}</span>}
        <svg className={`w-3.5 h-3.5 transition-transform ${open ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {open && (
        <>
          <div className="fixed inset-0 z-10" onClick={() => setOpen(false)} />
          <div className="absolute top-full left-0 mt-1 z-20 min-w-[160px] py-1 rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-gray-900 shadow-xl backdrop-blur-xl">
            {selected && (
              <button
                onClick={() => { onSelect(null); setOpen(false); }}
                className="w-full text-left px-3 py-1.5 text-sm text-gray-400 hover:bg-gray-50 dark:hover:bg-white/5"
              >
                Clear
              </button>
            )}
            {options.map((opt) => (
              <button
                key={opt}
                onClick={() => { onSelect(opt); setOpen(false); }}
                className={`w-full text-left px-3 py-1.5 text-sm hover:bg-gray-50 dark:hover:bg-white/5 ${
                  colorMap?.[opt] ?? 'text-gray-700 dark:text-gray-300'
                } ${selected === opt ? 'font-medium' : ''}`}
              >
                {opt}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

function ToolCard({ tool }: { tool: Tool }) {
  const riskClass: Record<string, string> = {
    low: 'chip-risk-low',
    medium: 'chip-risk-medium',
    high: 'chip-risk-high',
    critical: 'chip-risk-critical',
  };

  return (
    <a
      href={`/tools/${tool.slug}`}
      className="glass-card p-4 block group cursor-pointer"
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <h3 className="font-mono font-semibold text-base text-gray-900 dark:text-gray-100 group-hover:text-blue-500 dark:group-hover:text-blue-400 transition-colors">
          {tool.binary}
        </h3>
        <span className={`chip ${riskClass[tool.risk] ?? 'chip-default'}`}>
          {tool.risk}
        </span>
      </div>

      <p className="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
        {tool.description}
      </p>

      <div className="flex flex-wrap gap-1.5">
        {tool.category.slice(0, 3).map((cat) => (
          <span key={cat} className="chip chip-default text-[11px]">{cat}</span>
        ))}
        {!tool.lang.includes('all') && tool.lang.slice(0, 2).map((l) => (
          <span key={l} className="chip chip-default text-[11px]">{l}</span>
        ))}
        {tool.effects?.slice(0, 2).map((eff) => (
          <span key={eff} className="chip chip-default text-[11px]">{eff}</span>
        ))}
      </div>
    </a>
  );
}
