import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { watch } from 'vue'

const LandingPage = () => import('../views/LandingPage.vue')
const AboutPage = () => import('../views/AboutPage.vue')
const SelectRole = () => import('../views/RoleSelection.vue')
const AboutYou = () => import('../views/AboutYou.vue')
const Profile = () => import('../views/UserProfile.vue')
const Dashboard = () => import('../views/Dashboard.vue')
const SelectGoal = () => import('../views/GoalSelection.vue')
const CoachPortal = () => import('../views/CoachPortal.vue')
const CoachDashboard = () => import('../views/CoachDashboard.vue')
const Workout = () => import('../views/WorkoutPage.vue')
const Program = () => import('../views/WorkoutProgram.vue')
const MemberManagement = () => import('../views/MemberManagement.vue')
const MemberRequests = () => import('../views/MemberRequests.vue')
const CreateWorkoutProgram = () => import('../views/CreateWorkoutProgram.vue')
const MemberConnect = () => import('../views/MemberConnect.vue')
const FoodRecipe = () => import('../views/FoodRecipe.vue')
const FoodPost = () => import('../views/FoodPost.vue')
const FoodDiary = () => import('../views/FoodDiary.vue')
const AdminDashboard = () => import('../views/AdminDashboard.vue')

const routes = [
  { path: '/', name: 'LandingPage', component: LandingPage },
  { path: '/about', name: 'AboutPage', component: AboutPage },
  { path: '/select-role', name: 'SelectRole', component: SelectRole },
  { path: '/about-you', name: 'AboutYou', component: AboutYou },
  { path: '/profile', name: 'Profile', component: Profile },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/select-goal', name: 'SelectGoal', component: SelectGoal },
  { path: '/coach-portal', name: 'CoachPortal', component: CoachPortal },
  { path: '/coach-dashboard', name: 'CoachDashboard', component: CoachDashboard, meta: { requiresCoach: true } },
  { path: '/admin', name: 'AdminDashboard', component: AdminDashboard, meta: { requiresAdmin: true } },
  { path: '/workout', name: 'Workout', component: Workout },
  { path: '/workout/:id', name: 'Program', component: Program, props: true },
  { path: '/view-member', name: 'ViewMember', component: MemberManagement, meta: { requiresCoach: true } },
  { path: '/view-request', name: 'ViewRequest', component: MemberRequests, meta: { requiresCoach: true } },
  { path: '/create-workout-program', name: 'CreateWorkoutProgram', component: CreateWorkoutProgram, meta: { requiresCoach: true } },
  { path: '/coach', name: 'MemberConnect', component: MemberConnect, props: true, },
  { path: '/food-recipe', name: 'FoodRecipe', component: FoodRecipe, props: true, },
  { path: '/food-post', name: 'FoodPost', component: FoodPost, props: true, },
  { path: '/food-diary', name: 'MyFoodDiary', component: FoodDiary},
  { path: '/food-diary/:memberId', name: 'FoodDiary', component: FoodDiary, props: true, meta: { requiresCoach: true } },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

const SKIP_IF_COMPLETE = new Set(['/select-role', '/about-you'])

router.beforeEach(async (to, from, next) => {
  console.log(`Navigating from ${from.path} to ${to.path}`)

  const userStore = useUserStore()

  // Initialize user if not yet loaded
  if (!userStore.user && !userStore.loading) {
    await userStore.init()
  }

  // Wait if init is still loading
  if (userStore.loading) {
    await new Promise(resolve => {
      const unwatch = watch(
        () => userStore.loading,
        (val) => {
          if (!val) {
            unwatch()
            resolve()
          }
        }
      )
    })
  }

  const isCoach = userStore.role === 'coach' || userStore.profile?.role === 'coach'
  const isAdmin = userStore.role === 'admin' || userStore.profile?.role === 'admin'
  const isApproved = userStore.approved === true
  const profileComplete = userStore.profile_complete

  console.log('After init:', { isCoach, isAdmin, isApproved, profileComplete })

  // Onboarding redirect
  if (SKIP_IF_COMPLETE.has(to.path) && profileComplete) {
    if (isAdmin) return next('/admin')
    if (isCoach && isApproved) return next('/coach-dashboard')
    if (isCoach && !isApproved) return next('/coach-portal')
    return next('/dashboard')
  }

  // Admin-only pages
  if (to.meta.requiresAdmin) {
    if (!isAdmin) {
      console.warn('Not an admin — redirecting to dashboard')
      return next('/dashboard')
    }
  }

  // Coach-only pages
  if (to.meta.requiresCoach) {
    if (!isCoach) {
      console.warn('Not a coach — redirecting to dashboard')
      return next('/dashboard')
    }
    if (!isApproved) {
      console.warn('Coach not approved — redirecting to coach portal')
      return next('/coach-portal')
    }
  }

  next()
})

// Global router error handler
router.onError((error) => {
  console.error('Router error:', error)
})

export default router
