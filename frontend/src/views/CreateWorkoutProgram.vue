<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 py-6 font-body">
    <!-- Page Header -->
    <div class="mb-6">
      <h1 class="text-3xl font-subtitle text-[#B87C4C]">
        {{ isEditing ? 'Edit Workout Program' : 'Create Workout Program' }}
      </h1>
      <p class="text-gray-600 mt-2">
        {{
          isEditing
            ? 'Update your existing workout program'
            : 'Design a comprehensive workout program with YouTube video guides'
        }}
      </p>
    </div>

    <!-- Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- Program Details Card -->
      <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <div class="text-xl font-semibold text-gray-900 mb-6">Program Information</div>

        <form @submit.prevent="submitProgram" class="space-y-4">
          <!-- Program Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5" for="programName">
              Program Name *
            </label>
            <input
              id="programName"
              v-model="workoutProgram.title"
              type="text"
              class="w-full border border-gray-300 rounded-lg px-3.5 py-3 text-sm outline-none transition-all focus:border-blue-500 focus:ring-4 focus:ring-blue-50"
              placeholder="e.g., 8-Week Fat Loss Program"
              required
            />
          </div>

          <!-- Description with Character Counter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5" for="description">
              Description
            </label>
            <textarea
              id="description"
              v-model="workoutProgram.description"
              class="w-full border rounded-lg px-3.5 py-3 text-sm outline-none transition-all resize-none"
              :class="
                descriptionError
                  ? 'border-red-500 focus:border-red-500 focus:ring-4 focus:ring-red-50'
                  : 'border-gray-300 focus:border-blue-500 focus:ring-4 focus:ring-blue-50'
              "
              rows="4"
              maxlength="180"
              placeholder="Describe the goals, target audience, and overview of your program"
              @input="validateDescription"
            />
            <div class="flex justify-between items-center mt-1.5">
              <span v-if="descriptionError" class="text-xs text-red-500">
                {{ descriptionError }}
              </span>
              <span
                class="text-xs ml-auto"
                :class="
                  descriptionLength > 180
                    ? 'text-red-500 font-semibold'
                    : descriptionLength > 150
                      ? 'text-orange-500'
                      : 'text-gray-500'
                "
              >
                {{ descriptionLength }}/180 characters
              </span>
            </div>
          </div>

          <!-- Difficulty Level & Duration -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5" for="level">
                Difficulty Level *
              </label>
              <select
                id="level"
                v-model="workoutProgram.difficulty_level"
                class="w-full border border-gray-300 rounded-lg px-3.5 py-3 text-sm outline-none transition-all focus:border-blue-500 focus:ring-4 focus:ring-blue-50"
                required
              >
                <option value="" disabled>Select difficulty level</option>
                <option value="easy">EASY</option>
                <option value="medium">MEDIUM</option>
                <option value="hard">HARD</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5" for="duration">
                Duration (day{{ workoutProgram.duration === 1 ? '' : 's' }}) *
              </label>
              <input
                id="duration"
                v-model.number="workoutProgram.duration"
                type="number"
                min="1"
                max="365"
                class="w-full border border-gray-300 rounded-lg px-3.5 py-3 text-sm outline-none transition-all focus:border-blue-500 focus:ring-4 focus:ring-blue-50"
                placeholder="30"
                required
              />
            </div>
          </div>

          <!-- Category -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5" for="category">
              Category
            </label>
            <select
              id="category"
              v-model="workoutProgram.category"
              class="w-full border border-gray-300 rounded-lg px-3.5 py-3 text-sm outline-none transition-all focus:border-blue-500 focus:ring-4 focus:ring-blue-50"
            >
              <option value="" disabled>Select category</option>
              <option value="strength_training">Strength Training</option>
              <option value="cardio">Cardio</option>
              <option value="weight_loss">Weight Loss</option>
              <option value="muscle_building">Muscle Building</option>
              <option value="endurance">Endurance</option>
              <option value="flexibility">Flexibility</option>
              <option value="full_body">Full Body</option>
            </select>
          </div>

          <!-- Level Access -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5" for="levelAccess">
              Level Access
            </label>
            <select
              id="levelAccess"
              v-model="workoutProgram.level_access"
              class="w-full border border-gray-300 rounded-lg px-3.5 py-3 text-sm outline-none transition-all focus:border-blue-500 focus:ring-4 focus:ring-blue-50"
            >
              <option value="all">All levels</option>
              <option value="bronze">Bronze only</option>
              <option value="silver">Silver only</option>
              <option value="gold">Gold only</option>
            </select>
          </div>

          <!-- Visibility Toggle -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5"> Visibility </label>
            <div class="flex gap-3">
              <button
                type="button"
                class="flex-1 py-3 rounded-lg font-semibold text-sm transition-all"
                :class="
                  workoutProgram.is_public
                    ? 'bg-blue-500 text-white border-2 border-blue-500'
                    : 'bg-white text-gray-700 border-2 border-gray-300 hover:bg-gray-50'
                "
                @click="workoutProgram.is_public = true"
              >
                Public
              </button>
              <button
                type="button"
                class="flex-1 py-3 rounded-lg font-semibold text-sm transition-all"
                :class="
                  !workoutProgram.is_public
                    ? 'bg-blue-500 text-white border-2 border-blue-500'
                    : 'bg-white text-gray-700 border-2 border-gray-300 hover:bg-gray-50'
                "
                @click="workoutProgram.is_public = false"
              >
                Private
              </button>
            </div>
            <p class="text-xs text-gray-600 italic mt-2">
              Public programs are discoverable by users. Private programs are only visible to your
              assigned clients.
            </p>

            <!-- Member ID Input (only for private) -->
            <div v-if="workoutProgram.is_public === false" class="mt-4">
              <label class="block text-sm font-medium text-gray-700 mb-1.5" for="memberID">
                Member ID
              </label>
              <input
                id="memberID"
                v-model="workoutAssignment.member_id"
                type="text"
                class="w-full border border-gray-300 rounded-lg px-3.5 py-3 text-sm outline-none transition-all focus:border-blue-500 focus:ring-4 focus:ring-blue-50"
                placeholder="e.g., M-00001"
                pattern="M-\d+"
                title="Format: M- followed by numbers (e.g., M-00001)"
                required
              />
              <p class="text-xs text-gray-600 mt-1">
                Enter the member's ID exactly as shown in your accepted members list
              </p>
            </div>
          </div>
        </form>
      </div>

      <!-- Daily Workout Schedule Card -->
      <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <div class="text-xl font-semibold text-gray-900 mb-6">Daily Workout Schedule</div>

        <!-- Duration Info -->
        <div class="bg-gray-50 px-4 py-3 rounded-lg border-l-4 border-blue-500 mb-6">
          <span class="text-sm text-gray-700 font-medium">
            Program Duration:
            {{ workoutProgram.duration }} day{{ workoutProgram.duration === 1 ? '' : 's' }}
            {{
              workoutProgram.duration > 0
                ? `(${Math.ceil(workoutProgram.duration / 7)} week${Math.ceil(workoutProgram.duration / 7) === 1 ? '' : 's'})`
                : ''
            }}
          </span>
        </div>

        <!-- Day Selection -->
        <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Select Day to Add Workout:
          </label>
          <select
            v-model="selectedDay"
            class="w-full max-w-xs border border-gray-300 rounded-lg px-3.5 py-3 text-sm outline-none transition-all focus:border-blue-500 focus:ring-4 focus:ring-blue-50"
          >
            <option value="" disabled>Choose a day</option>
            <option v-for="day in workoutProgram.duration" :key="day" :value="day">
              Day {{ day }}
              {{
                workoutProgram.WorkoutDays[day]?.length
                  ? `(${workoutProgram.WorkoutDays[day].length} workouts)`
                  : ''
              }}
            </option>
          </select>
        </div>

        <!-- Existing Daily Workouts -->
        <div
          v-if="Object.keys(workoutProgram.WorkoutDays).length > 0"
          class="bg-gray-50 p-5 rounded-xl border border-gray-200 mb-6"
        >
          <h4 class="text-base font-semibold text-gray-700 mb-4">Added Workouts</h4>
          <div class="flex flex-col gap-6">
            <div
              v-for="(workouts, day) in workoutProgram.WorkoutDays"
              :key="day"
              class="bg-white border border-gray-200 rounded-xl p-5 transition-all hover:shadow-sm"
            >
              <!-- Day Header -->
              <div class="flex justify-between items-center mb-4 pb-3 border-b-2 border-gray-200">
                <div class="bg-blue-500 text-white px-4 py-2 rounded-lg text-base font-bold">
                  Day {{ day }}
                </div>
                <div class="text-sm text-gray-600 font-medium">
                  {{ workouts.length }} workout{{ workouts.length !== 1 ? 's' : '' }}
                </div>
              </div>

              <!-- Workouts for this day -->
              <div class="grid grid-cols-1 gap-4">
                <div
                  v-for="(workout, workoutIndex) in workouts"
                  :key="workoutIndex"
                  class="bg-gray-50 border border-gray-200 rounded-lg p-4 transition-all hover:border-blue-500 hover:shadow-md"
                >
                  <div class="flex justify-between items-center mb-3">
                    <div class="font-semibold text-gray-900 flex-1 mr-3">
                      {{ workout.title }}
                    </div>
                    <div class="flex gap-2">
                      <button
                        type="button"
                        class="px-3 py-1.5 text-xs font-semibold bg-white text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-all"
                        @click="editWorkout(Number(day), workoutIndex)"
                      >
                        Edit
                      </button>
                      <button
                        type="button"
                        class="px-3 py-1.5 text-xs font-semibold bg-red-500 text-white border border-red-500 rounded-lg hover:bg-red-600 transition-all"
                        @click="removeWorkout(Number(day), workoutIndex)"
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                  <div class="flex items-center gap-2 text-xs text-gray-600">
                    <span>{{ workout.duration }} min</span>
                    <span class="text-gray-300">•</span>
                    <span>{{ workout.type || 'General' }}</span>
                    <span
                      v-if="workout.video_link"
                      class="bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded text-[10px] font-medium"
                    >
                      📹 Video
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Add/Edit Workout Form -->
        <div
          v-if="selectedDay || editingDay !== null"
          class="bg-gray-50 p-5 rounded-xl border-2 border-dashed border-gray-300"
        >
          <h4 class="text-base font-semibold text-gray-700 mb-4 pt-3 border-t border-gray-300">
            {{
              editingDay !== null
                ? `Edit Workout for Day ${editingDay}`
                : `Add Workout for Day ${selectedDay}`
            }}
          </h4>

          <div class="space-y-4">
            <!-- Workout Name -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5" for="workoutName">
                Workout Name *
              </label>
              <input
                id="workoutName"
                v-model="currentWorkout.title"
                type="text"
                class="w-full border border-gray-300 rounded-lg px-3.5 py-3 text-sm outline-none transition-all focus:border-blue-500 focus:ring-4 focus:ring-blue-50"
                placeholder="e.g., Upper Body Strength Training"
                required
              />
            </div>

            <!-- Duration & Type -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5" for="workoutDuration">
                  Duration (minutes) *
                </label>
                <input
                  id="workoutDuration"
                  v-model.number="currentWorkout.duration"
                  type="number"
                  min="5"
                  max="180"
                  class="w-full border border-gray-300 rounded-lg px-3.5 py-3 text-sm outline-none transition-all focus:border-blue-500 focus:ring-4 focus:ring-blue-50"
                  placeholder="30"
                  required
                  @input="validateDuration"
                />
                <p v-if="durationError" class="text-xs text-red-500 mt-1">{{ durationError }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5" for="workoutType">
                  Workout Type
                </label>
                <select
                  id="workoutType"
                  v-model="currentWorkout.type"
                  class="w-full border border-gray-300 rounded-lg px-3.5 py-3 text-sm outline-none transition-all focus:border-blue-500 focus:ring-4 focus:ring-blue-50"
                >
                  <option value="">Select type</option>
                  <option value="strength_training">Strength Training</option>
                  <option value="cardio">Cardio</option>
                  <option value="hiit">HIIT</option>
                  <option value="flexibility">Flexibility</option>
                  <option value="recovery">Recovery</option>
                  <option value="full_body">Full Body</option>
                  <option value="upper_body">Upper Body</option>
                  <option value="lower_body">Lower Body</option>
                  <option value="core">Core</option>
                </select>
              </div>
            </div>

            <!-- YouTube URL -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5" for="workoutvideo_link">
                YouTube Video URL
              </label>
              <input
                id="workoutvideo_link"
                v-model="currentWorkout.video_link"
                type="url"
                class="w-full border border-gray-300 rounded-lg px-3.5 py-3 text-sm outline-none transition-all focus:border-blue-500 focus:ring-4 focus:ring-blue-50"
                placeholder="https://www.youtube.com/watch?v=..."
                required
                @blur="validatevideo_link"
              />
              <div v-if="youtubeError" class="text-xs text-red-500 mt-1">
                {{ youtubeError }}
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex gap-3">
              <button
                type="button"
                class="flex-1 bg-blue-500 text-white font-semibold px-4 py-3 rounded-lg transition-all hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
                @click="saveDayWorkout"
                :disabled="
                  !currentWorkout.title ||
                  !currentWorkout.duration ||
                  !currentWorkout.video_link ||
                  !youtubeRegex.test(currentWorkout.video_link)
                "
              >
                {{ editingDay !== null ? 'Update Workout' : 'Add Workout' }}
              </button>
              <button
                type="button"
                class="flex-1 bg-white text-gray-700 border border-gray-300 font-semibold px-4 py-3 rounded-lg transition-all hover:bg-gray-50"
                @click="cancelWorkoutEdit"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div
          v-if="
            !selectedDay &&
            editingDay === null &&
            Object.keys(workoutProgram.WorkoutDays).length === 0
          "
          class="text-center py-10 px-5 text-gray-600"
        >
          <div class="text-5xl mb-3">📅</div>
          <div class="text-base font-semibold text-gray-700 mb-2">No daily workouts added yet</div>
          <div class="text-sm leading-relaxed">
            Select a day above to start building your workout program schedule.
          </div>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex flex-col sm:flex-row gap-4 justify-center pt-6 border-t border-gray-200">
      <button
        type="button"
        class="bg-blue-500 text-white font-semibold px-6 py-3.5 rounded-lg text-base transition-all hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
        @click="submitProgram"
        :disabled="!canSubmitProgram"
      >
        {{ isEditing ? 'Update Program' : 'Create Program' }}
      </button>
      <button
        type="button"
        class="bg-white text-gray-700 border border-gray-300 font-semibold px-6 py-3.5 rounded-lg text-base transition-all hover:bg-gray-50 shadow-sm"
        @click="resetProgram"
      >
        Reset All
      </button>
      <button
        type="button"
        class="bg-white text-gray-700 border border-gray-300 font-semibold px-6 py-3.5 rounded-lg text-base transition-all hover:bg-gray-50 shadow-sm"
        @click="handleCancel"
      >
        Cancel
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const coachUserProfileId = ref<number | null>(null)
const editingProgramId = ref<number | null>(null)
const backupProgramData = ref<WorkoutProgram | null>(null)

const descriptionError = ref('')
const descriptionLength = computed(() => workoutProgram.description.length)

function validateDescription() {
  if (workoutProgram.description.length > 180) {
    descriptionError.value = 'Description cannot exceed 180 characters'
  } else {
    descriptionError.value = ''
  }
}

onMounted(async () => {
  const editId = route.query.edit as string

  if (editId) {
    editingProgramId.value = parseInt(editId)
    await loadExistingProgram(editingProgramId.value)

    backupProgramData.value = {
      title: workoutProgram.title,
      description: workoutProgram.description,
      difficulty_level: workoutProgram.difficulty_level,
      duration: workoutProgram.duration,
      category: workoutProgram.category,
      is_public: workoutProgram.is_public,
      level_access: workoutProgram.level_access,
      WorkoutDays: JSON.parse(JSON.stringify(workoutProgram.WorkoutDays)),
      member_id: workoutAssignment.member_id || '',
    }
  }

  try {
    const response = await fetch('http://127.0.0.1:8000/api/coach/status/', {
      credentials: 'include',
    })

    if (response.ok) {
      const data = await response.json()
      coachUserProfileId.value = data.user?.id || data.coach?.user || null
    } else {
      await fetchUserProfileId()
    }
  } catch (error) {
    console.error('Failed to fetch coach status:', error)
    await fetchUserProfileId()
  }
})

async function fetchUserProfileId() {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/user-info/', {
      credentials: 'include',
    })
    if (response.ok) {
      const data = await response.json()
      coachUserProfileId.value = data.user?.id
    }
  } catch (error) {
    console.error('Failed to fetch user profile:', error)
  }
}

interface Props {
  existingProgram?: {
    title: string
    description: string
    difficulty_level: string
    duration: number
    category: string
    WorkoutDays: Record<number, WorkoutDay[]>
  } | null
}

const props = defineProps<Props>()

const isEditing = computed(() => {
  return Boolean(props.existingProgram) || Boolean(editingProgramId.value)
})

const emit = defineEmits<{
  programCreated: [
    program: {
      title: string
      description: string
      difficulty_level: string
      duration: number
      category: string
      WorkoutDays: Record<number, WorkoutDay[]>
    },
  ]
  cancel: []
}>()

const backupWorkout = ref<WorkoutDay | null>(null)

interface WorkoutDay {
  day_number: number
  title: string
  duration: number
  type: string
  video_link: string
}

interface WorkoutProgram {
  title: string
  description: string
  difficulty_level: string
  duration: number
  category: string
  is_public: boolean
  level_access: string
  WorkoutDays: Record<number, WorkoutDay[]>
  member_id?: string
}

const workoutProgram = reactive<WorkoutProgram>({
  title: '',
  description: '',
  difficulty_level: '',
  duration: 30,
  category: '',
  is_public: true,
  level_access: 'all',
  WorkoutDays: {},
})

const currentWorkout = reactive<WorkoutDay>({
  day_number: 1,
  title: '',
  duration: 30,
  video_link: '',
  type: '',
})

const selectedDay = ref<number | ''>('')
const editingDay = ref<number | null>(null)
const editingWorkoutIndex = ref<number | null>(null)
const youtubeError = ref('')
const youtubeRegex =
  /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)[a-zA-Z0-9_-]{11}/

const workoutAssignment = reactive({
  member_id: '',
})

async function createAssignment(programId: number) {
  try {
    const payload = {
      program_id: programId,
      member_id: workoutAssignment.member_id,
    }

    const res = await fetch(`http://127.0.0.1:8000/api/member/assign/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
      body: JSON.stringify(payload),
    })

    if (!res.ok) {
      const err = await res.json().catch(() => null)
      alert('Failed to create assignment: ' + (err?.error || err?.detail || `HTTP ${res.status}`))
      return null
    }
    return await res.json()
  } catch (err) {
    console.error('Assignment create error', err)
    alert('Network error while creating assignment')
    return null
  }
}

const canSubmitProgram = computed(() => {
  return (
    workoutProgram.title &&
    workoutProgram.difficulty_level &&
    workoutProgram.duration &&
    Object.keys(workoutProgram.WorkoutDays).length > 0 &&
    !descriptionError.value
  )
})

const durationError = ref('')

function validateDuration() {
  const duration = currentWorkout.duration

  if (!duration || duration <= 0) {
    durationError.value = 'Duration must be a positive number'
    return false
  }

  if (duration < 5) {
    durationError.value = 'Duration must be at least 5 minutese'
    return false
  }

  if (duration > 180) {
    durationError.value = 'Duration cannot exceed 180 minutes'
    currentWorkout.duration = 180
    return false
  }

  if (!Number.isInteger(duration)) {
    currentWorkout.duration = Math.round(duration)
  }

  durationError.value = ''
  return true
}
function validatevideo_link() {
  youtubeError.value = ''
  if (!currentWorkout.video_link || currentWorkout.video_link.trim() === '') {
    return false
  }

  if (!youtubeRegex.test(currentWorkout.video_link)) {
    youtubeError.value = 'Please enter a valid YouTube URL'
    return false
  }
  return true
}

function saveDayWorkout() {
  if (!currentWorkout.title?.trim()) {
    alert('Please enter a workout title')
    return
  }

  if (!currentWorkout.duration || currentWorkout.duration <= 0) {
    alert('Duration must be a positive number')
    return
  }

  if (currentWorkout.duration < 5) {
    alert('Duration must be at least 5 minutes')
    currentWorkout.duration = 5
    return
  }

  if (currentWorkout.duration > 180) {
    alert('Duration cannot exceed 180 minutes')
    currentWorkout.duration = 180
    return
  }

  // Ensure duration is integer
  currentWorkout.duration = Math.round(currentWorkout.duration)

  // Validate YouTube URL if provided
  if (currentWorkout.video_link && currentWorkout.video_link.trim() !== '') {
    validatevideo_link()
    if (youtubeError.value) {
      alert('Please fix the YouTube URL error before saving')
      return
    }
  } else {
    alert('Please enter a YouTube video URL')
    return
  }

  const targetDay = editingDay.value || (selectedDay.value as number)

  const workout: WorkoutDay = {
    day_number: targetDay,
    title: currentWorkout.title.trim(),
    duration: currentWorkout.duration,
    video_link: currentWorkout.video_link.trim(),
    type: currentWorkout.type,
  }

  if (editingDay.value !== null && editingWorkoutIndex.value !== null) {
    workoutProgram.WorkoutDays[editingDay.value][editingWorkoutIndex.value] = workout
  } else {
    if (!workoutProgram.WorkoutDays[targetDay]) {
      workoutProgram.WorkoutDays[targetDay] = []
    }
    workoutProgram.WorkoutDays[targetDay].push(workout)
  }

  resetCurrentWorkout()
}

function editWorkout(day: number, workoutIndex: number) {
  const workout = workoutProgram.WorkoutDays[day]?.[workoutIndex]
  if (workout) {
    editingDay.value = day
    editingWorkoutIndex.value = workoutIndex
    selectedDay.value = ''
    currentWorkout.title = workout.title
    currentWorkout.duration = workout.duration
    currentWorkout.type = workout.type
    currentWorkout.video_link = workout.video_link
    currentWorkout.day_number = workout.day_number
    backupWorkout.value = { ...workout }
  }
}

function removeWorkout(day: number, workoutIndex: number) {
  if (workoutProgram.WorkoutDays[day]) {
    workoutProgram.WorkoutDays[day].splice(workoutIndex, 1)
    if (workoutProgram.WorkoutDays[day].length === 0) {
      delete workoutProgram.WorkoutDays[day]
    }
  }
}

function handleCancel() {
  if (editingProgramId.value && backupProgramData.value) {
    workoutProgram.title = backupProgramData.value.title
    workoutProgram.description = backupProgramData.value.description
    workoutProgram.difficulty_level = backupProgramData.value.difficulty_level
    workoutProgram.duration = backupProgramData.value.duration
    workoutProgram.category = backupProgramData.value.category
    workoutProgram.is_public = backupProgramData.value.is_public
    workoutProgram.level_access = backupProgramData.value.level_access
    workoutProgram.WorkoutDays = JSON.parse(JSON.stringify(backupProgramData.value.WorkoutDays))
    workoutAssignment.member_id = backupProgramData.value.member_id || ''
    router.push('/coach-dashboard')
  } else {
    resetProgram()
    router.push('/coach-dashboard')
  }
}

function cancelWorkoutEdit() {
  if (editingDay.value !== null && editingWorkoutIndex.value !== null && backupWorkout.value) {
    workoutProgram.WorkoutDays[editingDay.value][editingWorkoutIndex.value] = {
      ...backupWorkout.value,
    }
  }
  resetCurrentWorkout()
}

function resetCurrentWorkout() {
  selectedDay.value = ''
  editingDay.value = null
  editingWorkoutIndex.value = null
  backupWorkout.value = null

  currentWorkout.title = ''
  currentWorkout.duration = 30
  currentWorkout.type = ''
  currentWorkout.video_link = ''
  currentWorkout.day_number = 1
  youtubeError.value = ''
}

async function loadExistingProgram(programId: number) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/workout/programs/${programId}/`, {
      credentials: 'include',
    })

    if (!response.ok) {
      throw new Error(`Failed to load program: ${response.status}`)
    }

    const programData = await response.json()

    workoutProgram.title = programData.title || ''
    workoutProgram.description = programData.description || ''
    workoutProgram.difficulty_level = programData.difficulty_level || ''
    workoutProgram.duration = programData.duration || 30
    workoutProgram.category = programData.category || ''
    workoutProgram.is_public = programData.is_public ?? true
    workoutProgram.level_access = programData.level_access || 'all'

    workoutAssignment.member_id =
      programData.assignment?.member?.member_id || programData.assignment?.member_id || ''

    if (programData.days && Array.isArray(programData.days)) {
      workoutProgram.WorkoutDays = {}

      programData.days.forEach((day: any) => {
        const dayNumber = day.day_number
        if (!dayNumber) return

        // Initialize day array if missing
        if (!workoutProgram.WorkoutDays[dayNumber]) {
          workoutProgram.WorkoutDays[dayNumber] = []
        }

        // Handle multiple videos per day entry
        const videoLinks = day.video_links || []
        if (videoLinks.length > 0) {
          videoLinks.forEach((videoLink: string, index: number) => {
            const workout: WorkoutDay = {
              title:
                videoLinks.length > 1
                  ? `${day.title || `Day ${dayNumber}`} - Part ${index + 1}`
                  : day.title || `Day ${dayNumber}`,
              type: day.type || '',
              duration: Math.floor((day.duration || 30) / videoLinks.length),
              video_link: videoLink,
              day_number: dayNumber,
            }
            workoutProgram.WorkoutDays[dayNumber].push(workout)
          })
        } else {
          const workout: WorkoutDay = {
            title: day.title || `Day ${dayNumber}`,
            type: day.type || '',
            duration: day.duration || 30,
            video_link: '',
            day_number: dayNumber,
          }
          workoutProgram.WorkoutDays[dayNumber].push(workout)
        }
      })
    }
  } catch (error) {
    console.error('Error loading existing program:', error)
    alert('Failed to load program data. Please try again.')
  }
}

async function submitProgram() {
  if (!canSubmitProgram.value) {
    alert('Please fill in all required fields and add at least one daily workout')
    return
  }

  if (descriptionError.value) {
    alert('Please fix the description error before submitting')
    return
  }

  if (!coachUserProfileId.value) {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/user-info/', {
        credentials: 'include',
      })
      if (response.ok) {
        const data = await response.json()
        coachUserProfileId.value = data.user?.profile?.id
      }
    } catch (e) {
      console.error('UserProfile fetch retry failed', e)
    }
  }

  if (!coachUserProfileId.value) {
    alert(
      'Coach profile not found. Please create or confirm your coach profile before creating a program.',
    )
    return
  }

  const days = Object.entries(workoutProgram.WorkoutDays).flatMap(([day, workouts]) => {
    return workouts.map((workout) => ({
      day_number: Number(day),
      title: workout.title,
      type: workout.type || '',
      video_links: [workout.video_link].filter(Boolean), // Single video per workout
      duration: workout.duration,
    }))
  })

  const payload = {
    coach: coachUserProfileId.value,
    title: workoutProgram.title,
    description: workoutProgram.description,
    difficulty_level: workoutProgram.difficulty_level,
    level_access: workoutProgram.level_access || 'all',
    is_public: workoutProgram.is_public ?? true,
    duration: workoutProgram.duration,
    category: workoutProgram.category || 'full_body',
    days: days.map((day) => ({
      day_number: day.day_number,
      title: day.title,
      type: day.type || '',
      video_links: Array.isArray(day.video_links)
        ? day.video_links
        : [day.video_links].filter(Boolean),
      duration: day.duration,
    })),
  }

  const url = editingProgramId.value
    ? `http://127.0.0.1:8000/api/workout/programs/${editingProgramId.value}/`
    : 'http://127.0.0.1:8000/api/workout/programs/'

  try {
    const response = await fetch(url, {
      method: editingProgramId.value ? 'PUT' : 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
      body: JSON.stringify(payload),
    })

    const text = await response.text()
    let body = null
    try {
      body = JSON.parse(text)
    } catch {
      body = text
    }

    if (!response.ok) {
      console.error('Save program failed:', response.status, body)
      const message = body?.detail || body?.errors || body || `HTTP ${response.status}`
      alert('Failed to save program: ' + JSON.stringify(message))
      return
    }

    if (workoutProgram.is_public === false && workoutAssignment.member_id) {
      const assignment = await createAssignment(body.id)
      if (!assignment) {
        alert('Program saved but failed to create assignment for member.')
      }
    }

    emit('programCreated', body)
    alert('Program saved successfully!')
    router.push('/coach-dashboard')
  } catch (error) {
    console.error('Error saving program:', error)
    alert('Failed to save program: ' + error.message)
  }
}

function getCsrfToken() {
  const match = document.cookie.match(new RegExp('(^| )csrftoken=([^;]+)'))
  return match ? match[2] : ''
}

function resetProgram() {
  workoutProgram.title = ''
  workoutProgram.description = ''
  workoutProgram.difficulty_level = ''
  workoutProgram.duration = 30
  workoutProgram.category = ''
  workoutProgram.is_public = true
  workoutProgram.level_access = 'all'
  workoutProgram.WorkoutDays = {}
  editingProgramId.value = null
  backupProgramData.value = null
  workoutAssignment.member_id = ''
  descriptionError.value = ''

  resetCurrentWorkout()
}

watch(
  () => props.existingProgram,
  (program) => {
    if (program) {
      workoutProgram.title = program.title
      workoutProgram.description = program.description
      workoutProgram.difficulty_level = program.difficulty_level
      workoutProgram.duration = program.duration
      workoutProgram.category = program.category
      workoutProgram.is_public = (program as any).is_public ?? true
      workoutProgram.level_access = (program as any).level_access ?? 'all'
      workoutProgram.WorkoutDays = { ...program.WorkoutDays }
      workoutAssignment.member_id = (program as any).member_id || ''
    } else {
      resetProgram()
    }
  },
  { immediate: true },
)
</script>
