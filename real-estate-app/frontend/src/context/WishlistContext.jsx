import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import api from '../api/axios'
import { useAuth } from './AuthContext'

const WishlistContext = createContext(null)

export function WishlistProvider({ children }) {
  const { user } = useAuth()
  const [wishlist, setWishlist] = useState([]) // array of property objects
  const [loading, setLoading] = useState(false)

  const fetchWishlist = useCallback(async () => {
    if (!user) { setWishlist([]); return }
    try {
      setLoading(true)
      const res = await api.get('/favorites/')
      setWishlist(res.data.favorites || [])
    } catch { setWishlist([]) }
    finally { setLoading(false) }
  }, [user])

  useEffect(() => { fetchWishlist() }, [fetchWishlist])

  const isFavorited = (id) => wishlist.some(p => p.id === id)

  const toggleFavorite = async (property) => {
    if (!user) return false
    const already = isFavorited(property.id)
    try {
      if (already) {
        await api.delete(`/favorites/${property.id}`)
        setWishlist(prev => prev.filter(p => p.id !== property.id))
      } else {
        await api.post('/favorites/', { property_id: property.id })
        setWishlist(prev => [...prev, { ...property, is_favorited: true }])
      }
      return true
    } catch { return false }
  }

  return (
    <WishlistContext.Provider value={{ wishlist, loading, isFavorited, toggleFavorite, fetchWishlist }}>
      {children}
    </WishlistContext.Provider>
  )
}

export const useWishlist = () => useContext(WishlistContext)
