<template>
  <div class="bg-slate-800 h-full p-4">
    <h2 class="text-lg font-semibold text-white mb-4">Honeypots</h2>
    <ul>
      <li
        v-for="(sensor, index) in uniqueSensors"
        :key="sensor"
        @click="selectSensor(sensor)"
        class="cursor-pointer px-3 py-2 mb-2 rounded-lg"
        :class="sensor === selectedSensor ? 'bg-cyan-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'"
      >
        {{ sensor }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import mockData from '../data/mockCowrieEvents.json'
const selectedSensor = ref(null)

// Alle eindeutigen Honeypots (Sensor-Namen)
const uniqueSensors = computed(() => {
  return Array.from(new Set(mockData.map(e => e.sensor)))
})

function selectSensor(sensor) {
  selectedSensor.value = sensor
  console.log('Selected sensor:', sensor)
  // später um Detailansicht zu öffnen
}
</script>