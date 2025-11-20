<template>
  <div
    class="flex flex-col lg:flex-row w-full max-w-5xl mx-auto mt-4 sm:mt-6 lg:h-[300px] text-[#846757] font-body"
  >
    <!-- Left - Image Section -->
    <div
      class="flex-1 p-3 sm:p-4 bg-purple-100 rounded-t-xl lg:rounded-l-xl lg:rounded-tr-none flex flex-col items-center justify-center"
    >
      <div class="p-2 sm:p-4 text-center w-full">
        <h3 class="text-base sm:text-lg lg:text-xl font-bold break-words">
          {{ recipe.title.length > 40 ? recipe.title.slice(0, 40) + '…' : recipe.title }}
        </h3>

        <!-- Star Rating Display -->
        <div class="flex items-center justify-center gap-2 mt-2">
          <div class="flex gap-1">
            <span v-for="star in 5" :key="star" class="text-xl">
              {{ star <= Math.round(recipe.average_rating || 0) ? '⭐' : '☆' }}
            </span>
          </div>
          <span class="text-sm text-gray-600">
            ({{ recipe.average_rating ? recipe.average_rating.toFixed(1) : '0.0' }})
          </span>
          <span class="text-xs text-gray-500">
            {{ recipe.rating_count || 0 }} {{ recipe.rating_count === 1 ? 'rating' : 'ratings' }}
          </span>
        </div>
      </div>
      <div
        class="w-full max-w-[350px] h-[180px] sm:h-[200px] lg:h-[180px] rounded-lg overflow-hidden shadow-md"
      >
        <img
          :src="recipe.image || 'https://via.placeholder.com/300x300.png?text=No+Image'"
          :alt="recipe.title"
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
            {{ limitText(recipe.ingredients, 6) }}
          </p>

          <h4 class="text-sm sm:text-base lg:text-lg font-semibold mb-2">
            <span class="text-base sm:text-lg lg:text-xl">🎢</span> Steps
          </h4>
          <p class="whitespace-pre-line text-xs sm:text-sm lg:text-base">
            {{ limitText(recipe.steps, 6) }}
          </p>
        </div>
      </div>

      <!-- Buttons -->
      <div class="flex lg:flex-col lg:w-[10%] w-full">
        <!-- Download PDF Button -->
        <div class="relative flex-1 lg:h-full group">
          <a
            :href="`http://127.0.0.1:8000/api/recipe/${recipe.id}/download-pdf/`"
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

        <!-- Rating Button (only show if not owner and not in "My Recipes" view) -->
        <button
          v-if="!isMyRecipe && !isOwner"
          @click="$emit('rate', recipe)"
          class="bg-pink-200 hover:bg-pink-300 text-white flex-1 lg:h-full px-5 py-3 lg:py-2 font-semibold cursor-pointer text-lg sm:text-xl flex items-center justify-center"
          title="Rate this recipe"
        >
          {{ userRating > 0 ? '⭐' : '☆' }}
        </button>

        <!-- Edit and Delete Buttons (Only show if it's the user's recipe) -->
        <template v-if="isMyRecipe">
          <!-- Edit Button -->
          <button
            @click="$emit('edit', recipe)"
            class="bg-yellow-300 hover:bg-yellow-400 text-white flex-1 lg:h-full px-5 py-3 lg:py-2 font-semibold cursor-pointer text-lg sm:text-xl"
          >
            ✍🏻
          </button>

          <!-- Delete Button -->
          <button
            @click="$emit('delete', recipe)"
            class="bg-red-300 hover:bg-red-400 text-white flex-1 lg:h-full px-5 py-3 lg:py-2 font-semibold rounded-br-xl cursor-pointer text-lg sm:text-xl justify-center flex items-center"
          >
            🗑️
          </button>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  recipe: {
    type: Object,
    required: true
  },
  isMyRecipe: {
    type: Boolean,
    default: false
  },
  isOwner: {
    type: Boolean,
    default: false
  },
  userRating: {
    type: Number,
    default: 0
  }
})

defineEmits(['rate', 'edit', 'delete'])

const limitText = (text, maxLines) => {
  if (!text) return ''
  const lines = text.split('\n')
  if (lines.length <= maxLines) return text
  return lines.slice(0, maxLines).join('\n') + '\n… etc.'
}
</script>