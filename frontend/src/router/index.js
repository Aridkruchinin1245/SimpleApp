import { createRouter, createWebHistory } from 'vue-router'

import MainPage from '@/components/MainPage.vue'
import PostCreating from '@/components/PostCreating.vue'
import AuthorsPage from '@/components/AuthorsPage.vue'
import CommentsPage from '@/components/CommentsPage.vue'
import RegistrationPage from '@/components/RegistrationPage.vue'
import AuthPage from '@/components/AuthPage.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: MainPage
  },
  {
    path: '/postCreate',
    name: 'post creating',
    component: PostCreating
  },
  {
    path: '/authors',
    name : 'authors list',
    component : AuthorsPage
  },
  {
    path: '/comments/:id',
    name: 'comments list',
    props: true,
    component: CommentsPage
  },
  {
    path: '/reg',
    name : 'registration',
    component : RegistrationPage
  },
  {
    path: '/auth',
    name : 'authentication',
    component : AuthPage
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
