<template>
  <div class="max-w-[1200px] mx-auto p-6">
    <div class="flex justify-between items-start mb-8 gap-5">
      <!-- Header content -->
      <div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Coach Dashboard</h1>
        <p class="text-gray-500 text-base mb-3">
          Manage your workout programs and track your coaching progress
        </p>

        <div
          class="flex items-center gap-2 px-3 py-2 bg-blue-50 border border-blue-500 rounded-lg w-fit"
        >
          <span class="text-xs text-gray-500 font-medium">Your Coach ID:</span>
          <span class="text-sm text-blue-900 font-bold font-mono tracking-wide">{{ coachID }}</span>

          <div class="relative">
            <!-- Popup -->
            <transition name="fade">
              <div
                v-if="copied"
                class="absolute -top-9 left-1/2 -translate-x-1/2 bg-blue-600 text-white text-xs px-2 py-1 rounded-md shadow-md"
              >
                Copied!
              </div>
            </transition>

            <!-- Clipboard Icon -->
            <Clipboard
              size="20"
              class="text-blue-600 hover:text-blue-700 cursor-pointer transition"
              @click="copyCoachID"
              title="Copy"
            />
          </div>
        </div>
      </div>

      <!-- Header actions -->
      <div class="flex items-center gap-4 shrink-0">
        <NotificationBell v-if="isApproved" />
        <button
          class="px-4 py-2 rounded-lg text-white bg-blue-600 font-semibold hover:bg-blue-700 transition disabled:opacity-50"
          @click="router.push('/create-workout-program')"
          :disabled="!isApproved"
        >
          + Create New Program
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center text-gray-600">Loading dashboard...</div>

    <!-- Approval Status -->
    <div v-if="!isApproved" class="bg-white border border-gray-200 rounded-2xl p-6 mb-8 shadow">
      <div
        class="flex items-center gap-4 p-5 rounded-xl mb-5"
        :class="{
          'bg-yellow-100 border border-yellow-500': approvalStatus === 'pending',
          'bg-red-100 border border-red-500': approvalStatus === 'rejected',
        }"
      >
        <div class="text-2xl">
          <icon.Loader class="animate-spin" v-if="approvalStatus === 'pending'" />
          <icon.XCircle v-else-if="approvalStatus === 'rejected'" />
        </div>

        <div class="flex-1">
          <div class="font-semibold text-gray-700 text-base mb-1">
            {{ approvalStatus === 'pending' ? 'Application Under Review' : 'Application Rejected' }}
          </div>
          <div class="text-gray-500 leading-relaxed">
            {{
              approvalStatus === 'pending'
                ? 'Your application is being reviewed. You can create programs once approved.'
                : 'Please contact support or resubmit your application.'
            }}
          </div>
        </div>
      </div>
    </div>

    <!-- Dashboard Content -->
    <div v-else>
      <!-- Stats Grid -->
      <div class="grid grid-cols-[repeat(auto-fit,minmax(200px,1fr))] gap-5 mb-8">
        <div class="bg-white border border-gray-200 rounded-xl p-6 text-center shadow transition">
          <div class="text-3xl font-bold text-blue-600 mb-2">{{ programs.length }}</div>
          <div class="text-gray-500 font-medium">Total Programs</div>
        </div>

        <div class="bg-white border border-gray-200 rounded-xl p-6 text-center shadow transition">
          <div class="text-3xl font-bold text-blue-600 mb-2">{{ totalSessions }}</div>
          <div class="text-gray-500 font-medium">Total Sessions</div>
        </div>

        <div class="bg-white border border-gray-200 rounded-xl p-6 text-center shadow transition">
          <div class="text-3xl font-bold text-blue-600 mb-2">{{ programsWithVideos }}</div>
          <div class="text-gray-500 font-medium">Programs with Videos</div>
        </div>

        <div
          class="bg-white border border-gray-200 rounded-xl p-6 text-center shadow cursor-pointer hover:-translate-y-1 hover:shadow-xl hover:border-blue-600 transition"
          @click="router.push('/view-member')"
        >
          <div class="text-3xl font-bold text-blue-600 mb-2">{{ memberCount }}</div>
          <div class="text-gray-500 font-medium">My Members</div>
          <div class="mt-2 text-blue-600 text-xs font-semibold">View All →</div>
        </div>

        <div
          class="bg-white border border-gray-200 rounded-xl p-6 text-center shadow cursor-pointer hover:-translate-y-1 hover:shadow-xl hover:border-blue-600 transition"
          @click="router.push('/view-request')"
        >
          <div class="text-3xl font-bold text-blue-600 mb-2">{{ pendingRequestCount }}</div>
          <div class="text-gray-500 font-medium">Pending Requests</div>
          <div class="mt-2 text-blue-600 text-xs font-semibold">View All →</div>
        </div>
      </div>

      <!-- Programs Section -->
      <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-semibold text-gray-900">Your Workout Programs</h2>
        </div>

        <!-- Empty -->
        <div v-if="filteredPrograms.length === 0" class="text-center py-12 px-6">
          <div class="text-6xl mb-4">🏋️‍♂️</div>
          <div class="text-xl font-semibold text-gray-700 mb-3">No programs yet</div>
          <div class="text-gray-500 leading-relaxed max-w-md mx-auto mb-6">
            Start creating your first workout program to help your clients achieve their goals!
          </div>
          <button
            class="px-4 py-2 rounded-lg text-white bg-blue-600 font-semibold hover:bg-blue-700 transition"
            @click="router.push('/create-workout-program')"
          >
            Create Your First Program
          </button>
        </div>

        <!-- Programs Grid -->
        <div v-else class="grid grid-cols-[repeat(auto-fill,minmax(350px,1fr))] gap-5">
          <div
            v-for="program in filteredPrograms"
            :key="program.id"
            class="border border-gray-200 rounded-xl p-5 bg-gray-50 hover:border-blue-600 hover:shadow-xl transition"
          >
            <!-- Header -->
            <div class="flex justify-between mb-3">
              <div class="text-lg font-semibold text-gray-900">
                {{ program.title }}
              </div>

              <div
                class="px-2 py-1 rounded-md text-xs font-medium uppercase"
                :class="{
                  'bg-green-100 text-green-700': program.difficulty_level === 'beginner',
                  'bg-yellow-100 text-yellow-700': program.difficulty_level === 'intermediate',
                  'bg-red-100 text-red-700': program.difficulty_level === 'advanced',
                }"
              >
                {{ program.difficulty_level }}
              </div>
            </div>

            <!-- Description -->
            <div class="text-gray-500 mb-4 text-sm leading-relaxed">
              {{ truncate(program.description, 120) || 'No description provided' }}
            </div>

            <!-- Metadata -->
            <div class="grid gap-2 mb-4 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500">Duration:</span>
                <span class="text-gray-700 font-medium">
                  {{ program.duration }} day{{ program.duration === 1 ? '' : 's' }}
                </span>
              </div>

              <div class="flex justify-between">
                <span class="text-gray-500">Category:</span>
                <span class="text-gray-700 font-medium">
                  {{ program.category_display || 'Not specified' }}
                </span>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex gap-2 flex-wrap">
              <button
                class="px-3 py-2 text-xs rounded-md bg-blue-600 text-white font-semibold hover:bg-blue-700 transition"
                @click="editProgram(program.id)"
              >
                Edit
              </button>

              <button
                class="px-3 py-2 text-xs rounded-md bg-red-500 text-white font-semibold hover:bg-red-600 transition"
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
import * as icons from 'lucide-vue-next'
import { useToastStore } from "@/stores/toast";

const router = useRouter()
const toast = useToastStore();

const loading = ref(true)
const showCreateProgram = ref(false)
const approvalStatus = ref('pending')
const programs = ref([])
const coachID = ref('')
const memberCount = ref(0)
const editingProgram = ref(null)
const pendingRequestCount = ref(0)
const copied = ref(false)
const API_URL = 'http://127.0.0.1:8000'

const { Clipboard } = icons

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
    copied.value = true

    setTimeout(() => {
      copied.value = false
    }, 1500)
  }
}

async function loadCoachStatus() {
  try {
    const res = await fetch(`${API_URL}/api/coach/status/`, {
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

const API_BASE = `${API_URL}/api/workout/programs/`

async function loadPrograms() {
  try {
    const res = await fetch(API_BASE, { credentials: 'include' })
    const data = await res.json()
    if (Array.isArray(data)) {
      programs.value = data
    } else if (data.results && Array.isArray(data.results)) {
      programs.value = data.results
    } else if (data.id) {
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
    memberCount.value = data.filter(r => r.status === 'accepted').length
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
    pendingRequestCount.value = data.filter(r => r.status === 'pending').length
    memberCount.value = data.filter(r => r.status === 'accepted').length
  } catch (err) {
    console.error('Failed to load pending requests', err)
    pendingRequestCount.value = 0
    memberCount.value = 0
  }
}

async function editProgram(programId) {
  router.push({
    path: '/create-workout-program',
    query: { edit: programId }
  })
}

async function deleteProgram(programId) {
  try {
    const res = await fetch(`${API_BASE}${programId}/delete/`, {
      method: 'DELETE',
      credentials: 'include',
    })

    if (res.ok) {
      await loadPrograms()
      if (editingProgram.value && editingProgram.value.id === programId) {
        editingProgram.value = null
        showCreateProgram.value = false
      }
      toast.success('Program deleted successfully!')
    } else {
      const text = await res.text()
      let body = text
      try {
        body = JSON.parse(text)
      } catch (err) {
        console.warn('Failed to parse response as JSON:', err)
      }
      console.error('Delete program failed:', res.status, body)

    }
  } catch (err) {
    console.error('Error deleting program:', err)
    toast.error('Failed to delete program')
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
