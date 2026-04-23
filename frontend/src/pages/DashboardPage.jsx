import { useQuery } from '@tanstack/react-query'
import { reportsAPI, visitsAPI } from '../api'
import useAuthStore from '../store/authStore'

function Card({ label, value, color = '#4f8ef7' }) {
  return (
    <div style={{ background: '#fff', borderRadius: 8, padding: '20px 24px', minWidth: 140, borderTop: `4px solid ${color}` }}>
      <div style={{ fontSize: 28, fontWeight: 700 }}>{value ?? '—'}</div>
      <div style={{ color: '#888', fontSize: 13, marginTop: 4 }}>{label}</div>
    </div>
  )
}

export default function DashboardPage() {
  const { user } = useAuthStore()
  const { data: dash, isLoading } = useQuery({ queryKey: ['dashboard'], queryFn: () => reportsAPI.dashboard().then(r => r.data) })
  const { data: vs } = useQuery({ queryKey: ['visit-summary'], queryFn: () => visitsAPI.summary().then(r => r.data) })

  if (isLoading) return <p>Loading...</p>

  return (
    <div>
      <h2>Dashboard</h2>
      <p style={{ color: '#888', marginBottom: 20 }}>Welcome, <strong>{user?.username}</strong> — {user?.role?.replace(/_/g, ' ')}</p>

      <h4>Tasks</h4>
      <div style={s.grid}>
        <Card label="Total" value={dash?.tasks?.total} />
        <Card label="Pending" value={dash?.tasks?.pending} color="#f39c12" />
        <Card label="In Progress" value={dash?.tasks?.in_progress} color="#3498db" />
        <Card label="Completed" value={dash?.tasks?.completed} color="#2ecc71" />
        <Card label="Overdue" value={dash?.tasks?.overdue} color="#e74c3c" />
      </div>

      <h4 style={{ marginTop: 28 }}>Visits</h4>
      <div style={s.grid}>
        <Card label="Total" value={vs?.total} />
        <Card label="Active" value={vs?.by_status?.started} color="#9b59b6" />
        <Card label="Completed" value={vs?.by_status?.completed} color="#2ecc71" />
        <Card label="Successful" value={vs?.by_outcome?.successful} color="#27ae60" />
        <Card label="Failed" value={vs?.by_outcome?.failed} color="#e74c3c" />
      </div>

      <h4 style={{ marginTop: 28 }}>Activity</h4>
      <div style={s.grid}>
        <Card label="Last 24h" value={dash?.activity?.last_24h} />
        <Card label="Last 7 days" value={dash?.activity?.last_7d} />
        <Card label="Active Agents" value={dash?.agents?.total_active} color="#16a085" />
      </div>
    </div>
  )
}

const s = { grid: { display: 'flex', gap: 16, flexWrap: 'wrap', marginTop: 12 } }
