import { createRouter, createWebHistory } from 'vue-router'
import JournalPage from '../pages/JournalPage.vue'  // Импортируем реальный компонент
import ReferencePage from '../pages/ReferencePage.vue'
import TestBenchPage from '../pages/TestBenchPage.vue'
import ProfilePage from '../pages/ProfilePage.vue'
import UsersPage from '../pages/UsersPage.vue'

const routes = [
  {
    path: '/',
    redirect: '/journal'
  },
  {
    path: '/journal',
    name: 'journal',
    component: JournalPage 
  },
  {
    path: '/reference',
    name: 'reference',
    component: ReferencePage
  },
  {
    path: '/test-bench',
    name: 'test-bench',
    component: TestBenchPage
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfilePage
  },
  {
    path: '/users',
    name: 'users',
    component: UsersPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router