<template>
  <div class="min-h-screen py-8 px-4 font-subtitle">
    <!-- Header -->
    <div class="bg-pink-300 p-6 my-6 rounded-lg max-w-5xl mx-auto">
      <p class="text-2xl md:text-3xl font-bold leading-snug">
        "To eat is a necessity, but to eat intelligently is an art."
      </p>
      <p class="text-sm text-right mt-2 italic">– Michael Pollan -</p>
    </div>

    <!-- Share Banner -->
    <div
      class="bg-white rounded-xl p-8 w-full max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 my-6 shadow-md"
    >
      <p class="text-2xl md:text-3xl text-center md:text-left">
        Let’s share our favorite recipes and discover healthy meals from others!
      </p>

      <button
        @click="openModal"
        class="bg-pink-400 hover:bg-pink-500 text-white font-semibold px-6 py-3 rounded-lg shadow-md transition whitespace-nowrap"
      >
        Upload Recipe
      </button>
    </div>

    <!-- Upload / Edit Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50 p-4"
    >
      <div
        class="bg-white rounded-2xl shadow-2xl w-full max-w-lg p-6 relative max-h-[90vh] overflow-y-auto"
      >
        <!-- Close -->
        <button
          @click="closeModal"
          class="absolute top-3 right-3 text-gray-400 hover:text-gray-600 text-2xl"
        >
          ×
        </button>

        <h2 class="text-2xl font-bold mb-4 text-pink-400">
          {{ editMode ? 'Edit Recipe' : 'Upload Your Recipe' }}
        </h2>

        <form @submit.prevent="submitRecipe" class="space-y-4">
          <!-- Title -->
          <div>
            <label class="block text-gray-600 font-medium mb-1">Title</label>
            <input
              v-model="recipeTitle"
              type="text"
              maxlength="100"
              placeholder="e.g., Avocado Toast Deluxe"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-pink-400 focus:outline-none"
              required
            />
            <p class="text-xs text-gray-400 mt-1">
              {{ recipeTitle.length }}/100 characters
            </p>
          </div>

          <!-- Ingredients -->
          <div>
            <label class="block text-gray-600 font-medium mb-1">Ingredients</label>
            <textarea
              v-model="recipeIngredients"
              placeholder="e.g., 2 eggs, 1 avocado, salt ..."
              rows="3"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-pink-400 focus:outline-none"
            ></textarea>
          </div>

          <!-- Steps -->
          <div>
            <label class="block text-gray-600 font-medium mb-1">Steps</label>
            <textarea
              v-model="recipeSteps"
              placeholder="Write each step here ..."
              rows="3"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-pink-400 focus:outline-none"
            ></textarea>
          </div>

          <!-- Image -->
          <div>
            <label class="block text-gray-600 font-medium mb-1">Upload Image</label>
            <input
              type="file"
              accept="image/*"
              @change="handleImageUpload"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 bg-gray-50 cursor-pointer"
            />
            <p v-if="imageName" class="text-sm text-gray-500 mt-1">
              Selected: {{ imageName }}
            </p>
          </div>

          <div class="pt-2">
            <button
              type="submit"
              :disabled="uploading"
              class="w-full bg-pink-400 hover:bg-pink-500 text-white font-semibold py-2 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ uploading ? 'Uploading…' : (editMode ? 'Update Recipe' : 'Submit Recipe') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Recipe Display -->
    <div
      v-for="menu in menus"
      :key="menu.id"
      class="flex flex-col lg:flex-row w-full max-w-5xl mx-auto mt-6 font-body h-[300px]"
    >
      <!-- Left -->
      <div class="flex-1 p-6 bg-blue-200 rounded-xl flex flex-col items-center">
        <div class="w-48 h-48 rounded-lg overflow-hidden shadow-md flex-shrink-0">
          <img
            :src="menu.image || 'https://via.placeholder.com/300x300.png?text=No+Image'"
            :alt="menu.title"
            class="w-full h-full object-cover"
          />
        </div>
        <div class="p-4 text-center">
          <h3 class="text-2xl font-bold max-w-full">
            {{ menu.title.length > 40 ? menu.title.slice(0, 40) + '…' : menu.title }}
          </h3>
        </div>
      </div>

      <!-- Right -->
      <div class="flex-1 p-8 bg-blue-200 rounded-xl flex flex-col justify-between">
        <div class="overflow-y-auto flex-1">
          <h4 class="text-lg font-semibold mb-2">Ingredients</h4>
          <p class="whitespace-pre-line mb-4">
            {{ limitText(menu.ingredients, 6) }}
          </p>

          <h4 class="text-lg font-semibold mb-2">Steps</h4>
          <p class="whitespace-pre-line">
            {{ limitText(menu.steps, 6) }}
          </p>
        </div>

        <div class="mt-4 flex flex-wrap justify-end gap-3 flex-shrink-0">
          <a
            :href="`http://127.0.0.1:8000/api/recipe/${menu.id}/download-pdf/`"
            class="bg-blue-400 text-white font-semibold px-5 py-2 rounded-lg shadow hover:bg-blue-500 transition"
            download
          >
            Download PDF
          </a>

          <button
            @click="openEditModal(menu)"
            class="bg-yellow-400 hover:bg-yellow-500 text-white px-5 py-2 rounded-lg font-semibold shadow-md"
          >
            Edit
          </button>

          <button
            @click="deleteRecipe(menu.id)"
            class="bg-red-500 hover:bg-red-600 text-white px-5 py-2 rounded-lg font-semibold shadow-lg"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

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

const menus = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(() => {
  fetchMenus()
})

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
    alert('Please fill out all fields.')
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
      headers: {
        Authorization: token ? `Bearer ${token}` : '',
      },
      body: formData,
      credentials: 'include',
    })

    if (response.ok) {
      alert(editMode.value ? 'Recipe updated successfully!' : 'Recipe uploaded successfully!')
      closeModal()
      fetchMenus()
    } else {
      const errText = await response.text()
      alert((editMode.value ? 'Update' : 'Upload') + ' failed:\n' + errText)
    }
  } catch (err) {
    alert('Error connecting to backend: ' + err.message)
  } finally {
    uploading.value = false
  }
}

async function fetchMenus() {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/recipe', { credentials: 'include' })
    if (!response.ok) throw new Error(`Failed to fetch: ${response.status}`)
    menus.value = await response.json()
  } catch (err) {
    error.value = 'Could not load recipes.'
  } finally {
    loading.value = false
  }
}

function getCsrfToken() {
  const value = `; ${document.cookie}`
  const parts = value.split(`; csrftoken=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
  return ''
}

const deleteRecipe = async (id) => {
  if (!confirm('Are you sure you want to delete this recipe?')) return

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/recipe/${id}/delete/`, {
      method: 'DELETE',
      headers: { 'X-CSRFToken': getCsrfToken() },
      credentials: 'include',
    })

    if (response.ok) {
      alert('Recipe deleted successfully!')
      fetchMenus()
    } else {
      const errText = await response.text()
      alert('Delete failed:\n' + errText)
    }
  } catch (err) {
    alert('Error connecting to backend: ' + err.message)
  }
}
</script>
