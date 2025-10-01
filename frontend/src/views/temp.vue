<template>
  <div class="silver-dashboard space-y-8">
    <!-- ... profile header ... -->

    <!-- Content Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6">
      
      <!-- Today's Workout -->
      <DashboardCard
        title="Today's Workout"
        :content="`${todayWorkout.description} • Earn +${todayWorkout.xp} XP`"
      >
        <template #badge>
          <div class="bg-gray-100 text-gray-500 px-3 py-1 rounded-xl text-xs font-semibold">
            {{ todayWorkout.duration || '30 min' }}
          </div>
        </template>
        <template #footer>
          <button
            class="w-full bg-gradient-to-br from-emerald-500 to-emerald-600 text-white font-semibold px-4 py-3 rounded-xl"
            @click="startWorkout"
          >
            Start Workout
          </button>
        </template>
      </DashboardCard>

      <!-- Recipe Library -->
      <DashboardCard
        title="Recipe Library"
        content="Access 100+ healthy recipes and meal plans"
        badge="NEW"
        badgeType="new"
      >
        <template #footer>
          <button
            class="w-full bg-gray-100 text-gray-600 font-semibold px-4 py-3 rounded-xl hover:bg-gray-200 transition"
            @click="goToRecipes"
          >
            View Recipes
          </button>
        </template>
      </DashboardCard>

      <!-- Advanced Analytics -->
      <DashboardCard
        title="Advanced Analytics"
        content="Detailed insights into your progress"
        badge="SILVER"
        badgeType="silver"
      >
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
      </DashboardCard>

      <!-- Monthly Challenge -->
      <DashboardCard
        title="Monthly Challenge"
        :content="monthlyChallenge.description"
      >
        <template #badge>
          <div class="bg-gray-100 text-gray-500 px-3 py-1 rounded-xl text-xs font-semibold">
            {{ monthlyChallenge.daysLeft }} days left
          </div>
        </template>
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
      </DashboardCard>
    </div>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import DashboardCard from '@/components/DashboardCard.vue'

export default {
  name: 'UserDashboard',
  components: { DashboardCard },
  setup() {
    const store = useUserStore()

    onMounted(async () => {
      if (!store.user || !store.profile) {
        await store.init()
      }
    })

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

    const todayWorkout = computed(() => store.profile?.today_workout || { description: 'No workout assigned', xp: 0 })
    const analytics = computed(() => store.profile?.analytics || { weeklyImprovement: 0, consistency: 0, current_streak: 0 })
    const monthlyChallenge = computed(() => store.profile?.monthlyChallenge || { description: 'No active challenge', completed: 0, target: 0, daysLeft: 0 })

    const challengeProgress = computed(() => {
      if (!monthlyChallenge.value.target) return 0
      return Math.min(100, Math.round((monthlyChallenge.value.completed / monthlyChallenge.value.target) * 100))
    })

    const startWorkout = () => alert('Starting workout!')
    const goToRecipes = () => alert('Navigating to recipes...')

    return {
      store,
      xp,
      currentLevel,
      streak,
      nextRequirement,
      progressPercentage,
      todayWorkout,
      analytics,
      monthlyChallenge,
      challengeProgress,
      startWorkout,
      goToRecipes
    }
  }
}
</script>
