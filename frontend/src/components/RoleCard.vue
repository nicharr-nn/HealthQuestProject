<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  points: { type: Array, default: () => [] },
  color: { type: String, default: 'text-black'},
  bg: { type: String, default: 'bg-white' }, // tailwind class for background color
  titleColor: { type: String, default: 'text-gray-800' }
  
})
</script>


<template>
  <div class="relative rounded-xl2 p-8 border border-black/5 h-full flex flex-col transition-all duration-300 hover:shadow-xl hover:scale-105 hover:brightness-110 cursor-pointer" :class="bg">
    <h3 class="text-center font-bold tracking-wide mb-4 flex-shrink-0 transition-colors duration-300" :class="['text-lg', titleColor]">
      {{ title }}
    </h3>

    <ol class="list-decimal list-inside space-y-2 text-[15px] leading-relaxed flex-grow" :class="color">
      <li v-for="(p, i) in points" :key="i">{{ p }}</li>
    </ol>
  </div>
</template>

