<template>
  <div class="food-diary-container">
    <!-- Header Section -->
    <div class="header-section">
      <button @click="$emit('back')" class="back-button">
        ← Back to Members
      </button>

      <div class="member-info">
        <h1 class="member-name">{{ memberDisplayName }}'s Food Posts</h1>
        <p class="member-subtitle">Review meals and provide coaching feedback</p>
        <span class="member-badge">Member ID: {{ memberId }}</span>
      </div>
    </div>

    <!-- Filter Section -->
    <div class="filter-section">
      <div class="date-picker">
        <button @click="previousDay" class="date-nav-btn">
          <span>←</span>
        </button>
        <div class="current-date">
          <span class="date-label">Viewing:</span>
          <span class="date-value">{{ formattedDate }}</span>
        </div>
        <button @click="nextDay" class="date-nav-btn" :disabled="isToday">
          <span>→</span>
        </button>
      </div>

      <button @click="loadAllPosts" class="view-all-btn">
        View All Posts
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading food posts...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="foodPosts.length === 0" class="empty-state">
      <div class="empty-icon">🍽️</div>
      <h3 class="empty-title">No Food Posts Yet</h3>
      <p class="empty-message">
        {{ memberDisplayName }} hasn't posted any meals for {{ formattedDate }}.
      </p>
    </div>

    <!-- Food Posts Grid -->
    <div v-else class="posts-grid">
      <div
        v-for="post in foodPosts"
        :key="post.id"
        class="post-card"
      >
        <!-- Post Header -->
        <div class="post-header">
          <div class="post-meta">
            <h3 class="post-title">{{ post.title }}</h3>
            <span class="post-time">{{ formatTime(post.created_at) }}</span>
          </div>
        </div>

        <!-- Left-Right Split Layout -->
        <div class="post-body">
          <!-- Left Side: Image and Content -->
          <div class="post-left">
            <!-- Post Image -->
            <div v-if="post.image" class="post-image-container">
              <img :src="getImageUrl(post.image)" :alt="post.title" class="post-image" />
            </div>
            <div v-else class="no-image-placeholder">
              <span>📸 No image uploaded</span>
            </div>

            <!-- Post Content -->
            <div class="post-content">
              <p class="post-description">{{ post.content }}</p>
            </div>
          </div>

          <!-- Right Side: Comments -->
          <div class="post-right">
            <div class="comments-section">
              <div class="comments-header">
                <h4 class="comments-title">
                  Coach Comments
                  <span class="comment-count">({{ getCommentCount(post.id) }})</span>
                </h4>
              </div>

              <!-- Comments List -->
              <div v-if="hasComments(post.id)" class="comments-list">
                <div
                  v-for="comment in getComments(post.id)"
                  :key="comment.id"
                  class="comment-item"
                >
                  <div class="comment-header">
                    <span class="comment-author">🧑‍💼 {{ comment.author_name || 'You' }}</span>
                    <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
                  </div>
                  <p class="comment-text">{{ comment.text }}</p>

                  <!-- Comment Actions (if it's coach's own comment) -->
                  <div v-if="comment.is_own" class="comment-actions">
                    <button @click="editComment(post.id, comment)" class="edit-btn">
                      Edit
                    </button>
                    <button @click="deleteComment(post.id, comment.id)" class="delete-btn">
                      Delete
                    </button>
                  </div>
                </div>
              </div>

              <!-- No Comments Message -->
              <div v-else class="no-comments">
                <p>No feedback yet. Be the first to comment!</p>
              </div>

              <!-- Add Comment Form -->
              <div class="add-comment-form">
                <textarea
                  v-model="commentTexts[post.id]"
                  :placeholder="`Add feedback for ${memberDisplayName}...`"
                  class="comment-input"
                  rows="3"
                  maxlength="500"
                ></textarea>
                <div class="comment-form-footer">
                  <span class="char-count">
                    {{ getCharCount(post.id) }}/500
                  </span>
                  <button
                    @click="addComment(post.id)"
                    :disabled="!canSubmitComment(post.id) || submittingComment[post.id]"
                    class="submit-comment-btn"
                  >
                    {{ submittingComment[post.id] ? 'Posting...' : '💬 Post Comment' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Comment Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Edit Comment</h3>
          <button @click="closeEditModal" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <textarea
            v-model="editingCommentText"
            class="edit-textarea"
            rows="4"
            maxlength="500"
          ></textarea>
          <span class="char-count">{{ editingCommentText.length }}/500</span>
        </div>
        <div class="modal-footer">
          <button @click="closeEditModal" class="cancel-btn">Cancel</button>
          <button @click="updateComment" class="save-btn" :disabled="!editingCommentText.trim()">
            Update Comment
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Props
const props = defineProps({
  memberId: {
    type: String,
    required: true
  },
  memberName: {
    type: String,
    default: 'Member'
  }
})

// Emits
const emit = defineEmits(['back'])

// State
const foodPosts = ref([])
const comments = ref({}) // { postId: [comments] }
const commentTexts = ref({}) // { postId: 'text' }
const submittingComment = ref({}) // { postId: boolean }
const loading = ref(false)
const selectedDate = ref(new Date())
const viewingAll = ref(false)
const memberDisplayName = ref(props.memberName || 'Member')

// Edit Modal State
const showEditModal = ref(false)
const editingPostId = ref(null)
const editingCommentId = ref(null)
const editingCommentText = ref('')

// Computed
const formattedDate = computed(() => {
  if (viewingAll.value) return 'All Time'

  const today = new Date()
  const selected = selectedDate.value

  if (selected.toDateString() === today.toDateString()) return 'Today'

  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)
  if (selected.toDateString() === yesterday.toDateString()) return 'Yesterday'

  return selected.toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    year: 'numeric'
  })
})

const isToday = computed(() => {
  const today = new Date()
  return selectedDate.value.toDateString() === today.toDateString()
})

// Helper Functions
const getImageUrl = (path) => {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `http://127.0.0.1:8000${path}`
}

const formatTime = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getComments = (postId) => {
  return comments.value[postId] || []
}

const hasComments = (postId) => {
  return getComments(postId).length > 0
}

const getCommentCount = (postId) => {
  return getComments(postId).length
}

const getCharCount = (postId) => {
  return (commentTexts.value[postId] || '').length
}

const canSubmitComment = (postId) => {
  const text = commentTexts.value[postId] || ''
  return text.trim().length > 0
}

// Date Navigation
const previousDay = () => {
  const newDate = new Date(selectedDate.value)
  newDate.setDate(newDate.getDate() - 1)
  selectedDate.value = newDate
  viewingAll.value = false
  fetchFoodPosts()
}

const nextDay = () => {
  if (isToday.value) return
  const newDate = new Date(selectedDate.value)
  newDate.setDate(newDate.getDate() + 1)
  selectedDate.value = newDate
  viewingAll.value = false
  fetchFoodPosts()
}

const loadAllPosts = () => {
  viewingAll.value = true
  fetchFoodPosts()
}

// API Functions (Ready for backend integration)
const fetchFoodPosts = async () => {
  loading.value = true
  try {
    // TODO: Replace with actual API call
    // For now, this will prepare the structure for backend integration
    const token = localStorage.getItem('access_token') || ''
    const headers = token ? { Authorization: `Bearer ${token}` } : {}

    let url = `http://127.0.0.1:8000/api/member/food-posts/?member_id=${props.memberId}`

    if (!viewingAll.value) {
      const dateStr = selectedDate.value.toISOString().split('T')[0]
      url += `&date=${dateStr}`
    }

    const response = await fetch(url, {
      headers,
      credentials: 'include'
    })

    if (!response.ok) throw new Error(`Failed to fetch posts: ${response.status}`)

    const data = await response.json()
    foodPosts.value = data

    // Fetch comments for each post
    for (const post of foodPosts.value) {
      await fetchComments(post.id)
    }
  } catch (error) {
    console.error('Error fetching food posts:', error)
    // For development: show empty state instead of error
    foodPosts.value = []
  } finally {
    loading.value = false
  }
}

const fetchComments = async (postId) => {
  try {
    const token = localStorage.getItem('access_token') || ''
    const headers = token ? { Authorization: `Bearer ${token}` } : {}

    const response = await fetch(`http://127.0.0.1:8000/api/member/food-posts/${postId}/comments/`, {
      headers,
      credentials: 'include'
    })

    if (!response.ok) throw new Error(`Failed to fetch comments: ${response.status}`)

    const data = await response.json()
    comments.value[postId] = data
  } catch (error) {
    console.error('Error fetching comments:', error)
    comments.value[postId] = []
  }
}

const addComment = async (postId) => {
  const text = commentTexts.value[postId]?.trim()
  if (!text) return

  submittingComment.value[postId] = true

  try {
    const token = localStorage.getItem('access_token') || ''
    const response = await fetch(`http://127.0.0.1:8000/api/member/food-posts/${postId}/comments/`, {
      method: 'POST',
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({ text })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `Failed to add comment: ${response.status}`)
    }

    const newComment = await response.json()

    // Add to local state
    if (!comments.value[postId]) comments.value[postId] = []
    comments.value[postId].push(newComment)

    // Clear input
    commentTexts.value[postId] = ''

    alert('Comment posted successfully!')
  } catch (error) {
    console.error('Error adding comment:', error)
    alert('Failed to post comment: ' + error.message)
  } finally {
    submittingComment.value[postId] = false
  }
}

const editComment = (postId, comment) => {
  editingPostId.value = postId
  editingCommentId.value = comment.id
  editingCommentText.value = comment.text
  showEditModal.value = true
}

const updateComment = async () => {
  if (!editingCommentText.value.trim()) return

  try {
    const token = localStorage.getItem('access_token') || ''
    const response = await fetch(
      `http://127.0.0.1:8000/api/member/food-posts/${editingPostId.value}/comments/${editingCommentId.value}/`,
      {
        method: 'PUT',
        headers: {
          'Authorization': token ? `Bearer ${token}` : '',
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({ text: editingCommentText.value.trim() })
      }
    )

    if (!response.ok) throw new Error(`Failed to update comment: ${response.status}`)

    const updatedComment = await response.json()

    // Update local state
    const postComments = comments.value[editingPostId.value]
    const index = postComments.findIndex(c => c.id === editingCommentId.value)
    if (index !== -1) {
      postComments[index] = updatedComment
    }

    closeEditModal()
    alert('Comment updated successfully!')
  } catch (error) {
    console.error('Error updating comment:', error)
    alert('Failed to update comment: ' + error.message)
  }
}

const deleteComment = async (postId, commentId) => {
  if (!confirm('Are you sure you want to delete this comment?')) return

  try {
    const token = localStorage.getItem('access_token') || ''
    const response = await fetch(
      `http://127.0.0.1:8000/api/member/food-posts/${postId}/comments/${commentId}/`,
      {
        method: 'DELETE',
        headers: {
          'Authorization': token ? `Bearer ${token}` : ''
        },
        credentials: 'include'
      }
    )

    if (!response.ok) throw new Error(`Failed to delete comment: ${response.status}`)

    // Remove from local state
    comments.value[postId] = comments.value[postId].filter(c => c.id !== commentId)

    alert('Comment deleted successfully!')
  } catch (error) {
    console.error('Error deleting comment:', error)
    alert('Failed to delete comment: ' + error.message)
  }
}

const closeEditModal = () => {
  showEditModal.value = false
  editingPostId.value = null
  editingCommentId.value = null
  editingCommentText.value = ''
}

// Lifecycle
onMounted(() => {
  fetchFoodPosts()
})
</script>

<style scoped>
.food-diary-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Header Section */
.header-section {
  margin-bottom: 32px;
}

.back-button {
  background: transparent;
  border: none;
  color: #3b82f6;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.2s;
  margin-bottom: 16px;
}

.back-button:hover {
  background: #eff6ff;
}

.member-info {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 32px;
  border-radius: 16px;
  color: white;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
}

.member-name {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.member-subtitle {
  font-size: 16px;
  opacity: 0.9;
  margin: 0 0 12px 0;
}

.member-badge {
  display: inline-block;
  background: rgba(255, 255, 255, 0.2);
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  font-family: 'Courier New', monospace;
}

/* Filter Section */
.filter-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  gap: 16px;
  flex-wrap: wrap;
}

.date-picker {
  display: flex;
  align-items: center;
  gap: 16px;
  background: white;
  padding: 12px 20px;
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.date-nav-btn {
  background: #3b82f6;
  color: white;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.date-nav-btn:hover:not(:disabled) {
  background: #2563eb;
  transform: scale(1.05);
}

.date-nav-btn:disabled {
  background: #d1d5db;
  cursor: not-allowed;
}

.current-date {
  display: flex;
  flex-direction: column;
  min-width: 200px;
}

.date-label {
  font-size: 11px;
  color: #6b7280;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.date-value {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
}

.view-all-btn {
  background: #10b981;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
}

.view-all-btn:hover {
  background: #059669;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 64px 24px;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 64px 24px;
  background: white;
  border-radius: 16px;
  border: 2px dashed #d1d5db;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-title {
  font-size: 24px;
  font-weight: 700;
  color: #374151;
  margin: 0 0 8px 0;
}

.empty-message {
  color: #6b7280;
  font-size: 16px;
}

/* Posts Grid */
.posts-grid {
  display: grid;
  gap: 24px;
}

.post-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: all 0.3s;
  border: 2px solid transparent;
}

.post-card:hover {
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  border-color: #3b82f6;
}

/* Post Header */
.post-header {
  padding: 20px 24px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-title {
  font-size: 20px;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.post-time {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
}

/* Post Body - Left/Right Split */
.post-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
}

.post-left {
  background: #f9fafb;
  border-right: 2px solid #e5e7eb;
}

.post-right {
  background: #fef3c7;
}

/* Post Image */
.post-image-container {
  width: 100%;
  height: 250px;
  overflow: hidden;
  background: #f3f4f6;
}

.post-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image-placeholder {
  width: 100%;
  height: 200px;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  font-size: 16px;
}

/* Post Content */
.post-content {
  padding: 20px;
}

.post-description {
  color: #374151;
  line-height: 1.6;
  font-size: 14px;
  margin: 0;
  white-space: pre-line;
}

/* Comments Section */
.comments-section {
  padding: 24px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.comments-header {
  margin-bottom: 16px;
}

.comments-title {
  font-size: 16px;
  font-weight: 700;
  color: #92400e;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.comment-count {
  color: #d97706;
  font-weight: 600;
}

/* Comments List */
.comments-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.comment-item {
  background: white;
  padding: 16px;
  border-radius: 12px;
  border-left: 4px solid #10b981;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-author {
  font-size: 13px;
  font-weight: 700;
  color: #059669;
}

.comment-time {
  font-size: 12px;
  color: #6b7280;
}

.comment-text {
  color: #374151;
  line-height: 1.5;
  margin: 0;
  font-size: 14px;
}

.comment-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e5e7eb;
}

.edit-btn,
.delete-btn {
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.edit-btn {
  background: #fbbf24;
  color: #78350f;
}

.edit-btn:hover {
  background: #f59e0b;
}

.delete-btn {
  background: #fecaca;
  color: #991b1b;
}

.delete-btn:hover {
  background: #fca5a5;
}

/* No Comments */
.no-comments {
  text-align: center;
  padding: 24px;
  color: #92400e;
  font-style: italic;
  background: white;
  border-radius: 8px;
  margin-bottom: 16px;
}

.no-comments p {
  margin: 0;
}

/* Add Comment Form */
.add-comment-form {
  background: white;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.comment-input {
  width: 100%;
  border: 2px solid #d1d5db;
  border-radius: 8px;
  padding: 12px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.2s;
  margin-bottom: 12px;
}

.comment-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.comment-form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.char-count {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.submit-comment-btn {
  background: #10b981;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-comment-btn:hover:not(:disabled) {
  background: #059669;
  transform: translateY(-1px);
}

.submit-comment-btn:disabled {
  background: #d1d5db;
  cursor: not-allowed;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 20px 25px -5px rgba(0,0,0,0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 2px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #111827;
}

.close-btn {
  background: none;
  border: none;
  font-size: 32px;
  color: #6b7280;
  cursor: pointer;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: background 0.2s;
}

.close-btn:hover {
  background: #f3f4f6;
}

.modal-body {
  padding: 24px;
}

.edit-textarea {
  width: 100%;
  border: 2px solid #d1d5db;
  border-radius: 8px;
  padding: 12px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  margin-bottom: 8px;
}

.edit-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 2px solid #e5e7eb;
}

.cancel-btn,
.save-btn {
  padding: 10px 24px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.cancel-btn {
  background: #f3f4f6;
  color: #374151;
}

.cancel-btn:hover {
  background: #e5e7eb;
}

.save-btn {
  background: #3b82f6;
  color: white;
}

.save-btn:hover:not(:disabled) {
  background: #2563eb;
}

.save-btn:disabled {
  background: #d1d5db;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .food-diary-container {
    padding: 16px;
  }

  .member-name {
    font-size: 24px;
  }

  .filter-section {
    flex-direction: column;
    align-items: stretch;
  }

  /* Stack layout on mobile */
  .post-body {
    grid-template-columns: 1fr;
  }

  .post-left {
    border-right: none;
    border-bottom: 2px solid #e5e7eb;
  }

  .post-image-container {
    height: 200px;
  }

  .date-picker {
    justify-content: space-between;
  }

  .view-all-btn {
    width: 100%;
  }

  .post-image-container {
    height: 200px;
  }

  .comment-form-footer {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .submit-comment-btn {
    width: 100%;
  }
}
</style>
