<template>
  <div class="p-6">
    <!-- Page Title -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">User Management</h1>
      <p class="text-gray-500">View and manage all registered users</p>
    </div>

    <!-- Search + Filter Row -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
      
      <!-- Search -->
      <div class="relative w-full md:w-1/3">
        <input 
          v-model="search"
          @input="applyFilters"
          type="text" 
          placeholder="Search users..." 
          class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring focus:ring-blue-200"
        />
      </div>

      <!-- Filter -->
      <select
        v-model="filterRole"
        @change="applyFilters"
        class="px-4 py-2 rounded-lg border border-gray-300 bg-white"
      >
        <option value="">All Roles</option>
        <option value="member">Member</option>
        <option value="coach">Coach</option>
        <option value="admin">Admin</option>
      </select>
    </div>

    <!-- User List Card -->
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
            v-for="u in filtered"
            :key="u.id"
            class="border-b hover:bg-gray-50 transition"
          >
            <!-- User + Icon -->
            <td class="py-4 flex items-center gap-4">
              <div 
                class="w-10 h-10 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-semibold"
              >
                {{ getInitials(u.full_name || u.username) }}
              </div>
              <span class="font-medium text-gray-800">
                {{ u.full_name || u.username }}
              </span>
            </td>

            <!-- Email -->
            <td>{{ u.email }}</td>

            <!-- Role -->
            <td>
              <span 
                :class="roleClass(u.role)"
                class="px-3 py-1 rounded-full text-sm"
              >
                {{ u.role || "N/A" }}
              </span>
            </td>

            <!-- Date joined -->
            <td>{{ formatDate(u.date_joined) }}</td>

            <!-- Actions -->
            <td>
              <button
                @click="deleteUser(u.id)"
                class="px-4 py-1 bg-red-500 text-white rounded-lg hover:bg-red-600 transition"
              >
                Delete
              </button>
            </td>

          </tr>
        </tbody>
      </table>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted} from 'vue'

const users = ref([])
const search = ref("")
const filterRole = ref("")
const filtered = ref([])

function formatDate(date) {
  return new Date(date).toLocaleDateString()
}

function getInitials(name) {
  if (!name) return "U"
  const parts = name.split(" ")
  if (parts.length >= 2) return parts[0][0] + parts[1][0]
  return parts[0][0]
}

function roleClass(role) {
  if (role === "admin") return "bg-purple-100 text-purple-700"
  if (role === "coach") return "bg-yellow-100 text-yellow-700"
  return "bg-blue-100 text-blue-700"
}

async function fetchUsers() {
  const res = await fetch("http://127.0.0.1:8000/api/moderation/admin/users/", {
    credentials: "include"
  })
  users.value = await res.json()
  filtered.value = users.value
}

function applyFilters() {
  let list = [...users.value]

  if (search.value.length > 0) {
    list = list.filter(u =>
      u.username.toLowerCase().includes(search.value.toLowerCase()) ||
      (u.full_name || "").toLowerCase().includes(search.value.toLowerCase())
    )
  }

  if (filterRole.value) {
    list = list.filter(u => u.role === filterRole.value)
  }

  filtered.value = list
}

async function deleteUser(id) {
  if (!confirm("Are you sure you want to delete this user?")) return

  await fetch(`http://127.0.0.1:8000/api/moderation/admin/users/${id}/delete/`, {
    method: "DELETE",
    credentials: "include"
  })

  fetchUsers() // reload list
}

onMounted(fetchUsers)
</script>
