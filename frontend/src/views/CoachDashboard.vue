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
          🔧 Simulate Admin Approval (Demo)
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
          <div class="section-actions">
            <select v-model="filterLevel" class="filter-select">
              <option value="">All Levels</option>
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
            </select>
          </div>
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
              <div class="program-title">{{ program.name }}</div>
              <div class="program-level" :class="program.level.toLowerCase()">
                {{ program.level }}
              </div>
            </div>

            <div class="program-description">
              {{ program.description || 'No description provided' }}
            </div>

            <div class="program-meta">
              <div class="meta-item">
                <span class="meta-label">Duration:</span>
                <span class="meta-value">{{ program.duration }} weeks</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">Sessions:</span>
                <span class="meta-value">{{ program.sessions?.length || 0 }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">Category:</span>
                <span class="meta-value">{{ program.category || 'General' }}</span>
              </div>
            </div>

            <div v-if="program.sessions?.some(s => s.youtubeUrl)" class="program-features">
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
import { ref, computed } from 'vue'
import CreateWorkoutProgram from '../components/CreateWorkoutProgram.vue'

interface WorkoutSession {
  name: string
  duration: number
  type: string
  youtubeUrl: string
  notes: string
}

interface WorkoutProgram {
  id: string
  name: string
  description: string
  level: string
  duration: number
  category: string
  sessions: WorkoutSession[]
  createdAt: Date
}

const approvalStatus = ref('pending') // 'pending', 'approved', 'rejected'
const showCreateProgram = ref(false)
const editingProgram = ref<WorkoutProgram | null>(null)
const filterLevel = ref('')

const programs = ref<WorkoutProgram[]>([
  // Sample data - in real app this would come from API
])

const isApproved = computed(() => approvalStatus.value === 'approved')

const totalSessions = computed(() => {
  return programs.value.reduce((total, program) => total + (program.sessions?.length || 0), 0)
})

const programsWithVideos = computed(() => {
  return programs.value.filter(program =>
    program.sessions?.some(session => session.youtubeUrl)
  ).length
})

const filteredPrograms = computed(() => {
  if (!filterLevel.value) return programs.value
  return programs.value.filter(program => program.level === filterLevel.value)
})

function simulateApproval() {
  approvalStatus.value = 'approved'
  alert('Coach application approved! You can now create and manage workout programs.')
}

function closeCreateProgram() {
  showCreateProgram.value = false
  editingProgram.value = null
}

function editProgram(program: WorkoutProgram) {
  editingProgram.value = program
  showCreateProgram.value = true
}

function viewProgram(program: WorkoutProgram) {
  alert(`Viewing program: ${program.name}\n\nThis would open a detailed view with all sessions, exercises, and video links.`)
}

function deleteProgram(programId: string) {
  if (confirm('Are you sure you want to delete this program? This action cannot be undone.')) {
    const index = programs.value.findIndex(p => p.id === programId)
    if (index > -1) {
      programs.value.splice(index, 1)
      alert('Program deleted successfully!')
    }
  }
}

function handleProgramCreated(newProgram: Omit<WorkoutProgram, 'id' | 'createdAt'>) {
  const program: WorkoutProgram = {
    ...newProgram,
    id: `prog_${Date.now()}`,
    createdAt: new Date()
  }

  if (editingProgram.value) {
    // Update existing program
    const index = programs.value.findIndex(p => p.id === editingProgram.value?.id)
    if (index > -1) {
      programs.value[index] = { ...program, id: editingProgram.value.id, createdAt: editingProgram.value.createdAt }
    }
  } else {
    // Add new program
    programs.value.unshift(program)
  }

  closeCreateProgram()
  alert(editingProgram.value ? 'Program updated successfully!' : 'Program created successfully!')
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