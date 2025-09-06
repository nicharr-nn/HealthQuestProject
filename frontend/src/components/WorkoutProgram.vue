<!-- WorkoutProgram.vue -->
<template>
    <div class="workout-program">
      <div class="page-header">
        <h1 class="page-title">Maintain Health</h1>
        <p class="page-subtitle">by CAT (Coach) • 30 days • Bronze Level</p>
      </div>
  
      <!-- Program Progress -->
      <div class="dashboard-header">
        <div class="program-info">
          <div class="progress-info">
            <div class="progress-label">Program Progress</div>
            <div class="text-muted">Day {{ currentDay }} of {{ totalDays }}</div>
          </div>
          <div class="card-meta">{{ currentDay }}/{{ totalDays }} Days</div>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: programProgress + '%' }"></div>
        </div>
      </div>
  
      <!-- Day Selector -->
      <div class="day-selector">
        <div 
          v-for="day in visibleDays" 
          :key="day"
          class="day-pill" 
          :class="{ 
            active: selectedDay === day,
            completed: day < currentDay,
            locked: day > currentDay
          }"
          @click="selectDay(day)"
        >
          <span v-if="day < currentDay" class="day-status">✓</span>
          <span v-else-if="day > currentDay" class="day-status">🔒</span>
          Day {{ day }}
        </div>
      </div>
  
      <!-- Workout Content -->
      <div class="content-grid">
        <div 
          v-for="exercise in todayExercises" 
          :key="exercise.id"
          class="content-card exercise-card"
          :class="{ completed: exercise.completed, locked: exercise.locked }"
        >
          <div class="exercise-header">
            <div class="exercise-icon">{{ exercise.icon }}</div>
            <div class="exercise-info">
              <div class="card-title">{{ exercise.title }}</div>
              <div class="exercise-duration">{{ exercise.duration }}</div>
            </div>
            <div v-if="exercise.completed" class="completion-badge">✓</div>
          </div>
          
          <div class="card-description">{{ exercise.description }}</div>
          
          <div v-if="exercise.equipment" class="equipment-list">
            <div class="equipment-label">Equipment needed:</div>
            <div class="equipment-items">
              <span 
                v-for="item in exercise.equipment" 
                :key="item"
                class="equipment-tag"
              >
                {{ item }}
              </span>
            </div>
          </div>
          
          <div v-if="exercise.muscles" class="muscles-list">
            <div class="muscles-label">Target muscles:</div>
            <div class="muscles-items">
              <span 
                v-for="muscle in exercise.muscles" 
                :key="muscle"
                class="muscle-tag"
              >
                {{ muscle }}
              </span>
            </div>
          </div>
          
          <div class="exercise-actions">
            <button 
              v-if="!exercise.locked"
              class="action-btn" 
              :class="{ secondary: exercise.completed }"
              @click="startExercise(exercise)"
            >
              <span v-if="exercise.completed">✓ Completed</span>
              <span v-else-if="exercise.type === 'main'">▶ Start Now (+{{ exercise.xp }} XP)</span>
              <span v-else>▶ Watch Video</span>
            </button>
            <button 
              v-else
              class="action-btn locked-btn"
              disabled
            >
              🔒 Complete previous exercises
            </button>
          </div>
        </div>
      </div>
  
      <!-- Exercise Modal -->
      <div v-if="showExerciseModal" class="modal-overlay" @click="closeExerciseModal">
        <div class="modal-content exercise-modal" @click.stop>
          <div class="exercise-modal-header">
            <h3>{{ selectedExercise?.title }}</h3>
            <button class="close-btn" @click="closeExerciseModal">×</button>
          </div>
          
          <div class="exercise-details">
            <div class="detail-row">
              <span class="detail-label">Duration:</span>
              <span class="detail-value">{{ selectedExercise?.duration }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Difficulty:</span>
              <span class="detail-value">{{ selectedExercise?.difficulty }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">XP Reward:</span>
              <span class="detail-value">+{{ selectedExercise?.xp }} XP</span>
            </div>
          </div>
          
          <div class="exercise-instructions">
            <h4>Instructions:</h4>
            <ol>
              <li v-for="instruction in selectedExercise?.instructions" :key="instruction">
                {{ instruction }}
              </li>
            </ol>
          </div>
          
          <div v-if="!exerciseInProgress" class="modal-actions">
            <button class="action-btn" @click="beginExercise">Begin Exercise</button>
            <button class="action-btn secondary" @click="closeExerciseModal">Maybe Later</button>
          </div>
          
          <div v-else class="exercise-timer">
            <div class="timer-display">{{ formatTime(timeRemaining) }}</div>
            <div class="timer-progress">
              <div class="timer-fill" :style="{ width: timerProgress + '%' }"></div>
            </div>
            <div class="timer-controls">
              <button class="action-btn secondary" @click="pauseExercise">
                {{ isPaused ? '▶ Resume' : '⏸ Pause' }}
              </button>
              <button class="action-btn" @click="completeExercise">Complete Exercise</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted, onUnmounted } from 'vue'
  
  export default {
    name: 'WorkoutProgram',
    setup() {
      const currentDay = ref(5)
      const totalDays = ref(30)
      const selectedDay = ref(5)
      const showExerciseModal = ref(false)
      const selectedExercise = ref(null)
      const exerciseInProgress = ref(false)
      const timeRemaining = ref(0)
      const totalTime = ref(0)
      const isPaused = ref(false)
      const timer = ref(null)
  
      const programProgress = computed(() => {
        return Math.round((currentDay.value / totalDays.value) * 100)
      })
  
      const visibleDays = computed(() => {
        const start = Math.max(1, currentDay.value - 3)
        const end = Math.min(totalDays.value, currentDay.value + 3)
        const days = []
        for (let i = start; i <= end; i++) {
          days.push(i)
        }
        return days
      })
  
      const timerProgress = computed(() => {
        if (totalTime.value === 0) return 0
        return ((totalTime.value - timeRemaining.value) / totalTime.value) * 100
      })
  
      const exercises = ref({
        5: [
          {
            id: 1,
            title: '10 min Warm-up',
            duration: '10 minutes',
            description: 'Dynamic stretches and mobility exercises',
            icon: '🏃‍♀️',
            type: 'warmup',
            xp: 5,
            completed: true,
            locked: false,
            difficulty: 'Easy',
            equipment: ['None'],
            muscles: ['Full body'],
            instructions: [
              'Start with light marching in place for 2 minutes',
              'Perform arm circles - 30 seconds each direction',
              'Do leg swings - 30 seconds each leg',
              'Hip circles - 30 seconds each direction',
              'Light jumping jacks for 2 minutes',
              'Cool down with gentle stretching'
            ]
          },
          {
            id: 2,
            title: '10 min Abs',
            duration: '10 minutes',
            description: 'Core strengthening and stability work',
            icon: '💪',
            type: 'strength',
            xp: 10,
            completed: true,
            locked: false,
            difficulty: 'Medium',
            equipment: ['Yoga mat'],
            muscles: ['Core', 'Abs', 'Obliques'],
            instructions: [
              'Plank hold - 3 sets of 30 seconds',
              'Bicycle crunches - 3 sets of 20 each side',
              'Russian twists - 3 sets of 30',
              'Mountain climbers - 3 sets of 20',
              'Dead bug - 3 sets of 10 each side',
              'Cool down with gentle spinal twists'
            ]
          },
          {
            id: 3,
            title: '30 min HIIT',
            duration: '30 minutes',
            description: 'High intensity interval training session',
            icon: '🔥',
            type: 'main',
            xp: 15,
            completed: false,
            locked: false,
            difficulty: 'Hard',
            equipment: ['None', 'Optional: dumbbells'],
            muscles: ['Full body', 'Cardio'],
            instructions: [
              'Warm-up: 5 minutes light movement',
              'Round 1: Burpees - 45 seconds work, 15 seconds rest',
              'Round 2: Jump squats - 45 seconds work, 15 seconds rest',
              'Round 3: Push-ups - 45 seconds work, 15 seconds rest',
              'Round 4: High knees - 45 seconds work, 15 seconds rest',
              'Repeat circuit 4 times',
              'Cool-down: 5 minutes stretching'
            ]
          }
        ]
      })
  
      const todayExercises = computed(() => {
        return exercises.value[selectedDay.value] || []
      })
  
      const selectDay = (day) => {
        if (day <= currentDay.value) {
          selectedDay.value = day
        }
      }
  
      const startExercise = (exercise) => {
        selectedExercise.value = exercise
        showExerciseModal.value = true
      }
  
      const closeExerciseModal = () => {
        showExerciseModal.value = false
        selectedExercise.value = null
        exerciseInProgress.value = false
        if (timer.value) {
          clearInterval(timer.value)
          timer.value = null
        }
      }
  
      const beginExercise = () => {
        exerciseInProgress.value = true
        const duration = parseInt(selectedExercise.value.duration)
        timeRemaining.value = duration * 60 // Convert to seconds
        totalTime.value = duration * 60
        isPaused.value = false
        
        timer.value = setInterval(() => {
          if (!isPaused.value && timeRemaining.value > 0) {
            timeRemaining.value--
          }
          if (timeRemaining.value === 0) {
            completeExercise()
          }
        }, 1000)
      }
  
      const pauseExercise = () => {
        isPaused.value = !isPaused.value
      }
  
      const completeExercise = () => {
        if (timer.value) {
          clearInterval(timer.value)
          timer.value = null
        }
        
        // Mark exercise as completed
        const exercise = exercises.value[selectedDay.value].find(e => e.id === selectedExercise.value.id)
        if (exercise) {
          exercise.completed = true
          
          // Unlock next exercise if this was the blocking one
          const currentIndex = exercises.value[selectedDay.value].findIndex(e => e.id === selectedExercise.value.id)
          if (currentIndex < exercises.value[selectedDay.value].length - 1) {
            exercises.value[selectedDay.value][currentIndex + 1].locked = false
          }
        }
        
        alert(`Exercise completed! You earned +${selectedExercise.value.xp} XP!`)
        closeExerciseModal()
      }
  
      const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60)
        const secs = seconds % 60
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
      }
  
      onUnmounted(() => {
        if (timer.value) {
          clearInterval(timer.value)
        }
      })
  
      return {
        currentDay,
        totalDays,
        selectedDay,
        programProgress,
        visibleDays,
        todayExercises,
        showExerciseModal,
        selectedExercise,
        exerciseInProgress,
        timeRemaining,
        timerProgress,
        isPaused,
        selectDay,
        startExercise,
        closeExerciseModal,
        beginExercise,
        pauseExercise,
        completeExercise,
        formatTime
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
    color: #1e293b;
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
  
  /* Dashboard Header */
  .dashboard-header {
    background: white;
    border-radius: 15px;
    padding: 1.5rem;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    margin-bottom: 2rem;
  }
  
  .program-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }
  
  .progress-info {
    flex: 1;
  }
  
  .progress-label {
    font-weight: 600;
    color: #374151;
  }
  
  .text-muted {
    color: #6b7280;
    font-size: 0.9rem;
  }
  
  .card-meta {
    background: #f3f4f6;
    color: #6b7280;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 600;
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
  
  /* Day Selector */
  .day-selector {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }
  
  .day-pill {
    min-width: 80px;
    padding: 0.75rem 1rem;
    background: #f3f4f6;
    color: #6b7280;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 600;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
    position: relative;
  }
  
  .day-pill.active {
    background: #4f46e5;
    color: white;
  }
  
  .day-pill.completed {
    background: #10b981;
    color: white;
  }
  
  .day-pill.locked {
    background: #e5e7eb;
    color: #9ca3af;
    cursor: not-allowed;
  }
  
  .day-pill:not(.locked):hover {
    transform: translateY(-1px);
  }
  
  .day-status {
    margin-right: 0.25rem;
  }
  
  /* Content Grid */
  .content-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 1.5rem;
  }
  
  .content-card {
    background: white;
    border-radius: 15px;
    padding: 1.5rem;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;
  }
  
  .content-card:hover:not(.locked) {
    transform: translateY(-2px);
  }
  
  .exercise-card.completed {
    border-left: 4px solid #10b981;
  }
  
  .exercise-card.locked {
    opacity: 0.6;
    background: #f8fafc;
  }
  
  .exercise-header {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
  }
  
  .exercise-icon {
    font-size: 2rem;
    margin-right: 1rem;
  }
  
  .exercise-info {
    flex: 1;
  }
  
  .card-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 0.25rem;
  }
  
  .exercise-duration {
    color: #6b7280;
    font-size: 0.9rem;
    font-weight: 500;
  }
  
  .completion-badge {
    width: 30px;
    height: 30px;
    background: #10b981;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
  }
  
  .card-description {
    color: #6b7280;
    margin-bottom: 1rem;
    line-height: 1.4;
  }
  
  .equipment-list, .muscles-list {
    margin-bottom: 1rem;
  }
  
  .equipment-label, .muscles-label {
    font-weight: 600;
    color: #374151;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
  }
  
  .equipment-items, .muscles-items {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .equipment-tag, .muscle-tag {
    background: #f1f5f9;
    color: #475569;
    padding: 0.25rem 0.5rem;
    border-radius: 10px;
    font-size: 0.8rem;
    font-weight: 500;
  }
  
  .exercise-actions {
    margin-top: 1rem;
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
  
  .action-btn:hover:not(:disabled) {
    transform: translateY(-1px);
  }
  
  .action-btn.secondary {
    background: #f3f4f6;
    color: #6b7280;
  }
  
  .action-btn.secondary:hover {
    background: #e5e7eb;
  }
  
  .locked-btn {
    background: #e5e7eb !important;
    color: #9ca3af !important;
    cursor: not-allowed !important;
  }
  
  .locked-btn:hover {
    transform: none !important;
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
    max-width: 600px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
    animation: slideUp 0.3s ease-out;
  }
  
  .exercise-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }
  
  .exercise-modal-header h3 {
    color: #1e293b;
    font-weight: 700;
    margin: 0;
  }
  
  .close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #6b7280;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background 0.2s ease;
  }
  
  .close-btn:hover {
    background: #f3f4f6;
  }
  
  .exercise-details {
    margin-bottom: 1.5rem;
  }
  
  .detail-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid #f1f5f9;
  }
  
  .detail-label {
    font-weight: 600;
    color: #374151;
  }
  
  .detail-value {
    color: #6b7280;
  }
  
  .exercise-instructions {
    margin-bottom: 1.5rem;
  }
  
  .exercise-instructions h4 {
    color: #1e293b;
    margin-bottom: 1rem;
    font-weight: 600;
  }
  
  .exercise-instructions ol {
    padding-left: 1.5rem;
    color: #6b7280;
    line-height: 1.6;
  }
  
  .exercise-instructions li {
    margin-bottom: 0.5rem;
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
  
  /* Exercise Timer */
  .exercise-timer {
    text-align: center;
    padding: 1rem 0;
  }
  
  .timer-display {
    font-size: 3rem;
    font-weight: 700;
    color: #10b981;
    margin-bottom: 1rem;
    font-family: monospace;
  }
  
  .timer-progress {
    width: 100%;
    height: 8px;
    background: #e5e7eb;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 1.5rem;
  }
  
  .timer-fill {
    height: 100%;
    background: linear-gradient(90deg, #10b981, #059669);
    border-radius: 4px;
    transition: width 0.3s ease;
  }
  
  .timer-controls {
    display: flex;
    gap: 0.5rem;
  }
  
  .timer-controls .action-btn {
    flex: 1;
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
  
    .content-grid {
      grid-template-columns: 1fr;
    }
  
    .program-info {
      flex-direction: column;
      gap: 0.5rem;
      align-items: flex-start;
    }
  
    .day-selector {
      justify-content: flex-start;
    }
  
    .exercise-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }
  
    .completion-badge {
      align-self: flex-end;
    }
  
    .modal-actions {
      flex-direction: column;
    }
  
    .timer-controls {
      flex-direction: column;
    }
  }
  </style>