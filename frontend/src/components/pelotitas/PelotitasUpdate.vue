<template>
  <div class="panel-wrapper">
    <div class="panel-content">
      <div class="panel-header">
        <h2>Editar Operación</h2>
        <button @click="$emit('close')" class="btn-close">&times;</button>
      </div>
      <form @submit.prevent="handleSubmit" v-if="!loading">
        <div class="form-row">
          <div class="form-group">
            <label for="fecha">Fecha *</label>
            <input
              type="date"
              id="fecha"
              v-model="formData.fecha"
              required
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label for="tipo">Tipo *</label>
            <select id="tipo" v-model="formData.tipo" required class="form-control">
              <option value="compra">Compra</option>
              <option value="venta">Venta</option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="cantidad">Cantidad *</label>
            <input
              type="number"
              id="cantidad"
              v-model.number="formData.cantidad"
              required
              min="1"
              class="form-control"
              @input="calculateTotal"
            />
          </div>
          <div class="form-group">
            <label for="precio_unitario">Precio Unitario *</label>
            <input
              type="number"
              id="precio_unitario"
              v-model.number="formData.precio_unitario"
              required
              min="0"
              step="0.01"
              class="form-control"
              @input="calculateTotal"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="total">Total</label>
          <input
            type="number"
            id="total"
            v-model.number="formData.total"
            readonly
            class="form-control"
            style="background: #f5f5f5;"
          />
        </div>

        <div class="form-group" v-if="formData.tipo === 'compra'">
          <label for="proveedor">Proveedor</label>
          <input
            type="text"
            id="proveedor"
            v-model="formData.proveedor"
            class="form-control"
            placeholder="Nombre del proveedor"
          />
        </div>

        <div v-if="formData.tipo === 'venta'">
          <div class="form-group">
            <label for="comprador_tipo">Comprador *</label>
            <select 
              id="comprador_tipo" 
              v-model="formData.comprador_tipo" 
              required 
              class="form-control"
              @change="handleCompradorTipoChange"
            >
              <option value="">Seleccione...</option>
              <option value="socio">Socio</option>
              <option value="alumno">Alumno</option>
              <option value="otro">Otro</option>
            </select>
          </div>

          <div class="form-group" v-if="formData.comprador_tipo === 'socio'">
            <label for="comprador_id">Seleccionar Socio *</label>
            <select 
              id="comprador_id" 
              v-model.number="formData.comprador_id" 
              required 
              class="form-control"
            >
              <option :value="null">Seleccione un socio...</option>
              <option v-for="socio in socios" :key="socio.id" :value="socio.id">
                {{ socio.nombre }} {{ socio.apellido }} - DNI: {{ socio.dni }}
              </option>
            </select>
          </div>

          <div class="form-group" v-if="formData.comprador_tipo === 'alumno'">
            <label for="comprador_id">Seleccionar Alumno *</label>
            <select 
              id="comprador_id" 
              v-model.number="formData.comprador_id" 
              required 
              class="form-control"
            >
              <option :value="null">Seleccione un alumno...</option>
              <option v-for="alumno in alumnos" :key="alumno.id" :value="alumno.id">
                {{ alumno.nombre }} {{ alumno.apellido }} - DNI: {{ alumno.dni }}
              </option>
            </select>
          </div>

          <div class="form-group" v-if="formData.comprador_tipo === 'otro'">
            <label for="comprador_nombre">Nombre del Comprador *</label>
            <input
              type="text"
              id="comprador_nombre"
              v-model="formData.comprador_nombre"
              required
              class="form-control"
              placeholder="Nombre completo del comprador"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="observaciones">Observaciones</label>
          <textarea
            id="observaciones"
            v-model="formData.observaciones"
            class="form-control"
            rows="3"
            placeholder="Información adicional..."
          ></textarea>
        </div>

        <div class="panel-footer">
          <button type="button" @click="$emit('close')" class="btn-secondary">Cancelar</button>
          <button type="submit" class="btn-primary" :disabled="saving">
            {{ saving ? 'Guardando...' : 'Actualizar' }}
          </button>
        </div>
      </form>
      <div v-else class="loading-container">Cargando...</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { usePelotitasStore } from '@/stores/pelotitas'
import { useSociosStore } from '@/stores/socios'
import { useAlumnosStore } from '@/stores/alumnos'
import { storeToRefs } from 'pinia'
import type { Pelotita } from '@/interfaces/Pelotita'

const props = defineProps<{
  pelotitaId: number
}>()

const emit = defineEmits(['close', 'updated'])
const pelotitasStore = usePelotitasStore()
const sociosStore = useSociosStore()
const alumnosStore = useAlumnosStore()

const { socios } = storeToRefs(sociosStore)
const { alumnos } = storeToRefs(alumnosStore)
const loading = ref(true)
const saving = ref(false)

const formData = ref<Pelotita>({
  fecha: '',
  tipo: 'compra',
  cantidad: 0,
  precio_unitario: 0,
  total: 0,
  proveedor: '',
  comprador_tipo: null,
  comprador_id: null,
  comprador_nombre: null,
  observaciones: ''
})

onMounted(async () => {
  try {
    await Promise.all([
      sociosStore.fetchSocios(),
      alumnosStore.fetchAlumnos(),
      pelotitasStore.fetchPelotita(props.pelotitaId)
    ])
    
    if (pelotitasStore.pelotita) {
      formData.value = {
        ...pelotitasStore.pelotita,
        fecha: pelotitasStore.pelotita.fecha.split('T')[0]
      }
    }
  } catch (error) {
    console.error('Error al cargar pelotita:', error)
    alert('Error al cargar los datos')
    emit('close')
  } finally {
    loading.value = false
  }
})

const calculateTotal = () => {
  formData.value.total = formData.value.cantidad * formData.value.precio_unitario
}

const handleCompradorTipoChange = () => {
  formData.value.comprador_id = null
  formData.value.comprador_nombre = null
}

watch(() => formData.value.tipo, (newTipo) => {
  if (newTipo === 'venta') {
    formData.value.proveedor = ''
  } else if (newTipo === 'compra') {
    formData.value.comprador_tipo = null
    formData.value.comprador_id = null
    formData.value.comprador_nombre = null
  }
})

const handleSubmit = async () => {
  saving.value = true
  try {
    await pelotitasStore.updatePelotita(props.pelotitaId, formData.value)
    emit('updated')
    emit('close')
  } catch (error) {
    console.error('Error al actualizar:', error)
    alert('Error al actualizar la operación')
  } finally {
    saving.value = false
  }
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
  max-width: 600px;
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

form {
  padding: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #022F9D;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #00CDFF;
}

textarea.form-control {
  resize: vertical;
}

.panel-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #00CDFF;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #00B8E6;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 205, 255, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #e0e0e0;
  color: #333;
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
