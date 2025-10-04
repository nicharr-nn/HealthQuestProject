import { createRouter, createWebHistory } from "vue-router"

const LandingPage = () => import("../views/landing.vue")
const AboutPage = () => import("../views/about.vue")
const SelectRole = () => import("../views/RoleSelection.vue")
const AboutYou = () => import("../views/AboutYou.vue")
const Profile = () => import("../views/Profile.vue")
const DashBoard = () => import("../views/Dashboard.vue")
const SelectGoal = () => import("../views/GoalSelection.vue")
const Workout = () => import("../views/Workout.vue")
const Program = () => import("../views/Program.vue")


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
  { 
    path: "/dashboard", 
    name: "DashBoard",
    component: DashBoard 
  },
  { 
    path: "/select-goal", 
    name: "SelectGoal",
    component: SelectGoal 
  },
 { 
  path: "/workout", 
  name: "Workout",
  component: Workout 
},
{
  path: '/workout/:id',  // ✅ Changed from /programs/:id to /workout/:id
  name: 'Program',
  component: Program,
  props: true
},
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// Enhanced navigation guard with better error handling
router.beforeEach(async (to, from, next) => {
  console.log(`Navigating from ${from.path} to ${to.path}`)
  
  // Only check auth for specific routes
  if (to.path === "/select-role" || to.path === "/about-you") {
    try {
      // Add timeout to prevent hanging requests
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 5000) // 5 second timeout
      
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

// Global error handler for router
router.onError((error) => {
  console.error('Router error:', error)
})

export default router