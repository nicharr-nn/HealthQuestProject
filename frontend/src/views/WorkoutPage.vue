<template>
  <div class="m-8 rounded-xl flex justify-center font-body">
    <h1 class="ml-2 text-[50px] text-[#846757] font-subtitle">Choose Your Workout</h1>
  </div>

  <!-- Loading & Error States -->
  <div v-if="loading" class="text-center text-gray-500 mt-10">Loading programs...</div>
  <div v-else-if="error" class="text-center text-red-500 mt-10">{{ error }}</div>

  <!-- Member: Assigned Programs -->
  <div v-else-if="userRole === 'member'">
    <h2 class="m-8 text-2xl font-semibold text-[#B87C4C]">Assigned Programs</h2>
    <div v-if="assignments.length === 0" class="text-center text-gray-500 m-8">
      No assigned programs.
    </div>
    <div v-else class="grid gap-8 grid-cols-1 md:grid-cols-2 lg:grid-cols-3 m-8">
      <div
        v-for="assignment in assignments"
        :key="assignment.id"
        class="bg-[#B0D3cc] rounded-xl p-6 shadow-lg hover:shadow-2xl transition-shadow cursor-pointer flex flex-col justify-between"
      >
        <div>
          <h2 class="text-2xl font-extrabold text-[#846757] mb-2">
            {{ assignment.program.title }}
          </h2>
          <p class="text-gray-600 mb-4 line-clamp-3">
            {{ assignment.program.description }}
          </p>

          <div class="flex flex-wrap gap-2 mb-4 text-sm">
            <span class="bg-white px-3 py-1 rounded-full text-gray-700 shadow">
              {{ assignment.program.difficulty_level.toUpperCase() }}
            </span>
            <span class="bg-white px-3 py-1 rounded-full text-gray-700 shadow">
              {{ assignment.program.category.toUpperCase() }}
            </span>
          </div>
        </div>

        <button
          @click="selectProgram(assignment.program.id)"
          class="mt-4 bg-[#6AA6A0] hover:bg-[#5C938C] text-white px-5 py-2 rounded-lg font-semibold transition-colors"
        >
          View Program
        </button>
      </div>
    </div>
  </div>

  <!-- Non-member: Public programs -->
  <div v-else class="grid gap-8 grid-cols-1 md:grid-cols-2 lg:grid-cols-3 m-8">
    <div
      v-for="program in programs"
      :key="program.id"
      class="bg-[#B0D3cc] rounded-xl p-6 shadow-lg hover:shadow-2xl transition-shadow cursor-pointer flex flex-col justify-between"
    >
      <div>
        <h2 class="text-2xl font-extrabold text-gray-800 mb-2 uppercase">{{ program.title }}</h2>
        <p class="text-gray-600 mb-4 line-clamp-3">{{ program.description }}</p>

        <div class="flex flex-wrap gap-2 mb-4 text-sm">
          <span class="bg-white px-3 py-1 rounded-full text-gray-700 shadow">
            {{ program.difficulty_level.toUpperCase() }}
          </span>
          <span class="bg-white px-3 py-1 rounded-full text-gray-700 shadow">
            {{ program.category.toUpperCase() }}
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
import { useUserStore } from '@/stores/user'

const router = useRouter()
const programs = ref([])
const assignments = ref([])
const loading = ref(true)
const error = ref(null)
const userRole = ref(null)

const userStore = useUserStore()

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
  }
}

async function fetchWorkoutAssignments() {
  console.log('Fetching workout assignments for current user')
  try {
    const response = await fetch('http://127.0.0.1:8000/api/workout/assignments/', {
      credentials: 'include',
    })
    if (!response.ok) throw new Error(`Failed to fetch assignments: ${response.status}`)
    assignments.value = await response.json()
    console.log('Assignments loaded:', assignments.value)
  } catch (err) {
    console.error('Error fetching assignments:', err)
    error.value = 'Could not load your assignments.'
  }
}

function selectProgram(programId) {
  console.log('Navigating to program:', programId)
  router.push(`/workout/${programId}`)
}

onMounted(async () => {
  loading.value = true
  try {
    userRole.value = userStore.role || userStore.profile?.role || null
    console.log('User role resolved:', userRole.value)

    if (userRole.value === 'member') {
      await fetchWorkoutAssignments()
    } else {
      await fetchPrograms()
    }
  } catch (err) {
    console.error('Error during initialization:', err)
    error.value = 'Failed to load data'
  } finally {
    loading.value = false
  }
})
</script>
