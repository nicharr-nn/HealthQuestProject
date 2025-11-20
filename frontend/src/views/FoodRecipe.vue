<template>
  <div class="min-h-screen py-4 sm:py-8 px-2 sm:px-4 font-subtitle">
    <!-- Header with Quote -->
    <div class="bg-[#fac3e1] p-4 sm:p-6 my-4 sm:my-6 rounded-lg max-w-5xl mx-auto">
      <p class="text-[#9c547b] text-xl sm:text-2xl md:text-3xl font-bold leading-snug">
        "To eat is a necessity, but to eat intelligently is an art."
      </p>
      <p class="text-[#9c547b] text-xs sm:text-sm text-right mt-2 italic">– Michael Pollan -</p>
    </div>

    <!-- Filter Buttons -->
    <div class="bg-blue-100 p-3 sm:p-4 rounded-lg max-w-5xl mx-auto mb-4 sm:mb-6">
      <div class="flex flex-col sm:flex-row items-center justify-center gap-3 sm:gap-8">
        <div class="text-base sm:text-lg font-semibold text-center">Choose Recipes to Display:</div>
        <div class="flex gap-3 sm:gap-4 flex-wrap justify-center">
          <button
            v-if="
              userStore.level.level.toLowerCase() === 'gold' ||
              userStore.role.toLowerCase() === 'coach'
            "
            @click="showMyRecipes"
            :class="[
              'px-4 sm:px-6 py-2 rounded-lg font-semibold shadow-md transition text-sm sm:text-base',
              showMine ? 'bg-[#F9B4FF]' : 'bg-gray-200 hover:bg-gray-300',
            ]"
          >
            My Recipes
          </button>
          <button
            @click="showAllRecipes"
            :class="[
              'px-4 sm:px-6 py-2 rounded-lg font-semibold shadow-md transition text-sm sm:text-base',
              !showMine ? 'bg-[#F9B4FF]' : 'bg-gray-200 hover:bg-gray-300',
            ]"
          >
            All Recipes
          </button>
        </div>
      </div>
    </div>

    <!-- Share Banner -->
    <div
      class="bg-white rounded-xl p-4 sm:p-8 w-full max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 my-4 sm:my-6 shadow-md"
    >
      <p class="text-lg sm:text-2xl md:text-3xl text-center md:text-left">
        Let's share our favorite recipes and discover healthy meals from others!
      </p>

      <button
        v-if="showMine"
        @click="openModal"
        class="bg-pink-400 hover:bg-pink-500 text-white font-semibold px-4 sm:px-6 py-2 sm:py-3 rounded-lg shadow-md transition whitespace-nowrap text-sm sm:text-base"
      >
        Upload Recipe
      </button>
    </div>

    <!-- Search and Filter Section -->
<div class="bg-purple-50 p-3 sm:p-4 rounded-lg max-w-5xl mx-auto mb-4 sm:mb-6 shadow-md">
  <div class="flex flex-wrap gap-2 items-center">
    <!-- Search Bar -->
    <div class="flex-1 min-w-[180px]">
      <div class="relative">
        <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search..."
          class="w-full pl-9 pr-3 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-pink-400 focus:outline-none text-sm"
        />
      </div>
    </div>

    <!-- Rating Filter -->
    <select
      v-model="minRatingFilter"
      class="px-3 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-pink-400 focus:outline-none bg-white text-sm flex-shrink-0"
      title="Minimum Rating"
    >
      <option value="0">All Ratings</option>
      <option value="1">1 +</option>
      <option value="2">2 +</option>
      <option value="3">3 +</option>
      <option value="4">4 +</option>
      <option value="5">5</option>
    </select>

    <!-- Sort By -->
    <select
      v-model="sortBy"
      class="px-3 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-pink-400 focus:outline-none bg-white text-sm flex-shrink-0"
      title="Sort By"
    >
      <option value="newest">Newest</option>
      <option value="oldest">Oldest</option>
      <option value="rating_high">High</option>
      <option value="rating_low">Low</option>
      <option value="title_az">A→Z</option>
      <option value="title_za">Z→A</option>
    </select>

    <!-- Clear Button -->
    <button
      v-if="searchQuery || minRatingFilter > 0 || sortBy !== 'newest'"
      @click="clearFilters"
      class="px-3 py-2 bg-red-100 hover:bg-red-200 text-red-700 rounded-lg text-sm font-medium transition flex-shrink-0"
      title="Clear all filters"
    >
      ✖
    </button>
  </div>
</div>

    <!-- Upload / Edit Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/20 flex items-center justify-center z-50 p-4"
    >
      <div
        class="bg-white rounded-2xl shadow-2xl w-full max-w-lg p-4 sm:p-6 relative max-h-[90vh] overflow-y-auto"
      >
        <!-- Close -->
        <button
          @click="closeModal"
          class="absolute top-2 right-2 sm:top-3 sm:right-3 text-gray-400 hover:text-gray-600 text-2xl cursor-pointer"
        >
          ×
        </button>

        <h2 class="text-xl sm:text-2xl font-bold mb-4 text-pink-400">
          {{ editMode ? 'Edit Recipe' : 'Upload Your Recipe' }}
        </h2>

        <div class="space-y-4">
          <!-- Title -->
          <div>
            <label class="block text-gray-600 font-medium mb-1 text-sm sm:text-base">Title</label>
            <input
              v-model="recipeTitle"
              type="text"
              maxlength="30"
              placeholder="e.g., Avocado Toast Deluxe"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm sm:text-base focus:ring-2 focus:ring-pink-400 focus:outline-none"
              required
            />
            <p class="text-xs text-gray-400 mt-1">{{ recipeTitle.length }}/30 characters</p>
          </div>

          <!-- Ingredients -->
          <div>
            <label class="block text-gray-600 font-medium mb-1 text-sm sm:text-base"
              >Ingredients</label
            >
            <textarea
              v-model="recipeIngredients"
              placeholder="e.g., 2 eggs, 1 avocado, salt ..."
              rows="3"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm sm:text-base focus:ring-2 focus:ring-pink-400 focus:outline-none"
            ></textarea>
          </div>

          <!-- Steps -->
          <div>
            <label class="block text-gray-600 font-medium mb-1 text-sm sm:text-base">Steps</label>
            <textarea
              v-model="recipeSteps"
              placeholder="Write each step here ..."
              rows="3"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm sm:text-base focus:ring-2 focus:ring-pink-400 focus:outline-none"
            ></textarea>
          </div>

          <!-- Image -->
          <div>
            <label class="block text-gray-600 font-medium mb-1 text-sm sm:text-base"
              >Upload Image</label
            >
            <input
              type="file"
              accept="image/*"
              @change="handleImageUpload"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm sm:text-base bg-gray-50 cursor-pointer"
            />
            <p v-if="imageName" class="text-xs sm:text-sm text-gray-500 mt-1">
              Selected: {{ imageName }}
            </p>
          </div>

          <div class="pt-2">
            <button
              @click="submitRecipe"
              :disabled="uploading"
              class="w-full bg-pink-400 hover:bg-pink-500 text-white font-semibold py-2 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed text-sm sm:text-base cursor-pointer"
            >
              {{ uploading ? 'Uploading…' : editMode ? 'Update Recipe' : 'Submit Recipe' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Component -->
    <DeleteModal
      v-model:show="showDeleteModal"
      :message="'Are you sure to delete this recipe?'"
      :confirm-text="'Yes, sure!'"
      @confirm="confirmDelete"
    />

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12 text-gray-500 max-w-5xl mx-auto">
      <p class="text-xl">Loading recipes...</p>
    </div>

    <!-- No Results Message -->
    <div
      v-else-if="filteredMenus.length === 0"
      class="text-center py-12 text-gray-500 max-w-5xl mx-auto"
    >
      <p class="text-xl">No recipes found matching your criteria.</p>
      <button
        v-if="searchQuery || minRatingFilter > 0"
        @click="clearFilters"
        class="mt-4 px-6 py-2 bg-pink-400 hover:bg-pink-500 text-white rounded-lg font-medium"
      >
        Clear Filters
      </button>
    </div>

    <!-- Recipe Display -->
    <div
      v-for="menu in filteredMenus"
      :key="menu.id"
      class="flex flex-col lg:flex-row w-full max-w-5xl mx-auto mt-4 sm:mt-6 lg:h-[300px] text-[#846757] font-body"
    >
      <!-- Left - Image Section -->
      <div
        class="flex-1 p-3 sm:p-4 bg-purple-100 rounded-t-xl lg:rounded-l-xl lg:rounded-tr-none flex flex-col items-center justify-center"
      >
        <div class="p-2 sm:p-4 text-center w-full">
          <h3 class="text-base sm:text-lg lg:text-xl font-bold break-words">
            {{ menu.title.length > 40 ? menu.title.slice(0, 40) + '…' : menu.title }}
          </h3>

          <!-- Star Rating Display -->
          <div class="flex items-center justify-center gap-2 mt-2">
            <div class="flex gap-1">
              <span v-for="star in 5" :key="star" class="text-xl">
                {{ star <= Math.round(menu.average_rating || 0) ? '⭐' : '☆' }}
              </span>
            </div>
            <span class="text-sm text-gray-600">
              ({{ menu.average_rating ? menu.average_rating.toFixed(1) : '0.0' }})
            </span>
            <span class="text-xs text-gray-500">
              {{ menu.rating_count || 0 }} {{ menu.rating_count === 1 ? 'rating' : 'ratings' }}
            </span>
          </div>
        </div>
        <div
          class="w-full max-w-[350px] h-[180px] sm:h-[200px] lg:h-[180px] rounded-lg overflow-hidden shadow-md"
        >
          <img
            :src="menu.image || 'https://via.placeholder.com/300x300.png?text=No+Image'"
            :alt="menu.title"
            class="w-full h-full object-cover"
          />
        </div>
      </div>

      <!-- Right - Content Section -->
      <div
        class="flex-1 bg-purple-50 rounded-b-xl lg:rounded-r-xl lg:rounded-bl-none flex flex-col lg:flex-row overflow-hidden"
      >
        <!-- Content -->
        <div class="flex-1 p-4 sm:p-6 lg:p-8">
          <div class="h-full overflow-y-auto">
            <h4 class="text-sm sm:text-base lg:text-lg font-semibold mb-2">
              <span class="text-base sm:text-lg lg:text-xl">📝</span> Ingredients
            </h4>
            <p class="whitespace-pre-line mb-3 sm:mb-4 text-xs sm:text-sm lg:text-base">
              {{ limitText(menu.ingredients, 6) }}
            </p>

            <h4 class="text-sm sm:text-base lg:text-lg font-semibold mb-2">
              <span class="text-base sm:text-lg lg:text-xl">🎢</span> Steps
            </h4>
            <p class="whitespace-pre-line text-xs sm:text-sm lg:text-base">
              {{ limitText(menu.steps, 6) }}
            </p>

            <!-- User Rating Section -->
            <div v-if="!showMine && !isOwner(menu)" class="mt-4 pt-4 border-t border-gray-200">
              <h4 class="text-sm font-semibold mb-2">Rate this recipe:</h4>
              <div class="flex gap-1">
                <button
                  v-for="star in 5"
                  :key="star"
                  @click="rateRecipe(menu.id, star)"
                  class="text-2xl hover:scale-110 transition-transform cursor-pointer"
                >
                  {{ star <= (menu.user_rating || 0) ? '⭐' : '☆' }}
                </button>

                <!-- Remove Rating Button -->
                <button
                  v-if="menu.user_rating"
                  @click="removeRating(menu.id)"
                  class="ml-2 text-xs text-red-500 hover:text-red-700 underline"
                  title="Remove your rating"
                >
                  Remove
                </button>
              </div>
              <p v-if="menu.user_rating" class="text-xs text-gray-500 mt-1">
                Your rating: {{ menu.user_rating }} stars
              </p>
            </div>
          </div>
        </div>

        <!-- Buttons -->
        <div class="flex lg:flex-col lg:w-[10%] w-full flex-shrink-0">
          <!-- Download PDF Button -->
          <div class="relative flex-1 lg:h-full group">
            <a
              :href="`http://127.0.0.1:8000/api/recipe/${menu.id}/download-pdf/`"
              class="bg-blue-200 rounded-bl-xl lg:rounded-tr-xl lg:rounded-bl-none text-white h-full w-full font-semibold flex items-center justify-center hover:bg-blue-300 transition py-3 lg:py-0 text-lg sm:text-xl"
              download
            >
              💾
            </a>

            <span
              class="absolute bottom-full lg:bottom-auto lg:top-1/2 lg:-translate-y-1/2 mb-2 lg:mb-0 left-1/2 -translate-x-1/2 lg:left-full lg:translate-x-2 lg:ml-2 bg-[#846757] text-white text-xs px-2 py-1 rounded-md whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-10"
            >
              Download PDF
            </span>
          </div>

          <!-- Edit and Delete Buttons (Only show if it the user's recipe) -->
          <template v-if="showMine">
            <!-- Edit Button -->
            <button
              @click="openEditModal(menu)"
              class="bg-yellow-200 hover:bg-yellow-300 text-white flex-1 lg:h-full px-5 py-3 lg:py-2 font-semibold cursor-pointer text-lg sm:text-xl"
            >
              ✍🏻
            </button>

            <!-- Delete Button -->
            <button
              @click="openDeleteModal(menu)"
              class="bg-red-200 hover:bg-red-300 text-white flex-1 lg:h-full px-5 py-3 lg:py-2 font-semibold rounded-br-xl cursor-pointer text-lg sm:text-xl justify-center flex items-center"
            >
              🗑️
            </button>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import DeleteModal from '@/components/DeleteModal.vue'

const userStore = useUserStore()
const toast = useToastStore()

const showModal = ref(false)
const recipeTitle = ref('')
const recipeIngredients = ref('')
const recipeSteps = ref('')
const imageFile = ref(null)
const imageName = ref('')
const uploading = ref(false)
const token = localStorage.getItem('access_token') || ''

const editMode = ref(false)
const editingId = ref(null)
const showMine = ref(false)

const showDeleteModal = ref(false)
const recipeToDeleteId = ref(null)

const searchQuery = ref('')
const minRatingFilter = ref(0)
const sortBy = ref('newest')

const menus = ref([])
const loading = ref(true)

// Computed property for filtered menus
const filteredMenus = computed(() => {
  let filtered = menus.value

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter((menu) => menu.title.toLowerCase().includes(query))
  }

  // Filter by minimum rating
  if (minRatingFilter.value > 0) {
    filtered = filtered.filter((menu) => (menu.average_rating || 0) >= minRatingFilter.value)
  }

  return filtered
})

// Watch for sort changes to refetch from backend
watch(sortBy, () => {
  fetchMenus(showMine.value)
})

const clearFilters = () => {
  searchQuery.value = ''
  minRatingFilter.value = 0
  sortBy.value = 'newest'
}

onMounted(() => {
  fetchMenus()
})

const openModal = () => {
  showModal.value = true
  editMode.value = false
}

const openEditModal = (menu) => {
  editMode.value = true
  showModal.value = true
  editingId.value = menu.id
  recipeTitle.value = menu.title
  recipeIngredients.value = menu.ingredients
  recipeSteps.value = menu.steps
  imageName.value = ''
}

const closeModal = () => {
  showModal.value = false
  editMode.value = false
  editingId.value = null
  recipeTitle.value = ''
  recipeIngredients.value = ''
  recipeSteps.value = ''
  imageFile.value = null
  imageName.value = ''
}

const openDeleteModal = (menu) => {
  showDeleteModal.value = true
  recipeToDeleteId.value = menu.id
}

const confirmDelete = async () => {
  if (!recipeToDeleteId.value) return

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/recipe/${recipeToDeleteId.value}/delete/`,
      {
        method: 'DELETE',
        headers: { 'X-CSRFToken': getCsrfToken() },
        credentials: 'include',
      },
    )

    if (response.ok) {
      toast.success('Recipe deleted successfully!')
      fetchMenus(showMine.value)
    } else {
      const errText = await response.text()
      toast.error('Delete failed: ' + errText)
    }
  } catch (err) {
    toast.error('Error connecting to backend: ' + err.message)
  }
}

const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    imageName.value = file.name
  }
}

const limitText = (text, maxLines) => {
  if (!text) return ''
  const lines = text.split('\n')
  if (lines.length <= maxLines) return text
  return lines.slice(0, maxLines).join('\n') + '\n… etc.'
}

const submitRecipe = async () => {
  if (!recipeTitle.value || !recipeIngredients.value || !recipeSteps.value) {
    toast.warning('Please fill out all fields.')
    return
  }

  const formData = new FormData()
  formData.append('title', recipeTitle.value)
  formData.append('ingredients', recipeIngredients.value)
  formData.append('steps', recipeSteps.value)
  if (imageFile.value) formData.append('image', imageFile.value)

  const url = editMode.value
    ? `http://127.0.0.1:8000/api/recipe/${editingId.value}/update/`
    : 'http://127.0.0.1:8000/api/recipe/'

  const method = editMode.value ? 'PUT' : 'POST'

  try {
    uploading.value = true
    const response = await fetch(url, {
      method,
      headers: { Authorization: token ? `Bearer ${token}` : '' },
      body: formData,
      credentials: 'include',
    })

    if (response.ok) {
      toast.success(
        editMode.value ? 'Recipe updated successfully!' : 'Recipe uploaded successfully!',
      )
      closeModal()
      fetchMenus(showMine.value)
    } else {
      const errText = await response.text()
      toast.error((editMode.value ? 'Update' : 'Upload') + ' failed: ' + errText)
    }
  } catch (err) {
    toast.error('Error connecting to backend: ' + err.message)
  } finally {
    uploading.value = false
  }
}

const isOwner = (menu) => {
  return userStore.userId === menu.user_id
}

const rateRecipe = async (recipeId, rating) => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/recipe/${recipeId}/give-rating/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: token ? `Bearer ${token}` : '',
        'X-CSRFToken': getCsrfToken(),
      },
      body: JSON.stringify({ rating }),
      credentials: 'include',
    })

    if (response.ok) {
      await response.json()
      toast.success('Rating submitted successfully!')

      // Fetch updated rating data
      await fetchRecipeRating(recipeId)
    } else {
      const errText = await response.text()
      toast.error('Rating failed: ' + errText)
    }
  } catch (err) {
    toast.error('Error submitting rating: ' + err.message)
  }
}

const fetchRecipeRating = async (recipeId) => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/recipe/${recipeId}/get-rating/`, {
      headers: {
        Authorization: token ? `Bearer ${token}` : '',
      },
      credentials: 'include',
    })

    if (response.ok) {
      const data = await response.json()

      // Update the menu item with new rating data
      const menuIndex = menus.value.findIndex((m) => m.id === recipeId)
      if (menuIndex !== -1) {
        menus.value[menuIndex].average_rating = data.average_rating
        menus.value[menuIndex].rating_count = data.rating_count

        // Find user's rating from ratings array
        const userRating = data.ratings?.find((r) => r.user_profile_id === userStore.userId)
        menus.value[menuIndex].user_rating = userRating?.rating || 0
      }
    }
  } catch (err) {
    console.error('Error fetching rating:', err)
  }
}

async function fetchMenus(onlyMine = false) {
  loading.value = true
  try {
    const baseUrl = onlyMine
      ? 'http://127.0.0.1:8000/api/recipe/my-recipes/'
      : 'http://127.0.0.1:8000/api/recipe'

    // Build query parameters for sorting
    const params = new URLSearchParams()
    if (sortBy.value) params.append('sort_by', sortBy.value)

    const url = params.toString() ? `${baseUrl}?${params}` : baseUrl

    const response = await fetch(url, {
      headers: { Authorization: token ? `Bearer ${token}` : '' },
      credentials: 'include',
    })

    if (!response.ok) throw new Error(`Failed to fetch: ${response.status}`)
    const recipes = await response.json()

    // Fetch ratings for all recipes
    menus.value = recipes

    // Fetch rating data for each recipe
    await Promise.all(recipes.map((recipe) => fetchRecipeRating(recipe.id)))
  } catch (err) {
    toast.error('Error loading recipes: ' + err.message)
  } finally {
    loading.value = false
  }
}

const showMyRecipes = async () => {
  showMine.value = true
  await fetchMenus(true)
}

const showAllRecipes = async () => {
  showMine.value = false
  await fetchMenus(false)
}

function getCsrfToken() {
  const value = `; ${document.cookie}`
  const parts = value.split(`; csrftoken=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
  return ''
}

const removeRating = async (recipeId) => {
  if (!confirm('Are you sure you want to remove your rating?')) {
    return
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/recipe/${recipeId}/delete-rating/`, {
      method: 'DELETE',
      headers: {
        Authorization: token ? `Bearer ${token}` : '',
        'X-CSRFToken': getCsrfToken(),
      },
      credentials: 'include',
    })

    if (response.ok) {
      toast.success('Rating removed successfully!')

      // Update local state
      const menuIndex = menus.value.findIndex((m) => m.id === recipeId)
      if (menuIndex !== -1) {
        menus.value[menuIndex].user_rating = 0
      }

      // Fetch updated rating data
      await fetchRecipeRating(recipeId)
    } else {
      const errText = await response.text()
      toast.error('Failed to remove rating: ' + errText)
    }
  } catch (err) {
    toast.error('Error removing rating: ' + err.message)
  }
}
</script>
