import { createRouter, createWebHistory } from 'vue-router'
import CheckIn from '@/views/CheckIn.vue'
import CheckOut from '@/views/CheckOut.vue'
import Home from '@/views/Home.vue'
import Reshelve from '@/views/Reshelve.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/checkin',
      name: 'CheckIn',
      component: CheckIn,
    },
    {
      path: '/checkout',
      name: 'CheckOut',
      component: CheckOut,
    },
    {
      path: '/reshelve',
      name: 'Reshelve',
      component: Reshelve,
    },
  ],
})

export default router
