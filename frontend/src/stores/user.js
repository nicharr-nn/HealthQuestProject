import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    id: null,
    isAuthenticated: false,
    profile: null,
    profile_complete: false,
    role:null,
    goal:null
  }),
  actions: {
    setAuthStatus(isAuthenticated, profile = null, profileComplete = false) {
      this.isAuthenticated = isAuthenticated
      this.profile = profile
      this.profile_complete = profileComplete
      // Set the ID from the profile
      if (profile?.id) {
        this.id = profile.id
      }
    },
    setRole(role){
      this.role = role;
    },
    setGoal(goal){
      this.goal = goal;
    },

    setProfileComplete(value) {
      this.profile_complete = value
    },

    logout() {
      this.clearAuthStatus()
      localStorage.removeItem('user-token')
      sessionStorage.removeItem('user-session')
    },

    clearAuthStatus() {
      this.isAuthenticated = false
      this.profile = null
      this.profile_complete = false
      this.role = null
      this.goal = null
    },
  },
})