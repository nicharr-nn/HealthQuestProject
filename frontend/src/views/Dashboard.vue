<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-100 via-yellow-50 to-gray-100 p-8">
    <!-- Header with Stats -->
    <div class="max-w-7xl mx-auto mb-8">
      <h1 class="font-subtitle text-4xl font-bold text-[#846757] mb-6">Welcome back, {{ store.displayName }}</h1>
      
      <!-- Quick Stats Bar -->
      <div class="font-body flex gap-8 items-center">
        <div class="flex items-center gap-2">
          <span class="text-m text-gray-600">Current Level</span>
          <div 
            class="px-4 py-1 rounded-full text-m font-semibold text-white"
            :class="{
              'bg-gradient-to-br from-amber-400 to-yellow-500': currentLevel === 'Gold',
              'bg-gradient-to-br from-gray-400 to-gray-500': currentLevel === 'Silver',
              'bg-gradient-to-br from-[#CE8946] to-[#FCA956]': currentLevel === 'Bronze'
            }"
          >
            {{ currentLevel }}
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-m text-gray-600">Streak</span>
          <div class="bg-yellow-300 text-gray-800 px-4 py-1 rounded-full text-sm font-semibold">
            {{ streak }} days
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-m text-gray-600">Progress</span>
          <div class="bg-gray-300 text-gray-700 px-4 py-1 rounded-full text-sm font-semibold">
            {{ progressPercentage }}%
          </div>
        </div>
        
        <!-- Right side stats -->
        <div class="ml-auto flex gap-12">
          <div class="text-right">
            <div class="text-3xl font-bold text-gray-800">{{ xp }}</div>
            <div class="text-sm text-gray-600">Total XP</div>
          </div>
          <div class="text-right">
            <div class="text-3xl font-bold text-gray-800">{{ nextRequirement || 'MAX' }}</div>
            <div class="text-sm text-gray-600">Next Level</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="max-w-7xl mx-auto grid grid-cols-12 gap-6">
      <!-- Left Column: Profile Card -->
      <div class="col-span-3 space-y-6">
        <!-- Profile Card -->
        <div class="font-body bg-gradient-to-br from-[#88ACEA] to-gray-500 rounded-3xl p-8 text-white shadow-xl overflow-hidden relative">
          <div class="relative z-10">
            <div class="w-32 h-32 rounded-full overflow-hidden mx-auto mb-6 border-4 border-white/30 shadow-lg">
              <img
                v-if="store.profilePicture"
                :src="store.profilePicture"
                alt="Profile"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full bg-white/20 flex items-center justify-center">
                <span class="text-4xl font-bold">{{ userInitial }}</span>
              </div>
            </div>
            
            <div class="text-center mb-6">
              <h3 class="text-xl font-bold mb-1">{{ store.displayName }}</h3>
              <p class="text-sm text-white/80">{{ currentLevel }} Level</p>
            </div>
            
            <div class="bg-white/20 backdrop-blur-sm rounded-2xl px-4 py-3 text-center">
              <div class="text-sm text-white/80 mb-1">Current XP</div>
              <div class="text-2xl font-bold">{{ xp }}</div>
            </div>
          </div>
          
          <!-- Decorative circles -->
          <div class="absolute -top-10 -right-10 w-40 h-40 bg-white/10 rounded-full"></div>
          <div class="absolute -bottom-10 -left-10 w-40 h-40 bg-white/10 rounded-full"></div>
        </div>

      </div>

      <!-- Middle Column: Main Content -->
      <div class="col-span-6 space-y-6">
        <!-- XP Progress Card -->
        <div class="bg-white rounded-3xl p-8 shadow-lg">
          <div class="font-body flex items-start justify-between mb-6">
            <div>
              <h3 class="font-subtitle text-2xl font-bold text-gray-800">XP Progress</h3>
              <p class="text-gray-600 mt-1">Keep going to reach {{ currentLevel === 'Bronze' ? 'Silver' : 'Gold' }}!</p>
            </div>
            <button class="text-gray-400 hover:text-gray-600 transition-colors">
            </button>
          </div>
          
          <div class="mb-6">
            <div class="flex items-center justify-between mb-2">
              <span class="font-body text-sm font-medium text-gray-600">Progress to next level</span>
              <span class="font-body text-sm font-bold text-gray-800">{{ xp }} / {{ nextRequirement || 'MAX' }} XP</span>
            </div>
            <div class="h-3 bg-gray-200 rounded-full overflow-hidden">
              <div
                class="h-full bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-full transition-all duration-700 ease-out"
                :style="{ width: progressPercentage + '%' }"
              ></div>
            </div>
          </div>

          <!-- Weekly Activity Chart -->
          <div class="mt-8">
            <h4 class="font-body text-sm font-semibold text-gray-700 mb-4">Weekly Activity</h4>
            <div class="flex items-end justify-between h-32 gap-3">
              <div v-for="(day, i) in weekDays" :key="i" class="flex-1 flex flex-col items-center gap-2">
                <div class="relative w-full flex items-end justify-center" style="height: 100px;">
                  <div 
                    class="w-3 rounded-t-lg transition-all duration-500 hover:opacity-80 cursor-pointer"
                    :class="day.isActive ? 'bg-yellow-300' : 'bg-gray-800'"
                    :style="{ height: day.height + '%' }"
                  ></div>
                </div>
                <div class="text-xs text-gray-500 font-medium">{{ day.label }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Today's Workout Card -->
        <div class="bg-white rounded-3xl p-8 shadow-lg">
          <div class="flex items-start justify-between mb-4">
            <div class="font-body">
              <h3 class="font-subtitle text-2xl font-bold text-gray-800">Today's Workout</h3>
              <div class="flex items-center gap-2 mt-2">
                <span class="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-xs font-semibold">
                  {{ todayWorkout.duration || '30 min' }}
                </span>
                <span class="bg-emerald-100 text-emerald-700 px-3 py-1 rounded-full text-xs font-semibold">
                  +{{ todayWorkout.xp }} XP
                </span>
              </div>
            </div>
          </div>
          
          <p class="text-gray-600 mb-6">{{ todayWorkout.description || 'No workout assigned today' }}</p>
          
          <button 
            @click="startWorkout"
            class="w-full bg-gradient-to-br from-emerald-600 to-emerald-700 hover:from-[#225560] hover:to-[#225560] text-white font-semibold px-6 py-4 rounded-2xl transition-all duration-200 shadow-lg hover:shadow-xl"
          >
            Start Workout
          </button>
        </div>

      </div>

      <!-- Right Column: Additional Cards -->
      <div class="col-span-3 space-y-6">
        <!-- Advanced Analytics Card -->
        <div class="bg-white rounded-3xl p-6 shadow-lg">
          <div class="flex items-start justify-between mb-4">
            <h3 class="font-subtitle font-semibold text-lg font-bold text-gray-800">Analytics</h3>
          </div>
          
          <p class="text-sm text-gray-600 mb-6">Detailed insights into your progress</p>
          
          <div class="space-y-4">
            <div class="text-center p-4 bg-gradient-to-br from-[#99e2b4] to-[#99e2b4] rounded-2xl">
              <div class="text-3xl font-extrabold text-[#004e64] mb-1">{{ analytics.weeklyImprovement }}%</div>
              <div class="text-xs text-gray-700 font-medium">Weekly Improvement</div>
            </div>
            <div class="text-center p-4 bg-gradient-to-br from-[#a8d5e2] to-[#a8d5e2] rounded-2xl">
              <div class="text-3xl font-extrabold text-[#05668d] mb-1">{{ analytics.consistency }}%</div>
              <div class="text-xs text-gray-700 font-medium">Consistency Score</div>
            </div>
          </div>
        </div>

        <!-- Recipe Library Card -->
        <div class="bg-gradient-to-br from-[#f4e285] to-[#f4a259] rounded-3xl p-6 shadow-lg">
          <div class="flex items-start justify-between mb-4">
            <h3 class="font-subtitle text-lg text-gray-800">Recipe Library</h3>
            <div class="font-body bg-emerald-500 text-white px-2.5 py-1 rounded-lg text-[10px] font-extrabold">
              NEW
            </div>
          </div>
          
          <p class="text-sm text-gray-700 mb-6">Access 10+ healthy recipes and meal plans</p>
          
          <button 
            @click="goToRecipes"
            class="w-full bg-white hover:bg-gray-50 text-gray-800 font-semibold px-4 py-3 rounded-xl transition-colors shadow-sm"
          >
            View Recipes
          </button>
        </div>
        
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="store.loading" class="fixed inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl p-8 shadow-2xl">
        <div class="text-gray-600 font-medium">Loading your dashboard...</div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue'
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

    // --- XP + Level (Keep your existing logic) ---
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

    // --- API-driven fields  ---
    const todayWorkout = computed(() => store.profile?.today_workout || { description: 'No workout assigned', xp: 0 })
    const analytics = computed(() => store.profile?.analytics || { weeklyImprovement: 0, consistency: 0, current_streak: 0 })

    // --- Weekly activity chart data (mock)---
    const weekDays = ref([
      { label: 'M', height: 40, isActive: false },
      { label: 'T', height: 65, isActive: false },
      { label: 'W', height: 50, isActive: false },
      { label: 'T', height: 75, isActive: false },
      { label: 'F', height: 85, isActive: true },
      { label: 'S', height: 30, isActive: false },
      { label: 'S', height: 20, isActive: false }
    ])

    // --- Methods (Keep your existing methods) ---
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
      streak,
      weekDays,
      startWorkout,
      goToRecipes,
      viewAnalytics,
      viewChallenge
    }
  }
}
</script>