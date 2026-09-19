import { ref } from 'vue'

import { getMe } from './api.js'

export const user = ref(null)
export const userLoaded = getMe().then((u) => (user.value = u)).catch(() => {})  // API down → stay a guest

// route access: 'admin' | 'active' (student or admin) | undefined = public
export function canAccess(access) {
  const status = user.value?.status
  if (access === 'admin') return status === 'admin'
  if (access === 'active') return !!status && status !== 'pending'
  return true
}
