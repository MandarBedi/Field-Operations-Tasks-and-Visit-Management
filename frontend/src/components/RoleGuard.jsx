import useAuthStore from '../store/authStore'

export default function RoleGuard({ roles, children, fallback = null }) {
  const { user } = useAuthStore()
  if (!user) return fallback
  if (roles && !roles.includes(user.role)) return fallback
  return children
}
