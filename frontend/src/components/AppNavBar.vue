<template>
  <nav class="bg-[#88ACEA] shadow-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <!-- Left: Brand -->
        <div class="flex items-center">
          <RouterLink to="/" class="text-2xl font-subtitle text-white hover:text-indigo-200">
            HealthQuest
          </RouterLink>
        </div>

        <!-- Right: Navigation links -->
        <div class="hidden md:flex items-center space-x-6">
          <RouterLink to="/" class="text-white hover:text-indigo-200 font-body">
            Home
          </RouterLink>

          <RouterLink to="/service" class="text-white hover:text-indigo-200 font-body">
            Service
          </RouterLink>

          <RouterLink to="/about-us" class="text-white hover:text-indigo-200 font-body">
            About us
          </RouterLink>
          
          <RouterLink to="/select-role" class="text-white hover:text-indigo-200 font-body">
            Get Started
          </RouterLink>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.router-link-active {
  @apply text-indigo-200 font-bold;
}
</style>