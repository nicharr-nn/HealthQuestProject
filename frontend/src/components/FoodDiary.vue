<template>
  <div class="food-diary">
    <button class="back-btn" @click="emit('back-to-members')">
      ← Back to Members
    </button>

    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">{{ memberName }}'s Food Diary</h1>
        <p class="page-subtitle">Review and provide feedback on member's nutrition</p>
        <div class="member-id-badge">Member ID: {{ memberId }}</div>
      </div>
    </div>

    <!-- Date Filter -->
    <div class="date-filter">
      <button class="date-btn" @click="changeDate(-1)">← Previous Day</button>
      <div class="current-date">{{ formatDisplayDate(currentDate) }}</div>
      <button class="date-btn" @click="changeDate(1)" :disabled="isToday">Next Day →</button>
    </div>

    <!-- Food Entries -->
    <div class="food-entries">
      <div v-if="foodEntries.length === 0" class="empty-state">
        <div class="empty-icon">🍽️</div>
        <div class="empty-title">No food entries for this day</div>
        <div class="empty-message">
          The member hasn't logged any meals for {{ formatDisplayDate(currentDate) }}.
        </div>
      </div>

      <div v-else class="entries-grid">
        <div
          v-for="entry in foodEntries"
          :key="entry.id"
          class="food-entry-card"
        >
          <!-- Entry Header -->
          <div class="entry-header">
            <div class="meal-type" :class="entry.mealType.toLowerCase()">
              {{ entry.mealType }}
            </div>
            <div class="entry-time">{{ formatTime(entry.timestamp) }}</div>
          </div>

          <!-- Food Image -->
          <div v-if="entry.imageUrl" class="food-image-container">
            <img :src="entry.imageUrl" :alt="entry.foodName" class="food-image" />
          </div>

          <!-- Food Details -->
          <div class="food-details">
            <div class="food-name">{{ entry.foodName }}</div>
            <div v-if="entry.description" class="food-description">
              {{ entry.description }}
            </div>
          </div>

          <!-- Nutrition Info -->
          <div class="nutrition-info">
            <div class="nutrition-item">
              <span class="nutrition-label">Calories:</span>
              <span class="nutrition-value">{{ entry.calories }} kcal</span>
            </div>
            <div class="nutrition-item">
              <span class="nutrition-label">Protein:</span>
              <span class="nutrition-value">{{ entry.protein }}g</span>
            </div>
            <div class="nutrition-item">
              <span class="nutrition-label">Carbs:</span>
              <span class="nutrition-value">{{ entry.carbs }}g</span>
            </div>
            <div class="nutrition-item">
              <span class="nutrition-label">Fat:</span>
              <span class="nutrition-value">{{ entry.fats }}g</span>
            </div>
          </div>

          <!-- Coach Comments -->
          <div class="comments-section">
            <div class="comments-header">
              <span class="comments-title">Coach Comments</span>
              <button class="btn-add-comment" @click="openCommentDialog(entry.id)">
                + Add Comment
              </button>
            </div>

            <div v-if="entry.coachComments && entry.coachComments.length > 0" class="comments-list">
              <div
                v-for="comment in entry.coachComments"
                :key="comment.id"
                class="comment-item"
              >
                <div class="comment-header">
                  <span class="comment-author">You</span>
                  <span class="comment-time">{{ formatTime(comment.timestamp) }}</span>
                </div>
                <div class="comment-text">{{ comment.text }}</div>
              </div>
            </div>

            <div v-else class="no-comments">
              No comments yet. Add feedback to help your member!
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Comment Dialog -->
    <div v-if="showCommentDialog" class="modal-overlay" @click="closeCommentDialog">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">Add Coach Comment</h3>
          <button class="modal-close" @click="closeCommentDialog">×</button>
        </div>
        <div class="modal-body">
          <textarea
            v-model="newComment"
            class="comment-textarea"
            rows="5"
            placeholder="Provide feedback on this meal (e.g., nutritional advice, portion suggestions, alternatives, encouragement...)"
          />
        </div>
        <div class="modal-footer">
          <button class="btn ghost" @click="closeCommentDialog">Cancel</button>
          <button class="btn primary" @click="addComment" :disabled="!newComment.trim()">
            Post Comment
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  memberId: string
  memberName: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'back-to-members'): void
}>()

interface CoachComment {
  id: string
  text: string
  timestamp: Date
}

interface FoodEntry {
  id: string
  mealType: 'Breakfast' | 'Lunch' | 'Dinner' | 'Snack'
  foodName: string
  description?: string
  imageUrl?: string
  calories: number
  protein: number
  carbs: number
  fats: number
  timestamp: Date
  coachComments?: CoachComment[]
}

const currentDate = ref(new Date())
const showCommentDialog = ref(false)
const selectedEntryId = ref<string | null>(null)
const newComment = ref('')

// Sample data - in real app this would come from API
const foodEntries = ref<FoodEntry[]>([
  {
    id: 'entry_001',
    mealType: 'Breakfast',
    foodName: 'Oatmeal with Berries',
    description: 'Steel-cut oats with mixed berries and honey',
    calories: 320,
    protein: 12,
    carbs: 58,
    fats: 6,
    timestamp: new Date(currentDate.value.setHours(8, 30)),
    coachComments: [
      {
        id: 'comment_001',
        text: 'Great choice! The berries add good antioxidants. Consider adding some nuts for extra protein.',
        timestamp: new Date(currentDate.value.setHours(10, 15))
      }
    ]
  },
  {
    id: 'entry_002',
    mealType: 'Lunch',
    foodName: 'Grilled Chicken Salad',
    description: 'Mixed greens, grilled chicken breast, cherry tomatoes, cucumber, olive oil dressing',
    calories: 425,
    protein: 38,
    carbs: 22,
    fats: 18,
    timestamp: new Date(currentDate.value.setHours(12, 45)),
    coachComments: []
  },
  {
    id: 'entry_003',
    mealType: 'Snack',
    foodName: 'Protein Shake',
    description: 'Whey protein with almond milk and banana',
    calories: 280,
    protein: 30,
    carbs: 25,
    fats: 8,
    timestamp: new Date(currentDate.value.setHours(15, 30)),
    coachComments: []
  },
  {
    id: 'entry_004',
    mealType: 'Dinner',
    foodName: 'Salmon with Sweet Potato',
    description: 'Baked salmon fillet with roasted sweet potato and steamed broccoli',
    calories: 580,
    protein: 42,
    carbs: 45,
    fats: 22,
    timestamp: new Date(currentDate.value.setHours(19, 0)),
    coachComments: []
  }
])

const isToday = computed(() => {
  const today = new Date()
  return currentDate.value.toDateString() === today.toDateString()
})

function changeDate(days: number) {
  const newDate = new Date(currentDate.value)
  newDate.setDate(newDate.getDate() + days)
  currentDate.value = newDate
  // In real app: fetch food entries for new date
}

function formatDisplayDate(date: Date): string {
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)

  if (date.toDateString() === today.toDateString()) return 'Today'
  if (date.toDateString() === yesterday.toDateString()) return 'Yesterday'

  return date.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

function formatTime(date: Date): string {
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

function openCommentDialog(entryId: string) {
  selectedEntryId.value = entryId
  showCommentDialog.value = true
  newComment.value = ''
}

function closeCommentDialog() {
  showCommentDialog.value = false
  selectedEntryId.value = null
  newComment.value = ''
}

function addComment() {
  if (!newComment.value.trim() || !selectedEntryId.value) return

  const entry = foodEntries.value.find(e => e.id === selectedEntryId.value)
  if (entry) {
    if (!entry.coachComments) {
      entry.coachComments = []
    }
    entry.coachComments.push({
      id: `comment_${Date.now()}`,
      text: newComment.value.trim(),
      timestamp: new Date()
    })

    // In real app: POST comment to API
    alert('Comment added successfully!')
  }

  closeCommentDialog()
}
</script>

<style scoped>
.food-diary {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.back-btn {
  background: transparent;
  border: none;
  color: #3b82f6;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  padding: 8px 12px;
  margin-bottom: 16px;
  border-radius: 8px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 4px;
  width: fit-content;
}

.back-btn:hover {
  background: #eff6ff;
  color: #2563eb;
}

.page-header {
  margin-bottom: 24px;
}

.header-content {
  flex: 1;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 8px 0;
}

.page-subtitle {
  color: #6b7280;
  font-size: 16px;
  margin: 0 0 12px 0;
}

.member-id-badge {
  display: inline-block;
  padding: 6px 12px;
  background: #eff6ff;
  border: 1px solid #3b82f6;
  border-radius: 6px;
  font-size: 13px;
  color: #1e40af;
  font-weight: 600;
  font-family: monospace;
}

.date-filter {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 24px;
  padding: 16px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.date-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.date-btn:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-1px);
}

.date-btn:disabled {
  background: #d1d5db;
  cursor: not-allowed;
}

.current-date {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  min-width: 250px;
  text-align: center;
}

.food-entries {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.empty-state {
  text-align: center;
  padding: 64px 24px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-title {
  font-size: 20px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.empty-message {
  color: #6b7280;
  line-height: 1.5;
}

.entries-grid {
  display: grid;
  gap: 20px;
}

.food-entry-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  background: #fafafa;
  transition: all 0.2s ease;
}

.food-entry-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59,130,246,0.1);
}

.entry-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.meal-type {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
}

.meal-type.breakfast {
  background: #fef3c7;
  color: #92400e;
}

.meal-type.lunch {
  background: #d1fae5;
  color: #065f46;
}

.meal-type.dinner {
  background: #dbeafe;
  color: #1e40af;
}

.meal-type.snack {
  background: #ede9fe;
  color: #5b21b6;
}

.entry-time {
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
}

.food-image-container {
  margin-bottom: 16px;
  border-radius: 8px;
  overflow: hidden;
}

.food-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.food-details {
  margin-bottom: 16px;
}

.food-name {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 8px;
}

.food-description {
  color: #6b7280;
  line-height: 1.5;
}

.nutrition-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
  padding: 12px;
  background: #fff;
  border-radius: 8px;
}

.nutrition-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.nutrition-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  text-transform: uppercase;
  margin-bottom: 4px;
}

.nutrition-value {
  font-size: 16px;
  color: #111827;
  font-weight: 700;
}

.comments-section {
  border-top: 2px solid #e5e7eb;
  padding-top: 16px;
}

.comments-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.comments-title {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
}

.btn-add-comment {
  background: #10b981;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-add-comment:hover {
  background: #059669;
  transform: scale(1.05);
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comment-item {
  background: #f0fdf4;
  border-left: 3px solid #10b981;
  padding: 12px;
  border-radius: 6px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.comment-author {
  font-size: 12px;
  font-weight: 600;
  color: #065f46;
}

.comment-time {
  font-size: 11px;
  color: #6b7280;
}

.comment-text {
  color: #374151;
  line-height: 1.5;
  font-size: 14px;
}

.no-comments {
  color: #9ca3af;
  font-size: 13px;
  font-style: italic;
  text-align: center;
  padding: 16px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: #fff;
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6b7280;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: background 0.2s ease;
}

.modal-close:hover {
  background: #f3f4f6;
}

.modal-body {
  padding: 24px;
}

.comment-textarea {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 12px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  outline: none;
  transition: border-color 0.2s;
}

.comment-textarea:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #e5e7eb;
}

.btn {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 10px 20px;
  font-weight: 600;
  background: #fff;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
}

.btn:hover {
  background: #f9fafb;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn.primary {
  background: #3b82f6;
  color: #fff;
  border-color: #3b82f6;
}

.btn.primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn.ghost {
  background: transparent;
  color: #374151;
}

.btn.ghost:hover {
  background: #f3f4f6;
}

@media (max-width: 768px) {
  .date-filter {
    flex-direction: column;
    gap: 12px;
  }

  .current-date {
    min-width: auto;
  }

  .nutrition-info {
    grid-template-columns: repeat(2, 1fr);
  }

  .comments-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .btn-add-comment {
    width: 100%;
  }
}
</style>
