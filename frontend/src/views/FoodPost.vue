<template>
  <div class="font-subtitle min-h-screen py-8">
    <!-- Header -->
    <div
      class="bg-[#D0F4DE] p-6 my-6 rounded-lg max-w-5xl mx-auto flex items-center justify-between"
    >
      <h2 class="text-2xl md:text-3xl font-bold text-[#846757]">Share Your Meal with Your Coach</h2>
      <button
        @click="openModal"
        class="bg-[#fac3e1] hover:bg-pink-300 px-8 py-3 rounded-lg shadow-md cursor-pointer font-semibold"
        style="color: #9c547b;"
      >
        Upload Meal
      </button>
    </div>

    <!-- Food Posts -->
    <div
      v-for="post in foodPosts"
      :key="post.id"
      class="max-w-5xl mx-auto bg-purple-200 shadow-lg rounded-2xl my-8 grid lg:grid-cols-[1.5fr_1fr] overflow-hidden"
    >
      <!-- Left side (image, name, content) -->
      <div class="bg-[#e2dbff] flex flex-col font-body">
        <!-- Image Section -->
        <div class="flex flex-col items-center text-center p-6 text-[#846757]">
          <h3 class="text-3xl font-semibold mb-4">{{ post.title }}</h3>
          <div class="w-full h-64 md:h-80 rounded-lg overflow-hidden shadow-md mx-auto cursor-pointer">
            <img
              :src="getImageUrl(post.image)"
              :alt="post.title"
              class="w-full h-full object-cover"
              @click="openImageModal(getImageUrl(post.image))"
            />
          </div>
          <div
            v-if="showImageModal"
            class="fixed inset-0 bg-black/20 flex items-center justify-center z-50 p-4"
          >
            <div class="relative">
              <!-- Close button on top-left of the image -->
              <button
                @click="closeImageModal"
                class="absolute top-2 right-2 text-white text-2xl font-bold bg-black/30 rounded-full w-8 h-8 flex items-center justify-center cursor-pointer"
              >
                ×
              </button>

              <!-- Image -->
              <img
                :src="currentImage"
                alt="Full size"
                class="max-h-[90vh] max-w-full rounded-lg shadow-lg"
              />
            </div>
          </div>
        </div>

        <!-- Content Section -->
        <div class="flex-1 p-6 flex flex-col justify-between">
          <div class="text-center mb-6">
            <p class="text-[#846757] whitespace-pre-line">
              {{ post.content }}
            </p>
          </div>

          <div class="flex justify-center gap-3">
            <button
              @click="openEditModal(post)"
              class="cursor-pointer bg-yellow-400 hover:bg-yellow-500 text-white px-5 py-2 rounded-lg font-semibold shadow-md"
            >
              Edit
            </button>
            <button
              @click="openDeleteModal(post)"
              class="cursor-pointer bg-red-400 hover:bg-red-500 text-white px-5 py-2 rounded-lg font-semibold shadow-md"
            >
              Delete
            </button>
          </div>
        </div>
      </div>

      <!-- Right side (Comments) -->
      <div class="bg-[#E6F3E6] p-6 flex flex-col justify-between font-body">
        <h4 class="text-xl font-semibold mb-3">Coach Comments</h4>
        <div class="flex-1 overflow-y-auto space-y-2 mb-4 max-h-90">
          <div
            v-for="comment in comments[post.id] || []"
            :key="comment.id"
            class="bg-white p-3 rounded-lg shadow-sm text-sm text-gray-800"
          >
            <div class="flex justify-between items-center mb-1">
              <span 
                class="font-extrabold uppercase" 
                :class="{
                  'text-pink-500 text-xs': comment.author_role === 'coach',
                  'text-green-600 text-xs': comment.author_role === 'member',
                }"
              >
                {{ comment.author_name }}
              </span>
              <span class="text-xs text-gray-500">
                {{ formatCommentTime(comment.created_at) }}
              </span>
            </div>
            <p class="text-gray-800 whitespace-pre-line">{{ comment.text }}</p>
          </div>

          <p
            v-if="!comments[post.id] || comments[post.id].length === 0"
            class="text-gray-500 italic text-sm"
          >
            No comment yet.
          </p>
        </div>

        <div class="mt-auto">
          <input
            v-model="newComment"
            type="text"
            placeholder="Write a comment..."
            class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-2 text-sm"
          />
          <button
            @click="addComment(post.id)"
            class="cursor-pointer w-full bg-[#9CCC65] hover:bg-[#7CB342] text-white font-semibold py-2 rounded-lg transition"
          >
            Add Comment
          </button>
        </div>
      </div>
    </div>

    <!-- Upload/Edit Modal -->
    <div
        v-if="showModal"
        class="fixed inset-0 bg-black/20 flex items-center justify-center z-50 p-4"
      >
        <div
          class="bg-white rounded-2xl shadow-2xl w-full max-w-lg p-6 relative max-h-[90vh] overflow-y-auto"
        >
        <button
          @click="closeModal"
          class="absolute top-3 right-3 text-gray-400 hover:text-gray-600 text-2xl cursor-pointer"
        >
          ×
        </button>

        <h2 class="text-2xl font-bold mb-4 text-pink-400">
          {{ editMode ? 'Edit Meal' : 'Upload Your Meal' }}
        </h2>

        <form @submit.prevent="submitMeal" class="space-y-4">
          <!-- Food Name -->
          <div>
            <label class="block text-gray-600 font-medium mb-1">Food Name</label>
            <input
              v-model="foodName"
              type="text"
              maxlength="40"
              placeholder="e.g., Grilled Chicken Salad"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-pink-400 focus:outline-none"
              required
            />
            <p class="text-xs text-gray-400 mt-1">
              {{ foodName.length }}/40 characters
            </p>
          </div>

          <!-- Description -->
          <div>
            <label class="block text-gray-600 font-medium mb-1">Description</label>
            <textarea
                v-model="foodDescription"
                placeholder="Describe your meal..."
                maxlength="80"
                rows="3"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-pink-400 focus:outline-none"
                required
            ></textarea>
            <p class="text-xs text-gray-400 mt-1">
                {{ foodDescription.length }}/80 characters
            </p>
            </div>

          <!-- Image Upload -->
          <div>
            <label class="block text-gray-600 font-medium mb-1">
              {{ editMode ? 'Update Photo' : 'Upload Photo' }}
            </label>
            <input
              type="file"
              accept="image/*"
              @change="handleImageUpload"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 bg-gray-50 cursor-pointer"
              :required="!editMode"
            />
            <p v-if="imageName" class="text-sm text-gray-500 mt-1">
              Selected: {{ imageName }}
            </p>
            <div v-if="editMode && currentImageUrl" class="mt-2">
              <p class="text-sm text-gray-600 mb-1">Current Image:</p>
              <img 
                :src="getImageUrl(currentImageUrl)" 
                alt="Current meal image"
                class="w-32 h-32 object-cover rounded-lg border mx-auto"
              />
            </div>
          </div>

          <!-- Submit Button -->
          <div class="pt-2">
            <button
              type="submit"
              :disabled="uploading"
              class="w-full bg-pink-400 hover:bg-pink-500 text-white font-semibold py-2 rounded-lg transition 
              disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            >
              {{ uploading ? 'Uploading…' : (editMode ? 'Update Meal' : 'Submit Meal') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Component -->
    <DeleteModal
      v-model:show="showDeleteModal"
      title="Delete Meal Post?"
      message="Are you sure you want to delete"
      :item-name="postToDeleteTitle"
      cancel-text="Keep Post"
      confirm-text="Yes, Delete"
      @confirm="confirmDeletePost"
      @close="closeDeleteModal"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToastStore } from '@/stores/toast'
import DeleteModal from '@/components/DeleteModal.vue'

const toast = useToastStore()

const showModal = ref(false)
const foodPosts = ref([])
const foodName = ref('')
const foodDescription = ref('')
const imageFile = ref(null)
const imageName = ref('')
const uploading = ref(false)
const editMode = ref(false)
const editingId = ref(null)
const currentImageUrl = ref('')
const showImageModal = ref(false)
const currentImage = ref('')
const token = localStorage.getItem('access_token') || ''

// Delete modal state
const showDeleteModal = ref(false)
const postToDeleteId = ref(null)
const postToDeleteTitle = ref('')

// Comments (local only)
const comments = ref({})
const newComment = ref('')

// Delete modal functions
const openDeleteModal = (post) => {
  showDeleteModal.value = true
  postToDeleteId.value = post.id
  postToDeleteTitle.value = post.title
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  postToDeleteId.value = null
  postToDeleteTitle.value = ''
}

const confirmDeletePost = async () => {
  if (!postToDeleteId.value) return
  
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/member/food-posts/${postToDeleteId.value}/delete/`,
      {
        method: 'DELETE',
        headers: { Authorization: token ? `Bearer ${token}` : '' },
        credentials: 'include'
      }
    )
    if (response.ok) {
      toast.success('Post deleted successfully!')
      fetchFoodPosts()
    } else {
      const errText = await response.text()
      toast.error('Delete failed:\n' + errText)
    }
  } catch (err) {
    toast.error('Error connecting to backend: ' + err.message)
  } finally {
    closeDeleteModal()
  }
}

// Fetch comments for a post
const fetchComments = async (postId) => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/member/food-posts/${postId}/comments/`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      credentials: 'include'
    })
    if (!res.ok) throw new Error(`Failed to fetch comments for post ${postId}`)
    comments.value[postId] = await res.json()
  } catch (err) {
    console.error(err)
    comments.value[postId] = []
  }
}

// Add comment (send to backend)
const addComment = async (postId) => {
  if (!newComment.value.trim()) return
  try {
    const payload = { text: newComment.value }

    const res = await fetch(`http://127.0.0.1:8000/api/member/food-posts/${postId}/comments/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: token ? `Bearer ${token}` : ''
      },
      body: JSON.stringify(payload),
      credentials: 'include'
    })

    if (!res.ok) throw new Error(`Failed to add comment: ${res.statusText}`)

    // Backend returns the created comment
    const newCmt = await res.json()

    if (!comments.value[postId]) comments.value[postId] = []
    comments.value[postId].push(newCmt)
    newComment.value = ''
  } catch (err) {
    console.error(err)
    toast.success('Failed to post comment: ' + err.message)
  }
}

// Image helper
const getImageUrl = (path) => {
  if (!path) return 'https://via.placeholder.com/300x300.png?text=No+Image'
  if (path.startsWith('http')) return path
  return `http://127.0.0.1:8000${path}`
}

const fetchFoodPosts = async () => {
  try {
    const headers = token ? { Authorization: `Bearer ${token}` } : {}
    const response = await fetch('http://127.0.0.1:8000/api/member/food-posts/', {
      headers,
      credentials: 'include'
    })
    if (!response.ok) throw new Error(`Failed to fetch: ${response.status}`)
    foodPosts.value = await response.json()

    // Fetch comments for each post
    for (const post of foodPosts.value) {
      await fetchComments(post.id)
    }
  } catch (err) {
    console.error('Error:', err)
    toast.error('Failed to load posts: ' + err.message)
  }
}

// Submit or update post
const submitMeal = async () => {
  if (!foodName.value || !foodDescription.value || (!editMode.value && !imageFile.value)) {
    toast.error('Please fill all required fields')
    return
  }

  uploading.value = true
  try {
    if (editMode.value) {
      const postData = {
        title: foodName.value,
        content: foodDescription.value
      }

      const updateResponse = await fetch(
        `http://127.0.0.1:8000/api/member/food-posts/${editingId.value}/update/`,
        {
          method: 'PUT',
          headers: {
            'Authorization': token ? `Bearer ${token}` : '',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(postData),
          credentials: 'include'
        }
      )

      if (!updateResponse.ok) {
        let errText = ''
        try {
          const errData = await updateResponse.json()
          errText = Object.entries(errData)
            .map(([k, v]) => `${k}: ${v}`)
            .join('\n')
        } catch {
          errText = await updateResponse.text()
        }
        throw new Error(`Update failed:\n${errText}`)
      }

      if (imageFile.value) {
        await uploadImageToPost(editingId.value, imageFile.value)
      }

      toast.success('Post updated successfully!')
    } else {
      const formData = new FormData()
      formData.append('title', foodName.value)
      formData.append('content', foodDescription.value)
      formData.append('image', imageFile.value)

      const response = await fetch('http://127.0.0.1:8000/api/member/food-posts/', {
        method: 'POST',
        headers: { Authorization: token ? `Bearer ${token}` : '' },
        body: formData,
        credentials: 'include'
      })

      if (!response.ok) {
        let errText = ''
        try {
          const errData = await response.json()
          errText = Object.entries(errData)
            .map(([k, v]) => `${k}: ${v}`)
            .join('\n')
        } catch {
          errText = await response.text()
        }
        throw new Error(`Create failed:\n${errText}`)
      }

      toast.success('Post created successfully!')
    }

    closeModal()
    fetchFoodPosts()
  } catch (err) {
    toast.error('Error: ' + err.message)
  } finally {
    uploading.value = false
  }
}

// Upload image for existing post
const uploadImageToPost = async (postId, file) => {
  const formData = new FormData()
  formData.append('image', file)

  const response = await fetch(
    `http://127.0.0.1:8000/api/member/food-posts/${postId}/upload-image/`,
    {
      method: 'POST',
      headers: { Authorization: token ? `Bearer ${token}` : '' },
      body: formData,
      credentials: 'include'
    }
  )

  if (!response.ok) {
    const errorText = await response.text()
    throw new Error(`Image upload failed: ${response.status} - ${errorText}`)
  }

  return await response.json()
}

const openImageModal = (imgUrl) => {
  currentImage.value = imgUrl
  showImageModal.value = true
}

const closeImageModal = () => {
  showImageModal.value = false
  currentImage.value = ''
}

// Modal logic
const openEditModal = (post) => {
  editMode.value = true
  editingId.value = post.id
  foodName.value = post.title
  foodDescription.value = post.content
  currentImageUrl.value = post.image || ''
  imageFile.value = null
  imageName.value = ''
  showModal.value = true
}

const openModal = () => {
  editMode.value = false
  editingId.value = null
  foodName.value = ''
  foodDescription.value = ''
  imageFile.value = null
  imageName.value = ''
  currentImageUrl.value = ''
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editMode.value = false
  editingId.value = null
  foodName.value = ''
  foodDescription.value = ''
  imageFile.value = null
  imageName.value = ''
  currentImageUrl.value = ''
  uploading.value = false
}

// Handle file selection
const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    imageName.value = file.name
  } else {
    imageFile.value = null
    imageName.value = ''
  }
}

// Format date
const formatCommentTime = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const options = { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' }
  const formattedDate = date.toLocaleString('en-US', options)
  return formattedDate.replace(',', ' at')
}

onMounted(() => {
  fetchFoodPosts()
})
</script>