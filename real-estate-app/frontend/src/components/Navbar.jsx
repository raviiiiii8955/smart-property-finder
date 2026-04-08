import { useState, useEffect } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { Search, Heart, User, Menu, X, Building2, ChevronDown, LogOut, LayoutDashboard, Home as HomeIcon } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { useWishlist } from '../context/WishlistContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const { wishlist } = useWishlist()
  const navigate = useNavigate()
  const location = useLocation()
  const [searchQ, setSearchQ] = useState('')
  const [menuOpen, setMenuOpen] = useState(false)
  const [userDropdown, setUserDropdown] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 10)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => { setMenuOpen(false); setUserDropdown(false) }, [location])

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchQ.trim()) navigate(`/properties?location=${encodeURIComponent(searchQ.trim())}`)
  }

  return (
    <header className={`sticky top-0 z-50 transition-all duration-300 ${scrolled ? 'bg-white shadow-md' : 'bg-white border-b border-gray-100'}`}>
      <div className="page-container">
        <div className="flex items-center justify-between h-16 gap-4">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 flex-shrink-0">
            <div className="w-9 h-9 price-gradient rounded-xl flex items-center justify-center shadow">
              <Building2 className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-extrabold">
              <span className="text-primary-500">Prop</span>
              <span className="text-gray-900">Finder</span>
            </span>
          </Link>

          {/* Global search bar */}
          <form onSubmit={handleSearch} className="hidden md:flex flex-1 max-w-xl">
            <div className="relative w-full">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search by city, location or project..."
                value={searchQ}
                onChange={e => setSearchQ(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-300 focus:border-primary-400 bg-gray-50"
              />
              <button type="submit" className="absolute right-2 top-1/2 -translate-y-1/2 btn-primary py-1.5 px-3 text-xs rounded-lg">
                Search
              </button>
            </div>
          </form>

          {/* Nav Links */}
          <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-gray-600">
            <Link to="/properties" className="hover:text-primary-500 transition-colors">Buy</Link>
            <Link to="/properties?type=Apartment" className="hover:text-primary-500 transition-colors">Rent</Link>
            <Link to="/properties?type=Plot" className="hover:text-primary-500 transition-colors">Plots</Link>
          </nav>

          {/* Right Actions */}
          <div className="flex items-center gap-3">
            {user ? (
              <>
                <Link to="/wishlist" className="relative p-2 text-gray-600 hover:text-primary-500 transition-colors">
                  <Heart className="w-5 h-5" />
                  {wishlist.length > 0 && (
                    <span className="absolute -top-0.5 -right-0.5 w-4 h-4 bg-primary-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
                      {wishlist.length > 9 ? '9+' : wishlist.length}
                    </span>
                  )}
                </Link>
                <div className="relative">
                  <button
                    onClick={() => setUserDropdown(!userDropdown)}
                    className="flex items-center gap-2 bg-gray-100 hover:bg-gray-200 rounded-full pl-1 pr-3 py-1 text-sm font-medium transition-colors"
                  >
                    <div className="w-7 h-7 price-gradient rounded-full flex items-center justify-center text-white text-xs font-bold">
                      {user.name?.charAt(0).toUpperCase()}
                    </div>
                    <span className="hidden sm:block max-w-[80px] truncate">{user.name}</span>
                    <ChevronDown className="w-3.5 h-3.5 text-gray-500" />
                  </button>
                  {userDropdown && (
                    <div className="absolute right-0 top-10 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-1 animate-fade-in z-50">
                      <div className="px-4 py-2 border-b border-gray-50">
                        <p className="text-sm font-semibold text-gray-800 truncate">{user.name}</p>
                        <p className="text-xs text-gray-400 truncate">{user.email}</p>
                      </div>
                      <Link to="/wishlist" className="flex items-center gap-2 px-4 py-2.5 text-sm text-gray-600 hover:bg-gray-50 hover:text-primary-500 transition-colors">
                        <Heart className="w-4 h-4" /> Wishlist
                      </Link>
                      {user.role === 'admin' && (
                        <Link to="/admin" className="flex items-center gap-2 px-4 py-2.5 text-sm text-gray-600 hover:bg-gray-50 hover:text-primary-500 transition-colors">
                          <LayoutDashboard className="w-4 h-4" /> Admin Dashboard
                        </Link>
                      )}
                      <button onClick={() => { logout(); navigate('/') }} className="w-full flex items-center gap-2 px-4 py-2.5 text-sm text-red-500 hover:bg-red-50 transition-colors">
                        <LogOut className="w-4 h-4" /> Sign Out
                      </button>
                    </div>
                  )}
                </div>
              </>
            ) : (
              <div className="flex items-center gap-2">
                <Link to="/login" className="text-sm font-medium text-gray-600 hover:text-primary-500 px-3 py-2 transition-colors">Login</Link>
                <Link to="/signup" className="btn-primary text-sm py-2 px-4">Sign Up</Link>
              </div>
            )}
            {/* Mobile menu toggle */}
            <button className="md:hidden p-2 text-gray-600" onClick={() => setMenuOpen(!menuOpen)}>
              {menuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {menuOpen && (
          <div className="md:hidden border-t border-gray-100 py-4 space-y-3 animate-slide-up">
            <form onSubmit={handleSearch} className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search location..."
                value={searchQ}
                onChange={e => setSearchQ(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-300"
              />
            </form>
            <div className="flex flex-col space-y-1">
              <Link to="/" className="flex items-center gap-2 px-3 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-lg"><HomeIcon className="w-4 h-4" /> Home</Link>
              <Link to="/properties" className="px-3 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-lg">Buy Property</Link>
              {user && <Link to="/wishlist" className="px-3 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-lg">Wishlist ({wishlist.length})</Link>}
              {user?.role === 'admin' && <Link to="/admin" className="px-3 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-lg">Admin</Link>}
              {!user && <Link to="/login" className="btn-primary justify-center">Login / Sign Up</Link>}
              {user && <button onClick={() => { logout(); navigate('/') }} className="text-left px-3 py-2.5 text-sm font-medium text-red-500 hover:bg-red-50 rounded-lg">Sign Out</button>}
            </div>
          </div>
        )}
      </div>
    </header>
  )
}
