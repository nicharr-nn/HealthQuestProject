<template>
  <div class="min-h-screen p-6">
    <!-- Day Selector Component -->
    <div class="relative max-w-6xl mx-auto mb-8 rounded-full bg-[#E3CFD8]">
      <!-- Left Arrow -->
      <button 
        @click="scrollLeft"
        class="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-white rounded-full p-2 shadow-md hover:shadow-lg transition-shadow duration-200"
      >
        <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>

      <!-- Days Container -->
      <div 
        ref="daysContainer"
        class="flex gap-4 overflow-x-auto scrollbar-hide px-12 py-4 scroll-smooth"
        style="scrollbar-width: none; -ms-overflow-style: none;"
      >
        <div 
          v-for="day in days" 
          :key="day.id"
          @click="selectDay(day.id)"
          :class="[
            'flex-shrink-0 px-6 py-4 rounded-2xl font-medium text-center cursor-pointer transition-all duration-200 min-w-[120px]',
            day.id === selectedDay 
              ? 'bg-[#FD5E8F] text-white shadow-lg transform scale-105' 
              : day.type === 'rest' 
                ? 'bg-[#EEEAF3] hover:bg-purple-200' 
                : 'bg-white text-gray-700 hover:bg-gray-100 shadow-sm hover:shadow-md'
          ]"
        >
          {{ day.label }}
        </div>
      </div>

      <!-- Right Arrow -->
      <button 
        @click="scrollRight"
        class="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-white rounded-full p-2 shadow-md hover:shadow-lg transition-shadow duration-200"
      >
        <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>

    <!-- Workout Details Section -->
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-3xl font-bold text-gray-900">
          {{ selectedDayInfo.label }}'s Workout
        </h2>
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-3 text-gray-600">
            <span class="font-medium">{{ selectedDayInfo.workouts?.length || 0 }} Workouts</span>
            <span class="text-gray-400">|</span>
            <span class="font-medium">{{ calculateTotalTime(selectedDayInfo.workouts) }} Mins</span>
          </div>
        </div>
      </div>

      <!-- Rest Day Message -->
      <div v-if="selectedDayInfo.type === 'rest'" class="bg-purple-50 border-2 border-purple-200 rounded-2xl p-8 text-center">
        <h3 class="text-2xl font-bold text-purple-900 mb-2">Rest Day</h3>
        <p class="text-purple-700">Take a well-deserved rest today. Light stretching or a gentle walk is perfect!</p>
      </div>

      <!-- Workout List -->
      <div v-else class="space-y-4">
        <!-- Progress Line on the left -->
        <div class="relative">
          <!-- Vertical Progress Line -->
          <div class="absolute left-7 top-0 bottom-0 w-0.5 bg-gray-200" style="margin-top: 40px; margin-bottom: 40px;"></div>

          <!-- Workout Items -->
          <div 
            v-for="(workout, index) in selectedDayInfo.workouts" 
            :key="index"
            class="relative"
          >
            <!-- Checkpoint Circle - Clickable Checkbox -->
            <button
              @click.stop="toggleComplete(selectedDay, index)"
              type="button"
              :class="[
                'absolute left-4 w-6 h-6 rounded-full border-4 bg-white z-10 transition-all duration-200 cursor-pointer hover:scale-110 focus:outline-none',
                workout.completed 
                  ? 'border-indigo-600 bg-indigo-600 shadow-lg' 
                  : 'border-gray-300 hover:border-indigo-400'
              ]"
              style="top: 50%; transform: translateY(-50%);"
              :aria-label="workout.completed ? 'Mark as incomplete' : 'Mark as complete'"
            >
              <svg 
                v-if="workout.completed" 
                class="w-4 h-4 text-white absolute pointer-events-none" 
                style="top: 50%; left: 50%; transform: translate(-50%, -50%);"
                fill="currentColor" 
                viewBox="0 0 20 20"
              >
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
            </button>

            <!-- Workout Card -->
            <div 
              :class="[
                'ml-16 mb-4 rounded-2xl overflow-hidden transition-all duration-200',
                workout.completed ? 'bg-indigo-50 border-2 border-indigo-200' : 'bg-white border border-gray-200 hover:shadow-md'
              ]"
            >
              <!-- Completed Badge -->
              <div v-if="workout.completed" class="px-6 py-2 bg-indigo-600 flex items-center justify-between">
                <span class="text-white font-semibold">WORKOUT COMPLETE</span>
                <button class="text-white">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
              </div>

              <!-- Workout Content -->
              <div class="p-6 flex items-start gap-6">
                <!-- Video Thumbnail -->
                <div 
                  class="relative flex-shrink-0 rounded-xl overflow-hidden w-72 h-40 group cursor-pointer bg-gray-900"
                  @click="openYouTube(workout.youtubeId)"
                >
                  <!-- YouTube Thumbnail Image -->
                  <img 
                    v-if="workout.youtubeId"
                    :src="`https://img.youtube.com/vi/${workout.youtubeId}/mqdefault.jpg`"
                    :alt="workout.title"
                    class="w-full h-full object-cover"
                    @error="handleImageError"
                  />
                  
                  <!-- Fallback for custom thumbnails or no YouTube ID -->
                  <div 
                    v-else
                    class="w-full h-full bg-gradient-to-br from-gray-700 to-gray-900 flex items-center justify-center"
                    :style="{ 
                      backgroundImage: workout.thumbnail ? `url(${workout.thumbnail})` : 'none', 
                      backgroundSize: 'cover', 
                      backgroundPosition: 'center' 
                    }"
                  >
                    <div v-if="!workout.thumbnail" class="text-xl font-bold text-white text-center px-4">
                      {{ workout.title }}
                    </div>
                  </div>

                  <!-- Dark Overlay on Hover -->
                  <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-40 transition-all duration-200 flex items-center justify-center">
                    <!-- Play Button -->
                    <div class="w-16 h-16 bg-white bg-opacity-90 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transform scale-75 group-hover:scale-100 transition-all duration-200 shadow-2xl">
                      <svg class="w-7 h-7 text-gray-900 ml-1" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
                      </svg>
                    </div>
                  </div>
                  
                  <!-- Duration Badge -->
                  <div class="absolute bottom-3 right-3 bg-black bg-opacity-90 text-white px-2.5 py-1 rounded-md text-sm font-bold backdrop-blur-sm">
                    {{ workout.duration }}
                  </div>

                  <!-- YouTube Logo Badge -->
                  <div v-if="workout.youtubeId" class="absolute top-3 left-3 bg-red-600 text-white px-2.5 py-1 rounded-md text-xs font-bold flex items-center gap-1">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                    </svg>
                    YouTube
                  </div>
                </div>

                <!-- Workout Info -->
                <div class="flex-1">
                  <h3 class="text-2xl font-bold text-gray-900 mb-3">{{ workout.title }}</h3>
                  
                  <!-- Category Badge -->
                  <div class="flex items-center gap-2 mb-4">
                    <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    <span class="text-gray-700 font-medium">{{ workout.category }}</span>
                  </div>

                  <!-- Stats -->
                  <div class="flex items-center gap-4 text-gray-500 text-sm">
                    <span>{{ workout.views }} views</span>
                    <span>•</span>
                    <span>{{ workout.date }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Complete Day Button at the End -->
        <div class="mt-8 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl p-8 text-center border-2 border-indigo-200">
          <div v-if="!selectedDayInfo.dayCompleted">
            <!-- Progress Check -->
            <div class="mb-6">
              <div class="flex items-center justify-center gap-3 mb-3">
                <span class="text-2xl">{{ getCompletedCount(selectedDayInfo.workouts) }}</span>
                <span class="text-gray-400">/</span>
                <span class="text-2xl text-gray-600">{{ selectedDayInfo.workouts?.length || 0 }}</span>
                <span class="text-gray-600 font-medium">workouts completed</span>
              </div>
              
              <!-- Progress Bar -->
              <div class="max-w-md mx-auto bg-gray-200 rounded-full h-3 overflow-hidden">
                <div 
                  class="bg-gradient-to-r from-indigo-500 to-purple-600 h-full rounded-full transition-all duration-500"
                  :style="{ width: `${getProgressPercentage(selectedDayInfo.workouts)}%` }"
                ></div>
              </div>
            </div>

            <!-- Complete Day Button -->
            <button 
              @click="completeDayWithAPI(selectedDay)"
              :disabled="!allWorkoutsComplete(selectedDayInfo.workouts) || isCompletingDay"
              :class="[
                'px-10 py-4 rounded-full font-bold text-lg transition-all duration-300 transform hover:scale-105',
                allWorkoutsComplete(selectedDayInfo.workouts) && !isCompletingDay
                  ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-xl hover:shadow-2xl cursor-pointer'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              ]"
            >
              <span v-if="isCompletingDay" class="flex items-center gap-2 justify-center">
                <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Completing Day...
              </span>
              <span v-else-if="allWorkoutsComplete(selectedDayInfo.workouts)">
                🎉 Complete Day & Earn XP
              </span>
              <span v-else>
                Complete All Workouts First
              </span>
            </button>

            <p class="text-sm text-gray-600 mt-4">
              {{ allWorkoutsComplete(selectedDayInfo.workouts) 
                ? 'Great job! Click to earn your rewards!' 
                : 'Finish all workouts to unlock this button' 
              }}
            </p>
          </div>

          <!-- Day Already Completed State -->
          <div v-else class="py-4">
            <div class="text-6xl mb-4">🏆</div>
            <h3 class="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 mb-2">
              Day Completed!
            </h3>
            <p class="text-gray-600 mb-4">You earned <span class="font-bold text-indigo-600">+{{ selectedDayInfo.xpEarned || 50 }} XP</span></p>
            <div class="flex items-center justify-center gap-2 text-sm text-gray-500">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
              </svg>
              Completed on {{ selectedDayInfo.completedDate || 'Today' }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'WorkoutSchedule',
  setup() {
    const daysContainer = ref(null)
    const selectedDay = ref(1)
    const isCompletingDay = ref(false)

    // Generate workout data
    const days = ref([
      { 
        id: 1, 
        label: 'Day 1', 
        type: 'workout',
        dayCompleted: false,
        xpEarned: null,
        completedDate: null,
        workouts: [
          { 
            title: 'Lower Body Warmup', 
            category: 'Warmup', 
            duration: '8:45',
            views: '89K',
            date: 'Aug 25',
            completed: true,
            optional: false,
            favorite: false,
            youtubeId: 'B4Xlf8vOvn8' // Replace with actual video ID
          },
          { 
            title: 'Glutes Hourglass', 
            category: 'Booty', 
            duration: '21:15',
            views: '153K',
            date: 'Aug 25',
            completed: false,
            optional: false,
            favorite: true,
            youtubeId: 'dQw4w9WgXcQ' // Replace with actual video ID
          },
          { 
            title: 'Defined Abs', 
            category: 'Abs', 
            duration: '10:36',
            views: '665K',
            date: 'May 25',
            completed: false,
            optional: false,
            favorite: false,
            youtubeId: 'dQw4w9WgXcQ' // Replace with actual video ID
          },
          { 
            title: 'Stretch & Mobility Routine', 
            category: 'Cooldown', 
            duration: '15:50',
            views: '522K',
            date: 'Jul 25',
            completed: false,
            optional: true,
            favorite: false,
            youtubeId: 'dQw4w9WgXcQ' // Replace with actual video ID
          }
        ]
      },
      { 
        id: 2, 
        label: 'Day 2', 
        type: 'workout',
        dayCompleted: false,
        xpEarned: null,
        completedDate: null,
        workouts: [
          { 
            title: 'Upper Body Warmup', 
            category: 'Warmup', 
            duration: '7:30',
            views: '72K',
            date: 'Aug 25',
            completed: false,
            optional: false,
            favorite: false
          },
          { 
            title: 'Toned Arms & Shoulders', 
            category: 'Upper Body', 
            duration: '18:20',
            views: '245K',
            date: 'Aug 25',
            completed: false,
            optional: false,
            favorite: false
          },
          { 
            title: 'Core Burner', 
            category: 'Abs', 
            duration: '12:15',
            views: '432K',
            date: 'Jul 25',
            completed: false,
            optional: false,
            favorite: false
          }
        ]
      },
      { 
        id: 3, 
        label: 'Day 3', 
        type: 'workout',
        dayCompleted: false,
        xpEarned: null,
        completedDate: null,
        workouts: [
          { 
            title: 'Full Body Warmup', 
            category: 'Warmup', 
            duration: '9:00',
            views: '95K',
            date: 'Aug 25',
            completed: false,
            optional: false,
            favorite: false
          },
          { 
            title: 'Booty & Thigh Burn', 
            category: 'Lower Body', 
            duration: '25:40',
            views: '312K',
            date: 'Aug 25',
            completed: false,
            optional: false,
            favorite: false
          }
        ]
      },
      { id: 4, label: 'Day 4', type: 'workout', dayCompleted: false, xpEarned: null, completedDate: null, workouts: [] },
      { id: 5, label: 'Rest Day', type: 'rest' },
      { id: 6, label: 'Day 6', type: 'workout', dayCompleted: false, xpEarned: null, completedDate: null, workouts: [] },
      { id: 7, label: 'Rest Day', type: 'rest' },
    ])

    const selectedDayInfo = computed(() => {
      return days.value.find(day => day.id === selectedDay.value)
    })

    const selectDay = (dayId) => {
      selectedDay.value = dayId
    }

    const scrollLeft = () => {
      if (daysContainer.value) {
        daysContainer.value.scrollBy({ left: -200, behavior: 'smooth' })
      }
    }

    const scrollRight = () => {
      if (daysContainer.value) {
        daysContainer.value.scrollBy({ left: 200, behavior: 'smooth' })
      }
    }

    const calculateTotalTime = (workouts) => {
      if (!workouts) return 0
      return workouts.reduce((total, workout) => {
        const [mins, secs] = workout.duration.split(':').map(Number)
        return total + mins + (secs / 60)
      }, 0).toFixed(0)
    }

    const toggleFavorite = (dayId, workoutIndex) => {
      const day = days.value.find(d => d.id === dayId)
      if (day && day.workouts) {
        day.workouts[workoutIndex].favorite = !day.workouts[workoutIndex].favorite
      }
    }

    const toggleComplete = (dayId, workoutIndex) => {
      const day = days.value.find(d => d.id === dayId)
      if (day && day.workouts) {
        day.workouts[workoutIndex].completed = !day.workouts[workoutIndex].completed
      }
    }

    const allWorkoutsComplete = (workouts) => {
      if (!workouts || workouts.length === 0) return false
      return workouts.every(workout => workout.completed)
    }

    const toggleAllWorkouts = (dayId) => {
      const day = days.value.find(d => d.id === dayId)
      if (day && day.workouts) {
        const allComplete = allWorkoutsComplete(day.workouts)
        // If all are complete, mark all as incomplete. Otherwise, mark all as complete
        day.workouts.forEach(workout => {
          workout.completed = !allComplete
        })
      }
    }

    const openYouTube = (youtubeId) => {
      if (youtubeId) {
        window.open(`https://www.youtube.com/watch?v=${youtubeId}`, '_blank')
      }
    }

    const getCompletedCount = (workouts) => {
      if (!workouts) return 0
      return workouts.filter(w => w.completed).length
    }

    const getProgressPercentage = (workouts) => {
      if (!workouts || workouts.length === 0) return 0
      return (getCompletedCount(workouts) / workouts.length) * 100
    }

    const completeDayWithAPI = async (dayId) => {
      const day = days.value.find(d => d.id === dayId)
      
      // Check if all workouts are complete
      if (!day || !allWorkoutsComplete(day.workouts)) {
        alert('Please complete all workouts first!')
        return
      }

      isCompletingDay.value = true

      try {
        // EXAMPLE API CALL - Replace with your actual API endpoint
        const response = await fetch('/api/complete-day', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            // Add your auth token here
            // 'Authorization': `Bearer ${yourAuthToken}`
          },
          body: JSON.stringify({
            dayId: dayId,
            programId: '2025-hourglass-challenge',
            completedAt: new Date().toISOString(),
            workoutsCompleted: day.workouts.length
          })
        })

        if (response.ok) {
          const data = await response.json()
          
          // Update the day with completion data from API
          day.dayCompleted = true
          day.xpEarned = data.xpEarned || 50 // XP from API response
          day.completedDate = new Date().toLocaleDateString()

          // Optional: Show success message
          alert(`🎉 Congratulations! You earned ${day.xpEarned} XP!`)
        } else {
          throw new Error('Failed to complete day')
        }
      } catch (error) {
        console.error('Error completing day:', error)
        alert('Failed to complete day. Please try again.')
      } finally {
        isCompletingDay.value = false
      }
    }

    return {
      daysContainer,
      selectedDay,
      days,
      selectedDayInfo,
      isCompletingDay,
      selectDay,
      scrollLeft,
      scrollRight,
      calculateTotalTime,
      toggleFavorite,
      toggleComplete,
      allWorkoutsComplete,
      toggleAllWorkouts,
      openYouTube,
      getCompletedCount,
      getProgressPercentage,
      completeDayWithAPI
    }
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