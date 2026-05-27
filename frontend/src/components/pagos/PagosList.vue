<template>
  <div class="pagos-list">
    <div class="list-header">
      <h2>Registro de Pagos</h2>
      <button @click="handleCreate" class="btn-create" :disabled="loading" :class="{ 'is-loading': loading }">
        <Icon icon="mdi:plus" width="20" height="20" />
        {{ loading ? 'Cargando...' : 'Registrar Pago' }}
      </button>
    </div>
    
    <div v-if="loading" class="loading">Cargando pagos...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="pagos.length === 0" class="empty">No hay pagos registrados</div>
    
    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Tipo</th>
            <th>Monto</th>
            <th>Fecha Pago</th>
            <th>Período</th>
            <th>Pagado por</th>
            <th>Profesor</th>
            <th>Método</th>
            <th>Observaciones</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pago in pagos" :key="pago.id">
            <td>{{ pago.id }}</td>
            <td>
              <span :class="['badge-tipo', getTipoBadgeClass(pago.tipo)]">
                {{ formatTipo(pago.tipo) }}
              </span>
            </td>
            <td class="monto">${{ formatMonto(pago.monto) }}</td>
            <td>{{ formatDate(pago.fecha_pago) }}</td>
            <td>{{ formatPeriodo(pago.mes, pago.anio) }}</td>
            <td>{{ getBeneficiario(pago) }}</td>
            <td>{{ pago.profesor_nombre || '-' }}</td>
            <td>{{ pago.metodo_pago || '-' }}</td>
            <td class="observaciones">{{ pago.observaciones || '-' }}</td>
            <td class="actions">
              <button @click="$emit('show', pago.id)" class="btn-icon" title="Ver">
                <Icon icon="mdi:eye" width="18" height="18" />
              </button>
              <button @click="$emit('edit', pago.id)" class="btn-icon" title="Editar">
                <Icon icon="mdi:pencil" width="18" height="18" />
              </button>
              <button @click="handleDelete(pago.id)" class="btn-icon btn-delete" title="Eliminar">
                <Icon icon="mdi:delete" width="18" height="18" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="pagination-controls">
        <button @click="goToPage(currentPage - 1)" :disabled="currentPage <= 1" class="btn-pagination">
          <Icon icon="mdi:chevron-left" width="20" height="20" />
          Anterior
        </button>
        <span class="pagination-info">Pagina {{ currentPage }} de {{ totalPages }}</span>
        <button @click="goToPage(currentPage + 1)" :disabled="currentPage >= totalPages" class="btn-pagination">
          Siguiente
          <Icon icon="mdi:chevron-right" width="20" height="20" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { Icon } from '@iconify/vue'
import { usePagosStore } from '@/stores/pagos'
import { storeToRefs } from 'pinia'
import type { Pago } from '@/interfaces/Pago'

const emit = defineEmits(['create', 'show', 'edit'])
const pagosStore = usePagosStore()
const { pagos, loading, error, currentPage, totalPages } = storeToRefs(pagosStore)

onMounted(() => {
  pagosStore.fetchPagos()
})

function formatTipo(tipo: string): string {
  return tipo
}

function getTipoBadgeClass(tipo: string): string {
  const classes: Record<string, string> = {
    'Cuota Social': 'badge-cuota',
    'Abono Mensual': 'badge-mensual',
    'Abono Diario': 'badge-diario',
    'Clase': 'badge-clase'
  }
  return classes[tipo] || 'badge-default'
}

function formatMonto(monto: number): string {
  return new Intl.NumberFormat('es-AR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(monto)
}

function formatDate(dateString: string): string {
  const date = new Date(dateString + 'T00:00:00')
  return date.toLocaleDateString('es-AR')
}

function formatPeriodo(mes: number, anio: number): string {
  const meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
  return `${meses[mes - 1]} ${anio}`
}

function getBeneficiario(pago: Pago): string {
  if (pago.socio_nombre) return `Socio: ${pago.socio_nombre}`
  if (pago.alumno_nombre) return `Alumno: ${pago.alumno_nombre}`
  return '-'
}

async function handleDelete(id: number) {
  if (confirm('¿Está seguro de eliminar este pago?')) {
    try {
      await pagosStore.deletePago(id)
    } catch (e) {
      console.error('Error al eliminar pago:', e)
    }
  }
}

function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    pagosStore.fetchPagos(page)
  }
}

function handleCreate() {
  if (!loading.value) {
    emit('create')
  }
}
</script>

<style scoped>
.pagos-list {
  padding: 20px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h2 {
  color: #022F9D;
  margin: 0;
}

.btn-create {
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

.btn-create:hover {
  background: #00B8E6;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 205, 255, 0.3);
}

.btn-create:disabled,
.btn-create.is-loading {
  position: relative;
  padding-left: 2.2rem;
  opacity: 0.65;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-create.is-loading::before {
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

.table-container {
  overflow-x: auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background-color: #022F9D;
  color: white;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #CCCCCC;
}

th {
  font-weight: bold;
}

tbody tr:hover {
  background-color: #f5f5f5;
}

.badge-tipo {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  display: inline-block;
}

.badge-cuota {
  background-color: #022F9D;
  color: white;
}

.badge-mensual {
  background-color: #00CDFF;
  color: #000000;
}

.badge-diario {
  background-color: #FFCD00;
  color: #000000;
}

.badge-clase {
  background-color: #28a745;
  color: white;
}

.badge-default {
  background-color: #6c757d;
  color: white;
}

.monto {
  font-weight: bold;
  color: #28a745;
}

.observaciones {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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

.loading, .error, .empty {
  text-align: center;
  padding: 40px;
  color: #666;
}

.error {
  color: #dc3545;
}
</style>
