import ActivityPage from '@core/pages/ActivityPage.vue'
import AttendancePage from '@core/pages/AttendancePage.vue'
import DeadlinesPage from '@core/pages/DeadlinesPage.vue'
import HistoryPage from '@core/pages/HistoryPage.vue'
import LessonEditPage from '@core/pages/LessonEditPage.vue'
import LessonPage from '@core/pages/LessonPage.vue'
import LessonsPage from '@core/pages/LessonsPage.vue'
import LoginPage from '@core/pages/LoginPage.vue'
import MyWeekPage from '@core/pages/MyWeekPage.vue'
import NotFoundPage from '@core/pages/NotFoundPage.vue'
import PollEditPage from '@core/pages/PollEditPage.vue'
import PollMatrixPage from '@core/pages/PollMatrixPage.vue'
import PollPage from '@core/pages/PollPage.vue'
import PollTemplatesPage from '@core/pages/PollTemplatesPage.vue'
import PollsPage from '@core/pages/PollsPage.vue'
import ProfilePage from '@core/pages/ProfilePage.vue'
import StudentEditPage from '@core/pages/StudentEditPage.vue'
import StudentsPage from '@core/pages/StudentsPage.vue'
import TablePage from '@core/pages/TablePage.vue'
import ViewsPage from '@core/pages/ViewsPage.vue'
import WeekPage from '@core/pages/WeekPage.vue'
import { makeRouter } from '@core/router.js'

import DocPage from './pages/DocPage.vue'
import DocsPage from './pages/DocsPage.vue'
import HomePage from './pages/HomePage.vue'
import LabPartPage from './pages/LabPartPage.vue'
import LabResultsPage from './pages/LabResultsPage.vue'
import LabReviewPage from './pages/LabReviewPage.vue'
import MyLabPage from './pages/MyLabPage.vue'
import MyNotebookPage from './pages/MyNotebookPage.vue'

// lectures and labs are for signed-in NURE students (T166 Q4)
const docs = (kind, title) => [
  { path: `/${kind}`, component: DocsPage, meta: { title, kind, access: 'active' } },
  { path: `/${kind}/:n`, component: DocPage, meta: { title, kind, access: 'active', filters: true } },
]

// the platform's pages stand here with the same addresses and meta as on the python site (app/vue/src/router.js)
export default makeRouter([
  { path: '/', component: HomePage },
  ...docs('lectures', 'Лекції'),
  ...docs('labs', 'Лаби'),
  { path: '/labs/:n/my', component: MyLabPage, meta: { title: 'Моя лаба', access: 'active' } },
  { path: '/labs/:n/my/nb/:id', component: MyNotebookPage, meta: { title: 'Мій ноутбук', access: 'active', wide: true } },  // the file as the teacher sees it (T354)
  { path: '/labs/:n/results', component: LabResultsPage, meta: { title: 'Результати', access: 'admin', wide: true } },
  { path: '/labs/:n/results/:vid', component: LabReviewPage, meta: { title: 'Перевірка', access: 'admin', wide: true } },  // the notebook next to the key and the marks
  // the labs' pages beyond the task itself (labPages.js): /labs/3/guide — a part of a lab, /labs/about/grading — common to all labs
  { path: '/labs/about/:part', component: LabPartPage, meta: { title: 'Лаби', access: 'active', about: true } },
  { path: '/labs/:n(\\d+)/:part', component: LabPartPage, meta: { title: 'Лаби', access: 'active' } },
  { path: '/lessons', component: LessonsPage, meta: { title: 'Пари', access: 'active', filters: true } },
  { path: '/lessons/new', component: LessonEditPage, meta: { title: 'Нова пара', access: 'admin' } },
  { path: '/lessons/:slug', component: LessonPage, meta: { title: 'Пари', access: 'active' } },
  { path: '/lessons/:slug/edit', component: LessonEditPage, meta: { title: 'Пари', access: 'admin' } },
  { path: '/attendance', component: AttendancePage, meta: { title: 'Відвідування', access: 'admin', wide: true, filters: true } },  // students × lessons, from Zoom (T222)
  { path: '/my/week', component: MyWeekPage, meta: { title: 'Мій тиждень', access: 'active' } },
  { path: '/week/:day(\\d)?', component: WeekPage, meta: { title: 'Тиждень', access: 'active', filters: true, stay: true, wide: 'admin' } },
  { path: '/method/history', component: HistoryPage, meta: { title: 'Історія правок', access: 'admin' } },
  { path: '/login', component: LoginPage, meta: { title: 'Вхід' } },
  { path: '/my/profile', component: ProfilePage, meta: { title: 'Профіль', access: 'active' } },
  { path: '/students', component: StudentsPage, meta: { title: 'Студенти', access: 'admin' } },
  { path: '/students/:nick', redirect: (to) => `/students/${to.params.nick}/edit` },  // bot alerts and crumbs lead here
  { path: '/students/:nick/edit', component: StudentEditPage, meta: { title: 'Студенти', access: 'admin' } },
  { path: '/deadlines', component: DeadlinesPage, meta: { title: 'Дедлайни', access: 'admin', wide: true, filters: true } },  // students × labs (T235)
  { path: '/table', component: TablePage, meta: { title: 'Звід', access: 'admin', wide: 'table', filters: true } },  // students × anything, in views (T240, T315)
  { path: '/table/views', component: ViewsPage, meta: { title: 'Види', access: 'admin', filters: true } },
  { path: '/activity', component: ActivityPage, meta: { title: 'Активність', access: 'admin', filters: true } },
  { path: '/polls', component: PollsPage, meta: { title: 'Опитування', access: 'admin', filters: true } },
  { path: '/polls/new', component: PollEditPage, meta: { title: 'Нове опитування', access: 'admin' } },
  { path: '/polls/templates', component: PollTemplatesPage, meta: { title: 'Шаблони опитувань', access: 'admin' } },
  { path: '/polls/matrix', component: PollMatrixPage, meta: { title: 'Хто як відповідав', access: 'admin', wide: true, filters: true } },
  { path: '/polls/:id', component: PollPage, meta: { title: 'Опитування', access: 'admin' } },
  { path: '/polls/:id/edit', component: PollEditPage, meta: { title: 'Опитування', access: 'admin' } },
  { path: '/:pathMatch(.*)*', component: NotFoundPage, meta: { title: 'Такої сторінки нема' } },
])
