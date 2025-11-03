<template>
  <div class="min-h-screen bg-slate-50 text-slate-900 font-subtitle">
    <!-- Mobile overlay -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 z-40 bg-black/40 md:hidden"
      @click="sidebarOpen = false"
    />

    <!-- Sidebar -->
    <aside
      class="fixed inset-y-0 left-0 z-50 w-72 bg-slate-900 text-white transition-transform duration-300 md:translate-x-0"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'"
      aria-label="Sidebar"
    >
      <div class="px-6 pb-6 pt-8 border-b border-white/10">
        <h1 class="text-xl font-bold text-blue-400">HealthQuest Admin</h1>
      </div>

      <nav class="px-2 py-6 space-y-8 overflow-y-auto h-[calc(100vh-88px)]">
        <div v-for="group in nav" :key="group.title" class="space-y-2">
          <div class="px-4 text-[11px] font-semibold tracking-wider uppercase text-slate-400">
            {{ group.title }}
          </div>

          <a
            v-for="item in group.items"
            :key="item.id"
            href="#"
            class="group flex items-center gap-3 rounded-md px-4 py-2.5 text-slate-300 hover:text-blue-400 hover:bg-blue-500/10 border-r-2 border-transparent"
            :class="activeSection === item.id ? 'bg-blue-500/10 text-blue-400 border-blue-500' : ''"
            @click.prevent="setSection(item.id)"
          >
            <span class="w-5 h-5 shrink-0">{{ item.icon }}</span>
            <span class="truncate">{{ item.label }}</span>
            <span
              v-if="item.badge"
              class="ml-auto rounded-full px-2 py-0.5 text-[11px] font-medium bg-rose-500 text-white"
            >
              {{ item.badge }}
            </span>
          </a>
        </div>
      </nav>
    </aside>

    <!-- Main column -->
    <div class="md:pl-72">
      <!-- Header -->
      <header class="sticky top-0 z-30 bg-white/90 backdrop-blur supports-[backdrop-filter]:bg-white/60 shadow-sm">
        <div class="flex items-center justify-between px-4 py-3 md:px-8">
          <div class="flex items-center gap-3">
            <button
              class="inline-flex md:hidden items-center justify-center rounded-md p-2 text-slate-700 hover:bg-slate-100"
              @click="sidebarOpen = !sidebarOpen"
              aria-label="Toggle menu"
            >
              ☰
            </button>

            <div class="relative hidden md:block">
              <span class="absolute left-3 top-1/2 -translate-y-1/2">🔍</span>
              <input
                type="text"
                placeholder="Search coaches..."
                v-model="searchQuery"
                class="w-80 rounded-md border border-slate-200 pl-9 pr-3 py-2 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/40"
              />
            </div>
          </div>

          <div class="flex items-center gap-3">
            <button
              class="rounded-md bg-blue-600 px-3 py-2 text-sm text-white hover:bg-blue-700"
              @click="goBackToApp"
            >
              Back to App
            </button>
            <button class="relative rounded-md bg-slate-100 p-2" @click="showNotifications">
              🔔
              <span v-if="pendingCount > 0" class="absolute right-1 top-1 inline-block h-2 w-2 rounded-full bg-rose-500"></span>
            </button>
            <div class="flex items-center gap-2">
              <div class="grid h-10 w-10 place-items-center rounded-full bg-blue-500 font-bold text-white">A</div>
              <div class="leading-tight">
                <div class="font-medium">{{ userStore.profile?.user?.username || 'Admin' }}</div>
                <div class="text-[11px] text-slate-500">Administrator</div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <main class="px-4 py-6 md:px-8">
        <!-- COACHES CERTIFICATION SECTION -->
        <section v-show="activeSection === 'coaches'" class="space-y-6">
          <div>
            <h2 class="text-2xl font-bold">Coach Certification Verification</h2>
            <p class="text-sm text-slate-500">Review and verify coach certifications</p>
          </div>

          <!-- Backend API Notice -->
          <div class="rounded-xl bg-amber-50 border border-amber-200 p-4">
            <div class="flex items-start gap-3">
              <span class="text-2xl">⚠️</span>
              <div class="flex-1">
                <h4 class="font-semibold text-amber-900">Backend API Required</h4>
                <p class="text-sm text-amber-800 mt-1">
                  To fully implement coach certification verification, the following backend endpoints are needed:
                </p>
                <ul class="text-sm text-amber-800 mt-2 list-disc list-inside space-y-1">
                  <li><code class="bg-amber-100 px-1 rounded">GET /api/admin/coaches/</code> - List all coaches with filters</li>
                  <li><code class="bg-amber-100 px-1 rounded">POST /api/admin/coaches/{id}/approve/</code> - Approve certification</li>
                  <li><code class="bg-amber-100 px-1 rounded">POST /api/admin/coaches/{id}/reject/</code> - Reject certification</li>
                </ul>
                <p class="text-sm text-amber-800 mt-2">Currently showing demonstration with mock data.</p>
              </div>
            </div>
          </div>

          <div class="rounded-xl bg-white p-5 shadow-sm">
            <div class="mb-4 flex items-center justify-between">
              <h3 class="text-base font-semibold">Coach Applications</h3>
              <div class="flex items-center gap-3">
                <select class="rounded-md border border-slate-200 px-3 py-2 text-sm" v-model="coachFilter">
                  <option value="all">All Status</option>
                  <option value="pending">Pending</option>
                  <option value="approved">Approved</option>
                  <option value="rejected">Rejected</option>
                </select>
                <button class="rounded-md bg-blue-600 px-3 py-2 text-sm text-white hover:bg-blue-700" @click="exportCoachList">
                  Export List
                </button>
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
                    <th class="px-3 py-2 text-left font-semibold">Coach Name</th>
                    <th class="px-3 py-2 text-left font-semibold">Email</th>
                    <th class="px-3 py-2 text-left font-semibold">Bio</th>
                    <th class="px-3 py-2 text-left font-semibold">Applied Date</th>
                    <th class="px-3 py-2 text-left font-semibold">Status</th>
                    <th class="px-3 py-2 text-left font-semibold">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="filteredCoaches.length === 0">
                    <td colspan="6" class="px-3 py-8 text-center text-slate-500">
                      No coaches found{{ coachFilter !== 'all' ? ' with status: ' + coachFilter : '' }}
                    </td>
                  </tr>
                  <tr
                    v-for="coach in filteredCoaches"
                    :key="coach.coach_id"
                    class="border-b border-slate-100 hover:bg-slate-50"
                  >
                    <td class="px-3 py-3">
                      <div class="flex items-center gap-2">
                        <div class="grid h-8 w-8 place-items-center rounded-full bg-blue-500 text-xs font-bold text-white">
                          {{ getInitials(coach.name) }}
                        </div>
                        {{ coach.name }}
                      </div>
                    </td>
                    <td class="px-3 py-3">{{ coach.email || 'N/A' }}</td>
                    <td class="px-3 py-3">
                      <div class="max-w-xs truncate">{{ coach.bio || 'No bio provided' }}</div>
                    </td>
                    <td class="px-3 py-3">{{ formatDate(coach.created_at) }}</td>
                    <td class="px-3 py-3">
                      <span
                        class="rounded-full px-2 py-0.5 text-[11px] font-medium capitalize"
                        :class="getStatusClass(coach.status_approval)"
                      >
                        {{ coach.status_approval }}
                      </span>
                    </td>
                    <td class="px-3 py-3">
                      <button
                        class="rounded-md bg-blue-600 px-3 py-1.5 text-white hover:bg-blue-700"
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

        <!-- OTHER SECTIONS Placeholders -->
        <section
          v-for="placeholder in ['dashboard','analytics','users','workouts','recipes','reports','settings','logs']"
          :key="placeholder"
          v-show="activeSection === placeholder"
          class="rounded-xl bg-white p-5 shadow-sm"
        >
          <h2 class="text-xl font-semibold capitalize">{{ placeholder }}</h2>
          <p class="mt-2 text-sm text-slate-600">Content for {{ placeholder }} will be added here.</p>
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
          <h3 class="text-lg font-semibold">Coach Certification Review</h3>
          <button class="text-slate-500 hover:text-slate-700" @click="closeModal">✕</button>
        </div>

        <div class="px-5 py-4 space-y-4 max-h-[70vh] overflow-y-auto">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <div class="text-sm font-medium text-slate-700">Coach Name</div>
              <div class="text-base">{{ coachModal.coach?.name }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Email</div>
              <div class="text-base">{{ coachModal.coach?.email || 'N/A' }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Applied Date</div>
              <div class="text-base">{{ formatDate(coachModal.coach?.created_at) }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Current Status</div>
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
            <div class="text-sm font-medium text-slate-700 mb-2">Bio</div>
            <div class="text-sm bg-slate-50 p-3 rounded-md">
              {{ coachModal.coach?.bio || 'No bio provided' }}
            </div>
          </div>

          <div>
            <div class="text-sm font-medium text-slate-700 mb-2">Certification Document</div>
            <div v-if="coachModal.coach?.certification_doc" class="border border-slate-200 rounded-md p-4">
              <div class="flex items-center gap-3">
                <span class="text-3xl">📄</span>
                <div class="flex-1">
                  <div class="text-sm font-medium">Certification Document</div>
                  <div class="text-xs text-slate-500">{{ coachModal.coach.certification_doc }}</div>
                </div>
                <a
                  :href="getDocumentUrl(coachModal.coach.certification_doc)"
                  target="_blank"
                  class="rounded-md bg-blue-600 px-3 py-1.5 text-sm text-white hover:bg-blue-700"
                >
                  View PDF
                </a>
              </div>
            </div>
            <div v-else class="text-sm text-slate-500 italic">
              No certification document uploaded
            </div>
          </div>

          <div v-if="coachModal.coach?.status_approval === 'pending'" class="bg-blue-50 border border-blue-200 rounded-md p-4">
            <div class="text-sm font-medium text-blue-900 mb-2">Verification Checklist</div>
            <ul class="text-sm text-blue-800 space-y-1">
              <li>✓ Verify certification document is valid and current</li>
              <li>✓ Check coach credentials match the information provided</li>
              <li>✓ Ensure bio is professional and appropriate</li>
              <li>✓ Confirm coach meets platform requirements</li>
            </ul>
          </div>
        </div>

        <div class="flex justify-between items-center gap-3 border-t border-slate-200 px-5 py-4 bg-slate-50">
          <div class="text-xs text-slate-500">
            Reviewing: {{ coachModal.coach?.name }}
          </div>
          <div class="flex gap-2">
            <button
              class="rounded-md border border-slate-300 bg-white px-4 py-2 text-slate-700 hover:bg-slate-50"
              @click="closeModal"
            >
              Cancel
            </button>
            <button
              v-if="coachModal.coach?.status_approval !== 'rejected'"
              class="rounded-md bg-rose-600 px-4 py-2 text-white hover:bg-rose-700"
              @click="rejectCoach(coachModal.coach)"
            >
              Reject
            </button>
            <button
              v-if="coachModal.coach?.status_approval !== 'approved'"
              class="rounded-md bg-emerald-600 px-4 py-2 text-white hover:bg-emerald-700"
              @click="approveCoach(coachModal.coach)"
            >
              Approve Certification
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const sidebarOpen = ref(false)
const activeSection = ref('coaches')
const coachFilter = ref('all')
const searchQuery = ref('')
const loading = ref(false)
const error = ref(null)

// Mock coaches data - In production, this would come from API
const coaches = ref([
  {
    coach_id: 1,
    name: 'Sarah Johnson',
    email: 'sarah.johnson@email.com',
    bio: 'Certified personal trainer with 5 years of experience in strength training and nutrition coaching.',
    certification_doc: 'coach_certifications/sarah_johnson_cert.pdf',
    status_approval: 'pending',
    created_at: '2024-09-10T10:30:00Z'
  },
  {
    coach_id: 2,
    name: 'Mike Rodriguez',
    email: 'mike.rodriguez@email.com',
    bio: 'Yoga instructor and mindfulness coach with RYT-500 certification. Specializing in holistic wellness.',
    certification_doc: 'coach_certifications/mike_rodriguez_cert.pdf',
    status_approval: 'approved',
    created_at: '2024-09-09T14:20:00Z',
    approved_date: '2024-09-10T09:15:00Z'
  },
  {
    coach_id: 3,
    name: 'Lisa Wang',
    email: 'lisa.wang@email.com',
    bio: 'Nutrition coach and registered dietitian. Helping clients achieve sustainable healthy eating habits.',
    certification_doc: 'coach_certifications/lisa_wang_cert.pdf',
    status_approval: 'pending',
    created_at: '2024-09-08T16:45:00Z'
  },
  {
    coach_id: 4,
    name: 'James Smith',
    email: 'james.smith@email.com',
    bio: 'CrossFit Level 2 trainer with focus on functional fitness and athletic performance.',
    certification_doc: 'coach_certifications/james_smith_cert.pdf',
    status_approval: 'rejected',
    created_at: '2024-09-05T11:00:00Z'
  }
])

const nav = [
  {
    title: 'Overview',
    items: [
      { id: 'dashboard', label: 'Dashboard', icon: '📊' },
      { id: 'analytics', label: 'Analytics', icon: '📈' }
    ]
  },
  {
    title: 'User Management',
    items: [
      { id: 'users', label: 'Users', icon: '👥' },
      { id: 'coaches', label: 'Coaches', icon: '🏃', badge: pendingCount.value || null }
    ]
  },
  {
    title: 'Content Management',
    items: [
      { id: 'workouts', label: 'Workouts', icon: '💪' },
      { id: 'recipes', label: 'Recipes', icon: '🍽️' },
      { id: 'reports', label: 'Reports', icon: '⚠️' }
    ]
  },
  {
    title: 'System',
    items: [
      { id: 'settings', label: 'Settings', icon: '⚙️' },
      { id: 'logs', label: 'Audit Logs', icon: '📋' }
    ]
  }
]

const coachModal = ref({
  open: false,
  coach: null
})

const filteredCoaches = computed(() => {
  let result = coaches.value

  // Filter by status
  if (coachFilter.value !== 'all') {
    result = result.filter(c => c.status_approval === coachFilter.value)
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(c =>
      c.name.toLowerCase().includes(query) ||
      c.email?.toLowerCase().includes(query) ||
      c.bio?.toLowerCase().includes(query)
    )
  }

  return result
})

const pendingCount = computed(() => {
  return coaches.value.filter(c => c.status_approval === 'pending').length
})

function setSection(id) {
  activeSection.value = id
  if (window.innerWidth < 768) sidebarOpen.value = false
}

function goBackToApp() {
  router.push('/')
}

function getInitials(name) {
  if (!name) return '?'
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

function getStatusClass(status) {
  switch (status) {
    case 'pending':
      return 'bg-amber-100 text-amber-800'
    case 'approved':
      return 'bg-emerald-100 text-emerald-800'
    case 'rejected':
      return 'bg-rose-100 text-rose-800'
    default:
      return 'bg-slate-100 text-slate-800'
  }
}

function getDocumentUrl(doc) {
  if (!doc) return '#'
  // In production, this would be the full URL to the document
  return `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/media/${doc}`
}

function viewCoachDetails(coach) {
  coachModal.value = {
    open: true,
    coach: coach
  }
}

function closeModal() {
  coachModal.value = {
    open: false,
    coach: null
  }
}

function approveCoach(coach) {
  // In production, this would make an API call to approve the coach
  // POST /api/admin/coaches/{coach.coach_id}/approve/

  console.log('Approving coach:', coach)

  // Update local state (demo only)
  const index = coaches.value.findIndex(c => c.coach_id === coach.coach_id)
  if (index !== -1) {
    coaches.value[index].status_approval = 'approved'
    coaches.value[index].approved_date = new Date().toISOString()
  }

  alert(`✓ Coach "${coach.name}" has been approved!\n\nIn production, this would:\n1. Update the database\n2. Send approval email to coach\n3. Grant coach permissions\n4. Log the action in audit trail`)

  closeModal()
}

function rejectCoach(coach) {
  const reason = prompt('Please provide a reason for rejection (optional):')

  // In production, this would make an API call to reject the coach
  // POST /api/admin/coaches/{coach.coach_id}/reject/
  // Body: { reason: reason }

  console.log('Rejecting coach:', coach, 'Reason:', reason)

  // Update local state (demo only)
  const index = coaches.value.findIndex(c => c.coach_id === coach.coach_id)
  if (index !== -1) {
    coaches.value[index].status_approval = 'rejected'
    coaches.value[index].rejection_reason = reason
  }

  alert(`✗ Coach "${coach.name}" has been rejected.\n\nIn production, this would:\n1. Update the database\n2. Send rejection email to coach\n3. Log the action in audit trail\n4. Allow coach to resubmit`)

  closeModal()
}

function exportCoachList() {
  alert('Exporting coach list as CSV - download would start here\n\nIn production, this would generate a CSV file with all coach data.')
}

function showNotifications() {
  alert(`${pendingCount.value} pending coach applications require review`)
}

onMounted(() => {
  // In production, fetch coaches from API here
  // fetchCoaches()
  console.log('AdminDashboard mounted. Ready to verify coach certifications.')
})
</script>
