<template>
  <div v-if="userStore.loading" class="min-h-screen bg-white"></div>

  <template v-else>
    <!-- Demo Navigation Helper (Remove after testing) -->
    <div style="position: fixed; top: 10px; right: 10px; z-index: 9999; background: white; padding: 10px; border: 2px solid #3b82f6; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
      <div style="font-weight: bold; margin-bottom: 8px; color: #3b82f6;">Quick Demo Links:</div>
      <div style="display: flex; flex-direction: column; gap: 4px;">
        <a href="/coach-portal" style="color: #3b82f6; text-decoration: underline; font-size: 13px;">Coach Portal</a>
        <a href="/coach-dashboard" style="color: #3b82f6; text-decoration: underline; font-size: 13px;">Coach Dashboard</a>
      </div>
    </div>

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
