<template>
  <div class="min-h-screen bg-slate-50 text-slate-900">
    <!-- Mobile overlay -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 z-40 bg-black/40 md:hidden"
      @click="sidebarOpen = false"
    />

    <!-- Sidebar -->
    <AdminSideBar
      :sidebarOpen="sidebarOpen"
      :activeSection="activeSection"
      :nav="nav"
      @close="sidebarOpen = false"
      @select="setSection"
    />

    <!-- Main column -->
    <div :class="sidebarOpen ? 'md:pl-72' : 'md:pl-0'">
      <!-- Header -->
      <header class="sticky top-0 left-0 right-0 z-30 bg-white/90 backdrop-blur supports-[backdrop-filter]:bg-white/60 shadow-sm">
        <div class="flex items-center justify-between px-4 py-3 md:px-8">
          <div class="flex items-center gap-3">
            <button
              class="inline-flex items-center justify-center rounded-md p-2 text-slate-700 hover:bg-slate-100"
              @click="sidebarOpen = !sidebarOpen"
              aria-label="Toggle menu"
            >
              <Menu class="w-5 h-5" />
            </button>
            <div class="relative hidden md:block">
              <input
                type="text"
                placeholder="Search workouts..."
                v-model="searchQuery"
                class="w-80 rounded-md border border-slate-200 pl-5 pr-3 py-2 text-sm font-subtitle placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/40"
              />
            </div>
          </div>

          <div class="flex items-center gap-3">
            <AdminNotificationBell @review="viewCoachDetails" />

            <!-- Header User Info -->
            <div class="flex items-center gap-2">
              <div class="grid h-10 w-10 place-items-center rounded-full bg-blue-500 font-bold font-subtitle text-white">
                <template v-if="userStore.user?.username">
                  {{ getInitials(userStore.user.username) }}
                </template>
                <template v-else>?</template>
              </div>

              <div class="leading-tight">
                <div class="font-medium font-subtitle">
                  <template v-if="userStore.user?.username">
                    {{ userStore.user.username }}
                  </template>
                  <template v-else>Loading...</template>
                </div>
                <div class="text-[11px] text-slate-500 font-subtitle">Administrator</div>
              </div>
            </div>            

            <button 
              @click="logout"
              class="ml-3 flex items-center py-2 px-3 rounded-md hover:bg-gray-100"
            >
              <span class="material-symbols-outlined">logout</span>
            </button>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <div class="p-5 space-y-4">
        <div>
          <h2 class="text-2xl font-subtitle">Workout Management</h2>
          <p class="text-sm text-slate-500 font-subtitle">View all workout programs and their associated coaches</p>
        </div>

        <!-- Workouts Table -->
        <div class="rounded-xl bg-white p-5 shadow-sm">
          <div class="mb-4 flex items-center justify-between">
            <h3 class="text-base font-semibold font-subtitle">All Workout Programs ({{ workouts.length }})</h3>
            <div class="flex items-center gap-3">
              <select class="rounded-md border border-slate-200 px-3 py-2 text-sm font-subtitle" v-model="workoutCategoryFilter">
                <option value="all">All Categories</option>
                <option value="strength_training">Strength Training</option>
                <option value="cardio">Cardio</option>
                <option value="weight_loss">Weight Loss</option>
                <option value="muscle_building">Muscle Building</option>
                <option value="endurance">Endurance</option>
                <option value="flexibility">Flexibility</option>
                <option value="full_body">Full Body</option>
              </select>
              <select class="rounded-md border border-slate-200 px-3 py-2 text-sm font-subtitle" v-model="workoutDifficultyFilter">
                <option value="all">All Difficulties</option>
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>
          </div>

          <div v-if="loadingWorkouts" class="text-center py-8 text-slate-500">Loading workouts...</div>

          <div v-else class="overflow-x-auto">
            <table class="w-full border-collapse text-sm">
              <thead class="text-slate-500 font-subtitle">
                <tr class="border-b border-slate-200">
                  <th class="px-3 py-2 text-left font-semibold">Program Title</th>
                  <th class="px-3 py-2 text-left font-semibold">Coach</th>
                  <th class="px-3 py-2 text-left font-semibold">Category</th>
                  <th class="px-3 py-2 text-left font-semibold">Difficulty</th>
                  <th class="px-3 py-2 text-left font-semibold">Duration</th>
                  <th class="px-3 py-2 text-left font-semibold">Created</th>
                  <th class="px-3 py-2 text-left font-semibold">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="filteredWorkouts.length === 0">
                  <td colspan="8" class="px-3 py-8 text-center text-slate-500 font-semibold">
                    No workout programs found
                  </td>
                </tr>
                <tr v-for="workout in filteredWorkouts" :key="workout.id" class="border-b border-slate-100 hover:bg-slate-50">
                  <td class="px-3 py-3">
                    <div class="flex items-center gap-2">
                      <div class="font-semibold">{{ workout.title }}</div>
                    </div>
                  </td>
                  <td class="px-3 py-3">
                    <div class="flex items-center gap-2">
                      <div class="grid h-6 w-6 place-items-center rounded-full bg-emerald-500 text-xs font-bold text-white">
                        {{ getInitials(workout.coach_name) }}
                      </div>
                      <span class="font-semibold">{{ workout.coach_name }}</span>
                    </div>
                  </td>
                  <td class="px-3 py-3">
                    <span class="rounded-full px-2 py-0.5 text-[11px] font-semibold capitalize bg-purple-100 text-purple-800">
                      {{ formatCategory(workout.category) }}
                    </span>
                  </td>
                  <td class="px-3 py-3">
                    <span
                      class="rounded-full px-2 py-0.5 text-[11px] font-semibold capitalize"
                      :class="getDifficultyClass(workout.difficulty_level)"
                    >
                      {{ workout.difficulty_level }}
                    </span>
                  </td>
                  <td class="px-3 py-3 font-semibold">{{ workout.duration }} days</td>
                  <td class="px-3 py-3 font-semibold">{{ formatDate(workout.created_at) }}</td>
                  <td class="px-3 py-3 flex gap-2">
                    <button
                      class="rounded-md bg-blue-600 px-3 py-1.5 text-white hover:bg-blue-700 text-xs font-bold"
                      @click="viewWorkoutDetails(workout)"
                    >
                      View
                    </button>
                    <button
                      class="rounded-md bg-red-600 px-3 py-1.5 text-white hover:bg-red-700 text-xs font-bold"
                      @click="deleteWorkout(workout.id)"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Workout Details Modal -->
        <div
          v-if="workoutModal.open"
          class="fixed inset-0 z-[60] grid place-items-center bg-black/50 p-4"
          role="dialog"
          aria-modal="true"
          @click.self="closeWorkoutModal"
        >
          <div class="w-full max-w-3xl overflow-hidden rounded-xl bg-white shadow-lg">
            <div class="flex items-center justify-between border-b border-slate-200 px-5 py-4">
              <h3 class="text-lg font-subtitle">Workout Program Details</h3>
              <button class="text-slate-500 hover:text-slate-700" @click="closeWorkoutModal">✕</button>
            </div>

            <div class="px-5 py-4 space-y-4 max-h-[70vh] overflow-y-auto">
              <div>
                <h4 class="text-xl font-subtitle">{{ workoutModal.workout?.title }}</h4>
                <p class="text-sm text-slate-600 mt-2 font-medium ">{{ workoutModal.workout?.description }}</p>
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div>
                  <div class="text-sm font-subtitle text-slate-700">Coach</div>
                  <div class="flex items-center gap-2 mt-1">
                    <div class="grid h-8 w-8 place-items-center rounded-full bg-emerald-500 text-xs font-bold text-white">
                      {{ getInitials(workoutModal.workout?.coach_name) }}
                    </div>
                    <span class="text-base font-medium">{{ workoutModal.workout?.coach_name }}</span>
                  </div>
                </div>
                <div>
                  <div class="text-sm font-subtitle text-slate-700">Category</div>
                  <div class="text-base capitalize mt-1 font-medium ">{{ formatCategory(workoutModal.workout?.category) }}</div>
                </div>
                <div>
                  <div class="text-sm font-subtitle text-slate-700">Difficulty Level</div>
                  <div class="mt-1">
                    <span
                      class="rounded-full px-2 py-1 text-xs font-medium capitalize"
                      :class="getDifficultyClass(workoutModal.workout?.difficulty_level)"
                    >
                      {{ workoutModal.workout?.difficulty_level }}
                    </span>
                  </div>
                </div>
                <div>
                  <div class="text-sm font-subtitle text-slate-700">Duration</div>
                  <div class="text-base mt-1 font-medium ">{{ workoutModal.workout?.duration }} days</div>
                </div>
                <div>
                  <div class="text-sm font-subtitle text-slate-700">Level Access</div>
                  <div class="text-base capitalize mt-1 font-medium ">{{ workoutModal.workout?.level_access }}</div>
                </div>
                <div>
                  <div class="text-sm font-subtitle text-slate-700">Created</div>
                  <div class="text-base mt-1 font-medium ">{{ formatDate(workoutModal.workout?.created_at) }}</div>
                </div>
              </div>

              <div class="text-sm font-subtitle text-slate-700">Workout Schedule</div>
              <div
                v-for="day in workoutModal.workout.days"
                :key="day.id"
                class="flex items-center justify-between rounded-md bg-slate-50 p-3"
              >
                <div class="flex items-center gap-3">
                  <div class="grid h-8 w-8 place-items-center rounded-full bg-blue-500 text-xs font-bold text-white">
                    {{ day.day_number }}
                  </div>
                  <div>
                    <div class="text-sm font-medium">{{ day.title || `Day ${day.day_number}` }}</div>
                    <div class="text-xs text-slate-500">{{ day.duration }} minutes • {{ day.video_links?.length || 0 }} videos</div>
                  </div>
                </div>

                <!-- Video button -->
                <button
                  v-if="day.video_links?.length"
                  class="rounded-md bg-blue-600 px-3 py-1.5 text-white hover:bg-blue-700 text-xs font-bold"
                  @click="openVideo(day.video_links[0])"
                >
                  Video
                </button>
              </div>
            </div>

            <div class="flex justify-end gap-3 border-t border-slate-200 px-5 py-4 bg-slate-50">
              <button
                class="rounded-md border border-slate-300 bg-white px-4 py-2 text-slate-700 hover:bg-slate-50"
                @click="closeWorkoutModal"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import AdminSideBar from '@/components/AdminSideBar.vue'
import { Menu } from 'lucide-vue-next'
import AdminNotificationBell from '@/components/AdminNotificationBell.vue'
import { useToastStore } from '@/stores/toast'

const toast = useToastStore()

const userStore = useUserStore()
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

// Sidebar
const sidebarOpen = ref(true)
const activeSection = ref('workouts')

// Search & notifications
const searchQuery = ref('')

// Workouts
const workouts = ref([])
const workoutCategoryFilter = ref('all')
const workoutDifficultyFilter = ref('all')
const loadingWorkouts = ref(false)
const error = ref(null)

// Workout modal
const workoutModal = ref({ open: false, workout: null })

// Sidebar nav
const nav = ref([{ name: 'Workouts', key: 'workouts' }])
function setSection(sectionKey) {
  activeSection.value = sectionKey
}

// Computed: filtered workouts
const filteredWorkouts = computed(() => {
  let result = workouts.value

  // Category filter
  if (workoutCategoryFilter.value !== 'all') {
    result = result.filter(w => w.category === workoutCategoryFilter.value)
  }

  // Difficulty filter
  if (workoutDifficultyFilter.value !== 'all') {
    result = result.filter(w => w.difficulty_level === workoutDifficultyFilter.value)
  }

  // Search filter
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(
      w =>
        w.title.toLowerCase().includes(q) ||
        (w.coach_name && w.coach_name.toLowerCase().includes(q))
    )
  }

  return result
})

// Fetch workouts from backend
async function fetchWorkouts() {
  loadingWorkouts.value = true
  error.value = null
  try {
    const res = await fetch(`${API_URL}/api/workout/programs/`, {
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' }
    })
    if (!res.ok) throw new Error('Failed to fetch workouts')
    const data = await res.json()

    if (import.meta.env.DEV) {
      try {
        console.debug('Admin Workouts payload sample', Array.isArray(data) ? data.slice(0, 2) : data)
      } catch (e) {
        console.error(e)
      }
    }

    const base = data.map(w => {
      const nameCandidate = w.coach?.name || w.coach?.username || w.coach_name || w.coach_username || null
      const idCandidate = (typeof w.coach === 'number' || typeof w.coach === 'string') ? w.coach : (w.coach?.id || w.coach_id || w.coach?.public_id)
      const display = nameCandidate || (idCandidate ? `Coach ${idCandidate}` : 'Unknown Coach')
      return {
        ...w,
        coach_name: nameCandidate || null,
        coach_display: display,
      }
    })

    const numericCoachIds = Array.from(new Set(base
      .map(w => w.coach)
      .filter(id => typeof id === 'number')
    ))

    if (numericCoachIds.length > 0) {
      try {
        const coachRes = await fetch(`${API_URL}/api/moderation/coaches/`, { credentials: 'include' })
        if (coachRes.ok) {
          const list = await coachRes.json()
          const idToName = {}
          for (const c of Array.isArray(list) ? list : []) {
            const candidates = [
              c.profile_id,
              c.user_profile_id,
              c?.user_profile?.id,
              c?.user?.profile?.id,
              typeof c.id === 'number' ? c.id : null,
            ].filter(v => typeof v === 'number')
            for (const cid of candidates) {
              if (numericCoachIds.includes(cid)) {
                idToName[cid] = c.name || c.username || (c.email ? String(c.email).split('@')[0] : null)
              }
            }
          }
          base.forEach(w => {
            if (typeof w.coach === 'number' && idToName[w.coach]) {
              w.coach_display = idToName[w.coach]
            }
          })
        }
      } catch (e) {
        console.error(e)
      }
    }

    workouts.value = base

  } catch (err) {
    console.error('Error fetching workouts:', err)
    error.value = 'Failed to load workouts'
  } finally {
    loadingWorkouts.value = false
  }
}

function getCsrfToken() {
  const match = document.cookie.match(new RegExp('(^| )csrftoken=([^;]+)'))
  return match ? match[2] : ''
}

async function deleteWorkout(id) {
  if (!confirm("Are you sure you want to delete this workout program?")) return;

  try {
    const res = await fetch(`${API_URL}/api/workout/programs/${id}/delete/`, {
      method: "DELETE",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrfToken(),
      },
    });

    if (!res.ok) {
      const text = await res.text()
      let body = text
      try { 
        body = JSON.parse(text) 
      } catch (e) {
        console.error(e)
      }

      if (res.status === 403) {
        toast.error((body && (body.detail || body.error)) || "You don't have permission to delete this program")
      } else {
        toast.error((body && (body.error || body.detail)) || "Failed to delete workout")
      }
      return;
    }

    // Remove from local list
    workouts.value = workouts.value.filter(w => w.id !== id);
    toast.success("Workout program deleted successfully");
  } catch (err) {
    console.error("Delete workout error:", err);
    toast.error("Failed to delete workout");
  }
}

// Modal controls
function viewWorkoutDetails(workout) {
  workoutModal.value = { open: true, workout }
}

function closeWorkoutModal() {
  workoutModal.value = { open: false, workout: null }
}

// Helpers
function formatCategory(category) {
  if (!category) return 'N/A'
  return category.replace(/_/g, ' ')
}

function getDifficultyClass(difficulty) {
  switch (difficulty) {
    case 'easy':
      return 'bg-emerald-100 text-emerald-800'
    case 'medium':
      return 'bg-amber-100 text-amber-800'
    case 'hard':
      return 'bg-rose-100 text-rose-800'
    default:
      return 'bg-slate-100 text-slate-800'
  }
}

function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(n => n[0].toUpperCase()).join('')
}

function openVideo(link) {
  if (!link) return
  window.open(link, '_blank')
}

// format dates
function formatDate(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

// Load workouts on mount
onMounted(() => {
  fetchWorkouts()
})
</script>
