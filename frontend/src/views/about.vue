<template>
  <nav class="sticky top-0 z-50 bg-[#88ACEA] text-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <span class="text-xl font-bold">HealthQuest</span>
          </div>

          <div class="hidden md:flex space-x-4">
            <a href="#home" class="hover:bg-red-500 px-3 py-2 rounded">Home</a>
            <a href="#about" class="hover:bg-red-500 px-3 py-2 rounded">About</a>
            <a href="#contract" class="hover:bg-red-500 px-3 py-2 rounded">Contact</a>
          </div>

          <button
            class="md:hidden flex items-center focus:outline-none"
            @click="isOpen = !isOpen"
          >
            <svg
              class="h-6 w-6"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                v-if="!isOpen"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>

      <div
        v-if="isOpen"
        class="md:hidden bg-[#88ACEA] px-4 pb-3 space-y-2"
      >
        <a href="#home" class="block hover:bg-red-500 px-3 py-2 rounded">Home</a>
        <a href="#about" class="block hover:bg-red-500 px-3 py-2 rounded">About</a>
        <a href="#contract" class="block hover:bg-red-500 px-3 py-2 rounded">Contact</a>
      </div>
    </nav>
 <div class="h-screen text-[#846757] font-bold pl-6 md:pl-10 bg-[#FAF4E6] flex flex-col items-center justify-center gap-6">
  <p v-if="user">Welcome, {{ user.first_name || user.username }} 🎉</p>
  <p v-else-if="loading">Loading user info...</p>
  <h1 v-else class="text-lg md:text-[30px] font-bold">Please log in first</h1>

  <button 
    @click="logout" 
    class="bg-[#E99D7D] hover:bg-orange-500 text-[#A75B3A] text-lg md:text-[20px]
           h-[50px] w-[200px] rounded-full border-2 border-[#A75B3A]">
    Sign Out
  </button>
</div>


</template>

<script setup>
import { ref, onMounted } from "vue";

const user = ref(null);
const loading = ref(true);

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

async function fetchUserInfo() {
  loading.value = true;
  try {
    const response = await fetch("http://127.0.0.1:8000/api/user-info/", {
      method: "GET",
      credentials: 'include',
    });

    // Check if the request was successful
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Parse the JSON response directly
    const data = await response.json();
    console.log("Parsed response:", data);

    if (data.isAuthenticated && data.user) {
      user.value = data.user;
    } else {
      user.value = null;
      console.log("User not authenticated.");
    }
  } catch (err) {
    console.error("Error fetching user info:", err);
    user.value = null; // Ensure user is null on error
  } finally {
    loading.value = false;
  }
}

async function logout() {
  window.location.href = "http://127.0.0.1:8000/accounts/logout/"
}

onMounted(() => {
  fetchUserInfo();
});
</script>