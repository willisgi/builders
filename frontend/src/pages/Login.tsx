import { useState } from 'react'
import { apiFetch } from '../lib/api'
import { useNavigate } from 'react-router-dom'

export default function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('admin@example.com')
  const [password, setPassword] = useState('admin123')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const data = await apiFetch('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      })
      localStorage.setItem('token', data.access_token)
      navigate('/')
    } catch (err: any) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen grid place-items-center bg-slate-50 p-6">
      <form onSubmit={onSubmit} className="w-full max-w-sm bg-white p-6 rounded-lg shadow border border-slate-200">
        <h1 className="text-xl font-semibold mb-4">Sign in</h1>
        {error && <div className="text-red-600 text-sm mb-2">{error}</div>}
        <label className="block mb-2 text-sm font-medium">Email</label>
        <input value={email} onChange={e=>setEmail(e.target.value)} className="w-full mb-4 border rounded px-3 py-2" placeholder="you@example.com" />
        <label className="block mb-2 text-sm font-medium">Password</label>
        <input type="password" value={password} onChange={e=>setPassword(e.target.value)} className="w-full mb-4 border rounded px-3 py-2" placeholder="••••••••" />
        <button disabled={loading} className="w-full rounded bg-slate-900 text-white py-2 disabled:opacity-50">{loading ? 'Signing in...' : 'Sign in'}</button>
      </form>
    </div>
  )
}
