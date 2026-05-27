<template>
    <div class="container">
      <h2>Detalle de la categoría</h2>
      <h3>Nombre : {{ categoria?.nombre || '-' }}</h3>
      <h4>ID: {{ categoria?.id || '-' }}</h4>
  
      <RouterLink :to="{ name: 'categorias_list' }"><button>Volver</button> </RouterLink>
    </div>
  </template>
  
  <script setup lang="ts">
  import { storeToRefs } from 'pinia'
  import { onMounted } from 'vue'
  import useCategoriaStore from '../../stores/categorias'
  import { useRoute } from 'vue-router'
  
  const route = useRoute()
  const store = useCategoriaStore()
  const { categoria } = storeToRefs(store)
  
  onMounted(async () => {
    const id = Number(route.params.id)
    if (Number.isFinite(id)) {
      await store.fetchCategoria(id)
    }
  })
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
</style>