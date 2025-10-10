<template>
  <div class="min-h-screen p-6 font-subtitle">
    <!-- Loading & Error States -->
    <div v-if="loading" class="text-center text-gray-500">Loading program...</div>
    <div v-else-if="error" class="text-center text-red-500">{{ error }}</div>

    <div v-else>
      <!-- Program Title -->
      <h1 class="text-4xl font-bold text-center mb-8">{{ program.title }}</h1>

      <!-- 🧭 Day Selector -->
      <div class="relative max-w-6xl mx-auto mb-8 rounded-full bg-[#E3CFD8]">
        <button 
          @click="scrollLeft"
          class="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-white rounded-full p-2 shadow-md hover:shadow-lg transition-shadow"
        >
          <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <div ref="daysContainer" class="flex gap-4 overflow-x-auto scrollbar-hide px-12 py-4 scroll-smooth">
          <div
            v-for="day in days"
            :key="day.id"
            @click="selectDay(day.id)"
            :class="[
              'flex-shrink-0 px-6 py-3 rounded-full font-medium cursor-pointer transition-all duration-200 min-w-[120px] text-center',
              selectedDay === day.id ? 'bg-pink-500 text-white shadow-lg' : 'bg-gray-200 hover:bg-gray-300'
            ]"
          >
            {{ day.day_number }}
          </div>
        </div>

        <button 
          @click="scrollRight"
          class="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-white rounded-full p-2 shadow-md hover:shadow-lg transition-shadow"
        >
          <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <!-- 📝 Workouts for Selected Day -->
      <div v-if="selectedDayInfo" class="max-w-6xl mx-auto">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-3xl font-bold text-gray-900">{{ selectedDayInfo.title }}</h2>
          <div class="flex items-center gap-4">
            <span class="font-medium text-gray-600">{{ selectedDayInfo.video_links.length }} Workouts</span>
            <span class="text-gray-400">|</span>
            <span class="font-medium text-gray-600">{{ selectedDayInfo.duration }} Mins</span>
          </div>
        </div>

        <div v-if="selectedDayInfo.video_links.length === 0" class="text-gray-500">
          No workouts for this day.
        </div>

        <div v-else class="space-y-4">
          <div 
            v-for="(video, idx) in selectedDayInfo.video_links" 
            :key="idx"
          >
            <div 
              :class="[
                'mb-4 rounded-2xl overflow-hidden transition-all duration-200',
                workoutStates[`${selectedDay}-${idx}`]?.completed 
                  ? 'bg-indigo-50 border-2 border-indigo-200' 
                  : 'bg-white border border-gray-200 hover:shadow-md'
              ]"
            >
              <!-- ✅ Thumbnail & Controls -->
              <div class="p-6 flex items-start gap-6">
                <div 
                  class="relative flex-shrink-0 rounded-xl overflow-hidden w-72 h-40 group cursor-pointer bg-gray-900"
                  @click="openYouTube(video)"
                >
                  <!-- ✅ YouTube Thumbnail -->
                  <img 
                    v-if="extractYouTubeId(video)"
                    :src="`https://img.youtube.com/vi/${extractYouTubeId(video)}/mqdefault.jpg`" 
                    class="w-full h-full object-cover"
                    alt="Video thumbnail"
                    @error="handleImageError"
                  />
                  <!-- ❌ Fallback -->
                  <div v-else class="w-full h-full bg-gradient-to-br from-red-600 to-red-800 flex items-center justify-center">
                    <svg class="w-16 h-16 text-white" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                    </svg>
                  </div>

                  <!-- Overlay Play Button -->
                  <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-40 transition-all duration-200 flex items-center justify-center">
                    <div class="w-16 h-16 bg-white bg-opacity-90 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transform scale-75 group-hover:scale-100 transition-all duration-200 shadow-2xl">
                      <svg class="w-7 h-7 text-gray-900 ml-1" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
                      </svg>
                    </div>
                  </div>
                </div>

                <!-- Workout Info -->
                <div class="flex-1">
                  <h3 class="text-2xl font-bold text-gray-900 mb-3">Workout {{ idx + 1 }}</h3>
                  <div class="flex gap-3">
                    <button
                      @click="openYouTube(video)"
                      class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2"
                    >
                      ▶ Watch on YouTube
                    </button>
                    
                    <button
                      @click="toggleComplete(selectedDay, idx)"
                      :disabled="dayCompletionStates[selectedDay]"
                      :class="[
                        'px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center gap-2',
                        dayCompletionStates[selectedDay]
                          ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                          : workoutStates[`${selectedDay}-${idx}`]?.completed
                            ? 'bg-green-600 hover:bg-green-700 text-white'
                            : 'bg-indigo-600 hover:bg-indigo-700 text-white'
                      ]"
                    >
                      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path 
                          v-if="workoutStates[`${selectedDay}-${idx}`]?.completed" 
                          fill-rule="evenodd" 
                          d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" 
                          clip-rule="evenodd" 
                        />
                        <path 
                          v-else 
                          fill-rule="evenodd" 
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v3.586L7.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 10.586V7z" 
                          clip-rule="evenodd" 
                        />
                      </svg>
                      {{ workoutStates[`${selectedDay}-${idx}`]?.completed ? 'Completed' : 'Mark Complete' }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- ✅ Complete Day Section -->
          <div class="mt-8 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl p-8 text-center border-2 border-indigo-200">
            <div v-if="!dayCompletionStates[selectedDay]">
              <div class="mb-6">
                <div class="flex items-center justify-center gap-3 mb-3">
                  <span class="text-2xl">{{ getCompletedCount(selectedDay) }}</span>
                  <span class="text-gray-400">/</span>
                  <span class="text-2xl text-gray-600">{{ selectedDayInfo.video_links.length }}</span>
                  <span class="text-gray-600 font-medium">workouts completed</span>
                </div>
                <div class="max-w-md mx-auto bg-gray-200 rounded-full h-3 overflow-hidden">
                  <div 
                    class="bg-gradient-to-r from-pimk-100 to-pink-600 h-full rounded-full transition-all duration-500"
                    :style="{ width: `${getProgressPercentage(selectedDay)}%` }"
                  ></div>
                </div>
              </div>

              <button 
                @click="completeDay(selectedDay)"
                :disabled="!allWorkoutsComplete(selectedDay) || isCompletingDay"
                :class="[
                  'px-10 py-4 rounded-full font-bold text-lg transition-all duration-300 transform hover:scale-105',
                    allWorkoutsComplete(selectedDay) && !isCompletingDay
                    ? 'bg-[#F9B4FF] shadow-xl hover:bg-pink-400 hover:shadow-2xl cursor-pointer'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                ]"
              >
                <span v-if="isCompletingDay">Completing Day...</span>
                <span v-else-if="allWorkoutsComplete(selectedDay)">Complete Day</span>
                <span v-else>Complete All Workouts First</span>
              </button>
            </div>

            <div v-else class="py-4">
              <div class="text-6xl mb-4">🏆</div>
              <h3 class="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 mb-2">
                Day Completed!
              </h3>
              <p class="text-gray-600">You earned <span class="font-bold text-indigo-600">+{{ xp }} XP</span></p>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const programId = route.params.id

const program = ref({})
const days = ref([])
const selectedDay = ref(null)
const loading = ref(true)
const error = ref(null)
const daysContainer = ref(null)
const workoutStates = ref({})
const dayCompletionStates = ref({})
const isCompletingDay = ref(false)
const xp = ref(0)

const selectedDayInfo = computed(() => days.value.find(d => d.id === selectedDay.value))

onMounted(fetchProgramDetail)

async function fetchProgramDetail() {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/workout/programs/${programId}/`, {
      credentials: 'include',
    })
    if (!res.ok) throw new Error(`Failed to fetch program: ${res.status}`)
    const data = await res.json()

    program.value = data
    days.value = data.days || []
    if (days.value.length > 0) selectedDay.value = days.value[0].id
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

function selectDay(dayId) {
  selectedDay.value = dayId
}

function scrollLeft() {
  daysContainer.value?.scrollBy({ left: -200, behavior: 'smooth' })
}

function scrollRight() {
  daysContainer.value?.scrollBy({ left: 200, behavior: 'smooth' })
}

function extractYouTubeId(url) {
  if (!url) return null
  if (/^[a-zA-Z0-9_-]{11}$/.test(url)) return url
  const match = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\?\/]+)/)
  return match ? match[1] : null
}

function openYouTube(url) {
  const id = extractYouTubeId(url)
  if (id) window.open(`https://www.youtube.com/watch?v=${id}`, '_blank')
}

function handleImageError(event) {
  event.target.style.display = 'none'
}

function toggleComplete(dayId, workoutIndex) {
  if (dayCompletionStates.value[dayId]) return
  const key = `${dayId}-${workoutIndex}`
  if (!workoutStates.value[key]) workoutStates.value[key] = { completed: false }
  workoutStates.value[key].completed = !workoutStates.value[key].completed
}

function getCompletedCount(dayId) {
  const day = days.value.find(d => d.id === dayId)
  if (!day) return 0
  return day.video_links.reduce((count, _, idx) => 
    workoutStates.value[`${dayId}-${idx}`]?.completed ? count + 1 : count
  , 0)
}

function getProgressPercentage(dayId) {
  const day = days.value.find(d => d.id === dayId)
  if (!day || day.video_links.length === 0) return 0
  return (getCompletedCount(dayId) / day.video_links.length) * 100
}

function allWorkoutsComplete(dayId) {
  const day = days.value.find(d => d.id === dayId)
  if (!day) return false
  return getCompletedCount(dayId) === day.video_links.length
}

async function getCurrentXp() {
  const res = await fetch(`http://127.0.0.1:8000/api/user-info/`, {
    credentials: "include",
  })
  if (!res.ok) throw new Error("Failed to load user info")
  const data = await res.json()
  return data?.user?.profile?.current_level?.xp ?? 0
}

async function completeDay(dayId) {
  if (!allWorkoutsComplete(dayId)) {
    alert('Please complete all workouts first!')
    return
  }

  isCompletingDay.value = true
  try {
    const before = await getCurrentXp()

    const res = await fetch(`http://127.0.0.1:8000/api/workout/day/${dayId}/complete/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include'
    })

    if (!res.ok) throw new Error('Failed to complete day')
    dayCompletionStates.value[dayId] = true

    const after = await getCurrentXp()

    xp.value = Math.max(0, (after || 0) - (before || 0))
    console.log('XP before:', before, 'after:', after, 'earned:', xp.value)

    alert(`🎉 Congratulations! You earned ${xp.value} XP!`)
  } catch (err) {
    console.error(err)
    alert('Failed to complete day. Please try again.')
  } finally {
    isCompletingDay.value = false
  }
}

</script>

<style scoped>
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>