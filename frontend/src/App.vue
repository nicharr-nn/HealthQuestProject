<template>
  <main class="min-h-screen bg-paper">
    <Navbar />
    <router-view />
  </main>
</template>

<script setup>
import Navbar from "./components/Navbar.vue"
</script>
