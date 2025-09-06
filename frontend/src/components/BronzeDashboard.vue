<!-- BronzeDashboard.vue -->
<template>
    <div class="bronze-dashboard">
      <!-- User Profile Header -->
      <div class="dashboard-header">
        <div class="user-profile">
          <div class="user-info-section">
            <div class="user-avatar avatar-bronze">{{ userInitial }}</div>
            <div class="user-details">
              <h2>{{ userData.name }}</h2>
              <div class="user-level">Bronze Level • Day {{ userData.streak }} Streak</div>
            </div>
          </div>
          <div class="tier-badge badge-bronze">Bronze</div>
        </div>
  
        <div class="progress-section">
          <div class="progress-header">
            <div class="progress-label">Progress to Silver</div>
            <div class="progress-value">{{ userData.xp }}/{{ userData.totalXpForNextLevel }} XP</div>
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
            <div class="card-meta">Day {{ currentDay }}</div>
          </div>
          <div class="card-description">{{ todayWorkout.description }} • Earn +{{ todayWorkout.xp }} XP</div>
          <button class="action-btn" @click="startWorkout">Start Workout</button>
        </div>
  
        <!-- Weekly Challenge -->
        <div class="content-card">
          <div class="card-header">
            <div class="card-title">Weekly Challenge</div>
            <div class="card-meta">{{ weeklyChallenge.timeLeft }} days</div>
          </div>
          <div class="card-description">{{ weeklyChallenge.description }}</div>
          <div class="text-success fw-600 mb-2">
            {{ weeklyChallenge.completed }}/{{ weeklyChallenge.total }} Complete
          </div>
          <button class="action-btn secondary" @click="viewProgress">View Progress</button>
        </div>
  
        <!-- Locked Recipe Library -->
        <div class="content-card locked-section">
          <div class="card-title mb-2">Recipe Library</div>
          <div class="card-description">Unlock healthy recipes at Silver level</div>
          <div class="unlock-overlay">
            <div class="unlock-icon">🔒</div>
            <div class="unlock-text">Unlock at Silver Level</div>
            <div class="unlock-subtext">{{ xpNeeded }} XP to go!</div>
          </div>
        </div>
  
        <!-- Achievements -->
        <div class="content-card">
          <div class="card-header">
            <div class="card-title">Recent Achievements</div>
            <div class="card-meta">New</div>
          </div>
          <div class="achievement-list">
            <div 
              v-for="achievement in recentAchievements" 
              :key="achievement.id"
              class="achievement-item"
            >
              <span class="achievement-icon">{{ achievement.icon }}</span>
              <div class="achievement-details">
                <div class="achievement-name">{{ achievement.name }}</div>
                <div class="achievement-desc">{{ achievement.description }}</div>
              </div>
              <div class="achievement-xp">+{{ achievement.xp }} XP</div>
            </div>
          </div>
        </div>
  
        <!-- Quick Stats -->
        <div class="content-card">
          <div class="card-title mb-2">Quick Stats</div>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-value">{{ stats.workoutsCompleted }}</div>
              <div class="stat-label">Workouts</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ stats.totalMinutes }}</div>
              <div class="stat-label">Minutes</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ stats.caloriesBurned }}</div>
              <div class="stat-label">Calories</div>
            </div>
          </div>
        </div>
  
        <!-- Tips & Motivation -->
        <div class="content-card">
          <div class="card-header">
            <div class="card-title">Daily Tip</div>
            <div class="card-meta">💡</div>
          </div>
          <div class="card-description">{{ dailyTip }}</div>
          <button class="action-btn secondary" @click="getNewTip">Get New Tip</button>
        </div>
      </div>
  
      <!-- Workout Modal -->
      <div v-if="showWorkoutModal" class="modal-overlay" @click="closeWorkoutModal">
        <div class="modal-content workout-modal" @click.stop>
          <h3>Starting Workout Session!</h3>
          <div class="workout-schedule">
            <div class="workout-item">
              <span class="workout-icon">🏃‍♀️</span>
              <span>10 min Warm-up</span>
            </div>
            <div class="workout-item">
              <span class="workout-icon">💪</span>
              <span>10 min Abs</span>
            </div>
            <div class="workout-item">
              <span class="workout-icon">🔥</span>
              <span>30 min HIIT</span>
            </div>
          </div>
          <p class="motivation-text">You've got this! 💪</p>
          <div class="modal-actions">
            <button class="action-btn" @click="proceedToWorkout">Let's Go!</button>
            <button class="action-btn secondary" @click="closeWorkoutModal">Maybe Later</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue'
  
  export default {
    name: 'BronzeDashboard',
    props: {
      userData: {
        type: Object,
        default: () => ({
          name: 'Katie',
          level: 'Bronze',
          streak: 5,
          xp: 48,
          totalXpForNextLevel: 150
        })
      }
    },
    emits: ['page-change'],
    setup(props, { emit }) {
      const showWorkoutModal = ref(false)
      const currentDay = ref(5)
  
      const userInitial = computed(() => {
        return props.userData.name.charAt(0).toUpperCase()
      })
  
      const progressPercentage = computed(() => {
        return Math.round((props.userData.xp / props.userData.totalXpForNextLevel) * 100)
      })
  
      const xpNeeded = computed(() => {
        return props.userData.totalXpForNextLevel - props.userData.xp
      })
  
      const todayWorkout = ref({
        description: '30-min HIIT session',
        xp: 15
      })
  
      const weeklyChallenge = ref({
        description: 'Complete 5 workouts this week',
        completed: 4,
        total: 5,
        timeLeft: 5
      })
  
      const recentAchievements = ref([
        {
          id: 1,
          icon: '🏆',
          name: 'First Week',
          description: 'Completed your first week!',
          xp: 25
        },
        {
          id: 2,
          icon: '🔥',
          name: 'Streak Master',
          description: '5-day workout streak',
          xp: 15
        }
      ])
  
      const stats = ref({
        workoutsCompleted: 12,
        totalMinutes: 360,
        caloriesBurned: 2450
      })
  
      const tips = [
        "Stay hydrated! Drink water before, during, and after your workout.",
        "Focus on proper form rather than speed to prevent injuries.",
        "Get adequate sleep - your muscles grow during rest, not just exercise.",
        "Don't forget to warm up before intense exercises.",
        "Listen to your body - rest days are just as important as workout days."
      ]
  
      const dailyTip = ref(tips[0])
  
      const startWorkout = () => {
        showWorkoutModal.value = true
      }
  
      const closeWorkoutModal = () => {
        showWorkoutModal.value = false
      }
  
      const proceedToWorkout = () => {
        closeWorkoutModal()
        emit('page-change', 'workout-program')
      }
  
      const viewProgress = () => {
        alert('Weekly progress: 4/5 workouts completed. Keep going!')
      }
  
      const getNewTip = () => {
        const randomIndex = Math.floor(Math.random() * tips.length)
        dailyTip.value = tips[randomIndex]
      }
  
      return {
        userInitial,
        progressPercentage,
        xpNeeded,
        currentDay,
        todayWorkout,
        weeklyChallenge,
        recentAchievements,
        stats,
        dailyTip,
        showWorkoutModal,
        startWorkout,
        closeWorkoutModal,
        proceedToWorkout,
        viewProgress,
        getNewTip
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
  
  .avatar-bronze { 
    background: linear-gradient(135deg, #cd7f32, #b8860b); 
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
  
  .badge-bronze { 
    background: linear-gradient(135deg, #cd7f32, #b8860b); 
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
  
  /* Achievements */
  .achievement-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .achievement-item {
    display: flex;
    align-items: center;
    padding: 0.75rem;
    background: #f8fafc;
    border-radius: 10px;
    transition: background 0.2s ease;
  }
  
  .achievement-item:hover {
    background: #f1f5f9;
  }
  
  .achievement-icon {
    font-size: 1.5rem;
    margin-right: 0.75rem;
  }
  
  .achievement-details {
    flex: 1;
  }
  
  .achievement-name {
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 0.25rem;
  }
  
  .achievement-desc {
    font-size: 0.8rem;
    color: #6b7280;
  }
  
  .achievement-xp {
    background: #10b981;
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 10px;
    font-size: 0.8rem;
    font-weight: 600;
  }
  
  /* Stats Grid */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    text-align: center;
  }
  
  .stat-item {
    padding: 1rem 0;
  }
  
  .stat-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 0.25rem;
  }
  
  .stat-label {
    font-size: 0.8rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.5px;
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
  
  .workout-modal h3 {
    color: #1e293b;
    margin-bottom: 1.5rem;
    font-weight: 700;
  }
  
  .workout-schedule {
    margin: 1.5rem 0;
    text-align: left;
  }
  
  .workout-item {
    display: flex;
    align-items: center;
    padding: 0.75rem;
    margin-bottom: 0.5rem;
    background: #f8fafc;
    border-radius: 10px;
  }
  
  .workout-icon {
    margin-right: 0.75rem;
    font-size: 1.2rem;
  }
  
  .motivation-text {
    color: #10b981;
    font-weight: 600;
    margin: 1rem 0;
    font-size: 1.1rem;
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
  .text-center { text-align: center; }
  .mb-1 { margin-bottom: 0.5rem; }
  .mb-2 { margin-bottom: 1rem; }
  .mb-3 { margin-bottom: 1.5rem; }
  .mt-2 { margin-top: 1rem; }
  .text-success { color: #10b981; }
  .text-muted { color: #6b7280; }
  .fw-600 { font-weight: 600; }
  .fw-700 { font-weight: 700; }
  
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
  
    .stats-grid {
      grid-template-columns: repeat(3, 1fr);
      gap: 0.5rem;
    }
  
    .modal-actions {
      flex-direction: column;
    }
  }
  @media (max-width: 768px) {
    .user-profile { flex-direction: column; align-items: flex-start; gap: 1rem; }
    .user-info-section { width: 100%; }
    .content-grid { grid-template-columns: 1fr; }
    .stats-grid { grid-template-columns: repeat(3, 1fr); gap: 0.5rem; }
    .modal-actions { flex-direction: column; }
  }
</style>