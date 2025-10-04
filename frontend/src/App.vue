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

      <!-- Rechte Spalte: Map nimmt Rest ein -->
      <div class="relative flex-1">
        <WorldMap />

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
