import { extra, request, upload } from '@core/http.js'

// the site's own calls; the platform's are in @core/api.js
export const getLabs = () => request('/api/variants')  // which labs have cards
export const getMyLab = (n) => request(`/api/variants/${n}/my`)
export const findMyLab = (n) => request(`/api/variants/${n}/my?soft=1`)  // no card yet — {vid: null, why} instead of a 404
export const putMyLab = (n, data) => request(`/api/variants/${n}/my`, 'PUT', data)
export const getLabFree = (n) => request(`/api/variants/${n}/free`)  // the numbers of the student's stream nobody holds yet
export const claimLab = (n, num) => request(`/api/variants/${n}/my/claim`, 'POST', { n: num })
export const sendLabFile = (n, file) => upload(`/api/variants/${n}/my/file`, file)
export const pullLabFile = (n) => request(`/api/variants/${n}/my/pull`, 'POST')
export const labStartUrl = (n, as) => `/api/variants/${n}/my/start?as=${as}`  // the template with the student's card in it, as a file
export const getLabStart = async (n, as) => {
  const res = await fetch(labStartUrl(n, as), { headers: { ...extra } })
  if (!res.ok) throw new Error('Не вдалося взяти шаблон ноутбука')
  return res.text()
}
export const getLabFile = (id) => request(`/api/variants/file/${id}`)  // a notebook parsed for showing
export const labFileRawUrl = (id) => `/api/variants/file/${id}/raw`
export const getLabResults = (n) => request(`/api/variants/${n}/results`)
export const getLabReview = (n, vid) => request(`/api/variants/${n}/results/${vid}`)
export const putLabResult = (n, vid, data) => request(`/api/variants/${n}/results/${vid}`, 'PUT', data)
export const getLabStats = (n) => request(`/api/variants/${n}/stats`)
// «Вхідні» (T368): what the teacher forwarded to the bot from students' chats
export const getIntake = () => request('/api/intake')
export const putIntakePerson = (key, student) => request('/api/intake/person', 'PUT', { key, student })  // student — a nick; '' — nobody's again
export const putIntakeRow = (id, data) => request(`/api/intake/${id}`, 'PUT', data)  // {lab, asks, skip} — only what is sent changes
export const applyIntakeRow = (id) => request(`/api/intake/${id}/apply`, 'POST')  // once more: make the notebook a version of «Моя лаба»
export const intakeRawUrl = (id) => `/api/intake/${id}/raw`
