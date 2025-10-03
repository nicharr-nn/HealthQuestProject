<template>
  <div v-if="userStore.loading" class="min-h-screen bg-white"></div>

  <template v-else>
    <DashboardNavbar v-if="userStore.profile_complete" />
    <UnsignNavbar v-else />
    <RouterView />
  </template>
</template>

<script setup>
import Navbar from "./components/NavBar.vue"
</script>
