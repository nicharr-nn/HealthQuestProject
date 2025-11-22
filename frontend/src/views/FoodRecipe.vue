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
    <div
      v-if="userStore.level.level.toLowerCase() === 'gold' || userStore.role.toLowerCase() === 'coach'"
      class="bg-blue-100 p-3 sm:p-4 rounded-lg max-w-5xl mx-auto mb-4 sm:mb-6"
    >
      <div class="flex flex-col sm:flex-row items-center justify-center gap-3 sm:gap-8">
        <div class="text-base sm:text-lg font-semibold text-center">
          Choose Recipes to Display:
        </div>
        <div class="flex gap-3 sm:gap-4 flex-wrap justify-center">
          <button
            @click="showMyRecipes"
            :class="[
              'px-4 sm:px-6 py-2 rounded-lg font-semibold shadow-md transition text-sm sm:text-base',
              showMine ? 'bg-[#fcc2f6]' : 'bg-gray-100 hover:bg-gray-200',
            ]"
          >
            My Recipes
          </button>
          <button
            @click="showAllRecipes"
            :class="[
              'px-4 sm:px-6 py-2 rounded-lg font-semibold shadow-md transition text-sm sm:text-base',
              !showMine ? 'bg-[#fcc2f6]' : 'bg-gray-100 hover:bg-gray-200',
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
      <p class="text-lg sm:text-2xl md:text-2xl text-center">
        {{ userStore.level.level.toLowerCase() === 'gold' || userStore.role.toLowerCase() === 'coach'
          ? "Let's share your favorite recipes and discovery healthy meals!"
          : "Let's discover healthy meals from others!" }}
      </p>

      <button
        v-if="showMine"
        @click="openModal"
        class="bg-pink-400 hover:bg-pink-500 text-white font-semibold px-4 sm:px-5 py-2 sm:py-1 rounded-lg shadow-md transition whitespace-nowrap text-sm sm:text-base"
      >
        Upload Recipe
      </button>
    </div>

    <!-- Search and Filter Section -->
    <RecipeFilters
      v-model:search-query="searchQuery"
      v-model:min-rating="minRatingFilter"
      v-model:sort-by="sortBy"
      @clear="clearFilters"
    />

    <!-- Rating Modal -->
    <RatingModal
      :show="showRatingModal"
      :recipe-name="selectedRecipeName"
      :current-rating="tempRating"
      :has-rating="hasUserRated"
      @close="closeRatingModal"
      @submit="submitRating"
      @remove="removeRatingFromModal"
    />

    <!-- Upload / Edit Modal -->
    <RecipeModal
      :show="showModal"
      :edit-mode="editMode"
      :title="recipeTitle"
      :ingredients="recipeIngredients"
      :steps="recipeSteps"
      :uploading="uploading"
      @close="closeModal"
      @submit="submitRecipe"
    />

    <!-- Delete Confirmation Component -->
    <DeleteModal
      v-model:show="showDeleteModal"
      title="Delete Recipe?"
      message="Are you sure you want to delete"
      :item-name="recipeToDeleteName"
      additional-text=" This action cannot be undone."
      cancel-text="Cancel"
      confirm-text="Delete"
      @confirm="confirmDelete"
      @close="closeDeleteModal"
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
        class="mt-4 px-6 py-2 bg-pink-400 hover:bg-pink-500 text-white rounded-lg font-medium cursor-pointer"
      >
        Clear Filters
      </button>
    </div>

    <!-- Recipe Display -->
    <RecipeCard
      v-for="menu in filteredMenus"
      :key="menu.id"
      :recipe="menu"
      :is-my-recipe="showMine"
      :is-owner="isOwner(menu)"
      :user-rating="getUserRating(menu)"
      @rate="openRatingModal"
      @edit="openEditModal"
      @delete="openDeleteModal"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import DeleteModal from '@/components/DeleteModal.vue'
import RecipeCard from '@/components/Recipe/Card.vue'
import RecipeModal from '@/components/Recipe/Modal.vue'
import RatingModal from '@/components/Recipe/RatingModal.vue'
import RecipeFilters from '@/components/Recipe/Filter.vue'

const userStore = useUserStore()
const toast = useToastStore()

const showModal = ref(false)
const recipeTitle = ref('')
const recipeIngredients = ref('')
const recipeSteps = ref('')
const imageFile = ref(null)

const uploading = ref(false)

const editMode = ref(false)
const editingId = ref(null)
const showMine = ref(false)

const showDeleteModal = ref(false)
const recipeToDeleteId = ref(null)
const recipeToDeleteName = ref('')

// Rating modal refs
const showRatingModal = ref(false)
const selectedRecipeId = ref(null)
const selectedRecipeName = ref('')
const tempRating = ref(0)

const searchQuery = ref('')
const minRatingFilter = ref(0)
const sortBy = ref('newest')

const menus = ref([])
const loading = ref(true)

// Computed property for filtered menus
const filteredMenus = computed(() => {
  let filtered = menus.value


  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter((menu) => menu.title.toLowerCase().includes(query))
  }


  if (minRatingFilter.value > 0) {
    filtered = filtered.filter((menu) => (menu.average_rating || 0) >= minRatingFilter.value)
  }

  return filtered
})

const getUserRating = (menu) => {
  if (!menu.ratings || !Array.isArray(menu.ratings)) return 0
  
  for (const rating of menu.ratings) {
  const isUserMatch = rating.user === userStore.user?.username;
  const isUserIdMatch = rating.user_profile_id === userStore.userId;
  
  if (isUserMatch && isUserIdMatch) {
    return rating.rating;
  }
}
return 0;
}

const hasUserRated = computed(() => {
  const menu = menus.value.find(m => m.id === selectedRecipeId.value)
  if (!menu) return false
  
  return getUserRating(menu) > 0
})

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
  recipeTitle.value = ''
  recipeIngredients.value = ''
  recipeSteps.value = ''
}

const openEditModal = (menu) => {
  editMode.value = true
  showModal.value = true
  editingId.value = menu.id
  recipeTitle.value = menu.title
  recipeIngredients.value = menu.ingredients
  recipeSteps.value = menu.steps

}

const closeModal = () => {
  showModal.value = false
  editMode.value = false
  editingId.value = null
  recipeTitle.value = ''
  recipeIngredients.value = ''
  recipeSteps.value = ''
  imageFile.value = null
}

const openRatingModal = (menu) => {
  selectedRecipeId.value = menu.id
  selectedRecipeName.value = menu.title
  const userRating = getUserRating(menu)
  tempRating.value = userRating > 0 ? userRating : 0
  showRatingModal.value = true
}

const closeRatingModal = () => {
  showRatingModal.value = false
  selectedRecipeId.value = null
  selectedRecipeName.value = ''
  tempRating.value = 0
}

const submitRating = async (rating) => {
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/recipe/${selectedRecipeId.value}/give-rating/`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({ rating }),
        credentials: 'include',
      }
    )

    if (response.ok) {
      toast.success('Rating submitted successfully!')
      await fetchRecipeRating(selectedRecipeId.value)
      closeRatingModal()
    } else {
      const errText = await response.text()
      toast.error('Rating failed: ' + errText)
    }
  } catch (err) {
    toast.error('Error submitting rating: ' + err.message)
  }
}

const removeRatingFromModal = async () => {
  if (!hasUserRated.value) {
    toast.warning('No rating to remove')
    return
  }

  

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/recipe/${selectedRecipeId.value}/delete-rating/`,
      {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': getCsrfToken(),
        },
        credentials: 'include',
      }
    )

    if (response.ok) {
      toast.success('Rating removed successfully!')

      const menuIndex = menus.value.findIndex((m) => m.id === selectedRecipeId.value)
      if (menuIndex !== -1 && menus.value[menuIndex].ratings) {
        menus.value[menuIndex].ratings = menus.value[menuIndex].ratings.filter(
          rating => !(rating.user === userStore.user?.username || rating.user_profile_id === userStore.userId)
        )
      }

      await fetchRecipeRating(selectedRecipeId.value)
      closeRatingModal()
    } else {
      const errText = await response.text()
      toast.error('Failed to remove rating: ' + errText)
    }
  } catch (err) {
    toast.error('Error removing rating: ' + err.message)
  }
}

const openDeleteModal = (menu) => {
  showDeleteModal.value = true
  recipeToDeleteId.value = menu.id
  recipeToDeleteName.value = menu.title
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  recipeToDeleteId.value = null
  recipeToDeleteName.value = ''
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
  } finally {
    closeDeleteModal()
  }
}

const submitRecipe = async (data) => {
  if (!data.title || !data.ingredients || !data.steps) {
    toast.warning('Please fill out all fields.')
    return
  }

  const formData = new FormData()
  formData.append('title', data.title)
  formData.append('ingredients', data.ingredients)
  formData.append('steps', data.steps)
  if (data.imageFile) formData.append('image', data.imageFile)

  const url = editMode.value
    ? `http://127.0.0.1:8000/api/recipe/${editingId.value}/update/`
    : 'http://127.0.0.1:8000/api/recipe/'

  const method = editMode.value ? 'PUT' : 'POST'

  try {
    uploading.value = true
    const response = await fetch(url, {
      method,
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
  return (
    userStore.userId === menu.user_id ||
    userStore.user?.id === menu.user_id ||
    userStore.profile?.user_id === menu.user_id
  )
}

const fetchRecipeRating = async (recipeId) => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/recipe/${recipeId}/get-rating/`, {
      credentials: 'include',
    })

    if (response.ok) {
      const data = await response.json()
      
      const menuIndex = menus.value.findIndex((m) => m.id === recipeId)
      if (menuIndex !== -1) {
        menus.value[menuIndex].average_rating = data.average_rating
        menus.value[menuIndex].rating_count = data.rating_count
        menus.value[menuIndex].ratings = data.ratings || []
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


    const params = new URLSearchParams()
    if (sortBy.value) params.append('sort_by', sortBy.value)

    const url = params.toString() ? `${baseUrl}?${params}` : baseUrl

    const response = await fetch(url, {
      credentials: 'include',
    })

    if (!response.ok) throw new Error(`Failed to fetch: ${response.status}`)
    const recipes = await response.json()


    menus.value = recipes


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


</script>
