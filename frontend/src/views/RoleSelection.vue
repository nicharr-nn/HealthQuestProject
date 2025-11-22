<template>
  <section class="max-w-6xl mx-auto px-4 sm:px-6 py-12">
    <!-- Heading -->
    <h1
      class="font-subtitle text-3xl sm:text-4xl md:text-6xl lg:text-7xl text-center tracking-wide text-[#846757]"
    >
      SELECT ROLE
    </h1>
    <p
      class="font-subtitle text-center text-base sm:text-lg md:text-2xl text-gray-500 mt-4 leading-relaxed"
    >
      Choose your role to get started on your fitness journey. Each role offers different features
      and capabilities tailored to your needs.
    </p>

    <!-- Cards -->
    <div class="mt-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
      <button @click="selectRole('member')" class="text-left w-full">
        <RoleCard
          title="MEMBER"
          :points="memberPoints"
          color="text-[#8C876A]"
          bg="bg-cardKhaki"
          titleColor="text-[#7D7858]"
        />
      </button>

      <button @click="selectRole('normal')" class="text-left w-full">
        <RoleCard
          title="NORMAL USER"
          :points="normalUserPoints"
          color="text-[#417479]"
          bg="bg-cardBlue"
          titleColor="text-[#368492]"
        />
      </button>

      <button @click="selectRole('coach')" class="text-left w-full">
        <RoleCard
          title="COACH"
          :points="coachPoints"
          color="text-[#C4847C]"
          bg="bg-cardPink"
          titleColor="text-[#9C6963]"
        />
      </button>
    </div>
  </section>
</template>

<script setup>
import RoleCard from '../components/RoleCard.vue'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

const userStore = useUserStore()
const toast = useToastStore()
const API_URL = 'http://127.0.0.1:8000'
const router = useRouter()

const memberPoints = [
  'All Normal User features',
  'Follow coach-assigned workout programs',
  'Post food privately for coach feedback',
  'Get personalized workout schedules',
]

const normalUserPoints = [
  'Choose fitness goals',
  'Earn XP through workouts and daily activities',
  'Progress through Bronze, Silver, Gold level',
  'Access recipes based on your level',
]

const coachPoints = [
  'Design custom workout programs',
  'Assign daily workout schedules to members',
  'Monitor member progress and completion rates',
  'View and comment on client food posts',
  'Post recipes for the community',
]

function getCsrfToken() {
  const value = `; ${document.cookie}`
  const parts = value.split(`; csrftoken=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

async function selectRole(role) {
  userStore.setRole(role)

  try {
    const response = await fetch(`${API_URL}/api/user/select-role/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
      credentials: 'include',
      body: JSON.stringify({ role }),
    })

    if (response.ok) {
      if (role !== 'coach') {
        router.push('/select-goal')
      } else {
        router.push('/about-you')
      }
    } else {
      const error = await response.json()
      console.error('Error setting role:', error)
      toast.error('Failed to set role')
    }
  } catch (error) {
    console.error(error)
    toast.error('Error setting role')
  }
}

onMounted(async () => {
  try {
    const res = await fetch(`${API_URL}/api/user/user-info/`, {
      credentials: 'include',
    })
    const data = await res.json()

    if (data.isAuthenticated) {
      const profile = data.user?.profile || {}

      if (!profile.role) {
        return
      }

      const nonCoach = profile.role === 'member' || profile.role === 'normal'
      if (nonCoach && (!profile.current_goal || profile.current_goal === '')) {
        router.replace('/select-goal')
        return
      }

      if (!profile.height || !profile.weight) {
        router.replace('/about-you')
        return
      }

      if (profile.role === 'coach') {
        router.replace('/coach-portal')
      } else {
        router.replace('/dashboard')
      }
    }
  } catch (error) {
    console.error('Error fetching user info:', error)
  }
})
</script>
