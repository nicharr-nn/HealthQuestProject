<template>
  <div class="create-workout-program">
    <div class="page-header">
      <h1 class="page-title">{{ existingProgram ? 'Edit Workout Program' : 'Create Workout Program' }}</h1>
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
              <label class="form-label" for="duration">Duration (days) *</label>
              <input
                id="duration"
                v-model.number="workoutProgram.duration"
                type="number"
                min="1"
                max="365"
                class="form-input"
                placeholder="30"
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

      <!-- Daily Workout Schedule -->
      <div class="content-card">
        <div class="card-title mb-3">Daily Workout Schedule</div>

        <div class="duration-info mb-4">
          <span class="info-text">
            Program Duration: {{ workoutProgram.duration }} days
            {{ workoutProgram.duration > 0 ? `(${Math.ceil(workoutProgram.duration / 7)} weeks)` : '' }}
          </span>
        </div>

        <!-- Day Selection -->
        <div class="day-selector mb-4">
          <label class="form-label">Select Day to Add Workout:</label>
          <select v-model="selectedDay" class="form-input day-select">
            <option value="" disabled>Choose a day...</option>
            <option
              v-for="day in workoutProgram.duration"
              :key="day"
              :value="day"
            >
              Day {{ day }} {{ workoutProgram.dailyWorkouts[day]?.length ? `(${workoutProgram.dailyWorkouts[day].length} workouts)` : '' }}
            </option>
          </select>
        </div>

        <!-- Existing Daily Workouts -->
        <div v-if="Object.keys(workoutProgram.dailyWorkouts).length > 0" class="daily-workouts-list mb-4">
          <h4 class="form-section-title">Added Workouts</h4>
          <div class="days-container">
            <div
              v-for="(workouts, day) in workoutProgram.dailyWorkouts"
              :key="day"
              class="day-container"
            >
              <div class="day-header">
                <div class="day-number-large">Day {{ day }}</div>
                <div class="day-summary">{{ workouts.length }} workout{{ workouts.length !== 1 ? 's' : '' }}</div>
              </div>

              <div class="workouts-for-day">
                <div
                  v-for="(workout, workoutIndex) in workouts"
                  :key="workoutIndex"
                  class="workout-card"
                >
                  <div class="workout-header">
                    <div class="workout-title">{{ workout.name }}</div>
                    <div class="workout-actions">
                      <button
                        type="button"
                        class="btn small ghost"
                        @click="editWorkout(Number(day), workoutIndex)"
                      >
                        Edit
                      </button>
                      <button
                        type="button"
                        class="btn small danger"
                        @click="removeWorkout(Number(day), workoutIndex)"
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                  <div class="workout-meta">
                    <span>{{ workout.duration }} min</span>
                    <span class="separator">•</span>
                    <span>{{ workout.type || 'General' }}</span>
                    <span v-if="workout.youtubeUrl" class="youtube-indicator">
                      📹 Video
                    </span>
                  </div>
                  <div v-if="workout.notes" class="workout-notes">
                    {{ workout.notes.substring(0, 100) }}{{ workout.notes.length > 100 ? '...' : '' }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Add/Edit Workout Form -->
        <div v-if="selectedDay || editingDay !== null" class="add-workout-form">
          <h4 class="form-section-title">
            {{ editingDay !== null ? `Edit Workout for Day ${editingDay}` : `Add Workout for Day ${selectedDay}` }}
          </h4>

          <div class="form-group">
            <label class="form-label" for="workoutName">Workout Name *</label>
            <input
              id="workoutName"
              v-model="currentWorkout.name"
              type="text"
              class="form-input"
              placeholder="e.g., Upper Body Strength Training"
              required
            />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="workoutDuration">Duration (minutes) *</label>
              <input
                id="workoutDuration"
                v-model.number="currentWorkout.duration"
                type="number"
                min="5"
                max="180"
                class="form-input"
                placeholder="45"
                required
              />
            </div>

            <div class="form-group">
              <label class="form-label" for="workoutType">Workout Type</label>
              <select
                id="workoutType"
                v-model="currentWorkout.type"
                class="form-input"
              >
                <option value="">Select type</option>
                <option>Strength Training</option>
                <option>Cardio</option>
                <option>HIIT</option>
                <option>Flexibility</option>
                <option>Recovery</option>
                <option>Full Body</option>
                <option>Upper Body</option>
                <option>Lower Body</option>
                <option>Core</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label" for="workoutYoutubeUrl">YouTube Video URL</label>
            <input
              id="workoutYoutubeUrl"
              v-model="currentWorkout.youtubeUrl"
              type="url"
              class="form-input"
              placeholder="https://www.youtube.com/watch?v=..."
              @blur="validateYouTubeUrl"
            />
            <div v-if="youtubeError" class="error-message">{{ youtubeError }}</div>
          </div>

          <div class="form-group">
            <label class="form-label" for="workoutNotes">Workout Instructions</label>
            <textarea
              id="workoutNotes"
              v-model="currentWorkout.notes"
              class="form-input"
              rows="4"
              placeholder="Detailed instructions, exercises, sets/reps, equipment needed, etc."
            />
          </div>

          <div class="form-actions-inline">
            <button
              type="button"
              class="btn primary"
              @click="saveDayWorkout"
              :disabled="!currentWorkout.name || !currentWorkout.duration"
            >
              {{ editingDay !== null ? 'Update Workout' : 'Add Workout' }}
            </button>
            <button
              type="button"
              class="btn ghost"
              @click="cancelWorkoutEdit"
            >
              Cancel
            </button>
          </div>
        </div>

        <div v-if="!selectedDay && editingDay === null && Object.keys(workoutProgram.dailyWorkouts).length === 0" class="empty-state">
          <div class="empty-icon">📅</div>
          <div class="empty-title">No daily workouts added yet</div>
          <div class="empty-message">Select a day above to start building your workout program schedule.</div>
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
        {{ existingProgram ? 'Update Program' : 'Create Program' }}
      </button>
      <button
        type="button"
        class="btn ghost large"
        @click="resetProgram"
      >
        Reset All
      </button>
      <button
        type="button"
        class="btn ghost large"
        @click="emit('cancel')"
      >
        Cancel
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, watch } from 'vue'

interface Props {
  existingProgram?: {
    name: string
    description: string
    level: string
    duration: number
    category: string
    dailyWorkouts: Record<number, DailyWorkout[]>
  } | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  programCreated: [program: {
    name: string
    description: string
    level: string
    duration: number
    category: string
    dailyWorkouts: Record<number, DailyWorkout[]>
  }]
  cancel: []
}>()

interface WorkoutSession {
  name: string
  duration: number
  type: string
  youtubeUrl: string
  notes: string
}

interface DailyWorkout {
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
  dailyWorkouts: Record<number, DailyWorkout[]>
}

const workoutProgram = reactive<WorkoutProgram>({
  name: '',
  description: '',
  level: '',
  duration: 30,
  category: '',
  dailyWorkouts: {}
})

const selectedDay = ref<number | ''>('')
const editingDay = ref<number | null>(null)
const editingWorkoutIndex = ref<number | null>(null)

const currentWorkout = reactive<DailyWorkout>({
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
         Object.keys(workoutProgram.dailyWorkouts).length > 0
})

function validateYouTubeUrl() {
  youtubeError.value = ''

  if (!currentWorkout.youtubeUrl) return

  const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)[a-zA-Z0-9_-]{11}/

  if (!youtubeRegex.test(currentWorkout.youtubeUrl)) {
    youtubeError.value = 'Please enter a valid YouTube URL'
  }
}

function saveDayWorkout() {
  if (!currentWorkout.name || !currentWorkout.duration) {
    alert('Please fill in workout name and duration')
    return
  }

  if (currentWorkout.youtubeUrl) {
    validateYouTubeUrl()
    if (youtubeError.value) return
  }

  const targetDay = editingDay.value || selectedDay.value as number

  const workout: DailyWorkout = {
    name: currentWorkout.name,
    duration: currentWorkout.duration,
    type: currentWorkout.type,
    youtubeUrl: currentWorkout.youtubeUrl,
    notes: currentWorkout.notes
  }

  if (editingDay.value !== null && editingWorkoutIndex.value !== null) {
    // Editing existing workout
    workoutProgram.dailyWorkouts[editingDay.value][editingWorkoutIndex.value] = workout
  } else {
    // Adding new workout
    if (!workoutProgram.dailyWorkouts[targetDay]) {
      workoutProgram.dailyWorkouts[targetDay] = []
    }
    workoutProgram.dailyWorkouts[targetDay].push(workout)
  }

  resetCurrentWorkout()
}

function editWorkout(day: number, workoutIndex: number) {
  const workout = workoutProgram.dailyWorkouts[day]?.[workoutIndex]
  if (workout) {
    editingDay.value = day
    editingWorkoutIndex.value = workoutIndex
    selectedDay.value = ''
    currentWorkout.name = workout.name
    currentWorkout.duration = workout.duration
    currentWorkout.type = workout.type
    currentWorkout.youtubeUrl = workout.youtubeUrl
    currentWorkout.notes = workout.notes
  }
}

function removeWorkout(day: number, workoutIndex: number) {
  if (workoutProgram.dailyWorkouts[day]) {
    workoutProgram.dailyWorkouts[day].splice(workoutIndex, 1)

    // Remove the day entirely if no workouts left
    if (workoutProgram.dailyWorkouts[day].length === 0) {
      delete workoutProgram.dailyWorkouts[day]
    }
  }
}

function cancelWorkoutEdit() {
  resetCurrentWorkout()
}

function resetCurrentWorkout() {
  selectedDay.value = ''
  editingDay.value = null
  editingWorkoutIndex.value = null
  currentWorkout.name = ''
  currentWorkout.duration = 45
  currentWorkout.type = ''
  currentWorkout.youtubeUrl = ''
  currentWorkout.notes = ''
  youtubeError.value = ''
}

function submitProgram() {
  if (!canSubmitProgram.value) {
    alert('Please fill in all required fields and add at least one daily workout')
    return
  }

  // Emit the program data to parent component
  emit('programCreated', {
    name: workoutProgram.name,
    description: workoutProgram.description,
    level: workoutProgram.level,
    duration: workoutProgram.duration,
    category: workoutProgram.category,
    dailyWorkouts: { ...workoutProgram.dailyWorkouts }
  })
}

function resetProgram() {
  workoutProgram.name = ''
  workoutProgram.description = ''
  workoutProgram.level = ''
  workoutProgram.duration = 30
  workoutProgram.category = ''
  workoutProgram.dailyWorkouts = {}

  resetCurrentWorkout()
}

// Watch for existing program prop and populate form
watch(() => props.existingProgram, (program) => {
  if (program) {
    workoutProgram.name = program.name
    workoutProgram.description = program.description
    workoutProgram.level = program.level
    workoutProgram.duration = program.duration
    workoutProgram.category = program.category
    workoutProgram.dailyWorkouts = { ...program.dailyWorkouts }
  } else {
    resetProgram()
  }
}, { immediate: true })
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

.duration-info {
  background: #f3f4f6;
  padding: 12px 16px;
  border-radius: 8px;
  border-left: 4px solid #3b82f6;
}

.info-text {
  color: #374151;
  font-weight: 500;
  font-size: 14px;
}

.day-selector {
  background: #fafafa;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.day-select {
  max-width: 300px;
}

.daily-workouts-list {
  background: #fafafa;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.days-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-top: 16px;
}

.day-container {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s ease;
}

.day-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e5e7eb;
}

.day-number-large {
  background: #3b82f6;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 700;
}

.day-summary {
  color: #6b7280;
  font-weight: 500;
  font-size: 14px;
}

.workouts-for-day {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.workout-card {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  transition: all 0.2s ease;
}

.workout-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 2px 8px rgba(59,130,246,0.15);
}

.workout-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.day-number {
  background: #3b82f6;
  color: white;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.workout-title {
  font-weight: 600;
  color: #111827;
  font-size: 16px;
  flex: 1;
  margin-right: 12px;
}

.workout-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.workout-notes {
  color: #6b7280;
  font-size: 13px;
  line-height: 1.4;
  margin-top: 8px;
  padding: 8px;
  background: #f3f4f6;
  border-radius: 6px;
}

.workout-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6b7280;
  font-size: 12px;
  margin-bottom: 12px;
}

.separator {
  color: #d1d5db;
}

.youtube-indicator {
  background: #fef3c7;
  color: #92400e;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 500;
}

.add-workout-form {
  background: #f9fafb;
  padding: 20px;
  border-radius: 12px;
  border: 2px dashed #d1d5db;
  margin-top: 20px;
}

.form-actions-inline {
  display: flex;
  gap: 12px;
  align-items: center;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #6b7280;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.empty-title {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.empty-message {
  font-size: 14px;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .form-row { grid-template-columns: 1fr; }
  .form-actions { flex-direction: column; }
  .form-actions-inline { flex-direction: column; align-items: stretch; }
  .workouts-for-day { grid-template-columns: 1fr; }
  .workout-header { flex-direction: column; align-items: flex-start; gap: 8px; }
  .workout-actions { align-self: stretch; justify-content: space-between; }
  .day-header { flex-direction: column; align-items: flex-start; gap: 8px; }
  .day-select { max-width: 100%; }
}
</style>