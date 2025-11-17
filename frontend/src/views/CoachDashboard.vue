<template>
  <div class="max-w-[1200px] mx-auto p-6">
    <div class="flex justify-between items-start mb-8 gap-5">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2 font-subtitle">Coach Dashboard</h1>
        <p class="text-gray-600 text-base mb-3 font-body">Manage your workout programs and track your coaching progress</p>

        <div class="flex items-center gap-2 py-2 px-3 bg-blue-50 border border-blue-500 rounded-lg w-fit">
          <span class="text-xs text-gray-600 font-medium">Your Coach ID:</span>
          <span class="text-sm text-blue-800 font-bold font-mono tracking-wide">{{ coachID }}</span>
          <button class="bg-blue-500 text-white px-2 py-1 rounded-md text-xs font-semibold hover:bg-blue-600 hover:scale-105 transition-all" @click="copyCoachID" title="Copy Coach ID">📋 Copy</button>
        </div>
      </div>

      <div class="flex-shrink-0 flex items-center gap-4">
        <NotificationBell v-if="isApproved" />
        <button
          class="border border-gray-300 rounded-lg px-4 py-2 font-semibold bg-gray-900 text-white hover:brightness-105 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          @click="router.push('/create-workout-program')"
          :disabled="!isApproved"
        >
          + Create New Program
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-gray-500 text-center py-8">
      Loading dashboard...
    </div>

    <!-- Approval Status (only if not approved) -->
    <div v-if="!isApproved" class="bg-white border border-gray-200 rounded-2xl p-6 mb-8 shadow-sm">
      <div class="flex items-center gap-4 p-5 rounded-xl mb-5" :class="approvalStatus === 'pending' ? 'bg-yellow-50 border border-yellow-400' : 'bg-red-50 border border-red-500'">
        <div class="text-2xl">
          <span v-if="approvalStatus === 'pending'">⏳</span>
          <span v-else-if="approvalStatus === 'rejected'">❌</span>
        </div>
        <div class="flex-1">
          <div class="font-semibold text-base text-gray-700 mb-1">
            {{ approvalStatus === 'pending' ? 'Application Under Review' : 'Application Rejected' }}
          </div>
          <div class="text-gray-600 leading-relaxed">
            {{ approvalStatus === 'pending'
              ? "Your application is being reviewed. You can create programs once approved."
              : "Please contact support or resubmit your application." }}
          </div>
        </div>
      </div>
    </div>

    <!-- Dashboard Content -->
    <div v-else>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-5 mb-8">
        <div class="bg-white border border-gray-200 rounded-xl p-6 text-center shadow-sm transition-all">
          <div class="text-3xl font-bold text-blue-500 mb-2">{{ programs.length }}</div>
          <div class="text-gray-600 font-medium">Total Programs</div>
        </div>
        <div class="bg-white border border-gray-200 rounded-xl p-6 text-center shadow-sm transition-all">
          <div class="text-3xl font-bold text-blue-500 mb-2">{{ totalSessions }}</div>
          <div class="text-gray-600 font-medium">Total Sessions</div>
        </div>
        <div class="bg-white border border-gray-200 rounded-xl p-6 text-center shadow-sm transition-all">
          <div class="text-3xl font-bold text-blue-500 mb-2">{{ programsWithVideos }}</div>
          <div class="text-gray-600 font-medium">Programs with Videos</div>
        </div>

        <div class="bg-white border border-gray-200 rounded-xl p-6 text-center shadow-sm cursor-pointer hover:-translate-y-0.5 hover:shadow-lg hover:border-blue-500 transition-all" @click="router.push('/view-member')">
          <div class="text-3xl font-bold text-blue-500 mb-2">{{ memberCount }}</div>
          <div class="text-gray-600 font-medium">My Members</div>
          <div class="mt-2 text-xs text-blue-500 font-semibold">View All →</div>
        </div>

        <div class="bg-white border border-gray-200 rounded-xl p-6 text-center shadow-sm cursor-pointer hover:-translate-y-0.5 hover:shadow-lg hover:border-blue-500 transition-all" @click="router.push('/view-request')">
          <div class="text-3xl font-bold text-blue-500 mb-2">{{ pendingRequestCount }}</div>
          <div class="text-gray-600 font-medium">Pending Requests</div>
          <div class="mt-2 text-xs text-blue-500 font-semibold">View All →</div>
        </div>
      </div>

      <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-semibold text-gray-900">Your Workout Programs</h2>
        </div>

        <!-- Empty state -->
        <div v-if="filteredPrograms.length === 0" class="text-center py-12 px-6">
          <div class="text-6xl mb-4">🏋️‍♂️</div>
          <div class="text-xl font-semibold text-gray-700 mb-3">No programs yet</div>
          <div class="text-gray-600 mb-6 leading-relaxed max-w-md mx-auto">
            Start creating your first workout program to help your clients achieve their goals!
          </div>
          <button class="border border-gray-300 rounded-lg px-4 py-2 font-semibold bg-gray-900 text-white hover:brightness-105 transition-all" @click="router.push('/create-workout-program')">
            Create Your First Program
          </button>
        </div>

        <!-- Programs grid -->
        <div v-else class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-5">
          <div v-for="program in filteredPrograms" :key="program.id" class="border border-gray-200 rounded-xl p-5 bg-gray-50 hover:border-blue-500 hover:shadow-lg transition-all">
            <div class="flex justify-between items-start mb-3">
              <div class="text-lg font-semibold text-gray-900 flex-1">{{ program.title }}</div>
              <div class="px-2 py-1 rounded-md text-xs font-medium uppercase" :class="{
                'bg-green-100 text-green-800': program.difficulty_level === 'beginner',
                'bg-yellow-100 text-yellow-900': program.difficulty_level === 'intermediate',
                'bg-red-100 text-red-900': program.difficulty_level === 'advanced'
              }">
                {{ program.difficulty_level }}
              </div>
            </div>

            <div class="text-gray-600 mb-4 leading-relaxed text-sm">
              {{ truncate(program.description, 120) || 'No description provided' }}
            </div>

            <!-- Program metadata -->
            <div class="grid gap-2 mb-4">
              <div class="flex justify-between text-xs">
                <span class="text-gray-600">Duration:</span>
                <span class="text-gray-700 font-medium">{{ program.duration }} day{{ program.duration === 1 ? '' : 's' }}</span>
              </div>
              <div class="flex justify-between text-xs">
                <span class="text-gray-600">Category:</span>
                <span class="text-gray-700 font-medium">{{ program.category || 'Not specified' }}</span>
              </div>
            </div>

            <!-- Actions for each program -->
            <div class="flex gap-2 flex-wrap">
              <button
                class="border border-gray-300 rounded-lg px-3 py-1.5 text-xs font-semibold bg-blue-500 text-white hover:bg-blue-600 transition-all"
                @click="editProgram(program.id)"
              >
                Edit
              </button>

              <button
                class="border border-red-500 rounded-lg px-3 py-1.5 text-xs font-semibold bg-red-500 text-white hover:bg-red-600 transition-all"
                @click="deleteProgram(program.id)"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NotificationBell from '@/components/NotificationBell.vue'

const router = useRouter()

const loading = ref(true)
const showCreateProgram = ref(false)
const approvalStatus = ref('pending')
const programs = ref([])
const coachID = ref('')
const memberCount = ref(0)
const editingProgram = ref(null)
const pendingRequestCount = ref(0)

const isApproved = computed(() => approvalStatus.value === 'approved')
const totalSessions = computed(() =>
  programs.value.reduce((sum, p) => sum + (p.days?.length || 0), 0)
)
const programsWithVideos = computed(() =>
  programs.value.filter(p => p.days?.some(d => d.video_links?.length > 0)).length
)
const filteredPrograms = computed(() => programs.value)

function copyCoachID() {
  if (coachID.value) {
    navigator.clipboard.writeText(coachID.value)
    alert('Coach ID copied to clipboard!')
  }
}


async function loadCoachStatus() {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/coach/status/', {
      credentials: 'include'
    })
    if (!res.ok) {
      approvalStatus.value = 'pending'
      coachID.value = ''
      return
    }

    const data = await res.json()
    const status = data?.coach?.status_approval ?? data?.status_approval ?? null
    approvalStatus.value = status === 'approved' ? 'approved' : status === 'rejected' ? 'rejected' : 'pending'

    coachID.value = data?.coach?.public_id ?? ''
  } catch (err) {
    console.error('Error loading coach status', err)
    approvalStatus.value = 'pending'
    coachID.value = ''
  }
}
const API_BASE = 'http://127.0.0.1:8000/api/workout/programs/'

async function loadPrograms() {
  try {
    const res = await fetch(API_BASE, { credentials: 'include' })
    const data = await res.json()
    if (Array.isArray(data)) {
      programs.value = data
    } else if (data.results && Array.isArray(data.results)) {
      programs.value = data.results
    } else if (data.id) {
      // API returned a single program (not an array)
      programs.value = [data]
    } else {
      programs.value = []
    }

  } catch {
    programs.value = []
  }
}

async function loadMemberCount() {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/member/coach-requests/', { credentials: 'include' })
    if (!res.ok) throw new Error('Failed to fetch requests')
    const data = await res.json()

    memberCount.value = data.filter((r) => r.status === 'accepted').length
  } catch (err) {
    console.error('Failed to load member count', err)
    memberCount.value = 0
  }
}

async function loadPendingRequestCount() {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/member/coach-requests/', { credentials: 'include' })
    if (!res.ok) throw new Error('Failed to fetch requests')
    const data = await res.json()
    pendingRequestCount.value = data.filter((r) => r.status === 'pending').length
    memberCount.value = data.filter((r) => r.status === 'accepted').length
  } catch (err) {
    console.error('Failed to load pending requests', err)
    pendingRequestCount.value = 0
    memberCount.value = 0
  }
}

async function editProgram(programId) {
  // Navigate to create-workout-program with the program ID
  router.push({
    path: '/create-workout-program',
    query: { edit: programId }
  })
}

async function deleteProgram(programId) {
  try {
    const res = await fetch(`${API_BASE}${programId}/`, {
      method: 'DELETE',
      credentials: 'include',
    })

    if (res.ok) {
      // refresh list
      await loadPrograms()
      // close modal if editing the deleted program
      if (editingProgram.value && editingProgram.value.id === programId) {
        editingProgram.value = null
        showCreateProgram.value = false
      }
      alert('Program deleted successfully!')
    } else {
      const text = await res.text()
      let body = text
      try {
        body = JSON.parse(text)
      } catch (err) {
        console.warn('Failed to parse response as JSON:', err)
      }
      console.error('Delete program failed:', res.status, body)
      const message = body?.detail || body?.error || body || `HTTP ${res.status}`
      alert('Failed to delete program: ' + JSON.stringify(message))
    }
  } catch (err) {
    console.error('Error deleting program:', err)
    alert('Failed to delete program')
  }
}

function truncate(text, max = 120) {
  if (text === null || text === undefined) return ''
  const s = String(text).trim()
  return s.length > max ? s.slice(0, max).trimEnd() + '…' : s
}

onMounted(async () => {
  await loadCoachStatus()

 if (isApproved.value) {
    await Promise.all([loadPrograms(), loadMemberCount(), loadPendingRequestCount()])
  }

  loading.value = false
})
</script>