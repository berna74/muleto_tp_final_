<template>
  <div class="panel-wrapper">
    <div class="panel-content">
      <div class="panel-header">
        <h2>Detalle de Operación</h2>
        <button @click="$emit('close')" class="btn-close">&times;</button>
      </div>
      <div v-if="loading" class="loading-container">Cargando...</div>
      <div v-else-if="pelotitasStore.pelotita" class="detail-content">
        <div class="detail-row">
          <span class="label">ID:</span>
          <span class="value">{{ pelotitasStore.pelotita.id }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Fecha:</span>
          <span class="value">{{ formatDate(pelotitasStore.pelotita.fecha) }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Tipo:</span>
          <span class="value">
            <span class="badge" :class="pelotitasStore.pelotita.tipo">
              {{ pelotitasStore.pelotita.tipo === 'compra' ? 'Compra' : 'Venta' }}
            </span>
          </span>
        </div>
        <div class="detail-row">
          <span class="label">Cantidad:</span>
          <span class="value">{{ pelotitasStore.pelotita.cantidad }} unidades</span>
        </div>
        <div class="detail-row">
          <span class="label">Precio Unitario:</span>
          <span class="value">${{ formatMoney(pelotitasStore.pelotita.precio_unitario) }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Total:</span>
          <span class="value total">${{ formatMoney(pelotitasStore.pelotita.total) }}</span>
        </div>
        <div class="detail-row" v-if="pelotitasStore.pelotita.proveedor">
          <span class="label">Proveedor:</span>
          <span class="value">{{ pelotitasStore.pelotita.proveedor }}</span>
        </div>
        <div class="detail-row" v-if="pelotitasStore.pelotita.comprador_tipo">
          <span class="label">Comprador:</span>
          <span class="value">
            <span class="badge-comprador">{{ getCompradorLabel() }}</span>
          </span>
        </div>
        <div class="detail-row" v-if="pelotitasStore.pelotita.observaciones">
          <span class="label">Observaciones:</span>
          <span class="value">{{ pelotitasStore.pelotita.observaciones }}</span>
        </div>
        <div class="detail-row" v-if="pelotitasStore.pelotita.created_at">
          <span class="label">Registrado:</span>
          <span class="value">{{ formatDateTime(pelotitasStore.pelotita.created_at) }}</span>
        </div>
      </div>
      <div class="panel-footer">
        <button @click="$emit('close')" class="btn-secondary">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { usePelotitasStore } from '@/stores/pelotitas'

const props = defineProps<{
  pelotitaId: number
}>()

const emit = defineEmits(['close'])
const pelotitasStore = usePelotitasStore()
const loading = ref(true)

onMounted(async () => {
  try {
    await pelotitasStore.fetchPelotita(props.pelotitaId)
  } catch (error) {
    console.error('Error al cargar pelotita:', error)
    alert('Error al cargar los datos')
    emit('close')
  } finally {
    loading.value = false
  }
})

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-AR', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

const formatDateTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('es-AR', { 
    day: '2-digit', 
    month: '2-digit', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatMoney = (value: number) => {
  return value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, '.')
}

const getCompradorLabel = () => {
  const pelotita = pelotitasStore.pelotita
  if (!pelotita) return ''
  
  if (pelotita.comprador_tipo === 'otro') {
    return pelotita.comprador_nombre || 'Otro'
  } else if (pelotita.comprador_tipo === 'socio') {
    return `Socio: ${pelotita.comprador_nombre || 'ID ' + pelotita.comprador_id}`
  } else if (pelotita.comprador_tipo === 'alumno') {
    return `Alumno: ${pelotita.comprador_nombre || 'ID ' + pelotita.comprador_id}`
  }
  return ''
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
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 6px 18px rgba(2, 47, 157, 0.08);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.panel-header h2 {
  margin: 0;
  color: #022F9D;
}

.btn-close {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #666;
  line-height: 1;
}

.btn-close:hover {
  color: #c62828;
}

.detail-content {
  padding: 1.5rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.detail-row .label {
  font-weight: 500;
  color: #666;
}

.detail-row .value {
  color: #022F9D;
  font-weight: 500;
}

.detail-row .value.total {
  font-size: 1.2rem;
  font-weight: 700;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
  display: inline-block;
}

.badge.compra {
  background: #E8F5E9;
  color: #2E7D32;
}

.badge.venta {
  background: #FFF3E0;
  color: #E65100;
}

.panel-footer {
  display: flex;
  justify-content: flex-end;
  padding: 1.5rem;
  border-top: 1px solid #eee;
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  background: #e0e0e0;
  color: #333;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: #d0d0d0;
}

.loading-container {
  padding: 3rem;
  text-align: center;
  color: #666;
}
</style>
