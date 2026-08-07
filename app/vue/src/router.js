import { createRouter, createWebHistory } from 'vue-router'

import Colors2Page from './pages/Colors2Page.vue'
import ColorsPage from './pages/ColorsPage.vue'
import GameEditPage from './pages/GameEditPage.vue'
import GamePage from './pages/GamePage.vue'
import GamesPage from './pages/GamesPage.vue'
import HomePage from './pages/HomePage.vue'
import ProfilePage from './pages/ProfilePage.vue'
import StudentEditPage from './pages/StudentEditPage.vue'
import StudentsPage from './pages/StudentsPage.vue'
import TaskEditPage from './pages/TaskEditPage.vue'
import TasksPage from './pages/TasksPage.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomePage },
    { path: '/profile', component: ProfilePage },
    { path: '/students', component: StudentsPage },
    { path: '/students/:id', component: StudentEditPage },
    { path: '/games', component: GamesPage },
    { path: '/games/new', component: GameEditPage },
    { path: '/games/:slug', component: GamePage, meta: { wide: true } },
    { path: '/colors', component: ColorsPage },
    { path: '/colors2', component: Colors2Page },
    { path: '/games/:slug/edit', component: GameEditPage },
    { path: '/tasks', component: TasksPage, meta: { wide: true } },
    { path: '/tasks/new', component: TaskEditPage },
    { path: '/tasks/:slug/edit', component: TaskEditPage },
  ],
})
