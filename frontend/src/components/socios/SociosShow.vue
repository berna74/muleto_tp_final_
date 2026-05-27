<template>
  <div class="panel-wrapper">
    <div class="panel-content">
      <h2>Detalle del Socio</h2>
      <div v-if="socio">
        <div class="detail-section">
          <h3>Información Personal</h3>
          <div class="detail-item"><strong>ID:</strong> {{ socio.id }}</div>
          <div class="detail-item"><strong>Nombre Completo:</strong> {{ socio.nombre }} {{ socio.apellido }}</div>
          <div class="detail-item"><strong>DNI:</strong> {{ socio.dni }}</div>
          <div class="detail-item"><strong>Email:</strong> {{ socio.email }}</div>
          <div class="detail-item"><strong>Teléfono:</strong> {{ socio.telefono }}</div>
          <div class="detail-item" v-if="socio.direccion"><strong>Dirección:</strong> {{ socio.direccion }}</div>
          <div class="detail-item" v-if="socio.fecha_nacimiento"><strong>Fecha de Nacimiento:</strong> {{ formatDate(socio.fecha_nacimiento) }}</div>
          <div class="detail-item"><strong>Fecha de Inscripción:</strong> {{ formatDate(socio.fecha_inscripcion) }}</div>
        </div>

        <div class="detail-section">
          <h3>Estado Financiero</h3>
          <div class="detail-item">
            <strong>Estado de Deuda:</strong>
            <span :class="['badge-estado', socio.registra_deuda ? 'con-deuda' : 'sin-deuda']">
              {{ socio.registra_deuda ? 'Registra deuda' : 'No registra deuda' }}
            </span>
          </div>
        </div>

        <div class="detail-section" v-if="socio.profesor_nombre">
          <h3>Profesor Asignado</h3>
          <div class="detail-item">{{ socio.profesor_nombre }}</div>
        </div>

        <div class="detail-section" v-if="socio.categorias && socio.categorias.length > 0">
          <h3>Categorías</h3>
          <div class="categorias-list">
            <span v-for="categoria in socio.categorias" :key="categoria.id" class="badge-categoria">
              {{ categoria.nombre }}
            </span>
          </div>
        </div>

        <button @click="$emit('close')" class="btn-close">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Socio } from '@/interfaces/Socio'

const props = defineProps<{
  socio: Socio
}>()

const emit = defineEmits(['close'])

function formatDate(dateString: string): string {
  if (!dateString) return '-'
  const date = new Date(dateString + 'T00:00:00')
  return date.toLocaleDateString('es-AR', { day: '2-digit', month: '2-digit', year: 'numeric' })
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
  margin-bottom: 25px;
  border-bottom: 2px solid #00CDFF;
  padding-bottom: 10px;
}

h3 {
  color: #022F9D;
  margin: 20px 0 10px 0;
  font-size: 1.1rem;
}

.detail-section {
  margin-bottom: 20px;
}

.detail-item {
  margin-bottom: 12px;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 4px;
  border-left: 3px solid #00CDFF;
}

.detail-item strong {
  color: #022F9D;
  margin-right: 8px;
}

.categorias-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 10px;
}

.badge-categoria {
  display: inline-block;
  padding: 6px 12px;
  background: #00CDFF;
  color: white;
  border-radius: 16px;
  font-size: 0.9rem;
  font-weight: 500;
}

.badge-estado {
  display: inline-block;
  padding: 6px 12px;
  color: white;
  border-radius: 16px;
  font-size: 0.9rem;
  font-weight: 500;
  margin-left: 8px;
}

.badge-estado.sin-deuda {
  background-color: #4CAF50;
}

.badge-estado.con-deuda {
  background-color: #f44336;
}

.btn-close {
  background-color: #022F9D;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 20px;
  width: 100%;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.btn-close:hover {
  background-color: #00CDFF;
}

@media (max-width: 768px) {
  .panel-content {
    width: 95%;
    padding: 20px;
  }
}
</style>
