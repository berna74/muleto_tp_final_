import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import turnos_routes from './turnos_routes'
import socios_routes from './socios_routes'
import categorias_routes from './categorias_routes'
import profesores_routes from './profesores_routes'
import alumnos_routes from './alumnos_routes'
import pagos_routes from './pagos_routes'
import pelotitas_routes from './pelotitas_routes'

// Club de Tenis - Sistema de Administración

const routes = [
  { path: '/', name: 'home', component: HomeView },
  ...turnos_routes,
  ...socios_routes,
  ...categorias_routes,
  ...profesores_routes,
  ...alumnos_routes,
  ...pagos_routes,
  ...pelotitas_routes
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router