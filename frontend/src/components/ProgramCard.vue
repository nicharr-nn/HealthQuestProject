<template>
  <div
    class="bg-[#B0D3cc] rounded-xl p-6 shadow-lg hover:shadow-2xl transition-shadow cursor-pointer flex flex-col justify-between"
    @click="handleClick"
  >
    <!-- Header Section -->
    <div>
      <div class="mb-2">
        <!-- Title - Fixed to match view file -->
        <h2 class="text-2xl font-extrabold text-[#846757] mb-2 uppercase">
          {{ program.title }}
        </h2>

        <!-- Description - Fixed styling -->
        <p class="text-gray-600 mb-4 line-clamp-3">
          {{ program.description || 'No description available.' }}
        </p>

        <!-- Tags/Badges - Fixed to match view file -->
        <div class="flex flex-wrap gap-2 mb-4 text-sm">
          <span
            v-if="program.difficulty_level"
            class="bg-white px-3 py-1 rounded-full text-gray-700 shadow"
          >
            {{ formatStatus(program.difficulty_level) }}
          </span>

          <span 
            v-if="program.category" 
            class="bg-white px-3 py-1 rounded-full text-gray-700 shadow"
          >
            {{ formatStatus(program.category) }}
          </span>

          <!-- Assignment specific badges -->
          <span
            v-if="assignment && assignment.status"
            class="bg-white px-3 py-1 rounded-full text-gray-700 shadow"
            :class="getStatusClass(assignment.status)"
          >
            {{ formatStatus(assignment.status) }}
          </span>

          <span
            v-if="assignment && assignment.due_date"
            class="bg-orange-100 text-orange-800 px-3 py-1 rounded-full"
          >
            Due: {{ formatDate(assignment.due_date) }}
          </span>
        </div>
      </div>

      <!-- Action Button - Fixed to match view file -->
      <button
        @click.stop="handleClick"
        class="mt-4 bg-[#6AA6A0] hover:bg-[#5C938C] text-white px-5 py-2 rounded-lg font-semibold transition-colors w-full"
        :disabled="isLocked"
      >
        {{ buttonText }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  program: {
    type: Object,
    required: true,
  },
  assignment: {
    type: Object,
    default: null,
  },
  isLocked: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['select'])

const buttonText = computed(() => {
  if (props.assignment?.status === 'completed') return 'Review Program'
  if (props.assignment) return 'Continue Program'
  return 'View Program'
})

function getStatusClass(status) {
  const classes = {
    assigned: 'bg-blue-100 text-blue-800',
    in_progress: 'bg-purple-100 text-purple-800',
    completed: 'bg-green-100 text-green-800',
  }
  return classes[status?.toLowerCase()] || 'bg-gray-100 text-gray-800'
}

function formatStatus(data) {
  if (!data) return ''
  // Replace underscores with spaces and capitalize
  return data.replace(/_/g, ' ').toUpperCase()
}

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

function handleClick() {
  if (!props.isLocked) {
    emit('select', props.program.id)
  }
}
</script>