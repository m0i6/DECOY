<template>
  <div class="bg-slate-800 h-full p-4">
    <h2 class="text-lg font-semibold text-white mb-4">Honeypots</h2>
    <ul>
      <li
        v-for="sensor in uniqueSensors"
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
import { ref, computed, onMounted } from 'vue'
import { getHoneypots } from '../backendProxy.ts'

const selectedSensor = ref(null)
const honeypots = ref([])

// Fetch honeypots once the component mounts
onMounted(async () => {
  try {
    console.log("gethoneypots")
    console.log(await getHoneypots())
    honeypots.value = await getHoneypots()
  } catch (err) {
    console.error('Failed to fetch honeypots:', err)
  }
})

// Derived list of unique sensors
const uniqueSensors = computed(() => {
  return Array.from(honeypots.value.map(e => e.name))
})

function selectSensor(sensor) {
  selectedSensor.value = sensor
  console.log('Selected sensor:', sensor)
}
</script>
