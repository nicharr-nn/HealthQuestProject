<template>
  <div class="min-h-screen bg-slate-50 text-slate-900">
    <!-- Mobile overlay -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 z-40 bg-black/40 md:hidden"
      @click="sidebarOpen = false"
    />

    <AdminSideBar
      :sidebarOpen="sidebarOpen"
      :activeSection="activeSection"
      :nav="nav"
      @close="sidebarOpen = false"
      @select="setSection"
    />

     <!-- Main column -->
     <div :class="sidebarOpen ? 'md:pl-72' : 'md:pl-0'">
      <!-- Header -->
      <header class="sticky top-0 left-0 right-0 z-30 z-30 bg-white/90 backdrop-blur supports-[backdrop-filter]:bg-white/60 shadow-sm">
        <div class="flex items-center justify-between px-4 py-3 md:px-8">
          <div class="flex items-center gap-3">
            <button
              class="inline-flex items-center justify-center rounded-md p-2 text-slate-700 hover:bg-slate-100"
              @click="sidebarOpen = !sidebarOpen"
              aria-label="Toggle menu"
            >
              <Menu class="w-5 h-5" />
            </button>
            <div class="relative hidden md:block">
              <input
                type="text"
                placeholder="Search recipes..."
                v-model="searchQuery"
                class="w-80 rounded-md border border-slate-200 pl-5 pr-3 py-2 text-sm font-subtitle placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/40"
              />
            </div>
          </div>

          <div class="flex items-center gap-3">
            <AdminNotificationBell @review="viewCoachDetails" />
            <!-- Header User Info -->
            <div class="flex items-center gap-2">
              <!-- Avatar -->
              <div class="grid h-10 w-10 place-items-center rounded-full bg-blue-500 font-bold font-subtitle text-white">
                <template v-if="userStore.user?.username">
                  {{ getInitials(userStore.user.username) }}
                </template>
                <template v-else>?</template>
              </div>

              <!-- Username and Role -->
              <div class="leading-tight">
                <div class="font-medium font-subtitle">
                  <template v-if="userStore.user?.username">
                    {{ userStore.user.username }}
                  </template>
                  <template v-else>
                    Loading...
                  </template>
                </div>
                <div class="text-[11px] text-slate-500 font-subtitle">Administrator</div>
              </div>
            </div>            
            <button 
              @click="logout"
              class="ml-3 flex items-center py-2 px-3 rounded-md hover:bg-gray-100"
            >
              <span class="material-symbols-outlined">logout</span>
            </button>
          </div>
        </div>
      </header>

      <!-- RECIPES SECTION -->
      <section v-show="activeSection === 'recipes'" class="px-4 py-6 md:px-8 space-y-6">
        <div>
          <h2 class="text-2xl font-bold font-subtitle">Recipe Management</h2>
          <p class="text-sm text-slate-500 font-subtitle">View and manage all recipes posted on the platform</p>
        </div>

        <div class="rounded-xl bg-white p-5 shadow-sm">
          <div class="mb-4 flex items-center justify-between">
            <h3 class="text-base font-semibold font-subtitle">All Recipes ({{ recipes.length }})</h3>
          </div>

          <div v-if="loadingRecipes" class="text-center py-8 text-slate-500">
            Loading recipes...
          </div>
          <div v-else-if="error" class="text-center py-8 text-rose-600">{{ error }}</div>
          <div v-else class="overflow-x-auto">
            <table class="w-full border-collapse text-sm">
              <thead class="text-slate-500">
                <tr class="border-b border-slate-200">
                  <th class="px-3 py-2 text-left font-subtitle">Recipe</th>
                  <th class="px-3 py-2 text-left font-subtitle">Author</th>
                  <!-- <th class="px-3 py-2 text-left font-subtitle">Access Level</th> -->
                  <th class="px-3 py-2 text-left font-subtitle">Created</th>
                  <th class="px-3 py-2 text-left font-subtitle">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="filteredRecipes.length === 0">
                  <td colspan="5" class="px-3 py-8 text-center text-slate-500 font-semibold">
                    No recipes found
                  </td>
                </tr>
                <tr
                  v-for="recipe in filteredRecipes"
                  :key="recipe.id"
                  class="border-b border-slate-100 hover:bg-slate-50"
                >
                  <td class="px-3 py-3 flex items-center gap-3">
                    <div v-if="recipe.image" class="h-12 w-12 rounded-md bg-slate-200 overflow-hidden">
                      <img :src="recipe.image" :alt="recipe.title" class="h-full w-full object-cover" />
                    </div>
                    <div v-else class="grid h-12 w-12 place-items-center rounded-md bg-amber-100 text-xl">
                      🍽️
                    </div>
                    <div>
                      <div class="font-semibold">{{ recipe.title }}</div>
                      <div class="text-xs text-slate-500">{{ getIngredientCount(recipe.ingredients) }} ingredients</div>
                    </div>
                  </td>
                  <td class="px-3 py-3 font-semibold">{{ recipe.user_profile }}</td>
                  <!-- <td class="px-3 py-3 font-semibold">
                    <span
                      class="rounded-full px-2 py-0.5 text-[11px] font-semibold capitalize"
                      :class="recipe.access_level === 'gold' ? 'bg-amber-100 text-amber-800' : 'bg-slate-100 text-slate-800'"
                    >
                      {{ recipe.access_level }}
                    </span>
                  </td> -->
                  <td class="px-3 py-3 font-semibold">{{ formatDate(recipe.created_at) }}</td>
                  <td class="px-3 py-3 font-semibold">
                    <div class="flex gap-2">
                      <button
                        class="rounded-md bg-blue-500 px-3 py-1.5 text-white font-semibold hover:bg-blue-600"
                        @click="viewRecipeDetails(recipe)"
                      >
                        View
                      </button>
                      <button
                        class="rounded-md bg-rose-600 px-3 py-1.5 text-white font-semibold hover:bg-rose-700"
                        @click="deleteRecipe(recipe.id)"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>

    <!-- Recipe Modal -->
    <div
      v-if="recipeModal.open"
      class="fixed inset-0 z-[60] grid place-items-center bg-black/50 p-4"
      role="dialog"
      aria-modal="true"
      @click.self="closeRecipeModal"
    >
      <div class="w-full max-w-3xl overflow-hidden rounded-xl bg-white shadow-lg">
        <!-- Header -->
        <div class="flex items-center justify-between border-b border-slate-200 px-5 py-4">
          <h3 class="text-lg font-subtitle">Recipe Details</h3>
          <button class="text-slate-500 hover:text-slate-700" @click="closeRecipeModal">✕</button>
        </div>

        <!-- Body -->
        <div class="px-5 py-4 space-y-4 max-h-[70vh] overflow-y-auto">
          <div v-if="recipeModal.recipe?.image" class="w-full h-48 rounded-lg bg-slate-200 overflow-hidden">
            <img :src="recipeModal.recipe.image" :alt="recipeModal.recipe.title" class="h-full w-full object-cover" />
          </div>

          <div>
            <h4 class="text-xl font-subtitle">{{ recipeModal.recipe?.title }}</h4>
            <div class="flex items-center gap-3 mt-2">
              <span class="text-sm text-slate-600">By {{ recipeModal.recipe?.user_profile.split(' ')[0].toUpperCase() }}</span>
              <span
                class="rounded-full px-2 py-0.5 text-[11px] font-medium capitalize"
                :class="recipeModal.recipe?.access_level === 'gold' ? 'bg-amber-100 text-amber-800' : 'bg-slate-100 text-slate-800'"
              >
                {{ recipeModal.recipe?.access_level }}
              </span>
              <!-- <div class="flex items-center gap-1">
                <span class="text-amber-500">⭐</span>
                <span class="text-sm">{{ recipeModal.recipe?.average_rating || 'N/A' }}</span>
              </div> -->
            </div>
          </div>

          <div>
            <div class="text-sm font-subtitle text-slate-700 mb-2">Ingredients</div>
            <div class="text-sm bg-slate-50 p-3 rounded-md whitespace-pre-line">
              {{ recipeModal.recipe?.ingredients }}
            </div>
          </div>

          <div>
            <div class="text-sm font-subtitle text-slate-700 mb-2">Steps</div>
            <div class="text-sm bg-slate-50 p-3 rounded-md whitespace-pre-line">
              {{ recipeModal.recipe?.steps }}
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span class="text-slate-600 font-subtitle">Created at</span>
              <span class="ml-2 font-medium">{{ formatDate(recipeModal.recipe?.created_at) }}</span>
            </div>
            <div v-if="recipeModal.recipe?.pdf_file" class="flex justify-end">
            <a
              :href="recipeModal.recipe.pdf_file"
              target="_blank"
              class="rounded-md bg-blue-500 px-3 py-1.5 text-white hover:bg-blue-600 font-bold"
            >
              View PDF
            </a>
          </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="flex justify-end gap-2 border-t border-slate-200 px-5 py-4 bg-slate-50">
          <button
            class="rounded-md border border-slate-300 bg-white px-4 py-2 text-slate-700 hover:bg-slate-50"
            @click="closeRecipeModal"
          >
            Close
          </button>
          <button
            class="rounded-md bg-rose-600 px-4 py-2 text-white hover:bg-rose-700"
            @click="deleteRecipe(recipeModal.recipe.id)"
          >
            Delete Recipe
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import AdminSideBar from '@/components/AdminSideBar.vue'
import { Menu } from 'lucide-vue-next'
import AdminNotificationBell from '@/components/AdminNotificationBell.vue'

const userStore = useUserStore()
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

const sidebarOpen = ref(true)
const activeSection = ref('recipes')
const searchQuery = ref('')
const recipeAccessFilter = ref('all')
const loadingRecipes = ref(false)
const error = ref(null)
const recipes = ref([])

function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0,2)
}

// Sidebar nav
const nav = ref([{ name: 'Recipes', key: 'recipes' }])
function setSection(sectionKey) {
  activeSection.value = sectionKey
}

// Modal state
const recipeModal = ref({ open: false, recipe: null })

// Helpers
function formatDate(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function getIngredientCount(ingredients) {
  if (!ingredients) return 0
  if (Array.isArray(ingredients)) return ingredients.length
  return ingredients
    .split(',')
    .map(i => i.trim())
    .filter(i => i.length > 0)
    .length
}


// Computed filtered recipes
const filteredRecipes = computed(() => {
  let result = recipes.value
  if (recipeAccessFilter.value !== 'all') {
    result = result.filter(r => r.access_level === recipeAccessFilter.value)
  }
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(
      r => r.title.toLowerCase().includes(q) || r.user_profile.toLowerCase().includes(q)
    )
  }
  return result
})

// Modal controls
function viewRecipeDetails(recipe) {
  recipeModal.value.recipe = recipe
  recipeModal.value.open = true
}

function closeRecipeModal() {
  recipeModal.value.open = false
  recipeModal.value.recipe = null
}

// Delete recipe
const deleteRecipe = async (id) => {
  if (!confirm('Are you sure you want to delete this recipe?')) return

  try {
    const response = await fetch(`${API_URL}/api/recipe/${id}/delete/`, {
      method: 'DELETE',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    })

    if (response.status === 200 || response.status === 204) {
      alert('Recipe deleted successfully!')
      await fetchRecipes()
    } else {
      const data = await response.json().catch(() => ({}))
      alert('Delete failed: ' + (data.detail || response.statusText))
    }
  } catch (err) {
    console.error(err)
    alert('Error connecting to backend: ' + err.message)
  }
}

// Fetch recipes
async function fetchRecipes() {
  loadingRecipes.value = true
  error.value = null
  try {
    const res = await fetch(`${API_URL}/api/recipe/`, { credentials: 'include' })
    if (!res.ok) throw new Error('Failed to fetch recipes')
    recipes.value = await res.json()
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load recipes'
  } finally {
    loadingRecipes.value = false
  }
}

onMounted(async () => {
  if (!userStore.profile) await userStore.init()
  await fetchRecipes()
})
</script>