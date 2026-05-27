<template>
  <div class="profesores-view">
    <h1>Gestión de Profesores</h1>
    <ProfesoresList />
  </div>
</template>

<script setup lang="ts">
import ProfesoresList from '@/components/profesores/ProfesoresList.vue'
</script>

<style scoped>
.profesores-view {
  padding: 20px;
}

h1 {
  color: #022F9D;
  margin-bottom: 20px;
}
</style>
