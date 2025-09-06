import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const role = ref(null)
  const userData = ref(null)
  
  const setRole = (newRole) => {
    role.value = newRole
    // Optional: Save to localStorage for persistence
    localStorage.setItem('userRole', newRole)
  }
  
  const setUserData = (data) => {
    userData.value = data
  }
  
  const clearUser = () => {
    role.value = null
    userData.value = null
    localStorage.removeItem('userRole')
  }
  
  // Initialize from localStorage if available
  const initializeFromStorage = () => {
    const savedRole = localStorage.getItem('userRole')
    if (savedRole) {
      role.value = savedRole
    }
  }
  
  return {
    role,
    userData,
    setRole,
    setUserData,
    clearUser,
    initializeFromStorage
  }
})