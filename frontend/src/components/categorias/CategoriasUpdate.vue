<template>
    <div class="container">
      <h2>Modificar Categoría</h2>
      <form @submit.prevent="modificar">
        <div class="form-group">
          <label for="nombre">Nombre de la categoría</label>
          <input type="text" id="nombre" v-model="categoria.nombre" placeholder="Ingrese el nombre" />
        </div>
        
        <div class="botonera">
          <RouterLink :to="{ name: 'categorias_list' }">
            <button type="button">Volver</button>
          </RouterLink>
          <button type="submit">Modificar</button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import useCategoriaStore from '../../stores/categorias'
  import { useRoute, useRouter } from 'vue-router'
  import type { Categoria } from '@/interfaces/Categoria'
  
  const route = useRoute()
  const router = useRouter()
  
  const store = useCategoriaStore()
  
  const categoria = ref<Categoria>({
    id: 0,
    nombre: ''
  })
  
  onMounted(async () => {
    await store.fetchCategorias()
    const id = route.params.id
    const found = store.categorias.find((cat) => cat.id == parseInt(id as string))
    if (found) {
      categoria.value = { ...found }
    } else {
      alert('Categoría no encontrada')
      router.push({ name: 'categorias_list' })
    }
  })
  
  const modificar = async () => {
    if (!categoria.value.nombre || !categoria.value.nombre.trim()) {
      alert('Por favor, complete el nombre')
      return
    }
    
    try {
      if (!categoria.value.id) {
        throw new Error('ID de categoría inválido')
      }
      await store.updateCategoria(categoria.value.id, categoria.value)
      alert('Categoría modificada exitosamente')
      router.push({ name: 'categorias_list' })
    } catch (error) {
      console.error('Error al modificar:', error)
      alert('Error al modificar la categoría')
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

h2 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #1976d2;
  box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
}

.botonera {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.botonera button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.botonera button[type="button"] {
  background-color: #f5f5f5;
  color: #333;
}

.botonera button[type="button"]:hover {
  background-color: #e0e0e0;
}

.botonera button[type="submit"] {
  background-color: #1976d2;
  color: white;
}

.botonera button[type="submit"]:hover {
  background-color: #1565c0;
}
</style>