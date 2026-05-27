<template>
  <div class="panel-wrapper">
    <div class="panel-content">
      <h2>Detalle del Pago</h2>
      
      <div v-if="loading" class="loading">Cargando...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="pago" class="pago-details">
        <div class="detail-row">
          <span class="label">ID:</span>
          <span class="value">{{ pago.id }}</span>
        </div>
        
        <div class="detail-row">
          <span class="label">Tipo de Pago:</span>
          <span :class="['badge-tipo', getTipoBadgeClass(pago.tipo)]">
            {{ pago.tipo }}
          </span>
        </div>
        
        <div class="detail-row">
          <span class="label">Monto:</span>
          <span class="value monto">${{ formatMonto(pago.monto) }}</span>
        </div>
        
        <div class="detail-row">
          <span class="label">Fecha de Pago:</span>
          <span class="value">{{ formatDate(pago.fecha_pago) }}</span>
        </div>
        
        <div class="detail-row">
          <span class="label">Período:</span>
          <span class="value">{{ formatPeriodo(pago.mes, pago.anio) }}</span>
        </div>
        
        <div class="detail-row" v-if="pago.socio_nombre">
          <span class="label">Pagado por (Socio):</span>
          <span class="value">{{ pago.socio_nombre }}</span>
        </div>
        
        <div class="detail-row" v-if="pago.alumno_nombre">
          <span class="label">Pagado por (Alumno):</span>
          <span class="value">{{ pago.alumno_nombre }}</span>
        </div>
        
        <div class="detail-row" v-if="pago.profesor_nombre">
          <span class="label">Profesor:</span>
          <span class="value">{{ pago.profesor_nombre }}</span>
        </div>
        
        <div class="detail-row" v-if="pago.metodo_pago">
          <span class="label">Método de Pago:</span>
          <span class="value">{{ pago.metodo_pago }}</span>
        </div>
        
        <div class="detail-row" v-if="pago.observaciones">
          <span class="label">Observaciones:</span>
          <span class="value">{{ pago.observaciones }}</span>
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
import { usePagosStore } from '@/stores/pagos'
import { storeToRefs } from 'pinia'

const props = defineProps<{
  pagoId: number
}>()

const emit = defineEmits(['close'])
const pagosStore = usePagosStore()
const { pago, loading, error } = storeToRefs(pagosStore)

onMounted(() => {
  pagosStore.fetchPago(props.pagoId)
})

function getTipoBadgeClass(tipo: string): string {
  const classes: Record<string, string> = {
    'Cuota Social': 'badge-cuota',
    'Abono Mensual': 'badge-mensual',
    'Abono Diario': 'badge-diario',
    'Clase': 'badge-clase'
  }
  return classes[tipo] || 'badge-default'
}

function formatMonto(monto: number): string {
  return new Intl.NumberFormat('es-AR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(monto)
}

function formatDate(dateString: string): string {
  const date = new Date(dateString + 'T00:00:00')
  return date.toLocaleDateString('es-AR', { 
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  })
}

function formatPeriodo(mes: number, anio: number): string {
  const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
  return `${meses[mes - 1]} ${anio}`
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

.pago-details {
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

.monto {
  font-weight: bold;
  color: #28a745;
  font-size: 1.1em;
}

.badge-tipo {
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: bold;
  display: inline-block;
}

.badge-cuota {
  background-color: #022F9D;
  color: white;
}

.badge-mensual {
  background-color: #00CDFF;
  color: #000000;
}

.badge-diario {
  background-color: #FFCD00;
  color: #000000;
}

.badge-clase {
  background-color: #28a745;
  color: white;
}

.badge-default {
  background-color: #6c757d;
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
