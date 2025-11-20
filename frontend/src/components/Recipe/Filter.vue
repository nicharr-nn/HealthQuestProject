<template>
  <div class="bg-purple-50 p-3 sm:p-4 rounded-lg max-w-5xl mx-auto mb-4 sm:mb-6 shadow-md">
    <div class="flex flex-wrap gap-2 items-center">
      <!-- Search Bar -->
      <div class="flex-1 min-w-[180px]">
        <div class="relative">
          <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
          <input
            :value="searchQuery"
            @input="$emit('update:searchQuery', $event.target.value)"
            type="text"
            placeholder="Search..."
            class="w-full pl-9 pr-3 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-pink-400 focus:outline-none text-sm"
          />
        </div>
      </div>

      <!-- Rating Filter -->
      <select
        :value="minRating"
        @change="$emit('update:minRating', Number($event.target.value))"
        class="px-3 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-pink-400 focus:outline-none bg-white text-sm flex-shrink-0"
        title="Minimum Rating"
      >
        <option value="0">All Ratings</option>
        <option value="1">1⭐+</option>
        <option value="2">2⭐+</option>
        <option value="3">3⭐+</option>
        <option value="4">4⭐+</option>
        <option value="5">5⭐</option>
      </select>

      <!-- Sort By -->
      <select
        :value="sortBy"
        @change="$emit('update:sortBy', $event.target.value)"
        class="px-3 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-pink-400 focus:outline-none bg-white text-sm flex-shrink-0"
        title="Sort By"
      >
        <option value="newest">Newest</option>
        <option value="oldest">Oldest</option>
        <option value="rating_high">Highest Rating</option>
        <option value="rating_low">Lowest Rating</option>
        <option value="title_az">Title A→Z</option>
        <option value="title_za">Title Z→A</option>
      </select>

      <!-- Clear Button -->
      <button
        v-if="searchQuery || minRating > 0 || sortBy !== 'newest'"
        @click="$emit('clear')"
        class="px-3 py-2 bg-red-100 hover:bg-red-200 text-red-700 rounded-lg text-sm font-medium transition flex-shrink-0"
        title="Clear all filters"
      >
        ✖ Clear
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  searchQuery: {
    type: String,
    default: ''
  },
  minRating: {
    type: Number,
    default: 0
  },
  sortBy: {
    type: String,
    default: 'newest'
  }
})

defineEmits(['update:searchQuery', 'update:minRating', 'update:sortBy', 'clear'])
</script>