<template>
  <div class="pelotitas-list">
    <div class="list-header">
      <h2>Movimientos de Pelotitas</h2>
      <button
        @click="handleCreate"
        class="btn-primary"
        :disabled="pelotitasStore.loading"
        :class="{ 'is-loading': pelotitasStore.loading }"
      >
        <Icon icon="mdi:plus" width="20" height="20" />
        {{ pelotitasStore.loading ? 'Cargando...' : 'Nueva Operación' }}
      </button>
    </div>

    <div v-if="pelotitasStore.loading" class="loading">Cargando...</div>
    <div v-else-if="pelotitasStore.error" class="error">{{ pelotitasStore.error }}</div>
    <div v-else-if="pelotitasStore.pelotitas.length === 0" class="empty">
      No hay movimientos registrados
    </div>
    <table v-else class="data-table">
      <thead>
        <tr>
          <th>Fecha</th>
          <th>Tipo</th>
          <th>Cantidad</th>
          <th>Precio Unit.</th>
          <th>Total</th>
          <th>Proveedor</th>
          <th>Comprador</th>
          <th>Observaciones</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="pelotita in pelotitasStore.pelotitas" :key="pelotita.id">
          <td>{{ formatDate(pelotita.fecha) }}</td>
          <td>
            <span class="badge" :class="pelotita.tipo">
              {{ pelotita.tipo === 'compra' ? 'Compra' : 'Venta' }}
            </span>
          </td>
          <td class="text-right">{{ pelotita.cantidad }}</td>
          <td class="text-right">${{ formatMoney(pelotita.precio_unitario) }}</td>
          <td class="text-right"><strong>${{ formatMoney(pelotita.total) }}</strong></td>
          <td>{{ pelotita.proveedor || '-' }}</td>
          <td>{{ pelotita.comprador_nombre || '-' }}</td>
          <td>{{ pelotita.observaciones || '-' }}</td>
          <td class="actions">
            <button @click="$emit('showView', pelotita.id)" class="btn-icon" title="Ver">
              <Icon icon="mdi:eye" width="18" height="18" />
            </button>
            <button @click="$emit('showEdit', pelotita.id)" class="btn-icon" title="Editar">
              <Icon icon="mdi:pencil" width="18" height="18" />
            </button>
            <button @click="handleDelete(pelotita.id!)" class="btn-icon btn-delete" title="Eliminar">
              <Icon icon="mdi:delete" width="18" height="18" />
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="pelotitasStore.pelotitas.length > 0" class="pagination-controls">
      <button
        @click="goToPage(pelotitasStore.currentPage - 1)"
        :disabled="pelotitasStore.currentPage <= 1"
        class="btn-pagination"
      >
        <Icon icon="mdi:chevron-left" width="20" height="20" />
        Anterior
      </button>
      <span class="pagination-info">Pagina {{ pelotitasStore.currentPage }} de {{ pelotitasStore.totalPages }}</span>
      <button
        @click="goToPage(pelotitasStore.currentPage + 1)"
        :disabled="pelotitasStore.currentPage >= pelotitasStore.totalPages"
        class="btn-pagination"
      >
        Siguiente
        <Icon icon="mdi:chevron-right" width="20" height="20" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { Icon } from '@iconify/vue'
import { usePelotitasStore } from '@/stores/pelotitas'

const emit = defineEmits(['showCreate', 'showEdit', 'showView'])
const pelotitasStore = usePelotitasStore()

const resumen = computed(() => pelotitasStore.resumen)

const stockActual = computed(() => {
  const compras = resumen.value.find(r => r.tipo === 'compra')
  const ventas = resumen.value.find(r => r.tipo === 'venta')
  const totalCompras = compras?.total_cantidad || 0
  const totalVentas = ventas?.total_cantidad || 0
  return totalCompras - totalVentas
})

onMounted(async () => {
  await pelotitasStore.fetchPelotitas()
  await pelotitasStore.fetchResumen()
})

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-AR', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

const formatMoney = (value: number | null | undefined) => {
  if (!value) return '0.00'
  return Number(value).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, '.')
}

const handleDelete = async (id: number) => {
  if (confirm('¿Está seguro de eliminar este movimiento?')) {
    try {
      await pelotitasStore.deletePelotita(id)
      await pelotitasStore.fetchResumen()
    } catch (error) {
      console.error('Error al eliminar:', error)
    }
  }
}

const goToPage = async (page: number) => {
  if (page >= 1 && page <= pelotitasStore.totalPages) {
    await pelotitasStore.fetchPelotitas(page)
  }
}

const handleCreate = () => {
  if (!pelotitasStore.loading) {
    emit('showCreate')
  }
}
</script>

<style scoped>
.pelotitas-list {
  padding: 1.5rem;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.list-header h2 {
  color: #022F9D;
  margin: 0;
}

.resumen-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.resumen-card {
  background: #fff;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-left: 4px solid;
}

.resumen-card.compra {
  border-left-color: #4CAF50;
}

.resumen-card.venta {
  border-left-color: #FF9800;
}

.resumen-card.stock {
  border-left-color: #2196F3;
}

.resumen-card h3 {
  margin: 0 0 1rem 0;
  color: #022F9D;
  font-size: 1.1rem;
}

.resumen-stat {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.resumen-stat .label {
  color: #666;
  font-size: 0.9rem;
}

.resumen-stat .value {
  font-weight: 600;
  color: #022F9D;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
  display: inline-block;
}

.badge.compra {
  background: #E8F5E9;
  color: #2E7D32;
}

.badge.venta {
  background: #FFF3E0;
  color: #E65100;
}

.text-right {
  text-align: right;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.data-table thead {
  background: #022F9D;
  color: white;
}

.data-table th,
.data-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table tbody tr:hover {
  background: #f5f5f5;
}

.actions {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.btn-icon {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: #022F9D;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.btn-icon:hover {
  background: #e3f0fc;
  color: #00CDFF;
}

.btn-delete:hover {
  background: #ffebee;
  color: #c62828;
}

.btn-primary {
  background: #00CDFF;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: #00B8E6;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 205, 255, 0.3);
}

.btn-primary:disabled,
.btn-primary.is-loading {
  position: relative;
  padding-left: 2.2rem;
  opacity: 0.65;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-primary.is-loading::before {
  content: '';
  position: absolute;
  left: 0.85rem;
  top: 50%;
  width: 0.9rem;
  height: 0.9rem;
  margin-top: -0.45rem;
  border: 2px solid rgba(255, 255, 255, 0.45);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  margin-top: 1rem;
  padding: 1rem;
}

.btn-pagination {
  background: #022F9D;
  color: white;
  border: none;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.btn-pagination:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  color: #022F9D;
  font-weight: 600;
}

.loading,
.error,
.empty {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.error {
  color: #c62828;
}
</style>
