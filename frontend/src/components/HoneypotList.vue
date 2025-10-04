<template>
  <div class="bg-[#121313] h-full p-4">
    <h2 class="text-lg font-semibold text-[#EFE6A1] mb-4">Honeypots</h2>

    <!-- Searchbar -->
    <div class="relative mb-4">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search Honeypots..."
        class="w-full bg-[#1a1a1a] text-slate-200 rounded-lg pl-10 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#EFE6A1]"
      />
      <svg
        class="w-5 h-5 absolute left-3 top-2.5 text-slate-400"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1010.5 3a7.5 7.5 0 006.15 13.65z"
        />
      </svg>
    </div>

    <ul>
        <li
          v-for="(sensor, index) in uniqueSensors"
          :key="sensor"
          @click="selectSensor(sensor)"
          class="cursor-pointer px-3 py-2 mb-2 rounded-lg text-slate-300 transition-colors"
          :class="{
            'bg-slate-600 text-white': sensor === selectedSensor,
            'hover:bg-slate-700 hover:text-white': sensor !== selectedSensor
          }"
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
