import { createRouter, createWebHistory } from 'vue-router'

import Colors2Page from './pages/Colors2Page.vue'
import ColorsPage from './pages/ColorsPage.vue'
import GameEditPage from './pages/GameEditPage.vue'
import GamePage from './pages/GamePage.vue'
import GamesPage from './pages/GamesPage.vue'
import HomePage from './pages/HomePage.vue'
import MyGamePage from './pages/MyGamePage.vue'
import ProfilePage from './pages/ProfilePage.vue'
import RefsPage from './pages/RefsPage.vue'
import StudentEditPage from './pages/StudentEditPage.vue'
import StudentGamePage from './pages/StudentGamePage.vue'
import StudentsPage from './pages/StudentsPage.vue'
import TaskEditPage from './pages/TaskEditPage.vue'
import TasksPage from './pages/TasksPage.vue'
import { canAccess, userLoaded } from './user.js'

// for now students get only the profile; everything else stays admin-only until reopened page by page
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomePage },
    { path: '/profile', component: ProfilePage, meta: { access: 'active' } },
    { path: '/my/game', component: MyGamePage, meta: { access: 'admin' } },
    { path: '/students', component: StudentsPage, meta: { access: 'admin' } },
    { path: '/students/:nick', component: StudentGamePage, meta: { access: 'admin' } },
    { path: '/students/:nick/edit', component: StudentEditPage, meta: { access: 'admin' } },
    { path: '/refs', component: RefsPage, meta: { access: 'admin' } },
    { path: '/games', component: GamesPage, meta: { access: 'admin' } },
    { path: '/games/new', component: GameEditPage, meta: { access: 'admin' } },
    { path: '/games/:slug', component: GamePage, meta: { access: 'admin', wide: true } },
    { path: '/games/:slug/edit', component: GameEditPage, meta: { access: 'admin' } },
    { path: '/colors', component: ColorsPage, meta: { access: 'admin' } },
    { path: '/colors2', component: Colors2Page, meta: { access: 'admin' } },
    { path: '/tasks', component: TasksPage, meta: { access: 'admin', wide: true } },
    { path: '/tasks/new', component: TaskEditPage, meta: { access: 'admin' } },
    { path: '/tasks/:slug/edit', component: TaskEditPage, meta: { access: 'admin' } },
  ],
})

router.beforeEach(async (to) => {
  await userLoaded
  if (!canAccess(to.meta.access)) return '/'
})

export default router
