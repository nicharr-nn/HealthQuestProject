<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-[#FAF4E8] p-6">
    <h1 class="text-6xl font-subtitle text-[#909054] mb-6">Tell us about you</h1>

    <form
      @submit.prevent="submitProfile"
      class="bg-white p-6 rounded-xl shadow-md w-full max-w-md space-y-4"
    >
      <!-- Height -->
      <div>
        <label class="block text-gray-700 mb-1 font-body">Height (cm)</label>
        <input 
          v-model="form.height" 
          type="number" 
          class="w-full border p-2 rounded-lg"
          :class="{ 'border-red-500': errors.height }"
          @blur="validateField('height')"
        />
        <p v-if="errors.height" class="text-red-500 text-sm mt-1">{{ errors.height }}</p>
      </div>

      <!-- Weight -->
      <div>
        <label class="block text-gray-700 mb-1 font-body">Weight (kg)</label>
        <input 
          v-model="form.weight" 
          type="number" 
          class="w-full border p-2 rounded-lg"
          :class="{ 'border-red-500': errors.weight }"
          @blur="validateField('weight')"
        />
        <p v-if="errors.weight" class="text-red-500 text-sm mt-1">{{ errors.weight }}</p>
      </div>

      <!-- Age -->
      <div>
        <label class="block text-gray-700 mb-1 font-body">Age</label>
        <input 
          v-model="form.age" 
          type="number" 
          class="w-full border p-2 rounded-lg"
          :class="{ 'border-red-500': errors.age }"
          @blur="validateField('age')"
        />
        <p v-if="errors.age" class="text-red-500 text-sm mt-1">{{ errors.age }}</p>
      </div>

      <!-- Gender -->
      <div>
        <label class="block text-gray-700 mb-1 font-body">Gender</label>
        <select
          v-model="form.gender"
          class="w-full border p-2 rounded-lg font-body"
          :class="{ 'border-red-500': errors.gender }"
          @blur="validateField('gender')"
        >
          <option value="" disabled>Select your gender</option>
          <option value="M">Male</option>
          <option value="F">Female</option>
          <option value="O">Other</option>
        </select>
        <p v-if="errors.gender" class="text-red-500 text-sm mt-1">{{ errors.gender }}</p>
      </div>

      <!-- Location -->
      <div>
        <label class="block text-gray-700 mb-1 font-body">Location</label>
        <select
          v-model="form.location"
          class="w-full border p-2 rounded-lg"
          :class="{ 'border-red-500': errors.location }"
          @blur="validateField('location')"
        >
          <option value="" disabled>Select Location</option>
          <option value="TH">Thailand</option>
          <option value="USA">United States</option>
          <option value="UK">United Kingdom</option>
          <option value="JP">Japan</option>
          <option value="LA">Laos</option>
          <option value="KR">Korea</option>
          <option value="O">Other</option>
        </select>
        <p v-if="errors.location" class="text-red-500 text-sm mt-1">{{ errors.location }}</p>
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
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from '@/stores/user'
import { useToastStore } from "@/stores/toast";

const API_URL = 'http://127.0.0.1:8000'
const router = useRouter();
const loading = ref(false);
const userStore = useUserStore();
const toast = useToastStore();

const form = reactive({
  height: "",
  weight: "",
  age: "",
  gender: "",
  location: ""
});

const errors = reactive({
  height: "",
  weight: "",
  age: "",
  gender: "",
  location: ""
});

// Validate individual field
function validateField(fieldName) {
  const value = form[fieldName];
  
  switch (fieldName) {
    case 'height':
      if (!value) {
        errors.height = "Height is required";
      } else if (parseFloat(value) < 50 || parseFloat(value) > 250) {
        errors.height = "Height must be between 50-250 cm";
      } else {
        errors.height = "";
      }
      break;
      
    case 'weight':
      if (!value) {
        errors.weight = "Weight is required";
      } else if (parseFloat(value) < 20 || parseFloat(value) > 200) {
        errors.weight = "Weight must be between 20-200 kg";
      } else {
        errors.weight = "";
      }
      break;
      
    case 'age':
      if (!value) {
        errors.age = "Age is required";
      } else if (parseInt(value) < 1 || parseInt(value) > 120) {
        errors.age = "Age must be between 1-120";
      } else {
        errors.age = "";
      }
      break;
      
    case 'gender':
      if (!value) {
        errors.gender = "Please select your gender";
      } else {
        errors.gender = "";
      }
      break;
      
    case 'location':
      if (!value) {
        errors.location = "Please select your location";
      } else {
        errors.location = "";
      }
      break;
  }
}

// Validate all fields
function validateForm() {
  validateField('height');
  validateField('weight');
  validateField('age');
  validateField('gender');
  validateField('location');
  
  return Object.values(errors).every(error => error === "");
}


async function submitProfile() {
  if (!validateForm()) {
    toast.error("Please fix the errors in the form");
    return;
  }

  if (userStore.loading) {
    await userStore.init();
  }

  loading.value = true;
  try {
    const payload = {
      height: parseFloat(form.height),
      weight: parseFloat(form.weight),
      age: parseInt(form.age),
      gender: form.gender,
      location: form.location
    };

    const response = await fetch(`${API_URL}/api/user/update-profile/`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrfToken()
      },
      body: JSON.stringify(payload)
    });

if (response.ok) {
  const res = await response.json()


  const profile = res.data
  userStore.setRole(profile.role) 

  if (profile.role === "coach") {
    router.push("/coach-portal")
  } else {
    router.push("/dashboard")
  }
}


  } catch (error) {
    console.error("Error updating profile:", error);
    toast.error("Failed to update profile. Please try again.");
  } finally {
    loading.value = false;
  }
}

function getCsrfToken() {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; csrftoken=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return '';
}
</script>