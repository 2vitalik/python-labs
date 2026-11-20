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

import HomePage from './pages/HomePage.vue'
import IntakePage from './pages/IntakePage.vue'
import LabPage from './pages/LabPage.vue'
import LabResultsPage from './pages/LabResultsPage.vue'
import LabReviewPage from './pages/LabReviewPage.vue'
import LabsPage from './pages/LabsPage.vue'
import LectureChangesPage from './pages/LectureChangesPage.vue'
import LecturePage from './pages/LecturePage.vue'
import LecturesPage from './pages/LecturesPage.vue'
import MyLabPage from './pages/MyLabPage.vue'
import MyNotebookPage from './pages/MyNotebookPage.vue'
import OldLabsPage from './pages/OldLabsPage.vue'

// the platform's pages stand here with the same addresses and meta as on the python site (app/vue/src/router.js);
// lectures and labs are for signed-in NURE students (T166 Q4)
export default makeRouter([
  { path: '/', component: HomePage },
  { path: '/lectures', component: LecturesPage, meta: { title: 'Лекції', access: 'active' } },
  // what differs from the lecturer's slides (T374), the teacher's; before `:n` — that one would take «changes» for a number
  { path: '/lectures/changes', component: LectureChangesPage, meta: { title: 'Зміни в лекціях', access: 'admin', wide: 'admin', filters: true } },
  // filters: a change of ?slide keeps the scroll — the text comes back to the slide's place (LecturePage)
  { path: '/lectures/:n', component: LecturePage, meta: { title: 'Лекції', access: 'active', filters: true } },
  { path: '/labs', component: LabsPage, meta: { title: 'Лаби', access: 'active' } },
  { path: '/labs/old', component: OldLabsPage, meta: { title: 'Архів', access: 'admin' } },  // the labs as they were (old-labN)
  { path: '/labs/old/:n(\\d+)', component: OldLabsPage, meta: { title: 'Архів', access: 'admin' } },
  { path: '/labs/:n/my', component: MyLabPage, meta: { title: 'Моя лаба', access: 'active' } },
  { path: '/labs/:n/my/nb/:id', component: MyNotebookPage, meta: { title: 'Мій ноутбук', access: 'active', wide: true } },  // the file as the teacher sees it (T354)
  { path: '/labs/:n/results', component: LabResultsPage, meta: { title: 'Результати', access: 'admin', wide: 'table' } },
  { path: '/labs/:n/results/:vid', component: LabReviewPage, meta: { title: 'Перевірка', access: 'admin', wide: 'table' } },  // the notebook next to the key and the marks
  // a lab's pages (labPages.js): /labs/3 — its own, /labs/3/case1 — a part of it, /labs/about/grading — common to all labs.
  // `:n` without (\\d+): a pattern would outrank the plain `:n` of /labs/:n/my and /labs/:n/results above
  { path: '/labs/about/:part', component: LabPage, meta: { title: 'Лаби', access: 'active', about: true } },
  { path: '/labs/:n', component: LabPage, meta: { title: 'Лаби', access: 'active' } },
  { path: '/labs/:n/:part', component: LabPage, meta: { title: 'Лаби', access: 'active' } },
  { path: '/intake', component: IntakePage, meta: { title: 'Вхідні', access: 'admin', filters: true } },  // what the teacher forwarded to the bot (T368)
  { path: '/lessons', component: LessonsPage, meta: { title: 'Пари', access: 'active', filters: true } },
  { path: '/lessons/new', component: LessonEditPage, meta: { title: 'Нова пара', access: 'admin' } },
  { path: '/lessons/:slug', component: LessonPage, meta: { title: 'Пари', access: 'active' } },
  { path: '/lessons/:slug/edit', component: LessonEditPage, meta: { title: 'Пари', access: 'admin' } },
  { path: '/attendance', component: AttendancePage, meta: { title: 'Відвідування', access: 'admin', wide: true, filters: true } },  // students × lessons, from Zoom (T222)
  // the week is the teacher's alone for now: 'active' on both routes gives it back to students, with the menu entry
  { path: '/my/week', component: MyWeekPage, meta: { title: 'Мій тиждень', access: 'admin' } },
  { path: '/week/:day(\\d)?', component: WeekPage, meta: { title: 'Тиждень', access: 'admin', filters: true, stay: true, wide: 'admin' } },
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
