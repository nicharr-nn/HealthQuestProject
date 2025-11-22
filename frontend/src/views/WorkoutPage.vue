<template>
  <div class="m-8 rounded-xl flex justify-center font-body">
    <h1 class="ml-2 text-[50px] text-[#846757] font-subtitle">Choose Your Workout</h1>
  </div>

  <!-- Loading & Error States -->
  <div v-if="loading" class="text-center text-gray-500 mt-10">Loading programs...</div>
  <div v-else-if="error" class="text-center text-red-500 mt-10">{{ error }}</div>

  <!-- Member: Assigned Programs -->
  <div v-else-if="userRole === 'member'">
    <h2 class="m-8 text-2xl font-semibold text-[#B45253]">Assigned Programs</h2>
    <div v-if="assignments.length === 0" class="text-center text-gray-500 m-8">
      No assigned programs.
    </div>
    <div v-else class="grid gap-8 grid-cols-1 md:grid-cols-2 lg:grid-cols-3 m-8">
      <ProgramCard
        v-for="assignment in assignments"
        :key="assignment.id"
        :program="assignment.program"
        :assignment="assignment"
        @select="selectProgram"
      />
    </div>
    <h2 class="m-8 text-2xl font-semibold text-[#6FA4AF]">Available Programs</h2>
    <div v-if="availablePrograms.length === 0" class="text-center text-gray-500 m-8">
      No additional programs available.
    </div>
    <div v-else class="grid gap-8 grid-cols-1 md:grid-cols-2 lg:grid-cols-3 m-8">
      <ProgramCard
        v-for="program in availablePrograms"
        :key="program.id"
        :program="program"
        @select="selectProgram"
      />
    </div>
  </div>

  <!-- Non-member: Public programs -->
  <div v-else class="grid gap-8 grid-cols-1 md:grid-cols-2 lg:grid-cols-3 m-8">
    <ProgramCard
      v-for="program in programs"
      :key="program.id"
      :program="program"
      @select="selectProgram"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import ProgramCard from '@/components/ProgramCard.vue'

const router = useRouter()
const programs = ref([])
const assignments = ref([])
const loading = ref(true)
const error = ref(null)
const userRole = ref(null)
const API_URL = 'http://127.0.0.1:8000'
const userStore = useUserStore()

const availablePrograms = computed(() => {
  if (userRole.value !== 'member') {
    return programs.value
  }

  const assignedProgramIds = new Set(assignments.value.map((assignment) => assignment.program.id))

  return programs.value.filter((program) => !assignedProgramIds.has(program.id))
})

async function fetchPrograms() {
  try {
    const response = await fetch(`${API_URL}/api/workout/programs/`, {
      credentials: 'include',
    })
    if (!response.ok) throw new Error(`Failed to fetch: ${response.status}`)
    programs.value = await response.json()
  } catch (err) {
    console.error('Error fetching programs:', err)
    error.value = 'Could not load workout programs.'
  }
}

async function fetchWorkoutAssignments() {
  try {
    const response = await fetch(`${API_URL}/api/workout/assignments/`, {
      credentials: 'include',
    })
    if (!response.ok) throw new Error(`Failed to fetch assignments: ${response.status}`)
    assignments.value = await response.json()
  } catch (err) {
    console.error('Error fetching assignments:', err)
    error.value = 'Could not load your assignments.'
  }
}

function selectProgram(programId) {
  router.push(`/workout/${programId}`)
}

onMounted(async () => {
  loading.value = true
  try {
    userRole.value = userStore.role || userStore.profile?.role || null

    if (userRole.value === 'member') {
      await fetchWorkoutAssignments()
      await fetchPrograms()
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
