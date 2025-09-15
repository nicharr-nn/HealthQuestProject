<!-- BronzeDashboard.vue -->
<template>
  <div class="p-4">
    <!-- User Profile Header -->
    <div class="bg-white rounded-xl p-6 shadow-md mb-8">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-6 mb-6">
        <!-- Left Section -->
        <div class="flex items-center">
          <div
            class="w-16 h-16 rounded-full mr-4 flex items-center justify-center text-white text-2xl font-bold bg-gradient-to-br from-[#cd7f32] to-[#b8860b]"
          >
            {{ userInitial }}
          </div>
          <div>
            <h2 class="text-xl font-bold text-slate-800">{{ userData.name }}</h2>
            <div class="text-gray-500 font-medium">
              Bronze Level • Day {{ userData.streak }} Streak
            </div>
          </div>
        </div>
        <!-- Right Badge -->
        <div
          class="px-4 py-2 rounded-full text-xs font-bold uppercase text-white bg-gradient-to-br from-[#cd7f32] to-[#b8860b]"
        >
          Bronze
        </div>
      </div>

      <!-- Progress Bar -->
      <div class="mt-4">
        <div class="flex justify-between items-center mb-2">
          <div class="font-semibold text-gray-700">Progress to Silver</div>
          <div class="text-sm text-gray-500">
            {{ userData.xp }}/{{ userData.totalXpForNextLevel }} XP
          </div>
        </div>
        <div class="h-2 bg-gray-200 rounded overflow-hidden">
          <div
            class="h-full bg-gradient-to-r from-emerald-500 to-emerald-600 transition-all duration-700"
            :style="{ width: progressPercentage + '%' }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Content Grid -->
    <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3 mb-8">
      <!-- Today's Workout -->
      <div class="bg-white rounded-xl p-6 shadow-md hover:-translate-y-1 transition">
        <div class="flex justify-between items-start mb-4">
          <div class="text-lg font-bold text-slate-800">Today's Workout</div>
          <div class="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-xs font-semibold">
            Day {{ currentDay }}
          </div>
        </div>
        <div class="text-gray-500 mb-4">
          {{ todayWorkout.description }} • Earn +{{ todayWorkout.xp }} XP
        </div>
        <button
          class="w-full py-3 rounded-full font-semibold text-white bg-gradient-to-br from-emerald-500 to-emerald-600 hover:-translate-y-0.5 transition"
          @click="startWorkout"
        >
          Start Workout
        </button>
      </div>

      <!-- Weekly Challenge -->
      <div class="bg-white rounded-xl p-6 shadow-md hover:-translate-y-1 transition">
        <div class="flex justify-between items-start mb-4">
          <div class="text-lg font-bold text-slate-800">Weekly Challenge</div>
          <div class="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-xs font-semibold">
            {{ weeklyChallenge.timeLeft }} days
          </div>
        </div>
        <div class="text-gray-500 mb-2">{{ weeklyChallenge.description }}</div>
        <div class="text-emerald-500 font-semibold mb-4">
          {{ weeklyChallenge.completed }}/{{ weeklyChallenge.total }} Complete
        </div>
        <button
          class="w-full py-3 rounded-full font-semibold bg-gray-100 text-gray-600 hover:bg-gray-200 transition"
          @click="viewProgress"
        >
          View Progress
        </button>
      </div>

      <!-- Locked Recipe Library -->
      <div class="relative bg-white rounded-xl p-6 shadow-md opacity-60">
        <div class="text-lg font-bold text-slate-800 mb-2">Recipe Library</div>
        <div class="text-gray-500">Unlock healthy recipes at Silver level</div>
        <div
          class="absolute inset-0 bg-black/80 flex flex-col items-center justify-center text-white rounded-xl"
        >
          <div class="text-2xl mb-2">🔒</div>
          <div class="font-semibold mb-1">Unlock at Silver Level</div>
          <div class="text-sm opacity-80">{{ xpNeeded }} XP to go!</div>
        </div>
      </div>

      <!-- Achievements -->
      <div class="bg-white rounded-xl p-6 shadow-md hover:-translate-y-1 transition">
        <div class="flex justify-between items-start mb-4">
          <div class="text-lg font-bold text-slate-800">Recent Achievements</div>
          <div class="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-xs font-semibold">
            New
          </div>
        </div>
        <div class="flex flex-col gap-3">
          <div
            v-for="achievement in recentAchievements"
            :key="achievement.id"
            class="flex items-center p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition"
          >
            <span class="text-xl mr-3">{{ achievement.icon }}</span>
            <div class="flex-1">
              <div class="font-semibold text-slate-800">{{ achievement.name }}</div>
              <div class="text-sm text-gray-500">{{ achievement.description }}</div>
            </div>
            <div class="bg-emerald-500 text-white px-2 py-1 rounded text-xs font-semibold">
              +{{ achievement.xp }} XP
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="bg-white rounded-xl p-6 shadow-md hover:-translate-y-1 transition">
        <div class="text-lg font-bold text-slate-800 mb-4">Quick Stats</div>
        <div class="grid grid-cols-3 gap-4 text-center">
          <div>
            <div class="text-xl font-bold text-slate-800 mb-1">
              {{ stats.workoutsCompleted }}
            </div>
            <div class="text-xs text-gray-500 uppercase tracking-wide">Workouts</div>
          </div>
          <div>
            <div class="text-xl font-bold text-slate-800 mb-1">{{ stats.totalMinutes }}</div>
            <div class="text-xs text-gray-500 uppercase tracking-wide">Minutes</div>
          </div>
          <div>
            <div class="text-xl font-bold text-slate-800 mb-1">{{ stats.caloriesBurned }}</div>
            <div class="text-xs text-gray-500 uppercase tracking-wide">Calories</div>
          </div>
        </div>
      </div>

      <!-- Tips -->
      <div class="bg-white rounded-xl p-6 shadow-md hover:-translate-y-1 transition">
        <div class="flex justify-between items-start mb-4">
          <div class="text-lg font-bold text-slate-800">Daily Tip</div>
          <div class="text-xl">💡</div>
        </div>
        <div class="text-gray-500 mb-4">{{ dailyTip }}</div>
        <button
          class="w-full py-3 rounded-full font-semibold bg-gray-100 text-gray-600 hover:bg-gray-200 transition"
          @click="getNewTip"
        >
          Get New Tip
        </button>
      </div>
    </div>

    <!-- Workout Modal -->
    <div
      v-if="showWorkoutModal"
      class="fixed inset-0 bg-black/80 flex items-center justify-center z-50 animate-fadeIn"
      @click="closeWorkoutModal"
    >
      <div
        class="bg-white rounded-2xl p-8 text-center w-full max-w-md animate-slideUp"
        @click.stop
      >
        <h3 class="text-xl font-bold text-slate-800 mb-6">Starting Workout Session!</h3>
        <div class="space-y-2 text-left mb-6">
          <div class="flex items-center p-3 bg-slate-50 rounded-lg">
            <span class="mr-3 text-lg">🏃‍♀️</span>
            <span>10 min Warm-up</span>
          </div>
          <div class="flex items-center p-3 bg-slate-50 rounded-lg">
            <span class="mr-3 text-lg">💪</span>
            <span>10 min Abs</span>
          </div>
          <div class="flex items-center p-3 bg-slate-50 rounded-lg">
            <span class="mr-3 text-lg">🔥</span>
            <span>30 min HIIT</span>
          </div>
        </div>
        <p class="text-emerald-500 font-semibold mb-6">You've got this! 💪</p>
        <div class="flex flex-col sm:flex-row gap-3">
          <button
            class="flex-1 py-3 rounded-full font-semibold text-white bg-gradient-to-br from-emerald-500 to-emerald-600"
            @click="proceedToWorkout"
          >
            Let's Go!
          </button>
          <button
            class="flex-1 py-3 rounded-full font-semibold bg-gray-100 text-gray-600 hover:bg-gray-200 transition"
            @click="closeWorkoutModal"
          >
            Maybe Later
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"

const props = defineProps({
  userData: {
    type: Object,
    default: () => ({
      name: "Katie",
      level: "Bronze",
      streak: 5,
      xp: 48,
      totalXpForNextLevel: 150,
    }),
  },
})

const emit = defineEmits(["page-change"])

const showWorkoutModal = ref(false)
const currentDay = ref(5)

const userInitial = computed(() => props.userData.name.charAt(0).toUpperCase())
const progressPercentage = computed(() =>
  Math.round((props.userData.xp / props.userData.totalXpForNextLevel) * 100)
)
const xpNeeded = computed(() => props.userData.totalXpForNextLevel - props.userData.xp)

const todayWorkout = ref({ description: "30-min HIIT session", xp: 15 })
const weeklyChallenge = ref({
  description: "Complete 5 workouts this week",
  completed: 4,
  total: 5,
  timeLeft: 5,
})
const recentAchievements = ref([
  { id: 1, icon: "🏆", name: "First Week", description: "Completed your first week!", xp: 25 },
  { id: 2, icon: "🔥", name: "Streak Master", description: "5-day workout streak", xp: 15 },
])
const stats = ref({ workoutsCompleted: 12, totalMinutes: 360, caloriesBurned: 2450 })

const tips = [
  "Stay hydrated! Drink water before, during, and after your workout.",
  "Focus on proper form rather than speed to prevent injuries.",
  "Get adequate sleep - your muscles grow during rest, not just exercise.",
  "Don't forget to warm up before intense exercises.",
  "Listen to your body - rest days are just as important as workout days.",
]
const dailyTip = ref(tips[0])

const startWorkout = () => (showWorkoutModal.value = true)
const closeWorkoutModal = () => (showWorkoutModal.value = false)
const proceedToWorkout = () => {
  closeWorkoutModal()
  emit("page-change", "workout-program")
}
const viewProgress = () => alert("Weekly progress: 4/5 workouts completed. Keep going!")
const getNewTip = () => (dailyTip.value = tips[Math.floor(Math.random() * tips.length)])
</script>

<style>
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-slideUp {
  animation: slideUp 0.3s ease-out;
}
</style>
