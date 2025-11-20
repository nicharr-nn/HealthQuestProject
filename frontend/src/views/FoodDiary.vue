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
        <div class="absolute bottom-4 right-4">
          <div class="group relative">
            <!-- Input -->
            <input
              type="text"
              v-model="memberSearchQuery"
              @input="onMemberSearch"
              placeholder="Search members..."
              class="w-10 group-hover:w-64 transition-all duration-300 ease-in-out bg-white text-gray-900 px-2 py-2 rounded-lg shadow-md font-semibold focus:outline-none focus:ring-2 focus:ring-[#9c547b] pl-10"
            />

            <!-- Magnifying glass icon -->
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none" size="20" />
          </div>
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
      <Utensils class="w-12 h-12 text-gray-400 mx-auto mb-4" />
      <h3 class="text-2xl font-bold text-gray-700 mb-2">No Food Posts Yet</h3>
      <p class="text-gray-500">Looks like there is nothing here yet</p>
    </div>

    <!-- Food Posts Grid -->
    <div v-else class="grid gap-6">
      <div v-for="post in foodPosts" :key="post.id" class="bg-white rounded-xl overflow-hidden shadow hover:shadow-xl border-2 border-transparent hover:border-blue-500 transition">
        
        <!-- Post Header: Member Info -->
        <div class="px-6 py-5 bg-gray-50 border-b border-gray-200 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <!-- Avatar -->
            <div class="w-10 h-10 rounded-full flex items-center justify-center font-semibold text-sm flex-shrink-0"
              :class="!post.author_photo ? 'bg-gradient-to-br from-purple-500 to-indigo-500 text-white' : ''">
              <template v-if="post.author_photo">
                <img :src="getImageUrl(post.author_photo)" alt="Profile" class="w-full h-full object-cover rounded-full" />
              </template>
              <template v-else>
                {{ (post.author_first_name || memberDisplayName).charAt(0).toUpperCase() }}
              </template>
            </div>
            <div class="flex flex-col leading-tight">
              <span class="font-semibold text-gray-900">{{ post.author_first_name || memberDisplayName }}</span>
              <span class="text-xs text-gray-500">ID: {{ post.member_id }}</span>
            </div>
          </div>
          <span class="text-xs text-gray-500 font-medium">{{ formatTime(post.created_at) }}</span>
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
            <div v-else class="w-full h-48 flex items-center justify-center bg-gray-100 text-gray-400 text-sm">No image uploaded</div>

            <div class="p-5">
              <h3 class="font-bold text-lg text-gray-900 mb-2">{{ post.title }}</h3>
              <p class="text-gray-700 text-sm leading-relaxed whitespace-pre-line">{{ post.content }}</p>
            </div>
          </div>

          <!-- Right Side - Comments -->
          <div class="bg-[#ffe8f5] p-6 flex flex-col h-full">
            <!-- Header -->
            <div class="mb-4">
              <h4 class="text-xl font-semibold mb-3">
                Coach Comments
                <span class="font-semibold">({{ getCommentCount(post.id) }})</span>
              </h4>
            </div>

            <!-- Scrollable Comments -->
            <div
              v-if="hasComments(post.id)"
              class="flex-1 flex flex-col gap-3 overflow-y-auto mb-4"
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

            <div v-else class="flex-1 flex flex-col justify-center items-center text-gray-500 italic mb-4">
              No comments yet.
            </div>

            <!-- Add Comment Form -->
            <div class="bg-white p-4 rounded-lg shadow mt-auto">
              <textarea
                v-model="commentTexts[post.id]"
                :placeholder="`Write a comment...`"
                class="w-full border-2 border-gray-200 rounded p-3 text-sm resize-y focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-200 mb-3"
                rows="3"
                maxlength="500"
                @keydown.enter.prevent="handleEnter($event, post.id)"
              ></textarea>
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
import { Search, Utensils } from 'lucide-vue-next'

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

// Edit Modal State
const showEditModal = ref(false)
const editingPostId = ref(null)
const editingCommentId = ref(null)
const editingCommentText = ref('')

const members = ref([])
const selectedMemberId = ref('')
const memberId = ref('') // <-- default to all members
const memberDisplayName = ref('All Members')
const memberSearchQuery = ref('')
const allPosts = ref([]) 

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

const fetchFoodPosts = async () => {
  loading.value = true
  try {
    let url = 'http://127.0.0.1:8000/api/member/food-posts/'
    
    if (props.memberId) {
      url += `?member_id=${props.memberId}`
    }

    const response = await fetch(url, { credentials: 'include' })
    if (!response.ok) throw new Error(`Failed to fetch posts: ${response.status}`)
    
    const data = await response.json()
    foodPosts.value = data
    allPosts.value = data

    // Fetch comments for each post
    for (const post of foodPosts.value) {
      await fetchComments(post.id)
    }
  } catch (error) {
    console.error(error)
    foodPosts.value = []
    allPosts.value = []
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

const onMemberSearch = () => {
  const query = memberSearchQuery.value.trim().toLowerCase()

  if (!query) {
    // Show all posts
    foodPosts.value = [...allPosts.value]
    return
  }

  // Filter posts by author name
  foodPosts.value = allPosts.value.filter(post =>
    (post.author_name || '').toLowerCase().includes(query)
  )
}

const handleEnter = (event, postId) => {
  if (!event.shiftKey) {
    addComment(postId)
  }
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
