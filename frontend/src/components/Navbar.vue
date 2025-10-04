<template>
  <nav class="bg-slate-900 border-b border-slate-700 px-6 py-3 flex items-center justify-between">
    <!-- Left: Logo / Title -->
    <div class="flex items-center space-x-3">
      <!-- Optional: Logo Icon -->
      <svg class="h-7 w-7 text-cyan-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 2l9 4.5-9 4.5-9-4.5L12 2zm0 9l9 4.5-9 4.5-9-4.5 9-4.5z" />
      </svg>
      <span class="text-xl font-bold text-white">Honeypot SaaS</span>
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
      <span class="hidden sm:inline text-slate-400 text-sm">Team CyberCats 🐱</span>
    </div>
  </nav>
</template>

<script setup>
// Beispiel: Emit Event zum Parent oder Dummy-Funktion
function simulateAttack() {
  console.log("Simulate attack triggered (Navbar)")
}
</script>