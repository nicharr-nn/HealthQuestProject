<template>
    <div class="page">
      <!-- Header -->
      <header class="header">
        <div class="brand">select goal</div>
        <nav class="nav">
          <button class="nav-btn" @click="goHome">Home</button>
          <button class="nav-btn" @click="goDashboard">Dashboard</button>
        </nav>
      </header>
  
      <!-- Title -->
      <section class="hero">
        <h1 class="title">SELECT GOAL</h1>
        <p class="subtitle">TO START YOUR JOURNEY</p>
      </section>
  
      <!-- Cards -->
      <section class="cards">
        <div
          v-for="card in cards"
          :key="card.id"
          class="card"
          :class="{ selected: selected === card.id }"
          :style="{ backgroundColor: card.bg }"
          @click="select(card.id)"
        >
          <div class="badge">
            <span>OPTION {{ card.id }}</span>
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const selected = ref(null)
  
  const cards = [
    { id: 1, bg: '#CFF6FF' },
    { id: 2, bg: '#E9DFD6' },
    { id: 3, bg: '#EAD6FF' },
  ]
  
  function select(id) {
    selected.value = id
    if (navigator.vibrate) navigator.vibrate(30)
  }
  
  function goHome() { window.location.href = '/' }
  function goDashboard() { window.location.href = '/dashboard' }
  </script>
  
  <!-- Import fonts globally -->
  <style>
  @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&family=Oswald:wght@400;600;700&family=Tilt+Warp&display=swap');
  </style>
  
  <style scoped>
  .page {
    min-height: 100vh;
    background: #F4EEDC;
    display: flex;
    flex-direction: column;
  }
  
  /* Header */
  .header {
    background: #8C7A3A;
    color: #fff;
    padding: 10px 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .brand { text-transform: lowercase; font-weight: 700; letter-spacing: .02em; }
  .nav { display: flex; gap: 16px; }
  .nav-btn {
    background: rgba(255,255,255,.18);
    border: none; color: #fff;
    font-size: 14px; padding: 6px 14px;
    border-radius: 7px; cursor: pointer;
    transition: transform .15s ease, background .15s ease;
  }
  .nav-btn:hover { background: rgba(255,255,255,.28); transform: translateY(-1px); }
  
  /* Hero */
  .hero { text-align: center; padding: 40px 16px 10px; }
  .title {
    margin: 16px 0 6px;
    font-family: "Tilt Warp", system-ui, sans-serif;
    font-size: clamp(42px, 8vw, 104px);
    line-height: 1.05; font-weight: 900; letter-spacing: .01em; color: #111;
  }
  .subtitle {
    font-family: "Oswald", Arial, sans-serif;
    font-size: clamp(16px, 2.3vw, 28px);
    font-weight: 700;
    letter-spacing: .18em;
    margin: 0; color: #1e1e1e;
  }
  
  /* Cards */
  .cards {
    display: flex; justify-content: center; align-items: flex-start;
    gap: clamp(20px, 4vw, 64px);
    padding: 40px 20px 80px; flex-wrap: wrap;
  }
  .card {
    width: clamp(240px, 22vw, 360px);
    height: clamp(300px, 32vw, 420px);
    border-radius: 10px; position: relative; cursor: pointer;
    border: 3px solid transparent;
    box-shadow: 0 6px 10px rgba(0,0,0,.08);
    transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
  }
  .card:hover { transform: translateY(-6px); box-shadow: 0 16px 28px rgba(0,0,0,.12); }
  .card.selected { border-color: #059669; transform: translateY(-3px); box-shadow: 0 14px 24px rgba(5,150,105,.18); }
  
  /* Elliptical badge */
  .badge {
    position: absolute; top: -26px; left: 50%; transform: translateX(-50%);
    display: inline-flex; align-items: center; justify-content: center;
    height: 48px; padding: 0 42px;   /* wider → more ellipse */
    background: #F0D3CC;
    border-radius: 9999px;           /* pill/ellipse */
    box-shadow: 0 2px 0 rgba(0,0,0,.08);
  }
  .badge > span {
    font-family: "Luckiest Guy", system-ui, cursive;
    font-size: 16px; letter-spacing: .02em; color: #111;
    text-transform: uppercase;
  }
  
  @media (max-width: 880px) {
    .cards { padding-top: 24px; }
  }
  </style>
  