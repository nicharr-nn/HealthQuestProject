<template>
  <div class="coach-portal">
    <div class="page-header">
      <h1 class="page-title">Coach Portal</h1>
      <p class="page-subtitle">Create and manage programs</p>
    </div>

    <div class="content-grid">
      <!-- Coach Registration -->
      <div class="content-card">
        <div class="card-title mb-3">Coach Registration</div>

        <form @submit.prevent="submitApplication" class="coach-form">
          <div class="form-group">
            <label class="form-label">Name</label>
            <input
              v-if="isEditingProfile"
              v-model="googleName"
              type="text"
              class="form-input"
              placeholder="Your name"
            />
            <p v-else class="text-gray-700">{{ googleName }}</p>
          </div>

          <div class="form-group">
            <label class="form-label" for="bio">Short Bio</label>
            <textarea
              id="bio"
              v-model="coachForm.bio"
              class="form-input"
              rows="4"
              placeholder="Tell us a bit about your coaching style and experience"
              :disabled="hasSubmitted && !isEditingProfile"
              maxlength="250"
            ></textarea>
            <small class="text-gray-500">{{ coachForm.bio.length }}/250 characters</small>
          </div>

          <div v-if="!hasSubmitted || isResubmitting" class="form-group">
            <label for="certDoc" class="file-upload-label">
              <input
                id="certDoc"
                type="file"
                accept="application/pdf"
                @change="onFileSelected"
                class="hidden"
                :required="!hasSubmitted"
              />
              <span class="btn ghost">Choose File</span>
            </label>
            <span class="ml-2 mt-5 font-body text-gray-700">
              {{ selectedFile?.name || 'No file chosen' }}
            </span>
          </div>

          <!-- Show submitted file info when already submitted -->
          <div v-else-if="hasSubmitted && selectedFileName" class="form-group">
            <label class="form-label">Certification Document</label>
            <p class="text-gray-700">{{ selectedFileName }}</p>
          </div>

          <div class="form-row">
            <!-- Not submitted yet -->
            <button v-if="!hasSubmitted" type="submit" class="btn primary">Submit Application</button>
            <button v-if="!hasSubmitted" type="button" class="btn ghost" @click="resetForm">Reset</button>

            <!-- Already submitted and approved - can edit profile -->
            <template v-else-if="coachStatus === 'approved'">
              <button 
                v-if="!isEditingProfile"
                type="button" 
                class="btn primary" 
                @click="startEditProfile"
              >
                Edit Profile
              </button>
              <template v-else>
                <button 
                  type="button" 
                  class="btn primary" 
                  @click="saveProfile"
                >
                  Save Changes
                </button>
                <button 
                  type="button" 
                  class="btn ghost" 
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
              class="btn primary" 
              @click="startResubmit"
            >
              Resubmit Certification
            </button>
            <template v-else>
              <button type="submit" class="btn primary">Submit Application</button>
              <button type="button" class="btn ghost" @click="cancelResubmit">Cancel</button>
            </template>
          </div>

          <div v-if="hasSubmitted" class="form-status mt-2">
            <p>Your application status: <strong>{{ coachStatus }}</strong></p>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const router = useRouter()

interface CoachForm {
  bio: string
}

const coachForm = reactive({ bio: '' })
const selectedFile = ref<File | null>(null)
const selectedFileName = ref<string | null>(null)
const hasSubmitted = ref(false)
const coachStatus = ref<'not_submitted' | 'pending' | 'approved' | 'rejected'>('not_submitted')
const originalBio = ref('')
const originalName = ref('')
const isEditingProfile = ref(false)
const isResubmitting = ref(false)
const googleName = ref('')


// Called when file input changes
function onFileSelected(event: Event) {
  const files = (event.target as HTMLInputElement).files
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
  const payload: Record<string, any> = {}

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

<style scoped>
.coach-portal {
  width: 100%;
  padding: 24px;
  box-sizing: border-box;
}
.page-header { margin-bottom: 24px; }
.page-title { font-size: 28px; font-weight: 700; margin: 0; }
.page-subtitle { color: #6b7280; margin-top: 6px; }

.content-grid {
  display: flex;
  gap: 16px;
}
@media (min-width: 900px) { .content-grid { grid-template-columns: 1fr 1fr; } }

.content-card {
  flex: 1;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
  min-width: 0;
}
.card-title { font-weight: 600; font-size: 18px; }
.muted { color: #6b7280; }
.text-gray-700 { color: #374151; }
.mb-3 { margin-bottom: 12px; }
.ml-2 { margin-left: 8px; }
.mt-2 { margin-top: 8px; }
.mt-5 { margin-top: 20px; }

.coach-form { display: grid; gap: 14px; }
.form-group { display: grid; gap: 6px; }
.form-row { display: flex; gap: 10px; margin-top: 6px; }
.form-label { font-size: 14px; color: #374151; font-weight: 500; }
.form-input { border: 1px solid #d1d5db; border-radius: 10px; padding: 10px 12px; font-size: 14px; outline: none; width: 100%; }
.form-input:focus { border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.15); }
.form-input:disabled { background-color: #f9fafb; cursor: not-allowed; }

.btn { border: 1px solid #d1d5db; border-radius: 10px; padding: 10px 14px; font-weight: 600; background: #fff; cursor: pointer; transition: all 0.2s; }
.btn:hover { background: #f9fafb; }
.btn.primary { background: #111827; color: #fff; border-color: #111827; }
.btn.primary:hover { filter: brightness(1.05); }
.btn.ghost { background: #fff; }
.btn.small { padding: 8px 10px; font-size: 13px; }

.file-upload-label { display: inline-block; }
.hidden { display: none; }

.form-status p { margin-bottom: 12px; color: #374151; }
</style>