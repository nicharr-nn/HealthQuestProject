import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    isAuthenticated: false,
    profile: null,
    profile_complete: false,
  }),
  actions: {
    setAuthStatus(isAuthenticated, profile = null, profileComplete = false) {
      this.isAuthenticated = isAuthenticated
      this.profile = profile
      this.profile_complete = profileComplete
    },
    setProfileComplete(value) {
      this.profile_complete = value
    },
    clearAuthStatus() {
      this.isAuthenticated = false
      this.profile = null
      this.profile_complete = false
    },
  },
})