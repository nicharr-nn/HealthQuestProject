<template>
  <CoachNavbar
    v-if="userStore.profile_complete
      && (userStore.role === 'coach' || userStore.profile?.role === 'coach')
      && (userStore.approved || userStore.profile?.approved || userStore.coach_profile?.status_approval === 'approved')"
  />
  <DashboardNavbar v-else-if="userStore.profile_complete" />
  <UnsignNavbar v-else />
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import DashboardNavbar from './DashboardNavbar.vue'
import UnsignNavbar from './UnsignNavBar.vue'
import CoachNavbar from './CoachNavbar.vue'

const userStore = useUserStore()
</script>