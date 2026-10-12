import { request } from '@core/http.js'

// the site's own calls; the platform's are in @core/api.js
export const getLabs = () => request('/api/labs')
export const getMyLab = (n) => request(`/api/labs/${n}/my`)
export const putMyLab = (n, data) => request(`/api/labs/${n}/my`, 'PUT', data)
export const getLabResults = (n) => request(`/api/labs/${n}/results`)
export const putLabResult = (n, vid, data) => request(`/api/labs/${n}/results/${vid}`, 'PUT', data)
