<template>
  <div ref="mapContainer" :class="props.widthClass" style="min-height:400px;"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'

const mapContainer = ref(null)
let map: any

const props = defineProps({
  widthClass: String
})

onMounted(() => {
  if (!mapContainer?.value) return;
  map = new maplibregl.Map({
    container: mapContainer.value,
    style: "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
    zoom: 1.5
  })

  // Controls
  map.addControl(new maplibregl.NavigationControl())

  // Marker aus Mockdaten
  // mockData.forEach(event => {
  //   if (!event.geo) return
  //   new maplibregl.Marker({ color: '#f43f5e' })
  //     .setLngLat([event.geo.lon, event.geo.lat])
  //     .setPopup(
  //       new maplibregl.Popup().setHTML(`
  //         <div style="font-size:12px;">
  //           <b>IP:</b> ${event.source_ip}<br>
  //           <b>Land:</b> ${event.country}<br>
  //           <b>Protocol:</b> ${event.protocol}<br>
  //           <b>Event:</b> ${event.event_type}
  //         </div>
  //       `)
  //     )
  //     .addTo(map)
  // })
})

onBeforeUnmount(() => {
  if (map) map.remove()
})
</script>