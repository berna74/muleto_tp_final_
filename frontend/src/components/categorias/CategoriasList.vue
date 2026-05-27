<template>
  <div class="container">
    <h2>Categorias</h2>
    <router-link :to="{ name: 'categorias_create' }"><button>Crear Categoria</button></router-link>

    <div v-if="loading" class="alert alert-info mt-3">Cargando categorias...</div>
    <div v-else-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    <div v-else-if="categorias.length === 0" class="alert alert-info mt-3">
      No hay categorias registradas. Haz clic en "Crear Categoria" para agregar una.
    </div>

    <template v-else>
      <table class="table table-striped mt-3">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="categoria in categorias" :key="categoria.id">
            <td>{{ categoria.id }}</td>
            <td>{{ categoria.nombre }}</td>
            <td class="actions">
              <router-link v-if="categoria.id" :to="{ name: 'categorias_show', params: { id: categoria.id } }">
                <button class="btn-icon" title="Ver">
                  <Icon icon="mdi:eye" width="18" height="18" />
                </button>
              </router-link>
              <router-link v-if="categoria.id" :to="{ name: 'categorias_edit', params: { id: categoria.id } }">
                <button class="btn-icon" title="Editar">
                  <Icon icon="mdi:pencil" width="18" height="18" />
                </button>
              </router-link>
              <button @click.prevent="eliminar(categoria.id as number)" class="btn-icon btn-delete" title="Eliminar">
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
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { Icon } from '@iconify/vue'
import { useCategoriasStore } from '@/stores/categorias'

const categoriasStore = useCategoriasStore()
const { categorias, loading, error, currentPage, totalPages } = storeToRefs(categoriasStore)

onMounted(async () => {
  await categoriasStore.fetchCategorias()
})

async function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    await categoriasStore.fetchCategorias(page)
  }
}

async function eliminar(id: number) {
  if (confirm('Estas seguro de eliminar la categoria ' + id + '?')) {
    if (confirm('Esta accion no se puede deshacer. Deseas continuar?')) {
      try {
        await categoriasStore.deleteCategoria(id)
      } catch (error) {
        console.error('Error al eliminar categoria:', error)
        alert('Error al eliminar la categoria. Puede estar asociada a otros registros.')
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 700px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

h2 {
  margin-bottom: 1.5rem;
}

button {
  margin-bottom: 1.5rem;
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
</style>
