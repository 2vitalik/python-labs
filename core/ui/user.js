import { ref } from 'vue'

import { getMe, stopViewAs, viewAs } from './api.js'
import { down } from './http.js'

export const user = ref(null)
// a guest gets `null`, so any failure means nobody knows who is looking: the banner, not the guest's site
export const userLoaded = getMe().then((u) => (user.value = u), () => (down.value = true))

// one session, several tabs: «Очима студента» or a sign-out in another tab changes whom the API answers — a tab left open
// would show one person and write as another, so on coming back it checks who it is and reloads when that changed
document.addEventListener('visibilitychange', async () => {
  if (document.hidden) return
  const now = await getMe().catch(() => undefined)
  if (now !== undefined && now?.email !== user.value?.email) location.reload()
})

// the page the menu's eye was clicked on (this tab): «Повернутись» comes back to it; a look from the students — to /students
const FROM = 'look-from'
const keepFrom = (path) => { try { path ? sessionStorage.setItem(FROM, path) : sessionStorage.removeItem(FROM) } catch { /* → /students */ } }
const takeFrom = () => { try { return sessionStorage.getItem(FROM) } catch { return null } }
// assign() of this very page with another #hash would only scroll, without the reload
const land = (to) => (to.split('#')[0] === location.pathname + location.search ? location.reload() : location.assign(to))

// «Очима студента»: the whole site answers as to a test student; the reload drops what was loaded for the admin
export const lookAs = (nick, to = '/') => { keepFrom(null); return viewAs(nick).then(() => location.assign(to)) }  // `to` — where to land as them
// …as the site's test student (the API finds or makes one), from any page (`route` — the caller's: the router imports
// this module): stay on it unless a student may not open it
export function lookAsTest(route) {
  const here = location.pathname + location.search + location.hash
  keepFrom(here)
  return viewAs().then(() => land(route.meta.access === 'admin' ? '/' : here))
}
export function lookBack() {
  const to = takeFrom() || '/students'
  return stopViewAs().then(() => { keepFrom(null); land(to) })
}

// route access: 'admin' | 'active' (student or admin) | undefined = public
export function canAccess(access) {
  const status = user.value?.status
  if (access === 'admin') return status === 'admin'
  if (access === 'active') return !!status && status !== 'pending'
  return true
}

// `?next=` must stay a same-site path (mirrors safe_path() in the API)
export const safeNext = (p) => (typeof p === 'string' && /^\/(?![/\\])/.test(p) ? p : '/')
