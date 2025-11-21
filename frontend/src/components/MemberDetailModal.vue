<template>
  <transition name="modal">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm" @click.self="closeModal">
      <div class="bg-white rounded-2xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <!-- Header -->
        <div class="flex justify-between items-center px-6 py-4 border-b border-gray-200 sticky top-0 bg-white rounded-t-2xl">
          <h2 class="text-xl font-bold text-gray-900">Member Details</h2>
          <button @click="closeModal" class="p-2 hover:bg-gray-100 rounded-lg transition">
            <X class="w-5 h-5 text-gray-500" />
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="p-12 text-center">
          <div class="w-12 h-12 border-4 border-gray-200 border-t-blue-500 rounded-full animate-spin mx-auto mb-4"></div>
          <p class="text-gray-500">Loading member details...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="p-12 text-center">
          <p class="text-gray-700 font-semibold mb-2">Failed to load member details</p>
          <p class="text-gray-500 text-sm">{{ error }}</p>
        </div>

        <!-- Content -->
        <div v-else-if="memberDetails" class="p-6">
          <!-- Profile Section -->
          <div class="flex items-start gap-6 mb-6 p-6 bg-gradient-to-br from-purple-50 to-indigo-50 rounded-xl">
            <div
              class="w-15 h-15 rounded-full flex items-center justify-center font-bold text-3xl flex-shrink-0 overflow-hidden bg-gradient-to-br from-purple-500 to-indigo-500 text-white"
            >
              <template v-if="memberDetails.photo">
                <img
                  :src="getImageUrl(memberDetails.photo)"
                  alt="Avatar"
                  class="w-full h-full object-cover"
                />
              </template>
              <template v-else>
                {{ memberDetails.user?.first_name?.charAt(0) || memberDetails.user?.username?.charAt(0) || 'M' }}
              </template>
            </div>
            <div class="flex-1">
              <h3 class="text-2xl font-bold text-gray-900 mb-1">
                {{ memberDetails.user?.first_name || memberDetails.user?.username || 'Unknown' }}
                {{ memberDetails.user?.last_name || '' }}
              </h3>
              <div class="flex flex-wrap gap-2">
                <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-semibold">
                  ID: {{ memberId }}
                </span>
                <span class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-semibold">
                  {{ capitalizeFirst(memberDetails.experienceLevel || 'Member') }}
                </span>
              </div>
            </div>
          </div>

          <!-- Details Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <!-- Personal Information -->
            <div class="bg-gray-50 rounded-xl p-4">
              <h4 class="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                <User class="w-4 h-4" />
                Personal Information
              </h4>
              <div class="space-y-2">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Age:</span>
                  <span class="font-semibold text-gray-900">{{ memberDetails.age || 'Not specified' }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Gender:</span>
                  <span class="font-semibold text-gray-900">{{ formatGender(memberDetails.gender) }}</span>
                </div>
              </div>
            </div>

            <!-- Physical Information -->
            <div class="bg-gray-50 rounded-xl p-4">
              <h4 class="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                <Activity class="w-4 h-4" />
                Physical Information
              </h4>
              <div class="space-y-2">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Height:</span>
                  <span class="font-semibold text-gray-900">{{ memberDetails.height ? memberDetails.height + ' cm' : 'Not specified' }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Weight:</span>
                  <span class="font-semibold text-gray-900">{{ memberDetails.weight ? memberDetails.weight + ' kg' : 'Not specified' }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Member Message (if any) -->
          <div v-if="memberDetails.message" class="bg-blue-50 border border-blue-200 rounded-xl p-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
              <MessageCircle class="w-4 h-4" />
              Message
            </h4>
            <p class="text-gray-700 text-sm leading-relaxed">{{ memberDetails.message }}</p>
          </div>
        </div>

        <!-- Footer Actions -->
        <div class="px-6 py-4 border-t border-gray-200 bg-gray-50 rounded-b-2xl flex justify-end gap-3">
          <button @click="closeModal" class="px-4 py-2 border border-gray-300 rounded-lg font-semibold hover:bg-gray-100 transition">
            Close
          </button>
          <button @click="viewFoodDiary" class="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition">
            View Food Diary
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { X, User, Activity, Calendar, Dumbbell, MessageCircle } from 'lucide-vue-next'

const props = defineProps({
  show: Boolean,
  memberId: String
})

const emit = defineEmits(['close'])
const router = useRouter()

const loading = ref(false)
const error = ref(null)
const memberDetails = ref(null)

watch(() => props.show, (newVal) => {
  if (newVal && props.memberId) {
    loadMemberDetails()
  }
})

async function loadMemberDetails() {
  loading.value = true
  error.value = null
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/member/profile/${props.memberId}/`, {
      credentials: 'include'
    })

    if (!res.ok) {
      throw new Error('Failed to fetch member details')
    }

    const data = await res.json()
    memberDetails.value = data
  } catch (err) {
    console.error('Error loading member details:', err)
    error.value = err.message
  } finally {
    loading.value = false
  }
}

function closeModal() {
  emit('close')
}

function viewFoodDiary() {
  router.push(`/food-diary/${props.memberId}`)
  closeModal()
}

function formatGender(gender) {
  if (!gender) return 'Not specified'
  return gender.charAt(0).toUpperCase() + gender.slice(1)
}

function formatDate(dateStr) {
  if (!dateStr) return 'Not specified'
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
}

function getImageUrl(path) {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `http://127.0.0.1:8000${path}`
}

function capitalizeFirst(str) {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1)
}


</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .bg-white,
.modal-leave-active .bg-white {
  transition: transform 0.3s ease;
}

.modal-enter-from .bg-white,
.modal-leave-to .bg-white {
  transform: scale(0.95);
}
</style>
