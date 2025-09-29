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
            <label class="form-label" for="fullName">Full Name *</label>
            <input
              id="fullName"
              v-model="coachForm.fullName"
              type="text"
              class="form-input"
              placeholder="Enter your name"
              required
              :disabled="hasSubmitted"
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="phone">Phone Number</label>
            <input
              id="phone"
              v-model="coachForm.phone"
              type="tel"
              class="form-input"
              placeholder="+66 8x xxx xxxx"
              :disabled="hasSubmitted"
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="certDoc">Certification Document (PDF) *</label>
            <input
              id="certDoc"
              type="file"
              accept="application/pdf"
              @change="onFileSelected"
              class="form-input"
              :disabled="hasSubmitted"
              :required="!hasSubmitted"
            />
            <span v-if="selectedFile">{{ selectedFile.name }}</span>
            <span v-else-if="selectedFileName">{{ selectedFileName }}</span>
            <span v-else-if="hasSubmitted && coachStatus === 'pending'">File submitted</span>
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

          <div class="form-row">
            <button v-if="!hasSubmitted" type="submit" class="btn primary">Submit Application</button>
            <button v-if="!hasSubmitted" type="button" class="btn ghost" @click="resetForm">Reset</button>
            <button v-else type="button" class="btn primary" @click="resubmit">Resubmit Certification</button>
          </div>

          <div v-if="hasSubmitted" class="form-status mt-2">
            <p>Your application status: <strong>{{ coachStatus }}</strong></p>
          </div>
        </form>
      </div>

      <!-- Programs Overview (mock) -->
      <div class="content-card">
        <div class="card-title mb-3">Your Programs</div>
        <div v-if="programs.length === 0" class="muted">No programs yet. Create your first one!</div>
        <ul v-else class="program-list">
          <li v-for="p in programs" :key="p.id" class="program-item">
            <div>
              <div class="program-name">{{ p.name }}</div>
              <div class="program-meta">Level: {{ p.level }} · Duration: {{ p.duration }} weeks</div>
            </div>
            <button class="btn small" @click="openProgram(p.id)">Open</button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'

interface CoachForm {
  fullName: string
  phone: string
  bio: string
}

const coachForm = reactive<CoachForm>({
  fullName: '',
  phone: '',
  bio: ''
})

const selectedFile = ref<File | null>(null)
const selectedFileName = ref<string | null>(null)
const hasSubmitted = ref(false)
const coachStatus = ref<'not_submitted' | 'pending' | 'approved' | 'rejected'>('not_submitted')

// Mock programs array
const programs = ref<{ id: number; name: string; level: string; duration: number }[]>([])

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
  try {
    const res = await fetch("http://127.0.0.1:8000/api/coach/status/", { credentials: "include" })
    if (res.ok) {
      const data = await res.json()
      if (data.coach) {
        // Use backend values for form
        coachForm.fullName = data.coach.user.full_name || ""
        coachForm.phone = data.coach.user.phone || ""
        coachForm.bio = data.coach.bio || ""
        coachStatus.value = data.coach.status_approval
        hasSubmitted.value = true
        if (data.coach.certification_doc) {
          selectedFileName.value = data.coach.certification_doc.split("/").pop()
        }
      }
    }
  } catch (err) {
    console.error(err)
  }
})

// Submit coach application
async function submitApplication() {
  if (!coachForm.fullName || !selectedFile.value) {
    alert('Please fill in all required fields (Full Name, Certification PDF).')
    return
  }

  const formData = new FormData()
  formData.append('fullName', coachForm.fullName)
  formData.append('phone', coachForm.phone)
  formData.append('bio', coachForm.bio)
  formData.append('certification_doc', selectedFile.value)

  try {
    const response = await fetch('http://127.0.0.1:8000/api/coach/upload-cert/', {
      method: 'POST',
      body: formData,
      credentials: 'include'
    })

    if (!response.ok) throw new Error('Upload failed')

    const data = await response.json()
    coachStatus.value = 'pending'
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
  coachForm.fullName = ''
  coachForm.phone = ''
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

// Mock open program function
function openProgram(id: number) {
  alert(`Open program ID: ${id}`)
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
