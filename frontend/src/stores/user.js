import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    id: null,
    isAuthenticated: false,
    user: null,
    profile: null,
    profile_complete: false,
    role: null,
    goal: null,
    loading: true,
  }),

  getters: {
  displayName(state) {
    const p = state.profile
    const u = state.user
    const first = p?.first_name ?? u?.first_name
    const last = p?.last_name ?? u?.last_name
    const full = [first, last].filter(Boolean).join(' ').trim()
    if (full) return full
    if (p?.name || u?.name) return p?.name || u?.name
    if (p?.username || u?.username) return p?.username || u?.username
    if (u?.email) return u.email.split('@')[0]
    return 'Guest'
  },

  profilePicture(state) {
    const p = state.profile
    const u = state.user
    const path = p?.photo || p?.avatar || p?.picture || u?.photo || u?.avatar || u?.picture || null
    return path && path.startsWith('/') ? `http://127.0.0.1:8000${path}` : path
  }
},


  actions: {
    async init() {
      this.loading = true
      try {
        const res = await fetch('http://127.0.0.1:8000/api/user-info/', {
          credentials: 'include',
          headers: { Accept: 'application/json' },
        })

        if (res.ok) {
          const data = await res.json()

          this.isAuthenticated = data.isAuthenticated
          this.user = data.user || null
          this.profile_complete = data.user?.profile_complete === true
          this.profile = data.user?.profile || null
          this.role = data.user?.profile?.role || null
          this.level = data.profile?.current_level || { level_rank: 1, level: 'Bronze', xp: 0 }
        } else {
          this.clearAuthStatus()
        }
      } catch (err) {
        console.error('Failed to fetch user info:', err)
        this.clearAuthStatus()
      } finally {
        this.loading = false
      }
    },

    async logout() {
      try {
        await fetch('http://127.0.0.1:8000/accounts/logout/', {
          credentials: 'include',
        })
      } catch (err) {
        console.error('Logout failed:', err)
      } finally {
        this.clearAuthStatus()
        window.location.href = '/'
      }
    },

    setRole(role) {
      this.role = role
      if (this.profile) this.profile.role = role
    },

    setGoal(goal) {
      this.goal = goal
    },

    setProfileComplete(value) {
      this.profile_complete = value
    },

    clearAuthStatus() {
      this.isAuthenticated = false
      this.user = null
      this.profile = null
      this.profile_complete = false
      this.role = null
      this.goal = null
    },
    
  },
  
})

