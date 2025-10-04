<template>
  <div ref="mapContainer" :class="props.widthClass" style="min-height:400px;"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import mockData from '../data/mockCowrieEvents.json'
import { getHoneypots } from '../backendProxy'

const mapContainer = ref(null)
let map: maplibregl.Map | null = null
let userMarker: maplibregl.Marker | null = null
let geolocateControl: maplibregl.GeolocateControl | null = null

const props = defineProps({
  widthClass: String,
  hasDynamicInput: Boolean
})

const emit = defineEmits(['update-geolocation'])

const createCustomMarker = (color: string) => {
  const el = document.createElement('div')
    el.innerHTML = `
    <svg width="200" height="200" viewBox="0 0 200 200">
      <circle cx="100" cy="100" r="5" fill="${color}"/>
      <circle cx="100" cy="100" r="100" fill="${color}" opacity="0.2">
        <animate attributeName="r" from="15" to="100" dur="1.5s" repeatCount="indefinite" />
        <animate attributeName="opacity" from="0.2" to="0" dur="1.5s" repeatCount="indefinite" />
      </circle>
    </svg>`
  el.className = 'custom-marker'
  return el
}

onMounted(async () => {
  map = new maplibregl.Map({
    container: mapContainer.value || '',
    style: "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
    zoom: 1.5
  })

  if (props.hasDynamicInput) {
    // Optional: add a geolocate control
    geolocateControl = new maplibregl.GeolocateControl({
      positionOptions: { enableHighAccuracy: true },
      trackUserLocation: true,
    })
    map.addControl(geolocateControl)
    // Click handler: place or move marker
    const updateGeolocation = (e: any) => {
      const coords = e.lngLat
      console.log('Clicked coordinates:', coords)
      emit('update-geolocation', `${coords.lat},${coords.lng}`)

      // If a user marker exists, move it
      if (userMarker) {
        userMarker.setLngLat(coords)
      } else {
        // Otherwise, create a new marker
        if (!map) return
        userMarker = new maplibregl.Marker({ element: createCustomMarker('#e8e1a7'), draggable: true })
          .setLngLat(coords)
          .addTo(map)
      }
    }
    // map.on('click', updateGeolocation)
    map.on('mouseup', updateGeolocation)
  } else {
    // draw all markers of the honeypots
    const honeypots = await getHoneypots()
    honeypots.forEach(honeypot => {
      if (!honeypot.geolocation || !map) return
      const [lat, lon] = honeypot.geolocation.split(',').map(coord => parseFloat(coord.trim()))
      new maplibregl.Marker({ element: createCustomMarker('#e8e1a7') })
        .setLngLat([lon || 0, lat || 0])
        .addTo(map)
    })
  }

  // Marker aus Mockdaten
  mockData.forEach((event: any) => {
    if (!event.geo || !map) return
    new maplibregl.Marker({ color: '#f43f5e' })
      .setLngLat([event.geo.lon, event.geo.lat])
      .setPopup(
        new maplibregl.Popup().setHTML(`
          <div style="font-size:12px;">
            <b>IP:</b> ${event.source_ip}<br>
            <b>Land:</b> ${event.country}<br>
            <b>Protocol:</b> ${event.protocol}<br>
            <b>Event:</b> ${event.event_type}
          </div>
        `)
      )
      .addTo(map)
  })
})


onBeforeUnmount(() => {
  if (map) map.remove()
})
</script>