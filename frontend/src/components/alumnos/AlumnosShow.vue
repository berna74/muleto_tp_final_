<template>
  <div class="panel-wrapper">
    <div class="panel-content">
      <h2>Detalle del Alumno</h2>
      
      <div v-if="loading" class="loading">Cargando...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="alumno" class="alumno-details">
        <div class="detail-row">
          <span class="label">ID:</span>
          <span class="value">{{ alumno.id }}</span>
        </div>
        
        <div class="detail-row">
          <span class="label">Nombre Completo:</span>
          <span class="value">{{ alumno.nombre }} {{ alumno.apellido }}</span>
        </div>
        
        <div class="detail-row">
          <span class="label">DNI:</span>
          <span class="value">{{ alumno.dni }}</span>
        </div>
        
        <div class="detail-row">
          <span class="label">Email:</span>
          <span class="value">{{ alumno.email }}</span>
        </div>
        
        <div class="detail-row">
          <span class="label">Teléfono:</span>
          <span class="value">{{ alumno.telefono }}</span>
        </div>
        
        <div class="detail-row">
          <span class="label">Fecha de Inscripción:</span>
          <span class="value">{{ formatDate(alumno.fecha_inscripcion) }}</span>
        </div>
        
        <div class="detail-row" v-if="alumno.profesor">
          <span class="label">Profesor:</span>
          <span class="value">{{ alumno.profesor.nombre }} {{ alumno.profesor.apellido }}</span>
        </div>
        
        <div class="detail-row" v-if="alumno.nivel">
          <span class="label">Nivel:</span>
          <span class="value">{{ alumno.nivel }}</span>
        </div>
        
        <div class="detail-row">
          <span class="label">Estado:</span>
          <span :class="['badge', alumno.activo ? 'badge-active' : 'badge-inactive']">
            {{ alumno.activo ? 'Activo' : 'Inactivo' }}
          </span>
        </div>
      </div>
      
      <div class="panel-actions">
        <button @click="$emit('close')" class="btn-close">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAlumnosStore } from '@/stores/alumnos'
import { storeToRefs } from 'pinia'

const props = defineProps<{
  alumnoId: number
}>()

const emit = defineEmits(['close'])
const alumnosStore = useAlumnosStore()
const { alumno, loading, error } = storeToRefs(alumnosStore)

onMounted(() => {
  alumnosStore.fetchAlumno(props.alumnoId)
})

function formatDate(dateString: string): string {
  const date = new Date(dateString + 'T00:00:00')
  return date.toLocaleDateString('es-AR', { 
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  })
}
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
  max-width: 600px;
  width: 100%;
  border: 1px solid #e5e7eb;
  box-shadow: 0 6px 18px rgba(2, 47, 157, 0.08);
}

h2 {
  color: #022F9D;
  margin-bottom: 20px;
}

.alumno-details {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.detail-row {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 15px;
  padding: 10px;
  border-bottom: 1px solid #e0e0e0;
}

.detail-row:last-child {
  border-bottom: none;
}

.label {
  font-weight: bold;
  color: #022F9D;
}

.value {
  color: #333;
}

.badge {
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: bold;
  display: inline-block;
}

.badge-active {
  background-color: #28a745;
  color: white;
}

.badge-inactive {
  background-color: #dc3545;
  color: white;
}

.panel-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.btn-close {
  background-color: #022F9D;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-close:hover {
  background-color: #00CDFF;
}

.loading, .error {
  text-align: center;
  padding: 40px;
  color: #666;
}

.error {
  color: #dc3545;
}
</style>
