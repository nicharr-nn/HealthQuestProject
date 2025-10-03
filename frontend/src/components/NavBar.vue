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
import { onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import DashboardNavbar from './DashboardNavbar.vue'
import UnsignNavbar from './UnsignNavBar.vue'
import CoachNavbar from './CoachNavbar.vue'

const userStore = useUserStore()

// Run only after mount and store init
onMounted(async () => {
  await userStore.init()  // make sure you wrote an async init() in the store
  console.log('Profile complete?', userStore.profile_complete)
})

// Or watch for changes
watch(
  () => userStore.profile_complete,
  (newVal) => {
    console.log('Profile complete changed to:', newVal)
  }
)
</script>
