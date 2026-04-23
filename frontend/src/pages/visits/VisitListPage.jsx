import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { visitsAPI } from '../../api'
import useAuthStore from '../../store/authStore'

export default function VisitListPage() {
  const { user } = useAuthStore()
  const { data, isLoading } = useQuery({ queryKey: ['visits'], queryFn: () => visitsAPI.list().then(r => r.data) })

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <h2 style={{ margin: 0 }}>Visits</h2>
        {user?.role === 'field_agent' && <Link to="/visits/start" style={s.btn}>+ Start Visit</Link>}
      </div>
      {isLoading ? <p>Loading...</p> : (
        <table style={s.table}>
          <thead><tr style={{ background: '#f0f2f5', textAlign: 'left' }}>
            <th>ID</th><th>Agent</th><th>Location</th><th>Task</th><th>Status</th><th>Outcome</th><th>Started</th><th></th>
          </tr></thead>
          <tbody>
            {data?.results?.map(v => (
              <tr key={v.id} style={{ borderBottom: '1px solid #f0f0f0', fontSize: 14 }}>
                <td>#{v.id}</td>
                <td>{v.field_agent_username}</td>
                <td>{v.location_name}</td>
                <td>{v.task_title ?? '—'}</td>
                <td>{v.status}</td>
                <td>{v.outcome ?? '—'}</td>
                <td>{new Date(v.started_at).toLocaleString()}</td>
                <td><Link to={`/visits/${v.id}`}>View</Link></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {!isLoading && !data?.results?.length && <p style={{ color: '#888', marginTop: 16 }}>No visits found.</p>}
    </div>
  )
}

const s = {
  btn: { background: '#4f8ef7', color: '#fff', padding: '8px 16px', borderRadius: 4, textDecoration: 'none', fontSize: 14 },
  table: { width: '100%', borderCollapse: 'collapse', background: '#fff', borderRadius: 8, fontSize: 14 },
}
