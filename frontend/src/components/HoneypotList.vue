<script setup lang="ts">
import { ref, onMounted } from "vue"
import { getHoneypots } from "../backendProxy"
import type { HoneypotType } from "../types"

const emit = defineEmits<{ (e: "sensor-selected", honeypot: HoneypotType): void }>()

const honeypots = ref<HoneypotType[]>([])
const selectedLocal = ref<string>("")
const searchQuery = ref("")

onMounted(async () => {
  try {
    honeypots.value = await getHoneypots()
  } catch (err) {
    console.error("Failed to fetch honeypots:", err)
  }
})

function selectSensor(h: HoneypotType) {
  selectedLocal.value = h.name
  emit("sensor-selected", h)
}
</script>

<template>
  <div class="bg-[#121313] h-screen overflow-scroll p-4">
    <h2 class="text-xl font-semibold text-amber-200 mb-4">Honeypots</h2>

    <!-- Searchbar -->
    <div class="relative mb-4">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search..."
        class="w-full bg-[#1a1a1a] text-slate-200 rounded-full pl-10 pr-4 py-2
               border border-[#464746] focus:outline-none focus:ring-2 focus:ring-[#EFE6A1]"
      />
      <svg
        class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-[#464746] pointer-events-none"
        fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round"
              d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1010.5 3a7.5 7.5 0 006.15 13.65z"/>
      </svg>
    </div>

    <ul>
      <li
        v-for="h in honeypots.filter(h => h.name.toLowerCase().includes(searchQuery.toLowerCase()))"
        :key="h.id"
        @click="selectSensor(h)"
        class="cursor-pointer px-3 py-2 mb-2 rounded-lg text-slate-300 transition-colors"
        :class="{
          'bg-slate-600 text-white': h.name === selectedLocal,
          'hover:bg-slate-700 hover:text-white': h.name !== selectedLocal
        }"
      >
        {{ h.name }}
      </li>
    </ul>
  </div>
</template>