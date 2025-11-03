<template>
  <header class="bg-[#88ACEA] shadow-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <!-- Left: Brand -->
        <RouterLink 
          to="/" 
          class="font-subtitle text-2xl text-white hover:text-[#c7d2fe] transition-colors"
        >
          HealthQuest
        </RouterLink>

        <!-- Mobile Menu Button -->
        <button 
          @click="toggleMobileMenu"
          class="md:hidden text-white hover:text-[#c7d2fe] transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path 
              v-if="!mobileMenuOpen"
              stroke-linecap="round" 
              stroke-linejoin="round" 
              stroke-width="2" 
              d="M4 6h16M4 12h16M4 18h16"
            />
            <path 
              v-else
              stroke-linecap="round" 
              stroke-linejoin="round" 
              stroke-width="2" 
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>

        <!-- Desktop Navigation Links -->
        <ul class="hidden md:flex items-center space-x-8">
          <li>
            <RouterLink
              to="/coach-dashboard"
              class="font-body text-white hover:text-[#c7d2fe] transition-colors"
              active-class="text-[#c7d2fe]"
            >
              Dashboard
            </RouterLink>
          </li>

          <li>
            <RouterLink
              to="/view-member"
              class="font-body text-white hover:text-[#c7d2fe] transition-colors"
              active-class="text-[#c7d2fe]"
            >
              Member
            </RouterLink>
          </li>

          <!-- Clickable Food Post Dropdown -->
          <li class="relative">
            <button
              @click="toggleDropdown"
              class="font-body flex items-center px-3 py-2 rounded-md transition-colors"
              :class="showDropdown 
                ? 'bg-[#88ACEA] text-white' 
                : 'text-white hover:text-[#c7d2fe]'"
            >
              Post
              <svg
                class="w-4 h-4 ml-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                :class="showDropdown ? 'rotate-180 transition-transform' : 'transition-transform'"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>

            <transition name="fade">
              <ul
              v-if="showDropdown"
              class="absolute left-0 mt-2 w-44 bg-[#88ACEA] rounded-md shadow-lg z-50"
            >
              <li>
                <RouterLink
                  to="/food-recipe"
                  @click="closeDropdown"
                  class="block px-4 py-2 text-white hover:text-[#c7d2fe] rounded-t-md"
                >
                  Food Recipes
                </RouterLink>
              </li>
              <li>
                <RouterLink
                  to="/food-diary"
                  @click="closeDropdown"
                  class="block px-4 py-2 text-white hover:text-[#c7d2fe] rounded-t-md"
                >
                  Member Posts
                </RouterLink>
              </li>
            </ul>
            </transition>
          </li>

          <li>
            <RouterLink
              to="/coach-portal"
              class="font-body text-white hover:text-[#c7d2fe] transition-colors"
              active-class="text-[#c7d2fe]"
            >
              Profile
            </RouterLink>
          </li>

          <li>
            <button 
              @click="logout"
              class="text-white hover:text-[#c7d2fe] transition-colors cursor-pointer"
            >
              <span class="material-symbols-outlined">logout</span>
            </button>
          </li>
        </ul>
      </div>

      <!-- Mobile Navigation Menu -->
      <div 
        v-if="mobileMenuOpen"
        class="md:hidden absolute left-0 right-0 bg-[#88ACEA] shadow-lg py-4 z-50"
      >
        <ul class="flex flex-col space-y-2 px-4">
          <li>
            <RouterLink
              to="/coach-dashboard"
              @click="closeMobileMenu"
              class="block font-body text-white hover:text-[#c7d2fe] py-2"
              active-class="text-[#c7d2fe]"
            >
              Dashboard
            </RouterLink>
          </li>
          <li>
            <RouterLink
              to="/view-member"
              @click="closeMobileMenu"
              class="block font-body text-white hover:text-[#c7d2fe] py-2"
              active-class="text-[#c7d2fe]"
            >
              Member
            </RouterLink>
          </li>
          <li>
            <RouterLink
              to="/food-recipe"
              @click="closeMobileMenu"
              class="block font-body text-white hover:text-[#c7d2fe] py-2"
            >
              Recipe
            </RouterLink>
          </li>
          <li>
            <RouterLink
              to="/food-diary"
              @click="closeMobileMenu"
              class="block font-body text-white hover:text-[#c7d2fe] py-2"
            >
              Member Posts
            </RouterLink>
          </li>
          <li>
            <RouterLink
              to="/coach-portal"
              @click="closeMobileMenu"
              class="block font-body text-white hover:text-[#c7d2fe] py-2"
              active-class="text-[#c7d2fe]"
            >
              Profile
            </RouterLink>
          </li>
          <li>
            <button 
              @click="logout"
              class="flex items-center text-white hover:text-[#c7d2fe] py-2"
            >
              <span class="material-symbols-outlined">logout</span>
              <span class="ml-2">Logout</span>
            </button>
          </li>
        </ul>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const mobileMenuOpen = ref(false)
const showDropdown = ref(false)

function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

function closeMobileMenu() {
  mobileMenuOpen.value = false
}

function toggleDropdown() {
  showDropdown.value = !showDropdown.value
}

function closeDropdown() {
  showDropdown.value = false
}

async function logout() {
  window.location.href = "http://127.0.0.1:8000/accounts/logout/"
}
</script>

<style scoped>

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
