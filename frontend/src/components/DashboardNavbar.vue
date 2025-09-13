<template>
  <header class="header bg-[#88ACEA] shadow-md">
    <div class="nav-container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <!-- Left: Brand -->
        <RouterLink to="/" class="font-subtitle text-2xl text-white">HealthQuest</RouterLink>
        <!-- Right: Navigation Links -->
        <ul class="nav-links hidden md:flex items-center space-x-8">

          <li>
            <RouterLink
              to="/progress"
              class="nav-link font-body text-white hover:text-[#c7d2fe] transition-colors"
            >
              Progress
            </RouterLink>
          </li>
          <li>
            <RouterLink
              to="/workout-program"
              class="nav-link font-body text-white hover:text-[#c7d2fe] transition-colors"
            >
              Workout Program
            </RouterLink>
          </li>
          <li>
            <RouterLink
              to="/workout"
              class="nav-link font-body text-white hover:text-[#c7d2fe] transition-colors"
            >
              Workout
            </RouterLink>
          </li>
          <li>
            <RouterLink
              to="/food-recipe"
              class="nav-link font-body text-white hover:text-[#c7d2fe] transition-colors"
            >
              Food Recipe
            </RouterLink>
          </li>
          <li>
            <RouterLink
              to="/profile"
              class="nav-link font-body text-white hover:text-[#c7d2fe] transition-colors"
            >
              Profile
            </RouterLink>
          </li>
          <li>
          <span class="material-symbols-outlined text-white" @click="logout">
          logout
          </span>
          </li>
        </ul>
      </div>
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'

async function logout() {
  window.location.href = "http://127.0.0.1:8000/accounts/logout/"
}

</script>

<style scoped>
/* Active link styling */
.router-link-active {
  @apply text-[#c7d2fe];
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .nav-links {
    display: flex;
    flex-direction: column;
    position: absolute;
    top: 4rem;
    left: 0;
    width: 100%;
    background-color: #88acea;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    padding: 1rem 0;
  }

  .nav-links li {
    padding: 0.5rem 0;
    text-align: left;
  }
}
</style>
