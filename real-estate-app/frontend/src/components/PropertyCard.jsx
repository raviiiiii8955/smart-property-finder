import { Link } from 'react-router-dom'
import { Heart, MapPin, BedDouble, Maximize2, Building } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { useWishlist } from '../context/WishlistContext'

export function formatPrice(price) {
  if (price >= 10000000) return `₹${(price / 10000000).toFixed(2)} Cr`
  if (price >= 100000) return `₹${(price / 100000).toFixed(2)} L`
  return `₹${price.toLocaleString('en-IN')}`
}

export function furnishingColor(f) {
  if (f === 'Furnished') return 'tag-green'
  if (f === 'Semi-Furnished') return 'tag-blue'
  return 'tag-gray'
}

export default function PropertyCard({ property }) {
  const { user } = useAuth()
  const { isFavorited, toggleFavorite } = useWishlist()
  const favorited = isFavorited(property.id)
  const image = property.images?.[0] || 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=600'

  const handleFav = async (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (!user) { window.location.href = '/login'; return }
    await toggleFavorite(property)
  }

  return (
    <Link to={`/properties/${property.id}`} className="card group block">
      {/* Image */}
      <div className="relative overflow-hidden h-52 bg-gray-100">
        <img
          src={image}
          alt={property.title}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          loading="lazy"
          onError={e => { e.target.src = 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=600' }}
        />
        {/* Overlay badges */}
        <div className="absolute top-3 left-3 flex gap-2 flex-wrap">
          <span className={`tag ${furnishingColor(property.furnishing)}`}>
            {property.furnishing}
          </span>
          {property.type === 'Villa' && (
            <span className="tag bg-purple-50 text-purple-700">Villa</span>
          )}
        </div>
        {/* Save button */}
        <button
          onClick={handleFav}
          className={`absolute top-3 right-3 w-8 h-8 rounded-full flex items-center justify-center transition-all duration-200 shadow-md
            ${favorited
              ? 'bg-primary-500 text-white scale-110'
              : 'bg-white text-gray-400 hover:text-primary-500 hover:scale-110'
            }`}
        >
          <Heart className={`w-4 h-4 ${favorited ? 'fill-current' : ''}`} />
        </button>
        {/* Price tag */}
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-3">
          <p className="text-white font-bold text-lg leading-tight">{formatPrice(property.price)}</p>
        </div>
      </div>

      {/* Body */}
      <div className="p-4">
        <h3 className="font-semibold text-gray-900 text-sm leading-snug line-clamp-2 mb-2 group-hover:text-primary-600 transition-colors">
          {property.title}
        </h3>
        <div className="flex items-center gap-1 text-gray-500 text-xs mb-3">
          <MapPin className="w-3.5 h-3.5 flex-shrink-0 text-primary-400" />
          <span className="truncate">{property.location}</span>
        </div>

        {/* Specs */}
        <div className="flex items-center gap-3 text-xs text-gray-500 pt-3 border-t border-gray-50">
          {property.bhk > 0 && (
            <div className="flex items-center gap-1">
              <BedDouble className="w-3.5 h-3.5 text-gray-400" />
              <span className="font-medium text-gray-700">{property.bhk} BHK</span>
            </div>
          )}
          {property.area_sqft > 0 && (
            <div className="flex items-center gap-1">
              <Maximize2 className="w-3.5 h-3.5 text-gray-400" />
              <span>{property.area_sqft.toLocaleString()} sqft</span>
            </div>
          )}
          <div className="flex items-center gap-1 ml-auto">
            <Building className="w-3.5 h-3.5 text-gray-400" />
            <span>{property.type}</span>
          </div>
        </div>
      </div>
    </Link>
  )
}
