<template>
  <div class="member-requests">
    <div class="page-header">
      <button class="back-btn" @click="emit('back-to-dashboard')">
        ← Back to Dashboard
      </button>
      <div class="header-content">
        <h1 class="page-title">Member Requests</h1>
        <p class="page-subtitle">Review and manage membership requests from potential clients</p>
      </div>
      <div class="header-stats">
        <div class="stat-badge pending">
          <span class="stat-number">{{ pendingRequests.length }}</span>
          <span class="stat-label">Pending</span>
        </div>
        <div class="stat-badge approved">
          <span class="stat-number">{{ approvedRequests.length }}</span>
          <span class="stat-label">Approved</span>
        </div>
      </div>
    </div>

    <!-- Filter Tabs -->
    <div class="filter-tabs">
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'all' }"
        @click="activeTab = 'all'"
      >
        All Requests ({{ requests.length }})
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'pending' }"
        @click="activeTab = 'pending'"
      >
        Pending ({{ pendingRequests.length }})
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'approved' }"
        @click="activeTab = 'approved'"
      >
        Approved ({{ approvedRequests.length }})
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'rejected' }"
        @click="activeTab = 'rejected'"
      >
        Rejected ({{ rejectedRequests.length }})
      </button>
    </div>

    <!-- Requests List -->
    <div class="requests-container">
      <div v-if="filteredRequests.length === 0" class="empty-state">
        <div class="empty-icon">📋</div>
        <div class="empty-title">No {{ activeTab === 'all' ? '' : activeTab }} requests</div>
        <div class="empty-message">
          {{ activeTab === 'pending'
            ? 'All caught up! No pending requests at the moment.'
            : `You don't have any ${activeTab} requests.` }}
        </div>
      </div>

      <div v-else class="requests-grid">
        <div
          v-for="request in filteredRequests"
          :key="request.id"
          class="request-card"
        >
          <!-- Request Header -->
          <div class="request-header">
            <div class="member-info">
              <div class="member-avatar">
                {{ request.memberName.charAt(0).toUpperCase() }}
              </div>
              <div class="member-details">
                <div class="member-name">{{ request.memberName }}</div>
                <div class="member-email">{{ request.email }}</div>
              </div>
            </div>
            <div class="request-status" :class="request.status">
              {{ request.status }}
            </div>
          </div>

          <!-- Request Info -->
          <div class="request-info">
            <div class="info-row">
              <span class="info-label">Program:</span>
              <span class="info-value">{{ request.programName || 'Any Program' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Experience Level:</span>
              <span class="info-value">{{ request.experienceLevel }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Submitted:</span>
              <span class="info-value">{{ formatDate(request.submittedAt) }}</span>
            </div>
          </div>

          <!-- Request Message -->
          <div v-if="request.message" class="request-message">
            <div class="message-label">Message:</div>
            <div class="message-content">{{ request.message }}</div>
          </div>

          <!-- Goals -->
          <div v-if="request.goals && request.goals.length > 0" class="request-goals">
            <div class="goals-label">Goals:</div>
            <div class="goals-tags">
              <span
                v-for="goal in request.goals"
                :key="goal"
                class="goal-tag"
              >
                {{ goal }}
              </span>
            </div>
          </div>

          <!-- Actions -->
          <div class="request-actions">
            <template v-if="request.status === 'pending'">
              <button class="btn small success" @click="approveRequest(request.id)">
                ✓ Approve
              </button>
              <button class="btn small danger" @click="rejectRequest(request.id)">
                ✕ Reject
              </button>
              <button class="btn small ghost" @click="viewDetails(request)">
                View Details
              </button>
            </template>
            <template v-else>
              <button class="btn small ghost" @click="viewDetails(request)">
                View Details
              </button>
              <button v-if="request.status === 'approved'" class="btn small ghost" @click="contactMember(request)">
                Contact Member
              </button>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const emit = defineEmits<{
  (e: 'back-to-dashboard'): void
}>()

interface MemberRequest {
  id: string
  memberName: string
  email: string
  programName?: string
  experienceLevel: string
  message?: string
  goals?: string[]
  status: 'pending' | 'approved' | 'rejected'
  submittedAt: Date
}

const activeTab = ref<'all' | 'pending' | 'approved' | 'rejected'>('all')

// Sample data - in real app this would come from API
const requests = ref<MemberRequest[]>([
  {
    id: 'req_001',
    memberName: 'John Smith',
    email: 'john.smith@example.com',
    programName: 'Full Body Strength',
    experienceLevel: 'Beginner',
    message: 'I\'m looking to build strength and improve my overall fitness. I can train 3-4 times per week.',
    goals: ['Build Muscle', 'Lose Weight', 'Improve Endurance'],
    status: 'pending',
    submittedAt: new Date('2024-01-15')
  },
  {
    id: 'req_002',
    memberName: 'Sarah Johnson',
    email: 'sarah.j@example.com',
    programName: 'HIIT Training',
    experienceLevel: 'Intermediate',
    message: 'Looking for a challenging HIIT program to improve my cardio and lose fat.',
    goals: ['Lose Weight', 'Improve Endurance'],
    status: 'pending',
    submittedAt: new Date('2024-01-14')
  },
  {
    id: 'req_003',
    memberName: 'Mike Chen',
    email: 'mike.chen@example.com',
    experienceLevel: 'Advanced',
    message: 'Experienced lifter looking for an advanced strength program.',
    goals: ['Build Muscle', 'Increase Strength'],
    status: 'approved',
    submittedAt: new Date('2024-01-10')
  },
  {
    id: 'req_004',
    memberName: 'Emily Davis',
    email: 'emily.d@example.com',
    programName: 'Beginner Fitness',
    experienceLevel: 'Beginner',
    status: 'rejected',
    submittedAt: new Date('2024-01-08')
  }
])

const pendingRequests = computed(() =>
  requests.value.filter(r => r.status === 'pending')
)

const approvedRequests = computed(() =>
  requests.value.filter(r => r.status === 'approved')
)

const rejectedRequests = computed(() =>
  requests.value.filter(r => r.status === 'rejected')
)

const filteredRequests = computed(() => {
  if (activeTab.value === 'all') return requests.value
  return requests.value.filter(r => r.status === activeTab.value)
})

function formatDate(date: Date): string {
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'Today'
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays} days ago`

  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

function approveRequest(requestId: string) {
  const request = requests.value.find(r => r.id === requestId)
  if (request && confirm(`Approve membership request from ${request.memberName}?`)) {
    request.status = 'approved'
    alert(`Request approved! ${request.memberName} has been notified.`)
    // In real app: POST to API to approve request
  }
}

function rejectRequest(requestId: string) {
  const request = requests.value.find(r => r.id === requestId)
  if (request && confirm(`Reject membership request from ${request.memberName}?`)) {
    request.status = 'rejected'
    alert(`Request rejected. ${request.memberName} has been notified.`)
    // In real app: POST to API to reject request
  }
}

function viewDetails(request: MemberRequest) {
  alert(`View details for ${request.memberName}\n\nThis would open a detailed modal with full member information, history, and notes.`)
  // In real app: Open modal with detailed view
}

function contactMember(request: MemberRequest) {
  alert(`Contact ${request.memberName}\n\nEmail: ${request.email}\n\nThis would open your email client or messaging system.`)
  // In real app: Open messaging/email interface
}
</script>

<style scoped>
.member-requests {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  gap: 20px;
}

.header-content {
  flex: 1;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 8px 0;
}

.page-subtitle {
  color: #6b7280;
  font-size: 16px;
  margin: 0;
}

.header-stats {
  display: flex;
  gap: 12px;
}

.stat-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 16px;
  border-radius: 12px;
  min-width: 80px;
}

.stat-badge.pending {
  background: #fef3c7;
  border: 1px solid #f59e0b;
}

.stat-badge.approved {
  background: #d1fae5;
  border: 1px solid #10b981;
}

.stat-number {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  text-transform: uppercase;
}

.filter-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 0;
  flex-wrap: wrap;
}

.tab-btn {
  background: transparent;
  border: none;
  padding: 12px 20px;
  font-weight: 600;
  font-size: 14px;
  color: #6b7280;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s ease;
}

.tab-btn:hover {
  color: #374151;
}

.tab-btn.active {
  color: #3b82f6;
  border-bottom-color: #3b82f6;
}

.requests-container {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.empty-state {
  text-align: center;
  padding: 64px 24px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-title {
  font-size: 20px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.empty-message {
  color: #6b7280;
  line-height: 1.5;
}

.requests-grid {
  display: grid;
  gap: 16px;
}

.request-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  background: #fafafa;
  transition: all 0.2s ease;
}

.request-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59,130,246,0.1);
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.member-info {
  display: flex;
  gap: 12px;
  align-items: center;
  flex: 1;
}

.member-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 600;
  flex-shrink: 0;
}

.member-details {
  flex: 1;
  min-width: 0;
}

.member-name {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 2px;
}

.member-email {
  font-size: 14px;
  color: #6b7280;
}

.request-status {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  flex-shrink: 0;
}

.request-status.pending {
  background: #fef3c7;
  color: #92400e;
}

.request-status.approved {
  background: #d1fae5;
  color: #065f46;
}

.request-status.rejected {
  background: #fee2e2;
  color: #991b1b;
}

.request-info {
  display: grid;
  gap: 8px;
  margin-bottom: 16px;
  padding: 12px;
  background: #fff;
  border-radius: 8px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.info-label {
  color: #6b7280;
  font-weight: 500;
}

.info-value {
  color: #374151;
  font-weight: 600;
}

.request-message {
  margin-bottom: 16px;
  padding: 12px;
  background: #fff;
  border-radius: 8px;
  border-left: 3px solid #3b82f6;
}

.message-label {
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  margin-bottom: 6px;
}

.message-content {
  color: #374151;
  line-height: 1.5;
  font-size: 14px;
}

.request-goals {
  margin-bottom: 16px;
}

.goals-label {
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.goals-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.goal-tag {
  background: #ede9fe;
  color: #5b21b6;
  padding: 4px 10px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
}

.request-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.btn {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: 600;
  background: #fff;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
}

.btn:hover {
  background: #f9fafb;
}

.btn.small {
  padding: 6px 12px;
  font-size: 12px;
}

.btn.success {
  background: #10b981;
  color: #fff;
  border-color: #10b981;
}

.btn.success:hover {
  background: #059669;
}

.btn.danger {
  background: #ef4444;
  color: #fff;
  border-color: #ef4444;
}

.btn.danger:hover {
  background: #dc2626;
}

.btn.ghost {
  background: transparent;
  color: #374151;
}

.btn.ghost:hover {
  background: #f3f4f6;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
  }

  .header-stats {
    width: 100%;
    justify-content: space-around;
  }

  .filter-tabs {
    overflow-x: auto;
    scrollbar-width: none;
    -ms-overflow-style: none;
  }

  .filter-tabs::-webkit-scrollbar {
    display: none;
  }

  .tab-btn {
    white-space: nowrap;
  }

  .request-header {
    flex-direction: column;
    gap: 12px;
  }

  .request-status {
    align-self: flex-start;
  }

  .request-actions {
    flex-direction: column;
  }

  .btn.small {
    width: 100%;
  }
}
</style>
