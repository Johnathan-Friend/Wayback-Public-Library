import { createRouter, createWebHistory } from 'vue-router'
import CheckIn from "@/views/CheckIn.vue";
import CheckOut from "@/views/CheckOut.vue";
import Home from "@/views/Home.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/checkin/:branchID',
      name: 'CheckIn',
      component: CheckIn,
      props: true
    },
    {
      path: '/checkout/:branchID',
      name: 'CheckOut',
      component: CheckOut,
      props: true
    },
  ],
})

export default router
