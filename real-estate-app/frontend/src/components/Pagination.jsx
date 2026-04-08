import { ChevronLeft, ChevronRight } from 'lucide-react'

export default function Pagination({ page, totalPages, onChange }) {
  if (totalPages <= 1) return null

  const pages = []
  const delta = 1
  for (let i = Math.max(1, page - delta); i <= Math.min(totalPages, page + delta); i++) {
    pages.push(i)
  }
  const showLeftDots = pages[0] > 2
  const showRightDots = pages[pages.length - 1] < totalPages - 1

  return (
    <div className="flex items-center justify-center gap-1 mt-8">
      <button
        onClick={() => onChange(page - 1)}
        disabled={page === 1}
        className="w-9 h-9 flex items-center justify-center rounded-lg border border-gray-200 text-gray-500 hover:border-primary-400 hover:text-primary-500 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
      >
        <ChevronLeft className="w-4 h-4" />
      </button>

      {pages[0] > 1 && (
        <button onClick={() => onChange(1)} className="w-9 h-9 flex items-center justify-center rounded-lg border border-gray-200 text-sm hover:border-primary-400 hover:text-primary-500 transition-all">1</button>
      )}
      {showLeftDots && <span className="w-9 text-center text-gray-400">…</span>}

      {pages.map(p => (
        <button
          key={p}
          onClick={() => onChange(p)}
          className={`w-9 h-9 flex items-center justify-center rounded-lg border text-sm font-medium transition-all ${
            p === page
              ? 'bg-primary-500 border-primary-500 text-white shadow'
              : 'border-gray-200 text-gray-600 hover:border-primary-400 hover:text-primary-500'
          }`}
        >
          {p}
        </button>
      ))}

      {showRightDots && <span className="w-9 text-center text-gray-400">…</span>}
      {pages[pages.length - 1] < totalPages && (
        <button onClick={() => onChange(totalPages)} className="w-9 h-9 flex items-center justify-center rounded-lg border border-gray-200 text-sm hover:border-primary-400 hover:text-primary-500 transition-all">{totalPages}</button>
      )}

      <button
        onClick={() => onChange(page + 1)}
        disabled={page === totalPages}
        className="w-9 h-9 flex items-center justify-center rounded-lg border border-gray-200 text-gray-500 hover:border-primary-400 hover:text-primary-500 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
      >
        <ChevronRight className="w-4 h-4" />
      </button>
    </div>
  )
}
