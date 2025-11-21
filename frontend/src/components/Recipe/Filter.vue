<template>
  <div class="bg-purple-50 p-3 sm:p-4 rounded-lg max-w-5xl mx-auto mb-4 sm:mb-6 shadow-md">
    <div class="flex flex-wrap gap-2 items-center">
      <!-- Search Bar -->
      <div class="flex-1 min-w-[180px]">
        <div class="relative">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          
          <input
            :value="searchQuery"
            @input="$emit('update:searchQuery', $event.target.value)"
            type="text"
            placeholder="Search recipes..."
            class="w-full pl-10 pr-8 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-pink-400 focus:outline-none text-sm"
          />
          
          <!-- Clear button inside input -->
          <div
            v-if="searchQuery"
            @click="$emit('update:searchQuery', '')"
            class="absolute right-3 top-1/2 -translate-y-1/2 cursor-pointer text-gray-400 hover:text-gray-600"
            title="Clear search"
          >
            <X class="w-4 h-4" />
          </div>
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
        <option value="title_az">Title Ascending</option>
        <option value="title_za">Title Descending</option>
      </select>
    </div>
  </div>
</template>

<script setup>
import { Search, X } from 'lucide-vue-next';

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