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
      :activeSection="'users'"
      @close="sidebarOpen = false"
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
              <!-- use `search` (declared in script) -->
              <input
                type="text"
                placeholder="Search users..."
                v-model="search"
                class="w-80 rounded-md border border-slate-200 pl-5 pr-3 py-2 text-sm font-subtitle placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/40"
              />
            </div>
          </div>

          <div class="flex items-center gap-3">
            <AdminNotificationBell
              :coaches="coaches"
              @review="viewCoachDetails"
            />

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
        <div>
          <h2 class="text-2xl font-bold font-subtitle">User Management</h2>
          <p class="text-sm text-slate-500 font-subtitle">View and manage all registered users</p>
        </div>

        <!-- User Table -->
        <div class="bg-white rounded-xl shadow p-6 overflow-x-auto mt-4">
          <!-- Header -->
          <div class="flex items-center justify-between font-subtitle">
            <h3 class="text-base font-semibold">
              All Users ({{ filtered.filter(u => u.role).length }})
            </h3>

            <select
              class="rounded-md border border-slate-200 px-3 py-2 text-sm"
              v-model="filterRole"
              @change="applyFilters"
            >
              <option value="">All Roles</option>
              <option value="member">Member</option>
              <option value="coach">Coach</option>
              <option value="normal">Normal</option>
            </select>
          </div>

          <!-- Table -->
          <table class="w-full border-collapse text-sm">
            <thead class="text-slate-500">
              <tr class="border-b border-slate-200">
                <th class="px-3 py-2 text-left font-subtitle">User</th>
                <th class="px-3 py-2 text-left font-subtitle">Email</th>
                <th class="px-3 py-2 text-left font-subtitle">Role</th>
                <th class="px-3 py-2 text-left font-subtitle">Joined</th>
                <th class="px-3 py-2 text-left font-subtitle">Actions</th>
              </tr>
            </thead>

            <tbody>
              <tr v-if="filtered.filter(u => u.role).length === 0">
                <td colspan="5" class="px-3 py-8 text-center text-slate-500 font-semibold">
                  No users found
                </td>
              </tr>

              <tr
                v-for="u in filtered.filter(u => u.role)"
                :key="u.id"
                class="border-b border-slate-100 hover:bg-slate-50"
              >
                <td class="px-3 py-3 font-semibold text-slate-800">
                  <div class="flex items-center gap-2">
                    <div class="h-8 w-8 rounded-full overflow-hidden bg-blue-500">
                      <template v-if="u.photo">
                        <img :src="u.photo" class="h-full w-full object-cover" />
                      </template>
                      <template v-else>
                        <div class="grid h-full w-full place-items-center font-semibold text-white">
                          {{ getInitials(u.full_name || u.username) }}
                        </div>
                      </template>
                    </div>
                    {{ u.full_name || u.username }}
                  </div>
                </td>

                <td class="px-3 py-2 font-semibold">{{ u.email }}</td>

                <td class="px-3 py-2">
                  <span :class="roleClass(u.role)" class="rounded-full px-2 py-0.5 text-[11px] font-semibold capitalize">
                    {{ u.role.charAt(0).toUpperCase() + u.role.slice(1) }}
                  </span>
                </td>

                <td class="px-3 py-2 font-semibold">{{ formatDate(u.date_joined) }}</td>

                <td class="px-3 py-2 font-semibold">
                  <button 
                    class="rounded-md bg-red-500 px-3 py-1.5 text-white font-semibold hover:bg-red-600"
                    @click="openDeleteModal(u)"
                    >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Delete Modal -->
        <DeleteModal
          v-model:show="showDeleteModal"
          message="Are you sure you want to delete"
          :item-name="userToDeleteName"
          cancel-text="Cancel"
          confirm-text="Yes, Delete"
          @confirm="confirmDelete"
          @close="closeDeleteModal"
        />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import DeleteModal from '@/components/DeleteModal.vue'
import AdminSideBar from '@/components/AdminSideBar.vue'
import { Menu } from 'lucide-vue-next'
import AdminNotificationBell from '@/components/AdminNotificationBell.vue'

const userStore = useUserStore()
const toast = useToastStore()

const sidebarOpen = ref(true)
const users = ref([])
const search = ref('')
const filterRole = ref('')
const filtered = ref([])

const showDeleteModal = ref(false)
const userToDeleteId = ref(null)
const userToDeleteName = ref('')

// Functions
function openDeleteModal(user) {
  showDeleteModal.value = true
  userToDeleteId.value = user.id
  userToDeleteName.value = user.full_name || user.username
}

function closeDeleteModal() {
  showDeleteModal.value = false
  userToDeleteId.value = null
  userToDeleteName.value = ''
}

async function confirmDelete() {
  if (!userToDeleteId.value) return
  toast.info("Deleting user...")
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/moderation/users/${userToDeleteId.value}/delete/`, {
      method: "DELETE",
      credentials: "include"
    })
    if (res.ok) {
      toast.success("User deleted successfully")
      closeDeleteModal()
      await fetchUsers()
    } else toast.error("Failed to delete user")
  } catch (e) { toast.error("Error: " + e.message) }
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function getInitials(name) { return name?.split(' ').map(w => w[0]).join('').toUpperCase().slice(0,2) || '?' }
function roleClass(role) { if(role==='normal') return "bg-purple-100 text-purple-700"; if(role==='coach') return "bg-yellow-100 text-yellow-700"; return "bg-blue-100 text-blue-700" }

async function fetchUsers() {
  try {
    const res = await fetch("http://127.0.0.1:8000/api/moderation/users/", { credentials: "include" })
    users.value = await res.json()
    filtered.value = users.value
  } catch (error) { toast.error("Error fetching users: " + error.message) }
}

function applyFilters() {
  let list = [...users.value]
  if (search.value) list = list.filter(u => (u.username || '').toLowerCase().includes(search.value.toLowerCase()) || (u.full_name||"").toLowerCase().includes(search.value.toLowerCase()))
  if (filterRole.value) list = list.filter(u => u.role === filterRole.value)
  filtered.value = list
}

function logout() { userStore.logout?.(); window.location.href='/' }

onMounted(fetchUsers)
</script>
