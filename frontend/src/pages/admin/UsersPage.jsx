import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { usersAPI } from '../../api'

function Field({ label, children }) {
  return <div style={{ marginBottom: 10 }}><label style={{ fontSize: 12, color: '#666', display: 'block', marginBottom: 3 }}>{label}</label>{children}</div>
}

export default function UsersPage() {
  const qc = useQueryClient()
  const [form, setForm] = useState({ username: '', email: '', password: '', role: 'field_agent', region: '', team: '' })
  const [msg, setMsg] = useState('')
  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const { data: users, isLoading } = useQuery({ queryKey: ['users'], queryFn: () => usersAPI.list().then(r => r.data) })
  const { data: regions } = useQuery({ queryKey: ['regions'], queryFn: () => usersAPI.regions().then(r => r.data.results) })
  const { data: teams } = useQuery({ queryKey: ['teams', form.region], queryFn: () => usersAPI.teams(form.region).then(r => r.data.results) })

  const createMut = useMutation({
    mutationFn: () => usersAPI.create(Object.fromEntries(Object.entries(form).filter(([, v]) => v))),
    onSuccess: () => { setMsg('User created.'); qc.invalidateQueries({ queryKey: ['users'] }); setForm({ username: '', email: '', password: '', role: 'field_agent', region: '', team: '' }) },
    onError: (e) => setMsg(JSON.stringify(e.response?.data)),
  })
  const deactivateMut = useMutation({
    mutationFn: (id) => usersAPI.deactivate(id),
    onSuccess: () => { setMsg('Deactivated.'); qc.invalidateQueries({ queryKey: ['users'] }) },
  })

  return (
    <div>
      <h2>User Management</h2>
      {msg && <p style={{ background: '#eaf6ff', border: '1px solid #4f8ef7', padding: '8px 12px', borderRadius: 4, fontSize: 13, marginBottom: 12 }}>{msg}</p>}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
        <div style={{ background: '#fff', padding: 24, borderRadius: 8 }}>
          <h4>Create User</h4>
          <Field label="Username *"><input style={s.input} value={form.username} onChange={e => set('username', e.target.value)} /></Field>
          <Field label="Email *"><input type="email" style={s.input} value={form.email} onChange={e => set('email', e.target.value)} /></Field>
          <Field label="Password *"><input type="password" style={s.input} value={form.password} onChange={e => set('password', e.target.value)} /></Field>
          <Field label="Role">
            <select style={s.input} value={form.role} onChange={e => set('role', e.target.value)}>
              {['admin', 'regional_manager', 'team_lead', 'field_agent', 'auditor'].map(r => <option key={r} value={r}>{r.replace(/_/g, ' ')}</option>)}
            </select>
          </Field>
          <Field label="Region">
            <select style={s.input} value={form.region} onChange={e => set('region', e.target.value)}>
              <option value="">— None —</option>
              {regions?.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
            </select>
          </Field>
          <Field label="Team">
            <select style={s.input} value={form.team} onChange={e => set('team', e.target.value)}>
              <option value="">— None —</option>
              {teams?.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
            </select>
          </Field>
          <button onClick={() => createMut.mutate()} style={s.btn} disabled={createMut.isPending}>
            {createMut.isPending ? 'Creating...' : 'Create User'}
          </button>
        </div>

        <div style={{ background: '#fff', padding: 24, borderRadius: 8 }}>
          <h4>All Users</h4>
          {isLoading ? <p>Loading...</p> : (
            <table style={{ width: '100%', fontSize: 13, borderCollapse: 'collapse' }}>
              <thead><tr style={{ background: '#f5f6fa' }}><th style={{ padding: '8px 6px', textAlign: 'left' }}>Username</th><th>Role</th><th>Active</th><th></th></tr></thead>
              <tbody>
                {users?.results?.map(u => (
                  <tr key={u.id} style={{ borderBottom: '1px solid #f0f0f0' }}>
                    <td style={{ padding: '7px 6px' }}>{u.username}</td>
                    <td>{u.role?.replace(/_/g, ' ')}</td>
                    <td>{u.is_active ? '✓' : '✗'}</td>
                    <td>{u.is_active && <button onClick={() => { if (window.confirm('Deactivate?')) deactivateMut.mutate(u.id) }} style={{ background: '#e74c3c', color: '#fff', border: 'none', padding: '3px 8px', borderRadius: 3, cursor: 'pointer', fontSize: 12 }}>Deactivate</button>}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  )
}

const s = {
  input: { width: '100%', padding: '7px 10px', border: '1px solid #ddd', borderRadius: 4, fontSize: 13, boxSizing: 'border-box' },
  btn: { width: '100%', padding: 10, background: '#4f8ef7', color: '#fff', border: 'none', borderRadius: 4, cursor: 'pointer' },
}
