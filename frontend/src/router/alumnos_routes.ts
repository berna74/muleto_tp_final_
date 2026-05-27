import type { RouteRecordRaw } from 'vue-router'

const alumnosRoutes: RouteRecordRaw[] = [
  {
    path: '/alumnos',
    name: 'alumnos',
    component: () => import('@/views/AlumnosView.vue')
  }
]

export default alumnosRoutes
