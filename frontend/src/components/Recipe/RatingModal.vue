<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
  >
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6 relative">
      <!-- Close Button -->
      <button
        @click="$emit('close')"
        class="absolute top-3 right-3 text-gray-400 hover:text-gray-600 text-2xl cursor-pointer"
      >
        ×
      </button>

      <!-- Modal Title -->
      <h2 class="text-2xl font-bold mb-4 text-pink-400">Rate Recipe</h2>

      <!-- Recipe Name -->
      <p class="text-gray-700 mb-4 font-medium">
        {{ recipeName }}
      </p>

      <!-- Star Rating -->
      <div class="mb-6">
        <p class="text-sm font-semibold mb-3 text-gray-600">Select your rating:</p>
        <div class="flex gap-2 justify-center">
          <button
            v-for="star in 5"
            :key="star"
            @click="localRating = star"
            class="text-4xl hover:scale-110 transition-transform cursor-pointer"
          >
            {{ star <= localRating ? '⭐' : '☆' }}
          </button>
        </div>
        <p v-if="localRating > 0" class="text-center text-sm text-gray-500 mt-2">
          {{ localRating }} {{ localRating === 1 ? 'star' : 'stars' }}
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-3">
        <button
          @click="$emit('close')"
          class="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition text-gray-700 font-medium cursor-pointer"
        >
          Cancel
        </button>
        <button
          @click="handleSubmit"
          :disabled="localRating === 0"
          class="flex-1 px-4 py-2 bg-pink-400 hover:bg-pink-500 text-white rounded-lg transition font-medium disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
        >
          {{ hasRating ? 'Update Rating' : 'Submit Rating' }}
        </button>
      </div>

      <div v-if="hasRating" class="mt-3 pt-3 border-t border-gray-200">
        <button
          @click="$emit('remove')"
          class="w-full px-4 py-2 bg-red-100 hover:bg-red-200 text-red-700 rounded-lg transition font-medium text-sm cursor-pointer"
        >
          Remove My Rating
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  recipeName: {
    type: String,
    default: ''
  },
  currentRating: {
    type: Number,
    default: 0
  },
  hasRating: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'submit', 'remove'])

const localRating = ref(props.currentRating)

watch(() => props.currentRating, (newVal) => {
  localRating.value = newVal
})

const handleSubmit = () => {
  if (localRating.value > 0) {
    emit('submit', localRating.value)
  }
}
</script>