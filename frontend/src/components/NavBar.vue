<template>
  <DashboardNavbar v-if="userStore.profile_complete" />
  <AppNavbar v-else />
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import DashboardNavbar from './DashboardNavbar.vue'
import AppNavbar from './AppNavbar.vue'

const userStore = useUserStore()
</script>