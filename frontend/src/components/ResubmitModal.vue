<template>
    <div
      v-if="show"
      class="fixed inset-0 bg-black/30 flex items-center justify-center z-50 p-4"
      @click.self="close"
    >
      <div class="bg-gradient-to-br from-pink-50 to-purple-50 rounded-2xl shadow-2xl w-full max-w-md p-6 sm:p-8 relative border-2 border-pink-200">
        <button @click="close" class="absolute top-3 right-3 text-black text-xl cursor-pointer">×</button>
        <div class="flex items-center justify-center gap-2 mb-2">
          <Siren class="w-7 h-7 -mt-1 text-black" />
          <h2 class="text-xl sm:text-2xl font-bold text-center text-black">{{ title }}</h2>
        </div>
        <p class="text-center text-gray-600 mb-6">{{ message }}</p>
        <div class="flex flex-col sm:flex-row gap-3">
          <button @click="close" class="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-3 rounded-xl transition"> {{ cancelText }} </button>
          <button @click="confirm" class="flex-1 bg-pink-200 hover:bg-pink-400 font-semibold py-3 rounded-xl transition"> {{ confirmText }} </button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps, defineEmits } from 'vue'
  import { Siren } from 'lucide-vue-next'
  
  defineProps({
    show: Boolean,
    title: String,
    message: String,
    confirmText: { type: String, default: 'Confirm' },
    cancelText: { type: String, default: 'Cancel' },
  })
  
  const emit = defineEmits(['update:show', 'confirm', 'close'])
  
  const close = () => emit('update:show', false) && emit('close')
  const confirm = () => emit('confirm') && emit('update:show', false)
  </script>
  