<template>
  <div class="socios-view">
    <h1>Gestión de Socios</h1>
    <SociosList />
  </div>
</template>

<script setup lang="ts">
import SociosList from '@/components/socios/SociosList.vue'
</script>

<style scoped>
.socios-view {
  padding: 20px;
}

h1 {
  color: #022F9D;
  margin-bottom: 20px;
}
</style>
