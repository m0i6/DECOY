<script setup>
import Driver from 'driver.js'
import 'driver.js/dist/driver.css'

const driver = new Driver({
  animate: true,
  allowClose: true,
  overlayClickNext: false,
  showProgress: true,
  doneBtnText: 'Finish',
  nextBtnText: 'Next →',
  prevBtnText: '← Back'
})

function startTour() {
  driver.defineSteps([
    {
      element: '#navbar',
      popover: {
        title: 'Navigation Bar',
        description: 'Use this bar to move between sections of the app.'
      }
    },
    {
      element: '#search-box',
      popover: {
        title: 'Search',
        description: 'Type here to search through your data.'
      }
    },
    {
      element: '#settings-btn',
      popover: {
        title: 'Settings',
        description: 'Click here to configure preferences.'
      }
    }
  ])

  driver.start()
}
</script>

<template>
  <div>
    <button @click="startTour">Start Tour</button>
    <nav id="navbar">...</nav>
    <input id="search-box" placeholder="Search..." />
    <button id="settings-btn">⚙️</button>
  </div>
</template>
