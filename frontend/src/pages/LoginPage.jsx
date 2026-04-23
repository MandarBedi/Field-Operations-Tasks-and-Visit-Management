import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import useAuthStore from '../store/authStore'
import { authAPI } from '../api'

export default function LoginPage() {
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { setAuth } = useAuthStore()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const { data } = await authAPI.login(form)
      setAuth(data.user, data.access, data.refresh)
      navigate('/dashboard')
    } catch {
      setError('Invalid username or password.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={s.wrapper}>
      <form onSubmit={handleSubmit} style={s.card}>
        <h2 style={{ marginBottom: 24, textAlign: 'center' }}>FieldOps</h2>
        {error && <p style={s.error}>{error}</p>}
        <input style={s.input} placeholder="Username" value={form.username}
          onChange={(e) => setForm({ ...form, username: e.target.value })} required />
        <input style={s.input} type="password" placeholder="Password" value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })} required />
        <button style={s.btn} disabled={loading}>{loading ? 'Logging in...' : 'Login'}</button>
      </form>
    </div>
  )
}

const s = {
  wrapper: { display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', background: '#f5f6fa' },
  card: { background: '#fff', padding: 40, borderRadius: 8, width: 340, boxShadow: '0 2px 12px rgba(0,0,0,.1)' },
  input: { display: 'block', width: '100%', padding: '10px 12px', marginBottom: 14, border: '1px solid #ddd', borderRadius: 4, fontSize: 14, boxSizing: 'border-box' },
  btn: { width: '100%', padding: 11, background: '#4f8ef7', color: '#fff', border: 'none', borderRadius: 4, fontSize: 15, cursor: 'pointer' },
  error: { color: '#e74c3c', marginBottom: 12, fontSize: 13 },
}
