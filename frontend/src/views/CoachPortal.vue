<template>
  <div class="w-full p-6">
    <div class="mb-6">
      <h1 class="text-3xl font-bold font-subtitle">Coach Portal</h1>
      <p class="text-gray-600 mt-1.5 font-body">Create and manage programs</p>
    </div>

    <div class="flex gap-4">
      <!-- Coach Registration -->
      <div class="flex-1 bg-white border border-gray-200 rounded-2xl p-6 shadow-sm min-w-0">
        <div class="font-semibold text-lg mb-3 font-subtitle">Coach Registration</div>

        <form @submit.prevent="submitApplication" class="grid gap-3.5">
          <div class="grid gap-1.5">
            <label class="text-sm text-gray-700 font-medium">Name</label>
            <input
              v-if="isEditingProfile"
              v-model="googleName"
              type="text"
              class="border border-gray-300 rounded-xl px-3 py-2.5 text-sm outline-none w-full focus:border-indigo-500 focus:shadow-[0_0_0_3px_rgba(99,102,241,0.15)]"
              placeholder="Your name"
            />
            <p v-else class="text-gray-700 font-body">{{ googleName }}</p>
          </div>

          <div class="grid gap-1.5">
            <label class="text-sm text-gray-700 font-medium" for="bio">Short Bio</label>
            <textarea
              id="bio"
              v-model="coachForm.bio"
              class="border border-gray-300 rounded-xl px-3 py-2.5 text-sm outline-none w-full focus:border-indigo-500 focus:shadow-[0_0_0_3px_rgba(99,102,241,0.15)] disabled:bg-gray-50 disabled:cursor-not-allowed"
              rows="4"
              placeholder="Tell us a bit about your coaching style and experience"
              :disabled="hasSubmitted && !isEditingProfile"
              maxlength="250"
            ></textarea>
            <small class="text-gray-500">{{ coachForm.bio.length }}/250 characters</small>
          </div>

          <div v-if="!hasSubmitted || isResubmitting" class="grid gap-1.5">
            <label for="certDoc" class="inline-block">
              <input
                id="certDoc"
                type="file"
                accept="application/pdf"
                @change="onFileSelected"
                class="hidden"
                :required="!hasSubmitted"
              />
              <span class="border border-gray-300 rounded-xl px-3.5 py-2.5 font-semibold bg-white cursor-pointer hover:bg-gray-50 transition-all inline-block">Choose File</span>
            </label>
            <span class="ml-2 mt-5 font-body text-gray-700">
              {{ selectedFile?.name || 'No file chosen' }}
            </span>
          </div>

          <!-- Show submitted file info when already submitted -->
          <div v-else-if="hasSubmitted && selectedFileName" class="grid gap-1.5">
            <label class="text-sm text-gray-700 font-medium">Certification Document</label>
            <p class="text-gray-700 font-body">{{ selectedFileName }}</p>
          </div>

          <div class="flex gap-2.5 mt-1.5">
            <!-- Not submitted yet -->
            <button v-if="!hasSubmitted" type="submit" class="border border-gray-900 rounded-xl px-3.5 py-2.5 font-semibold bg-gray-900 text-white cursor-pointer hover:brightness-105 transition-all">Submit Application</button>
            <button v-if="!hasSubmitted" type="button" class="border border-gray-300 rounded-xl px-3.5 py-2.5 font-semibold bg-white cursor-pointer hover:bg-gray-50 transition-all" @click="resetForm">Reset</button>

            <!-- Already submitted and approved - can edit profile -->
            <template v-else-if="coachStatus === 'approved'">
              <button
                v-if="!isEditingProfile"
                type="button"
                class="border border-gray-900 rounded-xl px-3.5 py-2.5 font-semibold bg-gray-900 text-white cursor-pointer hover:brightness-105 transition-all"
                @click="startEditProfile"
              >
                Edit Profile
              </button>
              <template v-else>
                <button
                  type="button"
                  class="border border-gray-900 rounded-xl px-3.5 py-2.5 font-semibold bg-gray-900 text-white cursor-pointer hover:brightness-105 transition-all"
                  @click="saveProfile"
                >
                  Save Changes
                </button>
                <button
                  type="button"
                  class="border border-gray-300 rounded-xl px-3.5 py-2.5 font-semibold bg-white cursor-pointer hover:bg-gray-50 transition-all"
                  @click="cancelEdit"
                >
                  Cancel
                </button>
              </template>
            </template>

            <!-- Pending or rejected - can resubmit -->
            <button
              v-else-if="!isResubmitting"
              type="button"
              class="border border-gray-900 rounded-xl px-3.5 py-2.5 font-semibold bg-gray-900 text-white cursor-pointer hover:brightness-105 transition-all"
              @click="startResubmit"
            >
              Resubmit Certification
            </button>
            <template v-else>
              <button type="submit" class="border border-gray-900 rounded-xl px-3.5 py-2.5 font-semibold bg-gray-900 text-white cursor-pointer hover:brightness-105 transition-all">Submit Application</button>
              <button type="button" class="border border-gray-300 rounded-xl px-3.5 py-2.5 font-semibold bg-white cursor-pointer hover:bg-gray-50 transition-all" @click="cancelResubmit">Cancel</button>
            </template>
          </div>

          <div v-if="hasSubmitted" class="mt-2">
            <p class="mb-3 text-gray-700">Your application status: <strong>{{ coachStatus }}</strong></p>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

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
  const res = await fetch("http://127.0.0.1:8000/api/coach/status/", { credentials: 'include' })
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
    alert('Please upload a Certification PDF.')
    return
  }

  if (coachForm.bio.length > 250) {
    alert('Short Bio cannot exceed 250 characters.')
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
    selectedFileName.value = selectedFile.value?.name || null
    selectedFile.value = null
    alert('Application submitted! Status is now pending.')
  } catch (err) {
    console.error(err)
    alert('Upload failed')
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
    alert("No changes detected.")
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
    alert("Profile updated successfully!")
    coachForm.bio = data.bio
    googleName.value = data.name

    originalBio.value = data.bio
    originalName.value = data.name
    isEditingProfile.value = false
  } catch (err) {
    console.error(err)
    alert("Could not update profile")
  }
}
</script>