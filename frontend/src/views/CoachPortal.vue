<template>
  <div class="w-full p-6">
    <!-- Page Header -->
    <div class="mb-6">
      <h1 class="text-2xl md:text-3xl font-bold text-gray-900">Coach Portal</h1>
      <p class="text-gray-500 mt-1">Create and manage your profile</p>
    </div>

    <!-- Content Grid -->
    <div class="flex flex-col md:flex-row gap-4">
      <!-- Coach Registration Card -->
      <div class="flex-1 bg-white border border-gray-200 rounded-2xl shadow-sm p-6 min-w-0">

        <form @submit.prevent="submitApplication" class="grid gap-4">
          <!-- Name -->
          <div class="grid gap-1">
            <label class="text-gray-700 font-medium text-sm">Name</label>
            <p class="text-gray-700 text-sm">{{ googleName }}</p>
          </div>

          <!-- Bio -->
          <div class="grid gap-1">
            <label for="bio" class="text-gray-700 font-medium text-sm">Short Bio</label>
            <textarea
              id="bio"
              v-model="coachForm.bio"
              rows="4"
              placeholder="Tell us a bit about your coaching style and experience"
              :disabled="hasSubmitted && !isEditingProfile"
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
            <span class="text-gray-700 text-sm">{{ selectedFile?.name || 'No file chosen' }}</span>
          </div>

          <!-- Show submitted file info -->
          <div v-else-if="hasSubmitted && selectedFileName" class="grid gap-1">
            <label class="text-gray-700 font-medium text-sm">Certification Document</label>
            <p class="text-gray-700 text-sm">{{ selectedFileName }}</p>
          </div>

          <!-- Buttons -->
          <div class="flex flex-wrap gap-2 mt-2">
            <!-- Not submitted -->
            <button v-if="!hasSubmitted" type="submit" class="px-4 py-2 rounded-xl bg-gray-900 text-white font-semibold hover:brightness-105 transition">Submit Application</button>
            <button v-if="!hasSubmitted" type="button" @click="resetForm" class="px-4 py-2 rounded-xl border border-gray-300 font-semibold hover:bg-gray-100 transition">Reset</button>

            <!-- Already submitted -->
            <template v-else-if="coachStatus === 'approved'">
              <template v-if="!isEditingProfile">
                <button type="button" @click="startEditProfile" class="px-4 py-2 rounded-xl bg-gray-900 text-white font-semibold hover:brightness-105 transition">Edit Profile</button>
              </template>
              <template v-else>
                <button type="button" @click="saveProfile" class="px-4 py-2 rounded-xl bg-gray-900 text-white font-semibold hover:brightness-105 transition">Save Changes</button>
                <button type="button" @click="cancelEdit" class="px-4 py-2 rounded-xl border border-gray-300 font-semibold hover:bg-gray-100 transition">Cancel</button>
              </template>
            </template>

            <!-- Pending or rejected -->
            <button v-else-if="!isResubmitting" type="button" @click="startResubmit" class="px-4 py-2 rounded-xl bg-gray-900 text-white font-semibold hover:brightness-105 transition">Resubmit Certification</button>
            <template v-else>
              <button type="submit" class="px-4 py-2 rounded-xl bg-gray-900 text-white font-semibold hover:brightness-105 transition">Submit Application</button>
              <button type="button" @click="cancelResubmit" class="px-4 py-2 rounded-xl border border-gray-300 font-semibold hover:bg-gray-100 transition">Cancel</button>
            </template>
          </div>

          <!-- Status -->
          <div v-if="hasSubmitted" class="mt-2 text-sm text-gray-700">
            Your application status: <strong>{{ coachStatus }}</strong>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

const userStore = useUserStore()
const toast = useToastStore()

const coachForm = reactive({ bio: '' })
const selectedFile = ref(null)
const selectedFileName = ref(null)
const hasSubmitted = ref(false)
const coachStatus = ref('not_submitted')
const originalBio = ref('')
const originalName = ref('')
const isEditingProfile = ref(false)
const isResubmitting = ref(false)
const googleName = ref('')
const API_URL = 'http://127.0.0.1:8000'

// Called when file input changes
function onFileSelected(event) {
  const files = event.target.files
  if (files && files.length > 0) {
    selectedFile.value = files[0]
    selectedFileName.value = files[0].name
  }
}

// Fetch coach status on mount
onMounted(async () => {
  const res = await fetch(`${API_URL}/api/coach/status/`, { credentials: 'include' })
  if (!userStore.user || !userStore.profile) {
    await userStore.init()
  }

  googleName.value = userStore.user?.name || userStore.displayName || ''

  if (res.ok) {
    const data = await res.json()
    if (data.coach) {
      coachForm.bio = data.coach.bio || ''
      coachStatus.value = data.coach.status_approval
      hasSubmitted.value = true
      originalBio.value = coachForm.bio
      originalName.value = googleName.value
      if (data.coach.certification_doc) {
        selectedFileName.value = data.coach.certification_doc.split('/').pop()
      }
    }
  }
})

// Submit coach application
async function submitApplication() {
  if (!selectedFile.value && !hasSubmitted.value) {
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

  if (userStore.loading) {
    await userStore.init()
  }

  try {
    const response = await fetch(`${API_URL}/api/coach/upload-cert/`, {
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
    selectedFileName.value = selectedFile.value?.name || null
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

// Start resubmit process
function startResubmit() {
  const confirmed = confirm('Are you sure you want to resubmit your certification?')
  if (confirmed) {
    isResubmitting.value = true
    selectedFile.value = null
  }
}

// Cancel resubmit
function cancelResubmit() {
  isResubmitting.value = false
  selectedFile.value = null
}

// Start editing profile
function startEditProfile() {
  isEditingProfile.value = true
}

function cancelEdit() {
  isEditingProfile.value = false
  coachForm.bio = originalBio.value
  googleName.value = originalName.value
}

async function saveProfile() {
  const payload = {}

  if (coachForm.bio !== originalBio.value) payload.bio = coachForm.bio
  if (googleName.value !== originalName.value) payload.name = googleName.value

  if (Object.keys(payload).length === 0) {
    toast.info("No changes detected.")
    return
  }

  try {
    const response = await fetch(`${API_URL}/api/coach/edit-profile/`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(payload)
    })

    if (!response.ok) throw new Error("Failed to update profile")

    const data = await response.json()
    toast.success("Profile updated successfully!")
    coachForm.bio = data.bio
    googleName.value = data.name

    originalBio.value = data.bio
    originalName.value = data.name
    isEditingProfile.value = false
  } catch (err) {
    console.error(err)
    toast.error("Could not update profile")
  }
}
</script>
