<template>
<aside
    class="fixed inset-y-0 left-0 z-50 w-72 bg-slate-900 font-subtitle text-white transition-transform duration-300"
    :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
    aria-label="Sidebar"
    >
    <div class="px-6 pb-6 pt-8 border-b border-white/10 flex items-center justify-between">
    <h1 class="text-xl font-bold text-blue-400">HealthQuest Admin</h1>
    <!-- Close button for mobile -->
    <button
      class="md:hidden text-white text-xl"
      @click="$emit('close')"
      aria-label="Close sidebar"
    >
      <icons.X class="w-6 h-6" />
    </button>
    </div>

    <nav class="px-2 py-6 space-y-8 overflow-y-auto h-[calc(100vh-88px)]">
    <div v-for="group in nav" :key="group.title" class="space-y-2">
        <div class="px-4 text-[11px] font-semibold tracking-wider uppercase text-slate-400">
        {{ group.title }}
        </div>

        <RouterLink
            v-for="item in group.items"
            :key="item.id"
            :to="item.path"
            class="group flex items-center gap-3 rounded-md px-4 py-2.5 text-slate-300 hover:text-blue-400 hover:bg-blue-500/10 border-r-2 border-transparent"
            :class="activeSection === item.id ? 'bg-blue-500/10 text-blue-400 border-blue-500' : ''"
            >
            <span class="w-5 h-5 shrink-0">
              <component :is="icons[item.icon]" class="w-full h-full" />
            </span>
            <span class="truncate">{{ item.label }}</span>
            <span
                v-if="item.badge"
                class="ml-auto rounded-full px-2 py-0.5 text-[11px] font-medium bg-rose-500 text-white"
            >
                {{ item.badge }}
            </span>
        </RouterLink>
    </div>
    </nav>
</aside>
</template>

<script setup>
import * as icons from "lucide-vue-next";
defineProps({
  sidebarOpen: Boolean,
  activeSection: String,
})

defineEmits(['close', 'select'])

const nav = [
  {
    items: [
      { id: 'users', label: 'Users', icon: 'Users', path: '/admin-user' }, 
    ]
  },
  {
    title: 'Content Management',
    items: [
      { id: 'coaches', label: 'Certificates', icon: 'StickyNote', path: '/admin-certification' },
      { id: 'workouts', label: 'Workouts', icon: 'Dumbbell', path: '/admin-workout' },
      { id: 'recipes', label: 'Recipes', icon: 'Utensils', path: '/admin-recipe' },
    ]
  },
]

</script>

