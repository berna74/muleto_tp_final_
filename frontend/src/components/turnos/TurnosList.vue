<template>
  <div class="turnos-list">
    <div class="header">
      <h2>Lista de Turnos</h2>
      <button @click="showCreateForm = true" class="btn-primary">
        <Icon icon="mdi:plus" width="20" height="20" />
        Nuevo Turno
      </button>
    </div>

    <TurnosCreate v-if="showCreateForm" @close="showCreateForm = false" @created="handleCreated" />
    <TurnosShow v-if="showingTurnoId" :id="showingTurnoId" @close="showingTurnoId = null" />

    <div v-if="loading" class="loading">Cargando turnos...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <table class="turnos-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Fecha</th>
            <th>Horario</th>
            <th>Estado</th>
            <th>Reservado por</th>
            <th>Jugadores</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="turno in turnos" :key="turno.id">
            <td>{{ turno.id }}</td>
            <td>{{ formatDate(turno.fecha) }}</td>
            <td>{{ turno.hora_inicio }} - {{ turno.hora_fin }}</td>
            <td>
              <span :class="['estado', turno.estado]">{{ turno.estado }}</span>
            </td>
            <td>{{ turno.socio_reserva_nombre || '-' }}</td>
            <td>{{ turno.jugadores.join(', ') || '-' }}</td>
            <td class="actions">
              <button @click="viewTurno(turno.id)" class="btn-icon" title="Ver">
                <Icon icon="mdi:eye" width="18" height="18" />
              </button>
              <button @click="editTurno(turno.id)" class="btn-icon" title="Editar">
                <Icon icon="mdi:pencil" width="18" height="18" />
              </button>
              <button @click="confirmDelete(turno.id)" class="btn-icon btn-delete" title="Eliminar">
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
    <TurnosUpdate v-if="editingTurnoId" :id="editingTurnoId" @close="editingTurnoId = null" @updated="handleUpdated" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Icon } from '@iconify/vue'
import { useTurnosStore } from '@/stores/turnos'
import { storeToRefs } from 'pinia'
import TurnosCreate from './TurnosCreate.vue'
import TurnosShow from './TurnosShow.vue'
import TurnosUpdate from './TurnosUpdate.vue'

const turnosStore = useTurnosStore()
const { turnos, loading, error, currentPage, totalPages } = storeToRefs(turnosStore)

const showCreateForm = ref(false)
const showingTurnoId = ref<number | null>(null)
const editingTurnoId = ref<number | null>(null)

onMounted(() => {
  turnosStore.fetchTurnos()
})

function formatDate(dateString: string) {
  const date = new Date(dateString + 'T00:00:00')
  return date.toLocaleDateString('es-AR')
}

function viewTurno(id: number) {
  showingTurnoId.value = id
}

function editTurno(id: number) {
  editingTurnoId.value = id
}

function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    turnosStore.fetchTurnos(page)
  }
}

async function confirmDelete(id: number) {
  if (confirm('¿Está seguro de que desea eliminar este turno?')) {
    try {
      await turnosStore.deleteTurno(id)
    } catch (e) {
      alert('Error al eliminar el turno')
    }
  }
}

function handleCreated() {
  showCreateForm.value = false
  turnosStore.fetchTurnos(1)
}

function handleUpdated() {
  editingTurnoId.value = null
  turnosStore.fetchTurnos(currentPage.value)
}
</script>

<style scoped>
.turnos-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h2 {
  color: #022F9D;
  margin: 0;
}

.turnos-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.turnos-table th,
.turnos-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #CCCCCC;
}

.turnos-table th {
  background-color: #022F9D;
  color: white;
  font-weight: bold;
}

.turnos-table tr:hover {
  background-color: #f5f5f5;
}

.estado {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
  font-weight: bold;
}

.estado.ocupado {
  background-color: #dc3545;
  color: #ffffff;
}

.estado.disponible {
  background-color: #4CAF50;
  color: white;
}

.estado.reservado {
  background-color: #FFCD00;
  color: #000000;
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

.loading,
.error {
  text-align: center;
  padding: 20px;
  font-size: 16px;
}

.error {
  color: #dc3545;
}
</style>
