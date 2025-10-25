<template>
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