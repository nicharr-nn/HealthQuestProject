<template>
    <div class="relative" ref="bellContainer">
      <!-- Bell Icon with Badge -->
      <button
        @click="toggleDropdown"
        :class="[
          'relative p-2 rounded-full flex items-center justify-center transition-all hover:bg-blue-100',
          pendingCount > 0 ? 'animate-bounce' : ''
        ]"
      >
        <Bell class="w-6 h-6 text-gray-700" />
        <span
          v-if="pendingCount > 0"
          class="absolute top-0 right-0 bg-red-500 text-white text-xs font-bold px-1.5 h-4 min-w-[18px] flex items-center justify-center rounded-full shadow"
        >
          {{ pendingCount > 99 ? '99+' : pendingCount }}
        </span>
      </button>
  
      <!-- Dropdown -->
      <transition name="fade">
        <div
          v-if="showDropdown"
          class="absolute right-0 mt-2 w-72 max-h-80 bg-white rounded-xl shadow-xl overflow-hidden z-50"
        >
          <div class="p-3 border-b border-slate-100 font-semibold text-slate-700">
            Notifications
          </div>
  
          <div class="max-h-64 overflow-y-auto">
            <BellOff v-if="pendingCoaches.length === 0" class="w-12 h-12 text-slate-300 mx-auto my-5" />
            <div v-if="pendingCoaches.length === 0" class="p-4 text-center text-slate-500 text-sm">
              No new certification requests
            </div>
  
            <div
              v-for="coach in pendingCoaches"
              :key="coach.coach_id"
              class="px-4 py-3 hover:bg-slate-50 border-b border-slate-100 cursor-pointer"
              @click="goToCertification(coach)"
            >
              <div class="font-medium text-slate-800">{{ coach.name }}</div>
              <div class="text-xs text-slate-500">submitted a certification request</div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { Bell, BellOff } from 'lucide-vue-next'
  
  const router = useRouter()
  const showDropdown = ref(false)
  const coaches = ref([])
  
  const toggleDropdown = () => { 
    showDropdown.value = !showDropdown.value
    if (showDropdown.value) fetchCoaches()
  }
  
  const fetchCoaches = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/moderation/coaches/', { credentials: 'include' })
      if (!res.ok) throw new Error('Failed to fetch coaches')
      coaches.value = await res.json()
    } catch (err) {
      console.error(err)
      coaches.value = []
    }
  }
  
  const pendingCoaches = computed(() => coaches.value.filter(c => c.status_approval === 'pending'))
  const pendingCount = computed(() => pendingCoaches.value.length)
  
  const goToCertification = (coach) => {
    showDropdown.value = false
    router.push({ path: '/admin-certification', query: { coachId: coach.coach_id } })
  }
  
  onMounted(fetchCoaches)
  </script>
  
  <style scoped>
  .fade-enter-active,
  .fade-leave-active {
    transition: 0.15s ease;
  }
  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
    transform: translateY(-5px);
  }
  </style>
  