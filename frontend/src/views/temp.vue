<template>
  <div class="silver-dashboard space-y-8">
    <!-- User Profile Header -->
    <div class="bg-white rounded-2xl p-6 shadow space-y-6">
      <div v-if="store.loading" class="text-gray-500">Loading profile...</div>

      <div v-else>
        <div class="flex items-center justify-between gap-4 flex-wrap">
          <div class="flex items-center gap-4">
            <!-- Avatar -->
            <div class="w-16 h-16 rounded-full overflow-hidden bg-gradient-to-br from-neutral-300 to-neutral-400 flex items-center justify-center">
              <img
                v-if="store.profilePicture"
                :src="store.profilePicture"
                alt="Profile"
                class="w-full h-full object-cover"
              />
              <span v-else class="text-white text-2xl font-bold">{{ userInitial }}</span>
            </div>

            <div>
              <h2 class="font-subtitle text-2xl text-slate-700">{{ store.displayName }}</h2>
              <div class="font-body text-slate-500 font-medium">{{ currentLevel }} - Day {{ streak }} streak</div>
            </div>
          </div>

          <div
            class="font-body px-4 py-2 rounded-xl uppercase text-xs font-extrabold text-white"
            :class="{
              'bg-gradient-to-br from-amber-400 to-yellow-500': currentLevel === 'Gold',
              'bg-gradient-to-br from-gray-400 to-gray-500': currentLevel === 'Silver',
              'bg-gradient-to-br from-[#CE8946] to-[#FCA956]': currentLevel === 'Bronze'
            }"
          >
            {{ currentLevel }}
          </div>
        </div>
      </div>

      <!-- Progress bar -->
      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <div class="font-body font-semibold text-gray-700">Progress to next level</div>
          <div class="text-sm text-gray-500">{{ xp }}/{{ nextRequirement }} XP</div>
        </div>
        <div class="font-body h-2 bg-gray-200 rounded-md overflow-hidden">
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
      <div class="bg-white rounded-2xl p-6 shadow hover:-translate-y-0.5 transition">
        <div class="flex items-start justify-between mb-4">
          <div class="text-lg font-bold text-slate-800">Today's Workout</div>
          <div class="bg-gray-100 text-gray-500 px-3 py-1 rounded-xl text-xs font-semibold">{{ todayWorkout.duration || '30 min' }}</div>
        </div>
        <div class="text-gray-600 mb-4">{{ todayWorkout.description }} • Earn +{{ todayWorkout.xp }} XP</div>
        <button class="w-full bg-gradient-to-br from-emerald-500 to-emerald-600 text-white font-semibold px-4 py-3 rounded-xl" @click="startWorkout">
          Start Workout
        </button>
      </div>

      <!-- Recipe Library -->
      <div class="bg-white rounded-2xl p-6 shadow hover:-translate-y-0.5 transition">
        <div class="flex items-start justify-between mb-4">
          <div class="text-lg font-bold text-slate-800">Recipe Library</div>
          <div class="bg-emerald-500 text-white px-2.5 py-1 rounded-lg text-[10px] font-extrabold">NEW</div>
        </div>
        <div class="text-gray-600 mb-4">Access 100+ healthy recipes and meal plans</div>
        <button class="w-full bg-gray-100 text-gray-600 font-semibold px-4 py-3 rounded-xl hover:bg-gray-200 transition" @click="goToRecipes">
          View Recipes
        </button>
      </div>

      <!-- Advanced Analytics -->
      <div class="bg-white rounded-2xl p-6 shadow hover:-translate-y-0.5 transition">
        <div class="flex items-start justify-between mb-4">
          <div class="text-lg font-bold text-slate-800">Advanced Analytics</div>
          <div class="bg-gradient-to-br from-neutral-300 to-neutral-400 text-white px-2.5 py-1 rounded-lg text-[10px] font-extrabold">SILVER</div>
        </div>
        <div class="text-gray-600 mb-4">Detailed insights into your progress</div>
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
      </div>

      <!-- Monthly Challenge -->
      <div class="bg-white rounded-2xl p-6 shadow hover:-translate-y-0.5 transition">
        <div class="flex items-start justify-between mb-4">
          <div class="text-lg font-bold text-slate-800">Monthly Challenge</div>
          <div class="bg-gray-100 text-gray-500 px-3 py-1 rounded-xl text-xs font-semibold">{{ monthlyChallenge.daysLeft }} days left</div>
        </div>
        <div class="text-gray-600 mb-4">{{ monthlyChallenge.description }}</div>
        <div class="space-y-2 mb-4">
          <div class="h-2 bg-gray-200 rounded-md overflow-hidden">
            <div class="h-full bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-md transition-[width] duration-700 ease-out" :style="{ width: challengeProgress + '%' }"></div>
          </div>
          <div class="text-center text-sm text-gray-600">
            {{ monthlyChallenge.completed }} / {{ monthlyChallenge.target }} completed
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

export default {
  name: 'UserDashboard',
  setup() {
    const store = useUserStore()

    onMounted(async () => {
      if (!store.user || !store.profile) {
        await store.init()
      }
    })

    const userInitial = computed(() => (store.displayName?.charAt(0) || 'U').toUpperCase())

    // --- XP + Level ---
    const xp = computed(() => store.level?.xp || 0)
    const currentLevel = computed(() => store.level?.level || 'Bronze')
    const streak = computed(() => store.profile?.analytics?.current_streak || 0)

    const nextRequirement = computed(() => {
      if (store.level?.level_rank === 1) return 1000
      if (store.level?.level_rank === 2) return 5000
      return null
    })

    const progressPercentage = computed(() => {
      if (!nextRequirement.value) return 100
      return Math.min(100, Math.round((xp.value / nextRequirement.value) * 100))
    })

    // --- API-driven fields ---
    const todayWorkout = computed(() => store.profile?.today_workout || { description: 'No workout assigned', xp: 0 })
    const analytics = computed(() => store.profile?.analytics || { weeklyImprovement: 0, consistency: 0, current_streak: 0 })
    const monthlyChallenge = computed(() => store.profile?.monthlyChallenge || { description: 'No active challenge', completed: 0, target: 0, daysLeft: 0 })

    const challengeProgress = computed(() => {
      if (!monthlyChallenge.value.target) return 0
      return Math.min(100, Math.round((monthlyChallenge.value.completed / monthlyChallenge.value.target) * 100))
    })

    // --- Methods ---
    const startWorkout = () => alert('Starting workout!')
    const goToRecipes = () => alert('Navigating to recipes...')
    const viewAnalytics = () => alert('Analytics details coming soon!')
    const viewChallenge = () => alert('Challenge details coming soon!')

    return {
      store,
      userInitial,
      xp,
      currentLevel,
      nextRequirement,
      progressPercentage,
      todayWorkout,
      analytics,
      monthlyChallenge,
      challengeProgress,
      streak,
      startWorkout,
      goToRecipes,
      viewAnalytics,
      viewChallenge
    }
  }
}
</script>
