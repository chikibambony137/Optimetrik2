import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../pages/MainPage.vue' // Импортируем layout с меню
import JournalPage from '../pages/JournalPage.vue'
import ReferencePage from '../pages/ReferencePage.vue'
import TestToolPage from '../pages/TestToolPage.vue'
import ProfilePage from '../pages/ProfilePage.vue'
import UsersPage from '../pages/UsersPage.vue'
import Authorization from '../pages/Authorization.vue'
import Registration from '../pages/Registration.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'login',
    component: Authorization
  },
  {
    path: '/registration',
    name: 'registration',
    component: Registration
  },
  {
    path: '/main',
    component: MainPage, // Layout с меню
    children: [
      {
        path: 'journal',
        name: 'journal',
        component: JournalPage
      },
      {
        path: 'reference',
        name: 'reference',
        component: ReferencePage
      },
      {
        path: 'test-tool',
        name: 'test-tool',
        component: TestToolPage
      },
      {
        path: 'profile',
        name: 'profile',
        component: ProfilePage
      },
      {
        path: 'users',
        name: 'users',
        component: UsersPage
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router