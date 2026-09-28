import { createRouter, createWebHistory } from 'vue-router'

import ActivityPage from './pages/ActivityPage.vue'
import CardHistoryPage from './pages/CardHistoryPage.vue'
import Colors2Page from './pages/Colors2Page.vue'
import ColorsPage from './pages/ColorsPage.vue'
import GameEditPage from './pages/GameEditPage.vue'
import GamePage from './pages/GamePage.vue'
import GamesPage from './pages/GamesPage.vue'
import GuidePage from './pages/GuidePage.vue'
import HistoryPage from './pages/HistoryPage.vue'
import HomePage from './pages/HomePage.vue'
import LoginPage from './pages/LoginPage.vue'
import MethodPage from './pages/MethodPage.vue'
import MyGamePage from './pages/MyGamePage.vue'
import NotFoundPage from './pages/NotFoundPage.vue'
import ProfilePage from './pages/ProfilePage.vue'
import RefsPage from './pages/RefsPage.vue'
import StudentEditPage from './pages/StudentEditPage.vue'
import StudentGamePage from './pages/StudentGamePage.vue'
import StudentsPage from './pages/StudentsPage.vue'
import TaskEditPage from './pages/TaskEditPage.vue'
import TasksPage from './pages/TasksPage.vue'
import { CHANGES, SECTIONS } from './guide.js'
import { down } from './http.js'
import { canAccess, safeNext, user, userLoaded } from './user.js'

// the guide is unfinished, so it is admin-only for now (T136; drop `hidden` to reopen); students get only the profile
const hidden = { access: 'admin' }
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomePage },
    ...[...SECTIONS, CHANGES].filter((s) => s.page).map((s) => ({ path: s.path, component: GuidePage, meta: { title: s.nav, slug: s.slug, ...hidden } })),
    { path: '/labs/:n', component: GuidePage, meta: { title: 'Лаби', ...hidden } },
    { path: '/method', component: MethodPage, meta: { title: 'Методичка', ...hidden } },
    { path: '/method/history', component: HistoryPage, meta: { title: 'Історія правок', access: 'admin' } },
    { path: '/login', component: LoginPage, meta: { title: 'Вхід' } },
    { path: '/my/profile', component: ProfilePage, meta: { title: 'Профіль', access: 'active' } },
    { path: '/profile', redirect: '/my/profile' },  // old links in bot messages and the guide
    { path: '/my/game', component: MyGamePage, meta: { title: 'Моя гра', access: 'admin' } },
    { path: '/students', component: StudentsPage, meta: { title: 'Студенти', access: 'admin' } },
    { path: '/students/:nick', component: StudentGamePage, meta: { title: 'Студенти', access: 'admin' } },
    { path: '/students/:nick/edit', component: StudentEditPage, meta: { title: 'Студенти', access: 'admin' } },
    { path: '/activity', component: ActivityPage, meta: { title: 'Активність', access: 'admin', filters: true } },
    { path: '/ideas', component: RefsPage, meta: { title: 'Знахідки', access: 'admin' } },
    { path: '/refs', redirect: '/ideas' },
    { path: '/games', component: GamesPage, meta: { title: 'Ігри', ...hidden } },  // guide text + catalog; the catalog stays admin-only inside once the guide reopens (T116 Q13)
    { path: '/games/history', component: CardHistoryPage, meta: { title: 'Історія ігор', kind: 'games', access: 'admin' } },
    { path: '/games/new', component: GameEditPage, meta: { title: 'Нова гра', access: 'admin' } },
    { path: '/games/:slug', component: GamePage, meta: { title: 'Ігри', access: 'admin', filters: true } },
    { path: '/games/:slug/edit', component: GameEditPage, meta: { title: 'Ігри', access: 'admin' } },
    { path: '/colors', component: ColorsPage, meta: { title: 'Кольори', access: 'admin' } },
    { path: '/colors2', component: Colors2Page, meta: { title: 'Кольори v2', access: 'admin' } },
    { path: '/tasks', component: TasksPage, meta: { title: 'Таски', wide: true, filters: true, ...hidden } },
    { path: '/tasks/history', component: CardHistoryPage, meta: { title: 'Історія завдань', kind: 'tasks', access: 'admin' } },
    { path: '/tasks/new', component: TaskEditPage, meta: { title: 'Нове завдання', access: 'admin' } },
    { path: '/tasks/:slug/edit', component: TaskEditPage, meta: { title: 'Таски', access: 'admin' } },
    { path: '/:pathMatch(.*)*', component: NotFoundPage, meta: { title: 'Такої сторінки нема' } },  // the server answers any path with index.html, so 404 is ours to show
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
  if (down.value && !user.value) return true  // the API is silent: the app shows the banner, not «Потрібен вхід»
  if (to.path === '/login') {  // nothing to ask: go where they were heading
    const next = safeNext(to.query.next)
    return user.value && canAccess(router.resolve(next).meta.access) ? next : true
  }
  if (!canAccess(to.meta.access)) return { path: '/login', query: { next: to.fullPath } }
})

export default router
