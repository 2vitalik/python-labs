import ActivityPage from '@core/pages/ActivityPage.vue'
import HistoryPage from '@core/pages/HistoryPage.vue'
import LoginPage from '@core/pages/LoginPage.vue'
import NotFoundPage from '@core/pages/NotFoundPage.vue'
import ProfilePage from '@core/pages/ProfilePage.vue'
import StudentEditPage from '@core/pages/StudentEditPage.vue'
import StudentsPage from '@core/pages/StudentsPage.vue'
import { makeRouter } from '@core/router.js'

import DocPage from './pages/DocPage.vue'
import DocsPage from './pages/DocsPage.vue'
import HomePage from './pages/HomePage.vue'

// lectures and labs are for signed-in NURE students (T166 Q4)
const docs = (kind, title) => [
  { path: `/${kind}`, component: DocsPage, meta: { title, kind, access: 'active' } },
  { path: `/${kind}/:n`, component: DocPage, meta: { title, kind, access: 'active', filters: true } },
]

export default makeRouter([
  { path: '/', component: HomePage },
  ...docs('lectures', 'Лекції'),
  ...docs('labs', 'Лаби'),
  { path: '/method/history', component: HistoryPage, meta: { title: 'Історія правок', access: 'admin' } },
  { path: '/login', component: LoginPage, meta: { title: 'Вхід' } },
  { path: '/my/profile', component: ProfilePage, meta: { title: 'Профіль', access: 'active' } },
  { path: '/students', component: StudentsPage, meta: { title: 'Студенти', access: 'admin' } },
  { path: '/students/:nick', redirect: (to) => `/students/${to.params.nick}/edit` },  // bot alerts and crumbs lead here
  { path: '/students/:nick/edit', component: StudentEditPage, meta: { title: 'Студенти', access: 'admin' } },
  { path: '/activity', component: ActivityPage, meta: { title: 'Активність', access: 'admin', filters: true } },
  { path: '/:pathMatch(.*)*', component: NotFoundPage, meta: { title: 'Такої сторінки нема' } },
])
