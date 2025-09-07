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
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

async function fetchUserInfo() {
  loading.value = true;
  try {
    const csrftoken = getCookie('csrftoken');
    const response = await fetch("http://localhost:8000/api/user-info/", {
      method: "GET",
      credentials: "include",
      headers: {
        "X-CSRFToken": csrftoken,
        "Accept": "application/json"
      }
    });

    const text = await response.text();
    console.log("Raw response:", text);

    try {
      user.value = JSON.parse(text);
    } catch {
      user.value = null;
      console.error("Failed to parse JSON. Are you logged in?");
    }

  } catch (err) {
    console.error("Error fetching user info:", err);
  } finally {
    loading.value = false;
  }
}

async function logout() {
  const csrftoken = getCookie('csrftoken');
  await fetch("http://localhost:8000/accounts/logout/", {
    method: "POST",
    credentials: "include",
    headers: { "X-CSRFToken": csrftoken }
  });
  user.value = null;
  window.location.href = "http://localhost:5173/";
}

onMounted(() => {
  fetchUserInfo();
});
</script>
