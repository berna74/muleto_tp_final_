
<template>
  <div class="container">
    <h4>Categorías</h4>
    <RouterView />
  </div>
</template>
 <script setup lang="ts">
 import { useRouter } from 'vue-router'
import { onMounted } from 'vue'

const router = useRouter()

onMounted(() => {
  //console.log('componente montado')
  router.push({ name: 'categorias_list' })
})
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
</style>