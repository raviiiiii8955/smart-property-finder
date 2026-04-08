import { useState, useEffect } from 'react'
import { Plus, Pencil, Trash2, X, Building2, LayoutDashboard, TrendingUp, Home, Search, ChevronUp, ChevronDown } from 'lucide-react'
import api from '../api/axios'
import { formatPrice } from '../components/PropertyCard'

const EMPTY_FORM = {
  title: '', price: '', location: '', city: '', bhk: '', type: 'Apartment',
  furnishing: 'Unfurnished', area_sqft: '', description: '',
  amenities: '', images: '', owner_contact: '', lat: '', lng: ''
}

function Modal({ open, onClose, children }) {
  if (!open) return null
  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center p-4 bg-black/50 overflow-y-auto">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl my-8 animate-slide-up">
        {children}
      </div>
    </div>
  )
}

function StatCard({ label, value, icon: Icon, color }) {
  return (
    <div className="bg-white rounded-2xl p-5 shadow-card flex items-center gap-4">
      <div className={`w-12 h-12 ${color} rounded-xl flex items-center justify-center flex-shrink-0`}>
        <Icon className="w-6 h-6 text-white" />
      </div>
      <div>
        <p className="text-xs text-gray-500 font-medium">{label}</p>
        <p className="text-2xl font-extrabold text-gray-900">{value}</p>
      </div>
    </div>
  )
}

export default function Admin() {
  const [properties, setProperties] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [modalOpen, setModalOpen] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [deleteConfirm, setDeleteConfirm] = useState(null)
  const [sortCol, setSortCol] = useState('id')
  const [sortDir, setSortDir] = useState('desc')

  const fetchAll = async () => {
    setLoading(true)
    try {
      const res = await api.get('/properties/?per_page=200')
      setProperties(res.data.properties || [])
    } catch { setProperties([]) }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchAll() }, [])

  const openAdd = () => { setForm(EMPTY_FORM); setEditingId(null); setError(''); setModalOpen(true) }
  const openEdit = (p) => {
    setForm({
      title: p.title, price: p.price, location: p.location, city: p.city,
      bhk: p.bhk, type: p.type, furnishing: p.furnishing, area_sqft: p.area_sqft,
      description: p.description || '', amenities: (p.amenities || []).join(', '),
      images: (p.images || []).join('\n'), owner_contact: p.owner_contact || '',
      lat: p.lat || '', lng: p.lng || ''
    })
    setEditingId(p.id); setError(''); setModalOpen(true)
  }
  const closeModal = () => { setModalOpen(false); setEditingId(null); setForm(EMPTY_FORM) }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true); setError('')
    try {
      const payload = {
        ...form,
        price: parseInt(form.price),
        bhk: parseInt(form.bhk) || 0,
        area_sqft: parseInt(form.area_sqft) || 0,
        lat: parseFloat(form.lat) || 0,
        lng: parseFloat(form.lng) || 0,
        amenities: form.amenities.split(',').map(a => a.trim()).filter(Boolean),
        images: form.images.split('\n').map(i => i.trim()).filter(Boolean),
      }
      if (editingId) await api.put(`/properties/${editingId}`, payload)
      else await api.post('/properties/', payload)
      closeModal()
      fetchAll()
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to save property')
    } finally { setSubmitting(false) }
  }

  const handleDelete = async (id) => {
    try {
      await api.delete(`/properties/${id}`)
      setProperties(prev => prev.filter(p => p.id !== id))
      setDeleteConfirm(null)
    } catch { alert('Failed to delete property') }
  }

  const handleSort = (col) => {
    if (sortCol === col) setSortDir(d => d === 'asc' ? 'desc' : 'asc')
    else { setSortCol(col); setSortDir('asc') }
  }

  const filtered = properties
    .filter(p =>
      p.title.toLowerCase().includes(search.toLowerCase()) ||
      p.location.toLowerCase().includes(search.toLowerCase()) ||
      p.city.toLowerCase().includes(search.toLowerCase())
    )
    .sort((a, b) => {
      let av = a[sortCol], bv = b[sortCol]
      if (typeof av === 'string') av = av.toLowerCase()
      if (typeof bv === 'string') bv = bv.toLowerCase()
      return sortDir === 'asc' ? (av > bv ? 1 : -1) : (av < bv ? 1 : -1)
    })

  const SortIcon = ({ col }) => {
    if (sortCol !== col) return <ChevronUp className="w-3 h-3 text-gray-300" />
    return sortDir === 'asc' ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />
  }
  const Th = ({ col, children }) => (
    <th onClick={() => handleSort(col)} className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide cursor-pointer hover:text-gray-700 select-none">
      <span className="flex items-center gap-1">{children}<SortIcon col={col} /></span>
    </th>
  )

  const TYPES = ['Apartment', 'Villa', 'Plot', 'Commercial']
  const FURNISHING = ['Furnished', 'Semi-Furnished', 'Unfurnished']

  const stats = [
    { label: 'Total Properties', value: properties.length, icon: Building2, color: 'bg-blue-500' },
    { label: 'Apartments', value: properties.filter(p => p.type === 'Apartment').length, icon: Home, color: 'bg-primary-500' },
    { label: 'Villas', value: properties.filter(p => p.type === 'Villa').length, icon: Building2, color: 'bg-purple-500' },
    { label: 'Avg Price', value: properties.length ? formatPrice(Math.round(properties.reduce((s, p) => s + p.price, 0) / properties.length)) : '₹0', icon: TrendingUp, color: 'bg-green-500' },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-100 py-4">
        <div className="page-container flex items-center justify-between">
          <div className="flex items-center gap-2">
            <LayoutDashboard className="w-5 h-5 text-primary-500" />
            <h1 className="text-xl font-extrabold text-gray-900">Admin Dashboard</h1>
          </div>
          <button onClick={openAdd} className="btn-primary text-sm">
            <Plus className="w-4 h-4" /> Add Property
          </button>
        </div>
      </div>

      <div className="page-container py-6 space-y-6">
        {/* Stats */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map(s => <StatCard key={s.label} {...s} />)}
        </div>

        {/* Table */}
        <div className="bg-white rounded-2xl shadow-card overflow-hidden">
          <div className="p-4 border-b border-gray-100 flex items-center justify-between gap-4 flex-wrap">
            <h2 className="font-bold text-gray-900">All Properties</h2>
            <div className="relative flex-shrink-0">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search properties..."
                value={search}
                onChange={e => setSearch(e.target.value)}
                className="pl-9 pr-4 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-300 w-64"
              />
            </div>
          </div>

          {loading ? (
            <div className="p-8 text-center text-gray-400">Loading properties...</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 border-b border-gray-100">
                  <tr>
                    <Th col="id">ID</Th>
                    <Th col="title">Title</Th>
                    <Th col="city">City</Th>
                    <Th col="type">Type</Th>
                    <Th col="bhk">BHK</Th>
                    <Th col="price">Price</Th>
                    <th className="px-4 py-3 text-right text-xs font-semibold text-gray-500 uppercase">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                  {filtered.map(p => (
                    <tr key={p.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-3 text-gray-400 font-mono text-xs">{p.id}</td>
                      <td className="px-4 py-3">
                        <div className="font-medium text-gray-800 max-w-xs truncate">{p.title}</div>
                        <div className="text-xs text-gray-400 truncate max-w-xs">{p.location}</div>
                      </td>
                      <td className="px-4 py-3 text-gray-600">{p.city}</td>
                      <td className="px-4 py-3">
                        <span className={`tag text-xs ${
                          p.type === 'Apartment' ? 'bg-blue-50 text-blue-700' :
                          p.type === 'Villa' ? 'bg-purple-50 text-purple-700' :
                          p.type === 'Plot' ? 'bg-green-50 text-green-700' : 'bg-orange-50 text-orange-700'
                        }`}>{p.type}</span>
                      </td>
                      <td className="px-4 py-3 text-gray-600">{p.bhk > 0 ? `${p.bhk} BHK` : '—'}</td>
                      <td className="px-4 py-3 font-semibold text-primary-600">{formatPrice(p.price)}</td>
                      <td className="px-4 py-3">
                        <div className="flex items-center justify-end gap-2">
                          <button onClick={() => openEdit(p)} className="p-1.5 rounded-lg text-gray-400 hover:text-blue-500 hover:bg-blue-50 transition-colors">
                            <Pencil className="w-4 h-4" />
                          </button>
                          <button onClick={() => setDeleteConfirm(p)} className="p-1.5 rounded-lg text-gray-400 hover:text-red-500 hover:bg-red-50 transition-colors">
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {filtered.length === 0 && (
                <div className="py-12 text-center text-gray-400">No properties match your search</div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Add / Edit Modal */}
      <Modal open={modalOpen} onClose={closeModal}>
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <h2 className="font-bold text-lg text-gray-900">{editingId ? 'Edit Property' : 'Add New Property'}</h2>
          <button onClick={closeModal} className="text-gray-400 hover:text-gray-600"><X className="w-5 h-5" /></button>
        </div>
        <form onSubmit={handleSubmit} className="p-6 space-y-4 max-h-[70vh] overflow-y-auto">
          {error && <div className="bg-red-50 text-red-600 text-sm p-3 rounded-xl">{error}</div>}

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="sm:col-span-2">
              <label className="label">Property Title *</label>
              <input type="text" className="input-field" value={form.title} onChange={e => setForm({...form, title: e.target.value})} required placeholder="e.g. Spacious 3 BHK Apartment" />
            </div>
            <div>
              <label className="label">Price (₹) *</label>
              <input type="number" className="input-field" value={form.price} onChange={e => setForm({...form, price: e.target.value})} required placeholder="e.g. 5000000" />
            </div>
            <div>
              <label className="label">Area (sqft)</label>
              <input type="number" className="input-field" value={form.area_sqft} onChange={e => setForm({...form, area_sqft: e.target.value})} placeholder="e.g. 1200" />
            </div>
            <div>
              <label className="label">Location *</label>
              <input type="text" className="input-field" value={form.location} onChange={e => setForm({...form, location: e.target.value})} required placeholder="e.g. Koramangala, Bangalore" />
            </div>
            <div>
              <label className="label">City *</label>
              <input type="text" className="input-field" value={form.city} onChange={e => setForm({...form, city: e.target.value})} required placeholder="e.g. Bangalore" />
            </div>
            <div>
              <label className="label">Property Type *</label>
              <select className="input-field" value={form.type} onChange={e => setForm({...form, type: e.target.value})}>
                {TYPES.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
            </div>
            <div>
              <label className="label">BHK</label>
              <input type="number" className="input-field" value={form.bhk} onChange={e => setForm({...form, bhk: e.target.value})} placeholder="e.g. 2 (0 for plot/commercial)" min="0" max="10" />
            </div>
            <div>
              <label className="label">Furnishing</label>
              <select className="input-field" value={form.furnishing} onChange={e => setForm({...form, furnishing: e.target.value})}>
                {FURNISHING.map(f => <option key={f} value={f}>{f}</option>)}
              </select>
            </div>
            <div>
              <label className="label">Owner Contact</label>
              <input type="text" className="input-field" value={form.owner_contact} onChange={e => setForm({...form, owner_contact: e.target.value})} placeholder="+91 99999 00000" />
            </div>
            <div>
              <label className="label">Latitude</label>
              <input type="number" step="any" className="input-field" value={form.lat} onChange={e => setForm({...form, lat: e.target.value})} placeholder="e.g. 12.9352" />
            </div>
            <div>
              <label className="label">Longitude</label>
              <input type="number" step="any" className="input-field" value={form.lng} onChange={e => setForm({...form, lng: e.target.value})} placeholder="e.g. 77.6245" />
            </div>
            <div className="sm:col-span-2">
              <label className="label">Description</label>
              <textarea className="input-field" rows={3} value={form.description} onChange={e => setForm({...form, description: e.target.value})} placeholder="Describe the property..." />
            </div>
            <div className="sm:col-span-2">
              <label className="label">Amenities (comma-separated)</label>
              <input type="text" className="input-field" value={form.amenities} onChange={e => setForm({...form, amenities: e.target.value})} placeholder="Swimming Pool, Gym, Security, Parking" />
            </div>
            <div className="sm:col-span-2">
              <label className="label">Image URLs (one per line)</label>
              <textarea className="input-field font-mono text-xs" rows={3} value={form.images} onChange={e => setForm({...form, images: e.target.value})} placeholder="https://images.unsplash.com/photo-abc?w=800" />
            </div>
          </div>
        </form>
        <div className="flex gap-3 px-6 py-4 border-t border-gray-100">
          <button type="button" onClick={closeModal} className="btn-secondary flex-1 justify-center">Cancel</button>
          <button onClick={handleSubmit} disabled={submitting} className="btn-primary flex-1 justify-center">
            {submitting ? <span className="flex items-center gap-2"><span className="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin" />Saving...</span> : editingId ? 'Update Property' : 'Add Property'}
          </button>
        </div>
      </Modal>

      {/* Delete Confirm */}
      {deleteConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-white rounded-2xl shadow-2xl p-6 max-w-sm w-full animate-slide-up">
            <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Trash2 className="w-6 h-6 text-red-500" />
            </div>
            <h3 className="font-bold text-lg text-center text-gray-900 mb-2">Delete Property?</h3>
            <p className="text-sm text-gray-500 text-center mb-6">This will permanently delete <strong>"{deleteConfirm.title}"</strong>. This action cannot be undone.</p>
            <div className="flex gap-3">
              <button onClick={() => setDeleteConfirm(null)} className="btn-secondary flex-1 justify-center">Cancel</button>
              <button onClick={() => handleDelete(deleteConfirm.id)} className="flex-1 bg-red-500 hover:bg-red-600 text-white font-semibold px-4 py-2.5 rounded-lg transition-colors text-sm">Delete</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
