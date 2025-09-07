import { createRouter, createWebHistory } from "vue-router"
import LandingPage from "../views/landing.vue"
import AboutPage from "../views/about.vue"

const routes = [
  { path: "/", component: LandingPage },
  { path: "/about", component: AboutPage},
]

const router = createRouter({
  history: createWebHistory(),
  routes
})



export default router
