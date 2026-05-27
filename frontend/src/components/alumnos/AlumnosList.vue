<template>
  <div class="alumnos-list">
    <div class="list-header">
      <h2>Lista de Alumnos</h2>
      <button @click="handleCreate" class="btn-create" :disabled="loading" :class="{ 'is-loading': loading }">
        <Icon icon="mdi:plus" width="20" height="20" />
        {{ loading ? 'Cargando...' : 'Nuevo Alumno' }}
      </button>
    </div>
    
    <div v-if="loading" class="loading">Cargando alumnos...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="alumnos.length === 0" class="empty">No hay alumnos registrados</div>
    
    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Apellido y Nombre</th>
            <th>DNI</th>
            <th>Email</th>
            <th>Teléfono</th>
            <th>Profesor</th>
            <th>Nivel</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="alumno in alumnosOrdenados" :key="alumno.id">
            <td>{{ alumno.id }}</td>
            <td>{{ alumno.apellido }}, {{ alumno.nombre }}</td>
            <td>{{ alumno.dni }}</td>
            <td>{{ alumno.email }}</td>
            <td>{{ alumno.telefono }}</td>
            <td>{{ alumno.profesor?.nombre }} {{ alumno.profesor?.apellido }}</td>
            <td>{{ alumno.nivel }}</td>
            <td>
              <span :class="['badge', alumno.activo ? 'badge-active' : 'badge-inactive']">
                {{ alumno.activo ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td class="actions">
              <button @click="$emit('show', alumno.id)" class="btn-icon" title="Ver">
                <Icon icon="mdi:eye" width="18" height="18" />
              </button>
              <button @click="$emit('edit', alumno.id)" class="btn-icon" title="Editar">
                <Icon icon="mdi:pencil" width="18" height="18" />
              </button>
              <button @click="handleDelete(alumno.id)" class="btn-icon btn-delete" title="Eliminar">
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
import { computed, onMounted } from 'vue'
import { Icon } from '@iconify/vue'
import { useAlumnosStore } from '@/stores/alumnos'
import { storeToRefs } from 'pinia'

const emit = defineEmits(['create', 'show', 'edit'])
const alumnosStore = useAlumnosStore()
const { alumnos, loading, error, currentPage, totalPages } = storeToRefs(alumnosStore)

const alumnosOrdenados = computed(() => {
  return [...alumnos.value].sort((a, b) => {
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

onMounted(() => {
  alumnosStore.fetchAlumnos()
})

async function handleDelete(id: number) {
  if (confirm('¿Está seguro de eliminar este alumno?')) {
    try {
      await alumnosStore.deleteAlumno(id)
    } catch (e) {
      console.error('Error al eliminar alumno:', e)
    }
  }
}

function handleCreate() {
  if (!loading.value) {
    emit('create')
  }
}

function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    alumnosStore.fetchAlumnos(page)
  }
}
</script>

<style scoped>
.alumnos-list {
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

.badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.badge-active {
  background-color: #28a745;
  color: white;
}

.badge-inactive {
  background-color: #6c757d;
  color: white;
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
