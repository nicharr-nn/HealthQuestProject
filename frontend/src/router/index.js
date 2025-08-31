import { createRouter, createWebHistory } from "vue-router"
import SelectRole from "../views/RoleSelection.vue"
import AboutYou from "../views/AboutYou.vue"
import Profile from "../views/Profile.vue"

const routes = [
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




// import { createRouter, createWebHistory } from "vue-router"
// import SelectRole from "../views/RoleSelection.vue"
// // import Dashboard from "../views/Dashboard.vue"
// // import Goals from "../views/GoalSelection.vue"

// const routes = [
//   {
//     path: "/select-role",
//     name: "SelectRole",
//     component: SelectRole,
//     meta: { requiresAuth: true },
//   },
//   // {
//   //   path: "/dashboard",
//   //   name: "Dashboard",
//   //   component: Dashboard,
//   //   meta: { requiresAuth: true },
//   // },
//   // {
//   //   path: "/goals",
//   //   name: "Goals",
//   //   component: Goals,
//   //   meta: { requiresAuth: true },
//   // },
// ]

// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes,
// })

// /**
//  * Simulated API call to get user info from backend
//  * In real app, replace with your Django backend endpoint
//  */
// async function getCurrentUser() {
//   try {
//     const res = await fetch("http://localhost:8000/api/user/", {
//       credentials: "include",
//     })
//     if (!res.ok) return null
//     return await res.json() // { id, email, role }
//   } catch (err) {
//     return null
//   }
// }

// // Navigation guard
// router.beforeEach(async (to, from, next) => {
//   if (!to.meta.requiresAuth) {
//     return next()
//   }

//   const user = await getCurrentUser()

//   if (!user) {
//     // user not logged in → redirect to backend login
//     window.location.href = "http://localhost:8000/accounts/google/login/"
//     return
//   }

//   if (!user.role && to.path !== "/select-role") {
//     // logged in but no role → force select-role
//     return next("/select-role")
//   }

//   return next()
// })

// export default router
