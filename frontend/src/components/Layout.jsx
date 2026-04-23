import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import useAuthStore from '../store/authStore'
import { authAPI } from '../api'
import RoleGuard from './RoleGuard'

const NAV = [
  { to: '/dashboard', label: 'Dashboard', roles: null },
  { to: '/tasks', label: 'Tasks', roles: null },
  { to: '/tasks/create', label: '+ New Task', roles: ['admin', 'regional_manager', 'team_lead'] },
  { to: '/visits', label: 'Visits', roles: null },
  { to: '/visits/start', label: '+ Start Visit', roles: ['field_agent'] },
  { to: '/reports', label: 'Reports', roles: ['admin', 'regional_manager', 'auditor'] },
  { to: '/admin/users', label: 'Users', roles: ['admin'] },
]

export default function Layout() {
  const { user, clearAuth } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = async () => {
    try { await authAPI.logout(localStorage.getItem('refresh_token')) } finally {
      clearAuth()
      navigate('/login')
    }
  }

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <aside style={s.sidebar}>
        <div style={s.brand}>FieldOps</div>
        <nav>
          {NAV.map(({ to, label, roles }) => (
            <RoleGuard key={to} roles={roles}>
              <NavLink to={to} style={({ isActive }) => ({ ...s.navLink, ...(isActive ? s.navActive : {}) })}>
                {label}
              </NavLink>
            </RoleGuard>
          ))}
        </nav>
        <div style={s.userInfo}>
          <small>{user?.username}</small><br />
          <small style={{ color: '#aaa' }}>{user?.role?.replace(/_/g, ' ')}</small><br />
          <button onClick={handleLogout} style={s.logoutBtn}>Logout</button>
        </div>
      </aside>
      <main style={s.main}><Outlet /></main>
    </div>
  )
}

const s = {
  sidebar: { width: 220, background: '#1a1a2e', color: '#fff', display: 'flex', flexDirection: 'column', padding: '20px 0', position: 'fixed', top: 0, left: 0, height: '100vh' },
  brand: { fontSize: 22, fontWeight: 700, padding: '0 20px 20px', borderBottom: '1px solid #333', marginBottom: 10 },
  navLink: { display: 'block', padding: '10px 20px', color: '#ccc', textDecoration: 'none', fontSize: 14 },
  navActive: { color: '#fff', background: '#16213e', borderLeft: '3px solid #4f8ef7' },
  userInfo: { marginTop: 'auto', padding: '16px 20px', borderTop: '1px solid #333' },
  logoutBtn: { marginTop: 8, background: '#e74c3c', color: '#fff', border: 'none', padding: '6px 12px', cursor: 'pointer', borderRadius: 4 },
  main: { marginLeft: 220, padding: 30, flex: 1, background: '#f5f6fa', minHeight: '100vh' },
}
