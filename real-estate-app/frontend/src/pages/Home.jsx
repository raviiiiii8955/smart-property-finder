import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, MapPin, TrendingUp, Building2, Home as HomeIcon, TreePine, Store, ChevronRight, Star, Shield, Zap } from 'lucide-react'
import api from '../api/axios'
import PropertyCard from '../components/PropertyCard'
import SkeletonCard from '../components/SkeletonCard'

const HERO_CITIES = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Pune', 'Noida', 'Gurgaon']

const STATS = [
  { label: 'Properties Listed', value: '10,000+' },
  { label: 'Happy Buyers', value: '50,000+' },
  { label: 'Cities Covered', value: '50+' },
  { label: 'Trusted Agents', value: '5,000+' },
]

const QUICK_LINKS = [
  { icon: HomeIcon, label: 'Apartments', query: '?type=Apartment', color: 'bg-blue-50 text-blue-600' },
  { icon: Building2, label: 'Villas', query: '?type=Villa', color: 'bg-purple-50 text-purple-600' },
  { icon: TreePine, label: 'Plots', query: '?type=Plot', color: 'bg-green-50 text-green-600' },
  { icon: Store, label: 'Commercial', query: '?type=Commercial', color: 'bg-orange-50 text-orange-600' },
]

const WHY_US = [
  { icon: Shield, title: 'Verified Listings', desc: 'All properties are manually verified by our team.' },
  { icon: Zap, title: 'Instant Connect', desc: 'Get in touch with owners within minutes.' },
  { icon: Star, title: 'Best Deals', desc: 'Exclusive deals you won\'t find anywhere else.' },
]

export default function Home() {
  const navigate = useNavigate()
  const [query, setQuery] = useState('')
  const [selectedCity, setSelectedCity] = useState('')
  const [featured, setFeatured] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchFeatured = async () => {
      try {
        const res = await api.get('/properties/?per_page=6&sort=newest')
        setFeatured(res.data.properties || [])
      } catch { setFeatured([]) }
      finally { setLoading(false) }
    }
    fetchFeatured()
  }, [])

  const handleSearch = (e) => {
    e.preventDefault()
    const params = new URLSearchParams()
    if (query) params.set('location', query)
    if (selectedCity) params.set('city', selectedCity)
    navigate(`/properties?${params.toString()}`)
  }

  return (
    <div className="min-h-screen">
      {/* HERO */}
      <section className="relative bg-gradient-to-br from-brand-dark via-brand-navy to-gray-900 pt-16 pb-24 text-white overflow-hidden">
        {/* Background pattern */}
        <div className="absolute inset-0 opacity-10" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
        }} />
        <div className="page-container relative z-10 text-center">
          <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm border border-white/20 text-white text-sm font-medium px-4 py-2 rounded-full mb-6">
            <TrendingUp className="w-4 h-4 text-primary-400" />
            India's Fastest Growing Property Platform
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold mb-4 leading-tight">
            Find Your <span className="text-transparent bg-clip-text" style={{backgroundImage:'linear-gradient(135deg,#ff6624,#ff9e72)'}}>Dream</span> Home
          </h1>
          <p className="text-gray-300 text-lg mb-10 max-w-2xl mx-auto">
            Explore thousands of verified properties across India. Buy, rent, or invest with confidence.
          </p>

          {/* Search Box */}
          <form onSubmit={handleSearch} className="max-w-3xl mx-auto bg-white rounded-2xl shadow-2xl p-3 flex flex-col sm:flex-row gap-2">
            <div className="relative flex-1">
              <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search by city, locality or project name..."
                value={query}
                onChange={e => setQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-3 text-gray-800 text-sm focus:outline-none rounded-xl"
              />
            </div>
            <select
              value={selectedCity}
              onChange={e => setSelectedCity(e.target.value)}
              className="text-sm text-gray-600 border-l border-gray-100 pl-3 pr-4 py-3 focus:outline-none bg-transparent"
            >
              <option value="">All Cities</option>
              {HERO_CITIES.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
            <button type="submit" className="btn-primary whitespace-nowrap flex-shrink-0">
              <Search className="w-4 h-4" /> Search
            </button>
          </form>

          {/* Quick city links */}
          <div className="flex flex-wrap justify-center gap-2 mt-6">
            {HERO_CITIES.slice(0, 6).map(c => (
              <button
                key={c}
                onClick={() => navigate(`/properties?city=${c}`)}
                className="text-xs text-gray-300 hover:text-white bg-white/10 hover:bg-white/20 backdrop-blur-sm px-3 py-1.5 rounded-full transition-all border border-white/10"
              >
                {c}
              </button>
            ))}
          </div>
        </div>

        {/* Stats band */}
        <div className="page-container mt-12 relative z-10">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {STATS.map((s, i) => (
              <div key={i} className="bg-white/10 backdrop-blur-sm border border-white/10 rounded-2xl p-4 text-center">
                <p className="text-2xl font-extrabold text-white">{s.value}</p>
                <p className="text-xs text-gray-400 mt-1">{s.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Quick Links */}
      <section className="page-container py-12">
        <h2 className="section-title text-center mb-2">Browse by Property Type</h2>
        <p className="text-gray-500 text-sm text-center mb-8">Find exactly what you're looking for</p>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {QUICK_LINKS.map(({ icon: Icon, label, query: q, color }) => (
            <button
              key={label}
              onClick={() => navigate(`/properties${q}`)}
              className="flex flex-col items-center gap-3 p-6 bg-white rounded-2xl shadow-card hover:shadow-card-hover hover:-translate-y-1 transition-all duration-300 group"
            >
              <div className={`w-14 h-14 ${color} rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform`}>
                <Icon className="w-7 h-7" />
              </div>
              <span className="font-semibold text-gray-800 text-sm">{label}</span>
              <span className="text-xs text-gray-400 flex items-center gap-1">
                Browse <ChevronRight className="w-3 h-3" />
              </span>
            </button>
          ))}
        </div>
      </section>

      {/* Featured Listings */}
      <section className="bg-gray-50 py-12">
        <div className="page-container">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="section-title">Latest Properties</h2>
              <p className="text-gray-500 text-sm mt-1">Freshly listed, handpicked for you</p>
            </div>
            <button onClick={() => navigate('/properties')} className="btn-outline text-sm hidden sm:flex">
              View All <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {loading
              ? Array.from({length: 6}).map((_, i) => <SkeletonCard key={i} />)
              : featured.map(p => <PropertyCard key={p.id} property={p} />)
            }
          </div>

          <div className="text-center mt-8 sm:hidden">
            <button onClick={() => navigate('/properties')} className="btn-primary">
              View All Properties
            </button>
          </div>
        </div>
      </section>

      {/* Why Us */}
      <section className="page-container py-16">
        <h2 className="section-title text-center mb-2">Why Choose PropFinder?</h2>
        <p className="text-gray-500 text-sm text-center mb-10">Trusted by millions across India</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {WHY_US.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="text-center p-8 bg-white rounded-2xl shadow-card hover:shadow-card-hover transition-all">
              <div className="w-16 h-16 price-gradient rounded-2xl flex items-center justify-center mx-auto mb-4 shadow">
                <Icon className="w-8 h-8 text-white" />
              </div>
              <h3 className="font-bold text-gray-900 mb-2">{title}</h3>
              <p className="text-gray-500 text-sm leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-brand-dark text-gray-400 py-8 text-center text-sm">
        <div className="page-container">
          <p className="font-extrabold text-white text-xl mb-2">
            <span className="text-primary-400">Prop</span>Finder
          </p>
          <p>© 2024 PropFinder. India's Premium Real Estate Platform.</p>
        </div>
      </footer>
    </div>
  )
}
