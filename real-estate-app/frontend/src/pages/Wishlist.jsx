import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Heart, Trash2, MapPin, BedDouble, Maximize2 } from 'lucide-react'
import { useWishlist } from '../context/WishlistContext'
import { useAuth } from '../context/AuthContext'
import { formatPrice } from '../components/PropertyCard'
import SkeletonCard from '../components/SkeletonCard'

export default function Wishlist() {
  const { user } = useAuth()
  const { wishlist, loading, toggleFavorite, fetchWishlist } = useWishlist()

  useEffect(() => { fetchWishlist() }, [])

  if (loading) return (
    <div className="min-h-screen bg-gray-50 pt-8">
      <div className="page-container">
        <div className="skeleton h-8 w-48 rounded mb-6" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {Array.from({length: 6}).map((_, i) => <SkeletonCard key={i} />)}
        </div>
      </div>
    </div>
  )

  if (wishlist.length === 0) return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center px-4">
        <div className="w-24 h-24 bg-primary-50 rounded-full flex items-center justify-center mx-auto mb-6">
          <Heart className="w-10 h-10 text-primary-300" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Your wishlist is empty</h2>
        <p className="text-gray-500 mb-6">Start saving properties you love to view them later</p>
        <Link to="/properties" className="btn-primary">Browse Properties</Link>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="page-container">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-extrabold text-gray-900 flex items-center gap-2">
              <Heart className="w-6 h-6 text-primary-500 fill-primary-500" /> Saved Properties
            </h1>
            <p className="text-gray-500 text-sm mt-1">{wishlist.length} propert{wishlist.length !== 1 ? 'ies' : 'y'} saved</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {wishlist.map(property => (
            <div key={property.id} className="card group">
              <Link to={`/properties/${property.id}`}>
                <div className="relative h-48 overflow-hidden bg-gray-100">
                  <img
                    src={property.images?.[0] || 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=600'}
                    alt={property.title}
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                    onError={e => { e.target.src = 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=600' }}
                  />
                  <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-3">
                    <p className="text-white font-bold text-lg">{formatPrice(property.price)}</p>
                  </div>
                </div>
              </Link>
              <div className="p-4">
                <Link to={`/properties/${property.id}`}>
                  <h3 className="font-semibold text-gray-900 text-sm line-clamp-2 mb-2 hover:text-primary-500 transition-colors">{property.title}</h3>
                </Link>
                <div className="flex items-center gap-1 text-gray-500 text-xs mb-3">
                  <MapPin className="w-3.5 h-3.5 text-primary-400" />
                  <span className="truncate">{property.location}</span>
                </div>
                <div className="flex items-center gap-3 text-xs text-gray-500 pt-3 border-t border-gray-50">
                  {property.bhk > 0 && <span className="flex items-center gap-1"><BedDouble className="w-3.5 h-3.5" />{property.bhk} BHK</span>}
                  {property.area_sqft > 0 && <span className="flex items-center gap-1"><Maximize2 className="w-3.5 h-3.5" />{property.area_sqft} sqft</span>}
                  <button
                    onClick={() => toggleFavorite(property)}
                    className="ml-auto flex items-center gap-1 text-red-400 hover:text-red-600 transition-colors font-medium"
                  >
                    <Trash2 className="w-3.5 h-3.5" /> Remove
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
