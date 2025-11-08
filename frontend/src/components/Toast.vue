<template>
  <div class="fixed top-4 right-4 z-[60] space-y-2">
    <div
      v-for="toast in toasts"
      :key="toast.id"
      :class="[
        'px-6 py-4 rounded-lg shadow-lg transform transition-all duration-300',
        'flex items-center gap-3 min-w-[300px]',
        toast.type === 'success' ? 'bg-green-200' : '',
        toast.type === 'error' ? 'bg-red-200 text-black' : '',
        toast.type === 'warning' ? 'bg-yellow-200 text-black' : '',
        toast.type === 'info' ? 'bg-blue-200 text-black' : ''
      ]"
    >
      <span class="flex-1">{{ toast.message }}</span>
      <button @click="removeToast(toast.id)" class="text-black hover:opacity-80 text-xl">×</button>
    </div>
  </div>
</template>

<script setup>
import { useToastStore } from '@/stores/toast'
import { storeToRefs } from 'pinia'

const toastStore = useToastStore()
const { toasts } = storeToRefs(toastStore)
const { removeToast } = toastStore
</script>