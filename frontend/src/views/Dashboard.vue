<template>
  <div class="silver-dashboard space-y-8">
    <!-- User Profile Header -->
    <div class="bg-white rounded-2xl p-6 shadow shadow-slate-200 space-y-6">
      <div v-if="loading" class="text-gray-500">Loading profile...</div>

      <div v-else>
        <div class="flex items-center justify-between gap-4 flex-wrap">
          <div class="flex items-center gap-4">
            <div class="w-16 h-16 rounded-full overflow-hidden bg-gradient-to-br from-neutral-300 to-neutral-400 flex items-center justify-center">
              <img
                v-if="profile?.photo"
                :src="profile.photo"
                alt="Profile Photo"
                class="w-full h-full object-cover"
              />
              <span v-else class="text-white text-2xl font-bold">{{ userInitial }}</span>
            </div>

            <div>
              <h2 class="text-2xl font-bold text-slate-800 leading-tight">
                {{ user?.username }}
              </h2>
              <div class="text-slate-500 font-medium">
                {{ profile?.current_level?.level || 'Bronze' }} • 
                {{ profile?.current_goal || 'No Goal Set' }}
              </div>
            </div>
          </div>

          <div class="px-4 py-2 rounded-xl uppercase text-xs font-extrabold text-white bg-gradient-to-br from-neutral-300 to-neutral-400">
            {{ profile?.current_level?.level || 'Bronze' }}
          </div>
        </div>
      </div>

      <!-- Progress Bar -->
      <div v-if="profile?.current_level" class="space-y-2">
        <div class="flex items-center justify-between">
          <div class="font-semibold text-gray-700">Progress to Next Level</div>
          <div class="text-sm text-gray-500">
            {{ profile.current_level.xp }} XP
          </div>
        </div>
        <div class="h-2 bg-gray-200 rounded-md overflow-hidden">
          <div
            class="h-full bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-md transition-[width] duration-700 ease-out"
            :style="{ width: progressPercentage + '%' }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Example card: Today's Workout -->
    <div class="bg-white rounded-2xl p-6 shadow hover:-translate-y-0.5 transition">
      <div class="flex items-start justify-between mb-4">
        <div class="text-lg font-bold text-slate-800">Today's Workout</div>
        <div class="bg-gray-100 text-gray-500 px-3 py-1 rounded-xl text-xs font-semibold">
          {{ todayWorkout.duration || '30 min' }}
        </div>
      </div>
      <div class="text-gray-600 mb-4 leading-relaxed">
        {{ todayWorkout.description || 'No workout assigned today' }}
      </div>
      <button
        class="w-full bg-gradient-to-br from-emerald-500 to-emerald-600 text-white font-semibold px-4 py-3 rounded-xl"
        @click="startWorkout"
      >
        Start Workout
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const loading = ref(true)
const user = ref(null)
const profile = ref(null)
const todayWorkout = ref({})
const error = ref(null)

const userInitial = computed(() => {
  return user.value?.username ? user.value.username.charAt(0).toUpperCase() : '?'
})

const progressPercentage = computed(() => {
  if (!profile.value?.current_level) return 0
  const xp = profile.value.current_level.xp
  const needed = profile.value.current_level.goal_achieved ? 100 : 2000 // fallback
  return Math.min(100, (xp / needed) * 100)
})

async function fetchUserProfile() {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/user-info/', {
        credentials: 'include',
    })
    if (!response.ok) throw new Error('Failed to load user info')

    const data = await response.json()
    user.value = {
      id: data.user.id,
      username: data.user.username,
      profile_complete: data.user.profile_complete,
    }

    console.log('User data:', user.value)
    profile.value = {
        photo : `http://127.0.0.1:8000${data.user.profile.photo}`,
        current_level: data.user.profile.current_level,
        current_goal: data.user.profile.current_goal,
    }

    userStore.setAuthStatus(
      true,
      data.user.profile,
      data.user.profile_complete
    )
    
    console.log('Store after update:', {
      isAuthenticated: userStore.isAuthenticated,
      profile_complete: userStore.profile_complete,
      profile: userStore.profile
    })

  } catch (err) {
    console.error(err)
    error.value = err.message
    userStore.clearAuthStatus()
  } finally {
    loading.value = false
  }
}


// async function fetchTodayWorkout() {
//   try {
//     const response = await fetch('/api/assignment/1/', {
//       headers: {
//         'Authorization': `Bearer ${store.token}`
//       }
//     })
//     if (response.ok) {
//       todayWorkout.value = await response.json()
//     }
//   } catch (err) {
//     console.error(err)
//   }
// }

function startWorkout() {
  alert('Starting workout...')
}

onMounted(() => {
  fetchUserProfile()
//   fetchTodayWorkout()
})
</script>
