import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { tasksAPI } from '../../api'

const PC = { low: '#95a5a6', medium: '#f39c12', high: '#e67e22', critical: '#e74c3c' }
const SC = { pending: '#95a5a6', assigned: '#3498db', in_progress: '#9b59b6', completed: '#2ecc71', cancelled: '#e74c3c' }

export default function TaskListPage() {
  const [filters, setFilters] = useState({ status: '', priority: '' })
  const { data, isLoading } = useQuery({
    queryKey: ['tasks', filters],
    queryFn: () => tasksAPI.list(Object.fromEntries(Object.entries(filters).filter(([, v]) => v))).then(r => r.data),
  })
  const set = (k, v) => setFilters(f => ({ ...f, [k]: v }))

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <h2 style={{ margin: 0 }}>Tasks</h2>
        <Link to="/tasks/create" style={s.btn}>+ New Task</Link>
      </div>
      <div style={{ display: 'flex', gap: 10, marginBottom: 16 }}>
        <select value={filters.status} onChange={e => set('status', e.target.value)} style={s.select}>
          <option value="">All Statuses</option>
          {['pending', 'assigned', 'in_progress', 'completed', 'cancelled'].map(v => <option key={v} value={v}>{v.replace('_', ' ')}</option>)}
        </select>
        <select value={filters.priority} onChange={e => set('priority', e.target.value)} style={s.select}>
          <option value="">All Priorities</option>
          {['low', 'medium', 'high', 'critical'].map(v => <option key={v} value={v}>{v}</option>)}
        </select>
        <button onClick={() => setFilters({ status: '', priority: '' })} style={s.clearBtn}>Clear</button>
      </div>
      {isLoading ? <p>Loading...</p> : (
        <table style={s.table}>
          <thead><tr style={{ background: '#f0f2f5', textAlign: 'left' }}>
            <th>ID</th><th>Title</th><th>Priority</th><th>Status</th><th>Assigned</th><th>Due</th><th></th>
          </tr></thead>
          <tbody>
            {data?.results?.map(t => (
              <tr key={t.id} style={{ borderBottom: '1px solid #f0f0f0', fontSize: 14 }}>
                <td>#{t.id}</td>
                <td>{t.title}</td>
                <td><span style={{ ...s.badge, background: PC[t.priority] }}>{t.priority}</span></td>
                <td><span style={{ ...s.badge, background: SC[t.status] }}>{t.status.replace('_', ' ')}</span></td>
                <td>{t.assigned_to_username ?? '—'}</td>
                <td>{t.due_date ?? '—'}</td>
                <td><Link to={`/tasks/${t.id}`}>View</Link></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {!isLoading && !data?.results?.length && <p style={{ color: '#888', marginTop: 16 }}>No tasks found.</p>}
    </div>
  )
}

const s = {
  btn: { background: '#4f8ef7', color: '#fff', padding: '8px 16px', borderRadius: 4, textDecoration: 'none', fontSize: 14 },
  select: { padding: '7px 10px', border: '1px solid #ddd', borderRadius: 4, fontSize: 13 },
  clearBtn: { padding: '7px 12px', border: '1px solid #ddd', borderRadius: 4, cursor: 'pointer', background: '#fff' },
  table: { width: '100%', borderCollapse: 'collapse', background: '#fff', borderRadius: 8 },
  badge: { color: '#fff', padding: '3px 8px', borderRadius: 12, fontSize: 12 },
}
