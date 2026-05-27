<template>
  <div class="profesores-list">
    <div class="header">
      <h2>Lista de Profesores</h2>
      <button @click="showCreateForm = true" class="btn-primary">
        <Icon icon="mdi:plus" width="20" height="20" />
        Nuevo Profesor
      </button>
    </div>

    <ProfesoresCreate v-if="showCreateForm" @close="showCreateForm = false" @created="handleCreated" />
    <ProfesoresShow v-if="showingProfesorId" :id="showingProfesorId" @close="showingProfesorId = null" />

    <div v-if="loading" class="loading">Cargando profesores...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <table class="profesores-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Apellido</th>
            <th>Nombre</th>
            <th>DNI</th>
            <th>Horarios de clases</th>
            <th>Teléfono</th>
            <th>Email</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="profesor in profesoresOrdenados" :key="profesor.id">
            <td>{{ profesor.id }}</td>
            <td>{{ profesor.apellido }}</td>
            <td>{{ profesor.nombre }}</td>
            <td>{{ profesor.dni }}</td>
            <td>{{ profesor.horarios_clases }}</td>
            <td>{{ profesor.telefono }}</td>
            <td>{{ profesor.email }}</td>
            <td class="actions">
              <button v-if="profesor.id" @click="viewProfesor(profesor.id)" class="btn-icon" title="Ver">
                <Icon icon="mdi:eye" width="18" height="18" />
              </button>
              <button v-if="profesor.id" @click="editProfesor(profesor.id)" class="btn-icon" title="Editar">
                <Icon icon="mdi:pencil" width="18" height="18" />
              </button>
              <button v-if="profesor.id" @click="confirmDelete(profesor.id)" class="btn-icon btn-delete" title="Eliminar">
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
        <span class="pagination-info">Página {{ currentPage }} de {{ totalPages }}</span>
        <button @click="goToPage(currentPage + 1)" :disabled="currentPage >= totalPages" class="btn-pagination">
          Siguiente
          <Icon icon="mdi:chevron-right" width="20" height="20" />
        </button>
      </div>
    </div>
    <ProfesoresUpdate v-if="editingProfesorId" :id="editingProfesorId" @close="editingProfesorId = null" @updated="handleUpdated" />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { Icon } from '@iconify/vue'
import { useProfesoresStore } from '@/stores/profesores'
import { storeToRefs } from 'pinia'
import ProfesoresCreate from './ProfesoresCreate.vue'
import ProfesoresShow from './ProfesoresShow.vue'
import ProfesoresUpdate from './ProfesoresUpdate.vue'

const profesoresStore = useProfesoresStore()
const { profesores, loading, error, currentPage, totalPages } = storeToRefs(profesoresStore)

const profesoresOrdenados = computed(() => {
  return [...profesores.value].sort((a, b) => {
    const apellidoA = (a.apellido || '').toLowerCase().trim()
    const apellidoB = (b.apellido || '').toLowerCase().trim()
    const porApellido = apellidoA.localeCompare(apellidoB, 'es', { sensitivity: 'base' })

    if (porApellido !== 0) {
      return porApellido
    }

    const nombreA = (a.nombre || '').toLowerCase().trim()
    const nombreB = (b.nombre || '').toLowerCase().trim()
    return nombreA.localeCompare(nombreB, 'es', { sensitivity: 'base' })
  })
})

const showCreateForm = ref(false)
const showingProfesorId = ref<number | null>(null)
const editingProfesorId = ref<number | null>(null)

onMounted(() => {
  profesoresStore.fetchProfesores()
})

function viewProfesor(id: number) {
  showingProfesorId.value = id
}

function editProfesor(id: number) {
  editingProfesorId.value = id
}

function confirmDelete(id: number) {
  if (confirm('¿Está seguro de que desea eliminar este profesor?')) {
    profesoresStore.deleteProfesor(id)
  }
}

function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    profesoresStore.fetchProfesores(page)
  }
}

function handleCreated() {
  showCreateForm.value = false
  profesoresStore.fetchProfesores(1)
}

function handleUpdated() {
  editingProfesorId.value = null
  profesoresStore.fetchProfesores(currentPage.value)
}
</script>

<style scoped>
.profesores-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.profesores-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.profesores-table th,
.profesores-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

.profesores-table th {
  background-color: #022F9D;
  color: #FFFFFF;
}

.profesores-table tr:nth-child(even) {
  background-color: #f2f2f2;
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
  margin-top: 2rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 6px;
}

.btn-pagination {
  background: #022F9D;
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

.btn-pagination:hover:not(:disabled) {
  background: #00CDFF;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 205, 255, 0.3);
}

.btn-pagination:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  font-weight: 600;
  color: #022F9D;
  min-width: 150px;
  text-align: center;
  font-size: 1rem;
}

.loading,
.error {
  padding: 20px;
  text-align: center;
}

.error {
  color: #f44336;
}
</style>
