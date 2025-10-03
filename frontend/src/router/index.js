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

import { useUserStore } from '@/stores/user'

const SKIP_IF_COMPLETE = new Set(['/select-role', '/about-you'])

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach(async (to, from, next) => {
  console.log(`Navigating from ${from.path} to ${to.path}`)

  if (!SKIP_IF_COMPLETE.has(to.path)) {
    return next()
  }

  try {
    const userStore = useUserStore()

    // ensure store initialized (init is idempotent)
    if (userStore.loading || userStore.user === null) {
      await userStore.init()
    }

    if (userStore.profile_complete) {
      console.log('Profile complete, redirecting to appropriate dashboard')
      // send coaches to coach dashboard, others to regular dashboard
      if (userStore.role === 'coach' || userStore.profile?.role === 'coach') {
        return next('/coach-dashboard')
      }
      return next('/dashboard')
    }
  } catch (err) {
    console.warn('Profile check failed, allowing navigation', err)
  }

  next()
})

router.onError((error) => {
  console.error('Router error:', error)
})

export default router