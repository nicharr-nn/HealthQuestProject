<template>
  <div class="font-subtitle">
    <div class="bg-[#ED8FBF] p-6 my-6">
      <p class="text-2xl md:text-3xl font-bold text-white leading-snug">
        “To eat is a necessity, but to eat intelligently is an art.”
      </p>
      <p class="text-sm text-white text-right mt-2 italic">
        – Michael Pollan
      </p>
    </div>

    <!-- Share Banner -->
    <div
      class="bg-white rounded-xl p-8 w-full max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 my-6"
    >
      <p class="text-2xl md:text-3xl text-center md:text-left">
        Let’s share our favorite recipes and discover healthy meals from others!
      </p>

      <button
        @click="openModal"
        class="bg-[#ED8FBF] hover:bg-[#d977a4] text-white font-semibold px-6 py-3 rounded-lg shadow-md transition"
      >
        Upload Recipe
      </button>
    </div>

    <!-- Upload Recipe Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg p-6 relative">
        <!-- Close Button -->
        <button
          @click="closeModal"
          class="absolute top-3 right-3 text-gray-400 hover:text-gray-600 text-2xl"
        >
          ×
        </button>

        <h2 class="text-2xl font-bold mb-4 text-[#ED8FBF]">
          Upload Your Recipe
        </h2>

        <form @submit.prevent="submitRecipe" class="space-y-4">
          <div>
            <label class="block text-gray-600 font-medium mb-1">Recipe Title</label>
            <input
              v-model="recipeTitle"
              type="text"
              placeholder="e.g., Green Smoothie Bowl"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#ED8FBF] focus:outline-none"
              required
            />
          </div>

          <div>
            <label class="block text-gray-600 font-medium mb-1">Description</label>
            <textarea
              v-model="recipeDescription"
              placeholder="Briefly describe your recipe..."
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#ED8FBF] focus:outline-none"
              rows="3"
            ></textarea>
          </div>

          <div>
            <label class="block text-gray-600 font-medium mb-1">Upload Image / File</label>
            <input
              @change="handleFileUpload"
              type="file"
              accept="image/*,.pdf"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 bg-gray-50 cursor-pointer"
            />
            <p v-if="fileName" class="text-sm text-gray-500 mt-1">
              Selected: {{ fileName }}
            </p>
          </div>

          <div class="pt-2">
            <button
              type="submit"
              class="w-full bg-[#ED8FBF] hover:bg-[#d977a4] text-white font-semibold py-2 rounded-lg transition"
            >
              Submit Recipe
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Recipe Display -->
    <div class="flex flex-row justify-between w-full max-w-5xl mx-auto mt-6">
     <!-- Left Box: Photo & Name (smaller photo) -->
        <div class="flex-1 p-0 bg-[#B4D9E2] rounded-xl overflow-hidden flex flex-col items-center">
            <div class="w-48 h-48 mt-4 rounded-lg overflow-hidden">
                <img
                src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=600"
                alt="Food"
                class="w-full h-full object-cover"
                />
            </div>
            <div class="p-4 text-center text-white">
                <h3 class="text-2xl font-bold">Avocado Toast Deluxe</h3>
            </div>
        </div>

      <!-- Right Box: Description & Download -->
      <div class="flex-1 p-8 bg-[#B4D9E2] rounded-xl flex flex-col justify-between">
        <div>
          <h4 class="text-lg font-semibold text-white mb-2">Description</h4>
          <p class="text-white leading-relaxed">
            A simple yet delicious avocado toast topped with poached eggs, cherry tomatoes, and chili flakes. Perfect for a healthy breakfast!
          </p>
        </div>
        <div class="mt-4 text-right">
          <button
            @click="downloadPDF"
            class="bg-blue-200 font-semibold px-5 py-2 rounded-lg shadow hover:bg-gray-100 transition"
          >
            Download as PDF
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Modal state
const showModal = ref(false)

// Form fields
const recipeTitle = ref('')
const recipeDescription = ref('')
const fileName = ref('')

// Functions
function openModal() {
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  recipeTitle.value = ''
  recipeDescription.value = ''
  fileName.value = ''
}

function handleFileUpload(e) {
  const file = e.target.files[0]
  if (file) {
    fileName.value = file.name
  }
}

function submitRecipe() {
  console.log('📌 Recipe Submitted:')
  console.log('Title:', recipeTitle.value)
  console.log('Description:', recipeDescription.value)
  console.log('File:', fileName.value)

  alert(`Recipe "${recipeTitle.value}" uploaded successfully!`)
  closeModal()
}

// 📄 Demo PDF download
function downloadPDF() {
  const pdfUrl = 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf'
  const link = document.createElement('a')
  link.href = pdfUrl
  link.download = 'recipe.pdf'
  link.click()
}
</script>
