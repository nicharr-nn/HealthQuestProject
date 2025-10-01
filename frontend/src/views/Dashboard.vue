<template>
  <div class="silver-dashboard space-y-8">
    <!-- User Profile Header -->
    <div class="bg-white rounded-2xl p-6 shadow-[0_5px_15px_rgba(0,0,0,0.08)] space-y-6">
      <!-- use store.loading (your store has `loading`, not `loadingProfile`) -->
      <div v-if="store.loading" class="text-gray-500">Loading profile...</div>

      <div v-else>
        <div class="flex items-center justify-between gap-4 flex-wrap">
          <div class="flex items-center gap-4">
            <!-- Avatar: picture if available, else first-letter fallback -->
            <div class="w-16 h-16 min-w-16 min-h-16 rounded-full overflow-hidden bg-gradient-to-br from-neutral-300 to-neutral-400 flex items-center justify-center">
              <img
                v-if="store.profilePicture"
                :src="store.profilePicture"
                alt="Profile"
                class="w-full h-full object-cover"
              />
              <span v-else class="text-white text-2xl font-bold">{{ userInitial }}</span>
            </div>

            <div>
              <h2 class="text-2xl font-bold text-slate-800 leading-tight">
                {{ store.displayName }}
              </h2>
              <div class="text-slate-500 font-medium">Silver Level • Day 15 Streak</div>
            </div>
          </div>

          <div class="px-4 py-2 rounded-xl uppercase text-xs font-extrabold text-white bg-gradient-to-br from-neutral-300 to-neutral-400">
            Silver
          </div>
        </div>
      </div>

      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <div class="font-semibold text-gray-700">Progress to Gold</div>
          <div class="text-sm text-gray-500">{{ silverXp }}/{{ goldRequirement }} XP</div>
        </div>
        <div class="h-2 bg-gray-200 rounded-md overflow-hidden">
          <div
            class="h-full bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-md transition-[width] duration-700 ease-out"
            :style="{ width: progressPercentage + '%' }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Content Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6">
      <!-- Today's Workout -->
      <div class="bg-white rounded-2xl p-6 shadow-[0_5px_15px_rgba(0,0,0,0.08)] hover:-translate-y-0.5 transition">
        <div class="flex items-start justify-between mb-4">
          <div class="text-lg font-bold text-slate-800">Today's Workout</div>
          <div class="bg-gray-100 text-gray-500 px-3 py-1 rounded-xl text-xs font-semibold">45 min</div>
        </div>
        <div class="text-gray-600 mb-4 leading-relaxed">
          {{ todayWorkout.description }} • Earn +{{ todayWorkout.xp }} XP
        </div>
        <button
          class="w-full bg-gradient-to-br from-emerald-500 to-emerald-600 text-white font-semibold px-4 py-3 rounded-xl hover:-translate-y-0.5 transition"
          @click="startWorkout"
        >
          Start Workout
        </button>
      </div>

      <!-- Recipe Library -->
      <div class="bg-white rounded-2xl p-6 shadow-[0_5px_15px_rgba(0,0,0,0.08)] hover:-translate-y-0.5 transition">
        <div class="flex items-start justify-between mb-4">
          <div class="text-lg font-bold text-slate-800">🥗 Recipe Library</div>
          <div class="bg-emerald-500 text-white px-2.5 py-1 rounded-lg text-[10px] font-extrabold">NEW</div>
        </div>
        <div class="text-gray-600 mb-4 leading-relaxed">Access 100+ healthy recipes and meal plans</div>
        <button
          class="w-full bg-gray-100 text-gray-600 font-semibold px-4 py-3 rounded-xl hover:bg-gray-200 transition"
          @click="goToRecipes"
        >
          View Recipes
        </button>
      </div>

      <!-- Nutrition Tracking -->
      <div class="bg-white rounded-2xl p-6 shadow-[0_5px_15px_rgba(0,0,0,0.08)] hover:-translate-y-0.5 transition">
        <div class="flex items-start justify-between mb-4">
          <div class="text-lg font-bold text-slate-800">Nutrition Tracking</div>
          <div class="bg-gray-100 text-gray-500 px-3 py-1 rounded-xl text-xs font-semibold">Today</div>
        </div>
        <div class="text-gray-600 mb-4 leading-relaxed">Log your meals and track macros</div>
        <div class="mb-4 p-4 bg-slate-50 rounded-xl space-y-2">
          <div class="flex items-center justify-between text-sm" v-for="(value, key) in macroStats" :key="key">
            <span class="font-semibold text-gray-700">{{ key }}:</span>
            <span class="text-gray-600">{{ value.current }}g / {{ value.goal }}g</span>
          </div>
        </div>
        <button class="w-full bg-gray-100 text-gray-600 font-semibold px-4 py-3 rounded-xl hover:bg-gray-200 transition" @click="logMeal">
          Log Meal
        </button>
      </div>

      <!-- Advanced Analytics -->
      <div class="bg-white rounded-2xl p-6 shadow-[0_5px_15px_rgba(0,0,0,0.08)] hover:-translate-y-0.5 transition">
        <div class="flex items-start justify-between mb-4">
          <div class="text-lg font-bold text-slate-800">📊 Advanced Analytics</div>
          <div class="bg-gradient-to-br from-neutral-300 to-neutral-400 text-white px-2.5 py-1 rounded-lg text-[10px] font-extrabold">SILVER</div>
        </div>
        <div class="text-gray-600 mb-4 leading-relaxed">Detailed insights into your progress</div>
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div class="text-center p-4 bg-slate-50 rounded-xl">
            <div class="text-2xl font-extrabold text-emerald-600 mb-1">{{ analytics.weeklyImprovement }}%</div>
            <div class="text-xs text-gray-600">Weekly Improvement</div>
          </div>
          <div class="text-center p-4 bg-slate-50 rounded-xl">
            <div class="text-2xl font-extrabold text-emerald-600 mb-1">{{ analytics.consistency }}%</div>
            <div class="text-xs text-gray-600">Consistency Score</div>
          </div>
        </div>
        <button class="w-full bg-gray-100 text-gray-600 font-semibold px-4 py-3 rounded-xl hover:bg-gray-200 transition" @click="viewAnalytics">
          View Full Report
        </button>
      </div>

      <!-- Monthly Challenge -->
      <div class="bg-white rounded-2xl p-6 shadow-[0_5px_15px_rgba(0,0,0,0.08)] hover:-translate-y-0.5 transition">
        <div class="flex items-start justify-between mb-4">
          <div class="text-lg font-bold text-slate-800">Monthly Challenge</div>
          <div class="bg-gray-100 text-gray-500 px-3 py-1 rounded-xl text-xs font-semibold">{{ monthlyChallenge.daysLeft }} days left</div>
        </div>
        <div class="text-gray-600 mb-4 leading-relaxed">{{ monthlyChallenge.description }}</div>
        <div class="space-y-2 mb-4">
          <div class="h-2 bg-gray-200 rounded-md overflow-hidden">
            <div
              class="h-full bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-md transition-[width] duration-700 ease-out"
              :style="{ width: challengeProgress + '%' }"
            ></div>
          </div>
          <div class="text-center text-sm text-gray-600">
            {{ monthlyChallenge.completed }} / {{ monthlyChallenge.target }} completed
          </div>
        </div>
        <button class="w-full bg-gray-100 text-gray-600 font-semibold px-4 py-3 rounded-xl hover:bg-gray-200 transition" @click="viewChallenge">
          View Details
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

export default {
  name: 'Dashboard',
  setup() {
    const store = useUserStore()

    // Ensure global user/profile are loaded from your API once
    onMounted(async () => {
      // your store has `init()`, not `fetchMe()`
      if (!store.user && !store.profile) {
        await store.init()
      }
    })

    // Initial fallback if no picture
    const userInitial = computed(() => (store.displayName?.charAt(0) || 'U').toUpperCase())

    // 🧪 Demo data
    const silverXp = ref(195)
    const goldRequirement = ref(300)
    const todayWorkout = ref({ description: 'Strength training session', xp: 20 })
    const analytics = ref({ weeklyImprovement: 12, consistency: 89 })
    const monthlyChallenge = ref({ description: 'Complete 20 workouts this month', completed: 14, target: 20, daysLeft: 8 })

    const macroStats = ref({
      Protein: { current: 65, goal: 120 },
      Carbs: { current: 180, goal: 200 },
      Fat: { current: 45, goal: 60 }
    })

    // computed values
    const progressPercentage = computed(() => Math.round((silverXp.value / goldRequirement.value) * 100))
    const challengeProgress = computed(() => Math.round((monthlyChallenge.value.completed / monthlyChallenge.value.target) * 100))

    // methods (demo)
    const startWorkout = () => alert('Starting workout!')
    const goToRecipes = () => alert('Navigating to recipes...')
    const logMeal = () => alert('Opening meal logger...')
    const viewAnalytics = () => alert('Analytics details coming soon!')
    const viewChallenge = () => alert('Challenge details coming soon!')

    // Return all reactive data and methods to be used in template
    return {
      store,
      userInitial,
      silverXp,
      goldRequirement,
      todayWorkout,
      analytics,
      monthlyChallenge,
      macroStats,
      progressPercentage,
      challengeProgress,
      startWorkout,
      goToRecipes,
      logMeal,
      viewAnalytics,
      viewChallenge
    }
  }
}
</script>
