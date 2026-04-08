import { useState } from 'react'
import { SlidersHorizontal, X, ChevronDown, ChevronUp } from 'lucide-react'

const TYPES = ['Apartment', 'Villa', 'Plot', 'Commercial']
const FURNISHING = ['Furnished', 'Semi-Furnished', 'Unfurnished']
const BHKS = [1, 2, 3, 4, 5]
const CITIES = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Pune', 'Noida', 'Gurgaon']

function Section({ title, children, defaultOpen = true }) {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <div className="border-b border-gray-100 pb-4 mb-4">
      <button onClick={() => setOpen(!open)} className="w-full flex items-center justify-between mb-3 text-sm font-semibold text-gray-800">
        {title}
        {open ? <ChevronUp className="w-4 h-4 text-gray-400" /> : <ChevronDown className="w-4 h-4 text-gray-400" />}
      </button>
      {open && children}
    </div>
  )
}

export default function FilterSidebar({ filters, onChange, onClear }) {
  const MAX_PRICE = 50000000

  const handleCheckbox = (key, value) => {
    const current = filters[key] || []
    const updated = current.includes(value)
      ? current.filter(v => v !== value)
      : [...current, value]
    onChange({ ...filters, [key]: updated, page: 1 })
  }

  const handleBHK = (b) => {
    const current = filters.bhk === b ? null : b
    onChange({ ...filters, bhk: current, page: 1 })
  }

  const activeCount = [
    filters.city?.length,
    filters.types?.length,
    filters.furnishing?.length,
    filters.bhk != null ? 1 : 0,
    (filters.min_price && filters.min_price > 0) ? 1 : 0,
  ].reduce((a, b) => a + (b || 0), 0)

  const formatPriceLabel = (val) => {
    if (val >= 10000000) return `₹${(val / 10000000).toFixed(1)} Cr`
    if (val >= 100000) return `₹${(val / 100000).toFixed(0)} L`
    return `₹${val}`
  }

  return (
    <aside className="bg-white rounded-2xl shadow-card p-5 sticky top-20 h-fit">
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2">
          <SlidersHorizontal className="w-4 h-4 text-primary-500" />
          <h2 className="font-bold text-gray-900 text-sm">Filters</h2>
          {activeCount > 0 && (
            <span className="bg-primary-100 text-primary-600 text-xs font-bold px-2 py-0.5 rounded-full">{activeCount}</span>
          )}
        </div>
        {activeCount > 0 && (
          <button onClick={onClear} className="text-xs text-primary-500 hover:text-primary-700 font-medium flex items-center gap-1">
            <X className="w-3 h-3" /> Clear all
          </button>
        )}
      </div>

      {/* City */}
      <Section title="City">
        <div className="grid grid-cols-2 gap-1.5">
          {CITIES.map(c => (
            <label key={c} className="flex items-center gap-2 cursor-pointer group">
              <input
                type="checkbox"
                checked={(filters.city || []).includes(c)}
                onChange={() => handleCheckbox('city', c)}
                className="accent-primary-500 w-3.5 h-3.5 rounded"
              />
              <span className="text-xs text-gray-600 group-hover:text-primary-500 transition-colors">{c}</span>
            </label>
          ))}
        </div>
      </Section>

      {/* Budget */}
      <Section title="Budget">
        <div className="space-y-3">
          <div className="flex justify-between text-xs text-gray-500">
            <span>{formatPriceLabel(filters.min_price || 0)}</span>
            <span>{formatPriceLabel(filters.max_price || MAX_PRICE)}</span>
          </div>
          <div className="space-y-2">
            <label className="text-xs text-gray-500">Min Price</label>
            <input
              type="range" min={0} max={MAX_PRICE} step={500000}
              value={filters.min_price || 0}
              onChange={e => onChange({ ...filters, min_price: +e.target.value, page: 1 })}
              className="w-full"
            />
            <label className="text-xs text-gray-500">Max Price</label>
            <input
              type="range" min={0} max={MAX_PRICE} step={500000}
              value={filters.max_price || MAX_PRICE}
              onChange={e => onChange({ ...filters, max_price: +e.target.value, page: 1 })}
              className="w-full"
            />
          </div>
        </div>
      </Section>

      {/* BHK */}
      <Section title="BHK Type">
        <div className="flex flex-wrap gap-2">
          {BHKS.map(b => (
            <button
              key={b}
              onClick={() => handleBHK(b)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
                filters.bhk === b
                  ? 'bg-primary-500 border-primary-500 text-white'
                  : 'border-gray-200 text-gray-600 hover:border-primary-300 hover:text-primary-500'
              }`}
            >
              {b} BHK
            </button>
          ))}
        </div>
      </Section>

      {/* Property Type */}
      <Section title="Property Type">
        <div className="space-y-2">
          {TYPES.map(t => (
            <label key={t} className="flex items-center gap-2 cursor-pointer group">
              <input
                type="checkbox"
                checked={(filters.types || []).includes(t)}
                onChange={() => handleCheckbox('types', t)}
                className="accent-primary-500 w-3.5 h-3.5 rounded"
              />
              <span className="text-xs text-gray-600 group-hover:text-primary-500 transition-colors">{t}</span>
            </label>
          ))}
        </div>
      </Section>

      {/* Furnishing */}
      <Section title="Furnishing" defaultOpen={false}>
        <div className="space-y-2">
          {FURNISHING.map(f => (
            <label key={f} className="flex items-center gap-2 cursor-pointer group">
              <input
                type="checkbox"
                checked={(filters.furnishing || []).includes(f)}
                onChange={() => handleCheckbox('furnishing', f)}
                className="accent-primary-500 w-3.5 h-3.5 rounded"
              />
              <span className="text-xs text-gray-600 group-hover:text-primary-500 transition-colors">{f}</span>
            </label>
          ))}
        </div>
      </Section>
    </aside>
  )
}
