import { createRouter, createWebHistory } from "vue-router"
import LandingPage from "../views/landing.vue"
import AboutPage from "../views/about.vue"
import SelectRole from "../views/RoleSelection.vue"
import AboutYou from "../views/AboutYou.vue"
import Profile from "../views/Profile.vue"
import DashBoard  from "../views/DashBoard.vue"
import SelectGoal from "../views/GoalSelection.vue"
import CoachPortal from "../views/CoachPortal.vue"

const routes = [
  { path: "/", 
    name: "LandingPage",
    component: LandingPage },

  { path: "/about", 
    name: "AboutPage",
    component: AboutPage},
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
  { path: "/dashboard", 
    name: "DashBoard",
    component: DashBoard 
  },
  { path: "/select-goal", 
  name: "SelectGoal",
  component: SelectGoal 
  },
  { path: "/coach-portal",
  name: "CoachPortal",
  component: CoachPortal 
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach(async (to, from, next) => {
  if (to.path === "/select-role" || to.path === "/about-you") {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/user-info/", {
        credentials: "include"
      })
      if (response.ok) {
        const user = await response.json()

        if (user.profile_complete) {
          return next("/dashboard")
        }
      }
    } catch (err) {
      console.error("Auth check failed:", err)
    }
  }
  next()
})

export default router