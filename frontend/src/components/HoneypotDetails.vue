<script setup lang="ts">
import type { HoneypotType } from "../types"
defineProps<{ honeypot: HoneypotType }>()
</script>

<template>
  <div class="bg-[#121313] text-white p-6 rounded-xl shadow-lg h-full overflow-y-auto">
    <!-- Header -->
  <div class="flex items-center justify-between mb-6">
    <h2 class="text-xl font-bold">{{ honeypot.name }}</h2>
  </div>

    <!-- Kategorie -->
    <div class="mb-4">
      <h3 class="text-sm text-slate-400 uppercase tracking-wide mb-1">Kategorie</h3>
      <p class="text-base">{{ honeypot.server_category }}</p>
    </div>

    <!-- Creation Date -->
    <div class="mb-4">
      <h3 class="text-sm text-slate-400 uppercase tracking-wide mb-1">Erstellt am</h3>
      <p class="text-base">{{ new Date(honeypot.creation_date).toLocaleString() }}</p>
    </div>

     <!-- Beschreibung -->
    <div v-if="honeypot.description" class="mb-4">
      <h3 class="text-sm text-slate-400 uppercase tracking-wide mb-1">Beschreibung</h3>
      <p class="text-base text-slate-200">{{ honeypot.description }}</p>
    </div>

    <!-- Behaviors -->
    <div v-if="honeypot.behaviors" class="mb-4">
      <h3 class="text-sm text-slate-400 uppercase tracking-wide mb-1">Behaviors</h3>
      <ul class="list-disc list-inside space-y-1 text-slate-200">
        <li v-for="(b, i) in honeypot.behaviors" :key="i">{{ b }}</li>
      </ul>
    </div>
  </div>
</template>