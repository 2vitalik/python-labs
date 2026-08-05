async function request(url, method = 'GET', body) {
  const res = await fetch(url, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined,
  })
  const data = res.status === 204 ? null : await res.json()
  if (!res.ok) throw new Error(data?.detail || `Помилка ${res.status}`)
  return data
}

export const getMe = () => request('/api/me')
export const putProfile = (data) => request('/api/profile', 'PUT', data)
export const getStudents = () => request('/api/students')
export const getStudent = (id) => request(`/api/students/${id}`)
export const putStudent = (id, data) => request(`/api/students/${id}`, 'PUT', data)
export const importStudents = (text) => request('/api/students/import', 'POST', { text })
export const getZones = () => request('/api/zones')
export const getGames = () => request('/api/games')
export const getTasks = () => request('/api/tasks')
export const postGame = (data) => request('/api/games', 'POST', data)
export const putGame = (id, data) => request(`/api/games/${id}`, 'PUT', data)
export const postTask = (data) => request('/api/tasks', 'POST', data)
export const putTask = (id, data) => request(`/api/tasks/${id}`, 'PUT', data)
