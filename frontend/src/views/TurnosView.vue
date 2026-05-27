<template>
  <div class="turnos-view">
    <h1>Gestión de Turnos</h1>
    <TurnosList />
  </div>
</template>

<script setup lang="ts">
import TurnosList from '@/components/turnos/TurnosList.vue'
</script>

<style scoped>
.turnos-view {
  padding: 20px;
}

h1 {
  color: #022F9D;
  margin-bottom: 20px;
}
</style>
