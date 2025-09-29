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
                  placeholder="Search users, coaches, content..."
                  class="w-80 rounded-md border border-slate-200 pl-9 pr-3 py-2 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/40"
                />
              </div>
            </div>
  
            <div class="flex items-center gap-3">
              <button 
                class="rounded-md bg-blue-600 px-3 py-2 text-sm text-white hover:bg-blue-700"
                @click="$emit('page-change', 'goal-selection')"
              >
                Back to App
              </button>
              <button class="relative rounded-md bg-slate-100 p-2" @click="showNotifications">
                🔔
                <span class="absolute right-1 top-1 inline-block h-2 w-2 rounded-full bg-rose-500"></span>
              </button>
              <div class="flex items-center gap-2">
                <div class="grid h-10 w-10 place-items-center rounded-full bg-blue-500 font-bold text-white">A</div>
                <div class="leading-tight">
                  <div class="font-medium">Admin User</div>
                  <div class="text-[11px] text-slate-500">Super Admin</div>
                </div>
              </div>
            </div>
          </div>
        </header>
  
        <!-- Page content -->
        <main class="px-4 py-6 md:px-8">
          <!-- DASHBOARD -->
          <section v-show="activeSection === 'dashboard'" class="space-y-6">
            <div>
              <h2 class="text-2xl font-bold">Dashboard Overview</h2>
              <p class="text-sm text-slate-500">Monitor key metrics and platform activity</p>
            </div>
  
            <!-- Stats -->
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
              <div class="relative overflow-hidden rounded-xl p-5 text-white bg-gradient-to-br from-blue-500 to-blue-800">
                <div class="absolute right-4 top-4 text-xs/none opacity-80">↗️ +12%</div>
                <div class="text-3xl font-bold">2,847</div>
                <div class="opacity-90">Total Users</div>
              </div>
              <div class="relative overflow-hidden rounded-xl p-5 text-white bg-gradient-to-br from-emerald-500 to-emerald-700">
                <div class="absolute right-4 top-4 text-xs/none opacity-80">↗️ +8%</div>
                <div class="text-3xl font-bold">156</div>
                <div class="opacity-90">Active Coaches</div>
              </div>
              <div class="relative overflow-hidden rounded-xl p-5 text-white bg-gradient-to-br from-amber-500 to-amber-700">
                <div class="absolute right-4 top-4 text-xs/none opacity-80">⏳ 5 pending</div>
                <div class="text-3xl font-bold">1,248</div>
                <div class="opacity-90">Content Items</div>
              </div>
              <div class="relative overflow-hidden rounded-xl p-5 text-white bg-gradient-to-br from-rose-500 to-rose-700">
                <div class="absolute right-4 top-4 text-xs/none opacity-80">📈 99.9%</div>
                <div class="text-3xl font-bold">17</div>
                <div class="opacity-90">Reports Queue</div>
              </div>
            </div>
  
            <!-- Grid -->
            <div class="grid gap-6 xl:grid-cols-[2fr_1fr]">
              <!-- Chart -->
              <div class="rounded-xl bg-white p-5 shadow-sm">
                <div class="mb-4 flex items-center justify-between">
                  <h3 class="text-base font-semibold">User Growth & Engagement</h3>
                  <select
                    v-model="selectedRange"
                    class="rounded-md border border-slate-200 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40"
                    @change="refreshChart"
                  >
                    <option>Last 7 days</option>
                    <option>Last 30 days</option>
                    <option>Last 3 months</option>
                  </select>
                </div>
                <div class="h-72">
                  <canvas ref="growthCanvas" class="h-full w-full"></canvas>
                </div>
              </div>
  
              <!-- Activity -->
              <div class="rounded-xl bg-white p-5 shadow-sm">
                <div class="mb-4 flex items-center justify-between">
                  <h3 class="text-base font-semibold">Recent Activity</h3>
                  <button class="btn-secondary" @click="showAllActivity">View All</button>
                </div>
  
                <div class="max-h-96 space-y-4 overflow-y-auto pr-2">
                  <div v-for="(a,i) in activities" :key="i" class="flex items-center gap-3 border-b border-slate-100 pb-4 last:border-b-0">
                    <div
                      class="grid h-10 w-10 place-items-center rounded-full text-xl"
                      :class="a.type === 'user' ? 'bg-blue-100 text-blue-600' : a.type === 'coach' ? 'bg-emerald-100 text-emerald-600' : 'bg-amber-100 text-amber-700'"
                    >
                      {{ a.icon }}
                    </div>
                    <div class="flex-1">
                      <div class="font-medium">{{ a.title }}</div>
                      <div class="text-xs text-slate-500">{{ a.when }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
  
            <!-- Pending Actions -->
            <div class="rounded-xl bg-white p-5 shadow-sm">
              <div class="mb-4 flex items-center justify-between">
                <h3 class="text-base font-semibold">Pending Actions</h3>
                <span class="rounded-full bg-amber-100 px-3 py-1 text-xs font-medium text-amber-800">17 items require attention</span>
              </div>
  
              <div class="overflow-x-auto">
                <table class="w-full border-collapse text-sm">
                  <thead class="text-slate-500">
                    <tr class="border-b border-slate-200">
                      <th class="px-3 py-2 text-left font-semibold">Type</th>
                      <th class="px-3 py-2 text-left font-semibold">Item</th>
                      <th class="px-3 py-2 text-left font-semibold">Submitted By</th>
                      <th class="px-3 py-2 text-left font-semibold">Date</th>
                      <th class="px-3 py-2 text-left font-semibold">Priority</th>
                      <th class="px-3 py-2 text-left font-semibold">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="border-b border-slate-100 hover:bg-slate-50">
                      <td class="px-3 py-3">Coach Review</td>
                      <td class="px-3 py-3">Sarah Johnson - Fitness Cert.</td>
                      <td class="px-3 py-3">sarah.johnson@email.com</td>
                      <td class="px-3 py-3">Today</td>
                      <td class="px-3 py-3"><span class="rounded-full bg-amber-100 px-2 py-0.5 text-[11px] font-medium text-amber-800">High</span></td>
                      <td class="px-3 py-3 space-x-2">
                        <button class="rounded-md bg-emerald-600 px-3 py-1.5 text-white hover:bg-emerald-700" @click="approveItem('coach-review', 'Sarah Johnson')">Approve</button>
                        <button class="rounded-md bg-rose-600 px-3 py-1.5 text-white hover:bg-rose-700" @click="rejectItem('coach-review', 'Sarah Johnson')">Reject</button>
                      </td>
                    </tr>
                    <tr class="border-b border-slate-100 hover:bg-slate-50">
                      <td class="px-3 py-3">Content Flag</td>
                      <td class="px-3 py-3">"Keto Breakfast Bowl" Recipe</td>
                      <td class="px-3 py-3">System</td>
                      <td class="px-3 py-3">Yesterday</td>
                      <td class="px-3 py-3"><span class="rounded-full bg-amber-100 px-2 py-0.5 text-[11px] font-medium text-amber-800">Medium</span></td>
                      <td class="px-3 py-3">
                        <button class="rounded-md bg-blue-600 px-3 py-1.5 text-white hover:bg-blue-700" @click="reviewContent('Keto Breakfast Bowl')">Review</button>
                      </td>
                    </tr>
                    <tr class="hover:bg-slate-50">
                      <td class="px-3 py-3">User Report</td>
                      <td class="px-3 py-3">Inappropriate Coach Behavior</td>
                      <td class="px-3 py-3">user.complaint@email.com</td>
                      <td class="px-3 py-3">2 days ago</td>
                      <td class="px-3 py-3"><span class="rounded-full bg-rose-100 px-2 py-0.5 text-[11px] font-medium text-rose-800">High</span></td>
                      <td class="px-3 py-3">
                        <button class="rounded-md bg-blue-600 px-3 py-1.5 text-white hover:bg-blue-700" @click="investigateReport('Inappropriate Coach Behavior')">Investigate</button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </section>
  
          <!-- COACHES -->
          <section v-show="activeSection === 'coaches'" class="space-y-6">
            <div>
              <h2 class="text-2xl font-bold">Coach Management</h2>
              <p class="text-sm text-slate-500">Review applications and manage certified coaches</p>
            </div>
  
            <div class="rounded-xl bg-white p-5 shadow-sm">
              <div class="mb-4 flex items-center justify-between">
                <h3 class="text-base font-semibold">Coach Applications</h3>
                <div class="flex items-center gap-3">
                  <select class="rounded-md border border-slate-200 px-3 py-2 text-sm" v-model="coachFilter" @change="filterCoaches">
                    <option>All Status</option>
                    <option>Pending</option>
                    <option>Approved</option>
                    <option>Rejected</option>
                  </select>
                  <button class="rounded-md bg-blue-600 px-3 py-2 text-sm text-white hover:bg-blue-700" @click="exportCoachList">
                    Export List
                  </button>
                </div>
              </div>
  
              <div class="overflow-x-auto">
                <table class="w-full border-collapse text-sm">
                  <thead class="text-slate-500">
                    <tr class="border-b border-slate-200">
                      <th class="px-3 py-2 text-left font-semibold">Coach Name</th>
                      <th class="px-3 py-2 text-left font-semibold">Email</th>
                      <th class="px-3 py-2 text-left font-semibold">Specialization</th>
                      <th class="px-3 py-2 text-left font-semibold">Experience</th>
                      <th class="px-3 py-2 text-left font-semibold">Applied Date</th>
                      <th class="px-3 py-2 text-left font-semibold">Status</th>
                      <th class="px-3 py-2 text-left font-semibold">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="border-b border-slate-100 hover:bg-slate-50">
                      <td class="px-3 py-3">
                        <div class="flex items-center gap-2">
                          <div class="grid h-8 w-8 place-items-center rounded-full bg-blue-500 text-xs font-bold text-white">SJ</div>
                          Sarah Johnson
                        </div>
                      </td>
                      <td class="px-3 py-3">sarah.johnson@email.com</td>
                      <td class="px-3 py-3">Strength Training</td>
                      <td class="px-3 py-3">5 years</td>
                      <td class="px-3 py-3">2024-09-10</td>
                      <td class="px-3 py-3"><span class="rounded-full bg-amber-100 px-2 py-0.5 text-[11px] font-medium text-amber-800">Pending</span></td>
                      <td class="px-3 py-3">
                        <button class="rounded-md bg-blue-600 px-3 py-1.5 text-white hover:bg-blue-700" @click="viewCoachDetails('Sarah Johnson')">
                          Review
                        </button>
                      </td>
                    </tr>
                    <tr class="border-b border-slate-100 hover:bg-slate-50">
                      <td class="px-3 py-3">
                        <div class="flex items-center gap-2">
                          <div class="grid h-8 w-8 place-items-center rounded-full bg-blue-500 text-xs font-bold text-white">MR</div>
                          Mike Rodriguez
                        </div>
                      </td>
                      <td class="px-3 py-3">mike.rodriguez@email.com</td>
                      <td class="px-3 py-3">Yoga & Mindfulness</td>
                      <td class="px-3 py-3">8 years</td>
                      <td class="px-3 py-3">2024-09-09</td>
                      <td class="px-3 py-3"><span class="rounded-full bg-emerald-100 px-2 py-0.5 text-[11px] font-medium text-emerald-800">Approved</span></td>
                      <td class="px-3 py-3">
                        <button class="rounded-md bg-slate-100 px-3 py-1.5 text-slate-900 hover:bg-slate-200" @click="viewCoachProfile('Mike Rodriguez')">View Profile</button>
                      </td>
                    </tr>
                    <tr class="hover:bg-slate-50">
                      <td class="px-3 py-3">
                        <div class="flex items-center gap-2">
                          <div class="grid h-8 w-8 place-items-center rounded-full bg-blue-500 text-xs font-bold text-white">LW</div>
                          Lisa Wang
                        </div>
                      </td>
                      <td class="px-3 py-3">lisa.wang@email.com</td>
                      <td class="px-3 py-3">Nutrition Coaching</td>
                      <td class="px-3 py-3">3 years</td>
                      <td class="px-3 py-3">2024-09-08</td>
                      <td class="px-3 py-3"><span class="rounded-full bg-amber-100 px-2 py-0.5 text-[11px] font-medium text-amber-800">Pending</span></td>
                      <td class="px-3 py-3">
                        <button class="rounded-md bg-blue-600 px-3 py-1.5 text-white hover:bg-blue-700" @click="viewCoachDetails('Lisa Wang')">
                          Review
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </section>
  
          <!-- USERS -->
          <section v-show="activeSection === 'users'" class="space-y-6">
            <div>
              <h2 class="text-2xl font-bold">User Management</h2>
              <p class="text-sm text-slate-500">Monitor user activity and engagement</p>
            </div>
            <div class="rounded-xl bg-white p-5 shadow-sm">
              <h3 class="text-base font-semibold">User Overview</h3>
              <p class="mt-2 text-sm text-slate-600">User management content would go here…</p>
            </div>
          </section>
  
          <!-- Placeholders for other sections -->
          <section
            v-for="placeholder in ['analytics','workouts','recipes','reports','settings','logs']"
            :key="placeholder"
            v-show="activeSection === placeholder"
            class="rounded-xl bg-white p-5 shadow-sm"
          >
            <h2 class="text-xl font-semibold capitalize">{{ placeholder }}</h2>
            <p class="mt-2 text-sm text-slate-600">Content for {{ placeholder }} will be added here.</p>
          </section>
        </main>
      </div>
  
      <!-- Modal -->
      <div
        v-if="coachModal.open"
        class="fixed inset-0 z-[60] grid place-items-center bg-black/50 p-4"
        role="dialog"
        aria-modal="true"
      >
        <div class="w-full max-w-lg overflow-hidden rounded-xl bg-white shadow-lg">
          <div class="flex items-center justify-between border-b border-slate-200 px-5 py-4">
            <h3 class="text-base font-semibold">Coach Review</h3>
            <button class="text-slate-500 hover:text-slate-700" @click="coachModal.open = false">✕</button>
          </div>
          <div class="px-5 py-4 space-y-2">
            <div class="text-sm"><span class="font-medium">Name:</span> {{ coachModal.name }}</div>
            <div class="text-sm"><span class="font-medium">Docs:</span> Certification.pdf, ID.png</div>
            <div class="text-sm"><span class="font-medium">Notes:</span> Good portfolio, pending verification.</div>
          </div>
          <div class="flex justify-end gap-2 border-t border-slate-200 px-5 py-4">
            <button class="rounded-md bg-rose-600 px-4 py-2 text-white hover:bg-rose-700" @click="coachModal.open=false">
              Reject
            </button>
            <button class="rounded-md bg-emerald-600 px-4 py-2 text-white hover:bg-emerald-700" @click="coachModal.open=false">
              Approve
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
  import Chart from 'chart.js/auto'
  
  const sidebarOpen = ref(false)
  const activeSection = ref('dashboard')
  const selectedRange = ref('Last 7 days')
  const coachFilter = ref('All Status')
  const notifications = ref([])
  
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
        { id: 'coaches', label: 'Coaches', icon: '🏃', badge: 5 }
      ]
    },
    {
      title: 'Content Management',
      items: [
        { id: 'workouts', label: 'Workouts', icon: '💪' },
        { id: 'recipes', label: 'Recipes', icon: '🍽️', badge: 12 },
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
  
  function setSection(id) {
    activeSection.value = id
    if (window.innerWidth < 768) sidebarOpen.value = false
  }
  
  const activities = ref([
    { icon: '👤', type: 'user', title: 'New user registration', when: '2 minutes ago' },
    { icon: '🏃', type: 'coach', title: 'Coach certification submitted', when: '15 minutes ago' },
    { icon: '📝', type: 'content', title: 'Recipe flagged for review', when: '1 hour ago' },
    { icon: '👤', type: 'user', title: 'User reached Gold tier', when: '2 hours ago' },
    { icon: '🏃', type: 'coach', title: 'Coach application approved', when: '3 hours ago' }
  ])
  
  // Chart.js
  const growthCanvas = ref(null)
  let growthChart = null
  
  function growthData(range) {
    if (range === 'Last 3 months') {
      return {
        labels: Array.from({ length: 12 }, (_, i) => `W${i + 1}`),
        data1: [30, 28, 40, 35, 42, 50, 55, 53, 60, 62, 68, 75],
        data2: [12, 14, 18, 16, 22, 25, 30, 28, 31, 33, 36, 40]
      }
    }
    if (range === 'Last 30 days') {
      return {
        labels: Array.from({ length: 10 }, (_, i) => `D${i + 1}`),
        data1: [12, 14, 10, 16, 18, 22, 24, 20, 26, 28],
        data2: [5, 7, 6, 8, 9, 10, 12, 9, 11, 13]
      }
    }
    // Last 7 days
    return {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      data1: [10, 12, 9, 14, 16, 18, 15],
      data2: [4, 5, 4, 6, 7, 8, 7]
    }
  }
  
  function buildChart() {
    const ctx = growthCanvas.value?.getContext('2d')
    if (!ctx) return
    const { labels, data1, data2 } = growthData(selectedRange.value)
    growthChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          { label: 'New Users', data: data1, borderWidth: 2, tension: 0.3, fill: false },
          { label: 'Active Sessions', data: data2, borderWidth: 2, tension: 0.3, fill: false }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: { legend: { display: true } },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: 'rgba(148, 163, 184, 0.2)' } }
        }
      }
    })
  }
  
  function refreshChart() {
    if (activeSection.value !== 'dashboard') return
    if (growthChart) {
      const { labels, data1, data2 } = growthData(selectedRange.value)
      growthChart.data.labels = labels
      growthChart.data.datasets[0].data = data1
      growthChart.data.datasets[1].data = data2
      growthChart.update()
    } else {
      // in case canvas just mounted
      buildChart()
    }
  }
  
  watch(activeSection, (val) => {
    // Build/destroy chart depending on visible section
    if (val === 'dashboard') {
      queueMicrotask(() => {
        if (growthChart) growthChart.destroy()
        buildChart()
      })
    } else if (growthChart) {
      growthChart.destroy()
      growthChart = null
    }
  })
  
  onMounted(() => {
    if (activeSection.value === 'dashboard') buildChart()
    // simple ESC to close sidebar on mobile / modal
    window.addEventListener('keydown', onKey)
  })
  
  onBeforeUnmount(() => {
    if (growthChart) growthChart.destroy()
    window.removeEventListener('keydown', onKey)
  })
  
  function onKey(e) {
    if (e.key === 'Escape') {
      sidebarOpen.value = false
      coachModal.value.open = false
    }
  }
  
  // Modal
  const coachModal = ref({ open: false, name: '' })
  function viewCoachDetails(name) {
    coachModal.value = { open: true, name }
  }

  // Mock interaction handlers
  function showAllActivity() {
    alert('Showing all activity feed - this would open a detailed view')
  }

  function approveItem(type, item) {
    alert(`Approved ${type}: ${item}`)
    // Remove from pending actions in real app
  }

  function rejectItem(type, item) {
    alert(`Rejected ${type}: ${item}`)
    // Remove from pending actions in real app
  }

  function reviewContent(content) {
    alert(`Reviewing content: ${content}`)
  }

  function investigateReport(report) {
    alert(`Investigating report: ${report}`)
  }

  function exportCoachList() {
    alert('Exporting coach list as CSV - download would start here')
  }

  function filterCoaches() {
    alert(`Filtering coaches by: ${coachFilter.value}`)
  }

  function viewCoachProfile(name) {
    alert(`Viewing profile for coach: ${name}`)
  }

  function showNotifications() {
    alert('Notifications panel - showing 3 new notifications')
  }
  </script>
  
  <!-- No component CSS: entirely Tailwind v4 utilities -->
  