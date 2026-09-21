import { createRouter, createWebHistory } from 'vue-router'

import Colors2Page from './pages/Colors2Page.vue'
import ColorsPage from './pages/ColorsPage.vue'
import GameEditPage from './pages/GameEditPage.vue'
import GamePage from './pages/GamePage.vue'
import GamesPage from './pages/GamesPage.vue'
import GuideAllPage from './pages/GuideAllPage.vue'
import GuidePage from './pages/GuidePage.vue'
import HomePage from './pages/HomePage.vue'
import LoginPage from './pages/LoginPage.vue'
import MyGamePage from './pages/MyGamePage.vue'
import ProfilePage from './pages/ProfilePage.vue'
import RefsPage from './pages/RefsPage.vue'
import StudentEditPage from './pages/StudentEditPage.vue'
import StudentGamePage from './pages/StudentGamePage.vue'
import StudentsPage from './pages/StudentsPage.vue'
import TaskEditPage from './pages/TaskEditPage.vue'
import TasksPage from './pages/TasksPage.vue'
import { CHANGES, SECTIONS } from './guide.js'
import { canAccess, safeNext, user, userLoaded } from './user.js'

// the guide is public; students get only the profile, everything else stays admin-only until reopened page by page
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomePage },
    ...[...SECTIONS, CHANGES].filter((s) => s.page).map((s) => ({ path: s.path, component: GuidePage, meta: { slug: s.slug } })),
    { path: '/labs/:n', component: GuidePage },
    { path: '/all', component: GuideAllPage },
    { path: '/login', component: LoginPage },
    { path: '/profile', component: ProfilePage, meta: { access: 'active' } },
    { path: '/my/game', component: MyGamePage, meta: { access: 'admin' } },
    { path: '/students', component: StudentsPage, meta: { access: 'admin' } },
    { path: '/students/:nick', component: StudentGamePage, meta: { access: 'admin' } },
    { path: '/students/:nick/edit', component: StudentEditPage, meta: { access: 'admin' } },
    { path: '/refs', component: RefsPage, meta: { access: 'admin' } },
    { path: '/games', component: GamesPage },  // guide text for all, the catalog itself is admin-only inside
    { path: '/games/new', component: GameEditPage, meta: { access: 'admin' } },
    { path: '/games/:slug', component: GamePage, meta: { access: 'admin', filters: true } },
    { path: '/games/:slug/edit', component: GameEditPage, meta: { access: 'admin' } },
    { path: '/colors', component: ColorsPage, meta: { access: 'admin' } },
    { path: '/colors2', component: Colors2Page, meta: { access: 'admin' } },
    { path: '/tasks', component: TasksPage, meta: { wide: true, filters: true } },
    { path: '/tasks/new', component: TaskEditPage, meta: { access: 'admin' } },
    { path: '/tasks/:slug/edit', component: TaskEditPage, meta: { access: 'admin' } },
  ],
  scrollBehavior(to, from, saved) {
    if (saved) return saved
    if (to.hash) return  // the guide text scrolls to the anchor itself once it has loaded (anchors.js)
    if (to.path === from.path && to.meta.filters) return  // the catalog's ?query filters keep the position
    return { top: 0 }
  },
})

router.beforeEach(async (to) => {
  await userLoaded
  if (to.path === '/login') {  // nothing to ask: go where they were heading
    const next = safeNext(to.query.next)
    return user.value && canAccess(router.resolve(next).meta.access) ? next : true
  }
  if (!canAccess(to.meta.access)) return { path: '/login', query: { next: to.fullPath } }
})

export default router
