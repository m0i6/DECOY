<script setup lang="ts">
import type { HoneypotType } from "../types"
defineProps<{ honeypot: HoneypotType }>()

const emit = defineEmits(['close'])

</script>

<template>
  <div class="bg-[#121313] text-white p-6 rounded-xl shadow-lg h-full overflow-y-auto">
    <!-- Header -->
  <div class="flex items-center justify-between mb-6">
    <h2 class="text-xl font-bold">{{ honeypot.name }}</h2>
  </div>

    <!-- Kategorie -->
    <div class="mb-4">
      <h3 class="text-sm text-gray-300 uppercase tracking-wide mb-1">Kategorie</h3>
      <p class="text-base">{{ honeypot.server_category }}</p>
    </div>

    <!-- Creation Date -->
    <div class="mb-4">
      <h3 class="text-sm text-gray-300 uppercase tracking-wide mb-1">Erstellt am</h3>
      <p class="text-base">{{ new Date(honeypot.creation_date).toLocaleString() }}</p>
    </div>

     <!-- Beschreibung -->
    <div v-if="honeypot.description" class="mb-4">
      <h3 class="text-sm text-gray-300 uppercase tracking-wide mb-1">Beschreibung</h3>
      <p class="text-base text-gray-300">{{ honeypot.description }}</p>
    </div>

    <!-- Behaviors -->
    <div v-if="honeypot.behaviors" class="mb-4">
      <h3 class="text-sm text-gray-300 uppercase tracking-wide mb-1">Behaviors</h3>
      <ul class="list-disc list-inside space-y-1 text-gray-300">
        <li v-for="(b, i) in honeypot.behaviors.split(',')" :key="i">{{ b }}</li>
      </ul>
    </div>

    <!-- button for closing -->
    <div class="absolute top-4 right-4">
      <button @click="$emit('close')" class="text-gray-300 hover:text-white">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </div>
</template>