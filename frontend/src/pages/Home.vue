<script setup lang="ts">
import HoneypotList from '../components/HoneypotList.vue'
import WorldMap from '../components/WorldMap.vue'
</script>

<template>
    <!-- Linke Spalte: Honeypot Liste -->
    <div class="w-1/4">
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
</template>