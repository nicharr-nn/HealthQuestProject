<!-- <script setup>
import GoalSelectionPage from './components/GoalSelectionPage.vue'
</script>

<template>
  <GoalSelectionPage />
</template> -->

<!-- App.vue -->
<template>
  <div id="app">
    <!-- Header Navigation -->
    <header class="header">
      <nav class="nav-container">
        <div class="logo">HealthQuest</div>
        <ul class="nav-links">
          <li><a href="#" class="nav-link active">Progress</a></li>
          <li><a href="#" class="nav-link">Workout program</a></li>
          <li><a href="#" class="nav-link">Workout</a></li>
          <li><a href="#" class="nav-link">food recipe</a></li>
          <li><a href="#" class="nav-link">profile</a></li>
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
          class="page-btn"
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

// Pages (components)
import GoalSelectionPage from './components/GoalSelectionPage.vue'
import BronzeDashboard from './components/BronzeDashboard.vue'
import SilverDashboard from './components/SilverDashboard.vue'
import WorkoutProgram from './components/WorkoutProgram.vue'
import RecipeLibrary from './components/RecipeLibrary.vue'
import CoachPortal from './components/CoachPortal.vue'

// Map page id -> component (avoids string-name pitfalls)
const viewMap = {
  'goal-selection': GoalSelectionPage,
  'bronze-dashboard': BronzeDashboard,
  'silver-dashboard': SilverDashboard,
  'workout-program': WorkoutProgram,
  'recipe-library': RecipeLibrary,
  'coach-portal': CoachPortal
}

const pages = [
  { id: 'goal-selection', name: 'Goal Selection' },
  { id: 'bronze-dashboard', name: 'Bronze Dashboard' },
  { id: 'silver-dashboard', name: 'Silver Dashboard' },
  { id: 'workout-program', name: 'Workout Program' },
  { id: 'recipe-library', name: 'Recipe Library' },
  { id: 'coach-portal', name: 'Coach Portal' }
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
  return viewMap[currentPage.value] ?? GoalSelectionPage
})

function setCurrentPage(pageId) {
  if (viewMap[pageId]) currentPage.value = pageId
  // (optional) else console.warn('Unknown page id:', pageId)
}

function handleGoalSelection(goal) {
  userData.value.selectedGoal = goal
  // redirect after selection
  setTimeout(() => setCurrentPage('bronze-dashboard'), 1500)
}
</script>

<style>
/* (same styles you had) */
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  line-height: 1.6; color: #333; background: #f8fafc;
}
/* Header Navigation */
.header { background: linear-gradient(135deg, #9ca3af 0%, #6b7280 100%); padding: 1rem 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.nav-container { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 1rem; }
.logo { color: white; font-weight: 700; font-size: 1.25rem; }
.nav-links { display: flex; gap: 1rem; list-style: none; }
.nav-link { color: white; text-decoration: none; padding: 0.5rem 1rem; border-radius: 20px; background: rgba(255,255,255,0.1); transition: background 0.2s ease; font-weight: 500; }
.nav-link:hover, .nav-link.active { background: rgba(255,255,255,0.2); }
/* Main Container */
.container { max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }
/* Page Navigation */
.page-nav { display: flex; justify-content: center; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; }
.page-btn { background: white; border: 2px solid #e5e7eb; color: #6b7280; padding: 0.75rem 1.5rem; border-radius: 25px; cursor: pointer; font-weight: 600; transition: all 0.2s ease; }
.page-btn:hover, .page-btn.active { background: #4f46e5; color: white; border-color: #4f46e5; transform: translateY(-1px); }
/* Animations */
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.fade-enter-active, .fade-leave-active { transition: opacity 0.5s ease-out; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
/* Responsive */
@media (max-width: 768px) {
  .nav-links { display: none; }
  .container { padding: 1rem; }
  .page-nav { justify-content: flex-start; overflow-x: auto; padding-bottom: 0.5rem; }
  .page-btn { white-space: nowrap; min-width: max-content; }
}
</style>
