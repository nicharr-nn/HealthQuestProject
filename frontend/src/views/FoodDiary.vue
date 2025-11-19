<template>
  <div class="max-w-[1400px] mx-auto p-6 font-sans">
    
    <!-- Header Section -->
    <div class="mb-8 relative">
      <div class="mt-4 bg-[#fac3e1] p-8 rounded-xl text-white shadow-lg relative">
        <h1 class="font-subtitle text-[#9c547b] text-2xl md:text-3xl font-bold">
          {{ memberDisplayName }}'s Food Posts
        </h1>
        <p class="font-subtitle text-[#9c547b] text-sm opacity-90 mb-3">
          Review meals and provide coaching feedback
        </p>
        <span v-if="memberId" class="inline-block bg-[#9c547b] px-3 py-1 rounded text-xs font-mono font-subtitle">
          Member ID: {{ memberId }}
        </span>

        <!-- Member Selector in right-bottom corner -->
        <div v-if="!props.memberId" class="absolute bottom-4 right-4">
          <select
            @change="onMemberSelect"
            v-model="selectedMemberId"
            class="bg-[#9c547b] text-white px-4 py-2 rounded-lg shadow-md font-semibold hover:bg-[#7a3d63] cursor-pointer focus:outline-none"
          >
            <option value="">All Members</option>
            <option
              v-for="member in members"
              :key="member.memberId"
              :value="member.memberId"
              class="text-black"
            >
              {{ member.name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-16">
      <div class="w-12 h-12 border-4 border-gray-200 border-t-blue-500 rounded-full animate-spin mx-auto mb-4"></div>
      <p>Loading food posts...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="foodPosts.length === 0" class="text-center py-16 bg-white border-2 border-dashed border-gray-200 rounded-xl">
      <div class="text-6xl mb-4">🍽️</div>
      <h3 class="text-2xl font-bold text-gray-700 mb-2">No Food Posts Yet</h3>
      <p class="text-gray-500">{{ memberDisplayName }} hasn't posted any meals yet.</p>
    </div>

    <!-- Food Posts Grid -->
    <div v-else class="grid gap-6">
      <div v-for="post in foodPosts" :key="post.id" class="bg-white rounded-xl overflow-hidden shadow hover:shadow-xl border-2 border-transparent hover:border-blue-500 transition">
        
        <!-- Post Header -->
        <div class="px-6 py-5 bg-gray-50 border-b border-gray-200">
          <div class="flex justify-between items-center">
            <h3 class="font-bold text-lg text-gray-900">{{ post.title }}</h3>
            <span class="text-xs text-gray-500 font-medium">{{ formatTime(post.created_at) }}</span>
          </div>
        </div>

        <!-- Post Body -->
        <div class="grid md:grid-cols-2">
          <!-- Left Side -->
          <div class="bg-gray-50 border-r border-gray-200">
            <div
              v-if="post.image"
              class="w-full h-64 md:h-80 lg:h-[480px] overflow-hidden bg-gray-100"
            >
              <img :src="getImageUrl(post.image)" :alt="post.title" class="w-full h-full object-cover" />
            </div>
            <div v-else class="w-full h-48 flex items-center justify-center bg-gray-100 text-gray-400 text-sm">📸 No image uploaded</div>

            <div class="p-5">
              <p class="text-gray-700 text-sm leading-relaxed whitespace-pre-line">{{ post.content }}</p>
            </div>
          </div>

          <!-- Right Side - Comments -->
          <div class="bg-[#ffe8f5] p-6 flex flex-col">
            <div class="mb-4">
              <h4 class="text-xl font-semibold mb-3">
                Coach Comments
                <span class="font-semibold">({{ getCommentCount(post.id) }})</span>
              </h4>
            </div>

            <div
              v-if="hasComments(post.id)"
              class="flex flex-col gap-3 mb-4 overflow-y-auto"
              style="max-height: 400px;"
            >
              <div
                v-for="comment in getComments(post.id)"
                :key="comment.id"
                class="bg-white p-4 rounded-lg shadow-sm"
              >
                <div class="flex justify-between items-center mb-2">
                  <span
                    :class="{
                      'text-pink-600 font-extrabold uppercase text-xs': comment.author_role==='coach',
                      'text-green-600 font-extrabold uppercase text-xs': comment.author_role==='member'
                    }"
                  >
                    {{ comment.author_name || 'You' }}
                  </span>
                  <span class="text-xs text-gray-500">{{ formatTime(comment.created_at) }}</span>
                </div>
                <p class="text-gray-800 text-sm whitespace-pre-line">{{ comment.text }}</p>
              </div>
            </div>

            <div v-else class="text-center py-4 text-orange-800 italic bg-white rounded mb-4">
              <p>No feedback yet. Be the first to comment!</p>
            </div>          
            <!-- Add Comment Form -->
            <div class="bg-white p-4 rounded-lg shadow">
              <textarea v-model="commentTexts[post.id]" :placeholder="`Write a comment...`"
                class="w-full border-2 border-gray-200 rounded p-3 text-sm resize-y focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-200 mb-3"
                rows="3" maxlength="500">
              </textarea>
              <div class="flex flex-col md:flex-row md:justify-between items-start md:items-center gap-3">
                <span class="text-xs text-gray-500 font-medium">{{ getCharCount(post.id) }}/500</span>
                <button @click="addComment(post.id)" :disabled="!canSubmitComment(post.id) || submittingComment[post.id]"
                  class="cursor-pointer px-4 py-2 bg-[#9CCC65] hover:bg-[#7CB342] text-white font-semibold py-2 rounded-lg transition">
                  {{ submittingComment[post.id] ? 'Commenting...' : 'Add Comment' }}
                </button>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>

    <!-- Edit Comment Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4" @click="closeEditModal">
      <div class="bg-white rounded-xl w-full max-w-lg shadow-2xl" @click.stop>
        <div class="flex justify-between items-center px-6 py-4 border-b-2 border-gray-200">
          <h3 class="font-bold text-lg text-gray-900">Edit Comment</h3>
          <button @click="closeEditModal" class="text-gray-500 text-2xl hover:bg-gray-100 rounded px-2 py-1 transition">×</button>
        </div>
        <div class="px-6 py-4">
          <textarea v-model="editingCommentText" rows="4" maxlength="500"
            class="w-full border-2 border-gray-200 rounded p-3 text-sm resize-y focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-200 mb-2">
          </textarea>
          <span class="text-xs text-gray-500">{{ editingCommentText.length }}/500</span>
        </div>
        <div class="flex justify-end gap-3 px-6 py-4 border-t-2 border-gray-200">
          <button @click="closeEditModal" class="bg-gray-200 text-gray-700 px-4 py-2 rounded font-semibold hover:bg-gray-300 transition">Cancel</button>
          <button @click="updateComment" :disabled="!editingCommentText.trim()"
            class="bg-blue-500 text-white px-4 py-2 rounded font-semibold hover:bg-blue-600 transition disabled:bg-gray-300">Update Comment</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

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

// State
const foodPosts = ref([])
const comments = ref({}) // { postId: [comments] }
const commentTexts = ref({}) // { postId: 'text' }
const submittingComment = ref({}) // { postId: boolean }
const loading = ref(false)
const selectedDate = ref(new Date())
const viewingAll = ref(false)

// Edit Modal State
const showEditModal = ref(false)
const editingPostId = ref(null)
const editingCommentId = ref(null)
const editingCommentText = ref('')

const members = ref([])
const selectedMemberId = ref('') // <-- default to All Members
const memberId = ref('') // <-- default to all members
const memberDisplayName = ref('All Members')

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
  }).replace(',', ' at')
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

// API Calls
const fetchMembers = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/member/accepted/', { credentials: 'include' })
    members.value = await res.json()

    // Default selection: All Members
    selectedMemberId.value = ''
    memberId.value = ''
    memberDisplayName.value = 'All Members'

    // Then fetch posts
    fetchFoodPosts()
  } catch (err) {
    console.error(err)
  }
}

// API Functions (Ready for backend integration)
const fetchFoodPosts = async () => {
  loading.value = true
  try {
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

const closeEditModal = () => {
  showEditModal.value = false
  editingPostId.value = null
  editingCommentId.value = null
  editingCommentText.value = ''
}

// Member select
const onMemberSelect = () => {
  memberId.value = selectedMemberId.value || ''
  if (memberId.value) {
    const member = members.value.find(m => m.memberId === memberId.value)
    memberDisplayName.value = member?.name || 'Member'
  } else {
    memberDisplayName.value = 'All Members'
  }
  fetchFoodPosts()
}

onMounted(async () => {
  await fetchMembers()

  // if URL already has a member ID (e.g. food-diary/M0003)
  if (props.memberId) {
    selectedMemberId.value = props.memberId
    const selected = members.value.find(m => m.memberId === props.memberId)

    // use fetched name first, fallback to props.memberName
    memberDisplayName.value = selected?.name || props.memberName || 'Member'
  } else {
    memberDisplayName.value = 'All Members'
  }

  // then load the posts for that member
  fetchFoodPosts()
})
</script>
