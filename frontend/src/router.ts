import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'
import Deployment from './pages/Deployment.vue'
import About from './pages/About.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/deployment', name: 'Deployment', component: Deployment },
  { path: '/about', name: 'About', component: About },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router