<template>
  <nav class="sticky top-0 z-50 bg-[#88ACEA] text-white shadow-lg">
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex justify-between items-center h-16">
        <!-- Left: Brand -->
        <div class="flex items-center">
          <RouterLink to="/" class="font-subtitle text-2xl text-white">HealthQuest</RouterLink>
        </div>

        <div class="hidden md:flex space-x-4 scroll-behavior-smooth">
          <a @click.prevent="scrollToSection('home')" class="hover:bg-[#F3C6C1] px-3 py-2 rounded font-body cursor-pointer">Home</a>
          <a @click.prevent="scrollToSection('about')" class="hover:bg-[#F3C6C1] px-3 py-2 rounded font-body cursor-pointer">About</a>
          <a @click.prevent="scrollToSection('contact')" class="hover:bg-[#F3C6C1] px-3 py-2 rounded font-body cursor-pointer">Contact</a>
        </div>

        <button
          class="md:hidden flex items-center focus:outline-none"
          @click="isOpen = !isOpen"
        >
          <svg
            class="h-6 w-6"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              v-if="!isOpen"
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
      </div>
    </div>

    <div
      v-if="isOpen"
      class="md:hidden bg-[#88ACEA] px-4 pb-3 space-y-2"
    >
      <a @click="scrollToSection('home')" class="block hover:bg-[#F3C6C1] px-3 py-2 rounded font-body cursor-pointer">Home</a>
      <a @click="scrollToSection('about')" class="block hover:bg-[#F3C6C1] px-3 py-2 rounded font-body cursor-pointer">About</a>
      <a @click="scrollToSection('contact')" class="block hover:bg-[#F3C6C1] px-3 py-2 rounded font-body cursor-pointer">Contact</a>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

const isOpen = ref(false)

const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    })
    isOpen.value = false
  }
}
</script>