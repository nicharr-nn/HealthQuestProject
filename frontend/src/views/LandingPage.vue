<template>
  <div class="min-h-screen">

    <!-- Home Section -->
    <section id="home" class="grid grid-cols-1 md:grid-cols-2 min-h-screen">
      <div class="relative bg-cover bg-center" style="background-image: url(src/images/left_box.png)">
        <div class="absolute inset-0 flex items-center justify-center p-8 md:p-12 lg:p-16">
          <img 
            src="@/images/pure.jpg" 
            alt="Featured Image" 
            class="max-w-full max-h-full object-contain rounded-lg"
          />
        </div>
      </div>
      <div class="bg-[#FAF4E6] text-[#846757] p-8 md:p-12 lg:p-16">
        <h1 class="font-display text-6xl md:text-8xl lg:text-[100px] leading-tight mb-6">
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
    <section id="contract" class="bg-[#FAF4E6] text-[#846757] py-16 px-4 font-body">
      <div class="max-w-7xl mx-auto text-center">
        <h2 class="text-3xl md:text-4xl font-subtitle  mb-4">Contact Us</h2>
        <p class="text-lg md:text-xl mb-8">
          Get in touch with us! We'd love to hear from you.
        </p>

        <div class="flex flex-col md:grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="h-80 w-full bg-blue-200 rounded-xl flex flex-col items-center justify-center p-4">
            <div class="w-48 aspect-square overflow-hidden rounded-lg">
              <img 
                src="@/images/nicha.jpg" 
                alt="Contact Us" 
                class="w-full h-full object-cover"
              />
            </div>
            <p class="text-[#846757] mt-4">Nicha Ruangrit<br>
              Email: nicha.rua@ku.th
            </p>
          </div>
          <div class="h-80 w-full bg-blue-200 rounded-xl flex flex-col items-center justify-center p-4">
            <div class="w-48 aspect-square overflow-hidden rounded-lg">
              <img 
                src="@/images/phavida.jpg" 
                alt="Contact Us" 
                class="w-full h-full object-cover"
              />
            </div>
            <p class="text-[#846757] mt-4">Phavida Rattanamongkolkul<br>
              Email: phavida.r@ku.th
            </p>
          </div>          
          <div class="h-80 w-full bg-blue-200 rounded-xl flex flex-col items-center justify-center p-4">
            <div class="w-48 aspect-square overflow-hidden rounded-lg">
              <img 
                src="@/images/punnapa.jpg" 
                alt="Contact Us" 
                class="w-full h-full object-cover"
              />
            </div>
            <p class="text-[#846757] mt-4">Punnapa Pramotekul<br>
              Email: punnapa.pr@ku.th
            </p>
          </div>
          <div class="h-80 w-full bg-blue-200 rounded-xl flex flex-col items-center justify-center p-4">
            <div class="w-48 aspect-square overflow-hidden rounded-lg">
              <img 
                src="@/images/raveewan.jpeg" 
                alt="Contact Us" 
                class="w-full h-full object-cover"
              />
            </div>
            <p class="text-[#846757] mt-4">Raveewan Santipong<br>
              Email: raveewan.s@ku.th
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const redirectToGoogle = () => {
  window.location.href = "http://127.0.0.1:8000/accounts/google/login/"
}
</script>