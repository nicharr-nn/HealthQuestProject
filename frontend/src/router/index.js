import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const LandingPage = () => import('../views/landing.vue')
const AboutPage = () => import('../views/about.vue')
const SelectRole = () => import('../views/RoleSelection.vue')
const AboutYou = () => import('../views/AboutYou.vue')
const Profile = () => import('../views/Profile.vue')
const Dashboard = () => import('../views/Dashboard.vue')
const SelectGoal = () => import('../views/GoalSelection.vue')
const CoachPortal = () => import('../views/CoachPortal.vue')
const CoachDashboard = () => import('../views/CoachDashboard.vue')
const Workout = () => import('../views/Workout.vue')
const Program = () => import('../views/Program.vue')
const MemberConnect = () => import('../views/MemberConnect.vue')
const FoodRecipe = () => import('../views/FoodRecipe.vue')

const routes = [
  { path: '/', name: 'LandingPage', component: LandingPage },
  { path: '/about', name: 'AboutPage', component: AboutPage },
  { path: '/select-role', name: 'SelectRole', component: SelectRole },
  { path: '/about-you', name: 'AboutYou', component: AboutYou },
  { path: '/profile', name: 'Profile', component: Profile },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/select-goal', name: 'SelectGoal', component: SelectGoal },
  { path: '/coach-portal', name: 'CoachPortal', component: CoachPortal },
  { path: '/coach-dashboard', name: 'CoachDashboard', component: CoachDashboard },
  { path: '/workout', name: 'Workout', component: Workout },
  {
    path: '/workout/:id',
    name: 'Program',
    component: Program,
    props: true,
  },
  {
    path: '/coach',
    name: 'MemberConnect',
    component: MemberConnect,
    props: true,
  },
  {
    path: '/food-recipe',
    name: 'FoodRecipe',
    component: FoodRecipe,
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

const SKIP_IF_COMPLETE = new Set(['/select-role', '/about-you'])

router.beforeEach(async (to, from, next) => {
  console.log(`Navigating from ${from.path} to ${to.path}`)

  // Only run profile check for onboarding routes
  if (!SKIP_IF_COMPLETE.has(to.path)) return next()

  try {
    const userStore = useUserStore()

    // Ensure store is loaded (idempotent)
    if (userStore.loading || userStore.user === null) {
      // Timeout wrapper (prevent hanging)
      const controller = new AbortController()
      const timeout = setTimeout(() => controller.abort(), 5000)

      await userStore.init()
      clearTimeout(timeout)
    }

    // Redirect based on completion + role
    if (userStore.profile_complete) {
      console.log('Profile complete, redirecting to dashboard')

      if (userStore.role === 'coach' || userStore.profile?.role === 'coach') {
        return next('/coach-dashboard')
      }
      return next('/dashboard')
    }
  } catch (err) {
    if (err.name === 'AbortError') {
      console.warn('Auth check timed out, allowing navigation')
    } else {
      console.warn('Profile check failed, allowing navigation', err)
    }
  }

  next()
})

// Global router error handler
router.onError((error) => {
  console.error('Router error:', error)
})

export default router