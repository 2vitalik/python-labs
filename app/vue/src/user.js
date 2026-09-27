import { ref } from 'vue'

import { getMe, stopViewAs, viewAs } from './api.js'
import { down } from './http.js'

export const user = ref(null)
// a guest gets `null`, so any failure means nobody knows who is looking: the banner, not the guest's site
export const userLoaded = getMe().then((u) => (user.value = u), () => (down.value = true))

// «Очима студента»: the whole site answers as to a test student; the reload drops what was loaded for the admin
export const lookAs = (nick) => viewAs(nick).then(() => location.assign('/'))
export const lookBack = () => stopViewAs().then(() => location.assign('/students'))

// route access: 'admin' | 'active' (student or admin) | undefined = public
export function canAccess(access) {
  const status = user.value?.status
  if (access === 'admin') return status === 'admin'
  if (access === 'active') return !!status && status !== 'pending'
  return true
}

// `?next=` must stay a same-site path (mirrors safe_path() in the API)
export const safeNext = (p) => (typeof p === 'string' && /^\/(?![/\\])/.test(p) ? p : '/')
