<template>
  <div class="space-y-8">
    <!-- Page Header -->
    <div class="text-center mb-12">
      <h1 class="text-4xl md:text-5xl font-black text-slate-800 uppercase tracking-tight mb-2">
        Maintain Health
      </h1>
      <p class="text-sm md:text-base text-slate-500 font-medium uppercase tracking-wider">
        by CAT (Coach) • 30 days • Bronze Level
      </p>
    </div>

    <!-- Program Progress -->
    <div class="bg-white rounded-2xl p-6 shadow-[0_5px_15px_rgba(0,0,0,0.08)] space-y-4">
      <div class="flex items-center justify-between gap-3 flex-wrap">
        <div class="flex-1">
          <div class="font-semibold text-gray-700">Program Progress</div>
          <div class="text-gray-500 text-sm">Day {{ currentDay }} of {{ totalDays }}</div>
        </div>
        <div class="bg-gray-100 text-gray-600 px-3 py-1.5 rounded-xl text-xs font-semibold">
          {{ currentDay }}/{{ totalDays }} Days
        </div>
      </div>

      <div class="h-2 bg-gray-200 rounded overflow-hidden">
        <div
          class="h-full bg-gradient-to-r from-emerald-500 to-emerald-600 rounded transition-[width] duration-700 ease-out"
          :style="{ width: programProgress + '%' }"
        ></div>
      </div>
    </div>

    <!-- Day Selector -->
    <div class="flex gap-2 mb-6 overflow-x-auto pb-2">
      <div
        v-for="day in visibleDays"
        :key="day"
        @click="selectDay(day)"
        class="min-w-20 px-4 py-3 rounded-full text-center text-sm font-semibold transition transform select-none whitespace-nowrap relative"
        :class="[
          selectedDay === day
            ? 'bg-indigo-600 text-white'
            : day < currentDay
              ? 'bg-emerald-500 text-white'
              : day > currentDay
                ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                : 'bg-gray-100 text-gray-600 hover:-translate-y-0.5'
        ]"
      >
        <span class="mr-1" v-if="day < currentDay">✓</span>
        <span class="mr-1" v-else-if="day > currentDay">🔒</span>
        Day {{ day }}
      </div>
    </div>

    <!-- Workout Content -->
    <div class="grid gap-6 grid-cols-1 md:grid-cols-2 xl:grid-cols-3">
      <div
        v-for="exercise in todayExercises"
        :key="exercise.id"
        class="bg-white rounded-2xl p-6 shadow-[0_5px_15px_rgba(0,0,0,0.08)] transition transform hover:-translate-y-0.5"
        :class="{
          'border-l-4 border-emerald-500': exercise.completed,
          'opacity-60 bg-slate-50 pointer-events-none': exercise.locked
        }"
      >
        <div class="flex items-start gap-4 mb-4">
          <div class="text-3xl leading-none">{{ exercise.icon }}</div>
          <div class="flex-1">
            <div class="text-lg font-bold text-slate-800">{{ exercise.title }}</div>
            <div class="text-sm font-medium text-gray-500">{{ exercise.duration }}</div>
          </div>
          <div
            v-if="exercise.completed"
            class="w-8 h-8 rounded-full bg-emerald-500 text-white grid place-items-center font-bold"
            title="Completed"
          >
            ✓
          </div>
        </div>

        <p class="text-gray-600 mb-4 leading-relaxed">
          {{ exercise.description }}
        </p>

        <div v-if="exercise.equipment" class="mb-4">
          <div class="font-semibold text-gray-700 text-sm mb-2">Equipment needed:</div>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="item in exercise.equipment"
              :key="item"
              class="bg-slate-100 text-slate-600 px-2 py-1 rounded-md text-xs font-medium"
            >
              {{ item }}
            </span>
          </div>
        </div>

        <div v-if="exercise.muscles" class="mb-4">
          <div class="font-semibold text-gray-700 text-sm mb-2">Target muscles:</div>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="muscle in exercise.muscles"
              :key="muscle"
              class="bg-slate-100 text-slate-600 px-2 py-1 rounded-md text-xs font-medium"
            >
              {{ muscle }}
            </span>
          </div>
        </div>

        <div class="mt-4">
          <button
            v-if="!exercise.locked"
            @click="startExercise(exercise)"
            class="w-full rounded-full font-semibold px-4 py-3 transition transform hover:-translate-y-0.5"
            :class="exercise.completed
              ? 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              : 'bg-gradient-to-br from-emerald-500 to-emerald-600 text-white'"
          >
            <span v-if="exercise.completed">✓ Completed</span>
            <span v-else-if="exercise.type === 'main'">▶ Start Now (+{{ exercise.xp }} XP)</span>
            <span v-else>▶ Watch Video</span>
          </button>

          <button
            v-else
            disabled
            class="w-full rounded-full font-semibold px-4 py-3 bg-gray-200 text-gray-400 cursor-not-allowed"
          >
            🔒 Complete previous exercises
          </button>
        </div>
      </div>
    </div>

    <!-- Exercise Modal -->
    <div
      v-if="showExerciseModal"
      class="fixed inset-0 bg-black/80 grid place-items-center z-50"
      @click="closeExerciseModal"
    >
      <div
        class="bg-white rounded-2xl p-6 w-[min(90vw,700px)] max-h-[90vh] overflow-y-auto shadow-xl"
        @click.stop
      >
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-slate-800 m-0">{{ selectedExercise?.title }}</h3>
          <button
            class="w-8 h-8 grid place-items-center rounded-full text-xl text-gray-500 hover:bg-gray-100"
            @click="closeExerciseModal"
            aria-label="Close"
          >
            ×
          </button>
        </div>

        <div class="space-y-2 mb-6">
          <div class="flex items-center justify-between border-b border-slate-100 py-2">
            <span class="font-semibold text-gray-700">Duration:</span>
            <span class="text-gray-600">{{ selectedExercise?.duration }}</span>
          </div>
          <div class="flex items-center justify-between border-b border-slate-100 py-2">
            <span class="font-semibold text-gray-700">Difficulty:</span>
            <span class="text-gray-600">{{ selectedExercise?.difficulty }}</span>
          </div>
          <div class="flex items-center justify-between border-b border-slate-100 py-2">
            <span class="font-semibold text-gray-700">XP Reward:</span>
            <span class="text-gray-600">+{{ selectedExercise?.xp }} XP</span>
          </div>
        </div>

        <div class="mb-6">
          <h4 class="text-slate-800 font-semibold mb-3">Instructions:</h4>
          <ol class="list-decimal pl-6 text-gray-700 leading-7 space-y-2">
            <li v-for="instruction in selectedExercise?.instructions" :key="instruction">
              {{ instruction }}
            </li>
          </ol>
        </div>

        <div v-if="!exerciseInProgress" class="flex flex-col sm:flex-row gap-3">
          <button
            class="flex-1 rounded-full px-4 py-3 font-semibold bg-gradient-to-br from-emerald-500 to-emerald-600 text-white"
            @click="beginExercise"
          >
            Begin Exercise
          </button>
          <button
            class="flex-1 rounded-full px-4 py-3 font-semibold bg-gray-100 text-gray-700 hover:bg-gray-200"
            @click="closeExerciseModal"
          >
            Maybe Later
          </button>
        </div>

        <div v-else class="text-center py-4 space-y-4">
          <div class="text-5xl font-bold text-emerald-500 font-mono">
            {{ formatTime(timeRemaining) }}
          </div>

          <div class="w-full h-2 bg-gray-200 rounded overflow-hidden">
            <div
              class="h-full bg-gradient-to-r from-emerald-500 to-emerald-600 rounded transition-[width] duration-300"
              :style="{ width: timerProgress + '%' }"
            ></div>
          </div>

          <div class="flex flex-col sm:flex-row gap-3">
            <button
              class="flex-1 rounded-full px-4 py-3 font-semibold bg-gray-100 text-gray-700 hover:bg-gray-200"
              @click="pauseExercise"
            >
              {{ isPaused ? '▶ Resume' : '⏸ Pause' }}
            </button>
            <button
              class="flex-1 rounded-full px-4 py-3 font-semibold bg-gradient-to-br from-emerald-500 to-emerald-600 text-white"
              @click="completeExercise"
            >
              Complete Exercise
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onUnmounted } from 'vue'

export default {
  name: 'WorkoutProgram',
  setup() {
    const currentDay = ref(5)
    const totalDays = ref(30)
    const selectedDay = ref(5)
    const showExerciseModal = ref(false)
    const selectedExercise = ref(null)
    const exerciseInProgress = ref(false)
    const timeRemaining = ref(0)
    const totalTime = ref(0)
    const isPaused = ref(false)
    const timer = ref(null)

    const programProgress = computed(() => Math.round((currentDay.value / totalDays.value) * 100))

    const visibleDays = computed(() => {
      const start = Math.max(1, currentDay.value - 3)
      const end = Math.min(totalDays.value, currentDay.value + 3)
      const days = []
      for (let i = start; i <= end; i++) days.push(i)
      return days
    })

    const timerProgress = computed(() => (totalTime.value === 0 ? 0 : ((totalTime.value - timeRemaining.value) / totalTime.value) * 100))

    const exercises = ref({
      5: [
        {
          id: 1,
          title: '10 min Warm-up',
          duration: '10 minutes',
          description: 'Dynamic stretches and mobility exercises',
          icon: '🏃‍♀️',
          type: 'warmup',
          xp: 5,
          completed: true,
          locked: false,
          difficulty: 'Easy',
          equipment: ['None'],
          muscles: ['Full body'],
          instructions: [
            'Start with light marching in place for 2 minutes',
            'Perform arm circles - 30 seconds each direction',
            'Do leg swings - 30 seconds each leg',
            'Hip circles - 30 seconds each direction',
            'Light jumping jacks for 2 minutes',
            'Cool down with gentle stretching'
          ]
        },
        {
          id: 2,
          title: '10 min Abs',
          duration: '10 minutes',
          description: 'Core strengthening and stability work',
          icon: '💪',
          type: 'strength',
          xp: 10,
          completed: true,
          locked: false,
          difficulty: 'Medium',
          equipment: ['Yoga mat'],
          muscles: ['Core', 'Abs', 'Obliques'],
          instructions: [
            'Plank hold - 3 sets of 30 seconds',
            'Bicycle crunches - 3 sets of 20 each side',
            'Russian twists - 3 sets of 30',
            'Mountain climbers - 3 sets of 20',
            'Dead bug - 3 sets of 10 each side',
            'Cool down with gentle spinal twists'
          ]
        },
        {
          id: 3,
          title: '30 min HIIT',
          duration: '30 minutes',
          description: 'High intensity interval training session',
          icon: '🔥',
          type: 'main',
          xp: 15,
          completed: false,
          locked: false,
          difficulty: 'Hard',
          equipment: ['None', 'Optional: dumbbells'],
          muscles: ['Full body', 'Cardio'],
          instructions: [
            'Warm-up: 5 minutes light movement',
            'Round 1: Burpees - 45 seconds work, 15 seconds rest',
            'Round 2: Jump squats - 45 seconds work, 15 seconds rest',
            'Round 3: Push-ups - 45 seconds work, 15 seconds rest',
            'Round 4: High knees - 45 seconds work, 15 seconds rest',
            'Repeat circuit 4 times',
            'Cool-down: 5 minutes stretching'
          ]
        }
      ]
    })

    const todayExercises = computed(() => exercises.value[selectedDay.value] || [])

    const selectDay = (day) => {
      if (day <= currentDay.value) selectedDay.value = day
    }

    const startExercise = (exercise) => {
      selectedExercise.value = exercise
      showExerciseModal.value = true
    }

    const closeExerciseModal = () => {
      showExerciseModal.value = false
      selectedExercise.value = null
      exerciseInProgress.value = false
      if (timer.value) {
        clearInterval(timer.value)
        timer.value = null
      }
    }

    const beginExercise = () => {
      exerciseInProgress.value = true
      const duration = parseInt(selectedExercise.value.duration)
      timeRemaining.value = duration * 60
      totalTime.value = duration * 60
      isPaused.value = false

      timer.value = setInterval(() => {
        if (!isPaused.value && timeRemaining.value > 0) timeRemaining.value--
        if (timeRemaining.value === 0) completeExercise()
      }, 1000)
    }

    const pauseExercise = () => {
      isPaused.value = !isPaused.value
    }

    const completeExercise = () => {
      if (timer.value) {
        clearInterval(timer.value)
        timer.value = null
      }
      const exercise = exercises.value[selectedDay.value].find(e => e.id === selectedExercise.value.id)
      if (exercise) {
        exercise.completed = true
        const currentIndex = exercises.value[selectedDay.value].findIndex(e => e.id === selectedExercise.value.id)
        if (currentIndex < exercises.value[selectedDay.value].length - 1) {
          exercises.value[selectedDay.value][currentIndex + 1].locked = false
        }
      }
      alert(`Exercise completed! You earned +${selectedExercise.value.xp} XP!`)
      closeExerciseModal()
    }

    const formatTime = (seconds) => {
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }

    onUnmounted(() => {
      if (timer.value) clearInterval(timer.value)
    })

    return {
      currentDay,
      totalDays,
      selectedDay,
      programProgress,
      visibleDays,
      todayExercises,
      showExerciseModal,
      selectedExercise,
      exerciseInProgress,
      timeRemaining,
      timerProgress,
      isPaused,
      selectDay,
      startExercise,
      closeExerciseModal,
      beginExercise,
      pauseExercise,
      completeExercise,
      formatTime
    }
  }
}
</script>
