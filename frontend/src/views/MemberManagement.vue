<template>
  <div class="max-w-[1200px] mx-auto p-6">
    <button
      @click="goBackToDashboard"
      class="inline-flex items-center justify-center p-2 border border-gray-300 rounded-lg mb-6 hover:bg-gray-100 transition"
    >
      <ArrowLeft class="w-5 h-5 text-gray-700 mr-2" />
      Back to Dashboard
    </button>

    <div class="flex justify-between items-start mb-6">
      <div class="flex-1">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Member Management</h1>
        <p class="text-gray-500 text-base">View and manage members who have been accepted</p>
      </div>
      <div class="flex gap-3">
        <div
          class="flex flex-col items-center py-3 px-4 rounded-xl bg-green-100 border border-green-500"
        >
          <span class="text-2xl font-bold">{{ members.length }}</span>
          <span class="text-xs uppercase text-gray-600">Active Members</span>
        </div>
      </div>
    </div>

    <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
      <div v-if="loading" class="text-center py-16 px-6">Loading members...</div>

      <div v-else-if="members.length === 0" class="text-center py-16 px-6">
        <FileUser class="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <div class="text-xl font-semibold text-gray-700 mb-3">No active members</div>
        <div class="text-gray-600">Start approving member requests to see them here.</div>
      </div>

      <div v-else class="grid gap-4">
        <div
          v-for="member in members"
          :key="member.memberId"
          class="border border-gray-200 rounded-xl p-5 bg-gray-50"
        >
          <div class="flex flex-col md:flex-row justify-between items-center gap-3 mb-4">
            <div class="flex items-center gap-3 flex-1 min-w-0">
              <div
                class="w-12 h-12 rounded-full flex items-center justify-center font-semibold text-lg flex-shrink-0"
                :class="!member.member_photo ? 'bg-gradient-to-br from-purple-500 to-indigo-500 text-white' : ''"
              >
                <template v-if="member.member_photo">
                  <img :src="getImageUrl(member.member_photo)" alt="Profile" class="w-full h-full object-cover rounded-full" />
                </template>
                <template v-else>
                  {{ (member.name || '').charAt(0).toUpperCase() }}
                </template>
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-lg font-semibold text-gray-900 mb-1 truncate">{{ member.name }}</div>
                <div class="text-sm font-semibold text-blue-500 font-mono truncate">ID: {{ member.memberId }}</div>
              </div>
            </div>
            <div class="px-3 py-1.5 rounded-full bg-green-100 text-green-800 text-xs font-semibold self-start">ACTIVE</div>
          </div>

          <div class="grid gap-2 mb-4 p-3 bg-white rounded-lg border border-gray-100 shadow-sm">
            <div class="flex justify-between text-sm">
              <span class="text-gray-500 font-medium">Level:</span>
              <span class="font-semibold text-gray-800">
                {{
                  member.experienceLevel
                    ? member.experienceLevel.charAt(0).toUpperCase() +
                      member.experienceLevel.slice(1)
                    : 'Not specified'
                }}
              </span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-500 font-medium">Joined:</span>
              <span class="font-semibold text-gray-800">{{ formatDate(member.joinedAt) }}</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-500 font-medium">Assigned Program:</span>
              <span class="font-semibold text-gray-800">{{
                member.programName || 'Not specified'
              }}</span>
            </div>
          </div>

          <div class="flex gap-2 flex-wrap pt-4 border-t border-gray-200">
            <button
              class="border border-gray-300 rounded-lg px-3 py-1.5 text-xs font-semibold hover:bg-gray-50 transition-all"
              @click="viewProgress(member)"
            >
              View Details
            </button>
            <button
              class="border border-gray-300 rounded-lg px-3 py-1.5 text-xs font-semibold hover:bg-gray-50 transition-all"
              @click="viewFoodDiary(member)"
            >
              View Food Diary
            </button>
            <button
              class="bg-red-500 text-white border-red-500 rounded-lg px-3 py-1.5 text-xs font-semibold hover:bg-red-600 transition-all"
              @click="removeMember(member)"
            >
              Remove
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Member Detail Modal -->
    <MemberDetailModal
      :show="showDetailModal"
      :member-id="selectedMemberId"
      @close="closeDetailModal"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, FileUser } from 'lucide-vue-next'
import { useToastStore } from '@/stores/toast'
import MemberDetailModal from '@/components/MemberDetailModal.vue'

const router = useRouter()
const members = ref([])
const loading = ref(true)
const toast = useToastStore()
const API_BASE = 'http://127.0.0.1:8000/api/member/'
const showDetailModal = ref(false)
const selectedMemberId = ref(null)

function getImageUrl(path) {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `http://127.0.0.1:8000${path}`
}

function goBackToDashboard() {
  router.push('/coach-dashboard')
}

function closeDetailModal() {
  showDetailModal.value = false
  selectedMemberId.value = null
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

async function loadMembers() {
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}accepted/`, {
      credentials: 'include',
    })
    if (!res.ok) throw new Error('Failed to fetch members')
    const data = await res.json()
    members.value = data
  } catch (err) {
    console.error(err)
    members.value = []
  } finally {
    loading.value = false
  }
}

function viewFoodDiary(member) {
  router.push(`/food-diary/${member.memberId}`)
}

function viewProgress(member) {
  router.push(`/member-progress?memberId=${member.memberId}`)
}

async function removeMember(member) {
  if (!confirm(`Remove ${member.name} from your members?`)) return
  try {
    const res = await fetch(`${API_BASE}${member.memberId}/`, {
      method: 'DELETE',
      credentials: 'include',
    })
    if (!res.ok) throw new Error('Failed to remove')
    members.value = members.value.filter((m) => m.memberId !== member.memberId)
  } catch (err) {
    console.error(err)
    toast.error('Failed to remove member')
  }
}

onMounted(() => {
  loadMembers()
})
</script>
