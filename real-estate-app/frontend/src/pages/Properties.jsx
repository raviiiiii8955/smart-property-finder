import { useState, useEffect, useCallback } from 'react'
import { useSearchParams } from 'react-router-dom'
import {
  LayoutGrid, List, Map as MapIcon, SlidersHorizontal,
  X, ArrowUpDown, Zap, Database, AlertCircle, ExternalLink
} from 'lucide-react'
import api from '../api/axios'
import PropertyCard from '../components/PropertyCard'
import SkeletonCard from '../components/SkeletonCard'
import FilterSidebar from '../components/FilterSidebar'
import Pagination from '../components/Pagination'
import MapView from '../components/MapView'

const SORT_OPTIONS = [
  { value: 'newest',     label: 'Newest First' },
  { value: 'price_asc',  label: 'Price: Low to High' },
  { value: 'price_desc', label: 'Price: High to Low' },
]

const LIVE_CITIES = [
  'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai',
  'Pune', 'Kolkata', 'Ahmedabad', 'Noida', 'Gurgaon', 'Thane', 'Navi Mumbai',
]

// ── Live Property Card (Housing.com data) ────────────────────────────────────
function LivePropertyCard({ property }) {
  const formatPrice = (p) => {
    if (!p) return 'Price on request'
    if (p >= 10000000) return `₹${(p / 10000000).toFixed(2)} Cr`
    if (p >= 100000)   return `₹${(p / 100000).toFixed(1)} L`
    return `₹${p.toLocaleString('en-IN')}`
  }

  const image = property.images?.[0] ||
    'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=600'

  return (
    <div className="card group block relative">
      {/* Live badge */}
      <div className="absolute top-3 left-3 z-10 flex gap-1.5">
        <span className="flex items-center gap-1 bg-green-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow">
          <Zap className="w-2.5 h-2.5" /> LIVE
        </span>
        <span className="bg-black/60 text-white text-[10px] px-2 py-0.5 rounded-full backdrop-blur-sm">
          housing.com
        </span>
      </div>

      {/* Image */}
      <div className="relative overflow-hidden h-52 bg-gray-100">
        <img
          src={image}
          alt={property.title}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          loading="lazy"
          onError={e => { e.target.src = 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=600' }}
        />
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-3">
          <p className="text-white font-bold text-lg leading-tight">{formatPrice(property.price)}</p>
        </div>
      </div>

      {/* Body */}
      <div className="p-4">
        <h3 className="font-semibold text-gray-900 text-sm leading-snug line-clamp-2 mb-2 group-hover:text-primary-600 transition-colors">
          {property.title}
        </h3>
        <p className="text-xs text-gray-500 mb-3 flex items-center gap-1">
          <span className="w-2 h-2 rounded-full bg-primary-400 flex-shrink-0" />
          <span className="truncate">{property.location}</span>
        </p>

        <div className="flex items-center gap-3 text-xs text-gray-500 pt-3 border-t border-gray-50">
          {property.bhk > 0 && (
            <span className="font-medium text-gray-700">{property.bhk} BHK</span>
          )}
          {property.area_sqft > 0 && (
            <span>{property.area_sqft.toLocaleString()} sqft</span>
          )}
          <span className="ml-auto text-gray-400">{property.type}</span>
        </div>

        {property.source_url && (
          <a
            href={property.source_url}
            target="_blank"
            rel="noopener noreferrer"
            onClick={e => e.stopPropagation()}
            className="mt-3 flex items-center gap-1 text-[11px] text-primary-500 hover:text-primary-700 font-medium"
          >
            <ExternalLink className="w-3 h-3" /> View on housing.com
          </a>
        )}
      </div>
    </div>
  )
}

// ── Main Component ────────────────────────────────────────────────────────────
export default function Properties() {
  const [searchParams] = useSearchParams()

  // Data source toggle
  const [dataSource, setDataSource] = useState('local') // 'local' | 'live'

  // Local DB state
  const [properties, setProperties]   = useState([])
  const [total, setTotal]             = useState(0)
  const [totalPages, setTotalPages]   = useState(1)
  const [loading, setLoading]         = useState(true)
  const [view, setView]               = useState('grid')
  const [mobileSidebar, setMobileSidebar] = useState(false)

  const [filters, setFilters] = useState({
    location:  searchParams.get('location') || '',
    city:      searchParams.get('city') ? [searchParams.get('city')] : [],
    types:     searchParams.get('type')  ? [searchParams.get('type')]  : [],
    furnishing: [],
    bhk:       null,
    min_price: 0,
    max_price: 50000000,
    sort:      'newest',
    page:      1,
  })

  // Live API state
  const [liveProps, setLiveProps]       = useState([])
  const [liveLoading, setLiveLoading]   = useState(false)
  const [liveError, setLiveError]       = useState('')
  const [liveCity, setLiveCity]         = useState('Mumbai')
  const [liveType, setLiveType]         = useState('')
  const [liveTxn, setLiveTxn]           = useState('buy')
  const [livePage, setLivePage]         = useState(1)

  // ── Local fetch ──────────────────────────────────────────────────────────
  const buildQuery = (f) => {
    const p = {}
    if (f.location) p.location = f.location
    if (f.city?.length === 1) p.city = f.city[0]
    if (f.types?.length === 1) p.type = f.types[0]
    if (f.furnishing?.length === 1) p.furnishing = f.furnishing[0]
    if (f.bhk) p.bhk = f.bhk
    if (f.min_price > 0) p.min_price = f.min_price
    if (f.max_price < 50000000) p.max_price = f.max_price
    p.sort = f.sort
    p.page = f.page
    p.per_page = 12
    return p
  }

  const fetchProperties = useCallback(async () => {
    setLoading(true)
    try {
      const res = await api.get('/properties/', { params: buildQuery(filters) })
      setProperties(res.data.properties || [])
      setTotal(res.data.total || 0)
      setTotalPages(res.data.total_pages || 1)
    } catch { setProperties([]) }
    finally { setLoading(false) }
  }, [filters])

  useEffect(() => {
    if (dataSource === 'local') fetchProperties()
  }, [fetchProperties, dataSource])

  // ── Live fetch ───────────────────────────────────────────────────────────
  const fetchLiveProperties = useCallback(async () => {
    setLiveLoading(true)
    setLiveError('')
    try {
      const params = new URLSearchParams({
        city:        liveCity.toLowerCase(),
        transaction: liveTxn,
        page:        livePage,
      })
      if (liveType) params.append('type', liveType.toLowerCase())

      const res = await api.get(`/live/properties?${params.toString()}`)
      const data = res.data

      if (data.error) {
        setLiveError(data.error)
        setLiveProps([])
      } else {
        setLiveProps(data.properties || [])
        if ((data.properties || []).length === 0) {
          setLiveError('No live listings found for this search. Try a different city or type.')
        }
      }
    } catch (err) {
      const msg = err.response?.data?.error || 'Failed to fetch live listings.'
      setLiveError(msg)
      setLiveProps([])
    } finally {
      setLiveLoading(false)
    }
  }, [liveCity, liveType, liveTxn, livePage])

  useEffect(() => {
    if (dataSource === 'live') fetchLiveProperties()
  }, [fetchLiveProperties, dataSource])

  const handleFilterChange = (newFilters) => setFilters({ ...newFilters, page: 1 })
  const handleClear = () => setFilters(prev => ({
    location: '', city: [], types: [], furnishing: [], bhk: null,
    min_price: 0, max_price: 50000000, sort: prev.sort, page: 1,
  }))

  const activeCount = [
    filters.city?.length, filters.types?.length,
    filters.furnishing?.length, filters.bhk != null ? 1 : 0,
  ].reduce((a, b) => a + (b || 0), 0)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ── Top bar ─────────────────────────────────────────────────────── */}
      <div className="bg-white border-b border-gray-100 sticky top-16 z-30">
        <div className="page-container py-3 flex items-center justify-between gap-4 flex-wrap">

          {/* Source toggle */}
          <div className="flex items-center gap-2 bg-gray-100 rounded-xl p-1">
            <button
              onClick={() => setDataSource('local')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all duration-200
                ${dataSource === 'local'
                  ? 'bg-white shadow text-gray-800'
                  : 'text-gray-500 hover:text-gray-700'}`}
            >
              <Database className="w-3.5 h-3.5" /> Local DB
            </button>
            <button
              onClick={() => setDataSource('live')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all duration-200
                ${dataSource === 'live'
                  ? 'bg-green-500 shadow text-white'
                  : 'text-gray-500 hover:text-gray-700'}`}
            >
              <Zap className="w-3.5 h-3.5" />
              Live — housing.com
            </button>
          </div>

          {dataSource === 'local' ? (
            <div className="flex items-center gap-3 text-sm">
              <span className="text-sm text-gray-500">
                <span className="font-semibold text-gray-900">{total.toLocaleString()}</span> properties
              </span>

              {/* Mobile filter */}
              <button
                onClick={() => setMobileSidebar(true)}
                className="lg:hidden flex items-center gap-1.5 border border-gray-200 px-3 py-2 rounded-lg text-gray-600"
              >
                <SlidersHorizontal className="w-4 h-4" />
                Filters {activeCount > 0 && <span className="bg-primary-500 text-white text-xs w-4 h-4 rounded-full flex items-center justify-center">{activeCount}</span>}
              </button>

              {/* Sort */}
              <div className="flex items-center gap-1.5 border border-gray-200 px-3 py-2 rounded-lg">
                <ArrowUpDown className="w-3.5 h-3.5 text-gray-400" />
                <select
                  value={filters.sort}
                  onChange={e => setFilters(f => ({ ...f, sort: e.target.value, page: 1 }))}
                  className="text-sm text-gray-600 focus:outline-none bg-transparent"
                >
                  {SORT_OPTIONS.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
                </select>
              </div>

              {/* View toggle */}
              <div className="flex border border-gray-200 rounded-lg overflow-hidden">
                <button onClick={() => setView('grid')} className={`p-2 ${view === 'grid' ? 'bg-primary-500 text-white' : 'text-gray-500 hover:bg-gray-50'}`}>
                  <LayoutGrid className="w-4 h-4" />
                </button>
                <button onClick={() => setView('map')} className={`p-2 ${view === 'map'  ? 'bg-primary-500 text-white' : 'text-gray-500 hover:bg-gray-50'}`}>
                  <MapIcon className="w-4 h-4" />
                </button>
              </div>
            </div>
          ) : (
            /* ── Live filters ───────────────────────────────────────────── */
            <div className="flex items-center gap-2 flex-wrap text-sm">
              <select
                value={liveCity}
                onChange={e => { setLiveCity(e.target.value); setLivePage(1) }}
                className="border border-gray-200 px-3 py-2 rounded-lg text-gray-700 focus:outline-none focus:border-green-400 text-xs"
              >
                {LIVE_CITIES.map(c => <option key={c} value={c}>{c}</option>)}
              </select>

              <select
                value={liveTxn}
                onChange={e => { setLiveTxn(e.target.value); setLivePage(1) }}
                className="border border-gray-200 px-3 py-2 rounded-lg text-gray-700 focus:outline-none focus:border-green-400 text-xs"
              >
                <option value="buy">Buy</option>
                <option value="rent">Rent</option>
              </select>

              <select
                value={liveType}
                onChange={e => { setLiveType(e.target.value); setLivePage(1) }}
                className="border border-gray-200 px-3 py-2 rounded-lg text-gray-700 focus:outline-none focus:border-green-400 text-xs"
              >
                <option value="">All Types</option>
                <option value="apartment">Apartment</option>
                <option value="villa">Villa</option>
                <option value="plot">Plot</option>
                <option value="commercial">Commercial</option>
              </select>

              <button
                onClick={() => fetchLiveProperties()}
                disabled={liveLoading}
                className="flex items-center gap-1.5 bg-green-500 hover:bg-green-600 text-white text-xs font-semibold px-3 py-2 rounded-lg transition-colors disabled:opacity-60"
              >
                <Zap className="w-3.5 h-3.5" />
                {liveLoading ? 'Fetching…' : 'Fetch Live'}
              </button>

              {liveProps.length > 0 && (
                <span className="text-xs text-gray-500">
                  <span className="font-semibold text-gray-800">{liveProps.length}</span> live results
                </span>
              )}
            </div>
          )}
        </div>
      </div>

      {/* ── Body ────────────────────────────────────────────────────────── */}
      <div className="page-container py-6 flex gap-6">
        {/* Sidebar — only for local mode */}
        {dataSource === 'local' && (
          <>
            <div className="hidden lg:block w-72 flex-shrink-0">
              <FilterSidebar filters={filters} onChange={handleFilterChange} onClear={handleClear} />
            </div>
            {mobileSidebar && (
              <div className="fixed inset-0 z-50 lg:hidden">
                <div className="absolute inset-0 bg-black/40" onClick={() => setMobileSidebar(false)} />
                <div className="absolute right-0 top-0 bottom-0 w-80 bg-white shadow-xl overflow-y-auto p-4">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-bold">Filters</h3>
                    <button onClick={() => setMobileSidebar(false)}><X className="w-5 h-5" /></button>
                  </div>
                  <FilterSidebar
                    filters={filters}
                    onChange={(f) => { handleFilterChange(f); setMobileSidebar(false) }}
                    onClear={handleClear}
                  />
                </div>
              </div>
            )}
          </>
        )}

        {/* Main grid */}
        <div className="flex-1 min-w-0">
          {/* ── LOCAL mode ─────────────────────────────────────────────── */}
          {dataSource === 'local' && (
            <>
              {view === 'grid' ? (
                <>
                  {loading ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
                      {Array.from({ length: 12 }).map((_, i) => <SkeletonCard key={i} />)}
                    </div>
                  ) : properties.length === 0 ? (
                    <div className="flex flex-col items-center justify-center py-20 text-gray-400">
                      <SlidersHorizontal className="w-8 h-8 mb-4" />
                      <p className="font-semibold text-gray-600 mb-1">No properties found</p>
                      <button onClick={handleClear} className="btn-primary mt-4 text-sm">Clear Filters</button>
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5 animate-fade-in">
                      {properties.map(p => <PropertyCard key={p.id} property={p} />)}
                    </div>
                  )}
                  <Pagination
                    page={filters.page}
                    totalPages={totalPages}
                    onChange={p => setFilters(f => ({ ...f, page: p }))}
                  />
                </>
              ) : (
                <div style={{ height: '70vh' }} className="rounded-2xl overflow-hidden shadow-card">
                  <MapView properties={properties} zoom={10} />
                </div>
              )}
            </>
          )}

          {/* ── LIVE mode ──────────────────────────────────────────────── */}
          {dataSource === 'live' && (
            <>
              {/* Info banner */}
              <div className="mb-5 flex items-start gap-3 bg-green-50 border border-green-200 rounded-xl p-4 text-sm">
                <Zap className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-semibold text-green-800">Live Data from housing.com</p>
                  <p className="text-green-700 text-xs mt-0.5">
                    Real property listings fetched in real-time via the Housing API (RapidAPI).
                    Select a city, type, and click <strong>Fetch Live</strong>.
                  </p>
                </div>
              </div>

              {liveLoading ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
                  {Array.from({ length: 9 }).map((_, i) => <SkeletonCard key={i} />)}
                </div>
              ) : liveError ? (
                <div className="flex flex-col items-center justify-center py-20 text-center">
                  <div className="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mb-4">
                    <AlertCircle className="w-8 h-8 text-red-400" />
                  </div>
                  <p className="font-semibold text-gray-700 mb-2">Could not fetch live data</p>
                  <p className="text-sm text-gray-500 max-w-md">{liveError}</p>
                  {liveError.includes('RAPIDAPI_KEY') && (
                    <div className="mt-4 bg-amber-50 border border-amber-200 rounded-xl p-4 text-left max-w-md text-xs text-amber-800">
                      <p className="font-semibold mb-1">⚙️ Setup Required</p>
                      <p>Add your RapidAPI key to the backend <code className="bg-amber-100 px-1 rounded">.env</code> file:</p>
                      <pre className="mt-2 bg-amber-100 rounded p-2 font-mono">RAPIDAPI_KEY=your_key_here</pre>
                      <p className="mt-2">Then restart the backend server.</p>
                    </div>
                  )}
                  <button
                    onClick={fetchLiveProperties}
                    className="mt-4 flex items-center gap-1.5 bg-green-500 text-white text-sm font-semibold px-4 py-2 rounded-lg hover:bg-green-600"
                  >
                    <Zap className="w-4 h-4" /> Try Again
                  </button>
                </div>
              ) : liveProps.length === 0 ? (
                <div className="flex flex-col items-center justify-center py-20 text-gray-400">
                  <Zap className="w-8 h-8 mb-4 text-green-300" />
                  <p className="font-semibold text-gray-600 mb-1">Select a city and click Fetch Live</p>
                  <p className="text-sm">Live listings from housing.com will appear here</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5 animate-fade-in">
                  {liveProps.map((p, i) => <LivePropertyCard key={p.id || i} property={p} />)}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  )
}
