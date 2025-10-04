<template>
  <nav class="bg-[#09060B] text-900 px-6 py-3 flex items-center justify-between">
    <!-- Left: Logo / Title -->
    <div class="flex items-center space-x-3">
      <!-- Logo Icon -->
      <img src="../assets/devic.svg" alt="Logo" class="h-7 w-7 text-cyan-400" />
      <span class="text-xl font-bold text-white">deciv.ai</span>
    </div>

    <!-- Right: Navigation -->
    <div class="hidden md:flex items-center space-x-6">
      <router-link to="/" class="text-slate-300 hover:text-white">Dashboard</router-link>
      <router-link to="/deployment" class="text-slate-300 hover:text-white">Deploy</router-link>
      <router-link to="/about" class="text-slate-300 hover:text-white">About</router-link>
    </div>

    <!-- Right: Actions -->
    <div class="flex items-center space-x-4">
      <button
        @click="simulateAttack"
        class="px-3 py-1.5 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-semibold text-sm"
      >
        Simulate Attack
      </button>
    </div>
  </nav>
</template>

<script setup lang="ts">
// Beispiel: Emit Event zum Parent oder Dummy-Funktion
function simulateAttack() {
  console.log("Simulate attack triggered (Navbar)")
}
</script>