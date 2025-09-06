<!-- SilverDashboard.vue -->
<template>
  <div class="silver-dashboard">
    <!-- User Profile Header -->
    <div class="dashboard-header">
      <div class="user-profile">
        <div class="user-info-section">
          <div class="user-avatar avatar-silver">{{ userInitial }}</div>
          <div class="user-details">
            <h2>{{ userData.name }}</h2>
            <div class="user-level">Silver Level • Day {{ userData.streak }} Streak</div>
          </div>
        </div>
        <div class="tier-badge badge-silver">Silver</div>
      </div>

      <div class="progress-section">
        <div class="progress-header">
          <div class="progress-label">Progress to Gold</div>
          <div class="progress-value">{{ silverXp }}/{{ goldRequirement }} XP</div>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
        </div>
      </div>
    </div>

    <!-- Content Cards -->
    <div class="content-grid">
      <!-- Today's Workout -->
      <div class="content-card">
        <div class="card-header">
          <div class="card-title">Today's Workout</div>
          <div class="card-meta">45 min</div>
        </div>
        <div class="card-description">{{ todayWorkout.description }} • Earn +{{ todayWorkout.xp }} XP</div>
        <button class="action-btn" @click="startWorkout">Start Workout</button>
      </div>

      <!-- Recipe Library (Unlocked) -->
      <div class="content-card recipe-unlocked">
        <div class="card-header">
          <div class="card-title">🥗 Recipe Library</div>
          <div class="new-badge">NEW</div>
        </div>
        <div class="card-description">Access 100+ healthy recipes and meal plans</div>
        <button class="action-btn secondary" @click="goToRecipes">View Recipes</button>
      </div>

      <!-- Nutrition Tracking -->
      <div class="content-card">
        <div class="card-header">
          <div class="card-title">Nutrition Tracking</div>
          <div class="card-meta">Today</div>
        </div>
        <div class="card-description">Log your meals and track macros</div>
        <div class="nutrition-summary">
          <div class="macro-item">
            <span class="macro-label">Protein:</span>
            <span class="macro-value">{{ nutrition.protein }}g / {{ nutrition.proteinGoal }}g</span>
          </div>
          <div class="macro-item">
            <span class="macro-label">Carbs:</span>
            <span class="macro-value">{{ nutrition.carbs }}g / {{ nutrition.carbsGoal }}g</span>
          </div>
          <div class="macro-item">
            <span class="macro-label">Fat:</span>
            <span class="macro-value">{{ nutrition.fat }}g / {{ nutrition.fatGoal }}g</span>
          </div>
        </div>
        <button class="action-btn secondary" @click="logMeal">Log Meal</button>
      </div>

      <!-- Advanced Analytics (Silver Feature) -->
      <div class="content-card">
        <div class="card-header">
          <div class="card-title">📊 Advanced Analytics</div>
          <div class="new-badge">SILVER</div>
        </div>
        <div class="card-description">Detailed insights into your progress</div>
        <div class="analytics-preview">
          <div class="analytics-stat">
            <div class="stat-number">{{ analytics.weeklyImprovement }}%</div>
            <div class="stat-label">Weekly Improvement</div>
          </div>
          <div class="analytics-stat">
            <div class="stat-number">{{ analytics.consistency }}%</div>
            <div class="stat-label">Consistency Score</div>
          </div>
        </div>
        <button class="action-btn secondary" @click="viewAnalytics">View Full Report</button>
      </div>

      <!-- Monthly Challenge -->
      <div class="content-card">
        <div class="card-header">
          <div class="card-title">Monthly Challenge</div>
          <div class="card-meta">{{ monthlyChallenge.daysLeft }} days left</div>
        </div>
        <div class="card-description">{{ monthlyChallenge.description }}</div>
        <div class="challenge-progress">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: challengeProgress + '%' }"></div>
          </div>
          <div class="progress-text">
            {{ monthlyChallenge.completed }} / {{ monthlyChallenge.target }} completed
          </div>
        </div>
        <button class="action-btn secondary" @click="viewChallenge">View Details</button>
      </div>

      <!-- Locked Premium Features -->
      <div class="content-card locked-section">
        <div class="card-title mb-2">🏆 Premium Coaching</div>
        <div class="card-description">1-on-1 coaching sessions with certified trainers</div>
        <div class="unlock-overlay">
          <div class="unlock-icon">👑</div>
          <div class="unlock-text">Unlock at Gold Level</div>
          <div class="unlock-subtext">{{ goldXpNeeded }} XP to go!</div>
        </div>
      </div>
    </div>

    <!-- Meal Logging Modal -->
    <div v-if="showMealModal" class="modal-overlay" @click="closeMealModal">
      <div class="modal-content meal-modal" @click.stop>
        <h3>Log Your Meal</h3>
        <div class="meal-form">
          <div class="form-group">
            <label class="form-label">Meal Type</label>
            <select v-model="newMeal.type" class="form-input">
              <option value="breakfast">Breakfast</option>
              <option value="lunch">Lunch</option>
              <option value="dinner">Dinner</option>
              <option value="snack">Snack</option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="form-label">Food Item</label>
            <input v-model="newMeal.food" type="text" class="form-input" placeholder="e.g., Grilled Chicken Salad">
          </div>
          
          <div class="nutrition-inputs">
            <div class="input-group">
              <label class="form-label">Protein (g)</label>
              <input v-model.number="newMeal.protein" type="number" class="form-input" placeholder="25">
            </div>
            <div class="input-group">
              <label class="form-label">Carbs (g)</label>
              <input v-model.number="newMeal.carbs" type="number" class="form-input" placeholder="30">
            </div>
            <div class="input-group">
              <label class="form-label">Fat (g)</label>
              <input v-model.number="newMeal.fat" type="number" class="form-input" placeholder="15">
            </div>
          </div>
        </div>
        
        <div class="modal-actions">
          <button class="action-btn" @click="saveMeal">Log Meal</button>
          <button class="action-btn secondary" @click="closeMealModal">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'SilverDashboard',
  props: {
    userData: {
      type: Object,
      default: () => ({
        name: 'Katie',
        level: 'Silver',
        streak: 15,
        xp: 195
      })
    }
  },
  emits: ['page-change'],
  setup(props, { emit }) {
    const silverXp = ref(195)
    const goldRequirement = ref(300)
    const showMealModal = ref(false)

    const userInitial = computed(() => {
      return props.userData.name.charAt(0).toUpperCase()
    })

    const progressPercentage = computed(() => {
      return Math.round((silverXp.value / goldRequirement.value) * 100)
    })

    const goldXpNeeded = computed(() => {
      return goldRequirement.value - silverXp.value
    })

    const todayWorkout = ref({
      description: 'Strength training session',
      xp: 20
    })

    const nutrition = ref({
      protein: 65,
      proteinGoal: 120,
      carbs: 180,
      carbsGoal: 200,
      fat: 45,
      fatGoal: 60
    })

    const analytics = ref({
      weeklyImprovement: 12,
      consistency: 89
    })

    const monthlyChallenge = ref({
      description: 'Complete 20 workouts this month',
      completed: 14,
      target: 20,
      daysLeft: 8
    })

    const challengeProgress = computed(() => {
      return Math.round((monthlyChallenge.value.completed / monthlyChallenge.value.target) * 100)
    })

    const newMeal = ref({
      type: 'breakfast',
      food: '',
      protein: 0,
      carbs: 0,
      fat: 0
    })

    const startWorkout = () => {
      alert('Starting advanced strength training session! 💪')
    }

    const goToRecipes = () => {
      emit('page-change', 'recipe-library')
    }

    const logMeal = () => {
      showMealModal.value = true
    }

    const closeMealModal = () => {
      showMealModal.value = false
      resetMealForm()
    }

    const saveMeal = () => {
      if (!newMeal.value.food.trim()) {
        alert('Please enter a food item')
        return
      }

      // Update nutrition values
      nutrition.value.protein += newMeal.value.protein || 0
      nutrition.value.carbs += newMeal.value.carbs || 0
      nutrition.value.fat += newMeal.value.fat || 0

      alert(`Meal logged successfully! \n${newMeal.value.food} added to ${newMeal.value.type}`)
      closeMealModal()
    }

    const resetMealForm = () => {
      newMeal.value = {
        type: 'breakfast',
        food: '',
        protein: 0,
        carbs: 0,
        fat: 0
      }
    }

    const viewAnalytics = () => {
      alert('Analytics Feature: Detailed progress tracking, workout efficiency metrics, and personalized recommendations coming soon!')
    }

    const viewChallenge = () => {
      alert(`Monthly Challenge Progress:\n\n✅ Completed: ${monthlyChallenge.value.completed} workouts\n🎯 Target: ${monthlyChallenge.value.target} workouts\n📅 Days remaining: ${monthlyChallenge.value.daysLeft}\n\nKeep up the great work!`)
    }

    return {
      userInitial,
      silverXp,
      goldRequirement,
      progressPercentage,
      goldXpNeeded,
      todayWorkout,
      nutrition,
      analytics,
      monthlyChallenge,
      challengeProgress,
      showMealModal,
      newMeal,
      startWorkout,
      goToRecipes,
      logMeal,
      closeMealModal,
      saveMeal,
      viewAnalytics,
      viewChallenge
    }
  }
}
</script>

<style scoped>
/* Dashboard Header */
.dashboard-header {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 5px 15px rgba(0,0,0,0.08);
  margin-bottom: 2rem;
}

.user-profile {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.user-info-section {
  display: flex;
  align-items: center;
}

.user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  margin-right: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
}

.avatar-silver { 
  background: linear-gradient(135deg, #c0c0c0, #a8a8a8); 
}

.user-details h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.user-level {
  color: #6b7280;
  font-weight: 500;
}

.tier-badge {
  padding: 0.5rem 1rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  color: white;
}

.badge-silver { 
  background: linear-gradient(135deg, #c0c0c0, #a8a8a8); 
}

.progress-section {
  margin-top: 1rem;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.progress-label {
  font-weight: 600;
  color: #374151;
}

.progress-value {
  color: #6b7280;
  font-size: 0.9rem;
}

.progress-bar {
  height: 10px;
  background: #e5e7eb;
  border-radius: 5px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #059669);
  border-radius: 5px;
  transition: width 0.8s ease;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.content-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 5px 15px rgba(0,0,0,0.08);
  transition: transform 0.2s ease;
}

.content-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1e293b;
  flex: 1;
}

.card-meta {
  background: #f3f4f6;
  color: #6b7280;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.new-badge {
  background: #10b981;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 10px;
  font-size: 0.7rem;
  font-weight: 700;
}

.card-description {
  color: #6b7280;
  margin-bottom: 1rem;
  line-height: 1.4;
}

.action-btn {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 20px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease;
  width: 100%;
}

.action-btn:hover {
  transform: translateY(-1px);
}

.action-btn.secondary {
  background: #f3f4f6;
  color: #6b7280;
}

.action-btn.secondary:hover {
  background: #e5e7eb;
}

/* Nutrition Summary */
.nutrition-summary {
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 10px;
}

.macro-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.macro-label {
  font-weight: 600;
  color: #374151;
}

.macro-value {
  color: #6b7280;
}

/* Analytics Preview */
.analytics-preview {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
}

.analytics-stat {
  text-align: center;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 10px;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: #10b981;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.8rem;
  color: #6b7280;
}

/* Challenge Progress */
.challenge-progress {
  margin-bottom: 1rem;
}

.progress-text {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #6b7280;
  text-align: center;
}

/* Locked Content */
.locked-section {
  position: relative;
  opacity: 0.6;
}

.unlock-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 15px;
  color: white;
  text-align: center;
}

.unlock-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.unlock-text {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.unlock-subtext {
  font-size: 0.8rem;
  opacity: 0.8;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.modal-content {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  animation: slideUp 0.3s ease-out;
}

.meal-modal h3 {
  color: #1e293b;
  margin-bottom: 1.5rem;
  font-weight: 700;
  text-align: center;
}

.meal-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #4f46e5;
}

.nutrition-inputs {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.modal-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1.5rem;
}

.modal-actions .action-btn {
  width: auto;
  flex: 1;
}

/* Utility Classes */
.mb-2 { margin-bottom: 1rem; }

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { 
    opacity: 0; 
    transform: translateY(30px); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .user-profile {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .user-info-section {
    width: 100%;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

  .analytics-preview {
    grid-template-columns: 1fr;
  }

  .nutrition-inputs {
    grid-template-columns: 1fr;
  }

  .modal-actions {
    flex-direction: column;
  }
}
</style>