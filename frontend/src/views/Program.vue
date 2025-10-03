<template>
  <div class="p-6">
    <div class="relative max-w-6xl mx-auto">
      <button
        type="button"
        @click="scrollLeft"
        class="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-white rounded-full p-2 shadow-md hover:shadow-lg transition-shadow duration-200"
        aria-label="Scroll left"
      >
        <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>

      <!-- Days Container -->
      <div
        ref="daysContainer"
        class="flex gap-4 overflow-x-auto scrollbar-hide px-12 py-4 scroll-smooth"
        style="scrollbar-width: none; -ms-overflow-style: none;"
      >
        <button
          v-for="day in days"
          :key="day.id"
          type="button"
          @click="selectDay(day.id)"
          :aria-selected="day.id === selectedDay ? 'true' : 'false'"
          :class="[
            'flex-shrink-0 px-6 py-4 rounded-2xl font-medium text-center cursor-pointer transition-all duration-200 min-w-[120px] focus:outline-none',
            day.id === selectedDay
              ? 'bg-indigo-600 text-white shadow-lg scale-105'
              : day.type === 'rest'
                ? 'bg-purple-100 text-purple-600 hover:bg-purple-200'
                : 'bg-white text-gray-700 hover:bg-gray-100 shadow-sm hover:shadow-md border border-gray-200'
          ]"
        >
          {{ day.label }}
        </button>
      </div>

      <!-- Right Arrow -->
      <button
        type="button"
        @click="scrollRight"
        class="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-white rounded-full p-2 shadow-md hover:shadow-lg transition-shadow duration-200"
        aria-label="Scroll right"
      >
        <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>

    <!-- Demo content showing selected day -->
    <div class="max-w-4xl mx-auto mt-12 p-6 bg-white rounded-xl shadow-sm">
      <h3 class="text-2xl font-bold text-gray-900 mb-4">
        {{ selectedDayInfo.label }} - {{ selectedDayInfo.type === 'rest' ? 'Rest Day' : 'Workout Day' }}
      </h3>
      <p class="text-gray-600">
        {{
          selectedDayInfo.type === 'rest'
            ? 'Take a well-deserved rest today. Light stretching or a gentle walk is perfect!'
            : `Today's workout focuses on ${selectedDayInfo.focus}. Remember to warm up before starting!`
        }}
      </p>
    </div>

    <!-- Alternative Compact Version -->
    <div class="max-w-6xl mx-auto mt-16">
      <h3 class="text-lg font-semibold text-gray-800 mb-4">Compact Version:</h3>
      <div class="flex gap-2 overflow-x-auto scrollbar-hide pb-2">
        <button
          v-for="day in days.slice(0, 14)"
          :key="`compact-${day.id}`"
          type="button"
          @click="selectDay(day.id)"
          :class="[
            'flex-shrink-0 w-16 h-16 rounded-xl font-medium text-sm text-center cursor-pointer transition-all duration-200 flex items-center justify-center focus:outline-none',
            day.id === selectedDay
              ? 'bg-indigo-600 text-white shadow-lg'
              : day.type === 'rest'
                ? 'bg-purple-100 text-purple-600 hover:bg-purple-200'
                : 'bg-white text-gray-700 hover:bg-gray-100 shadow-sm hover:shadow-md border border-gray-200'
          ]"
        >
          {{ day.shortLabel }}
        </button>
      </div>
    </div>

    <!-- Week View Version -->
    <div class="max-w-6xl mx-auto mt-16">
      <h3 class="text-lg font-semibold text-gray-800 mb-4">Week View:</h3>
      <div class="grid grid-cols-7 gap-2">
        <button
          v-for="day in days.slice(0, 7)"
          :key="`week-${day.id}`"
          type="button"
          @click="selectDay(day.id)"
          :class="[
            'aspect-square rounded-xl font-medium text-center cursor-pointer transition-all duration-200 flex flex-col items-center justify-center p-2 focus:outline-none',
            day.id === selectedDay
              ? 'bg-indigo-600 text-white shadow-lg'
              : day.type === 'rest'
                ? 'bg-purple-100 text-purple-600 hover:bg-purple-200'
                : 'bg-white text-gray-700 hover:bg-gray-100 shadow-sm hover:shadow-md border border-gray-200'
          ]"
        >
          <div class="text-xs opacity-75 mb-1">{{ getDayOfWeek(day.id) }}</div>
          <div class="font-semibold">{{ day.shortLabel }}</div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const daysContainer = ref(null)
const selectedDay = ref(1)

const days = ref([
  { id: 1, label: 'Day 1', shortLabel: 'D1', type: 'workout', focus: 'booty & core' },
  { id: 2, label: 'Day 2', shortLabel: 'D2', type: 'workout', focus: 'upper body' },
  { id: 3, label: 'Day 3', shortLabel: 'D3', type: 'workout', focus: 'full body' },
  { id: 4, label: 'Day 4', shortLabel: 'D4', type: 'workout', focus: 'booty & abs' },
  { id: 5, label: 'Rest Day', shortLabel: 'R', type: 'rest' },
  { id: 6, label: 'Day 6', shortLabel: 'D6', type: 'workout', focus: 'cardio & core' },
  { id: 7, label: 'Rest Day', shortLabel: 'R', type: 'rest' },
  { id: 8, label: 'Day 8', shortLabel: 'D8', type: 'workout', focus: 'booty & core' },
  { id: 9, label: 'Day 9', shortLabel: 'D9', type: 'workout', focus: 'upper body' },
  { id: 10, label: 'Day 10', shortLabel: 'D10', type: 'workout', focus: 'full body' },
  { id: 11, label: 'Day 11', shortLabel: 'D11', type: 'workout', focus: 'booty & abs' },
  { id: 12, label: 'Rest Day', shortLabel: 'R', type: 'rest' },
  { id: 13, label: 'Day 13', shortLabel: 'D13', type: 'workout', focus: 'cardio & core' },
  { id: 14, label: 'Rest Day', shortLabel: 'R', type: 'rest' },
  { id: 15, label: 'Day 15', shortLabel: 'D15', type: 'workout', focus: 'booty & core' },
  { id: 16, label: 'Day 16', shortLabel: 'D16', type: 'workout', focus: 'upper body' },
  { id: 17, label: 'Day 17', shortLabel: 'D17', type: 'workout', focus: 'full body' },
  { id: 18, label: 'Day 18', shortLabel: 'D18', type: 'workout', focus: 'booty & abs' },
  { id: 19, label: 'Rest Day', shortLabel: 'R', type: 'rest' },
  { id: 20, label: 'Day 20', shortLabel: 'D20', type: 'workout', focus: 'cardio & core' },
  { id: 21, label: 'Final Day', shortLabel: 'F', type: 'workout', focus: 'celebration workout' }
])

const selectedDayInfo = computed(() => {
  return (
    days.value.find(d => d.id === selectedDay.value) || {
      id: 0, label: 'Unknown', shortLabel: '?', type: 'rest', focus: ''
    }
  )
})

function selectDay(dayId) {
  selectedDay.value = dayId
}

function scrollLeft() {
  daysContainer.value?.scrollBy({ left: -200, behavior: 'smooth' })
}

function scrollRight() {
  daysContainer.value?.scrollBy({ left: 200, behavior: 'smooth' })
}

function getDayOfWeek(dayId) {
  const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
  return daysOfWeek[(dayId - 1) % 7]
}
</script>

<style scoped>
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>
