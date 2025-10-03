import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/tailwind.css'
import { useUserStore } from '@/stores/user'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)

// initialize user store before mounting so NavBar sees correct coach status
const userStore = useUserStore()
userStore.init().finally(() => {
  app.mount('#app')
})