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
              />
            </div>
  
            <div class="form-group">
              <label class="form-label" for="email">Email *</label>
              <input
                id="email"
                v-model="coachForm.email"
                type="email"
                class="form-input"
                placeholder="coach@example.com"
                required
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
              />
            </div>
  
            <div class="form-group">
              <label class="form-label" for="cert">Certification *</label>
              <select
                id="cert"
                v-model="coachForm.certification"
                class="form-input"
                required
              >
                <option value="" disabled>Select your certification</option>
                <option>ACE</option>
                <option>NASM</option>
                <option>CSCS</option>
                <option>ISSA</option>
                <option>Other</option>
              </select>
            </div>
  
            <div class="form-group">
              <label class="form-label" for="bio">Short Bio</label>
              <textarea
                id="bio"
                v-model="coachForm.bio"
                class="form-input"
                rows="4"
                placeholder="Tell us a bit about your coaching style and experience"
              />
            </div>
  
            <div class="form-row">
              <button type="submit" class="btn primary">Submit Application</button>
              <button type="button" class="btn ghost" @click="resetForm">Reset</button>
            </div>
          </form>
        </div>
  
        <!-- Application Status & Programs Overview -->
        <div class="content-card">
          <div class="card-title mb-3">Application Status</div>

          <!-- Approval Status Display -->
          <div class="status-section mb-4">
            <div class="status-indicator" :class="approvalStatus">
              <div class="status-icon">
                <span v-if="approvalStatus === 'pending'">⏳</span>
                <span v-else-if="approvalStatus === 'approved'">✅</span>
                <span v-else-if="approvalStatus === 'rejected'">❌</span>
              </div>
              <div class="status-text">
                <div class="status-title">
                  {{ approvalStatus === 'pending' ? 'Application Under Review' :
                     approvalStatus === 'approved' ? 'Application Approved' :
                     'Application Rejected' }}
                </div>
                <div class="status-message">
                  {{ approvalStatus === 'pending' ? 'Your application is being reviewed by our admin team.' :
                     approvalStatus === 'approved' ? 'Congratulations! You can now create workout programs.' :
                     'Please contact support or resubmit your application.' }}
                </div>
              </div>
            </div>
          </div>

          <!-- Approval Success Message -->
          <div v-if="approvalStatus === 'approved'" class="approval-success">
            <div class="success-icon">🎉</div>
            <div class="success-title">Congratulations!</div>
            <div class="success-message">
              Your coach application has been approved! You will be redirected to your dashboard where you can start creating workout programs.
            </div>
          </div>

          <!-- Demo Approval Button (for testing) -->
          <div v-if="approvalStatus !== 'approved'" class="demo-section">
            <button class="btn primary small" @click="simulateApproval">
              🔧 Simulate Admin Approval (Demo)
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { reactive, ref } from 'vue'

  const emit = defineEmits<{
    approved: []
  }>()
  
  interface CoachForm {
    fullName: string
    email: string
    phone: string
    certification: string
    bio: string
  }
  
  const coachForm = reactive<CoachForm>({
    fullName: '',
    email: '',
    phone: '',
    certification: '',
    bio: ''
  })
  
  const approvalStatus = ref('pending') // 'pending', 'approved', 'rejected'

  
  function submitApplication() {
    // simple front-end validation beyond required attrs
    if (!coachForm.fullName || !coachForm.email || !coachForm.certification) {
      alert('Please fill in all required fields (Full Name, Email, Certification).')
      return
    }
    // In real app: POST to API here
    console.log('Submitted coach application:', { ...coachForm })
    alert('Application submitted! Check console for payload.')
    resetForm()
  }
  
  function resetForm() {
    coachForm.fullName = ''
    coachForm.email = ''
    coachForm.phone = ''
    coachForm.certification = ''
    coachForm.bio = ''
  }
  

  function simulateApproval() {
    approvalStatus.value = 'approved'
    alert('Coach application approved! Redirecting to your dashboard...')
    // Emit event to parent to show dashboard
    setTimeout(() => {
      emit('approved')
    }, 1000)
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

  .status-section { margin-bottom: 20px; }
  .status-indicator {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
  }
  .status-indicator.pending { background: #fef3c7; border-color: #f59e0b; }
  .status-indicator.approved { background: #d1fae5; border-color: #10b981; }
  .status-indicator.rejected { background: #fee2e2; border-color: #ef4444; }

  .status-icon { font-size: 20px; }
  .status-text { flex: 1; }
  .status-title { font-weight: 600; font-size: 14px; margin-bottom: 4px; }
  .status-title { color: #374151; }
  .status-message { color: #6b7280; font-size: 13px; line-height: 1.4; }

  .approval-success {
    text-align: center;
    padding: 32px 16px;
    border: 2px solid #10b981;
    border-radius: 12px;
    background: #d1fae5;
    margin-top: 16px;
  }
  .success-icon { font-size: 48px; margin-bottom: 12px; }
  .success-title {
    font-size: 20px;
    font-weight: 600;
    color: #065f46;
    margin-bottom: 8px;
  }
  .success-message {
    color: #047857;
    line-height: 1.5;
    max-width: 400px;
    margin-left: auto;
    margin-right: auto;
  }

  .demo-section {
    padding-top: 16px;
    border-top: 1px solid #e5e7eb;
    display: flex;
    justify-content: center;
  }
  </style>
  