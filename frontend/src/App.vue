<template>
  <Toast />
  <div v-if="userStore.loading" class="min-h-screen bg-white"></div>

  <template v-else>
    <template v-if="showNavbar">
      <CoachNavbar
        v-if="userStore.profile_complete
          && (userStore.role === 'coach' || userStore.profile?.role === 'coach')"
      />
      <SignNavbar v-else-if="userStore.profile_complete" />
      <UnsignNavbar v-else />
    </template>

    <RouterView />
  </template>
</template>


<script setup>
import { onMounted, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRoute } from 'vue-router'

import UnsignNavbar from '@/components/UnsignNavBar.vue'
import CoachNavbar from '@/components/CoachNavBar.vue'
import SignNavbar from './components/SignNavbar.vue'
import Toast from '@/components/Toast.vue'

const userStore = useUserStore()
const route = useRoute()

onMounted(() => {
  userStore.init()
})

// Check if user is on admin page
const showNavbar = computed(() => route.name !== 'AdminDashboard')
</script>