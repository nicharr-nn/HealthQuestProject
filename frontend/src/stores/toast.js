import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useToastStore = defineStore('toast', () => {
  const toasts = ref([])
  let toastId = 0

  const showToast = (message, type = 'success', duration = 4000) => {
    const id = toastId++
    toasts.value.push({ id, message, type })
    
    if (duration > 0) {
      setTimeout(() => removeToast(id), duration)
    }
  }

  const removeToast = (id) => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }

  const success = (message, duration) => showToast(message, 'success', duration)
  const error = (message, duration) => showToast(message, 'error', duration)
  const warning = (message, duration) => showToast(message, 'warning', duration)
  const info = (message, duration) => showToast(message, 'info', duration)

  return {
    toasts,
    showToast,
    removeToast,
    success,
    error,
    warning,
    info
  }
})