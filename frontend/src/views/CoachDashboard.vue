<template>
  <div class="coach-dashboard">
    <div class="dashboard-header">
      <div class="header-content">
        <h1 class="dashboard-title">Coach Dashboard</h1>
        <p class="dashboard-subtitle">Manage your workout programs and track your coaching progress</p>

        <div class="coach-id-display">
          <span class="coach-id-label">Your Coach ID:</span>
          <span class="coach-id-value">{{ coachID }}</span>
          <button class="btn-copy" @click="copyCoachID" title="Copy Coach ID">📋 Copy</button>
        </div>
      </div>

      <div class="header-actions">
        <button 
          class="btn primary" 
          @click="router.push('/create-workout-program')" 
          :disabled="!isApproved"
        >
          + Create New Program
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-message">
      Loading dashboard...
    </div>

    <!-- Approval Status (only if not approved) -->
    <div v-if="!isApproved" class="status-card">
      <div class="status-indicator" :class="approvalStatus">
        <div class="status-icon">
          <span v-if="approvalStatus === 'pending'">⏳</span>
          <span v-else-if="approvalStatus === 'rejected'">❌</span>
        </div>
        <div class="status-text">
          <div class="status-title">
            {{ approvalStatus === 'pending' ? 'Application Under Review' : 'Application Rejected' }}
          </div>
          <div class="status-message">
            {{ approvalStatus === 'pending'
              ? "Your application is being reviewed. You can create programs once approved."
              : "Please contact support or resubmit your application." }}
          </div>
        </div>
      </div>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="dashboard-content">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-number">{{ programs.length }}</div>
          <div class="stat-label">Total Programs</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ totalSessions }}</div>
          <div class="stat-label">Total Sessions</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ programsWithVideos }}</div>
          <div class="stat-label">Programs with Videos</div>
        </div>

        <div class="stat-card clickable" @click="router.push('/view-member')">
          <div class="stat-number">{{ memberCount }}</div>
          <div class="stat-label">My Members</div>
          <div class="stat-action">View All →</div>
        </div>

        <div class="stat-card clickable" @click="router.push('/view-request')">
          <div class="stat-number">{{ pendingRequestCount }}</div>
          <div class="stat-label">Pending Requests</div>
          <div class="stat-action">View All →</div>
        </div>
      </div>

      <div class="programs-section">
        <div class="section-header">
          <h2 class="section-title">Your Workout Programs</h2>
        </div>

        <!-- Empty state -->
        <div v-if="filteredPrograms.length === 0" class="empty-state">
          <div class="empty-icon">🏋️‍♂️</div>
          <div class="empty-title">No programs yet</div>
          <div class="empty-message">
            Start creating your first workout program to help your clients achieve their goals!
          </div>
          <button class="btn primary" @click="router.push('/create-workout-program')">
            Create Your First Program
          </button>
        </div>

        <!-- Programs grid -->
        <div v-else class="programs-grid">
          <div v-for="program in filteredPrograms" :key="program.id" class="program-card">
            <div class="program-header">
              <div class="program-title">{{ program.title }}</div>
              <div class="program-level" :class="program.difficulty_level">
                {{ program.difficulty_level }}
              </div>
            </div>

            <div class="program-description">
              {{ program.description || 'No description provided' }}
            </div>

            <!-- Actions for each program -->
            <div class="program-actions">
              <button 
                class="btn small primary"
                @click="router.push(`/workout-program/${program.id}`)"
              >
                Edit
              </button>

              <button 
                class="btn small danger"
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

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const loading = ref(true)
const showCreateProgram = ref(false)
const approvalStatus = ref<'pending'|'approved'|'rejected'>('pending')
const programs = ref<any[]>([])
const coachID = ref<string>('')
const pendingRequestCount = ref(0)
const memberCount = ref(0)
const editingProgram = ref<any>(null)

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
    alert('Coach ID copied to clipboard!')
  }
}


async function loadCoachStatus() {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/coach/status/', {
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

    coachID.value = data?.coach?.coach_id ?? ''
  } catch (err) {
    console.error('Error loading coach status', err)
    approvalStatus.value = 'pending'
    coachID.value = ''
  }
}

async function loadPrograms() {
  try {
    const res = await fetch('/api/workout/programs', { credentials: 'include' })
    const data = await res.json()
    programs.value = data.results || []
  } catch {
    programs.value = []
  }
}

async function loadPendingRequests() {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/member/coach-requests/', { credentials: 'include' })
    if (!res.ok) throw new Error('Failed to fetch requests')
    const data = await res.json()

    pendingRequestCount.value = data.filter((r: any) => r.status === 'pending').length
    memberCount.value = data.filter((r: any) => r.status === 'approved').length
  } catch (err) {
    console.error('Failed to load pending requests', err)
    pendingRequestCount.value = 0
    memberCount.value = 0
  }
}

async function deleteProgram(programId: number) {
  try {
    const res = await fetch(`/api/workout/programs/${programId}/`, {
      method: 'DELETE',
      credentials: 'include',
    })

    if (res.ok) {
      // refresh list
      await loadPrograms()
      // close modal if editing the deleted program
      if (editingProgram.value && editingProgram.value.id === programId) {
        editingProgram.value = null
        showCreateProgram.value = false
      }
      alert('Program deleted successfully!')
    } else {
      const text = await res.text()
      let body: any = text
      try { 
        body = JSON.parse(text) 
      } catch (err) {
        console.warn('Failed to parse response as JSON:', err)
      }
      console.error('Delete program failed:', res.status, body)
      const message = body?.detail || body?.error || body || `HTTP ${res.status}`
      alert('Failed to delete program: ' + JSON.stringify(message))
    }
  } catch (err) {
    console.error('Error deleting program:', err)
    alert('Failed to delete program')
  }
}

onMounted(async () => {
  await loadCoachStatus()

 if (isApproved.value) {
    await Promise.all([loadPrograms(), loadPendingRequests()])
  }
  
  loading.value = false
})
</script>


<style scoped>
.coach-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  gap: 20px;
}

.header-content h1.dashboard-title {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 8px 0;
}

.dashboard-subtitle {
  color: #6b7280;
  font-size: 16px;
  margin: 0 0 12px 0;
}

.coach-id-display {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #eff6ff;
  border: 1px solid #3b82f6;
  border-radius: 8px;
  width: fit-content;
}

.coach-id-label {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
}

.coach-id-value {
  font-size: 14px;
  color: #1e40af;
  font-weight: 700;
  font-family: monospace;
  letter-spacing: 0.5px;
}

.btn-copy {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-copy:hover {
  background: #2563eb;
  transform: scale(1.05);
}

.header-actions {
  flex-shrink: 0;
}

.status-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 32px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 20px;
}

.status-indicator.pending {
  background: #fef3c7;
  border: 1px solid #f59e0b;
}

.status-indicator.rejected {
  background: #fee2e2;
  border: 1px solid #ef4444;
}

.status-icon {
  font-size: 24px;
}

.status-text {
  flex: 1;
}

.status-title {
  font-weight: 600;
  font-size: 16px;
  color: #374151;
  margin-bottom: 4px;
}

.status-message {
  color: #6b7280;
  line-height: 1.5;
}

.demo-section {
  text-align: center;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  transition: all 0.2s ease;
}

.stat-card.clickable {
  cursor: pointer;
}

.stat-card.clickable:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  border-color: #3b82f6;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: #3b82f6;
  margin-bottom: 8px;
}

.stat-number.pending-highlight {
  color: #f59e0b;
}

.stat-label {
  color: #6b7280;
  font-weight: 500;
}

.stat-action {
  margin-top: 8px;
  font-size: 13px;
  color: #3b82f6;
  font-weight: 600;
}

.programs-section {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.filter-select {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 14px;
  background: #fff;
}

.empty-state {
  text-align: center;
  padding: 48px 24px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-title {
  font-size: 20px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 12px;
}

.empty-message {
  color: #6b7280;
  margin-bottom: 24px;
  line-height: 1.5;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.programs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.program-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  background: #fafafa;
  transition: all 0.2s ease;
}

.program-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59,130,246,0.15);
}

.program-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.program-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  flex: 1;
}

.program-level {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
}

.program-level.beginner {
  background: #d1fae5;
  color: #065f46;
}

.program-level.intermediate {
  background: #fef3c7;
  color: #92400e;
}

.program-level.advanced {
  background: #fee2e2;
  color: #991b1b;
}

.program-description {
  color: #6b7280;
  margin-bottom: 16px;
  line-height: 1.5;
  font-size: 14px;
}

.program-meta {
  display: grid;
  gap: 8px;
  margin-bottom: 16px;
}

.meta-item {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.meta-label {
  color: #6b7280;
}

.meta-value {
  color: #374151;
  font-weight: 500;
}

.program-features {
  margin-bottom: 16px;
}

.feature-badge {
  background: #fef3c7;
  color: #92400e;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 500;
}

.program-actions {
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
  text-align: center;
}

.btn:hover {
  background: #f9fafb;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn.primary {
  background: #3b82f6;
  color: #fff;
  border-color: #3b82f6;
}

.btn.primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn.ghost {
  background: transparent;
  color: #374151;
}

.btn.ghost:hover {
  background: #f3f4f6;
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: #fff;
  border-radius: 16px;
  width: 100%;
  max-width: 1000px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6b7280;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
}

.modal-close:hover {
  background: #f3f4f6;
}

.modal-body {
  padding: 0;
  max-height: calc(90vh - 80px);
  overflow-y: auto;
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: stretch;
  }

  .header-actions {
    align-self: stretch;
  }

  .section-header {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  .programs-grid {
    grid-template-columns: 1fr;
  }

  .program-actions {
    justify-content: space-between;
  }

  .modal-overlay {
    padding: 10px;
  }

  .modal-content {
    max-height: 95vh;
  }
}
</style>