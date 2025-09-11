import { createRouter, createWebHistory } from "vue-router"
import LandingPage from "../views/landing.vue"
import AboutPage from "../views/about.vue"
import SelectRole from "../views/RoleSelection.vue"
import AboutYou from "../views/AboutYou.vue"
import Profile from "../views/Profile.vue"

const routes = [
  { path: "/", component: LandingPage },
  { path: "/about", component: AboutPage},
  {
    path: "/select-role",
    name: "SelectRole",
    component: SelectRole,
  },
  {
    path: "/about-you",
    name: "AboutYou",
    component: AboutYou,
  },
    {
    path: "/profile",
    name: "Profile",
    component: Profile,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
