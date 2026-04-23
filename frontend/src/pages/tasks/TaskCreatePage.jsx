import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation, useQuery } from '@tanstack/react-query'
import { tasksAPI, usersAPI } from '../../api'

function Field({ label, children }) {
  return <div style={{ marginBottom: 14 }}><label style={{ fontSize: 13, color: '#555', display: 'block', marginBottom: 3 }}>{label}</label>{children}</div>
}

export default function TaskCreatePage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ title: '', description: '', priority: 'medium', region: '', team: '', assigned_to: '', due_date: '' })
  const [error, setError] = useState('')
  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const { data: regions } = useQuery({ queryKey: ['regions'], queryFn: () => usersAPI.regions().then(r => r.data.results) })
  const { data: teams } = useQuery({ queryKey: ['teams', form.region], queryFn: () => usersAPI.teams(form.region).then(r => r.data.results) })
  const { data: agents } = useQuery({ queryKey: ['agents'], queryFn: () => usersAPI.byRole('field_agent').then(r => r.data) })

  const mut = useMutation({
    mutationFn: () => tasksAPI.create(Object.fromEntries(Object.entries(form).filter(([, v]) => v !== ''))),
    onSuccess: (res) => navigate(`/tasks/${res.data.id}`),
    onError: (e) => setError(JSON.stringify(e.response?.data)),
  })

  return (
    <div style={{ maxWidth: 560 }}>
      <button onClick={() => navigate('/tasks')} style={s.back}>← Back</button>
      <h2>Create Task</h2>
      {error && <p style={{ color: '#e74c3c', fontSize: 13 }}>{error}</p>}
      <div style={{ background: '#fff', padding: 24, borderRadius: 8 }}>
        <Field label="Title *"><input style={s.input} value={form.title} onChange={e => set('title', e.target.value)} required /></Field>
        <Field label="Description"><textarea style={{ ...s.input, height: 80 }} value={form.description} onChange={e => set('description', e.target.value)} /></Field>
        <Field label="Priority">
          <select style={s.input} value={form.priority} onChange={e => set('priority', e.target.value)}>
            {['low', 'medium', 'high', 'critical'].map(p => <option key={p} value={p}>{p}</option>)}
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
        <Field label="Assign To">
          <select style={s.input} value={form.assigned_to} onChange={e => set('assigned_to', e.target.value)}>
            <option value="">— Unassigned —</option>
            {agents?.map(a => <option key={a.id} value={a.id}>{a.username}</option>)}
          </select>
        </Field>
        <Field label="Due Date"><input type="date" style={s.input} value={form.due_date} onChange={e => set('due_date', e.target.value)} /></Field>
        <button onClick={() => mut.mutate()} disabled={!form.title || mut.isPending} style={s.btn}>
          {mut.isPending ? 'Creating...' : 'Create Task'}
        </button>
      </div>
    </div>
  )
}

const s = {
  back: { background: 'none', border: 'none', color: '#4f8ef7', cursor: 'pointer', marginBottom: 12, fontSize: 14 },
  input: { width: '100%', padding: '8px 10px', border: '1px solid #ddd', borderRadius: 4, fontSize: 14, boxSizing: 'border-box' },
  btn: { width: '100%', padding: 11, background: '#4f8ef7', color: '#fff', border: 'none', borderRadius: 4, cursor: 'pointer', marginTop: 8 },
}
