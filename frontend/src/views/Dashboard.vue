<template>
  <div>
    <h1 class="text-3xl font-bold mb-4">Dashboard</h1>
    <p>Welcome to your dashboard! Here you can track your progress and manage your account.</p>
    <button @click="logout">Sign Out</button>
  </div>
</template>

<script setup>

async function logout() {
  window.location.href = "http://127.0.0.1:8000/accounts/logout/"
}
</script>