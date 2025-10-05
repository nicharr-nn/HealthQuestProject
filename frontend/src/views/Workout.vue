<template>
  <div class="m-8 rounded-xl flex justify-center">
    <h1 class="ml-2 text-[50px] font-subtitle">Choose Your Workout</h1>
  </div>

  <!-- Loading & Error States -->
  <div v-if="loading" class="text-center text-gray-500 mt-10">Loading programs...</div>
  <div v-else-if="error" class="text-center text-red-500 mt-10">{{ error }}</div>

  <!-- Program Cards -->
  <div v-else class="grid gap-8 grid-cols-1 md:grid-cols-2 lg:grid-cols-3 m-8">
    <div
      v-for="program in programs"
      :key="program.id"
      class="bg-[#B0D3cc] rounded-xl p-6 shadow-lg hover:shadow-2xl transition-shadow cursor-pointer flex flex-col justify-between"
    >
      <div>
        <h2 class="text-2xl font-bold text-gray-800 mb-2">{{ program.title }}</h2>
        <p class="text-gray-600 mb-4 line-clamp-3">{{ program.description }}</p>

        <div class="flex flex-wrap gap-2 mb-4 text-sm">
          <span class="bg-white px-3 py-1 rounded-full text-gray-700 shadow">
            Level: {{ program.level_access }}
          </span>
          <span class="bg-white px-3 py-1 rounded-full text-gray-700 shadow">
            {{ program.difficulty_level }}
          </span>
          <span class="bg-white px-3 py-1 rounded-full text-gray-700 shadow">
            {{ program.category }}
          </span>
        </div>
      </div>

      <button
        @click="selectProgram(program.id)"
        class="mt-4 bg-[#6AA6A0] hover:bg-[#5C938C] text-white px-5 py-2 rounded-lg font-semibold transition-colors"
      >
        View Program
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const programs = ref([])
const loading = ref(true)
const error = ref(null)

async function fetchPrograms() {
  console.log('Fetching programs...')
  try {
    const response = await fetch('http://127.0.0.1:8000/api/workout/programs/', {
      credentials: 'include',
    })
    if (!response.ok) throw new Error(`Failed to fetch: ${response.status}`)
    programs.value = await response.json()
    console.log('Programs loaded:', programs.value)
  } catch (err) {
    console.error('Error fetching programs:', err)
    error.value = 'Could not load workout programs.'
  } finally {
    loading.value = false
  }
}

function selectProgram(programId) {
  console.log('Navigating to program:', programId)
  console.log('Route:', `/workout/${programId}`)
  router.push(`/workout/${programId}`)
}

onMounted(() => {
  console.log('Workout list component mounted')
  fetchPrograms()
})
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>