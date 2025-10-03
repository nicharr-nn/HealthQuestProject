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
            <p>{{ googleName }}</p>
          </div>

          <div class="form-group">
            <label class="form-label" for="bio">Short Bio</label>
            <textarea
              id="bio"
              v-model="coachForm.bio"
              class="form-input"
              rows="4"
              placeholder="Tell us a bit about your coaching style and experience"
              :disabled="hasSubmitted"
            ></textarea>
          </div>
          
          <div class="form-group">
              <label for="certDoc" class="file-upload-label">
                <input
                  id="certDoc"
                  type="file"
                  accept="application/pdf"
                  @change="onFileSelected"
                  class="hidden"   
                  :disabled="hasSubmitted"
                  :required="!hasSubmitted"
                />
                <span class="btn ghost">Choose File</span>
              </label>

              <!-- Always show filename here -->
              <span class="ml-2 mt-5 font-body text-gray-700">
                {{ selectedFile?.name || selectedFileName || (hasSubmitted ? 'File submitted' : 'No file chosen') }}
              </span>
          </div>


        <div class="form-row">
          <button v-if="!hasSubmitted" type="submit" class="btn primary">Submit Application</button>
          <button v-if="!hasSubmitted" type="button" class="btn ghost" @click="resetForm">Reset</button>

          <!-- If already submitted -->
          <button 
            v-else-if="coachStatus === 'approved'" 
            type="button" 
            class="btn primary" 
            @click="editProfile"
          >
            Edit Profile
          </button>

          <button 
            v-else 
            type="button" 
            class="btn primary" 
            @click="resubmit"
          >
            Resubmit Certification
          </button>
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

interface CoachForm {
  bio: string
}

const coachForm = reactive<CoachForm>({
  bio: ''
})


const selectedFile = ref<File | null>(null)
const selectedFileName = ref<string | null>(null)
const hasSubmitted = ref(false)
const coachStatus = ref<'not_submitted' | 'pending' | 'approved' | 'rejected'>('not_submitted')
const originalBio = ref("")
const originalName = ref("")

// Called when file input changes
function onFileSelected(event: Event) {
  const files = (event.target as HTMLInputElement).files
  if (files && files.length > 0) {
    selectedFile.value = files[0]
    selectedFileName.value = files[0].name
  }
}

// Fetch coach status on mount
const googleName = ref('')

// router for redirects when coach is approved
const router = useRouter()

// On mounted, fetch from backend
onMounted(async () => {
  const res = await fetch("http://127.0.0.1:8000/api/coach/status/", { credentials: 'include' })
  if (res.ok) {
    const data = await res.json()
    if (data.coach) {
      googleName.value = data.coach.name
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
  if (!selectedFile.value) {
    alert('Please upload a Certification PDF.')
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
    //coachStatus.value = 'pending'
    const newStatus = data?.status_approval || data?.coach?.status_approval || data?.status || 'pending'
    coachStatus.value = newStatus
    hasSubmitted.value = true
    selectedFileName.value = selectedFile.value?.name || null
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

// Resubmit application
function resubmit() {
  const confirmed = confirm('Are you sure you want to resubmit your certification?')
  if (confirmed) {
    hasSubmitted.value = false
    selectedFile.value = null
    selectedFileName.value = null
  }
}


async function editProfile() {
  // Build payload only with changed fields
  const payload: Record<string, any> = {}

  if (coachForm.bio !== originalBio.value) {
    payload.bio = coachForm.bio
  }

  if (googleName.value !== originalName.value) {
    payload.name = googleName.value
  }

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

    // Update originals so user can’t save again without changes
    originalBio.value = data.bio
    originalName.value = data.name
  } catch (err) {
    console.error(err)
    alert("Could not update profile")
  }
}

</script>

<style scoped>
.coach-portal { max-width: 1100px; margin: 0 auto; padding: 24px; }
.page-header { margin-bottom: 24px; }
.page-title { font-size: 28px; font-weight: 700; margin: 0; }
.page-subtitle { color: #6b7280; margin-top: 6px; }

.content-grid { display: grid; grid-template-columns: 1fr; gap: 16px; }
@media (min-width: 900px) { .content-grid { grid-template-columns: 1fr 1fr; } }

.content-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 16px; padding: 20px; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }
.card-title { font-weight: 600; font-size: 18px; }
.muted { color: #6b7280; }

.coach-form { display: grid; gap: 14px; }
.form-group { display: grid; gap: 6px; }
.form-row { display: flex; gap: 10px; margin-top: 6px; }
.form-label { font-size: 14px; color: #374151; }
.form-input { border: 1px solid #d1d5db; border-radius: 10px; padding: 10px 12px; font-size: 14px; outline: none; }
.form-input:focus { border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.15); }

.btn { border: 1px solid #d1d5db; border-radius: 10px; padding: 10px 14px; font-weight: 600; background: #fff; cursor: pointer; }
.btn:hover { background: #f9fafb; }
.btn.primary { background: #111827; color: #fff; border-color: #111827; }
.btn.primary:hover { filter: brightness(1.05); }
.btn.ghost { background: #fff; }
.btn.small { padding: 8px 10px; font-size: 13px; }

.program-list { list-style: none; padding: 0; margin: 0; display: grid; gap: 10px; }
.program-item { display: flex; align-items: center; justify-content: space-between; border: 1px solid #e5e7eb; border-radius: 12px; padding: 12px 14px; }
.program-name { font-weight: 600; }
.program-meta { color: #6b7280; font-size: 13px; margin-top: 2px; }
.form-status p { margin-bottom: 12px; }
</style>