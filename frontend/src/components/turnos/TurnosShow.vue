<template>
  <div class="panel-wrapper">
    <div class="panel-content">
      <h2>Detalle del Turno</h2>
      <div v-if="loading">Cargando...</div>
      <div v-else-if="turno">
        <div class="detail-item"><strong>ID:</strong> {{ turno.id }}</div>
        <div class="detail-item"><strong>Cancha:</strong> {{ turno.cancha }}</div>
        <div class="detail-item"><strong>Fecha:</strong> {{ turno.fecha }}</div>
        <div class="detail-item"><strong>Horario:</strong> {{ turno.hora_inicio }} - {{ turno.hora_fin }}</div>
        <div class="detail-item"><strong>Estado:</strong> <span :class="['badge', turno.estado]">{{ turno.estado }}</span></div>
        <div class="detail-item"><strong>Reservado por:</strong> {{ turno.socio_reserva_nombre || 'No asignado' }}</div>
        <div class="detail-item">
          <strong>Jugadores:</strong>
          <ul v-if="turno.jugadores && turno.jugadores.length">
            <li v-for="(jugador, index) in turno.jugadores" :key="index">{{ jugador }}</li>
          </ul>
          <span v-else>Sin jugadores</span>
        </div>
        <button @click="$emit('close')" class="btn-close">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useTurnosStore } from '@/stores/turnos'
import { storeToRefs } from 'pinia'

const props = defineProps<{ id: number }>()
const emit = defineEmits(['close'])

const turnosStore = useTurnosStore()
const { turno, loading } = storeToRefs(turnosStore)

onMounted(() => {
  turnosStore.fetchTurno(props.id)
})
</script>

<style scoped>
.panel-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  margin: 1rem 0;
}

.panel-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  max-width: 500px;
  width: 100%;
  border: 1px solid #e5e7eb;
  box-shadow: 0 6px 18px rgba(2, 47, 157, 0.08);
}

h2 {
  color: #022F9D;
  margin-bottom: 20px;
}

.detail-item {
  margin-bottom: 15px;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 4px;
}

.detail-item strong {
  color: #022F9D;
}

.badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
}

.badge.disponible {
  background-color: #4CAF50;
  color: white;
}

.badge.reservado {
  background-color: #FFCD00;
  color: #000000;
}

ul {
  margin: 10px 0 0 20px;
}

.btn-close {
  margin-top: 20px;
  background-color: #022F9D;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
}

.btn-close:hover {
  background-color: #00CDFF;
}
</style>
