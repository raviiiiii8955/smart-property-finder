import { useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import { Link } from 'react-router-dom'
import { formatPrice } from './PropertyCard'

// Fix leaflet default icon
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

const priceIcon = (price) => L.divIcon({
  className: '',
  html: `<div style="background: linear-gradient(135deg,#ff6624,#cc0000); color:white; padding:4px 8px; border-radius:20px; font-size:11px; font-weight:700; white-space:nowrap; box-shadow:0 2px 8px rgba(0,0,0,0.3)">
    ${formatPrice(price)}
  </div>`,
  iconAnchor: [30, 15],
})

export default function MapView({ properties, center, zoom = 11, single = false }) {
  const mapCenter = center || (properties?.[0] ? [properties[0].lat, properties[0].lng] : [20.5937, 78.9629])

  if (!properties || properties.length === 0) return (
    <div className="flex items-center justify-center h-full bg-gray-100 rounded-xl text-gray-400 text-sm">
      No map data available
    </div>
  )

  return (
    <MapContainer center={mapCenter} zoom={zoom} className="w-full h-full rounded-xl z-0"
      scrollWheelZoom={false} style={{ minHeight: 300 }}>
      <TileLayer
        attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {properties.map(p => (
        p.lat && p.lng ? (
          <Marker key={p.id} position={[p.lat, p.lng]} icon={priceIcon(p.price)}>
            <Popup>
              <div className="text-sm min-w-[160px]">
                <p className="font-semibold text-gray-800 mb-1 leading-tight">{p.title}</p>
                <p className="text-primary-500 font-bold">{formatPrice(p.price)}</p>
                <p className="text-gray-500 text-xs mt-1">{p.location}</p>
                {!single && (
                  <Link to={`/properties/${p.id}`} className="text-primary-500 text-xs font-medium hover:underline mt-2 block">
                    View Details →
                  </Link>
                )}
              </div>
            </Popup>
          </Marker>
        ) : null
      ))}
    </MapContainer>
  )
}
