import { createRouter, createWebHistory } from 'vue-router'

import { down } from './http.js'
import { canAccess, safeNext, user, userLoaded } from './user.js'

// the site lists its routes, the platform's pages among them; meta.access: 'admin' | 'active' | none = open to all
export function makeRouter(routes) {
  const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, saved) {
      if (saved) return saved
      if (to.hash) return  // the guide text scrolls to the anchor itself once it has loaded (anchors.js)
      if (to.path === from.path && to.meta.filters) return  // ?query filters keep the position
      return { top: 0 }
    },
  })

  router.beforeEach(async (to) => {
    await userLoaded
    if (down.value && !user.value) return true  // the API is silent: the app shows the banner, not «Потрібен вхід»
    if (to.path === '/login') {  // nothing to ask: go where they were heading
      const next = safeNext(to.query.next)
      return user.value && canAccess(router.resolve(next).meta.access) ? next : true
    }
    if (!canAccess(to.meta.access)) return { path: '/login', query: { next: to.fullPath } }
  })
  return router
}
