<template>
  <header class="header bg-[#88ACEA] shadow-md">
    <div class="nav-container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <!-- Left: Brand Logo -->
        <div class="logo font-display text-2xl text-white">
          HealthQuest
        </div>

        <!-- Right: Navigation Links -->
        <ul class="nav-links hidden md:flex items-center space-x-8">
          <li>
            <RouterLink to="/progress" class="nav-link font-subtitle text-white hover:text-indigo-200 transition-colors">
              Progress
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/workout-program" class="nav-link font-subtitle text-white hover:text-indigo-200 transition-colors">
              Workout Program
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/workout" class="nav-link font-subtitle text-white hover:text-indigo-200 transition-colors">
              Workout
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/food-recipe" class="nav-link font-subtitle text-white hover:text-indigo-200 transition-colors">
              Food Recipe
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/profile" class="nav-link font-subtitle text-white hover:text-indigo-200 transition-colors">
              Profile
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
/* Active link styling */
.nav-link.router-link-active {
  @apply text-indigo-200 font-bold underline;
}

/* Optional: Add mobile hamburger menu for smaller screens */
@media (max-width: 768px) {
  .nav-links {
    @apply flex-col absolute top-16 left-0 w-full bg-[#88ACEA] shadow-lg py-4;
  }
  
  .nav-links li {
    @apply py-2 text-center;
  }
}