<template>
  <div class="create-workout-program">
    <div class="page-header">
      <h1 class="page-title">Create Workout Program</h1>
      <p class="page-subtitle">Design a comprehensive workout program with YouTube video guides</p>
    </div>

    <div class="content-grid">
      <!-- Program Details -->
      <div class="content-card">
        <div class="card-title mb-3">Program Information</div>

        <form @submit.prevent="submitProgram" class="workout-form">
          <div class="form-group">
            <label class="form-label" for="programName">Program Name *</label>
            <input
              id="programName"
              v-model="workoutProgram.name"
              type="text"
              class="form-input"
              placeholder="e.g., 8-Week Fat Loss Program"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="description">Description</label>
            <textarea
              id="description"
              v-model="workoutProgram.description"
              class="form-input"
              rows="4"
              placeholder="Describe the goals, target audience, and overview of your program"
            />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="level">Difficulty Level *</label>
              <select
                id="level"
                v-model="workoutProgram.level"
                class="form-input"
                required
              >
                <option value="" disabled>Select difficulty level</option>
                <option>Beginner</option>
                <option>Intermediate</option>
                <option>Advanced</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label" for="duration">Duration (weeks) *</label>
              <input
                id="duration"
                v-model.number="workoutProgram.duration"
                type="number"
                min="1"
                max="52"
                class="form-input"
                placeholder="8"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label" for="category">Category</label>
            <select
              id="category"
              v-model="workoutProgram.category"
              class="form-input"
            >
              <option value="" disabled>Select category</option>
              <option>Strength Training</option>
              <option>Cardio</option>
              <option>Weight Loss</option>
              <option>Muscle Building</option>
              <option>Endurance</option>
              <option>Flexibility</option>
              <option>Full Body</option>
            </select>
          </div>
        </form>
      </div>

      <!-- Workout Sessions -->
      <div class="content-card">
        <div class="card-title mb-3">Workout Sessions</div>

        <div v-if="workoutProgram.sessions.length === 0" class="muted mb-4">
          No workout sessions added yet. Add your first session below!
        </div>

        <div v-else class="sessions-list mb-4">
          <div
            v-for="(session, index) in workoutProgram.sessions"
            :key="index"
            class="session-item"
          >
            <div class="session-header">
              <div class="session-title">{{ session.name || `Session ${index + 1}` }}</div>
              <button
                type="button"
                class="btn small danger"
                @click="removeSession(index)"
              >
                Remove
              </button>
            </div>
            <div class="session-meta">
              Duration: {{ session.duration }} min
              <span v-if="session.youtubeUrl" class="youtube-indicator">
                📹 Video included
              </span>
            </div>
          </div>
        </div>

        <!-- Add New Session Form -->
        <div class="add-session-form">
          <h4 class="form-section-title">Add New Session</h4>

          <div class="form-group">
            <label class="form-label" for="sessionName">Session Name *</label>
            <input
              id="sessionName"
              v-model="newSession.name"
              type="text"
              class="form-input"
              placeholder="e.g., Upper Body Strength"
              required
            />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="sessionDuration">Duration (minutes) *</label>
              <input
                id="sessionDuration"
                v-model.number="newSession.duration"
                type="number"
                min="5"
                max="180"
                class="form-input"
                placeholder="45"
                required
              />
            </div>

            <div class="form-group">
              <label class="form-label" for="sessionType">Session Type</label>
              <select
                id="sessionType"
                v-model="newSession.type"
                class="form-input"
              >
                <option value="" disabled>Select type</option>
                <option>Strength</option>
                <option>Cardio</option>
                <option>HIIT</option>
                <option>Flexibility</option>
                <option>Recovery</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label" for="youtubeUrl">YouTube Video URL</label>
            <input
              id="youtubeUrl"
              v-model="newSession.youtubeUrl"
              type="url"
              class="form-input"
              placeholder="https://www.youtube.com/watch?v=..."
              @blur="validateYouTubeUrl"
            />
            <div v-if="youtubeError" class="error-message">{{ youtubeError }}</div>
          </div>

          <div class="form-group">
            <label class="form-label" for="sessionNotes">Session Notes</label>
            <textarea
              id="sessionNotes"
              v-model="newSession.notes"
              class="form-input"
              rows="3"
              placeholder="Instructions, tips, or equipment needed for this session"
            />
          </div>

          <button
            type="button"
            class="btn primary"
            @click="addSession"
            :disabled="!newSession.name || !newSession.duration"
          >
            Add Session
          </button>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="form-actions">
      <button
        type="button"
        class="btn primary large"
        @click="submitProgram"
        :disabled="!canSubmitProgram"
      >
        Create Program
      </button>
      <button
        type="button"
        class="btn ghost large"
        @click="resetProgram"
      >
        Reset All
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from 'vue'

interface WorkoutSession {
  name: string
  duration: number
  type: string
  youtubeUrl: string
  notes: string
}

interface WorkoutProgram {
  name: string
  description: string
  level: string
  duration: number
  category: string
  sessions: WorkoutSession[]
}

const workoutProgram = reactive<WorkoutProgram>({
  name: '',
  description: '',
  level: '',
  duration: 8,
  category: '',
  sessions: []
})

const newSession = reactive<WorkoutSession>({
  name: '',
  duration: 45,
  type: '',
  youtubeUrl: '',
  notes: ''
})

const youtubeError = ref('')

const canSubmitProgram = computed(() => {
  return workoutProgram.name &&
         workoutProgram.level &&
         workoutProgram.duration &&
         workoutProgram.sessions.length > 0
})

function validateYouTubeUrl() {
  youtubeError.value = ''

  if (!newSession.youtubeUrl) return

  const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)[a-zA-Z0-9_-]{11}/

  if (!youtubeRegex.test(newSession.youtubeUrl)) {
    youtubeError.value = 'Please enter a valid YouTube URL'
  }
}

function addSession() {
  if (!newSession.name || !newSession.duration) {
    alert('Please fill in session name and duration')
    return
  }

  if (newSession.youtubeUrl) {
    validateYouTubeUrl()
    if (youtubeError.value) return
  }

  workoutProgram.sessions.push({
    name: newSession.name,
    duration: newSession.duration,
    type: newSession.type,
    youtubeUrl: newSession.youtubeUrl,
    notes: newSession.notes
  })

  // Reset form
  newSession.name = ''
  newSession.duration = 45
  newSession.type = ''
  newSession.youtubeUrl = ''
  newSession.notes = ''
  youtubeError.value = ''
}

function removeSession(index: number) {
  workoutProgram.sessions.splice(index, 1)
}

function submitProgram() {
  if (!canSubmitProgram.value) {
    alert('Please fill in all required fields and add at least one session')
    return
  }

  // In real app: POST to API here
  console.log('Created workout program:', { ...workoutProgram })
  alert('Workout program created successfully! Check console for details.')
  resetProgram()
}

function resetProgram() {
  workoutProgram.name = ''
  workoutProgram.description = ''
  workoutProgram.level = ''
  workoutProgram.duration = 8
  workoutProgram.category = ''
  workoutProgram.sessions = []

  newSession.name = ''
  newSession.duration = 45
  newSession.type = ''
  newSession.youtubeUrl = ''
  newSession.notes = ''
  youtubeError.value = ''
}
</script>

<style scoped>
.create-workout-program { max-width: 1200px; margin: 0 auto; padding: 24px; }
.page-header { margin-bottom: 24px; }
.page-title { font-size: 28px; font-weight: 700; margin: 0; color: #111827; }
.page-subtitle { color: #6b7280; margin-top: 6px; font-size: 16px; }

.content-grid { display: grid; grid-template-columns: 1fr; gap: 24px; margin-bottom: 24px; }
@media (min-width: 1024px) { .content-grid { grid-template-columns: 1fr 1fr; } }

.content-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 16px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.card-title { font-weight: 600; font-size: 20px; color: #111827; }
.muted { color: #6b7280; font-style: italic; }

.workout-form, .add-session-form { display: grid; gap: 16px; }
.form-group { display: grid; gap: 6px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.form-label { font-size: 14px; color: #374151; font-weight: 500; }
.form-input {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 12px 14px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.form-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
}

.form-section-title {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 12px 0;
  padding-top: 12px;
  border-top: 1px solid #e5e7eb;
}

.sessions-list { display: grid; gap: 12px; }
.session-item {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
  background: #f9fafb;
}
.session-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.session-title { font-weight: 600; color: #111827; }
.session-meta {
  color: #6b7280;
  font-size: 13px;
  display: flex;
  gap: 12px;
  align-items: center;
}
.youtube-indicator {
  background: #fef3c7;
  color: #92400e;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
}

.btn {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 10px 16px;
  font-weight: 600;
  background: #fff;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
}
.btn:hover { background: #f9fafb; }
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.btn.primary {
  background: #3b82f6;
  color: #fff;
  border-color: #3b82f6;
}
.btn.primary:hover:not(:disabled) { background: #2563eb; }
.btn.ghost { background: #fff; color: #374151; }
.btn.ghost:hover { background: #f3f4f6; }
.btn.small { padding: 6px 12px; font-size: 12px; }
.btn.large { padding: 14px 24px; font-size: 16px; }
.btn.danger {
  background: #ef4444;
  color: #fff;
  border-color: #ef4444;
}
.btn.danger:hover { background: #dc2626; }

.form-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.error-message {
  color: #ef4444;
  font-size: 12px;
  margin-top: 4px;
}

@media (max-width: 768px) {
  .form-row { grid-template-columns: 1fr; }
  .form-actions { flex-direction: column; }
  .session-header { flex-direction: column; align-items: flex-start; gap: 8px; }
}
</style>