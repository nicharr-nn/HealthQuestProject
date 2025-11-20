<script setup>
defineProps({
  title: { type: String, required: true },
  color: { type: String, default: 'text-black' },
  bg: { type: String, default: 'bg-white' },
  titleColor: { type: String, default: 'text-gray-800' },
  selected: Boolean,
  description: { type: String, default: '' },
  duration: { type: String, default: '' },
  focus: { type: String, default: '' },
  level: { type: String, default: '' },
  benefits: { type: Array, default: () => [] },
})
</script>

<template>
  <div
    class="relative rounded-xl2 p-7 border border-black/5 h-full flex flex-col transition-all duration-300 hover:shadow-xl hover:scale-105 hover:brightness-110 cursor-pointer"
    :class="bg"
  >
    <h3
      class="font-body text-center font-bold tracking-wide mb-4 flex-shrink-0 transition-colors duration-300"
      :class="['text-lg', titleColor]"
    >
      {{ title }}
    </h3>
    <!-- Description -->
    <p v-if="description" class="text-base text-gray-600 mb-4 font-body">
      {{ description }}
    </p>

    <!-- Metadata as little squares/chips -->
    <div
      v-if="duration || focus || level"
      class="flex flex-wrap gap-2 mb-4 font-body justify-start max-w-full"
    >
      <div
        v-if="duration"
        class="bg-[#ffffffa6] px-1 py-1 rounded-full text-xs font-bold border-1 border-[##00000014] whitespace-nowrap"
      >
        {{ duration }}
      </div>

      <div
        v-if="focus"
        class="bg-[#ffffffa6] px-1 py-1 rounded-full text-xs font-bold border-1 border-[##00000014] whitespace-nowrap"
      >
        {{ focus }}
      </div>

      <div
        v-if="level"
        class="bg-[#ffffffa6] px-1 py-1 rounded-full text-xs font-bold border-1 border-[##00000014] whitespace-nowrap"
      >
        {{ level }}
      </div>
    </div>

    <!-- Benefits List -->
    <div v-if="benefits && benefits.length > 0" class="mt-auto font-body">
      <ul class="text-base text-gray-600 space-y-1">
        <li v-for="(benefit, index) in benefits" :key="index" class="flex items-start">
          <span class="text-[##00000014] mr-1">•</span>
          {{ benefit }}
        </li>
      </ul>
    </div>
  </div>
</template>
