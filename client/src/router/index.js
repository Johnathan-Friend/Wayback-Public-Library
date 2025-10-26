import { createRouter, createWebHistory } from 'vue-router'
import CheckIn from "@/views/CheckIn.vue";
import CheckOut from "@/views/CheckOut.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: CheckOut,
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
  ],
})

export default router
