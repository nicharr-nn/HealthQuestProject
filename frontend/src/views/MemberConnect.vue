<template>
  <div class="min-h-scree my-8">
    <div class="max-w-4xl mx-auto">
      <div class="bg-white rounded-2xl shadow-xl p-8">
        <!-- Header -->
        <div class="mb-8 text-center">
          <h1 class="text-3xl font-bold text-gray-800">Coach Management</h1>
          <p class="text-gray-500 text-sm mt-1">
            Connect with your coach or view your request status
          </p>
        </div>

        <!-- Connected Coach -->
        <div v-if="coachStatus === 'accepted'" class="mb-8">
          <h2 class="text-xl font-semibold text-gray-700 mb-4">Your Coach</h2>

          <div class="bg-gradient-to-r from-indigo-50 to-purple-50 border-2 border-indigo-200 rounded-xl p-6">
            <div class="grid md:grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-gray-600 mb-1">Coach Name</p>
                <p class="text-lg font-semibold text-gray-800">{{ currentCoach.name }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-600 mb-1">Email</p>
                <p class="text-lg font-semibold text-gray-800">{{ currentCoach.email }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-600 mb-1">Specialization</p>
                <p class="text-lg font-semibold text-gray-800">{{ currentCoach.specialization }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-600 mb-1">Member Since</p>
                <p class="text-lg font-semibold text-gray-800">{{ formatDate(currentCoach.joinedDate) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Pending Coach Request -->
        <div v-else-if="coachStatus === 'pending'" class="text-center mb-8">
          <h2 class="text-xl font-semibold text-gray-700 mb-3">Coach Request Pending</h2>
          <p class="text-gray-600 text-sm mb-4">
            Your request to connect with <strong>{{ pendingCoach.name }}</strong> is waiting for their approval.
          </p>
          <div class="bg-yellow-50 border border-yellow-300 text-yellow-800 p-4 rounded-lg inline-block">
            ⏳ Pending Acceptance
          </div>
        </div>

        <!-- No Coach Yet - Send Request -->
        <div v-else>
          <h2 class="text-xl font-semibold text-gray-700 mb-4">Add New Coach Code</h2>

          <div class="space-y-4">
            <div>
              <label for="coachCode" class="block text-sm font-medium text-gray-700 mb-2">
                Enter Coach Code
              </label>
              <input
                id="coachCode"
                v-model="coachCode"
                @keyup.enter="!loading && sendRequest()"
                type="text"
                placeholder="e.g., COACH123456"
                class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                :disabled="loading"
              />
              <p class="text-sm text-gray-500 mt-2">
                Enter the unique code provided by your coach to send a request
              </p>
            </div>

            <!-- Message Display -->
            <div
              v-if="message.text"
              :class="[
                'p-4 rounded-lg text-sm font-medium',
                message.type === 'error'
                  ? 'bg-red-50 text-red-700 border border-red-200'
                  : 'bg-green-50 text-green-700 border border-green-200'
              ]"
            >
              {{ message.text }}
            </div>

            <button
              @click="sendRequest"
              :disabled="loading"
              :class="[
                'w-full py-3 px-6 rounded-lg font-semibold text-white transition-all',
                loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700 hover:shadow-lg'
              ]"
            >
              <span v-if="loading" class="flex items-center justify-center gap-2">
                <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                Sending Request...
              </span>
              <span v-else>Send Request</span>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="coachStatus === 'accepted'">

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const coachStatus = ref('') // 'pending' | 'accepted' | ''
const coachCode = ref('')
const loading = ref(false)
const message = ref({ type: '', text: '' })
const currentCoach = ref(null)
const pendingCoach = ref(null)

onMounted(() => {
  // 🧠 Mock: You can switch between these three lines to test different states:
//   coachStatus.value = '' // No coach yet
//   coachStatus.value = 'pending' // Pending request
//   pendingCoach.value = {
//     name: 'Coach Olivia Chen',
//     email: 'olivia.chen@example.com'
//   }
//   coachStatus.value = 'accepted' // Already connected
//   currentCoach.value = {
//     name: 'Coach Emily Carter',
//     email: 'emily.carter@example.com',
//     specialization: 'Yoga & Mindfulness',
//     joinedDate: '2024-05-10'
//   }
 })

// 📝 Send request (mock)
function sendRequest() {
  if (!coachCode.value.trim()) {
    message.value = { type: 'error', text: 'Please enter a coach code.' }
    return
  }

  loading.value = true
  message.value = { type: '', text: '' }

  setTimeout(() => {
    // Simulate valid code
    pendingCoach.value = {
      name: 'Coach Olivia Chen',
      email: 'olivia.chen@example.com'
    }
    coachStatus.value = 'pending'
    message.value = { type: 'success', text: 'Request sent! Waiting for coach approval.' }
    coachCode.value = ''
    loading.value = false
  }, 1500)
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>
