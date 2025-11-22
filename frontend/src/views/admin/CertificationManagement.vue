<template>
  <div class="min-h-screen bg-slate-50 text-slate-900">
    <!-- Mobile overlay -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 z-40 bg-black/40 md:hidden"
      @click="sidebarOpen = false"
    />

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
      <header class="sticky top-0 left-0 right-0 z-30 z-30 bg-white/90 backdrop-blur supports-[backdrop-filter]:bg-white/60 shadow-sm">
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
                placeholder="Search coaches..."
                v-model="searchQuery"
                class="w-80 rounded-md border border-slate-200 pl-5 pr-3 py-2 text-sm font-subtitle placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/40"
              />
            </div>
          </div>

          <div class="flex items-center gap-3">
            <AdminNotificationBell @review="viewCoachDetails" />
            <!-- Header User Info -->
            <div class="flex items-center gap-2">
              <!-- Avatar -->
              <div class="grid h-10 w-10 place-items-center rounded-full bg-blue-500 font-bold font-subtitle text-white">
                <template v-if="userStore.user?.username">
                  {{ getInitials(userStore.user.username) }}
                </template>
                <template v-else>?</template>
              </div>

              <!-- Username and Role -->
              <div class="leading-tight">
                <div class="font-medium font-subtitle">
                  <template v-if="userStore.user?.username">
                    {{ userStore.user.username }}
                  </template>
                  <template v-else>
                    Loading...
                  </template>
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
      <main class="px-4 py-6 md:px-8">
        <!-- COACHES CERTIFICATION SECTION -->
        <section v-show="activeSection === 'coaches'" class="space-y-6">
          <div>
            <h2 class="text-2xl font-bold font-subtitle">Coach Certification Verification</h2>
            <p class="text-sm text-slate-500 font-subtitle">Review and verify coach certifications</p>
          </div>

          <div class="rounded-xl bg-white p-5 shadow-sm">
            <div class="mb-4 flex items-center justify-between">
              <h3 class="text-base font-semibold font-subtitle">Coach Applications</h3>
              <div class="flex items-center gap-3 font-subtitle">
                <select class="rounded-md border border-slate-200 px-3 py-2 text-sm" v-model="coachFilter" @change="fetchCoaches">
                  <option value="all">All Status</option>
                  <option value="pending">Pending</option>
                  <option value="approved">Approved</option>
                  <option value="rejected">Rejected</option>
                </select>
              </div>
            </div>

            <div v-if="loading" class="text-center py-8 text-slate-500">
              Loading coaches...
            </div>

            <div v-else-if="error" class="text-center py-8 text-rose-600">
              {{ error }}
            </div>

            <div v-else class="overflow-x-auto">
              <table class="w-full border-collapse text-sm">
                <thead class="text-slate-500">
                  <tr class="border-b border-slate-200">
                    <th class="px-3 py-2 text-left font-subtitle">Coach Name</th>
                    <th class="px-3 py-2 text-left font-subtitle">Email</th>
                    <th class="px-3 py-2 text-left font-subtitle">Applied Date</th>
                    <th class="px-3 py-2 text-left font-subtitle">Status</th>
                    <th class="px-3 py-2 text-left font-subtitle">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="filteredCoaches.length === 0">
                    <td colspan="6" class="px-3 py-8 text-center text-slate-500 font-semibold">
                      No {{ coachFilter !== 'all' ? coachFilter : '' }} coaches found
                    </td>
                  </tr>
                  <tr
                    v-for="coach in filteredCoaches"
                    :key="coach.coach_id"
                    class="border-b border-slate-100 hover:bg-slate-50"
                  >
                    <td class="px-3 py-3 font-semibold text-slate-800">
                      <div class="flex items-center gap-2">
                        <div class="grid h-8 w-8 place-items-center rounded-full bg-blue-500 text-xs font-semibold text-white">
                          {{ getInitials(coach.name) }}
                        </div>
                        {{ coach.name }}
                      </div>
                    </td>
                    <td class="px-3 py-3 font-semibold text-slate-800">{{ coach.email || 'N/A' }}</td>
                    <td class="px-3 py-3 font-semibold text-slate-800">{{ formatDate(coach.created_at) }}</td>
                    <td class="px-3 py-3 font-semibold">
                      <span
                        class="rounded-full px-2 py-0.5 text-[11px] font-semibold capitalize"
                        :class="getStatusClass(coach.status_approval)"
                      >
                        {{ coach.status_approval }}
                      </span>
                    </td>
                    <td class="px-3 py-3">
                      <button
                        class="rounded-md bg-blue-500 px-3 py-1.5 text-white font-semibold hover:bg-blue-600"
                        @click="viewCoachDetails(coach)"
                      >
                        Review
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>
      </main>
    </div>

    <!-- Coach Review Modal -->
    <div
      v-if="coachModal.open"
      class="fixed inset-0 z-[60] grid place-items-center bg-black/50 p-4"
      role="dialog"
      aria-modal="true"
      @click.self="closeModal"
    >
      <div class="w-full max-w-2xl overflow-hidden rounded-xl bg-white shadow-lg">
        <div class="flex items-center justify-between border-b border-slate-200 px-5 py-4">
          <h3 class="text-lg font-semibold font-subtitle">Coach Certification Review</h3>
          <button class="text-slate-500 hover:text-slate-700" @click="closeModal">✕</button>
        </div>

        <div class="px-5 py-4 space-y-4 max-h-[70vh] overflow-y-auto">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <div class="text-sm font-medium font-subtitle text-slate-700">Coach Name</div>
              <div class="text-base">{{ coachModal.coach?.name }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700 font-subtitle">Email</div>
              <div class="text-base">{{ coachModal.coach?.email || 'N/A' }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700 font-subtitle">Applied Date</div>
              <div class="text-base">{{ formatDate(coachModal.coach?.created_at) }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700 font-subtitle">Current Status</div>
              <div>
                <span
                  class="rounded-full px-2 py-1 text-xs font-medium capitalize"
                  :class="getStatusClass(coachModal.coach?.status_approval)"
                >
                  {{ coachModal.coach?.status_approval }}
                </span>
              </div>
            </div>
          </div>

          <div>
            <div class="text-sm font-medium text-slate-700 mb-2 font-subtitle">Bio</div>
            <div class="text-sm bg-slate-50 p-3 rounded-md">
              {{ coachModal.coach?.bio || 'No bio provided' }}
            </div>
          </div>

          <div>
            <div class="text-sm font-medium text-slate-700 mb-2 font-subtitle">Certification Document</div>
            <div v-if="coachModal.coach?.certification_doc" class="border border-slate-200 rounded-md p-4">
              <div class="flex items-center gap-3">
                <span class="text-3xl">📄</span>
                <div class="flex-1">
                  <div class="text-sm font-medium">Certification Document</div>
                </div>
                <a
                  :href="getDocumentUrl(coachModal.coach.certification_doc)"
                  target="_blank"
                  class="rounded-md bg-blue-500 px-3 py-1.5 text-sm text-white hover:bg-blue-600 font-bold"
                >
                  View PDF
                </a>
              </div>
            </div>
            <div v-else class="text-sm text-slate-500 italic">
              No certification document uploaded
            </div>
          </div>
        </div>

        <div class="flex justify-end items-center gap-3 border-t border-slate-200 px-5 py-4 bg-slate-50">
        <!-- Only show Approve/Reject when pending -->
          <div
            v-if="coachModal.coach?.status_approval === 'pending'"
            class="flex gap-2"
          >
            <button
              class="rounded-md bg-emerald-600 px-4 py-2 text-white hover:bg-emerald-700"
              @click="approveCoach(coachModal.coach)"
            >
              Approve Certification
            </button>
            <button
              class="rounded-md bg-rose-600 px-4 py-2 text-white hover:bg-rose-700"
              @click="openRejectModal(coachModal.coach)"
            >
              Reject
            </button>
          </div>
        </div>
      </div>
    </div>
    <div
      v-if="rejectModal.open"
      class="fixed inset-0 z-[70] grid place-items-center bg-black/50 p-4"
      role="dialog"
      aria-modal="true"
      @click.self="closeRejectModal"
    >
      <div class="w-full max-w-md rounded-xl bg-white shadow-lg p-6">
        <h3 class="text-lg font-semibold mb-4">Reject Coach</h3>
        <p class="mb-2">Reason for rejection (optional):</p>
        <textarea
          v-model="rejectModal.reason"
          rows="3"
          class="w-full border rounded p-2 mb-4"
          placeholder="Type a reason..."
        ></textarea>
        <div class="flex justify-end gap-3">
          <button @click="closeRejectModal" class="px-4 py-2 border rounded">Cancel</button>
          <button @click="confirmReject" class="px-4 py-2 bg-rose-600 text-white rounded hover:bg-rose-700">Reject</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import AdminSideBar from '@/components/AdminSideBar.vue'
import AdminNotificationBell from '@/components/AdminNotificationBell.vue'
import { Menu } from 'lucide-vue-next'
import { useToastStore } from '@/stores/toast'

const userStore = useUserStore()
const toast = useToastStore()

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
const sidebarOpen = ref(true)
const activeSection = ref('coaches')
const coachFilter = ref('all')
const searchQuery = ref('')
const loading = ref(false)
const error = ref(null)

const coaches = ref([])
const coachModal = ref({ open: false, coach: null })
const rejectModal = ref({
  open: false,
  coach: null,
  reason: ''
})

function openRejectModal(coach) {
  rejectModal.value.coach = coach
  rejectModal.value.reason = ''
  rejectModal.value.open = true
}

function closeRejectModal() {
  rejectModal.value = { open: false, coach: null, reason: '' }
}


const filteredCoaches = computed(() => {
  let result = [...coaches.value]

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(c =>
      c.name.toLowerCase().includes(q) ||
      c.email?.toLowerCase().includes(q) ||
      c.bio?.toLowerCase().includes(q)
    )
  }

  return result
})

function setSection(id) { activeSection.value = id; if(window.innerWidth < 768) sidebarOpen.value = false }
function getInitials(name) { return name?.split(' ').map(w => w[0]).join('').toUpperCase().slice(0,2) || '?' }
function formatDate(date) { return date ? new Date(date).toLocaleDateString('en-US', {year:'numeric',month:'short',day:'numeric'}) : 'N/A' }
function getStatusClass(status) {
  switch(status){case 'pending': return 'bg-amber-100 text-amber-800'; case 'approved': return 'bg-emerald-100 text-emerald-800'; case 'rejected': return 'bg-rose-100 text-rose-800'; default: return 'bg-slate-100 text-slate-800'}
}
function getDocumentUrl(doc) { 
  return doc.startsWith('http') ? doc : `${API_URL}${doc}`
}
function viewCoachDetails(coach) { coachModal.value = { open: true, coach } }
function closeModal() { coachModal.value = { open: false, coach: null } }

function logout() { userStore.logout?.(); window.location.href='/' }

async function fetchCoaches() {
  loading.value = true
  error.value = null
  try {
    const params = coachFilter.value !== 'all' ? `?status=${coachFilter.value}` : ''
    const res = await fetch(`${API_URL}/api/moderation/coaches/${params}`, {
      credentials: 'include',
      headers: { Accept: 'application/json' },
    })
    if (!res.ok) throw new Error('Failed to fetch coaches')
    coaches.value = await res.json()
  } catch(err) {
    console.error(err)
    error.value = 'Failed to load coaches'
  } finally { loading.value = false }
}

async function approveCoach(coach) {
  try {
    const res = await fetch(`${API_URL}/api/moderation/coaches/${coach.coach_id}/approve/`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    })
    if (!res.ok) throw new Error('Failed to approve coach')
    await fetchCoaches()
    closeModal()
  } catch(err) {
    console.error(err)
    toast.error('Failed to approve coach')
  }
}

async function confirmReject() {
  try {
    const coach = rejectModal.value.coach
    const res = await fetch(`${API_URL}/api/moderation/coaches/${coach.coach_id}/reject/`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ reason: rejectModal.value.reason })
    })
    if (!res.ok) throw new Error('Failed to reject coach')
    await fetchCoaches()
    closeRejectModal()
    closeModal() // optionally close the review modal too
  } catch(err) {
    console.error(err)
    toast.error('Failed to reject coach')
  }
}


onMounted(async () => {
  if (!userStore.profile) {
    await userStore.init()
  }
  await fetchCoaches()
})
</script>