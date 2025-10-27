<template>
  <div class="notification-bell" ref="bellContainer">
    <!-- Bell Icon with Badge -->
    <button
      class="bell-button"
      @click="toggleDropdown"
      :class="{ 'has-notifications': totalCount > 0 }"
    >
      <span class="bell-icon">🔔</span>
      <span v-if="totalCount > 0" class="notification-badge">
        {{ totalCount > 99 ? '99+' : totalCount }}
      </span>
    </button>

    <!-- Notification Dropdown -->
    <transition name="dropdown">
      <div v-if="showDropdown" class="notification-dropdown">
        <!-- Header -->
        <div class="dropdown-header">
          <h3 class="dropdown-title">Notifications</h3>
          <button @click="closeDropdown" class="close-btn">×</button>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading notifications...</p>
        </div>

        <!-- Notifications List -->
        <div v-else-if="hasNotifications" class="notifications-list">
          <!-- Member Requests Section -->
          <div v-if="pendingRequests.length > 0" class="notification-section">
            <div class="section-header">
              <span class="section-icon">👥</span>
              <span class="section-title">Member Requests</span>
              <span class="section-count">{{ pendingRequests.length }}</span>
            </div>
            <div
              v-for="request in pendingRequests"
              :key="'request-' + request.relationship_id"
              class="notification-item"
              @click="goToMemberRequests"
            >
              <div class="notification-icon member-request">👤</div>
              <div class="notification-content">
                <p class="notification-text">
                  <strong>{{ request.memberName }}</strong> wants you as their coach
                </p>
                <span class="notification-time">{{ formatTime(request.submittedAt) }}</span>
              </div>
            </div>
          </div>

          <!-- Pending Feedback Section -->
          <div v-if="pendingFeedback.length > 0" class="notification-section">
            <div class="section-header">
              <span class="section-icon">🍽️</span>
              <span class="section-title">Food Posts Need Feedback</span>
              <span class="section-count">{{ pendingFeedback.length }}</span>
            </div>
            <div
              v-for="post in pendingFeedback"
              :key="'post-' + post.id"
              class="notification-item"
              @click="goToFoodDiary(post.member_id)"
            >
              <div class="notification-icon food-post">🍴</div>
              <div class="notification-content">
                <p class="notification-text">
                  <strong>{{ post.member_name }}</strong> posted "{{ post.title }}"
                </p>
                <span class="notification-time">{{ formatTime(post.created_at) }}</span>
              </div>
              <img
                v-if="post.image"
                :src="post.image"
                class="notification-thumbnail"
                alt="Food thumbnail"
              />
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <div class="empty-icon">🔕</div>
          <p class="empty-text">No new notifications</p>
        </div>

        <!-- Footer -->
        <div class="dropdown-footer">
          <button @click="goToViewAll" class="view-all-btn">
            View All Activity
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

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

const goToViewAll = () => {
  closeDropdown()
  router.push('/view-member')
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

<style scoped>
.notification-bell {
  position: relative;
}

.bell-button {
  position: relative;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bell-button:hover {
  background: rgba(59, 130, 246, 0.1);
}

.bell-button.has-notifications {
  animation: ring 2s ease-in-out infinite;
}

@keyframes ring {
  0%, 100% { transform: rotate(0deg); }
  10%, 30% { transform: rotate(-10deg); }
  20%, 40% { transform: rotate(10deg); }
}

.bell-icon {
  font-size: 24px;
  display: block;
}

.notification-badge {
  position: absolute;
  top: 2px;
  right: 2px;
  background: #ef4444;
  color: white;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 5px;
  border-radius: 10px;
  min-width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

/* Dropdown */
.notification-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 400px;
  max-height: 600px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.15);
  overflow: hidden;
  z-index: 1000;
  display: flex;
  flex-direction: column;
}

/* Dropdown Animation */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

/* Header */
.dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e5e7eb;
}

.dropdown-title {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  color: #6b7280;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: background 0.2s;
}

.close-btn:hover {
  background: #f3f4f6;
}

/* Loading */
.loading-state {
  padding: 40px 20px;
  text-align: center;
  color: #6b7280;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 12px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Notifications List */
.notifications-list {
  overflow-y: auto;
  max-height: 500px;
}

.notification-section {
  border-bottom: 1px solid #e5e7eb;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.section-icon {
  font-size: 16px;
}

.section-title {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  flex: 1;
}

.section-count {
  background: #3b82f6;
  color: white;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 10px;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px 20px;
  cursor: pointer;
  transition: background 0.2s;
  border-bottom: 1px solid #f3f4f6;
}

.notification-item:hover {
  background: #f9fafb;
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.notification-icon.member-request {
  background: #dbeafe;
}

.notification-icon.food-post {
  background: #fef3c7;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-text {
  color: #374151;
  font-size: 14px;
  line-height: 1.5;
  margin: 0 0 4px 0;
}

.notification-text strong {
  color: #111827;
  font-weight: 600;
}

.notification-time {
  color: #9ca3af;
  font-size: 12px;
}

.notification-thumbnail {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  object-fit: cover;
  flex-shrink: 0;
}

/* Empty State */
.empty-state {
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.empty-text {
  color: #6b7280;
  font-size: 15px;
  margin: 0;
}

/* Footer */
.dropdown-footer {
  padding: 12px 20px;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

.view-all-btn {
  width: 100%;
  background: transparent;
  border: none;
  color: #3b82f6;
  font-weight: 600;
  font-size: 14px;
  padding: 8px;
  cursor: pointer;
  border-radius: 6px;
  transition: background 0.2s;
}

.view-all-btn:hover {
  background: #eff6ff;
}

/* Responsive */
@media (max-width: 480px) {
  .notification-dropdown {
    width: 100vw;
    max-width: 400px;
    right: -20px;
  }
}
</style>
