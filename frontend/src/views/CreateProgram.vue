<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 py-6 font-body">
    <!-- Page Header -->
    <PageHeader :is-editing="isEditing" />

    <!-- Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- Program Details -->
      <ProgramDetailsForm
        v-model:program="workoutProgram"
        v-model:assignment="workoutAssignment"
        :members="coachMembers"
        :is-loading-members="isLoadingMembers"
        :description-error="descriptionError"
        :due-date-error="dueDateError"
        @validate-description="validateDescription"
        @validate-due-date="validateDueDate"
      />

      <!-- Workout Schedule -->
      <WorkoutSchedule
        :selected-day="selectedDay"
        @update:selected-day="selectedDay = $event"
        :current-workout="currentWorkout"
        @update:current-workout="updateCurrentWorkout"
        :duration="workoutProgram.duration"
        :workout-days="workoutProgram.WorkoutDays"
        :editing-day="editingDay"
        :youtube-error="youtubeError"
        :duration-error="durationError"
        @edit-workout="editWorkout"
        @remove-workout="removeWorkout"
        @save-workout="saveDayWorkout"
        @cancel-edit="cancelWorkoutEdit"
        @validate-youtube="validateYoutubeUrl"
        @validate-duration="validateDuration"
      />
    </div>

    <!-- Action Buttons -->
    <ActionButtons
      :can-submit="canSubmitProgram"
      :is-editing="isEditing"
      @submit="submitProgram"
      @reset="handleReset"
      @cancel="handleCancel"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import PageHeader from '@/components/createprogram/PageHeader.vue'
import ProgramDetailsForm from '@/components/createprogram/ProgramDetailsForm.vue'
import WorkoutSchedule from '@/components/createprogram/WorkoutSchedule.vue'
import ActionButtons from '@/components/createprogram/ActionButtons.vue'
import { useWorkoutProgram } from '@/composables/useWorkoutProgram'
import { useWorkoutValidation } from '@/composables/useWorkoutValidation'
import { useWorkoutApi } from '@/composables/useWorkoutApi'

const router = useRouter()
const route = useRoute()

// Initialize composables
const { workoutProgram, workoutAssignment, editingProgramId, isEditing, resetProgram } =
  useWorkoutProgram()

const {
  descriptionError,
  dueDateError,
  durationError,
  youtubeError,
  canSubmitProgram,
  validateDescription,
  validateDueDate,
  validateYoutubeUrl,
  validateDuration,
} = useWorkoutValidation(workoutProgram, workoutAssignment)

const { loadProgram, saveProgram, manageAssignment, deleteAssignment, fetchMembers } =
  useWorkoutApi()

// Component state
const coachMembers = ref([])
const isLoadingMembers = ref(false)
const selectedDay = ref('')
const editingDay = ref(null)
const editingWorkoutIndex = ref(null)
const backupWorkout = ref(null)
const backupProgramData = ref(null)
const coachUserProfileId = ref(null)

const currentWorkout = reactive({
  day_number: 1,
  title: '',
  duration: 30,
  video_link: '',
  type: '',
})

onMounted(async () => {
  const editId = route.query.edit

  // Fetch coach members
  isLoadingMembers.value = true
  coachMembers.value = await fetchMembers()
  isLoadingMembers.value = false

  await fetchCoachProfileId()

  // Load existing program if editing
  if (editId) {
    editingProgramId.value = parseInt(editId)
    await loadExistingProgram(editingProgramId.value)

    // Backup program data for cancel functionality
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
      due_date: workoutAssignment.due_date || '',
    }
  }
})

// Fetch coach profile ID
async function fetchCoachProfileId() {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/coach/status/', {
      credentials: 'include',
    })

    if (response.ok) {
      const data = await response.json()
      coachUserProfileId.value = data.user?.id || data.coach?.user || null
    } else {
      // Fallback to user-info endpoint
      const userResponse = await fetch('http://127.0.0.1:8000/api/user/user-info/', {
        credentials: 'include',
      })
      if (userResponse.ok) {
        const userData = await userResponse.json()
        coachUserProfileId.value = userData.user?.id
      }
    }
  } catch (error) {
    console.error('Failed to fetch coach profile:', error)
  }
}

// Load existing program
async function loadExistingProgram(programId) {
  try {
    const programData = await loadProgram(programId)

    // Map program data
    workoutProgram.title = programData.title || ''
    workoutProgram.description = programData.description || ''
    workoutProgram.difficulty_level = programData.difficulty_level || ''
    workoutProgram.duration = programData.duration || 30
    workoutProgram.category = programData.category || ''
    workoutProgram.is_public = programData.is_public ?? true
    workoutProgram.level_access = programData.level_access || 'all'

    // Map assignment data
    workoutAssignment.member_id =
      programData.assignment?.member?.member_id || programData.assignment?.member_id || ''
    workoutAssignment.due_date = programData.assignment?.due_date || ''

    // Map workout days
    if (programData.days && Array.isArray(programData.days)) {
      workoutProgram.WorkoutDays = {}

      programData.days.forEach((day) => {
        const dayNumber = day.day_number
        if (!dayNumber) return

        if (!workoutProgram.WorkoutDays[dayNumber]) {
          workoutProgram.WorkoutDays[dayNumber] = []
        }

        const videoLinks = day.video_links || []
        if (videoLinks.length > 0) {
          videoLinks.forEach((videoLink, index) => {
            const workout = {
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
          const workout = {
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

// Workout management
function saveDayWorkout() {
  // Validate workout data
  if (!currentWorkout.title?.trim()) {
    alert('Please enter a workout title')
    return
  }

  if (!validateDuration(currentWorkout.duration)) {
    alert('Please fix duration errors')
    return
  }

  if (!currentWorkout.video_link?.trim()) {
    alert('Please enter a YouTube video URL')
    return
  }

  if (!validateYoutubeUrl(currentWorkout.video_link)) {
    alert('Please enter a valid YouTube URL')
    return
  }

  const targetDay = editingDay.value || selectedDay.value

  const workout = {
    day_number: targetDay,
    title: currentWorkout.title.trim(),
    duration: currentWorkout.duration,
    video_link: currentWorkout.video_link.trim(),
    type: currentWorkout.type,
  }

  // Update existing workout or add new one
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

function editWorkout({ day, index }) {
  const workout = workoutProgram.WorkoutDays[day]?.[index]
  if (workout) {
    editingDay.value = day
    editingWorkoutIndex.value = index
    selectedDay.value = ''

    currentWorkout.title = workout.title
    currentWorkout.duration = workout.duration
    currentWorkout.type = workout.type
    currentWorkout.video_link = workout.video_link
    currentWorkout.day_number = workout.day_number

    backupWorkout.value = { ...workout }
  }
}

function removeWorkout({ day, index }) {
  if (confirm('Are you sure you want to remove this workout?')) {
    if (workoutProgram.WorkoutDays[day]) {
      workoutProgram.WorkoutDays[day].splice(index, 1)
      if (workoutProgram.WorkoutDays[day].length === 0) {
        delete workoutProgram.WorkoutDays[day]
      }
    }
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
}

// Program submission
async function submitProgram() {
  if (!canSubmitProgram.value) {
    alert('Please fill in all required fields and add at least one daily workout')
    return
  }

  if (!workoutProgram.is_public && !workoutAssignment.member_id) {
    alert('Please select a member for private programs')
    return
  }

  if (workoutAssignment.due_date && !validateDueDate()) {
    alert('Please fix the due date error')
    return
  }

  if (!coachUserProfileId.value) {
    alert('Coach profile not found. Please refresh and try again.')
    return
  }

  // Prepare workout days data
  const days = Object.entries(workoutProgram.WorkoutDays).flatMap(([day, workouts]) => {
    return workouts.map((workout) => ({
      day_number: Number(day),
      title: workout.title,
      type: workout.type || '',
      video_links: [workout.video_link].filter(Boolean),
      duration: workout.duration,
    }))
  })

  // Prepare program payload
  const programPayload = {
    coach: coachUserProfileId.value,
    title: workoutProgram.title,
    description: workoutProgram.description,
    difficulty_level: workoutProgram.difficulty_level,
    level_access: workoutProgram.level_access || 'all',
    is_public: workoutProgram.is_public ?? true,
    duration: workoutProgram.duration,
    category: workoutProgram.category || 'full_body',
    days: days,
  }

  try {
    // Save program
    const programData = await saveProgram(programPayload, isEditing.value, editingProgramId.value)

    // Handle assignment
    if (!workoutProgram.is_public && workoutAssignment.member_id) {
      await manageAssignment(programData.id, workoutAssignment, isEditing.value)
    } else if (workoutProgram.is_public && isEditing.value) {
      await deleteAssignment(programData.id)
    }

    const action = isEditing.value ? 'updated' : 'created'
    alert(`Program ${action} successfully!`)
    router.push('/coach-dashboard')
  } catch (error) {
    console.error('Error saving program:', error)
    alert('Failed to save program: ' + error.message)
  }
}

// Action handlers
function handleReset() {
  if (confirm('Are you sure you want to reset all fields?')) {
    resetProgram()
    resetCurrentWorkout()
  }
}

function handleCancel() {
  if (editingProgramId.value && backupProgramData.value) {
    // Restore backup data
    Object.assign(workoutProgram, {
      title: backupProgramData.value.title,
      description: backupProgramData.value.description,
      difficulty_level: backupProgramData.value.difficulty_level,
      duration: backupProgramData.value.duration,
      category: backupProgramData.value.category,
      is_public: backupProgramData.value.is_public,
      level_access: backupProgramData.value.level_access,
      WorkoutDays: JSON.parse(JSON.stringify(backupProgramData.value.WorkoutDays)),
    })
    workoutAssignment.member_id = backupProgramData.value.member_id || ''
    workoutAssignment.due_date = backupProgramData.value.due_date || ''
  }
  router.push('/coach-dashboard')
}

function updateCurrentWorkout(updatedWorkout) {
  Object.assign(currentWorkout, updatedWorkout)
}
</script>
