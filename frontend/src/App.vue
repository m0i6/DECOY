<script setup lang="ts">
import Navbar from './components/Navbar.vue'
import HoneypotList from './components/HoneypotList.vue'
import WorldMap from './components/WorldMap.vue'
</script>

<template>
  <div id="app" class="h-screen flex flex-col bg-slate-900">
    <!-- Row 1: Navbar -->
    <Navbar />

    <!-- Row 2: Main Content -->
    <div class="flex flex-1">
      <!-- Linke Spalte: Honeypot Liste -->
      <div class="w-1/4 border-r border-slate-700">
        <HoneypotList />
      </div>

      <!-- Mitte: KPI Platzhalter -->
      <div class="w-2/4 p-6 text-white">
        <h2 class="text-xl font-bold mb-4">KPIs</h2>
        <p>Hier kommen die Stat Cards hin...</p>
      </div>

      <!-- Rechte Spalte: Map Platzhalter -->
      <div class="w-1/4 p-6 text-white border-l border-slate-700">
        <h2 class="text-xl font-bold mb-4">Map</h2>
        <WorldMap />
      </div>
    </div>
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
