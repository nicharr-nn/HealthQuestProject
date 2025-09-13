<template>
  <div class="min-h-screen py-10">
    <div v-if="loading" class="text-gray-500 text-center">Loading profile...</div>
    <div v-else-if="error" class="text-red-500 text-center">{{ error }}</div>
    <div v-else>
      <h1 class="font-subtitle text-5xl md:text-6xl text-center tracking-wide text-[#846757]">
        MY PROFILE
      </h1>
      <!-- Main Content -->
      <div class="px-6 py-10">
        <div class="max-w-3xl mx-auto">
          <div class="bg-white rounded-3xl shadow-2xl overflow-hidden">
            <div class="p-12">
              <div class="flex gap-12">
                <!-- Profile Picture -->
                <div class="flex-shrink-0">
                  <div class="relative">
                    <div class="w-64 h-64 rounded-full bg-gray-200 overflow-hidden shadow-lg"></div>
                    <button
                      class="absolute bottom-2 right-4 bg-white p-3 rounded-full hover:shadow-xl transition-shadow"
                    >
                      <span class="material-symbols-outlined text-gray-600 text-xl">
                        image_arrow_up
                      </span>
                    </button>
                  </div>
                </div>

                <!-- Profile Info -->
                <div class="flex-1">
                  <div class="space-y-5">
                    <!-- Name -->
                    <div class="flex justify-between items-center border-b border-gray-200 pb-4">
                      <label class="text-gray-600 font-medium text-lg w-32">Name</label>
                      <template v-if="isEditing">
                        <input
                          v-model="editProfile.name"
                          type="text"
                          class="flex-1 text-teal-600 text-lg font-medium bg-transparent border-none outline-none focus:bg-gray-50 px-2 py-1 rounded"
                        />
                      </template>
                      <template v-else>
                        <span class="flex-1 text-teal-600 text-lg font-medium text-right">{{
                          profile.name
                        }}</span>
                      </template>
                    </div>

                    <!-- Email -->
                    <div class="flex justify-between items-center border-b border-gray-200 pb-4">
                      <label class="text-gray-600 font-medium text-lg w-32">Email</label>
                      <template v-if="isEditing">
                        <input
                          v-model="editProfile.email"
                          type="email"
                          class="flex-1 text-teal-600 text-lg font-medium bg-transparent border-none outline-none focus:bg-gray-50 px-2 py-1 rounded"
                        />
                      </template>
                      <template v-else>
                        <span class="flex-1 text-teal-600 text-lg font-medium text-right">{{
                          profile.email
                        }}</span>
                      </template>
                    </div>

                    <!-- Height -->
                    <div class="flex justify-between items-center border-b border-gray-200 pb-4">
                      <label class="text-gray-600 font-medium text-lg w-32">Height</label>
                      <div class="flex-1 flex justify-end items-center">
                        <template v-if="isEditing">
                          <input
                            v-model="editProfile.height"
                            type="text"
                            class="text-teal-600 text-lg font-medium bg-transparent border-none outline-none focus:bg-gray-50 px-2 py-1 rounded w-32 text-right"
                          />
                        </template>
                        <template v-else>
                          <span class="text-teal-600 text-lg font-medium">{{
                            profile.height
                          }}</span>
                        </template>
                        <span class="text-gray-600 text-lg ml-2">cm</span>
                      </div>
                    </div>

                    <!-- Weight -->
                    <div class="flex justify-between items-center border-b border-gray-200 pb-4">
                      <label class="text-gray-600 font-medium text-lg w-32">Weight</label>
                      <div class="flex-1 flex justify-end items-center">
                        <template v-if="isEditing">
                          <input
                            v-model="editProfile.weight"
                            type="text"
                            class="text-teal-600 text-lg font-medium bg-transparent border-none outline-none focus:bg-gray-50 px-2 py-1 rounded w-32 text-right"
                          />
                        </template>
                        <template v-else>
                          <span class="text-teal-600 text-lg font-medium">{{
                            profile.weight
                          }}</span>
                        </template>
                        <span class="text-gray-600 text-lg ml-2">Kg</span>
                      </div>
                    </div>

                    <!-- Goal -->
                    <div class="flex justify-between items-center border-b border-gray-200 pb-4">
                      <label class="text-gray-600 font-medium text-lg w-32">Goal</label>
                      <template v-if="isEditing">
                        <select
                          v-model="editProfile.goal"
                          class="flex-1 text-teal-600 text-lg font-medium bg-transparent border-none outline-none focus:bg-gray-50 px-2 py-1 rounded"
                        >
                          <option value="">Select a goal</option>
                          <option value="WEIGHT_LOSS">Weight Loss</option>
                          <option value="MUSCLE_GAIN">Muscle Gain</option>
                          <option value="MAINTENANCE">Maintenance</option>
                        </select>
                      </template>
                      <template v-else>
                        <span class="flex-1 text-teal-600 text-lg font-medium text-right">{{
                          profile.goal
                        }}</span>
                      </template>
                    </div>

                    <!-- Location -->
                    <div class="flex justify-between items-center border-b border-gray-200 pb-4">
                      <label class="text-gray-600 font-medium text-lg w-32">Location</label>
                      <template v-if="isEditing">
                        <input
                          v-model="editProfile.location"
                          type="text"
                          class="flex-1 text-teal-600 text-lg font-medium bg-transparent border-none outline-none focus:bg-gray-50 px-2 py-1 rounded"
                        />
                      </template>
                      <template v-else>
                        <span class="flex-1 text-teal-600 text-lg font-medium text-right">{{
                          profile.location
                        }}</span>
                      </template>
                    </div>

                    <!-- Join Date -->
                    <div class="flex justify-between items-center border-b border-gray-200 pb-4">
                      <label class="text-gray-600 font-medium text-lg w-32">Join Date</label>
                      <span class="flex-1 text-teal-600 text-lg font-medium text-right">{{
                        profile.joinDate
                      }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Buttons -->
              <div class="flex justify-between mt-10">
                <div class="flex gap-4">
                  <template v-if="isEditing">
                    <button
                      @click="saveChanges"
                      class="bg-blue-500 hover:bg-blue-600 text-white px-8 py-3 rounded-full font-semibold text-lg transition-colors shadow-lg"
                    >
                      Save Changes
                    </button>
                    <button
                      @click="cancelEdit"
                      class="bg-gray-500 hover:bg-gray-600 text-white px-8 py-3 rounded-full font-semibold text-lg transition-colors shadow-lg"
                    >
                      Cancel
                    </button>
                  </template>
                  <template v-else>
                    <button
                      @click="isEditing = true"
                      class="bg-blue-500 hover:bg-blue-600 text-white px-8 py-3 rounded-full font-semibold text-lg transition-colors shadow-lg"
                    >
                      Edit Profile
                    </button>
                  </template>
                </div>

                <button
                  class="bg-red-500 hover:bg-red-600 text-white px-8 py-3 rounded-full font-semibold text-lg transition-colors shadow-lg"
                >
                  Delete Account
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const profile = ref({
  name: '',
  email: '',
  height: '',
  weight: '',
  goal: '',
  location: '',
  joinDate: '',
})
const editProfile = ref({ ...profile.value })

const isEditing = ref(false)
const loading = ref(true)
const error = ref(null)

const profileComplete = ref(userStore.profile_complete)
const isAuthenticated = computed(() => userStore.isAuthenticated)

async function fetchUserProfile() {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/user-info/', {
      credentials: 'include',
    })

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`)
    }

    const data = await response.json()

    if (data) {
      const userData = data
      const profileData = userData.profile || {}

      profile.value = {
        name:
          userData.first_name && userData.last_name
            ? `${userData.first_name} ${userData.last_name}`
            : userData.username || '',
        email: userData.email || '',
        height: profileData.height || '',
        weight: profileData.weight || '',
        goal: profileData.goal || '',
        location: profileData.location || '',
        joinDate: new Date().toLocaleDateString(),
      }

      profileComplete.value = userData.profile_complete
      userStore.setProfileComplete(userData.profile_complete)
    }

    editProfile.value = { ...profile.value }
  } catch (err) {
    console.error('Error fetching user profile:', err)
    error.value = 'Failed to load profile: ' + err.message
  } finally {
    loading.value = false
  }
}

function cancelEdit() {
  editProfile.value = { ...profile.value }
  isEditing.value = false
}

onMounted(() => {
  fetchUserProfile()
})
</script>
