<template>
  <div id="home" class="grid grid-rows-[auto_1fr] h-screen">
    <nav class="sticky top-0 z-50 bg-[#88ACEA] text-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <span class="text-xl font-bold">HealthQuest</span>
          </div>

          <div class="hidden md:flex space-x-4">
            <a href="#home" class="hover:bg-red-500 px-3 py-2 rounded">Home</a>
            <a href="#about" class="hover:bg-red-500 px-3 py-2 rounded">About</a>
            <a href="#contract" class="hover:bg-red-500 px-3 py-2 rounded">Contact</a>
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
        <a href="#home" class="block hover:bg-red-500 px-3 py-2 rounded">Home</a>
        <a href="#about" class="block hover:bg-red-500 px-3 py-2 rounded">About</a>
        <a href="#contract" class="block hover:bg-red-500 px-3 py-2 rounded">Contact</a>
      </div>
    </nav>

    <div class="grid grid-cols-1 md:grid-cols-2">
      <div class="bg-[url(src/images/left_box.png)] bg-cover bg-center min-h-[200px] md:min-h-full"></div>
      <div class="bg-[#FAF4E6] text-[#846757] font-bold pl-6 md:pl-10 flex flex-col justify-center">
        <p class="font-display text-5xl md:text-[100px] leading-tight">Health <br>Quest</p>
        <p class="text-base md:text-[20px] mt-4">
          Staying motivated is hard. HealthQuest makes <br class="hidden md:block">
          it easy with a structured, gamified journey that <br class="hidden md:block">
          rewards you for every healthy choice, big or small.
        </p>
        <button
          class="mt-6 bg-[#E99D7D] hover:bg-orange-500 text-[#A75B3A] text-lg md:text-[30px]
          h-[80px] w-[400px] rounded-[50%] border-2 border-[#A75B3A]"
          @click="redirectToGoogle"
        >
          Get Started
        </button>
      </div>
    </div>
  </div>

  <div id="about" class="bg-[#E99D7D] p-4"></div>
  
  <div class="bg-[#A75B3A] p-6 md:p-8">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row gap-6">
      <div class="bg-[#FAF4E6] rounded-lg p-6 flex-1">
        <h3 class="text-[#846757] font-bold text-2xl mb-4 border-b-2">About</h3>
        <p class="text-[#846757]">
          HealthQuest is a fitness platform that combines structured workouts, 
          nutrition tracking, and gamified progression. Users earn XP, set goals, 
          and unlock new features. With personalized coaching and private recipe sharing, 
          it fosters long-term healthy habits in a supportive community.
        </p>
      </div>
      <div class="bg-[#FAF4E6] rounded-lg p-6 flex-1">
        <h3 class="text-[#846757] font-bold text-2xl mb-4 border-b-2">Gamified Experience</h3>
        <ul class="list-disc list-inside text-[#846757]">
          <li>Level up your character</li>
          <li>Complete epic quests</li>
          <li>Earn achievements for every healthy choice you make</li>
        </ul>
      </div>
    </div>
  </div>

  <div id="contract" class="bg-[#FAF4E6] p-6 md:p-8">
    <h2 class="text-xl md:text-2xl font-bold">Contact Us</h2>
    <div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isOpen = ref(false)

const redirectToGoogle = () => {
  window.location.href = "http://127.0.0.1:8000/accounts/google/login/"
}
</script>
