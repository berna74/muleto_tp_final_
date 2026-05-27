<template>
  <div class="socios-list">
    <div class="header">
      <h2>Lista de Socios</h2>
      <button @click="showCreateForm = true" class="btn-primary">
        <Icon icon="mdi:plus" width="20" height="20" />
        Nuevo Socio
      </button>
    </div>

    <SociosCreate v-if="showCreateForm" @close="showCreateForm = false" @created="handleCreated" />
    <SociosShow v-if="showViewForm && selectedSocio" :socio="selectedSocio" @close="closeViewForm" />
    <SociosUpdate
      v-if="showUpdateForm && selectedSocio"
      :socio="selectedSocio"
      @close="closeUpdateForm"
      @updated="handleUpdated"
    />

    <div v-if="loading" class="loading">Cargando socios...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <table class="socios-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Apellido</th>
            <th>Nombre</th>
            <th>DNI</th>
            <th>Email</th>
            <th>Telefono</th>
            <th>Categorias</th>
            <th>Fecha Inscripcion</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="socio in sociosOrdenados" :key="socio.id">
            <td>{{ socio.id }}</td>
            <td>{{ socio.apellido }}</td>
            <td>{{ socio.nombre }}</td>
            <td>{{ socio.dni }}</td>
            <td>{{ socio.email }}</td>
            <td>{{ socio.telefono }}</td>
            <td>
              <div class="categorias-cell">
                <span v-for="categoria in socio.categorias" :key="categoria.id" class="badge-categoria">
                  {{ categoria.nombre }}
                </span>
                <span v-if="!socio.categorias || socio.categorias.length === 0" class="sin-categoria">
                  Sin categoria
                </span>
              </div>
            </td>
            <td>{{ socio.fecha_inscripcion }}</td>
            <td>
              <span :class="['badge-estado', socio.registra_deuda ? 'con-deuda' : 'sin-deuda']">
                {{ socio.registra_deuda ? 'Registra deuda' : 'No registra deuda' }}
              </span>
            </td>
            <td class="actions">
              <button @click="viewSocio(socio)" class="btn-icon" title="Ver">
                <Icon icon="mdi:eye" width="18" height="18" />
              </button>
              <button @click="openUpdateForm(socio)" class="btn-icon" title="Editar">
                <Icon icon="mdi:pencil" width="18" height="18" />
              </button>
              <button @click="confirmDelete(socio.id)" class="btn-icon btn-delete" title="Eliminar">
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
import { computed, ref, onMounted } from 'vue'
import { Icon } from '@iconify/vue'
import { useSociosStore } from '@/stores/socios'
import { storeToRefs } from 'pinia'
import SociosCreate from './SociosCreate.vue'
import SociosUpdate from './SociosUpdate.vue'
import SociosShow from './SociosShow.vue'
import type { Socio } from '@/interfaces/Socio'

const sociosStore = useSociosStore()
const { socios, loading, error, currentPage, totalPages } = storeToRefs(sociosStore)

const sociosOrdenados = computed(() => {
  return [...socios.value].sort((a, b) => {
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
const showUpdateForm = ref(false)
const showViewForm = ref(false)
const selectedSocio = ref<Socio | null>(null)

onMounted(() => {
  sociosStore.fetchSocios()
})

function handleCreated() {
  showCreateForm.value = false
  sociosStore.fetchSocios(1)
}

function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    sociosStore.fetchSocios(page)
  }
}

function viewSocio(socio: Socio) {
  selectedSocio.value = socio
  showViewForm.value = true
}

function openUpdateForm(socio: Socio) {
  selectedSocio.value = socio
  showUpdateForm.value = true
}

function closeUpdateForm() {
  showUpdateForm.value = false
  selectedSocio.value = null
}

function closeViewForm() {
  showViewForm.value = false
  selectedSocio.value = null
}

function handleUpdated() {
  closeUpdateForm()
  sociosStore.fetchSocios(currentPage.value)
}

function confirmDelete(id: number) {
  if (confirm('Esta seguro de que desea eliminar este socio?')) {
    sociosStore.deleteSocio(id)
  }
}
</script>

<style scoped>
.socios-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.socios-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.socios-table th,
.socios-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

.socios-table th {
  background-color: #022F9D;
  color: #FFFFFF;
}

.socios-table tr:nth-child(even) {
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

.badge-estado {
  padding: 5px 10px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
  text-align: center;
  display: inline-block;
  white-space: nowrap;
}

.badge-estado.sin-deuda {
  background-color: #4CAF50;
  color: white;
}

.badge-estado.con-deuda {
  background-color: #f44336;
  color: white;
}

.categorias-cell {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  justify-content: center;
}

.badge-categoria {
  display: inline-block;
  padding: 4px 8px;
  background: #00CDFF;
  color: white;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
}

.sin-categoria {
  color: #999;
  font-style: italic;
  font-size: 0.85rem;
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
