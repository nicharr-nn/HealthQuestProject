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
        <article
          v-for="card in cards"
          :key="card.id"
          class="card"
          :class="{ selected: selected === card.id }"
          :style="{ backgroundColor: card.bg }"
          @click="select(card.id)"
        >
          <div class="badge"><span>OPTION {{ card.id }}</span></div>
  
          <div class="card-body">
            <div class="icon-bubble">{{ card.icon }}</div>
            <h3 class="card-title">{{ card.title }}</h3>
            <p class="card-desc">{{ card.description }}</p>
  
            <div class="stats">
              <div class="chip">{{ card.duration }}</div>
              <div class="chip">{{ card.focus }}</div>
              <div class="chip">{{ card.level }}</div>
            </div>
  
            <ul class="benefits">
              <li v-for="(b, i) in card.benefits" :key="i">• {{ b }}</li>
            </ul>
  
            <div class="cta" :class="{ on: selected === card.id }">
              {{ selected === card.id ? 'Selected ✓' : 'Click to select' }}
            </div>
          </div>
        </article>
      </section>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const selected = ref(null)
  
  /* --- Mock Data: edit here freely --- */
  const cards = [
    {
      id: 1,
      icon: '🏃‍♂️',
      title: 'Fitness Journey',
      description: 'Build strength, boost cardio, and feel athletic again.',
      duration: '8 weeks',
      focus: 'Strength + Cardio',
      level: 'Beginner',
      benefits: ['3-day split plan', 'Video-guided moves', 'Weekly progress check'],
      bg: '#CFF6FF', // light cyan
    },
    {
      id: 2,
      icon: '🥗',
      title: 'Nutrition Focus',
      description: 'Clean eating plan with macro guidance and easy recipes.',
      duration: '6 weeks',
      focus: 'Balanced macros',
      level: 'All levels',
      benefits: ['Personalized portions', 'Grocery list', 'Thai-friendly recipes'],
      bg: '#E9DFD6', // beige
    },
    {
      id: 3,
      icon: '🧘‍♀️',
      title: 'Wellness Balance',
      description: 'Mindfulness, mobility, and light movement for balance.',
      duration: '4 weeks',
      focus: 'Mind & Body',
      level: 'Gentle',
      benefits: ['10-min daily flow', 'Breathwork audio', 'Sleep routine'],
      bg: '#EAD6FF', // lavender
    },
  ]
  
  function select(id) {
    selected.value = id
    if (navigator.vibrate) navigator.vibrate(30)
  }
  
  function goHome() { window.location.href = '/' }
  function goDashboard() { window.location.href = '/dashboard' }
  </script>
  
  <!-- Load fonts -->
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
  
  /* Cards grid */
  .cards {
    display: flex; justify-content: center; align-items: flex-start;
    gap: clamp(20px, 4vw, 64px);
    padding: 40px 20px 80px; flex-wrap: wrap;
  }
  
  /* Card */
  .card {
    width: clamp(260px, 24vw, 380px);
    min-height: clamp(340px, 34vw, 460px);
    border-radius: 12px;
    position: relative; cursor: pointer;
    border: 3px solid transparent;
    box-shadow: 0 6px 10px rgba(0,0,0,.08);
    transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
  }
  .card:hover { transform: translateY(-6px); box-shadow: 0 16px 28px rgba(0,0,0,.12); }
  .card.selected { border-color: #059669; transform: translateY(-3px); box-shadow: 0 14px 24px rgba(5,150,105,.18); }
  
  .card-body {
    font-family: "Oswald", Arial, sans-serif;
    padding: 22px 22px 26px;
    display: flex; flex-direction: column; gap: 10px;
  }
  
  /* badge (Luckiest Guy) */
  .badge {
    position: absolute; top: -26px; left: 50%; transform: translateX(-50%);
    display: inline-flex; align-items: center; justify-content: center;
    height: 48px; padding: 0 46px;           /* wide ellipse */
    background: #F0D3CC; border-radius: 9999px;
    box-shadow: 0 2px 0 rgba(0,0,0,.08);
  }
  .badge > span {
    font-family: "Luckiest Guy", system-ui, cursive;
    font-size: 16px; letter-spacing: .02em; color: #111; text-transform: uppercase;
  }
  
  /* content */
  .icon-bubble {
    width: 54px; height: 54px; border-radius: 50%;
    background: rgba(255,255,255,.6);
    display: grid; place-items: center;
    font-size: 26px;
    box-shadow: inset 0 0 0 2px rgba(255,255,255,.5);
  }
  .card-title {
    margin-top: 6px;
    font-size: 24px; font-weight: 700; letter-spacing: .02em; color: #121212;
    text-transform: uppercase;
  }
  .card-desc {
    margin: 2px 0 8px; color: #333; line-height: 1.35; font-size: 14px;
  }
  
  /* chips / stats */
  .stats { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 6px; }
  .chip {
    font-size: 12px; font-weight: 700; letter-spacing: .02em;
    background: rgba(255,255,255,.65);
    border: 1px solid rgba(0,0,0,.08);
    padding: 6px 10px; border-radius: 999px; color: #1b1b1b;
  }
  
  /* benefits list */
  .benefits { list-style: none; padding: 0; margin: 2px 0 8px; color: #1f1f1f; }
  .benefits li { font-size: 13px; line-height: 1.35; }
  
  /* CTA hint */
  .cta {
    margin-top: auto;
    text-align: center;
    font-weight: 700;
    font-size: 13px;
    padding: 10px 12px;
    border-radius: 10px;
    background: rgba(255,255,255,.7);
    border: 1px dashed rgba(0,0,0,.15);
    color: #333;
    transition: all .2s ease;
  }
  .cta.on {
    background: #059669; color: #fff; border: 1px solid #059669;
  }
  
  @media (max-width: 880px) {
    .cards { padding-top: 24px; }
  }
  </style>
  