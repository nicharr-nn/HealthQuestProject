<!-- App.vue -->
<template>
  <!-- Full-page AdminDashboard -->
  <AdminDashboard 
    v-if="currentPage === 'admin-dashboard'" 
    @page-change="setCurrentPage"
  />
  
  <!-- Regular App Layout -->
  <div v-else id="app" class="min-h-screen bg-paper font-subtitle">
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
      <!-- Page Navigation -->
      <div class="page-nav">
        <button
          v-for="page in pages"
          :key="page.id"
          class="page-btn font-subtitle"
          :class="{ active: currentPage === page.id }"
          @click="setCurrentPage(page.id)"
        >
          {{ page.name }}
        </button>
      </div>

      <!-- Dynamic Component Rendering (safe mapping) -->
      <keep-alive>
        <component
          :is="currentComponent"
          @goal-selected="handleGoalSelection"
          @page-change="setCurrentPage"
          :user-data="userData"
        />
      </keep-alive>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

import GoalSelectionPage from './components/GoalSelectionPage.vue'
import BronzeDashboard from './components/BronzeDashboard.vue'
import SilverDashboard from './components/SilverDashboard.vue'
import WorkoutProgram from './components/WorkoutProgram.vue'
import RecipeLibrary from './components/RecipeLibrary.vue'
import CoachPortal from './components/CoachPortal.vue'
// import AdminDashboard from './components/AdminDashboard.vue'

const viewMap = {
  'goal-selection': GoalSelectionPage,
  'bronze-dashboard': BronzeDashboard,
  'silver-dashboard': SilverDashboard,
  'workout-program': WorkoutProgram,
  'recipe-library': RecipeLibrary,
  'coach-portal': CoachPortal,
  // 'admin-dashboard': AdminDashboard
}

const pages = [
  { id: 'goal-selection', name: 'Goal Selection' },
  { id: 'bronze-dashboard', name: 'Bronze Dashboard' },
  { id: 'silver-dashboard', name: 'Silver Dashboard' },
  { id: 'workout-program', name: 'Workout Program' },
  { id: 'recipe-library', name: 'Recipe Library' },
  { id: 'coach-portal', name: 'Coach Portal' },
  // { id: 'admin-dashboard', name: 'Admin Dashboard' }
]

const currentPage = ref('goal-selection')

const userData = ref({
  name: 'Katie',
  level: 'Bronze',
  streak: 5,
  xp: 48,
  totalXpForNextLevel: 150,
  selectedGoal: null
})

const currentComponent = computed(() => {
  // AdminDashboard is handled separately in template
  if (currentPage.value === 'admin-dashboard') return null
  return viewMap[currentPage.value] ?? GoalSelectionPage
})

function setCurrentPage(pageId) {
  if (viewMap[pageId] || pageId === 'admin-dashboard') currentPage.value = pageId
}

function handleGoalSelection(goal) {
  userData.value.selectedGoal = goal
  setTimeout(() => setCurrentPage('bronze-dashboard'), 1500)
}
</script>

<style>

body {
  
  line-height: 1.6;
}

/* Header Navigation */
.nav-container { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 1rem; }
.logo { color: white; font-weight: 700; font-size: 1.25rem; }
.nav-links { display: flex; gap: 1rem; list-style: none; }


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
