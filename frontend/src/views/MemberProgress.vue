<template>
  <div class="max-w-[1200px] mx-auto p-6 text-[#134686]">
    <div class="max-w-7xl mx-auto">
      <!-- Back Button -->
      <button
        @click="$router.back()"
        class="inline-flex items-center justify-center p-2 border border-gray-300 rounded-lg mb-6 hover:bg-gray-100 transition"
      >
        <ArrowLeft class="w-5 h-5 text-gray-700 mr-2" />
        Back to Members
      </button>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div
          class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"
        ></div>
        <p class="mt-4 text-gray-600">Loading member details...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <p class="text-red-600">{{ error }}</p>
        <button
          @click="fetchMemberProgress"
          class="mt-4 px-4 py-2 bg-red-600 text-grey rounded-lg hover:bg-red-700"
        >
          Retry
        </button>
      </div>

      <!-- Member Details -->
      <div v-else>
        <!-- Member Header -->
        <div class="bg-[#fac3e1] rounded-xl shadow-md p-8 mb-6 relative overflow-hidden">
          <!-- Decorative circles -->
          <div
            class="absolute -top-10 -right-10 w-32 h-32 sm:w-40 sm:h-40 bg-white/20 rounded-full"
          ></div>
          <div
            class="absolute -bottom-10 -left-10 w-32 h-32 sm:w-40 sm:h-40 bg-white/20 rounded-full"
          ></div>
          <!-- Content (with relative positioning to stay above decorative circles) -->
          <div class="flex items-center gap-6 relative z-10">
            <!-- White circle background -->
            <div class="w-24 h-24 rounded-full bg-gray-200 overflow-hidden">
              <img
                v-if="memberInfo.photo"
                :src="memberInfo.photo"
                :alt="memberInfo.name"
                class="w-full h-full object-cover"
              />
              <div
                v-else
                class="w-full h-full flex items-center justify-center bg-gradient-to-br from-purple-400 to-pink-400"
              >
                <FileUser class="text-white w-12 h-12" />
              </div>
            </div>
            <div class="flex-1">
              <h1 class="text-3xl font-bold text-[#9c547b]">{{ memberInfo.name.toUpperCase() }}</h1>
              <div class="mt-2 flex gap-2">
                <span
                  class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
                  :class="{
                    'bg-[#7ED7C1] text-green-800': memberInfo.experience_level === 'beginner',
                    'bg-[#C2E2FA] text-blue-800': memberInfo.experience_level === 'intermediate',
                    'bg-[#B7A3E3] text-purple-800': memberInfo.experience_level === 'advanced',
                  }"
                >
                  {{
                    memberInfo.experience_level?.charAt(0).toUpperCase() +
                    memberInfo.experience_level?.slice(1)
                  }}
                </span>
                <span
                  class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-800"
                >
                  ID: {{ memberInfo.member_id }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Programs/Assignments -->
        <div v-if="programs.length === 0" class="bg-white rounded-xl shadow-md p-12 text-center">
          <p class="text-gray-500 mt-4">No workout programs assigned yet</p>
        </div>

        <div v-else class="space-y-6">
          <div
            v-for="program in programs"
            :key="program.program_id"
            class="bg-white rounded-xl shadow-md overflow-hidden"
          >
            <!-- Program Header -->
            <div class="bg-gradient-to-r bg-[#C2E2FA] p-6">
              <div class="flex items-center justify-between">
                <div>
                  <h2 class="text-2xl font-bold">{{ program.program_title }}</h2>
                  <p class="mt-1">{{ program.category }} • {{ program.difficulty_level }}</p>
                </div>
              </div>
              <div class="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <p class="text-sm">Progress</p>
                  <p class="font-medium text-lg">
                    {{ program.completed_workouts }} / {{ program.total_workouts }} workouts
                  </p>
                </div>
                <div>
                  <p class="text-sm">Completion</p>
                  <p class="font-medium text-lg">{{ program.completion_percentage }}%</p>
                </div>
                <div>
                  <p class="text-sm">XP Earned</p>
                  <p class="font-medium text-lg">{{ program.xp_earned }} XP</p>
                </div>
                <div>
                  <p class="text-sm">Status</p>
                  <span
                    class="inline-block px-3 py-1 rounded-full text-sm font-medium"
                    :class="{
                      'bg-[#7ED7C1]': program.assignment_status === 'completed',
                      'bg-yellow-300': program.assignment_status === 'in_progress',
                      'bg-[#EBD6FB]': program.assignment_status === 'assigned',
                      'bg-gray-500': program.assignment_status === 'paused',
                    }"
                  >
                    {{ program.assignment_status?.toUpperCase() || 'N/A' }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="px-6 pt-6">
              <div class="w-full bg-gray-200 rounded-full h-4 mb-2">
                <div
                  class="h-4 rounded-full transition-all duration-500"
                  :class="{
                    'bg-red-200': program.completion_percentage < 30,
                    'bg-yellow-200':
                      program.completion_percentage >= 30 && program.completion_percentage < 70,
                    'bg-green-200': program.completion_percentage >= 70,
                  }"
                  :style="{ width: `${program.completion_percentage}%` }"
                ></div>
              </div>
            </div>

            <!-- Completed Days -->
            <div class="p-6">
              <h3 class="text-lg font-semibold text-gray-800 mb-4">Completed Days</h3>
              <div
                v-if="program.completed_day_numbers && program.completed_day_numbers.length > 0"
                class="flex flex-wrap gap-2"
              >
                <span
                  v-for="dayNum in program.completed_day_numbers"
                  :key="dayNum"
                  class="inline-flex items-center justify-center w-10 h-10 bg-green-100 text-green-800 rounded-full font-semibold text-sm"
                >
                  {{ dayNum }}
                </span>
              </div>
              <p v-else class="text-gray-500 text-sm">No days completed yet</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, FileUser } from 'lucide-vue-next'
import { useToastStore } from '@/stores/toast'

const route = useRoute()
const toast = useToastStore()

const loading = ref(true)
const error = ref(null)
const memberInfo = ref({})
const programs = ref([])

const API_URL = 'http://127.0.0.1:8000'

const memberId = computed(() => {
  // Check route.params first
  if (route.params.memberId) {
    return route.params.memberId
  }
  // Check route.query as fallback
  if (route.query.memberId) {
    return route.query.memberId
  }
  return null
})

function getCsrfToken() {
  const value = `; ${document.cookie}`
  const parts = value.split(`; csrftoken=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
  return ''
}

function getFullPhotoUrl(photoPath) {
  if (!photoPath) return null

  // If already a full URL, return as is
  if (photoPath.startsWith('http://') || photoPath.startsWith('https://')) {
    return photoPath
  }

  // If it's a relative path, construct full URL
  if (photoPath.startsWith('/media/')) {
    return `${API_URL}${photoPath}`
  }

  return null
}

async function fetchMemberProgress() {
  loading.value = true
  error.value = null

  try {
    const currentMemberId = memberId.value
    if (!currentMemberId) {
      throw new Error('Member ID is missing from route')
    }

    // First, get member info from accepted members endpoint
    const memberResponse = await fetch(`${API_URL}/api/member/accepted/`, {
      credentials: 'include',
      headers: {
        'X-CSRFToken': getCsrfToken(),
      },
    })

    if (!memberResponse.ok) {
      throw new Error('Failed to fetch member info')
    }

    const members = await memberResponse.json()

    // Find member by memberId
    const member = members.find((m) => m.memberId === currentMemberId)

    if (!member) {
      throw new Error(`Member ${currentMemberId} not found in your accepted members list`)
    }

    memberInfo.value = {
      member_id: member.memberId,
      name: member.name,
      photo: getFullPhotoUrl(member.member_photo),
      experience_level: member.experienceLevel,
    }

    const assignmentsResponse = await fetch(
      `${API_URL}/api/member/member-assignments/${currentMemberId}/`,
      {
        credentials: 'include',
        headers: {
          'X-CSRFToken': getCsrfToken(),
        },
      },
    )

    if (!assignmentsResponse.ok) {
      programs.value = []
      return
    }

    const assignments = await assignmentsResponse.json()

    if (!assignments || assignments.length === 0) {
      programs.value = []
      return
    }

    const programsWithProgress = await Promise.all(
      assignments.map(async (assignment) => {
        try {
          const progressResponse = await fetch(
            `${API_URL}/api/member/member-progress/${assignment.program.id}/${currentMemberId}/`,
            {
              credentials: 'include',
              headers: {
                'X-CSRFToken': getCsrfToken(),
              },
            },
          )

          if (!progressResponse.ok) {
            return {
              program_id: assignment.program.id,
              program_title: assignment.program.title,
              category: assignment.program.category,
              difficulty_level: assignment.program.difficulty_level,
              total_workouts: 0,
              completed_workouts: 0,
              completion_percentage: 0,
              xp_earned: 0,
              completed_day_numbers: [],
              assignment_status: assignment.status,
            }
          }

          const progress = await progressResponse.json()

          return {
            program_id: progress.program_id,
            program_title: progress.program_title,
            category: assignment.program.category,
            difficulty_level: assignment.program.difficulty_level,
            total_workouts: progress.total_workouts,
            completed_workouts: progress.completed_workouts,
            completion_percentage: progress.completion_percentage,
            xp_earned: progress.xp_earned,
            completed_day_numbers: progress.completed_day_numbers,
            assignment_status: assignment.status,
            member: progress.member,
          }
        } catch {
          return null
        }
      }),
    )

    programs.value = programsWithProgress.filter((p) => p !== null)
  } catch {
    toast.error('Failed to load member progress')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchMemberProgress()
})
</script>
