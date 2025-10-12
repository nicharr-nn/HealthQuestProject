<template>
  <div class="member-management">
    <button class="back-btn" @click="emit('back-to-dashboard')">
      ← Back to Dashboard
    </button>

    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">My Members</h1>
        <p class="page-subtitle">Manage and track your approved members</p>
      </div>
      <div class="header-stats">
        <div class="stat-badge">
          <span class="stat-number">{{ members.length }}</span>
          <span class="stat-label">Total Members</span>
        </div>
      </div>
    </div>

    <!-- Members List -->
    <div class="members-container">
      <div v-if="members.length === 0" class="empty-state">
        <div class="empty-icon">👥</div>
        <div class="empty-title">No members yet</div>
        <div class="empty-message">
          Once you approve member requests, they will appear here.
        </div>
      </div>

      <div v-else class="members-grid">
        <div
          v-for="member in members"
          :key="member.memberId"
          class="member-card"
        >
          <!-- Member Header -->
          <div class="member-header">
            <div class="member-avatar">
              {{ member.name.charAt(0).toUpperCase() }}
            </div>
            <div class="member-info">
              <div class="member-name">{{ member.name }}</div>
              <div class="member-id">ID: {{ member.memberId }}</div>
              <div class="member-email">{{ member.email }}</div>
            </div>
          </div>

          <!-- Member Stats -->
          <div class="member-stats">
            <div class="stat-item">
              <span class="stat-label">Joined:</span>
              <span class="stat-value">{{ formatDate(member.joinedAt) }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Program:</span>
              <span class="stat-value">{{ member.programName }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Level:</span>
              <span class="stat-value">{{ member.experienceLevel }}</span>
            </div>
          </div>

          <!-- Progress Info -->
          <div v-if="member.lastActivity" class="member-activity">
            <div class="activity-label">Last Activity:</div>
            <div class="activity-value">{{ formatDate(member.lastActivity) }}</div>
          </div>

          <!-- Actions -->
          <div class="member-actions">
            <button class="btn small" @click="viewProgress(member)">
              📊 View Progress
            </button>
            <button class="btn small ghost" @click="viewFoodDiary(member)">
              🍽️ Food Diary
            </button>
            <button class="btn small ghost" @click="sendMessage(member)">
              💬 Message
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'back-to-dashboard'): void
  (e: 'view-food-diary', memberId: string): void
}>()

interface Member {
  memberId: string
  name: string
  email: string
  programName: string
  experienceLevel: string
  joinedAt: Date
  lastActivity?: Date
}

// Sample data - in real app this would come from API
const members = ref<Member[]>([
  {
    memberId: 'MEM_MC2024',
    name: 'Mike Chen',
    email: 'mike.chen@example.com',
    programName: 'Advanced Strength Program',
    experienceLevel: 'Advanced',
    joinedAt: new Date('2024-01-10'),
    lastActivity: new Date('2024-01-16')
  },
  {
    memberId: 'MEM_JD2024',
    name: 'Jane Doe',
    email: 'jane.doe@example.com',
    programName: 'Weight Loss Journey',
    experienceLevel: 'Intermediate',
    joinedAt: new Date('2024-01-05'),
    lastActivity: new Date('2024-01-15')
  },
  {
    memberId: 'MEM_TS2024',
    name: 'Tom Smith',
    email: 'tom.smith@example.com',
    programName: 'Beginner Full Body',
    experienceLevel: 'Beginner',
    joinedAt: new Date('2023-12-20'),
    lastActivity: new Date('2024-01-14')
  }
])

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

function viewProgress(member: Member) {
  alert(`View progress for ${member.name}\n\nThis would show workout completion, measurements, and progress photos.`)
}

function viewFoodDiary(member: Member) {
  // Emit event to show food diary where coach can comment
  emit('view-food-diary', member.memberId)
  alert(`View food diary for ${member.name}\n\nThis will take you to their food diary where you can comment on their meals.`)
}

function sendMessage(member: Member) {
  alert(`Send message to ${member.name}\n\nThis would open a messaging interface to communicate with your member.`)
}
</script>

<style scoped>
.member-management {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.back-btn {
  background: transparent;
  border: none;
  color: #3b82f6;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  padding: 8px 12px;
  margin-bottom: 16px;
  border-radius: 8px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 4px;
  width: fit-content;
}

.back-btn:hover {
  background: #eff6ff;
  color: #2563eb;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 24px;
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
  background: #eff6ff;
  border: 1px solid #3b82f6;
}

.stat-number {
  font-size: 24px;
  font-weight: 700;
  color: #1e40af;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  text-transform: uppercase;
}

.members-container {
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

.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.member-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  background: #fafafa;
  transition: all 0.2s ease;
}

.member-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59,130,246,0.1);
}

.member-header {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.member-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 600;
  flex-shrink: 0;
}

.member-info {
  flex: 1;
  min-width: 0;
}

.member-name {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 4px;
}

.member-id {
  font-size: 12px;
  color: #3b82f6;
  font-weight: 600;
  font-family: monospace;
  margin-bottom: 4px;
}

.member-email {
  font-size: 13px;
  color: #6b7280;
}

.member-stats {
  display: grid;
  gap: 8px;
  margin-bottom: 16px;
  padding: 12px;
  background: #fff;
  border-radius: 8px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.stat-label {
  color: #6b7280;
  font-weight: 500;
}

.stat-value {
  color: #374151;
  font-weight: 600;
}

.member-activity {
  margin-bottom: 16px;
  padding: 8px 12px;
  background: #f0fdf4;
  border-left: 3px solid #10b981;
  border-radius: 6px;
}

.activity-label {
  font-size: 11px;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 4px;
}

.activity-value {
  font-size: 13px;
  color: #065f46;
  font-weight: 600;
}

.member-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
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
  flex: 1;
}

.btn:hover {
  background: #f9fafb;
}

.btn.small {
  padding: 6px 12px;
  font-size: 12px;
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

  .members-grid {
    grid-template-columns: 1fr;
  }

  .member-actions {
    flex-direction: column;
  }

  .btn.small {
    width: 100%;
  }
}
</style>
