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
        ✕
    </button>
    </div>

    <nav class="px-2 py-6 space-y-8 overflow-y-auto h-[calc(100vh-88px)]">
    <div v-for="group in nav" :key="group.title" class="space-y-2">
        <div class="px-4 text-[11px] font-semibold tracking-wider uppercase text-slate-400">
        {{ group.title }}
        </div>

        <a
        v-for="item in group.items"
        :key="item.id"
        href="#"
        class="group flex items-center gap-3 rounded-md px-4 py-2.5 text-slate-300 hover:text-blue-400 hover:bg-blue-500/10 border-r-2 border-transparent"
        :class="activeSection === item.id ? 'bg-blue-500/10 text-blue-400 border-blue-500' : ''"
        @click.prevent="$emit('select', item.id)"
        >
        <span class="w-5 h-5 shrink-0">{{ item.icon }}</span>
        <span class="truncate">{{ item.label }}</span>
        <span
            v-if="item.badge"
            class="ml-auto rounded-full px-2 py-0.5 text-[11px] font-medium bg-rose-500 text-white"
        >
            {{ item.badge }}
        </span>
        </a>
    </div>
    </nav>
</aside>
</template>

<script setup>
defineProps({
  sidebarOpen: Boolean,
  activeSection: String,
})

defineEmits(['close', 'select'])

const nav = [
  { title: 'Overview', items: [{ id: 'dashboard', label: 'Dashboard', icon: '📊' }, { id: 'analytics', label: 'Analytics', icon: '📈' }] },
  { title: 'User Management', items: [{ id: 'users', label: 'Users', icon: '👥' }, { id: 'coaches', label: 'Coaches', icon: '🏃' }] },
  { title: 'Content Management', items: [{ id: 'workouts', label: 'Workouts', icon: '💪' }, { id: 'recipes', label: 'Recipes', icon: '🍽️' }, { id: 'reports', label: 'Reports', icon: '⚠️' }] },
  { title: 'System', items: [{ id: 'settings', label: 'Settings', icon: '⚙️' }, { id: 'logs', label: 'Audit Logs', icon: '📋' }] }
]
</script>

