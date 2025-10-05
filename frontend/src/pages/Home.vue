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

function closeDetails() {
  selectedHoneypot.value = null
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
        <HoneypotDetails :honeypot="selectedHoneypot" @close="closeDetails" />
      </div>

      <!-- KPI Overlay -->
      <div class="absolute top-4 right-4 flex flex-col gap-4 w-60">
        <div class="bg-[#0b0b0b]/90 text-amber-200 p-4 rounded-2xl shadow-[0_8px_30px_rgba(0,0,0,0.4)] ring-1 ring-white/5">
          <h3 class="text-sm font-medium tracking-tight text-white/80">Total Attacks</h3>
          <p class="text-2xl font-bold mt-1 text-amber-200 drop-shadow-[0_0_6px_rgba(255,255,200,0.5)]">134</p>
        </div>

        <div class="bg-[#0b0b0b]/90 text-amber-200 p-4 rounded-2xl shadow-[0_8px_30px_rgba(0,0,0,0.4)] ring-1 ring-white/5">
          <h3 class="text-sm font-medium tracking-tight text-white/80">Active Honeypots</h3>
          <p class="text-2xl font-bold mt-1 text-amber-200 drop-shadow-[0_0_6px_rgba(255,255,200,0.5)]">5</p>
        </div>

        <div class="bg-[#0b0b0b]/90 text-amber-200 p-4 rounded-2xl shadow-[0_8px_30px_rgba(0,0,0,0.4)] ring-1 ring-white/5">
          <h3 class="text-sm font-medium tracking-tight text-white/80">Unique IPs</h3>
          <p class="text-2xl font-bold mt-1 text-amber-200 drop-shadow-[0_0_6px_rgba(255,255,200,0.5)]">67</p>
        </div>
      </div>
    </div>  
  </div>
</template>