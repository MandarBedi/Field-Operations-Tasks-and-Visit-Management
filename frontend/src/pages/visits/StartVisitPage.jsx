import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation, useQuery } from '@tanstack/react-query'
import { visitsAPI, tasksAPI } from '../../api'

function Field({ label, children }) {
  return <div style={{ marginBottom: 14 }}><label style={{ fontSize: 13, color: '#555', display: 'block', marginBottom: 3 }}>{label}</label>{children}</div>
}

export default function StartVisitPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ task: '', location_name: '', latitude: '', longitude: '' })
  const [error, setError] = useState('')
  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const { data: tasks } = useQuery({ queryKey: ['my-tasks'], queryFn: () => tasksAPI.list({ status: 'assigned' }).then(r => r.data) })

  const mut = useMutation({
    mutationFn: () => visitsAPI.start(Object.fromEntries(Object.entries(form).filter(([, v]) => v !== ''))),
    onSuccess: (res) => navigate(`/visits/${res.data.id}`),
    onError: (e) => setError(e.response?.data?.non_field_errors?.[0] || JSON.stringify(e.response?.data)),
  })

  return (
    <div style={{ maxWidth: 480 }}>
      <button onClick={() => navigate('/visits')} style={s.back}>← Back</button>
      <h2>Start Visit</h2>
      {error && <p style={{ color: '#e74c3c', fontSize: 13 }}>{error}</p>}
      <div style={{ background: '#fff', padding: 24, borderRadius: 8 }}>
        <Field label="Link to Task (optional)">
          <select style={s.input} value={form.task} onChange={e => set('task', e.target.value)}>
            <option value="">— No task —</option>
            {tasks?.results?.map(t => <option key={t.id} value={t.id}>{t.title}</option>)}
          </select>
        </Field>
        <Field label="Location Name *"><input style={s.input} value={form.location_name} onChange={e => set('location_name', e.target.value)} required /></Field>
        <Field label="Latitude"><input style={s.input} type="number" step="any" value={form.latitude} onChange={e => set('latitude', e.target.value)} /></Field>
        <Field label="Longitude"><input style={s.input} type="number" step="any" value={form.longitude} onChange={e => set('longitude', e.target.value)} /></Field>
        <button onClick={() => mut.mutate()} disabled={!form.location_name || mut.isPending} style={s.btn}>
          {mut.isPending ? 'Starting...' : 'Start Visit'}
        </button>
      </div>
    </div>
  )
}

const s = {
  back: { background: 'none', border: 'none', color: '#4f8ef7', cursor: 'pointer', marginBottom: 12, fontSize: 14 },
  input: { width: '100%', padding: '8px 10px', border: '1px solid #ddd', borderRadius: 4, fontSize: 14, boxSizing: 'border-box' },
  btn: { width: '100%', padding: 11, background: '#27ae60', color: '#fff', border: 'none', borderRadius: 4, cursor: 'pointer', marginTop: 8 },
}
