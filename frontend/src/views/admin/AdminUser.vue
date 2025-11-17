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
      <header class="sticky top-0 left-0 right-0 z-30 bg-white/90 backdrop-blur shadow-sm">
        <div class="flex items-center justify-between px-4 py-3 md:px-8">
          <div class="flex items-center gap-3">
            <button
              class="inline-flex items-center justify-center rounded-md p-2 text-slate-700 hover:bg-slate-100"
              @click="sidebarOpen = !sidebarOpen"
              aria-label="Toggle menu"
            >
              ☰
            </button>
            <div class="relative hidden md:block">
              <input
                type="text"
                placeholder="Search users..."
                v-model="search"
                @input="applyFilters"
                class="w-80 rounded-md border border-slate-200 pl-5 pr-3 py-2 text-sm font-subtitle placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/40"
              />
            </div>
          </div>

          <!-- User Info + Logout -->
          <div class="flex items-center gap-3">
            <div class="grid h-10 w-10 place-items-center rounded-full bg-blue-500 font-bold text-white">
              {{ getInitials(userStore.user?.username) }}
            </div>
            <div class="leading-tight">
              <div class="font-medium">{{ userStore.user?.username || 'Loading...' }}</div>
              <div class="text-[11px] text-slate-500">Administrator</div>
            </div>
            <button @click="logout" class="ml-3 flex items-center py-2 px-3 rounded-md hover:bg-gray-100">
              <span class="material-symbols-outlined">logout</span>
            </button>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <main class="px-4 py-6 md:px-8">
        <div>
          <h2 class="text-2xl font-bold font-subtitle">User Management</h2>
          <p class="text-sm text-slate-500 font-subtitle">View and Manage all registered users</p>
        </div>
        <!-- Filter Row -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
          <div class="relative w-full md:w-1/3">
          </div>
          <select
            v-model="filterRole"
            @change="applyFilters"
            class="px-4 py-2 rounded-lg border border-gray-300 bg-white"
          >
            <option value="">All Roles</option>
            <option value="member">Member</option>
            <option value="coach">Coach</option>
            <option value="normal">Normal</option>
          </select>
        </div>

        <!-- User Table -->
        <div class="bg-white rounded-xl shadow p-6 overflow-x-auto">
          <table class="w-full text-left">
            <thead class="border-b text-gray-500 uppercase text-sm">
              <tr>
                <th class="pb-3">User</th>
                <th class="pb-3">Email</th>
                <th class="pb-3">Role</th>
                <th class="pb-3">Joined</th>
                <th class="pb-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="u in filtered.filter(u => u.role)"
                :key="u.id"
                class="border-b hover:bg-gray-50 transition text-xs"
              >
                <td class="py-4 flex items-center gap-4">
                  <div class="w-10 h-10 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-semibold">
                    {{ getInitials(u.full_name || u.username) }}
                  </div>
                  <span class="font-medium text-gray-800">{{ u.full_name || u.username }}</span>
                </td>
                <td>{{ u.email }}</td>
                <td>
                  <span :class="roleClass(u.role)" class="px-3 py-1 rounded-full text-sm">
                    {{ u.role || "N/A" }}
                  </span>
                </td>
                <td>{{ formatDate(u.date_joined) }}</td>
                <td>
                  <button
                    @click="openDeleteModal(u)"
                    class="px-4 py-1 bg-red-500 text-white rounded-lg hover:bg-red-600 transition cursor-pointer"
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

const userStore = useUserStore()
const toast = useToastStore()

const sidebarOpen = ref(true)
const users = ref([])
const search = ref("")
const filterRole = ref("")
const filtered = ref([])

// Delete modal state
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
    const res = await fetch(`http://127.0.0.1:8000/api/moderation/admin/users/${userToDeleteId.value}/delete/`, {
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

function formatDate(date) { return new Date(date).toLocaleDateString() }
function getInitials(name) { if (!name) return "U"; const parts = name.split(" "); return parts.length>=2 ? parts[0][0]+parts[1][0] : parts[0][0] }
function roleClass(role) { if(role==='normal') return "bg-purple-100 text-purple-700"; if(role==='coach') return "bg-yellow-100 text-yellow-700"; return "bg-blue-100 text-blue-700" }

async function fetchUsers() {
  try {
    const res = await fetch("http://127.0.0.1:8000/api/moderation/admin/users/", { credentials: "include" })
    users.value = await res.json()
    filtered.value = users.value
  } catch (error) { toast.error("Error fetching users: " + error.message) }
}

function applyFilters() {
  let list = [...users.value]
  if (search.value) list = list.filter(u => u.username.toLowerCase().includes(search.value.toLowerCase()) || (u.full_name||"").toLowerCase().includes(search.value.toLowerCase()))
  if (filterRole.value) list = list.filter(u => u.role===filterRole.value)
  filtered.value = list
}

function logout() { userStore.logout?.(); window.location.href='/' }

onMounted(fetchUsers)
</script>
