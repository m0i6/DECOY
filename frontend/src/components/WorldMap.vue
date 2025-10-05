<template>
  <div ref="mapContainer" :class="props.widthClass" style="min-height:400px;"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, type Ref } from 'vue'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import { getHoneypots } from '../backendProxy'
import type { HoneypotType, IncidentLogType } from '../types'
import { BACKEND_ROOT_URL } from "../config"

const mapContainer = ref(null)
let map: maplibregl.Map | null = null
let userMarker: maplibregl.Marker | null = null
let geolocateControl: maplibregl.GeolocateControl | null = null
const honeypots: Ref<Array<HoneypotType>> = ref([])
const incidents: Ref<Array<IncidentLogType>> = ref([])
const markers: Ref<Array<maplibregl.Marker>> = ref([])

const props = defineProps({
  widthClass: String,
  hasDynamicInput: Boolean
})

const emit = defineEmits(['update-geolocation'])

const createCustomMarker = (color: string) => {
  const el = document.createElement('div')
  el.innerHTML = `
    <svg width="100" height="100" viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="5" fill="${color}"/>
      <circle cx="50" cy="50" r="50" fill="${color}" opacity="0.2">
        <animate attributeName="r" from="15" to="25" dur="1.5s" repeatCount="indefinite" />
        <animate attributeName="opacity" from="0.2" to="0" dur="1.5s" repeatCount="indefinite" />
      </circle>
    </svg>`
  el.className = 'custom-marker'
  return el
}

const deleteAllMarkers = () => {
  markers.value.forEach(marker => marker.remove())
  markers.value = []
}

onMounted(async () => {
  // poll for incidents every minute
  setInterval(async () => {
    try {
      const newIncidents = await fetch(BACKEND_ROOT_URL + '/IncidentLogs/').then(res => res.json())
      if (JSON.stringify(newIncidents) !== JSON.stringify(incidents.value)) {
        incidents.value = newIncidents
        console.log('Updated incidents:', incidents.value)
      }
    } catch (err) {
      console.error('Failed to fetch incidents:', err)
    }
  }, 2000) // 2000 ms = 2 seconds
})

// setup polling to update honeypot markers every minute
onMounted(() => {
  setInterval(async () => {
    if (!map || props.hasDynamicInput) return

    // Fetch and add new honeypot markers
    const newHoneypots = await getHoneypots()
    // don't update anything if nothing changed
    if (JSON.stringify(newHoneypots) === JSON.stringify(honeypots.value)) return
    honeypots.value = newHoneypots
    honeypots.value.forEach((honeypot: HoneypotType) => {
      if (!honeypot.geolocation) return
      const [lat, lon] = honeypot.geolocation.split(',').map(coord => parseFloat(coord.trim()))
      // const incidents
      new maplibregl.Marker({ element: createCustomMarker('#e8e1a7'), className: 'honeypot-marker' })
        .setLngLat([lon || 0, lat || 0])
        .addTo(map!)
    })
    // Remove existing honeypot markers
    const existingMarkers = document.getElementsByClassName('honeypot-marker')
    while (existingMarkers[0]) {
      existingMarkers[0].parentNode?.removeChild(existingMarkers[0])
    }

  }, 1500) // 1000 ms = 1 second
})

onMounted(async () => {
  map = new maplibregl.Map({
    container: mapContainer.value || '',
    style: "https://api.maptiler.com/maps/darkmatter/style.json?key=oMCNJnPX9vPcFLw6GzlB",
    zoom: 1.5
  })
  map.addControl(new maplibregl.NavigationControl(), 'bottom-right')
  map.addControl(new maplibregl.ScaleControl(), 'bottom-left')
  map.dragRotate.disable()
})

const setupDynamicInput = () => {
  console.log("setting up dynamic input")
  if (!map) return

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
}

const setupStaticMap = async () => {
  if (!map) return
  deleteAllMarkers()
  // draw all markers of the honeypots
  honeypots.value.forEach((honeypot) => {
    if (!honeypot.geolocation) return
    const [lat, lon] = honeypot.geolocation.split(',').map(coord => parseFloat(coord.trim()))
    const foundIncidents = incidents.value.filter(incident => incident.honeypot_id === honeypot.id)
    const isCritical = foundIncidents.some(incident => incident.severity === 'critical')
    const isModerate = !isCritical && foundIncidents.some(incident => incident.severity === 'moderate')
    const isLow = !isCritical && !isModerate
    let color = '#e8e1a7' // default color
    if (isCritical) color = '#ff4c4c' // red for critical
    else if (isModerate) color = '#ffa500' // orange for moderate
    else if (isLow) color = '#ffff66' // yellow for low
    console.log(`Adding marker for honeypot ${honeypot.name} at ${honeypot.geolocation} with color ${color} (incidents: ${foundIncidents.length}) iscritical: ${isCritical}, isModerate: ${isModerate}, isLow: ${isLow}`)
    new maplibregl.Marker({ element: createCustomMarker(color) })
      .setLngLat([lon || 0, lat || 0])
      .addTo(map!)
  })
}


const setup_everything = async () => {
  if (!map) return
  if (props.hasDynamicInput) {
    setupDynamicInput()
  } else {
    setupStaticMap()
  }
}
watch([honeypots, map], setup_everything)
onMounted(setup_everything)

watch(incidents, () => {
  if (!map || props.hasDynamicInput) return
  // Remove existing incident markers
  setupStaticMap();
})


onBeforeUnmount(() => {
  if (map) map.remove()
})
</script>