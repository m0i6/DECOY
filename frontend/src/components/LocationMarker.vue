<script setup lang="ts">
import { defineProps } from 'vue'

const props = defineProps({
  color: {
    type: String,
    default: '#e8e1a7',
  },
  isMovable: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
    svg width="200" height="200" viewBox="0 0 200 200">
      <circle cx="100" cy="100" r="5" :fill="color"/>
      <circle cx="100" cy="100" r="100" :fill="color" opacity="0.2">
        <animate attributeName="r" from="15" to="100" dur="1.5s" repeatCount="indefinite" />
        <animate attributeName="opacity" from="0.2" to="0" dur="1.5s" repeatCount="indefinite" />
      </circle>
</template>