<template>
  <div>
    <p v-if="user">Welcome, {{ user.first_name || user.username }} 🎉</p>
    <p v-else-if="loading">Loading user info...</p>
    <p v-else>Please log in first</p>
    <button @click="logout">Sign Out</button>
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