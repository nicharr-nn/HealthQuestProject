import { createRouter, createWebHistory } from "vue-router"
import LandingPage from "../views/landing.vue"
import AboutPage from "../views/about.vue"
import SelectRole from "../views/RoleSelection.vue"
import AboutYou from "../views/AboutYou.vue"
import Profile from "../views/Profile.vue"
import Dashboard  from "../views/Dashboard.vue"
import SelectGoal from "../views/GoalSelection.vue"
import CoachPortal from "../views/CoachPortal.vue"
import CoachDashboard from "../views/CoachDashboard.vue"
import Workout from "../views/Workout.vue"
import Program from "../views/Program.vue"

const routes = [
  { 
    path: "/", 
    name: "LandingPage",
    component: LandingPage 
  },
  { 
    path: "/about", 
    name: "AboutPage",
    component: AboutPage
  },
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
    name: "Dashboard",
    component: Dashboard 
  },
  { path: "/select-goal", 
  name: "SelectGoal",
  component: SelectGoal 
  },
  { path: "/coach-portal",
  name: "CoachPortal",
  component: CoachPortal 
  },
  { path: "/coach-dashboard",
  name: "CoachDashboard",
  component: CoachDashboard 
  },  
  {
    path: "/workout",
    name: "Workout",
    component: Workout,
  },
  { path: "/program",
  name: "Program",
  component: Program 
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach(async (to, from, next) => {
  console.log(`Navigating from ${from.path} to ${to.path}`)
  
  // Only check auth for specific routes
  if (to.path === "/select-role" || to.path === "/about-you") {
    try {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 5000)
      
      const response = await fetch("http://127.0.0.1:8000/api/user-info/", {
        credentials: "include",
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
        }
      })
      
      clearTimeout(timeoutId)
      
      if (response.ok) {
        const user = await response.json()
        console.log('User profile check:', user)
        
        if (user.profile_complete) {
          console.log('Profile complete, redirecting to dashboard')
          return next("/dashboard")
        }
      } else {
        console.warn(`Auth check failed with status: ${response.status}`)
      }
    } catch (err) {
      console.error("Auth check failed:", err.name, err.message)
      
      // Don't block navigation if it's just a network error
      if (err.name === 'AbortError') {
        console.warn('Auth check timed out, allowing navigation')
      } else if (err.name === 'TypeError') {
        console.warn('Network error during auth check, allowing navigation')
      }
    }
  }
  
  next()
})

router.onError((error) => {
  console.error('Router error:', error)
})

export default router