<template>
  <nav class="bg-[#09060B] text-900 px-6 py-3 flex items-center justify-between">
    <!-- Left: Logo / Title -->
    <div class="flex items-center space-x-3">
      <!-- Logo Icon -->
      <img src="../assets/deciv.svg" alt="Logo" class="h-7 w-7 text-cyan-400" />
      <span class="text-xl font-bold text-white">deciv.eu</span>
    </div>

    <!-- Right: Navigation -->
    <div class="hidden md:flex items-center space-x-6">
      <router-link to="/" class="text-slate-300 hover:text-white">Dashboard</router-link>
      <router-link to="/deployment" class="text-slate-300 hover:text-white">Deploy</router-link>
      <router-link to="/about" class="text-slate-300 hover:text-white">About</router-link>
    </div>
  </nav>
</template>