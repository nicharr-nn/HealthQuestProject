<script setup>
defineProps({
  title: { type: String, required: true },
  color: { type: String, default: 'text-black'},
  bg: { type: String, default: 'bg-white' }, // tailwind class for background color
  titleColor: { type: String, default: 'text-gray-800' },
  selected: Boolean
  
})
</script>


<template>
  <div class="relative rounded-xl2 p-8 border border-black/5 h-full flex flex-col transition-all duration-300 hover:shadow-xl hover:scale-105 hover:brightness-110 cursor-pointer" :class="bg">
    <h3 class="text-center font-bold tracking-wide mb-4 flex-shrink-0 transition-colors duration-300" :class="['text-lg', titleColor]">
      {{ title }}
    </h3>

  </div>
</template>

