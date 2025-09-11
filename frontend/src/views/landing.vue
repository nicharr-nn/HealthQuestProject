<template>
  <div id ="home" class="grid grid-rows-[auto_1fr] h-screen">
    <nav class="bg-[#88ACEA] text-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <span class="text-xl font-bold">HealthQuest</span>
          </div>
          <div class="flex space-x-4">
            <a href="#home" class="hover:bg-red-500 px-3 py-2 rounded">Home</a>
            <a href="#about" class="hover:bg-red-500 px-3 py-2 rounded">About</a>
            <a href="#contract" class="hover:bg-red-500 px-3 py-2 rounded">Contact</a>
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
  <div id="about"class="bg-[#E99D7D] p-4">
  </div>
  <div class="bg-[#A75B3A] p-8">
        <div class="max-w-7xl mx-auto flex flex-row gap-6">
          <div class="bg-[#FAF4E6] rounded-lg p-6 basis-1/2">
            <h3 class="text-[#846757] font-bold text-2xl mb-4 border-b-2">About</h3>
            <p class="text-[#846757]">HealthQuest is a fitness platform that combines structured workouts, 
              nutrition tracking, and gamified progression. Users earn XP, set goals, 
              and unlock new features. With personalized coaching and private recipe sharing, 
              it fosters long-term healthy habits in a supportive community.</p>
          </div>
          <div class="bg-[#FAF4E6] rounded-lg p-6 basis-1/2">
            <h3 class="text-[#846757] font-bold text-2xl mb-4 border-b-2">Gamified Experience</h3>
            <ul class="list-disc list-inside text-[#846757]">
              <li>Level up your character</li>
              <li>Complete epic quests</li>
              <li>Earn achievements for every healthy choice you make</li>
            </ul>
          </div>
        </div>
  </div>
  <div id="contract" class="bg-[#FAF4E6] p-4">
    <h2>Contact Us</h2>
  <p>Get in touch with us!</p>

  </div>

</template>
<script setup>

import { ref } from 'vue'

const redirectToGoogle = () => {
  window.location.href = "http://127.0.0.1:8000/accounts/google/login/"
}
</script>
