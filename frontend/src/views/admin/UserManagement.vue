<template>
    <div class="min-h-screen bg-slate-50 text-slate-900">
      <!-- Sidebar overlay -->
      <div v-if="sidebarOpen" class="fixed inset-0 z-40 bg-black/40 md:hidden" @click="sidebarOpen = false" />
  
      <!-- Sidebar -->
      <AdminSideBar
        :sidebarOpen="sidebarOpen"
        :activeSection="activeSection"
        :nav="nav"
        @close="sidebarOpen = false"
        @select="setSection"
      />
  
      <!-- Main content -->
      <div :class="sidebarOpen ? 'md:pl-72' : 'md:pl-0'">
        <!-- Header -->
        <header class="sticky top-0 left-0 right-0 z-30 bg-white/90 backdrop-blur shadow-sm">
          <div class="flex items-center justify-between px-4 py-3 md:px-8">
            <div class="flex items-center gap-3">
              <button @click="sidebarOpen = !sidebarOpen" class="inline-flex items-center justify-center rounded-md p-2 text-slate-700 hover:bg-slate-100" aria-label="Toggle menu">☰</button>
              <input v-model="searchQuery" placeholder="Search coaches..." class="hidden md:block w-80 rounded-md border border-slate-200 pl-5 pr-3 py-2 text-sm font-subtitle placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/40"/>
            </div>
  
            <div class="flex items-center gap-3">
              <button @click="showNotifications" class="relative rounded-md bg-slate-100 p-2">
                🔔<span v-if="pendingCount > 0" class="absolute right-1 top-1 h-2 w-2 rounded-full bg-rose-500"></span>
              </button>
  
              <!-- User info -->
              <div class="flex items-center gap-2">
                <div class="grid h-10 w-10 place-items-center rounded-full bg-blue-500 font-bold text-white">
                  {{ userStore.user?.username ? getInitials(userStore.user.username) : '?' }}
                </div>
                <div class="leading-tight">
                  <div class="font-medium">{{ userStore.user?.username || 'Loading...' }}</div>
                  <div class="text-[11px] text-slate-500">Administrator</div>
                </div>
              </div>
  
              <button @click="logout" class="ml-3 flex items-center py-2 px-3 rounded-md hover:bg-gray-100">
                <span class="material-symbols-outlined">logout</span>
              </button>
            </div>
          </div>
        </header>
  
        <!-- Page content -->
        <div class="p-5 space-y-4">
          <div>
            <h2 class="text-2xl font-bold">User Management</h2>
            <p class="text-sm text-slate-500">View all users and manage their accounts</p>
          </div>
  
          <div class="rounded-xl bg-white p-5 shadow-sm">
            <div class="mb-4 flex items-center justify-between">
              <h3 class="text-base font-semibold">All Users</h3>
              <div class="flex items-center gap-3">
                <select v-model="userRoleFilter" class="rounded-md border border-slate-200 px-3 py-2 text-sm">
                  <option value="all">All Roles</option>
                  <option value="normal">Normal Users</option>
                  <option value="coach">Coaches</option>
                  <option value="member">Members</option>
                </select>
                <div class="relative">
                  <span class="absolute left-3 top-1/2 -translate-y-1/2">🔍</span>
                  <input v-model="userSearchQuery" placeholder="Search users..." class="rounded-md border border-slate-200 pl-9 pr-3 py-2 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/40"/>
                </div>
              </div>
            </div>
  
            <!-- Loading / Error / Table -->
            <div v-if="loadingUsers" class="text-center py-8 text-slate-500">Loading users...</div>
            <div v-else-if="loadError" class="text-center py-8 text-rose-500">Failed to load users.</div>
            <div v-else-if="filteredUsers.length === 0" class="text-center py-8 text-slate-500">No users found.</div>
            <div v-else class="overflow-x-auto">
              <table class="w-full border-collapse text-sm">
                <thead class="text-slate-500">
                  <tr class="border-b border-slate-200">
                    <th class="px-3 py-2 text-left font-semibold">User</th>
                    <th class="px-3 py-2 text-left font-semibold">Email</th>
                    <th class="px-3 py-2 text-left font-semibold">Role</th>
                    <th class="px-3 py-2 text-left font-semibold">Level</th>
                    <th class="px-3 py-2 text-left font-semibold">Joined</th>
                    <th class="px-3 py-2 text-left font-semibold">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in filteredUsers" :key="user.id" class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="px-3 py-3 flex items-center gap-2">
                      <div class="grid h-8 w-8 place-items-center rounded-full bg-blue-500 text-xs font-bold text-white">{{ getInitials(user.username) }}</div>
                      {{ user.username }}
                    </td>
                    <td class="px-3 py-3">{{ user.email || 'N/A' }}</td>
                    <td class="px-3 py-3"><span class="rounded-full px-2 py-0.5 text-[11px] font-medium capitalize" :class="getRoleClass(user.role)">{{ user.role }}</span></td>
                    <td class="px-3 py-3"><span class="text-xs text-slate-600">{{ user.level }} ({{ user.xp }} XP)</span></td>
                    <td class="px-3 py-3">{{ formatDate(user.created_at) }}</td>
                    <td class="px-3 py-3 flex gap-2">
                      <button @click="viewUserDetails(user)" class="rounded-md bg-blue-600 px-3 py-1.5 text-white hover:bg-blue-700 text-xs">View</button>
                      <button @click="confirmDeleteUser(user)" class="rounded-md bg-rose-600 px-3 py-1.5 text-white hover:bg-rose-700 text-xs">Delete</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
  
        <!-- User Modal -->
        <div v-if="userModal.open" class="fixed inset-0 z-[60] grid place-items-center bg-black/50 p-4" role="dialog" aria-modal="true" @click.self="closeUserModal">
          <div class="w-full max-w-2xl rounded-xl bg-white shadow-lg overflow-hidden">
            <div class="flex items-center justify-between border-b border-slate-200 px-5 py-4">
              <h3 class="text-lg font-semibold">User Profile Details</h3>
              <button @click="closeUserModal" class="text-slate-500 hover:text-slate-700">✕</button>
            </div>
            <div class="px-5 py-4 max-h-[70vh] overflow-y-auto space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <template v-for="(value, label) in modalFields" :key="label">
                  <div>
                    <div class="text-sm font-medium text-slate-700">{{ label }}</div>
                    <div class="text-base">{{ value }}</div>
                  </div>
                </template>
              </div>
  
              <div v-if="userModal.user?.fitness_goals?.length">
                <div class="text-sm font-medium text-slate-700 mb-2">Fitness Goals</div>
                <div class="flex flex-wrap gap-2">
                  <span v-for="goal in userModal.user.fitness_goals" :key="goal" class="rounded-full bg-blue-100 px-3 py-1 text-xs text-blue-800">{{ goal.goal_type }}</span>
                </div>
              </div>
  
              <div v-if="userModal.user?.achievements?.length">
                <div class="text-sm font-medium text-slate-700 mb-2">Achievements</div>
                <div class="space-y-2">
                  <div v-for="ach in userModal.user.achievements" :key="ach.title" class="flex items-center gap-2 rounded-md bg-amber-50 p-2">
                    <span class="text-xl">🏆</span>
                    <div>
                      <div class="text-sm font-medium">{{ ach.title }}</div>
                      <div class="text-xs text-slate-600">+{{ ach.xp_reward }} XP</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
  
            <div class="flex justify-end gap-3 border-t border-slate-200 px-5 py-4 bg-slate-50">
              <button @click="closeUserModal" class="rounded-md border border-slate-300 bg-white px-4 py-2 text-slate-700 hover:bg-slate-50">Close</button>
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
  
  const userStore = useUserStore()
  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
  
  const sidebarOpen = ref(true)
  const activeSection = ref('workouts')
  const searchQuery = ref('')
  const pendingCount = ref(0)
  
  const users = ref([])
  const loadingUsers = ref(true)
  const loadError = ref(false)
  const userRoleFilter = ref('all')
  const userSearchQuery = ref('')
  const userModal = ref({ open: false, user: null })
  
  const nav = ref([])
  function setSection(section) { activeSection.value = section }
  
  const filteredUsers = computed(() => 
  users.value.filter(user => {
    const matchesRole = userRoleFilter.value === 'all' || user.role === userRoleFilter.value
    const matchesSearch = !userSearchQuery.value || user.username.toLowerCase().includes(userSearchQuery.value.toLowerCase())
    const isNotAdmin = user.role !== 'admin'
    return matchesRole && matchesSearch && isNotAdmin
  })
)
  
  const modalFields = computed(() => {
    if (!userModal.value.user) return {}
    const u = userModal.value.user
    return {
      Username: u.username,
      Email: u.email || 'N/A',
      Role: u.role,
      Level: `${u.level} (${u.xp} XP)`,
      Gender: u.gender || 'N/A',
      Age: u.age || 'N/A',
      Height: u.height ? u.height + ' cm' : 'N/A',
      Weight: u.weight ? u.weight + ' kg' : 'N/A',
      Location: u.location || 'N/A',
      'Joined Date': u.created_at ? new Date(u.created_at).toLocaleDateString() : 'N/A'
    }

  })
  
  onMounted(async () => {
    loadingUsers.value = true
    try {
        const res = await fetch(`${API_URL}/api/users/`, { credentials: 'include' })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)

        const data = await res.json()
        // data is an array of users
        users.value = data.map(u => ({
        id: u.id,
        username: u.username,
        email: u.email,
        role: u.profile?.role || 'normal',
        level: u.profile?.current_level?.level || 'Bronze',
        xp: u.profile?.current_level?.xp || 0,
        gender: u.profile?.gender,
        age: u.profile?.age,
        height: u.profile?.height,
        weight: u.profile?.weight,
        location: u.profile?.location,
        fitness_goals: u.profile?.fitness_goals?.map(g => g.goal_type) || [],
        achievements: u.profile?.achievements || [],
        created_at: u.profile?.created_at || u.date_joined
        }))
    } catch (err) {
        console.error('Failed to fetch users:', err)
        loadError.value = true
    } finally {
        loadingUsers.value = false
    }
    })
  
  function formatDate(d) { return d ? new Date(d).toLocaleDateString() : 'N/A' }
  function getInitials(name) { return name ? name.split(' ').map(n=>n[0]).join('').toUpperCase() : '?' }
  function getRoleClass(role) {
    switch(role) {
      case 'coach': return 'bg-emerald-100 text-emerald-800'
      case 'member': return 'bg-purple-100 text-purple-800'
      case 'admin': return 'bg-amber-100 text-amber-800'
      default: return 'bg-blue-100 text-blue-800'
    }
  }
  
  function viewUserDetails(user) { userModal.value = { open: true, user } }
  function closeUserModal() { userModal.value = { open: false, user: null } }
  function confirmDeleteUser(user) { if (confirm(`Delete "${user.username}"?`)) deleteUser(user) }
  function deleteUser(user) { const i = users.value.findIndex(u=>u.id===user.id); if(i!==-1) users.value.splice(i,1); alert(`User "${user.username}" deleted (demo).`) }
  function logout() { userStore.logout(); window.location.href='/login' }
  function showNotifications() { alert(`You have ${pendingCount.value} pending notifications.`) }
  </script>  