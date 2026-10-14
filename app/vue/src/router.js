import ActivityPage from '@core/pages/ActivityPage.vue'
import AttendancePage from '@core/pages/AttendancePage.vue'
import GuidePage from '@core/pages/GuidePage.vue'
import HistoryPage from '@core/pages/HistoryPage.vue'
import LessonEditPage from '@core/pages/LessonEditPage.vue'
import LessonPage from '@core/pages/LessonPage.vue'
import LessonsPage from '@core/pages/LessonsPage.vue'
import LoginPage from '@core/pages/LoginPage.vue'
import MethodPage from '@core/pages/MethodPage.vue'
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
import WeekPage from '@core/pages/WeekPage.vue'
import { makeRouter } from '@core/router.js'

import CardHistoryPage from './pages/CardHistoryPage.vue'
import Colors2Page from './pages/Colors2Page.vue'
import ColorsPage from './pages/ColorsPage.vue'
import GameEditPage from './pages/GameEditPage.vue'
import GamePage from './pages/GamePage.vue'
import GamesPage from './pages/GamesPage.vue'
import HomePage from './pages/HomePage.vue'
import MyGamePage from './pages/MyGamePage.vue'
import RefsPage from './pages/RefsPage.vue'
import StudentGamePage from './pages/StudentGamePage.vue'
import TaskEditPage from './pages/TaskEditPage.vue'
import TasksPage from './pages/TasksPage.vue'
import { CHANGES, SECTIONS } from './site.js'

export default makeRouter([
  { path: '/', component: HomePage },
  ...[...SECTIONS, CHANGES].filter((s) => s.page).map((s) => ({ path: s.path, component: GuidePage, meta: { title: s.nav, slug: s.slug } })),  // the guide is open to all, a guest too (T214)
  { path: '/labs/:n', component: GuidePage, meta: { title: 'Лаби' } },
  { path: '/method', component: MethodPage, meta: { title: 'Методичка' } },
  { path: '/method/history', component: HistoryPage, meta: { title: 'Історія правок', access: 'admin' } },
  { path: '/login', component: LoginPage, meta: { title: 'Вхід' } },
  { path: '/my/profile', component: ProfilePage, meta: { title: 'Профіль', access: 'active' } },
  { path: '/profile', redirect: '/my/profile' },  // old links in bot messages and the guide
  { path: '/my/game', component: MyGamePage, meta: { title: 'Моя гра', access: 'active' } },  // a student picks their game here; its insides stay the admin's for now (T216)
  { path: '/my/week', component: MyWeekPage, meta: { title: 'Мій тиждень', access: 'active' } },
  // meetings with their transcripts: signed-in students read what is published (T218)
  { path: '/lessons', component: LessonsPage, meta: { title: 'Заняття', access: 'active', filters: true } },
  { path: '/lessons/new', component: LessonEditPage, meta: { title: 'Нове заняття', access: 'admin' } },
  { path: '/lessons/:slug', component: LessonPage, meta: { title: 'Заняття', access: 'active' } },
  { path: '/lessons/:slug/edit', component: LessonEditPage, meta: { title: 'Заняття', access: 'admin' } },
  { path: '/attendance', component: AttendancePage, meta: { title: 'Відвідування', access: 'admin', wide: true, filters: true } },  // students × lessons, from Zoom (T222)
  // a student's own week; the teacher's summary on the whole window, /week/3 — one day of it (T186)
  { path: '/week/:day(\\d)?', component: WeekPage, meta: { title: 'Тиждень', access: 'active', filters: true, stay: true, wide: 'admin' } },
  // a student sees the slice of these two the API gives them: «Ігри студентів» (site.js students.asStudent)
  { path: '/students', component: StudentsPage, meta: { title: 'Студенти', access: 'active' } },
  { path: '/students/:nick', component: StudentGamePage, meta: { title: 'Студенти', access: 'active' } },
  { path: '/students/:nick/edit', component: StudentEditPage, meta: { title: 'Студенти', access: 'admin' } },
  { path: '/activity', component: ActivityPage, meta: { title: 'Активність', access: 'admin', filters: true } },
  { path: '/polls', component: PollsPage, meta: { title: 'Опитування', access: 'admin', filters: true } },
  { path: '/polls/new', component: PollEditPage, meta: { title: 'Нове опитування', access: 'admin' } },
  { path: '/polls/templates', component: PollTemplatesPage, meta: { title: 'Шаблони опитувань', access: 'admin' } },
  { path: '/polls/matrix', component: PollMatrixPage, meta: { title: 'Хто як відповідав', access: 'admin', wide: true, filters: true } },
  { path: '/polls/:id', component: PollPage, meta: { title: 'Опитування', access: 'admin' } },
  { path: '/polls/:id/edit', component: PollEditPage, meta: { title: 'Опитування', access: 'admin' } },
  { path: '/ideas', component: RefsPage, meta: { title: 'Знахідки', access: 'active' } },  // students too, not guests (T214)
  { path: '/refs', redirect: '/ideas' },
  { path: '/games', component: GamesPage, meta: { title: 'Ігри' } },
  { path: '/games/history', component: CardHistoryPage, meta: { title: 'Історія ігор', kind: 'games', access: 'admin' } },
  { path: '/games/new', component: GameEditPage, meta: { title: 'Нова гра', access: 'admin' } },
  { path: '/games/:slug', component: GamePage, meta: { title: 'Ігри', filters: true } },
  { path: '/games/:slug/edit', component: GameEditPage, meta: { title: 'Ігри', access: 'admin' } },
  { path: '/colors', component: ColorsPage, meta: { title: 'Кольори', access: 'admin' } },
  { path: '/colors2', component: Colors2Page, meta: { title: 'Кольори v2', access: 'admin' } },
  { path: '/tasks', component: TasksPage, meta: { title: 'Таски', wide: true, filters: true } },
  { path: '/tasks/history', component: CardHistoryPage, meta: { title: 'Історія завдань', kind: 'tasks', access: 'admin' } },
  { path: '/tasks/new', component: TaskEditPage, meta: { title: 'Нове завдання', access: 'admin' } },
  { path: '/tasks/:slug/edit', component: TaskEditPage, meta: { title: 'Таски', access: 'admin' } },
  { path: '/:pathMatch(.*)*', component: NotFoundPage, meta: { title: 'Такої сторінки нема' } },  // the server answers any path with index.html, so 404 is ours to show
])
