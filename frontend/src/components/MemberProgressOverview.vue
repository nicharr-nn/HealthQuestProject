<template>
  <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-semibold text-gray-900">Members Progress Overview</h2>
      <button
        @click="loadProgress"
        class="px-3 py-2 text-xs rounded-md border border-gray-300 font-semibold hover:bg-gray-50 transition"
        :disabled="loading"
      >
        <span v-if="loading">Loading...</span>
        <span v-else>Refresh</span>
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading && membersProgress.length === 0" class="text-center py-12">
      <div class="w-8 h-8 border-4 border-gray-200 border-t-blue-500 rounded-full animate-spin mx-auto mb-3"></div>
      <p class="text-gray-500">Loading member progress...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="!loading && membersProgress.length === 0" class="text-center py-12">
      <div class="text-6xl mb-4">📊</div>
      <div class="text-xl font-semibold text-gray-700 mb-3">No member data yet</div>
      <div class="text-gray-500">Assign programs to your members to track their progress.</div>
    </div>

    <!-- Progress List -->
    <div v-else class="space-y-4">
      <div
        v-for="member in membersProgress"
        :key="member.member_id"
        class="border border-gray-200 rounded-xl p-4 bg-gray-50 hover:border-blue-600 hover:shadow-md transition"
      >
        <!-- Member Info -->
        <div class="flex justify-between items-start mb-3">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-indigo-500 text-white flex items-center justify-center font-semibold text-sm flex-shrink-0">
              {{ member.name.charAt(0).toUpperCase() }}
            </div>
            <div>
              <div class="text-base font-semibold text-gray-900">{{ member.name }}</div>
              <div class="text-xs text-gray-500">{{ member.experience_level }}</div>
            </div>
          </div>
          <div
            class="px-3 py-1 rounded-full text-xs font-bold"
            :class="{
              'bg-green-100 text-green-700': member.completion_rate >= 75,
              'bg-yellow-100 text-yellow-700': member.completion_rate >= 50 && member.completion_rate < 75,
              'bg-orange-100 text-orange-700': member.completion_rate >= 25 && member.completion_rate < 50,
              'bg-red-100 text-red-700': member.completion_rate < 25
            }"
          >
            {{ member.completion_rate }}%
          </div>
        </div>

        <!-- Program Info -->
        <div class="mb-3">
          <div class="text-sm text-gray-600 mb-1">
            <span class="font-medium">Program:</span> {{ member.program_name || 'Not assigned' }}
          </div>
          <div class="text-sm text-gray-600">
            <span class="font-medium">Progress:</span> {{ member.completed_days }} / {{ member.total_days }} days completed
          </div>
        </div>

        <!-- Progress Bar -->
        <div class="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
          <div
            class="h-2.5 rounded-full transition-all duration-500"
            :class="{
              'bg-green-500': member.completion_rate >= 75,
              'bg-yellow-500': member.completion_rate >= 50 && member.completion_rate < 75,
              'bg-orange-500': member.completion_rate >= 25 && member.completion_rate < 50,
              'bg-red-500': member.completion_rate < 25
            }"
            :style="{ width: member.completion_rate + '%' }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Summary Stats -->
    <div v-if="membersProgress.length > 0" class="mt-6 pt-6 border-t border-gray-200">
      <div class="grid grid-cols-3 gap-4 text-center">
        <div>
          <div class="text-2xl font-bold text-blue-600">{{ averageCompletion }}%</div>
          <div class="text-xs text-gray-500">Average Completion</div>
        </div>
        <div>
          <div class="text-2xl font-bold text-green-600">{{ membersOnTrack }}</div>
          <div class="text-xs text-gray-500">On Track (≥75%)</div>
        </div>
        <div>
          <div class="text-2xl font-bold text-orange-600">{{ membersNeedingAttention }}</div>
          <div class="text-xs text-gray-500">Need Attention (<50%)</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const loading = ref(false)
const membersProgress = ref([])

const averageCompletion = computed(() => {
  if (membersProgress.value.length === 0) return 0
  const total = membersProgress.value.reduce((sum, m) => sum + m.completion_rate, 0)
  return Math.round(total / membersProgress.value.length)
})

const membersOnTrack = computed(() => {
  return membersProgress.value.filter(m => m.completion_rate >= 75).length
})

const membersNeedingAttention = computed(() => {
  return membersProgress.value.filter(m => m.completion_rate < 50 && m.total_days > 0).length
})

async function loadProgress() {
  loading.value = true
  try {
    const res = await fetch('http://127.0.0.1:8000/api/member/progress-overview/', {
      credentials: 'include'
    })
    if (!res.ok) throw new Error('Failed to fetch progress')
    const data = await res.json()
    membersProgress.value = data.members || []
  } catch (err) {
    console.error('Failed to load member progress', err)
    membersProgress.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadProgress()
})
</script>
