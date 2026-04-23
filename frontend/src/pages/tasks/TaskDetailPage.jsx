import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { tasksAPI, usersAPI } from '../../api'
import useAuthStore from '../../store/authStore'
import RoleGuard from '../../components/RoleGuard'

function Info({ label, value }) {
  return <div><div style={{ fontSize: 11, color: '#999', textTransform: 'uppercase' }}>{label}</div><div style={{ fontSize: 15, fontWeight: 500 }}>{value ?? '—'}</div></div>
}

export default function TaskDetailPage() {
  const { id } = useParams()
  const { user } = useAuthStore()
  const qc = useQueryClient()
  const navigate = useNavigate()
  const [assignId, setAssignId] = useState('')
  const [newStatus, setNewStatus] = useState('')
  const [msg, setMsg] = useState('')

  const { data: task, isLoading } = useQuery({ queryKey: ['task', id], queryFn: () => tasksAPI.detail(id).then(r => r.data) })
  const { data: agents } = useQuery({ queryKey: ['agents'], queryFn: () => usersAPI.byRole('field_agent').then(r => r.data) })
  const { data: ai } = useQuery({ queryKey: ['task-ai', id], queryFn: () => tasksAPI.aiSuggestion(id).then(r => r.data) })

  const inv = () => qc.invalidateQueries({ queryKey: ['task', id] })

  const assignMut = useMutation({
    mutationFn: () => tasksAPI.assign(id, { assigned_to: parseInt(assignId) }),
    onSuccess: () => { setMsg('Assigned.'); inv() },
    onError: (e) => setMsg(e.response?.data?.detail || 'Failed.'),
  })
  const statusMut = useMutation({
    mutationFn: () => tasksAPI.updateStatus(id, { status: newStatus }),
    onSuccess: () => { setMsg('Status updated.'); inv() },
    onError: (e) => setMsg(JSON.stringify(e.response?.data)),
  })
  const delMut = useMutation({ mutationFn: () => tasksAPI.delete(id), onSuccess: () => navigate('/tasks') })

  if (isLoading) return <p>Loading...</p>
  if (!task) return <p>Not found.</p>

  return (
    <div style={{ maxWidth: 720 }}>
      <button onClick={() => navigate('/tasks')} style={s.back}>← Back</button>
      <h2>{task.title}</h2>
      {msg && <p style={s.msg}>{msg}</p>}

      <div style={s.grid}>
        <Info label="Status" value={task.status?.replace('_', ' ')} />
        <Info label="Priority" value={task.priority} />
        <Info label="Region" value={task.region?.name} />
        <Info label="Team" value={task.team?.name} />
        <Info label="Assigned To" value={task.assigned_to?.username ?? 'Unassigned'} />
        <Info label="Due Date" value={task.due_date} />
        <Info label="Created By" value={task.created_by?.username} />
        <Info label="Visits" value={task.visit_count} />
      </div>

      {task.description && <div style={{ background: '#fff', padding: 16, borderRadius: 8, marginBottom: 16 }}><strong>Description</strong><p style={{ marginTop: 6, color: '#555' }}>{task.description}</p></div>}

      {ai && (
        <div style={{ background: '#fffbea', border: '1px solid #f39c12', borderRadius: 6, padding: 16, marginBottom: 16 }}>
          <strong>AI Suggestion</strong>
          <p style={{ marginTop: 6, fontSize: 14 }}>{ai.suggestion}</p>
          <small style={{ color: '#888' }}>Rule: {ai.rule} | Confidence: {ai.confidence}%</small>
        </div>
      )}

      <RoleGuard roles={['admin', 'regional_manager', 'team_lead']}>
        <div style={{ marginBottom: 16 }}>
          <strong>Assign Task</strong>
          <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
            <select value={assignId} onChange={e => setAssignId(e.target.value)} style={s.select}>
              <option value="">Select agent...</option>
              {agents?.map(a => <option key={a.id} value={a.id}>{a.username}</option>)}
            </select>
            <button onClick={() => assignMut.mutate()} disabled={!assignId} style={s.btn}>Assign</button>
          </div>
        </div>
      </RoleGuard>

      <div style={{ marginBottom: 16 }}>
        <strong>Update Status</strong>
        <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
          <select value={newStatus} onChange={e => setNewStatus(e.target.value)} style={s.select}>
            <option value="">Select status...</option>
            {['pending', 'assigned', 'in_progress', 'completed', 'cancelled'].map(v => <option key={v} value={v}>{v.replace('_', ' ')}</option>)}
          </select>
          <button onClick={() => statusMut.mutate()} disabled={!newStatus} style={s.btn}>Update</button>
        </div>
      </div>

      <RoleGuard roles={['admin']}>
        <button onClick={() => { if (window.confirm('Delete?')) delMut.mutate() }} style={{ ...s.btn, background: '#e74c3c' }}>Delete Task</button>
      </RoleGuard>
    </div>
  )
}

const s = {
  back: { background: 'none', border: 'none', color: '#4f8ef7', cursor: 'pointer', marginBottom: 12, fontSize: 14 },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, background: '#fff', padding: 20, borderRadius: 8, marginBottom: 16 },
  select: { padding: '7px 10px', border: '1px solid #ddd', borderRadius: 4 },
  btn: { padding: '8px 16px', background: '#4f8ef7', color: '#fff', border: 'none', borderRadius: 4, cursor: 'pointer' },
  msg: { background: '#eaf6ff', border: '1px solid #4f8ef7', padding: '8px 12px', borderRadius: 4, fontSize: 13, marginBottom: 12 },
}
