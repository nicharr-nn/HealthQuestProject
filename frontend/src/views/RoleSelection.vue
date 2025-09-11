<template>
  <section class="max-w-6xl mx-auto px-6 py-12">
    <!-- Heading - Use your configured font-display class -->
    <h1 class="font-subtitle text-5xl md:text-7xl text-center tracking-wide text-[#846757]">
      SELECT ROLE
    </h1>
    <p class="font-subtitle text-center text-xl md:text-2xl text-gray-500 mt-4">
      Choose your role to get started on your fitness journey. Each role offers different
      features and capabilities tailored to your needs.
    </p>

    <!-- Cards -->
    <div class="mt-10 grid grid-cols-1 md:grid-cols-3 gap-8">
      <button @click="select('member')" class="text-left">
        <RoleCard
          title="MEMBER"
          :points="memberPoints"
          color= "text-[#8C876A]"
          bg="bg-cardKhaki"
          titleColor="text-[#7D7858]"
        />
      </button>

      <button @click="select('normal')" class="text-left">
        <RoleCard
          title="NORMAL USER"
          :points="normalUserPoints"
          color= "text-[#417479]"
          bg="bg-cardBlue"
          titleColor="text-[#368492]"
        />
      </button>

      <button @click="select('coach')" class="text-left">
        <RoleCard
          title="COACH"
          :points="coachPoints"
          color= "text-[#C4847C]"
          bg="bg-cardPink"
          titleColor="text-[#9C6963]"
        />
      </button>
    </div>
  </section>
</template>

<script setup>
import RoleCard from '../components/RoleCard.vue'
import { useRouter } from 'vue-router' // Import router

const router = useRouter() // Get router instance

const memberPoints = [
  "All Normal User features (XP, levels, goals)",
  "Follow coach-assigned workout programs",
  "Post food privately for coach feedback",
  "Get personalized workout schedules"
]

const normalUserPoints = [
  "Choose fitness goals",
  "Earn XP through workouts and daily activities",
  "Progress through Bronze, Silver, Gold level",
  "Access recipes based on your level"
]

const coachPoints = [
  "Design custom workout programs",
  "Assign daily workout schedules to members",
  "Monitor member progress and completion rates",
  "View and comment on client food posts",
  "Post recipes for the community"
]

function select(role) {
  console.log('Selected:', role)
  router.push('/about-you')
}

async function selectRole(role) {
  try {
    await fetch("/api/set-role/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ role }),
    })

    // after setting role, go to About You page
    router.push("/about-you")
  } catch (error) {
    console.error(error)
    alert("Error setting role")
  }
}

</script>