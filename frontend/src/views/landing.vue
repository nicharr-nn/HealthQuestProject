<template>
  <div class="grid grid-rows-[auto_1fr] h-screen">
    <!-- Navbar -->
    <nav class="bg-[#88ACEA] text-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <span class="text-xl font-bold">HealthQuest</span>
          </div>
          <div class="flex space-x-4">
            <a href="#" class="hover:bg-red-500 px-3 py-2 rounded">Home</a>
            <a href="#" class="hover:bg-red-500 px-3 py-2 rounded">About</a>
            <a href="#" class="hover:bg-red-500 px-3 py-2 rounded">Contact</a>
          </div>
        </div>
      </div>
    </nav>
    
    <div class="grid grid-cols-2">
      <div class="bg-[url(src/images/left_box.png)]">
      </div>
      <div class="bg-[#FAF4E6] text-[#846757] text-[100px] font-bold pl-10">
        <p class="font-display">Health <br>Quest</p>
        <p class="text-[20px]">Staying motivated is hard. HealthQuest makes <br>
        it easy with a structured, gamified journey that <br>
        rewards you for every healthy choice, big or small.</p>
        <button class="bg-[#E99D7D] hover:bg-orange-500 text-[#A75B3A] text-[30px]
        h-[100px] w-[300px] rounded-[50%] outline-4 border-[#A75B3A]" @click="redirectToGoogle">Get Started</button>
          
      </div>
    </div>
  </div>
</template>
<script setup>

import { ref } from 'vue'

const redirectToGoogle = () => {
  window.location.href = "http://127.0.0.1:8000/accounts/google/login/"
}
</script>
