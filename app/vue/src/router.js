import { createRouter, createWebHistory } from 'vue-router'

import HomePage from './pages/HomePage.vue'
import ProfilePage from './pages/ProfilePage.vue'
import StudentEditPage from './pages/StudentEditPage.vue'
import StudentsPage from './pages/StudentsPage.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomePage },
    { path: '/profile', component: ProfilePage },
    { path: '/students', component: StudentsPage },
    { path: '/students/:id', component: StudentEditPage },
  ],
})
