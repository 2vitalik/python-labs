import { request, upload } from '@core/http.js'

// the site's own calls; the platform's are in @core/api.js
export const getStudentGame = (nick) => request(`/api/students/${nick}/game`)
export const judgeClaim = (nick, id, data) => request(`/api/students/${nick}/claims/${id}`, 'PUT', data)
export const getGameHistory = (nick, params) => request(`/api/students/${nick}/game/history?${new URLSearchParams(params)}`)  // {limit, before}
export const getZones = () => request('/api/zones')
export const getVocab = () => request('/api/vocab')
export const getTemplates = () => request('/api/templates')
export const getGames = () => request('/api/games')
export const getEtalon = (slug) => request(`/api/games/${slug}/etalon`)  // the base game's reference description, shaped as a student's game
export const getSandbox = (slug) => request(`/api/games/${slug}/sandbox`)  // the reader's scratch copy of the sample (T274 §7)
export const resetSandbox = (slug) => request(`/api/games/${slug}/sandbox`, 'POST')
export const getTasks = () => request('/api/tasks')
export const postGame = (data) => request('/api/games', 'POST', data)
export const putGame = (id, data) => request(`/api/games/${id}`, 'PUT', data)
export const postTask = (data) => request('/api/tasks', 'POST', data)
export const putTask = (id, data) => request(`/api/tasks/${id}`, 'PUT', data)
export const getAsks = () => request('/api/asks')  // the cards «за запитом» someone added, the most asked first (T319)
export const putAsk = (id, data) => request(`/api/asks/${id}`, 'PUT', data)  // { verdict?, status?, task? }: a reply, return, accept, move
export const getCardHistory = (kind, slug) => request(`/api/catalog/history/${kind}${slug ? `?slug=${slug}` : ''}`)
export const revertCard = (kind, id) => request(`/api/catalog/history/${kind}/${id}/revert`, 'POST')
export const getMyGame = () => request('/api/my/game')
export const postMyGame = (data) => request('/api/my/game', 'POST', data)
export const putMyGame = (data) => request('/api/my/game', 'PUT', data)
export const putMyExtras = (extras) => request('/api/my/game/extras', 'PUT', { extras })  // the features turned on (T319)
export const putFeatures = (closed) => request('/api/features', 'PUT', { closed })  // the teacher: the features closed for students
export const applyTemplate = (slug = '') => request('/api/my/game/template', 'POST', { slug })
export const postPart = (data) => request('/api/my/game/parts', 'POST', data)
export const putPart = (id, data) => request(`/api/my/game/parts/${id}`, 'PUT', data)
export const deletePart = (id) => request(`/api/my/game/parts/${id}`, 'DELETE')
export const uploadShot = (id, file) => upload(`/api/my/game/parts/${id}/screenshot`, file)
export const deleteShot = (id, name) => request(`/api/my/game/parts/${id}/screenshot/${name}`, 'DELETE')
export const postClaim = (data) => request('/api/my/claims', 'POST', data)
export const putClaim = (id, data) => request(`/api/my/claims/${id}`, 'PUT', data)
export const deleteClaim = (id) => request(`/api/my/claims/${id}`, 'DELETE')
export const uploadClaimShot = (id, file) => upload(`/api/my/claims/${id}/shot`, file)  // the claim's proof (T284 §7)
export const deleteClaimShot = (id, name) => request(`/api/my/claims/${id}/shot/${name}`, 'DELETE')
export const putVideo = (slot, data) => request(`/api/my/game/videos/${encodeURIComponent(slot)}`, 'PUT', data)  // { link, note }: a new link is a new version (T318)
export const judgeVideo = (nick, slot, data) => request(`/api/students/${nick}/videos/${encodeURIComponent(slot)}`, 'PUT', data)  // the teacher: need, why, status, verdict
export const postRule = (data) => request('/api/my/game/rules', 'POST', data)
export const putRule = (id, data) => request(`/api/my/game/rules/${id}`, 'PUT', data)
export const deleteRule = (id) => request(`/api/my/game/rules/${id}`, 'DELETE')
export const getRefs = () => request('/api/refs')
export const postRef = (data) => request('/api/refs', 'POST', data)
export const putRef = (id, data) => request(`/api/refs/${id}`, 'PUT', data)
export const deleteRef = (id) => request(`/api/refs/${id}`, 'DELETE')
export const judgeRef = (id, data) => request(`/api/refs/${id}/verdict`, 'PUT', data)  // the teacher: taken / dropped, a reply
// defenses and their remarks (T326): the teacher's pages, then the student's answers
export const getDefenseVocab = () => request('/api/defenses/vocab')
export const getDefenses = () => request('/api/defenses')
export const postDefense = (data) => request('/api/defenses', 'POST', data)  // { nick, labs, kind }: it starts now
export const getDefense = (id) => request(`/api/defenses/${id}`)
export const putDefense = (id, data) => request(`/api/defenses/${id}`, 'PUT', data)
export const sendDefense = (id) => request(`/api/defenses/${id}/send`, 'POST')  // the drafts open to the student
export const deleteDefense = (id) => request(`/api/defenses/${id}`, 'DELETE')
export const postRemarks = (id, text) => request(`/api/defenses/${id}/remarks`, 'POST', { text })  // a line — a remark
export const putRemark = (id, data) => request(`/api/remarks/${id}`, 'PUT', data)
export const checkRemark = (id, data) => request(`/api/remarks/${id}/check`, 'PUT', data)  // { state, note }
export const deleteRemark = (id) => request(`/api/remarks/${id}`, 'DELETE')
export const getMyRemarks = () => request('/api/my/remarks')
export const replyRemark = (id, data) => request(`/api/my/remarks/${id}`, 'PUT', data)  // { state, note, link }
