import type { RouteRecordRaw } from 'vue-router'

const pagosRoutes: RouteRecordRaw[] = [
  {
    path: '/pagos',
    name: 'pagos',
    component: () => import('@/views/PagosView.vue')
  }
]

export default pagosRoutes
