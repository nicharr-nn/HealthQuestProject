<template>
  <div class="w-full p-6">
    <!-- Page Header -->
    <div class="mb-6">
      <h1 class="text-2xl md:text-3xl font-bold text-gray-900">Coach Portal</h1>
      <p class="text-gray-500 mt-1">Create and manage your profile</p>
    </div>

    <!-- Content Grid - Half and Half -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Coach Profile Card -->
      <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Coach Profile</h2>

        <!-- Profile Picture -->
        <div class="flex justify-center mb-4">
          <div class="relative">
            <div class="w-24 h-24 rounded-full bg-gray-200 overflow-hidden shadow-sm">
              <img
                v-if="profilePicture"
                :src="profilePicture"
                alt="Profile Photo"
                class="w-full h-full object-cover"
              />
              <span v-else class="text-gray-500 flex items-center justify-center h-full text-sm">
                No Photo
              </span>
            </div>
            <!-- Upload Button -->
            <label class="absolute bottom-0 right-0 bg-gray-900 text-white p-1.5 rounded-full cursor-pointer hover:bg-gray-700 transition">
              <input type="file" accept="image/*" @change="onProfilePictureSelected" class="hidden" />
              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </label>
          </div>
        </div>

        <!-- Profile Info -->
        <div class="space-y-3">
          <div>
            <label class="text-xs text-gray-500 uppercase tracking-wide">Name</label>
            <p class="text-gray-900 font-medium">{{ googleName }}</p>
          </div>
          <div>
            <label class="text-xs text-gray-500 uppercase tracking-wide">Email</label>
            <p class="text-gray-900 font-medium text-sm break-all">{{ userEmail }}</p>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-xs text-gray-500 uppercase tracking-wide">Height</label>
              <p class="text-gray-900 font-medium">{{ profileHeight || '-' }} cm</p>
            </div>
            <div>
              <label class="text-xs text-gray-500 uppercase tracking-wide">Weight</label>
              <p class="text-gray-900 font-medium">{{ profileWeight || '-' }} kg</p>
            </div>
          </div>
          <div>
            <label class="text-xs text-gray-500 uppercase tracking-wide">Location</label>
            <p class="text-gray-900 font-medium">{{ profileLocation || '-' }}</p>
          </div>
          <div>
            <label class="text-xs text-gray-500 uppercase tracking-wide">Joined Date</label>
            <p class="text-gray-900 font-medium">{{ joinedDate || '-' }}</p>
          </div>
          <div>
            <label class="text-xs text-gray-500 uppercase tracking-wide">Status</label>
            <p class="mt-1">
              <span :class="statusBadgeClass">{{ coachStatus }}</span>
            </p>
          </div>
        </div>
        <!-- Profile Actions -->
        <div class="mt-6 flex gap-2 justify-start">
          <!-- DELETE ACCOUNT BUTTON -->
          <button
            @click="confirmDeleteProfile"
            class="px-3 py-2 rounded-xl border border-red-300 text-red-600 text-sm font-medium hover:bg-red-50 transition cursor-pointer"
          >
            Delete Account
          </button>
        </div>
      </div>

      <!-- Coach Registration / Details Form -->
      <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6 flex flex-col">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">
          {{ hasSubmitted ? 'Profile Details' : 'Coach Application' }}
        </h2>

        <form @submit.prevent="submitApplication" class="grid gap-4">
          <!-- Profile Info Fields -->
          <div class="grid grid-cols-2 gap-3">
            <div class="grid gap-1">
              <label for="height" class="text-gray-700 font-medium text-sm">Height (cm)</label>
              <input
                id="height"
                v-model="coachForm.height"
                type="number"
                placeholder="170"
                :disabled="hasSubmitted && !isEditingProfile"
                class="border border-gray-300 rounded-xl px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 disabled:bg-gray-50 disabled:cursor-not-allowed"
              />
            </div>
            <div class="grid gap-1">
              <label for="weight" class="text-gray-700 font-medium text-sm">Weight (kg)</label>
              <input
                id="weight"
                v-model="coachForm.weight"
                type="number"
                placeholder="70"
                :disabled="hasSubmitted && !isEditingProfile"
                class="border border-gray-300 rounded-xl px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 disabled:bg-gray-50 disabled:cursor-not-allowed"
              />
            </div>
          </div>

          <!-- Location -->
          <div class="grid gap-1">
            <label for="location" class="text-gray-700 font-medium text-sm">Location</label>
            <select
              id="location"
              v-model="coachForm.location"
              :disabled="hasSubmitted && !isEditingProfile"
              class="border border-gray-300 rounded-xl px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 disabled:bg-gray-50 disabled:cursor-not-allowed"
            >
              <option value="">Select your location</option>
              <option value="TH">Thailand</option>
              <option value="USA">United States</option>
              <option value="UK">United Kingdom</option>
              <option value="JP">Japan</option>
              <option value="LA">Laos</option>
              <option value="KR">South Korea</option>
              <option value="O">Other</option>
            </select>
          </div>

          <!-- Bio -->
          <div class="grid gap-1">
            <label for="bio" class="text-gray-700 font-medium text-sm">Short Bio</label>
            <textarea
              id="bio"
              v-model="coachForm.bio"
              rows="4"
              placeholder="Tell us a bit about your coaching style and experience"
              :disabled="hasSubmitted && !isEditingProfile && !isResubmitting"
              maxlength="250"
              class="border border-gray-300 rounded-xl px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 disabled:bg-gray-50 disabled:cursor-not-allowed"
            ></textarea>
            <small class="text-gray-400 text-xs">{{ coachForm.bio.length }}/250 characters</small>
          </div>

          <!-- File Upload -->
          <div v-if="!hasSubmitted || isResubmitting" class="grid gap-2">
            <label for="certDoc" class="inline-block cursor-pointer">
              <input
                id="certDoc"
                type="file"
                accept="application/pdf"
                @change="onFileSelected"
                class="hidden"
                :required="!hasSubmitted"
              />
              <span class="px-4 py-2 border border-gray-300 rounded-xl text-sm font-semibold hover:bg-gray-100 transition">Choose File</span>
            </label>
            <span class="text-gray-700 text-sm max-w-full truncate">{{ selectedFile?.name || 'No file chosen' }}</span>
          </div>

          <!-- Show submitted file info -->
          <div v-else-if="hasSubmitted && selectedFileName" class="grid gap-1">
            <label class="text-gray-700 font-medium text-sm">Certification Document</label>
            <p class="text-gray-700 text-sm max-w-full truncate">{{ selectedFileName }}</p>
          </div>

          <!-- Form Buttons -->
          <div class="flex justify-end gap-2 mt-2">
            <button
              v-if="!hasSubmitted"
              type="submit"
              class="px-4 py-2 rounded-xl bg-gray-900 text-white font-semibold hover:brightness-105 transition cursor-pointer"
            >
              Submit Application
            </button>
            <button
              v-if="!hasSubmitted"
              type="button"
              @click="resetForm"
              class="px-4 py-2 rounded-xl border border-gray-300 font-semibold hover:bg-gray-100 transition cursor-pointer"
            >
              Reset
            </button>

            <button
              v-if="hasSubmitted && coachStatus === 'approved'"
              type="button"
              @click="toggleEdit"
              class="px-4 py-2 rounded-xl bg-gray-900 text-white font-semibold hover:brightness-105 transition cursor-pointer"
            >
              {{ isEditingProfile ? (hasChanges ? 'Save Changes' : 'Cancel') : 'Edit Profile' }}
            </button>

            <button
              v-if="hasSubmitted && coachStatus !== 'approved' && !isResubmitting"
              type="button"
              @click="startResubmit"
              class="px-4 py-2 rounded-xl bg-gray-900 text-white font-semibold hover:brightness-105 transition cursor-pointer"
            >
              Resubmit Certification
            </button>

            <template v-if="isResubmitting">
              <button
                type="submit"
                class="px-4 py-2 rounded-xl bg-gray-900 text-white font-semibold hover:brightness-105 transition cursor-pointer"
              >
                Submit Application
              </button>
            </template>
          </div>
        </form>
      </div>
    </div>
    <DeleteModal
      :show="showDeleteAccountModal"
      title="Delete Account"
      message="Are you sure you want to delete your entire account?"
      additionalText="This action cannot be undone."
      confirmText="Delete"
      cancelText="Cancel"
      @confirm="deleteUserAccount"
      @update:show="val => (showDeleteAccountModal = val)"
    />
    <div
      v-if="showResubmitConfirm"
      class="fixed inset-0 z-50 grid place-items-center bg-black/50 p-4"
      @click.self="showResubmitConfirm = false"
    >
      <div class="bg-white rounded-xl shadow-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-semibold mb-4">Confirm Resubmit</h3>
        <p class="mb-4">Are you sure you want to resubmit your certification? This will overwrite your previous submission.</p>
        <div class="flex justify-end gap-3">
          <button @click="showResubmitConfirm = false" class="px-4 py-2 border rounded cursor-pointer">Cancel</button>
          <button
            @click="confirmResubmitAction"
            class="px-4 py-2 bg-gray-900 text-white rounded hover:brightness-105 cursor-pointer"
          >
            Resubmit
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import DeleteModal from '@/components/DeleteModal.vue'

const userStore = useUserStore()
const toast = useToastStore()

const coachForm = reactive({ bio: '', height: '', weight: '', location: '' })
const selectedFile = ref(null)
const selectedFileName = ref(null)
const hasSubmitted = ref(false)
const coachStatus = ref('not submitted')
const originalBio = ref('')
const originalName = ref('')
const originalHeight = ref('')
const originalWeight = ref('')
const originalLocation = ref('')
const isEditingProfile = ref(false)
const isResubmitting = ref(false)
const googleName = ref('')
const userEmail = ref('')
const profilePicture = ref('')
const profileHeight = ref('')
const profileWeight = ref('')
const profileLocation = ref('')
const joinedDate = ref('')

const showDeleteAccountModal = ref(false)
const showResubmitConfirm = ref(false)

function confirmDeleteProfile() {
  showDeleteAccountModal.value = true
}

const hasChanges = computed(() => {
  return (
    coachForm.bio !== originalBio.value ||
    coachForm.height !== originalHeight.value ||
    coachForm.weight !== originalWeight.value ||
    coachForm.location !== originalLocation.value
  );
});

function toggleEdit() {
  // When not editing
  if (!isEditingProfile.value) {
    isEditingProfile.value = true;
    return;
  }
  // When editing
  if (!hasChanges.value) {
    // cancel
    cancelEdit();
    return;
  }
  // save
  saveProfile();
}

// Computed for status badge styling
const statusBadgeClass = computed(() => {
  const base = 'px-2 py-1 rounded-full text-xs font-medium'
  switch (coachStatus.value) {
    case 'approved':
      return `${base} bg-green-100 text-green-700`
    case 'pending':
      return `${base} bg-yellow-100 text-yellow-700`
    case 'rejected':
      return `${base} bg-red-100 text-red-700`
    default:
      return `${base} bg-gray-100 text-gray-700`
  }
})

// Called when file input changes
function onFileSelected(event) {
  const files = event.target.files
  if (files && files.length > 0) {
    selectedFile.value = files[0]
    // Truncate filename if too long
    selectedFileName.value = truncateFileName(files[0].name, 50)
  }
}

// Function to truncate long filenames
function truncateFileName(filename, maxLength = 50) {
  if (filename.length <= maxLength) return filename
  
  const extension = filename.split('.').pop()
  const nameWithoutExt = filename.substring(0, filename.lastIndexOf('.'))
  const truncatedName = nameWithoutExt.substring(0, maxLength - extension.length - 3) // -3 for "..."
  
  return `${truncatedName}...${extension}`
}

function getCsrfToken() {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1] || '';
}

const onProfilePictureSelected = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("photo", file);

  try {
    const response = await fetch("http://127.0.0.1:8000/api/user/upload-photo/", {
      method: "POST",
      body: formData,
      credentials: "include",
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
    });

    const data = await response.json();

    userStore.profile.photo = data.photo_url;
    profilePicture.value = `http://127.0.0.1:8000${data.photo_url}`;

    toast.success('Profile updated successfully!')
  } catch (error) {
    console.error("Upload failed", error);
  }
}

// Fetch coach status on mount
onMounted(async () => {
  const res = await fetch("http://127.0.0.1:8000/api/coach/status/", { credentials: 'include' })
  if (!userStore.user || !userStore.profile) {
    await userStore.init()
  }

  googleName.value = userStore.user?.name || userStore.displayName || ''
  userEmail.value = userStore.user?.email || userStore.profile?.email || ''
  profileHeight.value = userStore.profile?.height || ''
  profileWeight.value = userStore.profile?.weight || ''
  profileLocation.value = userStore.profile?.location || ''
  profilePicture.value = userStore.profile?.photo
  ? `http://127.0.0.1:8000${userStore.profile.photo}`
  : '';

  // Load into form
  coachForm.height = profileHeight.value
  coachForm.weight = profileWeight.value
  coachForm.location = profileLocation.value
  originalHeight.value = profileHeight.value
  originalWeight.value = profileWeight.value
  originalLocation.value = profileLocation.value

  // Format joined date
  const dateJoined = userStore.user.profile.created_at
  if (dateJoined) {
    joinedDate.value = new Date(dateJoined).toLocaleDateString('en-US', {
      year: 'numeric', month: 'short', day: 'numeric'
    })
  }

  if (res.ok) {
    const data = await res.json()
    if (data.coach) {
      coachForm.bio = data.coach.bio || ''
      coachStatus.value = data.coach.status_approval
      hasSubmitted.value = true
      originalBio.value = coachForm.bio
      originalName.value = googleName.value
      if (data.coach.certification_doc) {
        // Truncate existing filename on load
        const fileName = data.coach.certification_doc.split('/').pop()
        selectedFileName.value = truncateFileName(fileName, 50)
      }
    }
  }
})

// Submit coach application
async function submitApplication() {
  // Validate Bio
  if (!coachForm.bio || !coachForm.bio.trim()) {
    toast.error('Please enter a Short Bio.')
    return
  }

  // Validate Certification (file must be selected if first submission or resubmitting)
  if (!selectedFile.value && (!hasSubmitted.value || isResubmitting.value)) {
    toast.error('Please upload a Certification PDF.')
    return
  }

  if (coachForm.bio.length > 250) {
    toast.error('Short Bio cannot exceed 250 characters.')
    return
  }

  const formData = new FormData()
  formData.append('bio', coachForm.bio)
  if (selectedFile.value) formData.append('certification_doc', selectedFile.value)

  const method = hasSubmitted.value ? 'PATCH' : 'POST'

  try {
    const response = await fetch('http://127.0.0.1:8000/api/coach/upload-cert/', {
      method,
      body: formData,
      credentials: 'include'
    })

    if (!response.ok) throw new Error('Upload failed')

    const data = await response.json()
    const newStatus = data?.status_approval || data?.coach?.status_approval || data?.status || 'pending'
    coachStatus.value = newStatus
    hasSubmitted.value = true
    isResubmitting.value = false
    // Truncate filename when setting after submission
    selectedFileName.value = selectedFile.value ? truncateFileName(selectedFile.value.name, 50) : selectedFileName.value
    selectedFile.value = null
    toast.info('Application submitted! Status is now pending.')
  } catch (err) {
    console.error(err)
    toast.error('Upload failed')
  }
}

// Reset form (used before submit)
function resetForm() {
  coachForm.bio = ''
  selectedFile.value = null
  selectedFileName.value = null
}

function startResubmit() {
  // Show confirmation modal first
  showResubmitConfirm.value = true
}

function confirmResubmitAction() {
  // User confirmed resubmit
  isResubmitting.value = true
  selectedFile.value = null
  selectedFileName.value = null
  showResubmitConfirm.value = false
}


function cancelEdit() {
  isEditingProfile.value = false
  coachForm.bio = originalBio.value
  coachForm.height = originalHeight.value
  coachForm.weight = originalWeight.value
  coachForm.location = originalLocation.value
}

async function saveProfile() {
  const payload = {}

  if (coachForm.bio !== originalBio.value) payload.bio = coachForm.bio
  if (coachForm.height !== originalHeight.value) payload.height = coachForm.height
  if (coachForm.weight !== originalWeight.value) payload.weight = coachForm.weight
  if (coachForm.location !== originalLocation.value) payload.location = coachForm.location

  if (Object.keys(payload).length === 0) {
    toast.info("No changes detected.")
    return
  }

  try {
    const response = await fetch("http://127.0.0.1:8000/api/coach/edit-profile/", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(payload)
    })

    if (!response.ok) throw new Error("Failed to update profile")

    const data = await response.json()
    toast.success('Profile updated successfully!')

    // Update form and display values
    coachForm.bio = data.bio || coachForm.bio
    coachForm.height = data.height || coachForm.height
    coachForm.weight = data.weight || coachForm.weight
    coachForm.location = data.location || coachForm.location

    profileHeight.value = coachForm.height
    profileWeight.value = coachForm.weight
    profileLocation.value = coachForm.location

    originalBio.value = coachForm.bio
    originalHeight.value = coachForm.height
    originalWeight.value = coachForm.weight
    originalLocation.value = coachForm.location

    isEditingProfile.value = false
  } catch (err) {
    console.error(err)
    toast.error("Could not update profile")
  }
}

// Delete account
const deleteUserAccount = async () => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/user/delete-account/${userStore.id}/`, {
      method: 'DELETE',
      credentials: 'include',
      headers: {
        'X-CSRFToken': getCsrfToken(),
      },
    });

    if (response.ok) {
      toast.success('Account deactivated successfully.')
      userStore.clearAuthStatus()
      window.location.href = '/'
    } else {
      const data = await response.json().catch(() => ({}))
      toast.error(`Failed: ${response.status} ${data.detail || ''}`)
    }
  } catch (err) {
    console.error('Error deleting account:', err)
    toast.error('Error connecting to server')
  }
}
</script>