import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Eye, EyeOff, Building2, ArrowRight, CheckCircle } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

const PERKS = ['Access exclusive property listings', 'Save properties to wishlist', 'Connect with verified owners']

export default function Signup() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [showPw, setShowPw] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    if (form.password.length < 6) { setError('Password must be at least 6 characters'); return }
    setLoading(true)
    try {
      await register(form.name, form.email, form.password)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed. Please try again.')
    } finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center p-4">
      <div className="w-full max-w-4xl grid md:grid-cols-2 gap-0 bg-white rounded-3xl shadow-card-hover overflow-hidden animate-slide-up">
        {/* Left panel */}
        <div className="price-gradient p-10 text-white flex flex-col justify-between hidden md:flex">
          <div>
            <div className="flex items-center gap-2 mb-12">
              <Building2 className="w-7 h-7" />
              <span className="text-2xl font-extrabold">PropFinder</span>
            </div>
            <h2 className="text-3xl font-bold mb-4">Find your perfect home today</h2>
            <p className="text-white/80 text-sm leading-relaxed">Join over 50,000 happy homebuyers who found their dream property with PropFinder.</p>
          </div>
          <div className="space-y-4">
            {PERKS.map(p => (
              <div key={p} className="flex items-center gap-3">
                <CheckCircle className="w-5 h-5 text-white/80 flex-shrink-0" />
                <span className="text-sm text-white/90">{p}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Right panel */}
        <div className="p-8 md:p-10">
          <div className="md:hidden text-center mb-6">
            <div className="w-14 h-14 price-gradient rounded-2xl flex items-center justify-center mx-auto mb-3 shadow"><Building2 className="w-7 h-7 text-white" /></div>
          </div>
          <h1 className="text-2xl font-extrabold text-gray-900 mb-1">Create account</h1>
          <p className="text-gray-500 text-sm mb-6">It's free and takes less than a minute</p>

          {error && (
            <div className="bg-red-50 border border-red-100 text-red-600 text-sm px-4 py-3 rounded-xl mb-4">{error}</div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label">Full Name</label>
              <input type="text" placeholder="John Doe" value={form.name} onChange={e => setForm({...form, name: e.target.value})} className="input-field" required />
            </div>
            <div>
              <label className="label">Email Address</label>
              <input type="email" placeholder="you@example.com" value={form.email} onChange={e => setForm({...form, email: e.target.value})} className="input-field" required />
            </div>
            <div>
              <label className="label">Password</label>
              <div className="relative">
                <input type={showPw ? 'text' : 'password'} placeholder="Min 6 characters" value={form.password} onChange={e => setForm({...form, password: e.target.value})} className="input-field pr-10" required />
                <button type="button" onClick={() => setShowPw(!showPw)} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                  {showPw ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <button type="submit" disabled={loading} className="btn-primary w-full justify-center py-3 text-base mt-2">
              {loading ? (
                <span className="flex items-center gap-2"><span className="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin" /> Creating account...</span>
              ) : (
                <span className="flex items-center gap-2">Create Account <ArrowRight className="w-4 h-4" /></span>
              )}
            </button>
          </form>

          <p className="text-center text-sm text-gray-500 mt-6">
            Already have an account?{' '}
            <Link to="/login" className="text-primary-500 font-semibold hover:text-primary-700 transition-colors">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
