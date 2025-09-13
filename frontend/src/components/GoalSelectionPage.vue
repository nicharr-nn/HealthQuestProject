<!-- GoalSelectionPage.vue -->
<template>
  <div class="goal-selection-page">
    <div class="page-header">
      <h1 class="page-title">Select Goal</h1>
      <p class="page-subtitle">To Start Your Journey</p>
    </div>

    <div class="goal-grid">
      <div 
        v-for="goal in goals" 
        :key="goal.id"
        class="goal-card" 
        :class="goal.type"
        @click="selectGoal(goal)"
      >
        <div class="goal-icon">{{ goal.icon }}</div>
        <h3 class="goal-title">{{ goal.title }}</h3>
        <p class="goal-description">{{ goal.description }}</p>
        
        <div class="goal-features">
          <span 
            v-for="feature in goal.features" 
            :key="feature"
            class="feature-tag"
          >
            {{ feature }}
          </span>
        </div>
        
        <div class="goal-details">
          <div 
            v-for="detail in goal.details" 
            :key="detail"
            class="detail-item"
          >
            {{ detail }}
          </div>
        </div>
        
        <button class="select-btn">Click to Select</button>
      </div>
    </div>

    <!-- Success Modal -->
    <div v-if="showSuccessModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="success-icon">✨</div>
        <h2>Goal Selected!</h2>
        <p>You selected: <strong>{{ selectedGoal?.title }}</strong></p>
        <p class="redirect-text">Redirecting to dashboard...</p>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressWidth + '%' }"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'GoalSelectionPage',
  emits: ['goal-selected'],
  setup(props, { emit }) {
    const selectedGoal = ref(null)
    const showSuccessModal = ref(false)
    const progressWidth = ref(0)

    const goals = ref([
      {
        id: 'fitness',
        type: 'fitness',
        icon: '🏃‍♂️',
        title: 'Fitness Journey',
        description: 'Build strength, boost cardio, and feel athletic again.',
        features: ['8 weeks', 'Strength + Cardio', 'Beginner'],
        details: [
          '3-day split plan',
          'Video-guided moves',
          'Weekly progress check'
        ]
      },
      {
        id: 'nutrition',
        type: 'nutrition',
        icon: '🥗',
        title: 'Nutrition Focus',
        description: 'Clean eating plan with macro guidance and easy recipes.',
        features: ['6 weeks', 'Balanced macros', 'All levels'],
        details: [
          'Personalized portions',
          'Grocery list',
          'Thai-friendly recipes'
        ]
      },
      {
        id: 'wellness',
        type: 'wellness',
        icon: '🧘‍♀️',
        title: 'Wellness Balance',
        description: 'Mindfulness, mobility, and light movement for balance.',
        features: ['4 weeks', 'Mind & Body', 'Gentle'],
        details: [
          '10-min daily flow',
          'Breathwork guides',
          'Sleep routine'
        ]
      }
    ])

    const selectGoal = (goal) => {
      selectedGoal.value = goal
      showSuccessModal.value = true
      
      // Animate progress bar
      let progress = 0
      const interval = setInterval(() => {
        progress += 2
        progressWidth.value = progress
        
        if (progress >= 100) {
          clearInterval(interval)
          setTimeout(() => {
            emit('goal-selected', goal)
            closeModal()
          }, 500)
        }
      }, 30)
    }

    const closeModal = () => {
      showSuccessModal.value = false
      progressWidth.value = 0
    }

    return {
      goals,
      selectedGoal,
      showSuccessModal,
      progressWidth,
      selectGoal,
      closeModal
    }
  }
}
</script>

<style scoped>
/* Page Header */
.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 3rem;
  font-weight: 900;
  color: #5a4633;
  text-transform: uppercase;
  letter-spacing: -2px;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  font-size: 1.2rem;
  color: #64748b;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Goal Grid */
.goal-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.goal-card {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.goal-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  border-radius: 20px 20px 0 0;
}

.goal-card.fitness::before { background: #B8D7DF; }
.goal-card.nutrition::before { background: #EDB6B6; }
.goal-card.wellness::before { background: #DED8B4; }

.goal-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

.goal-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin: 0 auto 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: white;
  font-weight: bold;
}

.goal-card.fitness .goal-icon { background: linear-gradient(135deg,#B8D7DF); }
.goal-card.nutrition .goal-icon { background: linear-gradient(135deg, #EDB6B6); }
.goal-card.wellness .goal-icon { background: linear-gradient(135deg, #DED8B4); }

.goal-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: -1px;
}

.goal-description {
  color: #64748b;
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.goal-features {
  display: flex;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.feature-tag {
  background: #f1f5f9;
  color: #475569;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
}

.goal-details {
  text-align: left;
  margin-bottom: 2rem;
}

.detail-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  color: #64748b;
  font-size: 0.9rem;
}

.detail-item::before {
  content: '•';
  color: #10b981;
  font-weight: bold;
  width: 1em;
  margin-right: 0.5rem;
}

.select-btn {
  background: linear-gradient(135deg, #609da1);
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease;
  width: 100%;
  font-size: 1rem;
}

.select-btn:hover {
  transform: translateY(-2px);
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
  text-align: center;
  max-width: 400px;
  width: 90%;
  animation: slideUp 0.3s ease-out;
}

.success-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.modal-content h2 {
  color: #1e293b;
  margin-bottom: 1rem;
  font-weight: 700;
}

.modal-content p {
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.redirect-text {
  color: #10b981;
  font-weight: 600;
  margin: 1rem 0;
}

.progress-bar {
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
  margin-top: 1rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #059669);
  border-radius: 3px;
  transition: width 0.3s ease;
}

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
  .page-title {
    font-size: 2rem;
  }

  .goal-grid {
    grid-template-columns: 1fr;
  }

  .modal-content {
    margin: 1rem;
    width: calc(100% - 2rem);
  }
}
</style>