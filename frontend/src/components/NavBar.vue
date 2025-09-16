<template>
  <DashboardNavbar v-if="userStore.profile_complete" />
  <UnsignNavbar v-else />
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import DashboardNavbar from './DashboardNavbar.vue'
import UnsignNavbar from './UnsignNavBar.vue'

const userStore = useUserStore()
</script>