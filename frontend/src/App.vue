<!-- App.vue -->
<template>
  <div id="app" class="min-h-screen bg-paper font-subtitle">
    <!-- Header Navigation -->
    <header class="py-4 bg-[#88ACEA] shadow-md">
      <nav class="nav-container">
        <div class="logo font-display">HealthQuest</div>
        <ul class="nav-links">
          <li><a href="#" class="nav-link active font-subtitle">Progress</a></li>
          <li><a href="#" class="nav-link font-subtitle">Workout program</a></li>
          <li><a href="#" class="nav-link font-subtitle">Workout</a></li>
          <li><a href="#" class="nav-link font-subtitle">food recipe</a></li>
          <li><a href="#" class="nav-link font-subtitle">profile</a></li>
        </ul>
      </nav>
    </header>

    <!-- Main Container -->
    <div class="container">
      <!-- Coach Portal for registration, then Dashboard for approved coaches -->
      <CoachPortal @approved="showDashboard = true" v-if="!showDashboard" />

      <!-- Page Navigation (only show when dashboard is visible) -->
      <div v-if="showDashboard" class="page-nav">
        <button
          class="page-btn"
          :class="{ active: currentPage === 'dashboard' }"
          @click="currentPage = 'dashboard'"
        >
          Dashboard
        </button>
        <button
          class="page-btn"
          :class="{ active: currentPage === 'requests' }"
          @click="currentPage = 'requests'"
        >
          Member Requests
        </button>
      </div>

      <!-- Show Dashboard or Member Requests based on currentPage -->
      <CoachDashboard v-if="showDashboard && currentPage === 'dashboard'" />
      <MemberRequests v-if="showDashboard && currentPage === 'requests'" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CoachPortal from './components/CoachPortal.vue'
import CoachDashboard from './components/CoachDashboard.vue'
import MemberRequests from './components/MemberRequests.vue'

const showDashboard = ref(false)
const currentPage = ref('dashboard') // 'dashboard' or 'requests'
</script>

<style>
/* (same styles you had)  ✅ คงสัดส่วน/spacing เดิมทั้งหมด */
/* * { margin: 0; padding: 0; box-sizing: border-box; } */
body {
  /* ฟอนต์/สีจะถูกกำหนดด้วย Tailwind class บน #app แทน */
  line-height: 1.6;
}

/* Header Navigation */
.nav-container { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 1rem; }
.logo { color: white; font-weight: 700; font-size: 1.25rem; }
.nav-links { display: flex; gap: 1rem; list-style: none; }

/* ปล่อย proportion เดิมไว้, เปลี่ยนสีด้วย Tailwind utility ผ่าน class บน element แล้ว */
.nav-link {
  color: white; text-decoration: none; padding: 0.5rem 1rem; border-radius: 20px;
  background: rgba(255,255,255,0.1); transition: background 0.2s ease; font-weight: 500;
}
.nav-link:hover, .nav-link.active { background: rgba(255,255,255,0.2); }

/* Main Container */
.container { max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }

/* Page Navigation */
.page-nav { display: flex; justify-content: center; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; }
.page-btn {
  background: white; border: 2px solid #e5e7eb; color: #6b7280; padding: 0.75rem 1.5rem;
  border-radius: 25px; cursor: pointer; font-weight: 600; transition: all 0.2s ease;
}
.page-btn:hover, .page-btn.active {
  /* ใช้คู่สีเข้ากับธีมมากขึ้นโดยไม่แตะสัดส่วน */
  background: #1e293b; /* ใกล้เคียง text-slate-800 */
  color: white;
  border-color: #1e293b;
  transform: translateY(-1px);
}

/* Responsive */
@media (max-width: 768px) {
  .nav-links { display: none; }
  .container { padding: 1rem; }
  .page-nav { justify-content: flex-start; overflow-x: auto; padding-bottom: 0.5rem; }
  .page-btn { white-space: nowrap; min-width: max-content; }
}
</style>
