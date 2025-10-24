<template>
  <div class="member-management">
    <button class="btn primary" @click="goBackToDashboard">
      ← Back to Dashboard
    </button>

    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">Member Management</h1>
        <p class="page-subtitle">
          View and manage members who have been accepted
        </p>
      </div>
      <div class="header-stats">
        <div class="stat-badge approved">
          <span class="stat-number">{{ members.length }}</span>
          <span class="stat-label">Active Members</span>
        </div>
      </div>
    </div>

    <div class="members-container">
      <div v-if="loading" class="empty-state">
        Loading members...
      </div>

      <div v-else-if="members.length === 0" class="empty-state">
        <div class="empty-icon">🙌</div>
        <div class="empty-title">No active members</div>
        <div class="empty-message">Start approving member requests to see them here.</div>
      </div>

      <div v-else class="members-grid">
        <div
          v-for="member in members"
          :key="member.memberId"
          class="member-card"
        >
          <div class="member-header">
            <div class="member-info">
              <div class="member-avatar">{{ member.name.charAt(0).toUpperCase() }}</div>
              <div class="member-details">
                <div class="member-name">{{ member.name }}</div>
                <div class="member-id">ID: {{ member.memberId }}</div>
                <div class="member-email">{{ member.email }}</div>
              </div>
            </div>
            <div class="member-status">ACTIVE</div>
          </div>

          <div class="member-info-body">
            <div class="info-row"><span class="info-label">Program:</span><span class="info-value">{{ member.programName }}</span></div>
            <div class="info-row"><span class="info-label">Level:</span><span class="info-value">{{ member.level }}</span></div>
            <div class="info-row"><span class="info-label">Joined:</span><span class="info-value">{{ formatDate(member.joinedAt) }}</span></div>
            <div class="info-row"><span class="info-label">Last Activity:</span><span class="info-value">{{ formatDate(member.lastActivity) }}</span></div>
          </div>

          <div class="member-actions">
            <button class="btn small ghost" @click="viewProgress(member)">📊 View Progress</button>
            <button class="btn small danger" @click="removeMember(member)">Remove</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

interface Member {
  memberId: string
  name: string
  email: string
  programName: string
  level: string
  joinedAt: string
  lastActivity: string
}

const router = useRouter()
const members = ref<Member[]>([])
const loading = ref(true)

function goBackToDashboard() {
  router.push('/coach-dashboard')
}

function formatDate(dateStr: string) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

async function loadMembers() {
  loading.value = true
  try {
    const res = await fetch('http://127.0.0.1:8000/api/member/accepted/', {
      credentials: 'include'
    })
    if (!res.ok) throw new Error('Failed to fetch members')
    const data: Member[] = await res.json()
    members.value = data
  } catch (err) {
    console.error(err)
    members.value = []
  } finally {
    loading.value = false
  }
}

function viewProgress(member: Member) {
  router.push(`/member/${member.memberId}/progress`)
}

async function removeMember(member: Member) {
  if (!confirm(`Remove ${member.name} from your members?`)) return
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/member/${member.memberId}/`, {
      method: 'DELETE',
      credentials: 'include'
    })
    if (!res.ok) throw new Error('Failed to remove')
    members.value = members.value.filter(m => m.memberId !== member.memberId)
  } catch (err) {
    console.error(err)
    alert('Failed to remove member')
  }
}

onMounted(() => {
  loadMembers()
})
</script>

<style scoped>
.member-management {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
}

.page-subtitle {
  color: #6b7280;
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
  background: #d1fae5;
  border: 1px solid #10b981;
}

.stat-number {
  font-size: 24px;
  font-weight: 700;
}

.stat-label {
  font-size: 12px;
  text-transform: uppercase;
  color: #6b7280;
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

.members-grid {
  display: grid;
  gap: 16px;
}

.member-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  background: #fafafa;
}

.member-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}

.member-info {
  display: flex;
  gap: 12px;
  align-items: center;
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
}

.member-name {
  font-size: 18px;
  font-weight: 600;
}

.member-id {
  font-size: 12px;
  color: #3b82f6;
  font-family: monospace;
}

.member-email {
  font-size: 14px;
  color: #6b7280;
}

.member-status {
  padding: 6px 12px;
  border-radius: 20px;
  background: #d1fae5;
  color: #065f46;
  font-size: 12px;
  font-weight: 600;
  align-self: flex-start;
}

.member-info-body {
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
}

.info-label {
  color: #6b7280;
}

.info-value {
  font-weight: 600;
}

.member-actions {
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
  font-size: 14px;
}

.btn.small {
  padding: 6px 12px;
  font-size: 12px;
}

.btn.danger {
  background: #ef4444;
  color: #fff;
  border-color: #ef4444;
}

.btn.danger:hover {
  background: #dc2626;
}

.btn.ghost:hover {
  background: #f3f4f6;
}
</style>
