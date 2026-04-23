import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { visitsAPI } from '../../api'
import useAuthStore from '../../store/authStore'

function Info({ label, value }) {
  return <div><div style={{ fontSize: 11, color: '#999', textTransform: 'uppercase' }}>{label}</div><div style={{ fontSize: 15, fontWeight: 500 }}>{value ?? '—'}</div></div>
}

export default function VisitDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuthStore()
  const qc = useQueryClient()
  const [cf, setCf] = useState({ notes: '', outcome: '' })
  const [cancelNotes, setCancelNotes] = useState('')
  const [msg, setMsg] = useState('')

  const { data: visit, isLoading } = useQuery({ queryKey: ['visit', id], queryFn: () => visitsAPI.detail(id).then(r => r.data) })
  const inv = () => qc.invalidateQueries({ queryKey: ['visit', id] })

  const completeMut = useMutation({
    mutationFn: () => visitsAPI.complete(id, cf),
    onSuccess: () => { setMsg('Completed.'); inv() },
    onError: (e) => setMsg(e.response?.data?.detail || JSON.stringify(e.response?.data)),
  })
  const cancelMut = useMutation({
    mutationFn: () => visitsAPI.cancel(id, { notes: cancelNotes }),
    onSuccess: () => { setMsg('Cancelled.'); inv() },
    onError: (e) => setMsg(e.response?.data?.detail || 'Failed.'),
  })

  if (isLoading) return <p>Loading...</p>
  if (!visit) return <p>Not found.</p>

  const canAct = visit.field_agent?.id === user?.id || ['admin', 'regional_manager', 'team_lead'].includes(user?.role)

  return (
    <div style={{ maxWidth: 680 }}>
      <button onClick={() => navigate('/visits')} style={s.back}>← Back</button>
      <h2>Visit #{visit.id}</h2>
      {msg && <p style={s.msg}>{msg}</p>}
      <div style={s.grid}>
        <Info label="Agent" value={visit.field_agent?.username} />
        <Info label="Status" value={visit.status} />
        <Info label="Location" value={visit.location_name} />
        <Info label="Task" value={visit.task?.title} />
        <Info label="Outcome" value={visit.outcome} />
        <Info label="Duration" value={visit.duration_minutes ? `${visit.duration_minutes} min` : null} />
        <Info label="Started" value={visit.started_at ? new Date(visit.started_at).toLocaleString() : null} />
        <Info label="Completed" value={visit.completed_at ? new Date(visit.completed_at).toLocaleString() : null} />
      </div>
      {visit.notes && <div style={{ background: '#fff', padding: 16, borderRadius: 8, marginBottom: 16 }}><strong>Notes</strong><p style={{ marginTop: 6, color: '#555' }}>{visit.notes}</p></div>}

      {visit.status === 'started' && canAct && (
        <>
          <div style={{ marginBottom: 16 }}>
            <strong>Complete Visit</strong>
            <textarea style={s.input} placeholder="Notes..." value={cf.notes} onChange={e => setCf(f => ({ ...f, notes: e.target.value }))} />
            <select style={s.input} value={cf.outcome} onChange={e => setCf(f => ({ ...f, outcome: e.target.value }))}>
              <option value="">Select outcome *</option>
              {['successful', 'partial', 'failed', 'no_contact'].map(o => <option key={o} value={o}>{o.replace('_', ' ')}</option>)}
            </select>
            <button onClick={() => completeMut.mutate()} disabled={!cf.outcome} style={{ ...s.btn, background: '#27ae60' }}>Complete</button>
          </div>
          <div>
            <strong>Cancel Visit</strong>
            <textarea style={s.input} placeholder="Reason..." value={cancelNotes} onChange={e => setCancelNotes(e.target.value)} />
            <button onClick={() => { if (window.confirm('Cancel?')) cancelMut.mutate() }} style={{ ...s.btn, background: '#e74c3c' }}>Cancel Visit</button>
          </div>
        </>
      )}
    </div>
  )
}

const s = {
  back: { background: 'none', border: 'none', color: '#4f8ef7', cursor: 'pointer', marginBottom: 12, fontSize: 14 },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, background: '#fff', padding: 20, borderRadius: 8, marginBottom: 16 },
  input: { display: 'block', width: '100%', padding: '8px 10px', border: '1px solid #ddd', borderRadius: 4, fontSize: 14, boxSizing: 'border-box', marginTop: 8 },
  btn: { padding: '9px 18px', color: '#fff', border: 'none', borderRadius: 4, cursor: 'pointer', marginTop: 8 },
  msg: { background: '#eaf6ff', border: '1px solid #4f8ef7', padding: '8px 12px', borderRadius: 4, fontSize: 13, marginBottom: 12 },
}
