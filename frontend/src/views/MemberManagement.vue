<template>
  <div class="max-w-[1200px] mx-auto p-6">
    <button class="border border-gray-300 rounded-lg px-4 py-2 font-semibold bg-blue-500 text-white hover:bg-blue-600 mb-6 transition-all" @click="goBackToDashboard">
      ← Back to Dashboard
    </button>

    <div class="flex justify-between items-start mb-6">
      <div>
        <h1 class="text-3xl font-bold font-subtitle">Member Management</h1>
        <p class="text-gray-600 font-body">
          View and manage members who have been accepted
        </p>
      </div>
      <div class="flex gap-3">
        <div class="flex flex-col items-center py-3 px-4 rounded-xl bg-green-100 border border-green-500">
          <span class="text-2xl font-bold">{{ members.length }}</span>
          <span class="text-xs uppercase text-gray-600">Active Members</span>
        </div>
      </div>
    </div>

    <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
      <div v-if="loading" class="text-center py-16 px-6">
        Loading members...
      </div>

      <div v-else-if="members.length === 0" class="text-center py-16 px-6">
        <div class="text-6xl mb-4">🙌</div>
        <div class="text-xl font-semibold text-gray-700 mb-3">No active members</div>
        <div class="text-gray-600">Start approving member requests to see them here.</div>
      </div>

      <div v-else class="grid gap-4">
        <div
          v-for="member in members"
          :key="member.memberId"
          class="border border-gray-200 rounded-xl p-5 bg-gray-50"
        >
          <div class="flex justify-between mb-4">
            <div class="flex gap-3 items-center">
              <div class="w-12 h-12 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 text-white flex items-center justify-center text-xl font-semibold">{{ member.name.charAt(0).toUpperCase() }}</div>
              <div>
                <div class="text-lg font-semibold">{{ member.name }}</div>
                <div class="text-xs text-blue-500 font-mono">ID: {{ member.memberId }}</div>
              </div>
            </div>
            <div class="px-3 py-1.5 rounded-full bg-green-100 text-green-800 text-xs font-semibold self-start">ACTIVE</div>
          </div>

          <div class="grid gap-2 mb-4 p-3 bg-white rounded-lg">
            <div class="flex justify-between"><span class="text-gray-600">Program:</span><span class="font-semibold">{{ member.programName || 'Not specified'}}</span></div>
            <div class="flex justify-between"><span class="text-gray-600">Level:</span><span class="font-semibold">{{ member.experienceLevel || 'Not specified' }}</span></div>
            <div class="flex justify-between"><span class="text-gray-600">Joined:</span><span class="font-semibold">{{ formatDate(member.joinedAt) }}</span></div>
          </div>

          <div class="flex gap-2 flex-wrap pt-4 border-t border-gray-200">
            <button class="border border-gray-300 rounded-lg px-3 py-1.5 text-xs font-semibold hover:bg-gray-50 transition-all" @click="viewFoodDiary(member)">View Food Diary</button>
            <button class="bg-red-500 text-white border-red-500 rounded-lg px-3 py-1.5 text-xs font-semibold hover:bg-red-600 transition-all" @click="removeMember(member)">Remove</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const members = ref([])
const loading = ref(true)

function goBackToDashboard() {
  router.push('/coach-dashboard')
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

async function loadMembers() {
  loading.value = true
  try {
    const res = await fetch('http://127.0.0.1:8000/api/member/accepted/', {
      credentials: 'include'
    })
    if (!res.ok) throw new Error('Failed to fetch members')
    const data = await res.json()
    members.value = data
  } catch (err) {
    console.error(err)
    members.value = []
  } finally {
    loading.value = false
  }
}

function viewFoodDiary(member) {
  router.push(`/food-diary/${member.memberId}`)
}

async function removeMember(member) {
  if (!confirm(`Remove ${member.name} from your members?`)) return
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/member/${member.memberId}/`, {
      method: 'DELETE',
      credentials: 'include'
    })
    if (!res.ok) throw new Error('Failed to remove')
    members.value = members.value.filter(m => m.memberId !== member.memberId)
  } catch (err) {
    console.error(err)
    alert('Failed to remove member')
  }
}

onMounted(() => {
  loadMembers()
})
</script>
