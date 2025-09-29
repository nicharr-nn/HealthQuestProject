<template>
  <div v-if="userStore.loading" class="min-h-screen bg-white"></div>

  <template v-else>
    <DashboardNavbar v-if="userStore.profile_complete" />
    <UnsignNavbar v-else />
    <RouterView />
  </template>
</template>

<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import DashboardNavbar from '@/components/DashboardNavbar.vue'
import UnsignNavbar from '@/components/UnsignNavBar.vue'

const userStore = useUserStore()

onMounted(() => {
  userStore.init()
})
</script>
