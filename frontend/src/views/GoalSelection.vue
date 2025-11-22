<template>
  <section class="max-w-6xl mx-auto px-6 py-12">
    <!-- Heading  -->
    <h1 class="font-subtitle text-5xl md:text-7xl text-center tracking-wide text-[#846757]">
      SELECT GOAL
    </h1>
    <p class="font-subtitle text-center text-xl md:text-2xl text-gray-500 mt-4">
      TO START YOUR JOURNEY
    </p>

    <!-- Selected Goal Indicator -->
    <div v-if="selectedGoal" class="mt-4 text-center">
      <div
        class="inline-flex items-center gap-2 bg-red-100 text-red-600 px-4 py-2 rounded-full font-body"
      >
        <span class="font-subtitle">{{ formatGoalName(selectedGoal) }} selected</span>
      </div>
    </div>

    <!-- Cards -->
    <div class="mt-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <button
        @click="selectGoal('lose_weight')"
        class="cursor-pointer text-left focus:outline-none transition-transform hover:scale-105"
      >
        <GoalCard
          title="LOSE WEIGHT"
          color="text-[#8C876A]"
          bg="bg-cardKhaki"
          titleColor="text-[#7D7858]"
          :selected="selectedGoal === 'lose_weight'"
          description="Shed pounds, and feel lighter."
          duration="3 months"
          focus="Weight Loss"
          level="Beginner"
        />
      </button>

      <button
        @click="selectGoal('build_muscle')"
        class="cursor-pointer text-left focus:outline-none transition-transform hover:scale-105 "
      >
        <GoalCard
          title="BUILD MUSCLE"
          color="text-[#417479]"
          bg="bg-cardBlue"
          titleColor="text-[#368492]"
          :selected="selectedGoal === 'build_muscle'"
          description="Gain strength, and feel powerful."
          duration="6 months"
          focus="Strength Training"
          level="Intermediate"
        />
      </button>

      <button
        @click="selectGoal('improve_endurance')"
        class="cursor-pointer text-left focus:outline-none transition-transform hover:scale-105"
      >
        <GoalCard
          title="IMPROVE ENDURANCE"
          color="text-[#C4847C]"
          bg="bg-cardPink"
          titleColor="text-[#9C6963]"
          :selected="selectedGoal === 'improve_endurance'"
          description="Boost stamina, and feel unstoppable."
          duration="2 months"
          focus="Cardio + Stamina"
          level="All Levels"
        />
      </button>

      <button
        @click="selectGoal('general_fitness')"
        class="cursor-pointer text-left focus:outline-none transition-transform hover:scale-105"
      >
        <GoalCard
          title="GENERAL FITNESS"
          color="text-[#7D6A8C]"
          bg="bg-purple-200"
          titleColor="text-[#5D4A6C]"
          :selected="selectedGoal === 'general_fitness'"
          description="Maintain health, and feel great."
          duration="1 year"
          focus="Overall Wellness"
          level="All Levels"
        />
      </button>
    </div>

    <!-- Continue Button -->
    <div class="mt-12 text-center">
      <button
        @click="saveGoal"
        :disabled="!selectedGoal || isLoading"
        class="bg-[#88ACEA] hover:bg-[#6a96d3] disabled:bg-gray-400 text-white font-bold py-3 px-8 rounded-full text-lg shadow-lg transition-colors disabled:cursor-not-allowed cursor-pointer"
      >
        <span v-if="isLoading">Saving...</span>
        <span v-else>Continue</span>
      </button>
      <p v-if="!selectedGoal" class="text-sm text-gray-500 mt-2">
        Please select a goal to continue
      </p>
    </div>
  </section>
</template>

<script setup>
import GoalCard from '../components/GoalCard.vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ref } from 'vue'
import { useToastStore } from '@/stores/toast'

const userStore = useUserStore()
const router = useRouter()
const selectedGoal = ref(null)
const isLoading = ref(false)
const toast = useToastStore()
const API_URL = 'http://127.0.0.1:8000'

function getCsrfToken() {
  const value = `; ${document.cookie}`
  const parts = value.split(`; csrftoken=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

function selectGoal(goal) {
  selectedGoal.value = goal
  userStore.setGoal(goal)
}

function formatGoalName(goalType) {
  const goalMap = {
    lose_weight: 'Lose Weight',
    build_muscle: 'Build Muscle',
    improve_endurance: 'Improve Endurance',
    general_fitness: 'General Fitness',
  }
  return goalMap[goalType] || goalType
}

async function saveGoal() {
  if (!selectedGoal.value) {
    toast.error('Please select a goal first')
    return
  }

  isLoading.value = true

  try {
    const csrfToken = getCsrfToken()
    const response = await fetch(`${API_URL}/api/user/select-goal/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken || '',
      },
      credentials: 'include',
      body: JSON.stringify({
        goal_type: selectedGoal.value,
        end_date: calculateEndDate(selectedGoal.value),
      }),
    })

    if (response.ok) {
      await response.json()
      router.push('/about-you')
    } else if (response.status === 400) {
      const error = await response.json()
      console.error('Error setting goal:', error)

      // Handle specific error for non-normal users
      if (
        error.user_profile &&
        error.user_profile.role !== 'normal' &&
        error.user_profile.role !== 'member'
      ) {
        router.push('/about-you')
      } else {
        toast.error('Failed to set goal: ' + (error.detail || JSON.stringify(error)))
      }
    } else {
      const error = await response.text()
      console.error('Error setting goal:', error)
      toast.error('Failed to set goal. Please try again.')
    }
  } catch (error) {
    console.error('Network error:', error)
    toast.error('Network error. Please check your connection and try again.')
  } finally {
    isLoading.value = false
  }
}

function calculateEndDate(goalType) {
  const today = new Date()
  const endDate = new Date()

  // Set different end dates based on goal type
  switch (goalType) {
    case 'lose_weight':
      endDate.setMonth(today.getMonth() + 3) // 3 months for weight loss
      break
    case 'build_muscle':
      endDate.setMonth(today.getMonth() + 6) // 6 months for muscle building
      break
    case 'improve_endurance':
      endDate.setMonth(today.getMonth() + 2) // 2 months for endurance
      break
    case 'general_fitness':
      endDate.setMonth(today.getMonth() + 12) // 1 year for general fitness
      break
    default:
      endDate.setMonth(today.getMonth() + 3)
  }

  return endDate.toISOString().split('T')[0] // Format as YYYY-MM-DD
}
</script>
