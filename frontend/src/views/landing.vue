<template>
  <div class="min-h-screen">
    <!-- Use the Navbar component -->    
    <!-- Home Section -->
    <section id="home" class="grid grid-cols-1 md:grid-cols-2 min-h-screen">
      <div class="bg-cover bg-center" style="background-image: url(src/images/left_box.png)">
      </div>
      <div class="bg-[#FAF4E6] text-[#846757] p-8 md:p-12 lg:p-16">
        <h1 class="font-display font-bold text-6xl md:text-8xl lg:text-[100px] leading-tight mb-6">
          Health <br>Quest
        </h1>
        <p class="text-lg md:text-xl lg:text-2xl mb-8 leading-relaxed">
          Staying motivated is hard. HealthQuest makes
          it easy with a structured, gamified journey that
          rewards you for every healthy choice, big or small.
        </p>
        <button 
          @click="redirectToGoogle"
          class="bg-[#E99D7D] hover:bg-[#D88C6C] text-[#A75B3A] 
                 font-bold text-xl md:text-2xl lg:text-3xl
                 h-16 md:h-20 lg:h-24 w-48 md:w-56 lg:w-64
                 rounded-full border-2 border-[#A75B3A]
                 transition-colors duration-200
                 flex items-center justify-center"
        >
          Get Started
        </button>
      </div>
    </section>

    <!-- About Section -->
    <section id="about" class="bg-[#E99D7D] py-16 px-4">
      <div class="max-w-7xl mx-auto">
        <div class="flex flex-col md:flex-row gap-6">
          <div class="bg-[#FAF4E6] rounded-lg p-6 md:basis-1/2">
            <h3 class="text-[#846757] font-bold text-2xl mb-4 border-b-2 border-[#846757]">About</h3>
            <p class="text-[#846757] text-lg">
              HealthQuest is a fitness platform that combines structured workouts, 
              nutrition tracking, and gamified progression. Users earn XP, set goals, 
              and unlock new features. With personalized coaching and private recipe sharing, 
              it fosters long-term healthy habits in a supportive community.
            </p>
          </div>
          <div class="bg-[#FAF4E6] rounded-lg p-6 md:basis-1/2">
            <h3 class="text-[#846757] font-bold text-2xl mb-4 border-b-2 border-[#846757]">Gamified Experience</h3>
            <ul class="list-disc list-inside text-[#846757] text-lg space-y-2">
              <li>Level up your character</li>
              <li>Complete epic quests</li>
              <li>Earn achievements for every healthy choice you make</li>
              <li>Unlock new features as you progress</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Contact Section -->
    <section id="contract" class="bg-[#FAF4E6] py-16 px-4">
      <div class="max-w-7xl mx-auto text-center">
        <h2 class="text-3xl md:text-4xl font-bold text-[#846757] mb-4">Contact Us</h2>
        <p class="text-lg md:text-xl text-[#846757] mb-8">
          Get in touch with us! We'd love to hear from you.
        </p>
      </div>
    </section>
  </div>
</template>

<script setup>

const redirectToGoogle = () => {
  window.location.href = "http://127.0.0.1:8000/accounts/google/login/"
}
</script>