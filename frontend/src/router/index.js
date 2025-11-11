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
const CertificationManagement = () => import('../views/admin/CertificationManagement.vue')
const RecipeManagement = () => import('../views/admin/RecipeManagement.vue')
const WorkoutManagement = () => import('../views/admin/WorkoutManagement.vue')
const UserManagement = () => import('../views/admin/UserManagement.vue')
const AdminDashboard = () => import('../views/admin/AdminDashboard.vue')

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
  { path: '/workout', name: 'Workout', component: Workout },
  { path: '/workout/:id', name: 'Program', component: Program, props: true },
  { path: '/view-member', name: 'ViewMember', component: MemberManagement, meta: { requiresCoach: true } },
  { path: '/view-request', name: 'ViewRequest', component: MemberRequests, meta: { requiresCoach: true } },
  { path: '/create-workout-program', name: 'CreateWorkoutProgram', component: CreateWorkoutProgram, meta: { requiresCoach: true } },
  { path: '/coach', name: 'MemberConnect', component: MemberConnect, props: true },
  { path: '/food-recipe', name: 'FoodRecipe', component: FoodRecipe, props: true },
  { path: '/food-post', name: 'FoodPost', component: FoodPost, props: true },
  { path: '/food-diary', name: 'MyFoodDiary', component: FoodDiary },
  { path: '/food-diary/:memberId', name: 'FoodDiary', component: FoodDiary, props: true, meta: { requiresCoach: true } },
  { path: '/admin-certification', name: 'CertificationManagement', component: CertificationManagement, meta: { requiresAdmin: true } },
  { path: '/admin-recipe', name: 'RecipeManagement', component: RecipeManagement, meta: { requiresAdmin: true } },
  { path: '/admin-workout', name: 'WorkoutManagement', component: WorkoutManagement, meta: { requiresAdmin: true } },
  { path: '/admin-user', name: 'UserManagement', component: UserManagement, meta: { requiresAdmin: true } },
  { path: '/admin', name: 'AdminDashboard', component: AdminDashboard, meta: { requiresAdmin: true } },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()

  // --- Load user info if not already ---
  if (!userStore.user && !userStore.loading) {
    await userStore.init()
  }

  if (userStore.loading) {
    await new Promise((resolve) => {
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

  const isAdmin = userStore.isAdmin
  const isCoach = userStore.role === 'coach' || userStore.profile?.role === 'coach'
  const isApproved = userStore.approved === true
  const profileComplete = userStore.profile_complete

  // --- Redirect admin users away from onboarding pages ---
  if (isAdmin && ['/select-role', '/about-you'].includes(to.path)) {
    return next('/admin')
  }

  // --- Redirect approved coaches away from onboarding pages ---
  if (isCoach && profileComplete && ['/select-role', '/about-you'].includes(to.path)) {
    if (isApproved) return next('/coach-dashboard')
    return next('/coach-portal')
  }

  // --- Redirect regular users away from onboarding pages if profile complete ---
  if (profileComplete && ['/select-role', '/about-you'].includes(to.path)) {
    return next('/dashboard')
  }

  // --- Admin-only pages ---
  if (to.meta.requiresAdmin && !isAdmin) {
    return next('/dashboard')
  }
  

  // --- Coach-only pages ---
  if (to.meta.requiresCoach) {
    if (!isCoach) return next('/dashboard')
    if (!isApproved) return next('/coach-portal')
  }

  // --- Default: allow access ---
  next()
})

export default router
