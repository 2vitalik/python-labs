import ActivityPage from '@core/pages/ActivityPage.vue'
import AttendancePage from '@core/pages/AttendancePage.vue'
import HistoryPage from '@core/pages/HistoryPage.vue'
import LessonEditPage from '@core/pages/LessonEditPage.vue'
import LessonPage from '@core/pages/LessonPage.vue'
import LessonsPage from '@core/pages/LessonsPage.vue'
import LoginPage from '@core/pages/LoginPage.vue'
import NotFoundPage from '@core/pages/NotFoundPage.vue'
import ProfilePage from '@core/pages/ProfilePage.vue'
import StudentEditPage from '@core/pages/StudentEditPage.vue'
import StudentsPage from '@core/pages/StudentsPage.vue'
import { makeRouter } from '@core/router.js'

import DocPage from './pages/DocPage.vue'
import DocsPage from './pages/DocsPage.vue'
import HomePage from './pages/HomePage.vue'
import LabResultsPage from './pages/LabResultsPage.vue'
import MyLabPage from './pages/MyLabPage.vue'

// lectures and labs are for signed-in NURE students (T166 Q4)
const docs = (kind, title) => [
  { path: `/${kind}`, component: DocsPage, meta: { title, kind, access: 'active' } },
  { path: `/${kind}/:n`, component: DocPage, meta: { title, kind, access: 'active', filters: true } },
]

export default makeRouter([
  { path: '/', component: HomePage },
  ...docs('lectures', 'Лекції'),
  ...docs('labs', 'Лаби'),
  { path: '/labs/:n/my', component: MyLabPage, meta: { title: 'Моя лаба', access: 'active' } },
  { path: '/labs/:n/results', component: LabResultsPage, meta: { title: 'Результати', access: 'admin' } },
  { path: '/lessons', component: LessonsPage, meta: { title: 'Заняття', access: 'active', filters: true } },
  { path: '/lessons/new', component: LessonEditPage, meta: { title: 'Нове заняття', access: 'admin' } },
  { path: '/lessons/:slug', component: LessonPage, meta: { title: 'Заняття', access: 'active' } },
  { path: '/lessons/:slug/edit', component: LessonEditPage, meta: { title: 'Заняття', access: 'admin' } },
  { path: '/attendance', component: AttendancePage, meta: { title: 'Відвідування', access: 'admin', wide: true, filters: true } },  // students × lessons, from Zoom (T222)
  { path: '/method/history', component: HistoryPage, meta: { title: 'Історія правок', access: 'admin' } },
  { path: '/login', component: LoginPage, meta: { title: 'Вхід' } },
  { path: '/my/profile', component: ProfilePage, meta: { title: 'Профіль', access: 'active' } },
  { path: '/students', component: StudentsPage, meta: { title: 'Студенти', access: 'admin' } },
  { path: '/students/:nick', redirect: (to) => `/students/${to.params.nick}/edit` },  // bot alerts and crumbs lead here
  { path: '/students/:nick/edit', component: StudentEditPage, meta: { title: 'Студенти', access: 'admin' } },
  { path: '/activity', component: ActivityPage, meta: { title: 'Активність', access: 'admin', filters: true } },
  { path: '/:pathMatch(.*)*', component: NotFoundPage, meta: { title: 'Такої сторінки нема' } },
])
