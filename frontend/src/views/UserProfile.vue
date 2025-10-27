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
                        <label 
                          for="photo" 
                          :class="{ 'cursor-pointer': isEditing, 'cursor-not-allowed opacity-0': !isEditing }"
                          class="absolute bottom-2 right-4 bg-white p-3 rounded-full hover:shadow-xl transition-shadow"
                        >
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
                <div class="flex-1 min-w-0">
                  <div class="space-y-5">
                    <!-- Name (Read-only) -->
                    <div class="flex justify-between items-center border-b border-gray-200 pb-4">
                      <label class="text-gray-600 font-medium text-lg w-32 flex-shrink-0">Name</label>
                      <div class="flex-1 min-w-0 text-right">
                        <span class="text-teal-600 text-lg font-medium break-words">
                          {{ profile.name }}
                        </span>
                        <p v-if="isEditing" class="text-xs text-gray-400 mt-1">
                          (Linked to Google account)
                        </p>
                      </div>
                    </div>

                    <!-- Email (Read-only) -->
                    <div class="flex justify-between items-center border-b border-gray-200 pb-4">
                      <label class="text-gray-600 font-medium text-lg w-32 flex-shrink-0">Email</label>
                      <div class="flex-1 min-w-0 text-right">
                        <span class="text-teal-600 text-lg font-medium break-all">
                          {{ profile.email }}
                        </span>
                        <p v-if="isEditing" class="text-xs text-gray-400 mt-1">
                          (Linked to Google account)
                        </p>
                      </div>
                    </div>

                    <!-- Height -->
                    <div class="flex justify-between items-center border-b border-gray-200 pb-4">
                      <label class="text-gray-600 font-medium text-lg w-32 flex-shrink-0">Height</label>
                      <div class="flex-1 min-w-0">
                        <div class="flex justify-end items-center">
                          <template v-if="isEditing">
                            <input
                              v-model="editProfile.height"
                              @input="handleHeightInput"
                              @blur="handleHeightInput"
                              type="number"
                              step="0.1"
                              min="50"
                              max="220"
                              class="text-teal-600 text-lg font-medium bg-gray-100 border outline-none focus:bg-gray-50 px-3 py-2 rounded w-32 text-right"
                              :class="validationErrors.height ? 'border-red-500' : 'border-gray-300'"
                            />
                          </template>
                          <template v-else>
                            <span class="text-teal-600 text-lg font-medium">
                              {{ profile.height }}
                            </span>
                          </template>
                          <span class="text-gray-600 text-lg ml-2">cm</span>
                        </div>
                        <p v-if="isEditing && validationErrors.height" class="text-red-500 text-xs mt-1 text-right">
                          {{ validationErrors.height }}
                        </p>
                      </div>
                    </div>

                    <!-- Weight -->
                    <div class="flex justify-between items-center border-b border-gray-200 pb-4">
                      <label class="text-gray-600 font-medium text-lg w-32 flex-shrink-0">Weight</label>
                      <div class="flex-1 min-w-0">
                        <div class="flex justify-end items-center">
                          <template v-if="isEditing">
                            <input
                              v-model="editProfile.weight"
                              @input="handleWeightInput"
                              @blur="handleWeightInput"
                              type="number"
                              step="0.1"
                              min="20"
                              max="200"
                              class="text-teal-600 text-lg font-medium bg-gray-100 border outline-none focus:bg-gray-50 px-3 py-2 rounded w-32 text-right"
                              :class="validationErrors.weight ? 'border-red-500' : 'border-gray-300'"
                            />
                          </template>
                          <template v-else>
                            <span class="text-teal-600 text-lg font-medium">
                              {{ profile.weight }}
                            </span>
                          </template>
                          <span class="text-gray-600 text-lg ml-2">Kg</span>
                        </div>
                        <p v-if="isEditing && validationErrors.weight" class="text-red-500 text-xs mt-1 text-right">
                          {{ validationErrors.weight }}
                        </p>
                      </div>
                    </div>

                    <!-- Goal -->
                    <div class="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-gray-200 pb-4" v-if="profile.current_goal !== undefined">
                      <label class="text-gray-600 font-medium text-lg w-32 mb-2 md:mb-0 flex-shrink-0">Goal</label>
                      <div class="flex-1 min-w-0 text-right">
                        <template v-if="isEditing">
                          <select
                            v-model="editProfile.current_goal"
                            class="w-full text-teal-600 text-lg font-medium bg-gray-100 border border-gray-300 outline-none focus:bg-gray-50 px-3 py-2 rounded"
                          >
                            <option value="">Select a goal</option>
                            <option value="lose_weight">Lose Weight</option>
                            <option value="build_muscle">Build Muscle</option>
                            <option value="improve_endurance">Improve Endurance</option>
                            <option value="general_fitness">General Fitness</option>
                          </select>
                        </template>
                        <template v-else>
                          <span class="text-teal-600 text-lg font-medium break-words">
                            {{ formatGoalName(profile.current_goal) || 'No goal set' }}
                          </span>
                        </template>
                      </div>
                    </div>

                    <!-- Location -->
                    <div class="flex justify-between items-center border-b border-gray-200 pb-4">
                      <label class="text-gray-600 font-medium text-lg w-32 flex-shrink-0">Location</label>
                      <div class="flex-1 min-w-0 text-right">
                        <template v-if="isEditing">
                          <select
                            v-model="editProfile.location"
                            class="w-full text-teal-600 text-lg font-medium bg-gray-100 border border-gray-300 outline-none focus:bg-gray-50 px-3 py-2 rounded"
                          >
                            <option value="">Select location</option>
                            <option value="TH">Thailand</option>
                            <option value="USA">United States</option>
                            <option value="UK">United Kingdom</option>
                            <option value="JP">Japan</option>
                            <option value="LA">Laos</option>
                            <option value="KR">South Korea</option>
                            <option value="O">Other</option>
                          </select>
                        </template>
                        <template v-else>
                          <span class="text-teal-600 text-lg font-medium break-words">
                            {{ formatLocationName(profile.location) }}
                          </span>
                        </template>
                      </div>
                    </div>

                    <!-- Join Date -->
                    <div class="flex justify-between items-center border-b border-gray-200 pb-4">
                      <label class="text-gray-600 font-medium text-lg w-32 flex-shrink-0">Join Date</label>
                      <span class="flex-1 text-teal-600 text-lg font-medium text-right min-w-0 break-words">
                        {{ profile.joinDate }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Buttons -->
              <div class="flex flex-col md:flex-row justify-between mt-10 gap-4">
                <div class="flex gap-4">
                  <template v-if="isEditing">
                    <button
                      @click="saveChanges"
                      :disabled="isFormInvalid"
                      :class="{ 'opacity-50 cursor-not-allowed': validationErrors.height || validationErrors.weight }"
                      class="bg-blue-500 hover:bg-blue-600 text-white px-8 py-3 rounded-full font-semibold text-lg transition-colors shadow-lg disabled:hover:bg-blue-500"
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
                  @click="deleteAccount"
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
const validationErrors = ref({
  height: '',
  weight: ''
})

const isFormInvalid = computed(() => 
  validationErrors.value.height !== '' || validationErrors.value.weight !== ''
)


function getCsrfToken() {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; csrftoken=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return '';
}

function validateHeight(value) {
  const height = parseFloat(value)
  
  if (!value || value === '') {
    return 'Height is required'
  }
  
  if (isNaN(height)) {
    return 'Height must be a valid number'
  }
  
  if (height <= 50) {
    return 'Height must be greater than 50 cm'
  }
  
  if (height > 220) {
    return 'Height must be less than or equal to 220 cm'
  }
  
  return ''
}

function validateWeight(value) {
  const weight = parseFloat(value)
  
  if (!value || value === '') {
    return 'Weight is required'
  }
  
  if (isNaN(weight)) {
    return 'Weight must be a valid number'
  }
  
  if (weight <= 20) {
    return 'Weight must be greater than 20 kg'
  }
  
  if (weight > 200) {
    return 'Weight must be less than or equal to 200 kg'
  }
  
  return ''
}

function validateForm() {
  // Clear previous errors
  validationErrors.value = {
    height: '',
    weight: ''
  }
  
  // Validate height
  validationErrors.value.height = validateHeight(editProfile.value.height)
  
  // Validate weight
  validationErrors.value.weight = validateWeight(editProfile.value.weight)
  
  // Return true if no errors
  return !validationErrors.value.height && !validationErrors.value.weight
}

function handleHeightInput() {
  if (isEditing.value) {
    validationErrors.value.height = validateHeight(editProfile.value.height)
  }
}

function handleWeightInput() {
  if (isEditing.value) {
    validationErrors.value.weight = validateWeight(editProfile.value.weight)
  }
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

function formatLocationName(locationValue) {
  const locationMap = {
    'TH': 'Thailand',
    'USA': 'United States',
    'UK': 'United Kingdom',
    'JP': 'Japan',
    'LA': 'Laos',
    'KR': 'South Korea',
    'O': 'Other'
  };
  return locationMap[locationValue] || locationValue;
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
  // Validate form before saving
  if (!validateForm()) {
    uploadMessage.value = 'Please fix the validation errors before saving.'
    return
  }

  try {
    // Upload photo (if new one selected)
    let uploadedPhoto = null
    if (selectedFile.value) {
      uploadedPhoto = await uploadPhoto()
    }

    const profileData = {
      height: parseFloat(editProfile.value.height),
      weight: parseFloat(editProfile.value.weight),
      location: editProfile.value.location,
    }

    // Update profile info
    const profileResponse = await fetch('http://127.0.0.1:8000/api/user-info/', {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      credentials: 'include',
      body: JSON.stringify(profileData),
    })

    if (!profileResponse.ok) {
      throw new Error(`Failed to save profile changes. Status: ${profileResponse.status}`)
    }

    // Update goal (only if user is normal or member)
    if ((userStore.role === 'normal' || userStore.role === 'member') && editProfile.value.current_goal) {
      const goalResponse = await fetch("http://127.0.0.1:8000/api/select-goal/", {
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
    
    // Clear validation errors
    validationErrors.value = {
      height: '',
      weight: ''
    }
  } catch (err) {
    console.error('Error saving changes:', err)
    uploadMessage.value = 'Error saving changes: ' + err.message
  }
}

const profileComplete = ref(userStore.profile_complete)

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
  validationErrors.value = {
    height: '',
    weight: ''
  }
}

async function deleteAccount() {
  if (!confirm('Are you sure you want to deactivate your account?')) return

  const res = await fetch(`http://127.0.0.1:8000/api/user-info/`, {
    method: 'DELETE',
    credentials: 'include',
    headers: {
      'X-CSRFToken': getCsrfToken(),
    },
  })

  if (res.ok) {
    alert('Account deactivated successfully.')
    userStore.clearAuthStatus()
    window.location.href = '/'
  } else {
    const data = await res.json().catch(() => ({}))
    alert(`Failed: ${res.status} ${data.detail || ''}`)
  }
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