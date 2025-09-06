<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-[#FAF4E8] p-6">
    <h1 class="text-6xl font-subtitle text-[#909054] mb-6">Tell us about you</h1>

    <form
      @submit.prevent="submitForm"
      class="bg-white p-6 rounded-xl shadow-md w-full max-w-md space-y-3"
    >
      <div>
        <label class="block text-gray-700 mb-1 font-body">Height (cm)</label>
        <input v-model="form.height" type="number" class="w-full border p-2 rounded-lg" />
      </div>

      <div>
        <label class="block text-gray-700 mb-1 font-body">Weight (kg)</label>
        <input v-model="form.weight" type="number" class="w-full border p-2 rounded-lg" />
      </div>

      <div>
        <label class="block text-gray-700 mb-1 font-body">Age</label>
        <input v-model="form.age" type="number" class="w-full border p-2 rounded-lg" />
      </div>

      <div>
        <label class="block text-gray-700 mb-1 font-body">Gender</label>
        <select
          v-model="form.gender"
          class="w-full border p-2 rounded-lg font-body"
        >
          <option value="" disabled>Select your gender</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>
      </div>

      <button
        type="submit"
        class="w-full bg-[#88ACEA] text-white font-body py-2 rounded-lg hover:bg-indigo-700"
      >
        Save & Continue
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({
  height: '',
  weight: '',
  age: '',
  gender: '',
})

async function submitForm() {
  console.log('Sending About You data:', form.value)

  // Example API call
  await fetch('/set-about-you/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(form.value),
  })

  // Redirect to dashboard after saving
  router.push('/profile')
}
</script>
