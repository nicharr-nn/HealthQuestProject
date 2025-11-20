<template>
  <div class="min-h-screen my-8">
    <div class="max-w-4xl mx-auto font-body">
      <div class="bg-white rounded-2xl shadow-xl p-8">
        <!-- Header -->
        <div class="mb-8 text-center font-subtitle text-[#846757]">
          <h1 class="text-3xl font-bold">Coach Management</h1>
          <p class=" text-sm mt-1">
            Connect with your coach or view your request status
          </p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-8">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-300 mx-auto"></div>
          <p class="text-gray-600 mt-4">Loading your coach information...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 text-center mb-8">
          <div class="text-red-600 text-lg font-semibold mb-2">Error</div>
          <p class="text-red-700">{{ error }}</p>
          <button 
            @click="loadMemberData"
            class="mt-4 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg"
          >
            Try Again
          </button>
        </div>

        <!-- Connected Coach -->
        <div v-else-if="coachStatus === 'accepted' || coachStatus === 'approved'" class="mb-8">
          <h2 class="text-xl font-semibold text-[#846757] mb-4">Your Coach</h2>

          <div class="bg-[#ffc3d3] rounded-xl p-6">
            <div class="grid md:grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-gray-800 mb-1">Coach Name</p>
                <p class="text-lg font-semibold text-gray-800">{{ currentCoach.name }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-800 mb-1">Coach ID</p>
                <p class="text-lg font-semibold text-gray-800">{{ currentCoach.coach_id }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-800 mb-1">Joined Date</p>
                <p class="text-lg font-semibold text-gray-800">{{ formatDate(currentCoach.joined_date) }}</p>
              </div>
            </div>
            
            <!-- Program Information -->
            <div v-if="memberProfile?.program_name" class="mt-4 pt-4 border-t border-[#ff9ba6]">
              <p class="text-sm text-gray-600 mb-1">Your Assigned Program</p>
              <p class="text-lg font-bold text-gray-800">{{ memberProfile.program_name }}</p>
            </div>
          </div>

          <!-- Cancel Request Button -->
          <div class="mt-4 text-center">
            <button
              @click="cancelCoachRequest"
              class="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg font-semibold transition-colors cursor-pointer"
            >
              Cancel Coach Connection
            </button>
          </div>
        </div>

        <!-- Pending Coach Request -->
        <div v-else-if="coachStatus === 'pending'" class="text-center mb-8">
          <p class="text-gray-600 text-l mb-4">
            Your request to connect with <strong>{{ pendingCoach.name }}</strong> is waiting for their approval.
          </p>
          <div class="bg-yellow-50 border border-yellow-300 text-yellow-800 p-4 rounded-lg inline-block mb-4">
            ⏳ Pending Acceptance
          </div>

          <!-- Cancel Request Button -->
          <div class="mt-4">
            <button
              @click="cancelCoachRequest"
              class="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg font-semibold transition-colors cursor-pointer"
            >
              Cancel Request
            </button>
          </div>
        </div>

        <!-- No Coach Yet - Send Request -->
        <div v-else>
          <h2 class="text-xl font-semibold text-gray-700 mb-4 font-subtitle">Connect with a Coach</h2>

          <!-- Member Profile Setup -->
          <div v-if="!memberProfile" class="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
            <h3 class="text-lg font-semibold text-blue-800 mb-2">Setup Required</h3>
            <p class="text-blue-700 mb-4">You need to create your member profile before connecting with a coach.</p>
            <button
              @click="setupMemberProfile"
              class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-semibold"
            >
              Setup Member Profile
            </button>
          </div>

          <!-- Coach Connection Section -->
          <div v-else>
            <!-- Coach Connection Form -->
            <div class="space-y-6">
              <div>
                <label for="coachCode" class="block text-sm font-medium text-gray-700 mb-2">
                  Coach ID
                </label>
                <div class="flex gap-2">
                  <input
                    id="coachCode"
                    v-model="coachCode"
                    type="text"
                    placeholder="e.g., C-XXXXX"
                    class="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-300 outline-none transition-all"
                    :disabled="requestLoading"
                  />
                </div>
                <p class="text-sm text-gray-500 mt-2">
                  Enter the Coach ID (starts with C-) or select from available coaches above
                </p>
              </div>

              <!-- Experience Level -->
              <div>
                <label for="experienceLevel" class="block text-sm font-medium text-gray-700 mb-2">
                  Your Experience Level
                </label>
                <select
                  id="experienceLevel"
                  v-model="experienceLevel"
                  class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-300 outline-none transition-all"
                  :disabled="requestLoading"
                >
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                </select>
              </div>

              <!-- Message to Coach -->
              <div>
                <label for="message" class="block text-sm font-medium text-gray-700 mb-2">
                  Message to Coach (Optional)
                </label>
                <textarea
                  id="message"
                  v-model="message"
                  rows="3"
                  placeholder="Tell the coach about your fitness goals and expectations..."
                  class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-300 outline-none transition-all"
                  :disabled="requestLoading"
                ></textarea>
              </div>

              <!-- Message Display -->
              <div
                v-if="messageDisplay.text"
                :class="[
                  'p-4 rounded-lg text-sm font-medium',
                  messageDisplay.type === 'error'
                    ? 'bg-red-50 text-red-700 border border-red-200'
                    : 'bg-green-50 text-green-700 border border-green-200'
                ]"
              >
                {{ messageDisplay.text }}
              </div>

              <button
                @click="sendRequest"
                :disabled="requestLoading || !coachCode.trim()"
                :class="[
                  'w-full py-3 px-6 rounded-lg font-semibold text-white transition-all cursor-pointer',
                  requestLoading || !coachCode.trim() 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : 'bg-blue-400 hover:bg-blue-500 hover:shadow-lg'
                ]"
              >
                <span v-if="requestLoading" class="flex items-center justify-center gap-2">
                  <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  Sending Request...
                </span>
                <span v-else>Send Connection Request</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// Reactive data
const coachStatus = ref('') // 'pending' | 'accepted' | 'rejected' | ''
const coachCode = ref('')
const experienceLevel = ref('beginner')
const message = ref('')
const loading = ref(false)
const requestLoading = ref(false)
const messageDisplay = ref({ type: '', text: '' })
const currentCoach = ref(null)
const pendingCoach = ref(null)
const memberProfile = ref(null)
const error = ref('')

// API base URL
const API_BASE = 'http://127.0.0.1:8000/api/member/'

onMounted(() => {
  loadMemberData()
})

async function loadMemberData() {
  loading.value = true
  error.value = ''
  
  try {
    // Load member profile
    const profileResponse = await fetch(`${API_BASE}member-profile/`, {
      credentials: 'include',
    })

    if (profileResponse.ok) {
      memberProfile.value = await profileResponse.json()
    } else if (profileResponse.status === 404) {
      memberProfile.value = null
    } else {
      throw new Error('Failed to load member profile')
    }

    // Load coach relationship
    const relationshipResponse = await fetch(`${API_BASE}member-request/`, {
      credentials: 'include',
    })

    if (relationshipResponse.ok) {
      const relationshipData = await relationshipResponse.json()      
      if (relationshipData.message === 'No coach request found.') {
        coachStatus.value = ''
      } else {
        coachStatus.value = relationshipData.status
        if (relationshipData.status === 'approved' || relationshipData.status === 'accepted') {
          currentCoach.value = {
            name: relationshipData.coach?.name || 'Coach',
            coach_id: relationshipData.coach?.public_id || relationshipData.coach?.coach_id,
            joined_date: relationshipData.submittedAt || '',
          }
        } else if (relationshipData.status === 'pending') {
          pendingCoach.value = {
            name: relationshipData.coach?.name || 'Coach',
            coach_id: relationshipData.coach?.public_id || relationshipData.coach?.coach_id
          }
        }
      }
    } else if (relationshipResponse.status === 404) {
      coachStatus.value = ''
    } else {
      throw new Error('Failed to load coach relationship')
    }

  } catch (err) {
    console.error('Error loading member data:', err)
    error.value = 'Failed to load your data. Please try again.'
  } finally {
    loading.value = false
  }
}

async function setupMemberProfile() {
  requestLoading.value = true
  messageDisplay.value = { type: '', text: '' }

  try {
    const response = await fetch(`${API_BASE}member-apply/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({
        experience_level: experienceLevel.value,
        message: message.value
      })
    })

    if (response.ok) {
      memberProfile.value = await response.json()
      messageDisplay.value = { 
        type: 'success', 
        text: 'Member profile created successfully! You can now connect with a coach.' 
      }

    } else {
      const errorData = await response.json()
      throw new Error(errorData.error || 'Failed to create member profile')
    }
  } catch (err) {
    console.error('Error creating member profile:', err)
    messageDisplay.value = { type: 'error', text: err.message }
  } finally {
    requestLoading.value = false
  }
}

async function sendRequest() {
  if (!coachCode.value.trim()) {
    messageDisplay.value = { type: 'error', text: 'Please enter a Coach ID.' }
    return
  }

  requestLoading.value = true
  messageDisplay.value = { type: '', text: '' }

  try {
    const response = await fetch(`${API_BASE}member-apply/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({
        coach_code: coachCode.value.trim(),
        experience_level: experienceLevel.value,
        message: message.value
      })
    })

    if (response.ok) {
      const data = await response.json()
      memberProfile.value = data.member || data
      messageDisplay.value = { 
        type: 'success', 
        text: data.message || 'Request sent successfully! Waiting for coach approval.' 
      }
      
      // Reload to get updated relationship status
      await loadMemberData()
      
      // Reset form
      coachCode.value = ''
      message.value = ''
      
    } else if (response.status === 404) {
      const errorData = await response.json()
      messageDisplay.value = { 
        type: 'error', 
        text: errorData.error || 'Coach not found.' 
      }
      
    } else if (response.status === 400) {
      const errorData = await response.json()
      messageDisplay.value = { 
        type: 'error', 
        text: errorData.error || 'Cannot send request.' 
      }
    } else {
      const errorData = await response.json()
      throw new Error(errorData.error || 'Failed to send request')
    }
  } catch (err) {
    console.error('Error sending coach request:', err)
    messageDisplay.value = { type: 'error', text: err.message }
  } finally {
    requestLoading.value = false
  }
}

async function cancelCoachRequest() {
  if (!confirm('Are you sure you want to cancel this coach connection?')) {
    return
  }

  requestLoading.value = true

  try {
    const response = await fetch(`${API_BASE}member-request/`, {
      method: 'DELETE',
      credentials: 'include',
    })

    if (response.ok) {
      messageDisplay.value = { 
        type: 'success', 
        text: 'Coach connection cancelled successfully.' 
      }
      await loadMemberData()
    } else {
      throw new Error('Failed to cancel coach connection')
    }
  } catch (err) {
    console.error('Error cancelling coach request:', err)
    messageDisplay.value = { type: 'error', text: err.message }
  } finally {
    requestLoading.value = false
  }
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
</style>