<template>
  <div class="bg-white rounded-2xl p-6 shadow hover:-translate-y-0.5 transition">
    <!-- Header -->
    <div class="flex items-start justify-between mb-4">
      <div class="text-lg font-bold text-slate-800">{{ title }}</div>
      <div
        v-if="badge"
        class="px-2.5 py-1 rounded-lg text-[10px] font-extrabold"
        :class="badgeClass"
      >
        {{ badge }}
      </div>
    </div>

    <!-- Main Content -->
    <div class="text-gray-600 mb-4 leading-relaxed">
      <slot name="content">{{ content }}</slot>
    </div>

    <!-- Extra slot (e.g., stats or progress bars) -->
    <slot />

    <!-- Footer (button or info) -->
    <div v-if="$slots.footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardCard',
  props: {
    title: { type: String, required: true },
    badge: { type: String, default: null },
    badgeType: { type: String, default: 'neutral' }, // neutral | new | silver | gold
    content: { type: String, default: '' }
  },
  computed: {
    badgeClass() {
      switch (this.badgeType) {
        case 'new':
          return 'bg-emerald-500 text-white'
        case 'silver':
          return 'bg-gradient-to-br from-neutral-300 to-neutral-400 text-white'
        case 'gold':
          return 'bg-gradient-to-br from-amber-400 to-yellow-500 text-white'
        default:
          return 'bg-gray-100 text-gray-500'
      }
    }
  }
}
</script>
