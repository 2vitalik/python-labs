import { request } from '@core/http.js'

// the site's own calls; the platform's are in @core/api.js
export const getLabs = () => request('/api/variants')  // which labs have cards
export const getMyLab = (n) => request(`/api/variants/${n}/my`)
export const putMyLab = (n, data) => request(`/api/variants/${n}/my`, 'PUT', data)
export const getLabResults = (n) => request(`/api/variants/${n}/results`)
export const putLabResult = (n, vid, data) => request(`/api/variants/${n}/results/${vid}`, 'PUT', data)
