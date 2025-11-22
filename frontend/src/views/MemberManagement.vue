<template>
  <div class="max-w-[1200px] mx-auto p-6">
    <!-- Back Button -->
    <button
      @click="goBackToDashboard"
      class="inline-flex items-center justify-center p-2 border border-gray-300 bg-white rounded-lg mb-6 hover:bg-gray-100 transition"
    >
      <ArrowLeft class="w-5 h-5 text-gray-700 mr-2" />
      Back to Dashboard
    </button>

    <!-- Header -->
    <div class="flex justify-between items-start mb-6">
      <div class="flex-1">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Member Management</h1>
        <p class="text-gray-500 text-base">View and manage members who have been accepted</p>
      </div>
      <div class="flex gap-3">
        <div class="flex flex-col items-center py-3 px-4 rounded-xl bg-green-100 border border-green-500">
          <span class="text-2xl font-bold">{{ members.length }}</span>
          <span class="text-xs uppercase text-gray-600">Active Members</span>
        </div>
      </div>
    </div>

    <!-- Members List -->
    <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-16 px-6">
        Loading members...
      </div>

      <!-- No Members -->
      <div v-else-if="members.length === 0" class="text-center py-16 px-6">
        <FileUser class="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <div class="text-xl font-semibold text-gray-700 mb-3">No active members</div>
        <div class="text-gray-600">Start approving member requests to see them here.</div>
      </div>

      <!-- Members Grid -->
      <div v-else class="grid gap-4">
        <div
          v-for="member in members"
          :key="member.memberId"
          class="border border-gray-200 rounded-xl p-5 bg-gray-50"
        >
          <!-- Member Header -->
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

          <!-- Member Details -->
          <div class="grid gap-2 mb-4 p-3 bg-white rounded-lg border border-gray-100 shadow-sm">
            <div class="flex justify-between text-sm">
              <span class="text-gray-500 font-medium">Level:</span>
              <span class="font-semibold text-gray-800">
                {{ member.experienceLevel ? member.experienceLevel.charAt(0).toUpperCase() + member.experienceLevel.slice(1) : 'Not specified' }}
              </span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-500 font-medium">Joined:</span>
              <span class="font-semibold text-gray-800">{{ formatDate(member.joinedAt) }}</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-500 font-medium">Assigned Program:</span>
              <span class="font-semibold text-gray-800">{{ member.programName || 'Not specified' }}</span>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-2 flex-wrap pt-4 border-t border-gray-200">
            <button
              class="border border-gray-300 rounded-lg px-3 py-1.5 text-xs font-semibold hover:bg-gray-50 transition-all"
              @click="viewDetails(member)"
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

    <!-- Delete Modal -->
    <DeleteModal
      v-model:show="showRemoveModal"
      title="Remove Member"
      message="Are you sure you want to remove this member?"
      confirmText="Remove"
      cancelText="Cacel"
      @confirm="confirmRemoveMember"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, FileUser } from 'lucide-vue-next'
import { useToastStore } from '@/stores/toast'
import MemberDetailModal from '@/components/MemberDetailModal.vue'
import DeleteModal from '@/components/DeleteModal.vue'

const router = useRouter()
const toast = useToastStore()

const members = ref([])
const loading = ref(true)

const showDetailModal = ref(false)
const selectedMemberId = ref(null)

const showRemoveModal = ref(false)
const memberToRemove = ref(null)

// Helpers
function getImageUrl(path) {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `http://127.0.0.1:8000${path}`
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

// Navigation
function goBackToDashboard() {
  router.push('/coach-dashboard')
}

// Member Actions
function viewDetails(member) {
  selectedMemberId.value = member.memberId
  showDetailModal.value = true
}

function closeDetailModal() {
  showDetailModal.value = false
  selectedMemberId.value = null
}

function viewFoodDiary(member) {
  router.push(`/food-diary/${member.memberId}`)
}

// Remove Member
function removeMember(member) {
  memberToRemove.value = member
  showRemoveModal.value = true
}

async function confirmRemoveMember() {
  if (!memberToRemove.value) return
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/member/${memberToRemove.value.memberId}/`, {
      method: 'DELETE',
      credentials: 'include'
    })
    if (!res.ok) throw new Error('Failed to remove member')
    members.value = members.value.filter(m => m.memberId !== memberToRemove.value.memberId)
    memberToRemove.value = null
    toast.success('Member removed successfully')
  } catch (err) {
    console.error(err)
    toast.error('Failed to remove member')
  } finally {
    showRemoveModal.value = false
  }
}

// Load members from API
async function loadMembers() {
  loading.value = true
  try {
    const res = await fetch('http://127.0.0.1:8000/api/member/accepted/', { credentials: 'include' })
    if (!res.ok) throw new Error('Failed to fetch members')
    const data = await res.json()
    members.value = data
  } catch (err) {
    console.error(err)
    members.value = []
    toast.error('Failed to load members')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadMembers()
})
</script>
