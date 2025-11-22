<template>
  <div class="max-w-[1200px] mx-auto p-6">
    <button
      @click="goBackToDashboard"
      class="inline-flex items-center justify-center p-2 border border-gray-300 bg-white rounded-lg mb-6 hover:bg-gray-100 transition"
    >
      <ArrowLeft class="w-5 h-5 text-gray-700 mr-2" />
      Back to Dashboard
    </button>

    <!-- Page Header -->
    <div class="flex flex-col md:flex-row justify-between gap-5 mb-6">
      <div class="flex-1">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Member Requests</h1>
        <p class="text-gray-500 text-base">Review and manage membership requests</p>
      </div>

      <div class="flex gap-3">
        <div
          class="flex flex-col items-center px-4 py-3 rounded-xl min-w-[80px] border"
          :class="{ 'bg-yellow-100 border-yellow-400': true }"
        >
          <span class="text-2xl font-bold text-gray-900">{{ pendingRequests.length }}</span>
          <span class="text-xs font-medium text-gray-500 uppercase">Pending</span>
        </div>
        <div
          class="flex flex-col items-center px-4 py-3 rounded-xl min-w-[80px] border"
          :class="{ 'bg-green-100 border-green-400': true }"
        >
          <span class="text-2xl font-bold text-gray-900">{{ acceptedRequests.length }}</span>
          <span class="text-xs font-medium text-gray-500 uppercase">Accepted</span>
        </div>
      </div>
    </div>

    <!-- Filter Tabs -->
    <div class="flex flex-wrap gap-2 mb-6 border-b-2 border-gray-200">
      <button
        class="px-5 py-3 text-sm font-semibold text-gray-500 border-b-2 border-transparent hover:text-gray-700 transition"
        :class="{ 'text-blue-500 border-blue-500': activeTab === 'all' }"
        @click="activeTab = 'all'"
      >
        All Requests ({{ requests.length }})
      </button>
      <button
        class="px-5 py-3 text-sm font-semibold text-gray-500 border-b-2 border-transparent hover:text-gray-700 transition"
        :class="{ 'text-blue-500 border-blue-500': activeTab === 'pending' }"
        @click="activeTab = 'pending'"
      >
        Pending ({{ pendingRequests.length }})
      </button>
      <button
        class="px-5 py-3 text-sm font-semibold text-gray-500 border-b-2 border-transparent hover:text-gray-700 transition"
        :class="{ 'text-blue-500 border-blue-500': activeTab === 'accepted' }"
        @click="activeTab = 'accepted'"
      >
        Accepted ({{ acceptedRequests.length }})
      </button>
      <button
        class="px-5 py-3 text-sm font-semibold text-gray-500 border-b-2 border-transparent hover:text-gray-700 transition"
        :class="{ 'text-blue-500 border-blue-500': activeTab === 'rejected' }"
        @click="activeTab = 'rejected'"
      >
        Rejected ({{ rejectedRequests.length }})
      </button>
    </div>

    <!-- Requests List -->
    <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
      <div v-if="loading" class="text-center py-16">Loading requests...</div>

      <div v-else-if="filteredRequests.length === 0" class="text-center py-16">
        <clipboard-pen class="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <div class="text-xl font-semibold text-gray-700 mb-2">
          No {{ activeTab === 'all' ? '' : activeTab }} requests
        </div>
        <div class="text-gray-500 leading-relaxed">
          {{
            activeTab === 'pending'
              ? 'No pending requests at the moment.'
              : `You don't have any ${activeTab} requests.`
          }}
        </div>
      </div>

      <div v-else class="grid gap-4">
        <div
          v-for="request in filteredRequests"
          :key="request.id"
          class="bg-gray-50 border border-gray-200 rounded-xl p-5 hover:border-blue-500 hover:shadow-md transition"
        >
          <!-- Request Header -->
          <div class="flex flex-col md:flex-row justify-between items-center gap-3 mb-4">
          <div class="flex items-center gap-3 flex-1 min-w-0">
              <div
                class="w-12 h-12 rounded-full flex items-center justify-center font-semibold text-lg flex-shrink-0"
                :class="!request.member_photo ? 'bg-gradient-to-br from-purple-500 to-indigo-500 text-white' : ''"
              >
                <template v-if="request.member_photo">
                  <img :src="getImageUrl(request.member_photo)" alt="Profile" class="w-full h-full object-cover rounded-full" />
                </template>
                <template v-else>
                  {{ (request.memberName || '').charAt(0).toUpperCase() }}
                </template>
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-lg font-semibold text-gray-900 mb-1 truncate">
                  {{ request.memberName }}
                </div>
                <div class="text-sm font-semibold text-blue-500 font-mono truncate">
                  ID: {{ request.memberId }}
                </div>
              </div>
            </div>

            <div
              class="inline-flex items-center justify-center px-3 py-1 rounded-full text-xs font-semibold uppercase whitespace-nowrap flex-shrink-0"
              :class="{
                'bg-yellow-100 text-yellow-800': request.status === 'pending',
                'bg-green-100 text-green-800': request.status === 'accepted',
                'bg-red-100 text-red-800': request.status === 'rejected',
              }"
            >
              {{ request.status }}
            </div>
          </div>

          <!-- Request Info -->
          <div class="grid gap-2 mb-4 p-3 bg-white rounded-lg">
            <div class="flex justify-between text-sm">
              <span class="text-gray-500 font-medium">Experience Level:</span>
              <span class="text-gray-800 font-semibold">{{
                request.experienceLevel
                  ? request.experienceLevel.charAt(0).toUpperCase() +
                    request.experienceLevel.slice(1)
                  : 'Not specified'
              }}</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-500 font-medium">Submitted:</span>
              <span class="text-gray-800 font-semibold">{{ formatDate(request.submittedAt) }}</span>
            </div>
          </div>

          <!-- Goals -->
          <div v-if="request.goals?.length" class="mb-4">
            <div class="text-xs font-semibold text-gray-500 uppercase mb-2">Goals:</div>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="goal in [...new Set(request.goals)]"
                :key="goal"
                class="bg-purple-100 text-purple-800 px-2.5 py-1 rounded-full text-xs font-medium"
              >
                {{ goal }}
              </span>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex flex-wrap gap-2 pt-4 border-t border-gray-200">
            <template v-if="request.status === 'pending'">
              <button class="px-3 py-1.5 text-xs font-semibold rounded bg-green-500 text-white hover:bg-green-600 transition" @click="updateRequestStatus(request.relationship_id, 'accepted')">Accept</button>
              <button class="px-3 py-1.5 text-xs font-semibold rounded bg-red-500 text-white hover:bg-red-600 transition" @click="updateRequestStatus(request.relationship_id, 'rejected')">Reject</button>
              <button class="px-3 py-1.5 text-xs font-semibold rounded bg-transparent border border-gray-300 text-gray-700 hover:bg-gray-100 transition" @click="viewDetails(request)">View Details</button>
            </template>
            <template v-else>
              <button
                class="px-3 py-1.5 text-xs font-semibold rounded bg-transparent border border-gray-300 text-gray-700 hover:bg-gray-100 transition cursor-pointer"
                @click="viewDetails(request)"
              >
                View Details
              </button>
            </template>
          </div>
        </div>
      </div>
    </div>
    <MemberDetailModal
      :show="showDetailModal"
      :member-id="selectedMemberId"
      @close="closeDetailModal"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, ClipboardPen } from 'lucide-vue-next'
import { useToastStore } from '@/stores/toast'
import MemberDetailModal from '@/components/MemberDetailModal.vue'

const toast = useToastStore()
const router = useRouter()
const requests = ref([])
const activeTab = ref('all')
const loading = ref(true)
const API_URL = 'http://127.0.0.1:8000'

const pendingRequests = computed(() => requests.value.filter((r) => r.status === 'pending'))
const acceptedRequests = computed(() => requests.value.filter((r) => r.status === 'accepted'))
const rejectedRequests = computed(() => requests.value.filter((r) => r.status === 'rejected'))
const filteredRequests = computed(() =>
  activeTab.value === 'all'
    ? requests.value
    : requests.value.filter((r) => r.status === activeTab.value),
)

const showDetailModal = ref(false)
const selectedMemberId = ref(null)

function closeDetailModal() {
  showDetailModal.value = false
  selectedMemberId.value = null
}

function getImageUrl(path) {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `${API_URL}${path}`
}


function goBackToDashboard() {
  router.push('/coach-dashboard')
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'Today'
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

async function loadRequests() {
  loading.value = true
  try {
    const res = await fetch(`${API_URL}/api/member/coach-requests/`, { credentials: 'include' })
    if (!res.ok) throw new Error('Failed to fetch')
    const data = await res.json()
    requests.value = data
  } catch (err) {
    console.error(err)
    requests.value = []
  } finally {
    loading.value = false
  }
}

async function updateRequestStatus(relationshipId, status) {
  try {
    const res = await fetch(`${API_URL}/api/member/coach-requests/${relationshipId}/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ status }),
    })

    if (!res.ok) throw new Error('Failed to update status')

    const req = requests.value.find((r) => r.relationship_id === relationshipId)
    if (req) req.status = status
  } catch (err) {
    console.error(err)
    toast.error('Failed to update request status')
  }
}

function viewDetails(request) {
  selectedMemberId.value = request.memberId
  showDetailModal.value = true
}


onMounted(() => {
  loadRequests()
})
</script>
