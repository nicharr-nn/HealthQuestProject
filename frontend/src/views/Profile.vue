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
                    <div class="w-64 h-64 rounded-full bg-gray-200 overflow-hidden shadow-lg">
                      <img
                        v-if="profile.photo"
                        :src="profile.photo"
                        alt="Profile Photo"
                        class="w-full h-full object-cover"
                      />
                      <span v-else class="text-gray-500 flex items-center justify-center h-full">
                        No Photo
                      </span>
                    </div>  
                    <div class="upload-container">
                      <div class="relative">
                        <!-- Hidden File Input -->
                        <input
                          type="file"
                          id="photo"
                          @change="handleFileChange"
                          class="hidden"
                          :disabled="!isEditing"
                        />

                        <!-- Visible Upload Icon -->
                        <label for="photo" class="absolute bottom-2 right-4 bg-white p-3 rounded-full hover:shadow-xl transition-shadow cursor-pointer">
                          <span class="material-symbols-outlined text-gray-600 text-xl">
                            image_arrow_up
                          </span>
                        </label>
                      </div>
                      <p v-if="uploadMessage" class="mt-4 text-gray-600">{{ uploadMessage }}</p>
                    </div>
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
                          class="flex-1 text-teal-600 text-lg font-medium bg-gray-100 border border-gray-300 outline-none focus:bg-gray-50 px-3 py-2 rounded"
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
                          class="flex-1 text-teal-600 text-lg font-medium bg-gray-100 border border-gray-300 outline-none focus:bg-gray-50 px-3 py-2 rounded"
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
                            class="text-teal-600 text-lg font-medium bg-gray-100 border border-gray-300 outline-none focus:bg-gray-50 px-3 py-2 rounded w-32 text-right"
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
                            class="text-teal-600 text-lg font-medium bg-gray-100 border border-gray-300 outline-none focus:bg-gray-50 px-3 py-2 rounded w-32 text-right"
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
                    <div class="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-gray-200 pb-4" v-if="profile.current_goal !== undefined">
                      <label class="text-gray-600 font-medium text-lg w-32 mb-2 md:mb-0">Goal</label>
                      <template v-if="isEditing">
                        <select
                          v-model="editProfile.current_goal"
                          class="flex-1 text-teal-600 text-lg font-medium bg-gray-100 border border-gray-300 outline-none focus:bg-gray-50 px-3 py-2 rounded"
                        >
                          <option value="">Select a goal</option>
                          <option value="lose_weight">Lose Weight</option>
                          <option value="build_muscle">Build Muscle</option>
                          <option value="improve_endurance">Improve Endurance</option>
                          <option value="general_fitness">General Fitness</option>
                        </select>
                      </template>
                      <template v-else>
                        <span class="flex-1 text-teal-600 text-lg font-medium text-right">
                          {{ formatGoalName(profile.current_goal) || 'No goal set' }}
                        </span>
                      </template>
                    </div>

                    <!-- Location -->
                    <div class="flex justify-between items-center border-b border-gray-200 pb-4">
                      <label class="text-gray-600 font-medium text-lg w-32">Location</label>
                      <template v-if="isEditing">
                        <input
                          v-model="editProfile.location"
                          type="text"
                          class="flex-1 text-teal-600 text-lg font-medium bg-gray-100 border border-gray-300 outline-none focus:bg-gray-50 px-3 py-2 rounded"
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

const userStore = useUserStore()

const profile = ref({
  name: '',
  email: '',
  height: '',
  weight: '',
  current_goal: '',
  location: '',
  joinDate: '',
  photo: null,
})
const editProfile = ref({ ...profile.value })

const isEditing = ref(false)
const loading = ref(true)
const error = ref(null)

const selectedFile = ref(null)
const uploadMessage = ref('')

function getCsrfToken() {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; csrftoken=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return '';
}

function formatGoalName(goalValue) {
  const goalMap = {
    'lose_weight': 'Lose Weight',
    'build_muscle': 'Build Muscle',
    'improve_endurance': 'Improve Endurance',
    'general_fitness': 'General Fitness'
  };
  return goalMap[goalValue] || goalValue;
}

function handleFileChange(event) {
  selectedFile.value = event.target.files[0]
  uploadMessage.value = `Selected file: ${selectedFile.value.name}`
}

async function uploadPhoto() {
  if (!selectedFile.value) return null

  const formData = new FormData()
  formData.append('photo', selectedFile.value)

  try {
    const response = await fetch('http://127.0.0.1:8000/api/upload-photo/', {
      method: 'POST',
      body: formData,
      credentials: 'include',
      headers: {
        'X-CSRFToken': getCsrfToken()
      }
    })

    if (response.ok) {
      const data = await response.json()
      return data.photo_url
    } else {
      const errorData = await response.json()
      uploadMessage.value = `Error: ${errorData.detail || 'Failed to upload photo.'}`
      return null
    }
  } catch (error) {
    console.error('Error uploading photo:', error)
    uploadMessage.value = 'An error occurred while uploading the photo.'
    return null
  }
}


async function saveChanges() {
  try {
    // Upload photo (if new one selected)
    let uploadedPhoto = null
    if (selectedFile.value) {
      uploadedPhoto = await uploadPhoto()
    }

    // Update profile info
    const profileResponse = await fetch('http://127.0.0.1:8000/api/user-info/', {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      credentials: 'include',
      body: JSON.stringify({
        userprofile: {
          height: parseFloat(editProfile.value.height),
          weight: parseFloat(editProfile.value.weight),
          location: editProfile.value.location,
          photo: uploadedPhoto || profile.value.photo,
        }
      }),
    })

    if (!profileResponse.ok) {
      throw new Error(`Failed to save profile changes. Status: ${profileResponse.status}`)
    }

    // Update goal (only if user is normal)
    if (userStore.role === 'normal' && editProfile.value.current_goal) {
      const goalResponse = await fetch("http://127.0.0.1:8000/api/fitness/select-goal/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCsrfToken()
        },
        credentials: "include",
        body: JSON.stringify({
          goal_type: editProfile.value.current_goal
        })
      });

      if (!goalResponse.ok) {
        const errorData = await goalResponse.json();
        if (goalResponse.status !== 400 || !errorData.user_profile) {
          throw new Error("Failed to update goal");
        }
      }
    }

    // Update local state with new values
    if (uploadedPhoto) {
      profile.value.photo = `${uploadedPhoto}?v=${Date.now()}`
      editProfile.value.photo = profile.value.photo
    }

    profile.value.height = editProfile.value.height
    profile.value.weight = editProfile.value.weight
    profile.value.location = editProfile.value.location
    profile.value.current_goal = editProfile.value.current_goal

    isEditing.value = false
    uploadMessage.value = 'Profile updated successfully!'
  } catch (err) {
    console.error('Error saving changes:', err)
    uploadMessage.value = 'Error saving changes: ' + err.message
  }
}

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
      const userData = data.user || {}
      const profileData = userData.profile || {}

      console.log('Current goal:', profileData.current_goal) // Debug log

      profile.value = {
        name:
          userData.first_name && userData.last_name
            ? `${userData.first_name} ${userData.last_name}`
            : userData.username || '',
        email: userData.email || '',
        height: profileData.height || '',
        weight: profileData.weight || '',
        current_goal: profileData.current_goal || '',
        location: profileData.location || '',
        joinDate: new Date().toLocaleDateString(),
        photo: profileData.photo ? `http://127.0.0.1:8000${profileData.photo}` : null,
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
  selectedFile.value = null
  uploadMessage.value = ''
}

onMounted(() => {
  fetchUserProfile()
})
</script>

<style scoped>
img {
  object-fit: cover;
}

.upload-container {
  margin-top: 1rem;
}
</style>