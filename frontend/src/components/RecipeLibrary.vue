<!-- RecipeLibrary.vue -->
<template>
    <div class="recipe-library">
      <div class="page-header">
        <h1 class="page-title">Recipe Library</h1>
        <p class="page-subtitle">Healthy dishes for your journey</p>
      </div>
  
      <!-- Search and Filter Controls -->
      <div class="dashboard-header">
        <div class="search-section">
          <div class="search-wrapper">
            <input 
              v-model="searchQuery"
              type="text" 
              class="form-input search-input" 
              placeholder="Search recipes..."
              @input="filterRecipes"
            >
            <div class="search-icon">🔍</div>
          </div>
        </div>
        
        <div class="filter-section">
          <div class="category-selector">
            <div 
              v-for="category in categories" 
              :key="category.id"
              class="category-pill" 
              :class="{ active: selectedCategory === category.id }"
              @click="selectCategory(category.id)"
            >
              {{ category.name }}
            </div>
          </div>
          
          <div class="filter-controls">
            <select v-model="sortBy" @change="sortRecipes" class="form-select">
              <option value="name">Sort by Name</option>
              <option value="prep-time">Sort by Prep Time</option>
              <option value="rating">Sort by Rating</option>
              <option value="calories">Sort by Calories</option>
            </select>
            
            <select v-model="difficultyFilter" @change="filterRecipes" class="form-select">
              <option value="all">All Difficulties</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>
        </div>
      </div>
  
      <!-- Recipe Grid -->
      <div v-if="filteredRecipes.length > 0" class="recipe-grid">
        <div 
          v-for="recipe in filteredRecipes" 
          :key="recipe.id"
          class="recipe-card"
          @click="openRecipeModal(recipe)"
        >
          <div class="recipe-image" :style="{ background: recipe.gradient }">
            <div class="recipe-badges">
              <span v-if="recipe.isNew" class="badge new-badge">NEW</span>
              <span v-if="recipe.isPremium" class="badge premium-badge">PREMIUM</span>
              <span class="badge difficulty-badge" :class="recipe.difficulty.toLowerCase()">
                {{ recipe.difficulty }}
              </span>
            </div>
            <div class="recipe-rating">
              <span class="stars">{{ '★'.repeat(recipe.rating) }}{{ '☆'.repeat(5 - recipe.rating) }}</span>
            </div>
          </div>
          
          <div class="recipe-content">
            <div class="recipe-title">{{ recipe.name }}</div>
            <div class="recipe-meta">
              <span class="prep-time">⏱ {{ recipe.prepTime }}</span>
              <span class="calories">🔥 {{ recipe.calories }} cal</span>
              <span class="servings">👥 {{ recipe.servings }} servings</span>
            </div>
            <div class="recipe-description">{{ recipe.description }}</div>
            <div class="recipe-tags">
              <span 
                v-for="tag in recipe.tags" 
                :key="tag"
                class="recipe-tag"
              >
                {{ tag }}
              </span>
            </div>
            <div class="recipe-author">by {{ recipe.author }}</div>
          </div>
        </div>
      </div>
  
      <!-- No Results Message -->
      <div v-else class="no-results">
        <div class="no-results-icon">🔍</div>
        <h3>No recipes found</h3>
        <p>Try adjusting your search or filters</p>
        <button class="action-btn secondary" @click="clearFilters">Clear Filters</button>
      </div>
  
      <!-- Recipe Detail Modal -->
      <div v-if="showRecipeModal" class="modal-overlay" @click="closeRecipeModal">
        <div class="modal-content recipe-modal" @click.stop>
          <div class="recipe-modal-header">
            <h2>{{ selectedRecipe?.name }}</h2>
            <button class="close-btn" @click="closeRecipeModal">×</button>
          </div>
          
          <div class="recipe-modal-content">
            <div class="recipe-hero" :style="{ background: selectedRecipe?.gradient }">
              <div class="recipe-meta-large">
                <div class="meta-item">
                  <span class="meta-icon">⏱</span>
                  <span class="meta-text">{{ selectedRecipe?.prepTime }}</span>
                </div>
                <div class="meta-item">
                  <span class="meta-icon">🔥</span>
                  <span class="meta-text">{{ selectedRecipe?.calories }} cal</span>
                </div>
                <div class="meta-item">
                  <span class="meta-icon">👥</span>
                  <span class="meta-text">{{ selectedRecipe?.servings }} servings</span>
                </div>
                <div class="meta-item">
                  <span class="meta-icon">⭐</span>
                  <span class="meta-text">{{ selectedRecipe?.rating }}/5</span>
                </div>
              </div>
            </div>
            
            <div class="recipe-details">
              <div class="recipe-description-full">
                {{ selectedRecipe?.description }}
              </div>
              
              <div class="nutrition-info">
                <h4>Nutrition per serving</h4>
                <div class="nutrition-grid">
                  <div class="nutrition-item">
                    <span class="nutrition-value">{{ selectedRecipe?.nutrition.protein }}g</span>
                    <span class="nutrition-label">Protein</span>
                  </div>
                  <div class="nutrition-item">
                    <span class="nutrition-value">{{ selectedRecipe?.nutrition.carbs }}g</span>
                    <span class="nutrition-label">Carbs</span>
                  </div>
                  <div class="nutrition-item">
                    <span class="nutrition-value">{{ selectedRecipe?.nutrition.fat }}g</span>
                    <span class="nutrition-label">Fat</span>
                  </div>
                  <div class="nutrition-item">
                    <span class="nutrition-value">{{ selectedRecipe?.nutrition.fiber }}g</span>
                    <span class="nutrition-label">Fiber</span>
                  </div>
                </div>
              </div>
              
              <div class="ingredients-section">
                <h4>Ingredients</h4>
                <ul class="ingredients-list">
                  <li 
                    v-for="ingredient in selectedRecipe?.ingredients" 
                    :key="ingredient"
                    class="ingredient-item"
                  >
                    {{ ingredient }}
                  </li>
                </ul>
              </div>
              
              <div class="instructions-section">
                <h4>Instructions</h4>
                <ol class="instructions-list">
                  <li 
                    v-for="(instruction, index) in selectedRecipe?.instructions" 
                    :key="index"
                    class="instruction-item"
                  >
                    {{ instruction }}
                  </li>
                </ol>
              </div>
              
              <div class="recipe-actions">
                <button class="action-btn" @click="addToMealPlan">Add to Meal Plan</button>
                <button class="action-btn secondary" @click="saveRecipe">
                  {{ isSaved(selectedRecipe?.id) ? 'Saved ✓' : 'Save Recipe' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue'
  
  export default {
    name: 'RecipeLibrary',
    setup() {
      const searchQuery = ref('')
      const selectedCategory = ref('all')
      const sortBy = ref('name')
      const difficultyFilter = ref('all')
      const showRecipeModal = ref(false)
      const selectedRecipe = ref(null)
      const savedRecipes = ref(new Set())
  
      const categories = ref([
        { id: 'all', name: 'All' },
        { id: 'breakfast', name: 'Breakfast' },
        { id: 'lunch', name: 'Lunch' },
        { id: 'dinner', name: 'Dinner' },
        { id: 'snacks', name: 'Snacks' },
        { id: 'desserts', name: 'Desserts' }
      ])
  
      const recipes = ref([
        {
          id: 1,
          name: 'Overnight Oats',
          category: 'breakfast',
          prepTime: '5 min',
          calories: 320,
          servings: 1,
          difficulty: 'Easy',
          rating: 5,
          author: 'PK',
          description: 'Creamy overnight oats with fresh berries and nuts',
          gradient: 'linear-gradient(135deg, #fbbf24, #f59e0b)',
          isNew: true,
          isPremium: false,
          tags: ['High Protein', 'Fiber Rich', 'Make Ahead'],
          nutrition: { protein: 12, carbs: 45, fat: 8, fiber: 6 },
          ingredients: [
            '1/2 cup rolled oats',
            '1/2 cup milk of choice',
            '1 tbsp chia seeds',
            '1 tbsp honey',
            '1/4 cup mixed berries',
            '2 tbsp chopped nuts'
          ],
          instructions: [
            'Mix oats, milk, chia seeds, and honey in a jar',
            'Stir well and refrigerate overnight',
            'In the morning, top with berries and nuts',
            'Enjoy cold or warm up if preferred'
          ]
        },
        {
          id: 2,
          name: 'Sushi Bowl',
          category: 'lunch',
          prepTime: '15 min',
          calories: 450,
          servings: 2,
          difficulty: 'Medium',
          rating: 4,
          author: 'KP',
          description: 'Fresh and healthy deconstructed sushi bowl',
          gradient: 'linear-gradient(135deg, #10b981, #059669)',
          isNew: false,
          isPremium: false,
          tags: ['Low Carb', 'Fresh', 'Omega-3'],
          nutrition: { protein: 25, carbs: 35, fat: 12, fiber: 4 },
          ingredients: [
            '1 cup cooked brown rice',
            '4 oz fresh salmon',
            '1/2 avocado, sliced',
            '1/2 cucumber, julienned',
            '1/4 cup edamame',
            '2 tbsp soy sauce',
            '1 tsp sesame oil',
            'Nori sheets, cut into strips'
          ],
          instructions: [
            'Divide rice between two bowls',
            'Arrange salmon, avocado, cucumber, and edamame on top',
            'Mix soy sauce and sesame oil for dressing',
            'Drizzle dressing over bowls',
            'Garnish with nori strips and serve'
          ]
        },
        {
          id: 3,
          name: 'Flourless Chocolate Cake',
          category: 'desserts',
          prepTime: '30 min',
          calories: 280,
          servings: 8,
          difficulty: 'Hard',
          rating: 5,
          author: 'Min',
          description: 'Rich and decadent gluten-free chocolate cake',
          gradient: 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
          isNew: false,
          isPremium: true,
          tags: ['Gluten Free', 'Rich', 'Special Occasion'],
          nutrition: { protein: 6, carbs: 24, fat: 18, fiber: 3 },
          ingredients: [
            '6 oz dark chocolate',
            '6 tbsp butter',
            '3 large eggs',
            '1/4 cup sugar',
            '1/4 cup cocoa powder',
            'Pinch of salt',
            'Fresh berries for garnish'
          ],
          instructions: [
            'Preheat oven to 375°F',
            'Melt chocolate and butter together',
            'Whisk eggs and sugar until fluffy',
            'Fold in chocolate mixture and cocoa powder',
            'Pour into greased pan and bake 25 minutes',
            'Cool before serving with berries'
          ]
        },
        {
          id: 4,
          name: 'Protein Smoothie',
          category: 'snacks',
          prepTime: '3 min',
          calories: 250,
          servings: 1,
          difficulty: 'Easy',
          rating: 4,
          author: 'CAT',
          description: 'Post-workout protein-packed smoothie',
          gradient: 'linear-gradient(135deg, #ef4444, #dc2626)',
          isNew: false,
          isPremium: false,
          tags: ['High Protein', 'Post-Workout', 'Quick'],
          nutrition: { protein: 30, carbs: 20, fat: 5, fiber: 4 },
          ingredients: [
            '1 scoop protein powder',
            '1 banana',
            '1 cup almond milk',
            '1 tbsp almond butter',
            '1/2 cup frozen berries',
            'Ice cubes'
          ],
          instructions: [
            'Add all ingredients to blender',
            'Blend until smooth',
            'Add ice if needed for desired consistency',
            'Pour into glass and enjoy immediately'
          ]
        },
        {
          id: 5,
          name: 'Quinoa Salad',
          category: 'lunch',
          prepTime: '20 min',
          calories: 380,
          servings: 4,
          difficulty: 'Easy',
          rating: 4,
          author: 'Susan',
          description: 'Mediterranean quinoa salad with fresh vegetables',
          gradient: 'linear-gradient(135deg, #06b6d4, #0891b2)',
          isNew: false,
          isPremium: false,
          tags: ['Vegetarian', 'Complete Protein', 'Meal Prep'],
          nutrition: { protein: 14, carbs: 42, fat: 10, fiber: 5 },
          ingredients: [
            '1 cup quinoa',
            '2 cups vegetable broth',
            '1 cucumber, diced',
            '2 tomatoes, diced',
            '1/4 red onion, minced',
            '1/4 cup olive oil',
            '2 tbsp lemon juice',
            'Fresh herbs',
            'Feta cheese'
          ],
          instructions: [
            'Cook quinoa in vegetable broth until tender',
            'Let quinoa cool completely',
            'Mix in diced vegetables',
            'Whisk olive oil and lemon juice for dressing',
            'Toss salad with dressing',
            'Top with herbs and feta before serving'
          ]
        },
        {
          id: 6,
          name: 'Energy Balls',
          category: 'snacks',
          prepTime: '10 min',
          calories: 120,
          servings: 12,
          difficulty: 'Easy',
          rating: 5,
          author: 'Max',
          description: 'No-bake energy balls with dates and nuts',
          gradient: 'linear-gradient(135deg, #f59e0b, #d97706)',
          isNew: true,
          isPremium: false,
          tags: ['No Bake', 'Natural Sweetener', 'Portable'],
          nutrition: { protein: 4, carbs: 16, fat: 6, fiber: 3 },
          ingredients: [
            '1 cup dates, pitted',
            '1/2 cup almonds',
            '1/4 cup rolled oats',
            '2 tbsp chia seeds',
            '1 tsp vanilla extract',
            'Coconut flakes for rolling'
          ],
          instructions: [
            'Process dates in food processor until paste forms',
            'Add almonds, oats, and chia seeds',
            'Pulse until mixture holds together',
            'Add vanilla and mix',
            'Roll into 12 balls',
            'Roll in coconut flakes and refrigerate'
          ]
        }
      ])
  
      const filteredRecipes = ref([...recipes.value])
  
      const selectCategory = (categoryId) => {
        selectedCategory.value = categoryId
        filterRecipes()
      }
  
      const filterRecipes = () => {
        let filtered = [...recipes.value]
  
        // Filter by category
        if (selectedCategory.value !== 'all') {
          filtered = filtered.filter(recipe => recipe.category === selectedCategory.value)
        }
  
        // Filter by search query
        if (searchQuery.value.trim()) {
          const query = searchQuery.value.toLowerCase()
          filtered = filtered.filter(recipe => 
            recipe.name.toLowerCase().includes(query) ||
            recipe.description.toLowerCase().includes(query) ||
            recipe.author.toLowerCase().includes(query) ||
            recipe.tags.some(tag => tag.toLowerCase().includes(query))
          )
        }
  
        // Filter by difficulty
        if (difficultyFilter.value !== 'all') {
          filtered = filtered.filter(recipe => 
            recipe.difficulty.toLowerCase() === difficultyFilter.value.toLowerCase()
          )
        }
  
        filteredRecipes.value = filtered
        sortRecipes()
      }
  
      const sortRecipes = () => {
        filteredRecipes.value.sort((a, b) => {
          switch (sortBy.value) {
            case 'name':
              return a.name.localeCompare(b.name)
            case 'prep-time':
              return parseInt(a.prepTime) - parseInt(b.prepTime)
            case 'rating':
              return b.rating - a.rating
            case 'calories':
              return a.calories - b.calories
            default:
              return 0
          }
        })
      }
  
      const clearFilters = () => {
        searchQuery.value = ''
        selectedCategory.value = 'all'
        sortBy.value = 'name'
        difficultyFilter.value = 'all'
        filterRecipes()
      }
  
      const openRecipeModal = (recipe) => {
        selectedRecipe.value = recipe
        showRecipeModal.value = true
      }
  
      const closeRecipeModal = () => {
        showRecipeModal.value = false
        selectedRecipe.value = null
      }
  
      const saveRecipe = () => {
        if (selectedRecipe.value) {
          const recipeId = selectedRecipe.value.id
          if (savedRecipes.value.has(recipeId)) {
            savedRecipes.value.delete(recipeId)
          } else {
            savedRecipes.value.add(recipeId)
          }
        }
      }
  
      const isSaved = (recipeId) => {
        return savedRecipes.value.has(recipeId)
      }
  
      const addToMealPlan = () => {
        alert(`${selectedRecipe.value?.name} added to your meal plan!`)
      }
  
      onMounted(() => {
        filterRecipes()
      })
  
      return {
        searchQuery,
        selectedCategory,
        sortBy,
        difficultyFilter,
        categories,
        filteredRecipes,
        showRecipeModal,
        selectedRecipe,
        selectCategory,
        filterRecipes,
        sortRecipes,
        clearFilters,
        openRecipeModal,
        closeRecipeModal,
        saveRecipe,
        isSaved,
        addToMealPlan
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
  
  /* Search and Filter Controls */
  .dashboard-header {
    background: white;
    border-radius: 15px;
    padding: 1.5rem;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    margin-bottom: 2rem;
  }
  
  .search-section {
    margin-bottom: 1.5rem;
  }
  
  .search-wrapper {
    position: relative;
    max-width: 400px;
  }
  
  .search-input {
    width: 100%;
    padding: 0.75rem 3rem 0.75rem 1rem;
    border: 2px solid #e5e7eb;
    border-radius: 25px;
    font-size: 1rem;
    transition: border-color 0.2s ease;
  }
  
  .search-input:focus {
    outline: none;
    border-color: #4f46e5;
  }
  
  .search-icon {
    position: absolute;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: #6b7280;
  }
  
  .filter-section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .category-selector {
    display: flex;
    gap: 0.5rem;
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }
  
  .category-pill {
    min-width: 80px;
    padding: 0.5rem 1rem;
    background: #f3f4f6;
    color: #6b7280;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 600;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
  }
  
  .category-pill.active {
    background: #4f46e5;
    color: white;
  }
  
  .category-pill:hover {
    transform: translateY(-1px);
  }
  
  .filter-controls {
    display: flex;
    gap: 1rem;
  }
  
  .form-input, .form-select {
    padding: 0.5rem;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    font-size: 0.9rem;
    background: white;
  }
  
  .form-select {
    cursor: pointer;
  }
  
  /* Recipe Grid */
  .recipe-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
  }
  
  .recipe-card {
    background: white;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;
    cursor: pointer;
  }
  
  .recipe-card:hover {
    transform: translateY(-3px);
  }
  
  .recipe-image {
    width: 100%;
    height: 180px;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 1rem;
  }
  
  .recipe-badges {
    display: flex;
    gap: 0.5rem;
    align-self: flex-start;
  }
  
  .badge {
    padding: 0.25rem 0.5rem;
    border-radius: 10px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
  }
  
  .new-badge {
    background: #10b981;
    color: white;
  }
  
  .premium-badge {
    background: #f59e0b;
    color: white;
  }
  
  .difficulty-badge.easy {
    background: #10b981;
    color: white;
  }
  
  .difficulty-badge.medium {
    background: #f59e0b;
    color: white;
  }
  
  .difficulty-badge.hard {
    background: #ef4444;
    color: white;
  }
  
  .recipe-rating {
    align-self: flex-end;
    color: #fbbf24;
    font-size: 1rem;
  }
  
  .recipe-content {
    padding: 1.5rem;
  }
  
  .recipe-title {
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 0.75rem;
    font-size: 1.1rem;
  }
  
  .recipe-meta {
    display: flex;
    gap: 1rem;
    margin-bottom: 0.75rem;
    color: #6b7280;
    font-size: 0.8rem;
    flex-wrap: wrap;
  }
  
  .recipe-description {
    color: #6b7280;
    font-size: 0.9rem;
    line-height: 1.4;
    margin-bottom: 1rem;
  }
  
  .recipe-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.25rem;
    margin-bottom: 0.75rem;
  }
  
  .recipe-tag {
    background: #f1f5f9;
    color: #475569;
    padding: 0.15rem 0.5rem;
    border-radius: 8px;
    font-size: 0.7rem;
    font-weight: 500;
  }
  
  .recipe-author {
    color: #9ca3af;
    font-size: 0.8rem;
    font-style: italic;
  }
  
  /* No Results */
  .no-results {
    text-align: center;
    padding: 3rem 1rem;
    color: #6b7280;
  }
  
  .no-results-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
  }
  
  .no-results h3 {
    color: #374151;
    margin-bottom: 0.5rem;
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
    margin-top: 1rem;
  }
  
  .action-btn:hover {
    transform: translateY(-1px);
  }
  
  .action-btn.secondary {
    background: #f3f4f6;
    color: #6b7280;
  }
  
  .action-btn.secondary:hover {
    background: #e5e7eb;
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
    max-width: 800px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
    animation: slideUp 0.3s ease-out;
  }
  
  .recipe-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .recipe-modal-header h2 {
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
  
  .recipe-hero {
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
  }
  
  .recipe-meta-large {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .meta-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
  }
  
  .meta-icon {
    font-size: 1.5rem;
  }
  
  .meta-text {
    font-weight: 600;
    font-size: 0.9rem;
  }
  
  .recipe-details {
    padding: 2rem;
  }
  
  .recipe-description-full {
    color: #6b7280;
    margin-bottom: 2rem;
    line-height: 1.6;
  }
  
  .nutrition-info, .ingredients-section, .instructions-section {
    margin-bottom: 2rem;
  }
  
  .nutrition-info h4, .ingredients-section h4, .instructions-section h4 {
    color: #1e293b;
    font-weight: 700;
    margin-bottom: 1rem;
  }
  
  .nutrition-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .nutrition-item {
    text-align: center;
    padding: 1rem;
    background: #f8fafc;
    border-radius: 10px;
  }
  
  .nutrition-value {
    display: block;
    font-weight: 700;
    color: #10b981;
    font-size: 1.2rem;
    margin-bottom: 0.25rem;
  }
  
  .nutrition-label {
    color: #6b7280;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  
  .ingredients-list, .instructions-list {
    margin: 0;
    padding-left: 1.5rem;
  }
  
  .ingredient-item, .instruction-item {
    color: #374151;
    margin-bottom: 0.5rem;
    line-height: 1.5;
  }
  
  .recipe-actions {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
  }
  
  .recipe-actions .action-btn {
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
  
    .recipe-grid {
      grid-template-columns: 1fr;
    }
  
    .filter-controls {
      flex-direction: column;
    }
  
    .category-selector {
      justify-content: flex-start;
    }
  
    .recipe-meta-large {
      grid-template-columns: repeat(2, 1fr);
      gap: 1rem;
    }
  
    .nutrition-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  
    .recipe-actions {
      flex-direction: column;
    }
  }
  </style>