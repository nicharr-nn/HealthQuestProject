<template>
  <div class="relative" ref="bellContainer">
    <!-- Bell Icon with Badge -->
    <button
      @click="toggleDropdown"
      :class="[
        'relative p-2 rounded-full flex items-center justify-center transition-all hover:bg-blue-100',
        totalCount > 0 ? 'animate-bounce' : ''
      ]"
    >
      <icons.Bell class="w-6 h-6 text-gray-700" />
      <span
        v-if="totalCount > 0"
        class="absolute top-0 right-0 bg-red-500 text-white text-xs font-bold px-1.5 h-4 min-w-[18px] flex items-center justify-center rounded-full shadow"
      >
        {{ totalCount > 99 ? '99+' : totalCount }}
      </span>
    </button>

    <!-- Notification Dropdown -->
    <transition name="dropdown">
      <div
        v-if="showDropdown"
        class="absolute right-0 mt-2 w-[400px] max-h-[600px] bg-white rounded-xl shadow-xl flex flex-col overflow-hidden z-50"
      >
        <!-- Header -->
        <div class="flex justify-between items-center px-5 py-4 border-b border-gray-200">
          <h3 class="text-lg font-bold text-gray-900 m-0">Notifications</h3>
          <button
            @click="closeDropdown"
            class="w-8 h-8 flex items-center justify-center rounded-md text-gray-500 hover:bg-gray-100 transition"
          >
            <icons.X class="w-5 h-5" />
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="py-10 text-center text-gray-500">
          <div class="w-8 h-8 border-4 border-gray-200 border-t-blue-500 rounded-full animate-spin mx-auto mb-3"></div>
          <p>Loading notifications...</p>
        </div>

        <!-- Notifications List -->
        <div v-else-if="hasNotifications" class="overflow-y-auto max-h-[500px]">
          <!-- Member Requests Section -->
          <div v-if="pendingRequests.length > 0" class="border-b border-gray-200">
            <div class="flex items-center gap-2 px-5 py-3 bg-gray-50 border-b border-gray-200">
              <icons.Users class="w-4 h-4 text-gray-700" />
              <span class="text-xs font-semibold text-gray-700 uppercase flex-1">Member Requests</span>
              <span class="bg-blue-500 text-white text-[11px] font-bold px-2 py-0.5 rounded-full">
                {{ pendingRequests.length }}
              </span>
            </div>
            <div
              v-for="request in pendingRequests"
              :key="'request-' + request.relationship_id"
              @click="goToMemberRequests"
              class="flex items-start gap-3 px-5 py-4 cursor-pointer border-b last:border-b-0 hover:bg-gray-50"
            >
              <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                <icons.User class="w-5 h-5 text-blue-500" />
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-gray-700 text-sm mb-1">
                  <strong class="text-gray-900 font-semibold">{{ request.memberName }}</strong> wants you as their coach
                </p>
                <span class="text-gray-400 text-xs">{{ formatTime(request.submittedAt) }}</span>
              </div>
            </div>
          </div>

          <!-- Pending Feedback Section -->
          <div v-if="pendingFeedback.length > 0" class="border-b border-gray-200">
            <div class="flex items-center gap-2 px-5 py-3 bg-gray-50 border-b border-gray-200">
              <icons.SpoonKnife class="w-4 h-4 text-gray-700" />
              <span class="text-xs font-semibold text-gray-700 uppercase flex-1">Food Posts Need Feedback</span>
              <span class="bg-blue-500 text-white text-[11px] font-bold px-2 py-0.5 rounded-full">
                {{ pendingFeedback.length }}
              </span>
            </div>
            <div
              v-for="post in pendingFeedback"
              :key="'post-' + post.id"
              @click="goToFoodDiary(post.member_id)"
              class="flex items-start gap-3 px-5 py-4 cursor-pointer border-b last:border-b-0 hover:bg-gray-50"
            >
              <div class="w-10 h-10 bg-yellow-100 rounded-full flex items-center justify-center flex-shrink-0">
                <icons.SpoonKnife class="w-5 h-5 text-yellow-500" />
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-gray-700 text-sm mb-1">
                  <strong class="text-gray-900 font-semibold">{{ post.member_name }}</strong> posted "{{ post.title }}"
                </p>
                <span class="text-gray-400 text-xs">{{ formatTime(post.created_at) }}</span>
              </div>
              <img
                v-if="post.image"
                :src="post.image"
                class="w-12 h-12 rounded-lg object-cover flex-shrink-0"
                alt="Food thumbnail"
              />
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="py-16 text-center">
          <icons.BellOff class="w-12 h-12 text-gray-400 mx-auto mb-3" />
          <p class="text-gray-500 text-sm m-0">No new notifications</p>
        </div>
      </div>
    </transition>
  </div>
</template>


<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import * as icons from 'lucide-vue-next'

const router = useRouter()

// State
const showDropdown = ref(false)
const loading = ref(false)
const pendingRequests = ref([])
const pendingFeedback = ref([])
const bellContainer = ref(null)

// Computed
const totalCount = computed(() => {
  return pendingRequests.value.length + pendingFeedback.value.length
})

const hasNotifications = computed(() => {
  return totalCount.value > 0
})

// Methods
const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
  if (showDropdown.value) {
    loadNotifications()
  }
}

const closeDropdown = () => {
  showDropdown.value = false
}

const loadNotifications = async () => {
  loading.value = true
  try {
    await Promise.all([
      loadPendingRequests(),
      loadPendingFeedback()
    ])
  } finally {
    loading.value = false
  }
}

const loadPendingRequests = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/member/coach-requests/', {
      credentials: 'include'
    })
    if (!res.ok) throw new Error('Failed to fetch requests')
    const data = await res.json()
    pendingRequests.value = data.filter((r) => r.status === 'pending')
  } catch (err) {
    console.error('Failed to load pending requests', err)
    pendingRequests.value = []
  }
}

const loadPendingFeedback = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/member/food-posts/pending-feedback/', {
      credentials: 'include'
    })
    if (!res.ok) throw new Error('Failed to fetch pending feedback')
    const data = await res.json()
    pendingFeedback.value = data.posts || []
  } catch (err) {
    console.error('Failed to load pending feedback', err)
    pendingFeedback.value = []
  }
}

const formatTime = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diffInSeconds = Math.floor((now - date) / 1000)

  if (diffInSeconds < 60) return 'Just now'
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`
  if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}d ago`

  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

// Navigation
const goToMemberRequests = () => {
  closeDropdown()
  router.push('/view-request')
}

const goToFoodDiary = (memberId) => {
  closeDropdown()
  router.push(`/food-diary/${memberId}`)
}

// Click outside to close
const handleClickOutside = (event) => {
  if (bellContainer.value && !bellContainer.value.contains(event.target)) {
    closeDropdown()
  }
}

// Lifecycle
onMounted(() => {
  loadNotifications()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Auto-refresh every 30 seconds
const refreshInterval = setInterval(() => {
  if (!showDropdown.value) {
    loadNotifications()
  }
}, 30000)

onUnmounted(() => {
  clearInterval(refreshInterval)
})
</script>
