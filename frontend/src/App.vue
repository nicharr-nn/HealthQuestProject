<template>
  <div v-if="userStore.loading" class="min-h-screen bg-white"></div>

  <template v-else>
    <CoachNavbar
      v-if="userStore.profile_complete
        && (userStore.role === 'coach' || userStore.profile?.role === 'coach')"
    />
    <DashboardNavbar v-else-if="userStore.profile_complete" />
    <UnsignNavbar v-else />
    <RouterView />
  </template>
</template>

<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import DashboardNavbar from '@/components/DashboardNavbar.vue'
import UnsignNavbar from '@/components/UnsignNavBar.vue'
import CoachNavbar from '@/components/CoachNavBar.vue'

const userStore = useUserStore()

onMounted(() => {
  userStore.init()
})
</script>
