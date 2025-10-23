<template>
  <div class="coach-dashboard">
    <div class="dashboard-header">
      <div class="header-content">
        <h1 class="dashboard-title">Coach Dashboard</h1>
        <p class="dashboard-subtitle">Manage your workout programs and track your coaching progress</p>
      </div>
      <div class="header-actions">
        <button
          class="btn primary"
          @click="showCreateProgram = true"
          :disabled="!isApproved"
        >
          + Create New Program
        </button>
      </div>
    </div>

    <!-- Approval Status (if not approved) -->
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
            {{ approvalStatus === 'pending' ?
                'Your application is being reviewed by our admin team. You\'ll be able to create programs once approved.' :
                'Please contact support or resubmit your application.' }}
          </div>
        </div>
      </div>
      <!-- Demo Approval Button (for testing) -->
      <div class="demo-section">
        <button class="btn primary small" @click="simulateApproval">
          Simulate Admin Approval (Demo)
        </button>
      </div>
    </div>

    <!-- Dashboard Content (only visible when approved) -->
    <div v-if="isApproved && !showCreateProgram" class="dashboard-content">
      <!-- Stats Overview -->
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
      </div>

      <!-- Programs List -->
      <div class="programs-section">
        <div class="section-header">
          <h2 class="section-title">Your Workout Programs</h2>
          <!-- <div class="section-actions">
            <select v-model="filterLevel" class="filter-select">
              <option value="">All Levels</option>
              <option value="easy">Beginner</option>
              <option value="medium">Intermediate</option>
              <option value="hard">Advanced</option>
            </select> -->

          <!-- </div> -->
        </div>

        <div v-if="filteredPrograms.length === 0" class="empty-state">
          <div class="empty-icon">🏋️‍♂️</div>
          <div class="empty-title">No programs yet</div>
          <div class="empty-message">
            Start creating your first workout program to help your clients achieve their fitness goals!
          </div>
          <button class="btn primary" @click="showCreateProgram = true">
            Create Your First Program
          </button>
        </div>

        <div v-else class="programs-grid">
          <div
            v-for="program in filteredPrograms"
            :key="program.id"
            class="program-card"
          >
            <div class="program-header">
              <div class="program-title">{{ program.title }}</div>
              <div class="program-level" :class="program.difficulty_level">
                {{ program.difficulty_level }}
              </div>

            </div>

            <div class="program-description">
              {{ program.description || 'No description provided' }}
            </div>

            <div class="program-meta">
              <div class="meta-item">
                <span class="meta-label">Duration:</span>
                <span class="meta-value">{{ program.duration_days }} Days </span>
              </div>
              <div class="meta-item">
                <span class="meta-label">Sessions:</span>
                <span class="meta-value">{{ program.days?.length || 0 }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">Category:</span>
                <span class="meta-value">{{ program.category || 'General' }}</span>
              </div>
            </div>

            <div v-if="program.days?.some(d => d.video_links.length > 0)" class="program-features">
              <span class="feature-badge">📹 Video Included</span>
            </div>

            <div class="program-actions">
              <button class="btn small ghost" @click="editProgram(program)">
                Edit
              </button>
              <button class="btn small" @click="viewProgram(program)">
                View Details
              </button>
              <button class="btn small danger" @click="deleteProgram(program.id)">
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Program Modal -->
    <div v-if="showCreateProgram" class="modal-overlay" @click="closeCreateProgram">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">
            {{ editingProgram ? 'Edit Program' : 'Create New Program' }}
          </h2>
          <button class="modal-close" @click="closeCreateProgram">×</button>
        </div>
        <div class="modal-body">
          <CreateWorkoutProgram
            :existing-program="editingProgram"
            @program-created="handleProgramCreated"
            @cancel="closeCreateProgram"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import CreateWorkoutProgram from '../components/CreateWorkoutProgram.vue'

interface WorkoutDay {
  day_number: number
  title: string
  duration: number
  video_links: string[]
}

interface WorkoutProgram {
  id: number
  title: string
  description: string
  difficulty_level: string
  duration_days: number
  category: string
  is_public: boolean
  days: WorkoutDay[]
}

const approvalStatus = ref<'pending'|'approved'|'rejected'>('pending')
const showCreateProgram = ref(false)
const editingProgram = ref<WorkoutProgram | null>(null)
const filterLevel = ref('')

const programs = ref<WorkoutProgram[]>([])

const isApproved = computed(() => approvalStatus.value === 'approved')

const API_BASE = 'http://127.0.0.1:8000/api/workout/programs/'

function mapApiProgram(p: any): WorkoutProgram {
  return {
    id: p.id,
    title: p.title,
    description: p.description,
    difficulty_level: p.difficulty_level ?? '',
    duration_days: p.duration ?? p.duration_days ?? 0,
    category: p.category ?? 'general',
    is_public: p.is_public ?? true,
    days: (p.days || []).map((d: any) => ({
      day_number: d.day_number,
      title: d.title,
      duration: d.duration ?? d.duration_minutes ?? 0,
      video_links: d.video_links || []
    }))
  }
}

async function loadPrograms() {
  try {
    const res = await fetch(API_BASE, { credentials: 'include' })
    if (!res.ok) {
      console.error('Failed loading programs', res.status)
      programs.value = []
      return
    }
    const data = await res.json()
    // assume list returned
    programs.value = (Array.isArray(data) ? data : data.results || []).map(mapApiProgram)
  } catch (err) {
    console.error('Error loading programs', err)
    programs.value = []
  }
}

async function loadApprovalStatus() {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/coach/status/', { credentials: 'include' })
    if (!res.ok) {
      approvalStatus.value = 'pending'
      return
    }
    const data = await res.json()
    const status = data?.coach?.status_approval ?? data?.status_approval ?? null
    if (status === 'approved') approvalStatus.value = 'approved'
    else if (status === 'rejected') approvalStatus.value = 'rejected'
    else approvalStatus.value = 'pending'
  } catch (err) {
    console.error('Error loading coach status', err)
    approvalStatus.value = 'pending'
  }
}

onMounted(async () => {
  await loadApprovalStatus()
  if (isApproved.value) {
    await loadPrograms()
  }
})

// total sessions = all days across all programs
const totalSessions = computed(() => {
  return programs.value.reduce((total, program) => total + (program.days?.length || 0), 0)
})

// programs with at least one video link
const programsWithVideos = computed(() => {
  return programs.value.filter(program =>
    program.days?.some(day => (day.video_links || []).length > 0)
  ).length
})

// filter by difficulty
const filteredPrograms = computed(() => {
  if (!filterLevel.value) return programs.value
  return programs.value.filter(p => p.difficulty_level === filterLevel.value)
})

function simulateApproval() {
  approvalStatus.value = 'approved'
  loadPrograms()
  alert('Coach application approved! You can now create and manage workout programs.')
}

function closeCreateProgram() {
  showCreateProgram.value = false
  editingProgram.value = null
}

async function editProgram(program: WorkoutProgram) {
  // fetch latest program from API before editing
  try {
    const res = await fetch(`${API_BASE}${program.id}/`, { credentials: 'include' })
    if (!res.ok) {
      console.error('Failed to fetch program for edit', res.status)
      alert('Failed to load program for editing')
      return
    }
    const data = await res.json()
    editingProgram.value = mapApiProgram(data)
    showCreateProgram.value = true
  } catch (err) {
    console.error('Error fetching program', err)
    alert('Failed to load program for editing')
  }
}

function viewProgram(program: WorkoutProgram) {
  alert(`Viewing program: ${program.title}\n\nDuration: ${program.duration_days} days\nSessions: ${program.days?.length || 0}\nDescription: ${program.description || 'N/A'}\nStatus: ${program.is_public ? 'Public' : 'Private'}`)
}

async function deleteProgram(programId: number) {
  if (!confirm('Are you sure you want to delete this program? This action cannot be undone.')) {
    return
  }

  try {
    const res = await fetch(`${API_BASE}${programId}/`, {
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

async function handleProgramCreated() {
  // refresh list after create/update
  await loadPrograms()
  closeCreateProgram()
}
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
  margin: 0;
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
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: #3b82f6;
  margin-bottom: 8px;
}

.stat-label {
  color: #6b7280;
  font-weight: 500;
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