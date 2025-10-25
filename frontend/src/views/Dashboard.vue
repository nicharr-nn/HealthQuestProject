<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-100 via-yellow-50 to-gray-100 p-4 sm:p-6 lg:p-8">
    <!-- Header with Stats -->
    <div class="max-w-7xl mx-auto mb-6 sm:mb-8">
      <h1 class="font-subtitle text-2xl sm:text-3xl lg:text-4xl text-[#846757] mb-4 sm:mb-6">
        Welcome back, {{ store.displayName }}
      </h1>
      
      <!-- Quick Stats Bar -->
      <div class="font-body flex flex-wrap gap-4 sm:gap-6 lg:gap-8 items-center">
        <div class="flex items-center gap-2">
          <span class="text-sm sm:text-base text-gray-600">Current Level</span>
          <div 
            class="px-3 sm:px-4 py-1 rounded-full text-sm font-semibold text-white"
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
          <span class="text-sm sm:text-base text-gray-600">Streak</span>
          <div class="bg-yellow-300 text-gray-800 px-3 sm:px-4 py-1 rounded-full text-sm font-semibold">
            {{ streak }} days
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-sm sm:text-base text-gray-600">Progress</span>
          <div class="bg-gray-300 text-gray-700 px-3 sm:px-4 py-1 rounded-full text-sm font-semibold">
            {{ progressPercentage }}%
          </div>
        </div>
        
        <!-- Right side stats -->
        <div class="ml-auto flex gap-6 sm:gap-8 lg:gap-12">
          <div class="text-right">
            <div class="text-xl sm:text-2xl lg:text-3xl font-bold text-gray-800">{{ xp }}</div>
            <div class="text-xs sm:text-sm text-gray-600">Total XP</div>
          </div>
          <div class="text-right">
            <div class="text-xl sm:text-2xl lg:text-3xl font-bold text-gray-800">{{ nextRequirement || 'MAX' }}</div>
            <div class="text-xs sm:text-sm text-gray-600">Next Level</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-6">
      <!-- Left Column: Profile Card -->
      <div class="lg:col-span-3 space-y-4 sm:space-y-6">
        <!-- Profile Card -->
        <div class="font-body bg-gradient-to-br from-[#88ACEA] to-[#88ACEA] rounded-3xl p-6 sm:p-8 text-white shadow-xl overflow-hidden relative h-full min-h-[400px] flex flex-col justify-center">
          <div class="relative z-10">
            <div class="w-24 h-24 sm:w-32 sm:h-32 rounded-full overflow-hidden mx-auto mb-4 sm:mb-6 border-4 border-white/30 shadow-lg">
              <img
                v-if="store.profilePicture"
                :src="store.profilePicture"
                alt="Profile"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full bg-white/20 flex items-center justify-center">
                <span class="text-3xl sm:text-4xl font-bold">{{ userInitial }}</span>
              </div>
            </div>
            
            <div class="text-center mb-4 sm:mb-6">
              <h3 class="text-lg sm:text-xl font-bold mb-1">{{ store.displayName }}</h3>
              <p class="text-sm text-white/80">{{ currentLevel }} Level</p>
            </div>
            
            <div class="bg-white/20 backdrop-blur-sm rounded-2xl px-4 py-3 text-center">
              <div class="text-sm text-white/80 mb-1">Current XP</div>
              <div class="text-xl sm:text-2xl font-bold">{{ xp }}</div>
            </div>
          </div>
          
          <!-- Decorative circles -->
          <div class="absolute -top-10 -right-10 w-32 h-32 sm:w-40 sm:h-40 bg-white/10 rounded-full"></div>
          <div class="absolute -bottom-10 -left-10 w-32 h-32 sm:w-40 sm:h-40 bg-white/10 rounded-full"></div>
        </div>
      </div>

      <!-- Middle Column: Main Content -->
      <div class="lg:col-span-6 space-y-4 sm:space-y-6">
        <!-- XP Progress Card -->
        <div class="bg-white rounded-3xl p-6 sm:p-8 shadow-lg">
          <div class="font-body flex flex-col sm:flex-row items-start justify-between mb-4 sm:mb-6 gap-2">
            <div>
              <h3 class="font-subtitle text-xl sm:text-2xl text-gray-800">XP Progress</h3>
              <p class="text-sm sm:text-base text-gray-600 mt-1">
                Keep going to reach {{ currentLevel === 'Bronze' ? 'Silver' : 'Gold' }}!
              </p>
            </div>
          </div>
          
          <div class="mb-4 sm:mb-6">
            <div class="flex items-center justify-between mb-2">
              <span class="font-body text-xs sm:text-sm font-medium text-gray-600">Progress to next level</span>
              <span class="font-body text-xs sm:text-sm text-gray-800">{{ xp }} / {{ nextRequirement || 'MAX' }} XP</span>
            </div>
            <div class="h-2 sm:h-3 bg-gray-200 rounded-full overflow-hidden">
              <div
                class="h-full bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-full transition-all duration-700 ease-out"
                :style="{ width: progressPercentage + '%' }"
              ></div>
            </div>
          </div>

          <!-- Weekly Activity Chart -->
          <div class="mt-6 sm:mt-8">
            <h4 class="font-body text-xs sm:text-sm font-semibold text-gray-700 mb-3 sm:mb-4">Weekly Activity</h4>
            <div class="flex items-end justify-between h-24 sm:h-32 gap-2 sm:gap-3">
              <div v-for="(day, i) in weekDays" :key="i" class="flex-1 flex flex-col items-center gap-1 sm:gap-2">
                <div class="relative w-full flex items-end justify-center h-16 sm:h-24">
                  <div 
                    class="w-2 sm:w-3 rounded-t-lg transition-all duration-500 hover:opacity-80 cursor-pointer"
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
        <div class="bg-white rounded-3xl p-6 sm:p-8 shadow-lg">
          <div v-if="store.profile?.role === 'member'" class="flex flex-col sm:flex-row items-start justify-between mb-4 gap-2">
            <div class="font-body w-full">
              <h3 class="font-subtitle text-xl sm:text-2xl text-gray-800">Today's Workout</h3>
              <div class="flex flex-wrap items-center gap-2 mt-2">
                <span class="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-xs font-semibold">
                  {{ todayWorkout.duration || '30 min' }}
                </span>
                <span class="bg-emerald-100 text-emerald-700 px-3 py-1 rounded-full text-xs font-semibold">
                  +{{ todayWorkout.xp }} XP
                </span>
              </div>
            </div>
            
            <p class="text-sm sm:text-base text-gray-600 mb-4 sm:mb-6">
              {{ todayWorkout.description || 'No workout assigned today' }}
            </p>
          </div>
          
          <button 
            @click="startWorkout"
            class="w-full bg-gradient-to-br from-emerald-500 to-emerald-500 hover:from-[#225560] hover:to-[#225560] text-white font-semibold px-6 py-3 sm:py-4 rounded-2xl transition-all duration-200 shadow-lg hover:shadow-xl text-sm sm:text-base"
          >
            Start Workout
          </button>
        </div>
      </div>

      <!-- Right Column: Additional Cards -->
      <div class="lg:col-span-3 space-y-4 sm:space-y-6">
        <!-- Advanced Analytics Card -->
        <div class="bg-white rounded-3xl p-5 sm:p-6 shadow-lg">
          <div class="flex items-start justify-between mb-3 sm:mb-4">
            <h3 class="font-subtitle text-base sm:text-lg text-gray-800">Analytics</h3>
          </div>
          
          <p class="text-xs sm:text-sm text-gray-600 mb-4 sm:mb-6">Detailed insights into your progress</p>
          
          <div class="space-y-3 sm:space-y-4">
            <div class="text-center p-3 sm:p-4 bg-gradient-to-br from-[#F3C6C1] to-[#F3C6C1] rounded-2xl">
              <div class="text-2xl sm:text-3xl font-extrabold text-[#9C6963] mb-1">{{ analytics.weeklyImprovement }}%</div>
              <div class="text-xs text-gray-700 font-medium">Weekly Improvement</div>
            </div>
            <div class="text-center p-3 sm:p-4 bg-gradient-to-br from-[#a8d5e2] to-[#a8d5e2] rounded-2xl">
              <div class="text-2xl sm:text-3xl font-extrabold text-[#05668d] mb-1">{{ analytics.consistency }}%</div>
              <div class="text-xs text-gray-700 font-medium">Consistency Score</div>
            </div>
          </div>
        </div>

        <!-- Recipe Library Card -->
        <div v-if="currentLevel !== 'Bronze'" class="bg-gradient-to-br from-[#f4e285] to-[#f4e285] rounded-3xl p-5 sm:p-6 shadow-lg">
          <div class="flex items-start justify-between mb-3 sm:mb-4">
            <h3 class="font-subtitle text-base sm:text-lg text-gray-800">Recipe Library</h3>
            <div class="font-body bg-emerald-500 text-white px-2.5 py-1 rounded-lg text-[10px] font-extrabold">
              NEW
            </div>
          </div>
          
          <p class="text-xs sm:text-sm text-gray-700 mb-4 sm:mb-6">Access 10+ healthy recipes and meal plans</p>
          
          <button 
            @click="goToRecipes"
            class="w-full bg-white hover:bg-gray-50 text-gray-800 font-semibold px-4 py-2 sm:py-3 rounded-xl transition-colors shadow-sm text-sm sm:text-base"
          >
            View Recipes
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="store.loading" class="fixed inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-2xl mx-4">
        <div class="text-gray-600 font-medium text-sm sm:text-base">Loading your dashboard...</div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

export default {
  name: 'UserDashboard',
  setup() {
    const store = useUserStore()
    const router = useRouter()

    onMounted(async () => {
      if (!store.user || !store.profile) {
        await store.init()
      }
      await loadWeeklyActivity()
      await loadAnalytics()
    })

    const userInitial = computed(() => (store.displayName?.charAt(0) || 'U').toUpperCase())

    // --- XP + Level ---
    const xp = computed(() => store.level?.xp || 0)
    const currentLevel = computed(() => store.level?.level || 'Bronze')
    const streak = computed(() => analytics.value.current_streak || 0)

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
    const analyticsRaw = ref(null)
    const loadingAnalytics = ref(false)
    const analyticsError = ref(null)

    const analytics = computed(() => analyticsRaw.value ?? { weeklyImprovement: 0, consistency: 0, current_streak: 0 })
    const todayWorkout = computed(() => store.profile?.today_workout || { description: 'No workout assigned', xp: 0 })

    async function loadAnalytics() {
      loadingAnalytics.value = true
      analyticsError.value = null
      try {
        const res = await fetch('http://127.0.0.1:8000/api/workout/analytics/', {
          credentials: 'include'
        })
        if (!res.ok) {
          const err = await res.json().catch(() => ({}))
          analyticsError.value = err.detail || `HTTP ${res.status}`
          analyticsRaw.value = null
          return
        }
        const data = await res.json()
        analyticsRaw.value = data.analytics || {}
      } catch (err) {
        analyticsError.value = err.message || String(err)
        analyticsRaw.value = null
      } finally {
        loadingAnalytics.value = false
      }
    }

    // --- Weekly activity chart data ---
    const weekDays = ref([
      { label: 'M', height: 40, isActive: false },
      { label: 'T', height: 65, isActive: false },
      { label: 'W', height: 50, isActive: false },
      { label: 'T', height: 75, isActive: false },
      { label: 'F', height: 85, isActive: true },
      { label: 'S', height: 30, isActive: false },
      { label: 'S', height: 20, isActive: false }
    ])

    async function loadWeeklyActivity() {
      try {
        const res = await fetch('http://127.0.0.1:8000/api/workout/analytics/weekly-activity/', {
          credentials: 'include'
        })
        if (!res.ok) {
          console.error('Failed to load weekly activity', res.status)
          return
        }
        const data = await res.json()
        // expect data: [{ label, height, isActive, date?, count? }, ...]
        if (Array.isArray(data) && data.length === 7) {
          weekDays.value = data.map(item => ({
            label: item.label ?? (new Date(item.date || '').toLocaleDateString(undefined, { weekday: 'short' }).charAt(0) || '?'),
            // ensure height is a number (frontend uses height + '%')
            height: typeof item.height === 'number' ? item.height : Math.max(20, Math.min(100, (item.count || 0) * 10)),
            isActive: !!item.isActive || (item.count || 0) > 0
          }))
        } else {
          console.warn('Unexpected weekly-activity response shape', data)
        }
      } catch (err) {
        console.error('Error fetching weekly activity', err)
      }
    }


    const startWorkout = () => {
      router.push('/workout').catch(() => {})
    }

    const goToRecipes = () => {
      router.push('/food-recipe').catch(() => {})
    }

    return {
      store,
      userInitial,
      xp,
      currentLevel,
      nextRequirement,
      progressPercentage,
      todayWorkout,
      analytics,
      loadingAnalytics,
      analyticsError,
      streak,
      weekDays,
      startWorkout,
      goToRecipes,
    }
  }
}
</script>