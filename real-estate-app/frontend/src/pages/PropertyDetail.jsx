import { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import {
  MapPin, BedDouble, Maximize2, Building, Phone, Heart,
  ChevronLeft, ChevronRight, Star, Share2, Calendar, CheckCircle
} from 'lucide-react'
import api from '../api/axios'
import { formatPrice } from '../components/PropertyCard'
import MapView from '../components/MapView'
import { useAuth } from '../context/AuthContext'
import { useWishlist } from '../context/WishlistContext'

function Gallery({ images }) {
  const [idx, setIdx] = useState(0)
  if (!images || images.length === 0) return (
    <div className="h-80 bg-gray-200 rounded-2xl flex items-center justify-center text-gray-400">No images</div>
  )
  const prev = () => setIdx(i => (i - 1 + images.length) % images.length)
  const next = () => setIdx(i => (i + 1) % images.length)

  return (
    <div className="space-y-3">
      <div className="relative h-80 md:h-[420px] rounded-2xl overflow-hidden bg-gray-100 group">
        <img src={images[idx]} alt="property" className="w-full h-full object-cover" />
        {images.length > 1 && (
          <>
            <button onClick={prev} className="absolute left-3 top-1/2 -translate-y-1/2 w-10 h-10 bg-black/40 hover:bg-black/60 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
              <ChevronLeft className="w-5 h-5" />
            </button>
            <button onClick={next} className="absolute right-3 top-1/2 -translate-y-1/2 w-10 h-10 bg-black/40 hover:bg-black/60 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
              <ChevronRight className="w-5 h-5" />
            </button>
            <div className="absolute bottom-3 right-3 bg-black/50 text-white text-xs px-2.5 py-1 rounded-full">
              {idx + 1} / {images.length}
            </div>
          </>
        )}
      </div>
      {images.length > 1 && (
        <div className="flex gap-2 overflow-x-auto pb-1">
          {images.map((img, i) => (
            <button key={i} onClick={() => setIdx(i)} className={`flex-shrink-0 w-20 h-16 rounded-lg overflow-hidden border-2 transition-all ${i === idx ? 'border-primary-500 scale-105' : 'border-transparent opacity-60 hover:opacity-100'}`}>
              <img src={img} alt="" className="w-full h-full object-cover" />
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

export default function PropertyDetail() {
  const { id } = useParams()
  const { user } = useAuth()
  const { isFavorited, toggleFavorite } = useWishlist()
  const navigate = useNavigate()
  const [property, setProperty] = useState(null)
  const [loading, setLoading] = useState(true)
  const [contactShown, setContactShown] = useState(false)

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await api.get(`/properties/${id}`)
        setProperty(res.data)
      } catch { navigate('/properties') }
      finally { setLoading(false) }
    }
    fetch()
    window.scrollTo(0, 0)
  }, [id])

  if (loading) return (
    <div className="min-h-screen bg-gray-50 pt-8">
      <div className="page-container space-y-4">
        <div className="skeleton h-10 w-48 rounded-xl" />
        <div className="skeleton h-96 rounded-2xl" />
        <div className="grid md:grid-cols-3 gap-6">
          <div className="md:col-span-2 skeleton h-64 rounded-2xl" />
          <div className="skeleton h-64 rounded-2xl" />
        </div>
      </div>
    </div>
  )

  if (!property) return null

  const favorited = isFavorited(property.id)
  const handleFav = async () => {
    if (!user) { navigate('/login'); return }
    await toggleFavorite(property)
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-16">
      {/* Breadcrumb */}
      <div className="bg-white border-b border-gray-100">
        <div className="page-container py-3 flex items-center gap-2 text-sm text-gray-500">
          <Link to="/" className="hover:text-primary-500 transition-colors">Home</Link>
          <ChevronRight className="w-3.5 h-3.5" />
          <Link to="/properties" className="hover:text-primary-500 transition-colors">Properties</Link>
          <ChevronRight className="w-3.5 h-3.5" />
          <span className="text-gray-700 font-medium truncate max-w-xs">{property.title}</span>
        </div>
      </div>

      <div className="page-container pt-6">
        {/* Title + actions */}
        <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 mb-6">
          <div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-gray-900 mb-2">{property.title}</h1>
            <div className="flex items-center gap-1.5 text-gray-500 text-sm">
              <MapPin className="w-4 h-4 text-primary-400" />
              {property.location}
            </div>
          </div>
          <div className="flex items-center gap-2 flex-shrink-0">
            <button onClick={handleFav} className={`flex items-center gap-1.5 px-4 py-2 rounded-xl border text-sm font-medium transition-all ${favorited ? 'bg-primary-50 border-primary-300 text-primary-600' : 'border-gray-200 text-gray-600 hover:border-primary-300 hover:text-primary-500'}`}>
              <Heart className={`w-4 h-4 ${favorited ? 'fill-current text-primary-500' : ''}`} />
              {favorited ? 'Saved' : 'Save'}
            </button>
            <button className="flex items-center gap-1.5 px-4 py-2 rounded-xl border border-gray-200 text-sm font-medium text-gray-600 hover:border-gray-300 transition-all">
              <Share2 className="w-4 h-4" /> Share
            </button>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Left: Gallery + Details */}
          <div className="lg:col-span-2 space-y-6">
            <Gallery images={property.images} />

            {/* Quick specs */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              {[
                { icon: BedDouble, label: 'BHK', val: property.bhk > 0 ? `${property.bhk} BHK` : 'N/A' },
                { icon: Maximize2, label: 'Area', val: `${property.area_sqft?.toLocaleString()} sqft` },
                { icon: Building, label: 'Type', val: property.type },
                { icon: Star, label: 'Furnishing', val: property.furnishing },
              ].map(({ icon: Icon, label, val }) => (
                <div key={label} className="bg-white rounded-xl p-4 text-center shadow-card">
                  <Icon className="w-5 h-5 text-primary-500 mx-auto mb-2" />
                  <p className="text-xs text-gray-500 mb-1">{label}</p>
                  <p className="font-semibold text-gray-800 text-sm">{val}</p>
                </div>
              ))}
            </div>

            {/* Description */}
            <div className="bg-white rounded-2xl p-6 shadow-card">
              <h2 className="font-bold text-gray-900 mb-3">About this property</h2>
              <p className="text-gray-600 text-sm leading-relaxed">{property.description}</p>
            </div>

            {/* Amenities */}
            {property.amenities?.length > 0 && (
              <div className="bg-white rounded-2xl p-6 shadow-card">
                <h2 className="font-bold text-gray-900 mb-4">Amenities</h2>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                  {property.amenities.map(a => (
                    <div key={a} className="flex items-center gap-2 text-sm text-gray-600">
                      <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0" />
                      {a}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Map */}
            {property.lat && property.lng && (
              <div className="bg-white rounded-2xl p-6 shadow-card">
                <h2 className="font-bold text-gray-900 mb-4">Location on Map</h2>
                <div style={{height: 300}}>
                  <MapView properties={[property]} center={[property.lat, property.lng]} zoom={14} single />
                </div>
              </div>
            )}
          </div>

          {/* Right: Price card */}
          <div className="space-y-4">
            <div className="bg-white rounded-2xl shadow-card p-6 sticky top-24">
              <div className="mb-4">
                <p className="text-3xl font-extrabold text-gray-900">{formatPrice(property.price)}</p>
                {property.area_sqft > 0 && (
                  <p className="text-sm text-gray-500 mt-1">
                    ₹{Math.round(property.price / property.area_sqft).toLocaleString('en-IN')} / sqft
                  </p>
                )}
              </div>

              <div className="space-y-2 mb-6 text-sm text-gray-600">
                <div className="flex justify-between py-2 border-b border-gray-50">
                  <span>Property ID</span>
                  <span className="font-medium text-gray-800">PF-{property.id?.toString().padStart(5, '0')}</span>
                </div>
                <div className="flex justify-between py-2 border-b border-gray-50">
                  <span>Listed</span>
                  <span className="font-medium text-gray-800 flex items-center gap-1"><Calendar className="w-3.5 h-3.5" />{new Date(property.created_at).toLocaleDateString()}</span>
                </div>
                <div className="flex justify-between py-2">
                  <span>City</span>
                  <span className="font-medium text-gray-800">{property.city}</span>
                </div>
              </div>

              {!contactShown ? (
                <button
                  onClick={() => { if (!user) navigate('/login'); else setContactShown(true) }}
                  className="btn-primary w-full justify-center py-3 text-base mb-3"
                >
                  <Phone className="w-4 h-4" /> View Contact
                </button>
              ) : (
                <a href={`tel:${property.owner_contact}`} className="btn-primary w-full justify-center py-3 text-base mb-3 block text-center">
                  <Phone className="w-4 h-4 inline mr-2" />{property.owner_contact}
                </a>
              )}

              <button onClick={handleFav} className={`btn-secondary w-full justify-center py-3 text-sm ${favorited ? 'border-primary-300 text-primary-600' : ''}`}>
                <Heart className={`w-4 h-4 ${favorited ? 'fill-primary-500 text-primary-500' : ''}`} />
                {favorited ? 'Saved to Wishlist' : 'Add to Wishlist'}
              </button>
            </div>

            {/* Back to listings */}
            <Link to="/properties" className="flex items-center gap-2 text-sm text-gray-500 hover:text-primary-500 transition-colors">
              <ChevronLeft className="w-4 h-4" /> Back to listings
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
