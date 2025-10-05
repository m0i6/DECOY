<script setup lang="ts">
import { ref } from 'vue'
import HoneypotList from '../components/HoneypotList.vue'
import WorldMap from '../components/WorldMap.vue'
import HoneypotDetails from '../components/HoneypotDetails.vue'
import type { HoneypotType } from '../types'

const selectedHoneypot = ref<HoneypotType | null>(null)

function handleSensorSelected(honeypot: HoneypotType) {
  selectedHoneypot.value = honeypot
}
</script>

<template>
  <div class="flex flex-1">
    <!-- Linke Spalte: Honeypot Liste -->
    <div class="w-1/4">
      <HoneypotList @sensor-selected="handleSensorSelected" />
    </div>

    <!-- Rechte Spalte: Map nimmt Rest ein -->
    <div class="relative flex-1">
      <WorldMap widthClass="h-full w-full" />

      <!-- Details Overlay -->
      <div v-if="selectedHoneypot" class="fixed top-20 bottom-10 right-10 w-96 z-40">
        <HoneypotDetails :honeypot="selectedHoneypot" />
      </div>

      <!-- KPI Overlay -->
      <div class="absolute top-4 right-4 flex flex-col gap-4 w-48">
            <div class="bg-slate-800 bg-opacity-80 text-white p-4 rounded-lg shadow">
                <h3 class="text-sm font-semibold">Total Attacks</h3>
                <p class="text-xl font-bold">134</p>
            </div>
            <div class="bg-slate-800 bg-opacity-80 text-white p-4 rounded-lg shadow">
                <h3 class="text-sm font-semibold">Active Honeypots</h3>
                <p class="text-xl font-bold">5</p>
            </div>
            <div class="bg-slate-800 bg-opacity-80 text-white p-4 rounded-lg shadow">
                <h3 class="text-sm font-semibold">Unique IPs</h3>
                <p class="text-xl font-bold">67</p>
            </div>
        </div>
    </div>
  </div>
</template>