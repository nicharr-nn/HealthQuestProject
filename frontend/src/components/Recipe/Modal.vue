<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black/20 flex items-center justify-center z-50 p-4"
  >
    <div
      class="bg-white rounded-2xl shadow-2xl w-full max-w-lg p-4 sm:p-6 relative max-h-[90vh] overflow-y-auto"
    >
      <!-- Close -->
      <button
        @click="$emit('close')"
        class="absolute top-2 right-2 sm:top-3 sm:right-3 text-gray-400 hover:text-gray-600 text-2xl cursor-pointer"
      >
        ×
      </button>

      <h2 class="text-xl sm:text-2xl font-bold mb-4 text-pink-400">
        {{ editMode ? 'Edit Recipe' : 'Upload Your Recipe' }}
      </h2>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Title -->
        <div>
          <label class="block text-gray-600 font-medium mb-1 text-sm sm:text-base">Title</label>
          <input
            v-model="localTitle"
            type="text"
            maxlength="30"
            placeholder="e.g., Avocado Toast Deluxe"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm sm:text-base focus:ring-2 focus:ring-pink-400 focus:outline-none"
            required
          />
          <p class="text-xs text-gray-400 mt-1">{{ localTitle.length }}/30 characters</p>
        </div>

        <!-- Ingredients -->
        <div>
          <label class="block text-gray-600 font-medium mb-1 text-sm sm:text-base"
            >Ingredients</label
          >
          <textarea
            v-model="localIngredients"
            placeholder="e.g., 2 eggs, 1 avocado, salt ..."
            rows="3"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm sm:text-base focus:ring-2 focus:ring-pink-400 focus:outline-none"
            required
          ></textarea>
        </div>

        <!-- Steps -->
        <div>
          <label class="block text-gray-600 font-medium mb-1 text-sm sm:text-base">Steps</label>
          <textarea
            v-model="localSteps"
            placeholder="Write each step here ..."
            rows="3"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm sm:text-base focus:ring-2 focus:ring-pink-400 focus:outline-none"
            required
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
          <p v-if="localImageName" class="text-xs sm:text-sm text-gray-500 mt-1">
            Selected: {{ localImageName }}
          </p>
        </div>

        <div class="pt-2">
          <button
            type="submit"
            :disabled="uploading"
            class="w-full bg-pink-400 hover:bg-pink-500 text-white font-semibold py-2 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed text-sm sm:text-base cursor-pointer"
          >
            {{ uploading ? 'Uploading…' : editMode ? 'Update Recipe' : 'Submit Recipe' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  editMode: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  ingredients: {
    type: String,
    default: ''
  },
  steps: {
    type: String,
    default: ''
  },
  uploading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'submit'])

const localTitle = ref(props.title)
const localIngredients = ref(props.ingredients)
const localSteps = ref(props.steps)
const localImageFile = ref(null)
const localImageName = ref('')

watch(() => props.title, (newVal) => {
  localTitle.value = newVal
})

watch(() => props.ingredients, (newVal) => {
  localIngredients.value = newVal
})

watch(() => props.steps, (newVal) => {
  localSteps.value = newVal
})

watch(() => props.show, (newVal) => {
  if (!newVal) {
    localImageFile.value = null
    localImageName.value = ''
  }
})

const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    localImageFile.value = file
    localImageName.value = file.name
  }
}

const handleSubmit = () => {
  emit('submit', {
    title: localTitle.value,
    ingredients: localIngredients.value,
    steps: localSteps.value,
    imageFile: localImageFile.value
  })
}
</script>