import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import ProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import TaskListPage from './pages/tasks/TaskListPage'
import TaskDetailPage from './pages/tasks/TaskDetailPage'
import TaskCreatePage from './pages/tasks/TaskCreatePage'
import VisitListPage from './pages/visits/VisitListPage'
import VisitDetailPage from './pages/visits/VisitDetailPage'
import StartVisitPage from './pages/visits/StartVisitPage'
import ReportsPage from './pages/reports/ReportsPage'
import UsersPage from './pages/admin/UsersPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/tasks" element={<TaskListPage />} />
            <Route path="/tasks/create" element={
              <ProtectedRoute roles={['admin', 'regional_manager', 'team_lead']}>
                <TaskCreatePage />
              </ProtectedRoute>
            } />
            <Route path="/tasks/:id" element={<TaskDetailPage />} />
            <Route path="/visits" element={<VisitListPage />} />
            <Route path="/visits/start" element={
              <ProtectedRoute roles={['field_agent']}>
                <StartVisitPage />
              </ProtectedRoute>
            } />
            <Route path="/visits/:id" element={<VisitDetailPage />} />
            <Route path="/reports" element={
              <ProtectedRoute roles={['admin', 'regional_manager', 'auditor']}>
                <ReportsPage />
              </ProtectedRoute>
            } />
            <Route path="/admin/users" element={
              <ProtectedRoute roles={['admin']}>
                <UsersPage />
              </ProtectedRoute>
            } />
          </Route>
        </Route>
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
