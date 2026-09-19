async function handle(res) {
  const data = res.status === 204 ? null : await res.json()
  if (!res.ok) throw new Error(data?.detail || `Помилка ${res.status}`)
  return data
}

async function request(url, method = 'GET', body) {
  return handle(await fetch(url, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined,
  }))
}

async function upload(url, file) {
  const fd = new FormData()
  fd.append('file', file)
  return handle(await fetch(url, { method: 'POST', body: fd }))
}

export const getMe = () => request('/api/me')
export const putProfile = (data) => request('/api/profile', 'PUT', data)
export const unlinkTelegram = () => request('/api/me/telegram', 'DELETE')
export const getStudents = () => request('/api/students')
export const getStudent = (nick) => request(`/api/students/${nick}`)
export const putStudent = (nick, data) => request(`/api/students/${nick}`, 'PUT', data)
export const importStudents = (text) => request('/api/students/import', 'POST', { text })
export const getStudentGame = (nick) => request(`/api/students/${nick}/game`)
export const getZones = () => request('/api/zones')
export const getGames = () => request('/api/games')
export const getTasks = () => request('/api/tasks')
export const postGame = (data) => request('/api/games', 'POST', data)
export const putGame = (id, data) => request(`/api/games/${id}`, 'PUT', data)
export const postTask = (data) => request('/api/tasks', 'POST', data)
export const putTask = (id, data) => request(`/api/tasks/${id}`, 'PUT', data)
export const getMyGame = () => request('/api/my/game')
export const postMyGame = (data) => request('/api/my/game', 'POST', data)
export const putMyGame = (data) => request('/api/my/game', 'PUT', data)
export const postPart = (data) => request('/api/my/game/parts', 'POST', data)
export const putPart = (id, data) => request(`/api/my/game/parts/${id}`, 'PUT', data)
export const deletePart = (id) => request(`/api/my/game/parts/${id}`, 'DELETE')
export const uploadShot = (id, file) => upload(`/api/my/game/parts/${id}/screenshot`, file)
export const deleteShot = (id, name) => request(`/api/my/game/parts/${id}/screenshot/${name}`, 'DELETE')
export const postClaim = (data) => request('/api/my/claims', 'POST', data)
export const putClaim = (id, data) => request(`/api/my/claims/${id}`, 'PUT', data)
export const deleteClaim = (id) => request(`/api/my/claims/${id}`, 'DELETE')
export const postRule = (data) => request('/api/my/game/rules', 'POST', data)
export const putRule = (id, data) => request(`/api/my/game/rules/${id}`, 'PUT', data)
export const deleteRule = (id) => request(`/api/my/game/rules/${id}`, 'DELETE')
export const getRefs = () => request('/api/refs')
export const postRef = (data) => request('/api/refs', 'POST', data)
export const putRef = (id, data) => request(`/api/refs/${id}`, 'PUT', data)
export const deleteRef = (id) => request(`/api/refs/${id}`, 'DELETE')
