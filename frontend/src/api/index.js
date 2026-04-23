import api from './axios'

export const authAPI = {
  login: (data) => api.post('/auth/login/', data),
  logout: (refresh) => api.post('/auth/logout/', { refresh }),
  me: () => api.get('/auth/me/'),
}

export const tasksAPI = {
  list: (params) => api.get('/tasks/', { params }),
  detail: (id) => api.get(`/tasks/${id}/`),
  create: (data) => api.post('/tasks/', data),
  update: (id, data) => api.patch(`/tasks/${id}/`, data),
  delete: (id) => api.delete(`/tasks/${id}/`),
  assign: (id, data) => api.post(`/tasks/${id}/assign/`, data),
  updateStatus: (id, data) => api.post(`/tasks/${id}/status/`, data),
  aiSuggestion: (id) => api.get(`/tasks/${id}/ai-suggestion/`),
  summary: () => api.get('/tasks/summary/'),
}

export const visitsAPI = {
  list: (params) => api.get('/visits/', { params }),
  detail: (id) => api.get(`/visits/${id}/`),
  start: (data) => api.post('/visits/start/', data),
  complete: (id, data) => api.post(`/visits/${id}/complete/`, data),
  cancel: (id, data) => api.post(`/visits/${id}/cancel/`, data),
  addNotes: (id, data) => api.patch(`/visits/${id}/notes/`, data),
  active: () => api.get('/visits/active/'),
  summary: () => api.get('/visits/summary/'),
}

export const reportsAPI = {
  dashboard: () => api.get('/dashboard/'),
  taskSummary: (params) => api.get('/reports/task-summary/', { params }),
  agentPerformance: (params) => api.get('/reports/agent-performance/', { params }),
  visitOutcomes: (params) => api.get('/reports/visit-outcomes/', { params }),
}

export const usersAPI = {
  list: (params) => api.get('/users/', { params }),
  detail: (id) => api.get(`/users/${id}/`),
  create: (data) => api.post('/users/', data),
  update: (id, data) => api.patch(`/users/${id}/`, data),
  deactivate: (id) => api.delete(`/users/${id}/`),
  byRole: (role) => api.get(`/users/by-role/${role}/`),
  regions: () => api.get('/regions/'),
  teams: (regionId) => api.get('/teams/', { params: regionId ? { region: regionId } : {} }),
}
