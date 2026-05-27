<template>
  <div class="panel-wrapper">
    <div class="panel-content">
      <h2>Editar Socio</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-row">
          <div class="form-group">
            <label>Nombre:*</label>
            <input type="text" v-model="formData.nombre" required />
          </div>
          <div class="form-group">
            <label>Apellido:*</label>
            <input type="text" v-model="formData.apellido" required />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>DNI:*</label>
            <input type="text" v-model="formData.dni" required disabled />
            <small>El DNI no se puede modificar</small>
          </div>
          <div class="form-group">
            <label>Teléfono:*</label>
            <input type="tel" v-model="formData.telefono" required />
          </div>
        </div>

        <div class="form-group">
          <label>Email:*</label>
          <input type="email" v-model="formData.email" required />
        </div>

        <div class="form-group">
          <label>Dirección:</label>
          <input type="text" v-model="formData.direccion" />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Fecha de Nacimiento:</label>
            <input type="date" v-model="formData.fecha_nacimiento" />
          </div>
          <div class="form-group">
            <label>Fecha de Inscripción:*</label>
            <input type="date" v-model="formData.fecha_inscripcion" required />
          </div>
        </div>

        <div class="form-group">
          <label>Profesor:</label>
          <select v-model.number="formData.profesor_id">
            <option :value="null">Sin profesor asignado</option>
            <option v-for="prof in profesores" :key="prof.id" :value="prof.id">
              {{ prof.nombre }} {{ prof.apellido }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Categorías:</label>
          <div class="checkbox-group">
            <label v-for="cat in categorias" :key="cat.id" class="checkbox-label">
              <input 
                type="checkbox" 
                :value="cat.id" 
                v-model="selectedCategorias"
              />
              {{ cat.nombre }}
            </label>
          </div>
        </div>

        <div class="form-group">
          <label>Estado de Deuda:</label>
          <div class="radio-group">
            <label class="radio-label">
              <input 
                type="radio" 
                name="registra_deuda"
                value="0"
                :checked="!formData.registra_deuda"
                @change="formData.registra_deuda = false"
              />
              No registra deuda
            </label>
            <label class="radio-label">
              <input 
                type="radio" 
                name="registra_deuda"
                value="1"
                :checked="formData.registra_deuda"
                @change="formData.registra_deuda = true"
              />
              Registra deuda
            </label>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-submit" :disabled="submitLoading">
            {{ submitLoading ? 'Actualizando...' : 'Actualizar Socio' }}
          </button>
          <button type="button" class="btn-cancel" @click="$emit('close')">Cancelar</button>
        </div>
        
        <div v-if="error" class="error">{{ error }}</div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSociosStore } from '@/stores/socios'
import { useProfesoresStore } from '@/stores/profesores'
import { useCategoriasStore } from '@/stores/categorias'
import { storeToRefs } from 'pinia'
import type { Socio } from '@/interfaces/Socio'

const props = defineProps<{
  socio: Socio
}>()

const emit = defineEmits(['close', 'updated'])
const sociosStore = useSociosStore()
const profesoresStore = useProfesoresStore()
const categoriasStore = useCategoriasStore()

const { profesores } = storeToRefs(profesoresStore)
const { categorias } = storeToRefs(categoriasStore)

const formData = ref({
  nombre: props.socio.nombre,
  apellido: props.socio.apellido,
  dni: props.socio.dni,
  email: props.socio.email,
  telefono: props.socio.telefono,
  direccion: props.socio.direccion || '',
  fecha_nacimiento: props.socio.fecha_nacimiento || '',
  fecha_inscripcion: props.socio.fecha_inscripcion,
  profesor_id: props.socio.profesor_id || null,
  registra_deuda: props.socio.registra_deuda === true
})

const selectedCategorias = ref<number[]>(
  props.socio.categorias?.map(cat => cat.id).filter((id): id is number => id !== undefined) || []
)

const submitLoading = ref(false)
const error = ref<string | null>(null)

onMounted(async () => {
  await profesoresStore.fetchProfesores()
  await categoriasStore.fetchCategorias()
})

async function handleSubmit() {
  submitLoading.value = true
  error.value = null
  
  try {
    await sociosStore.updateSocio(props.socio.id, {
      ...formData.value,
      categorias: selectedCategorias.value
    })
    emit('updated')
  } catch (e: any) {
    error.value = e.response?.data?.mensaje || 'Error al actualizar socio'
  } finally {
    submitLoading.value = false
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

.form-group {
  margin-bottom: 15px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #022F9D;
  font-weight: bold;
}

input, select {
  width: 100%;
  padding: 8px;
  border: 1px solid #CCCCCC;
  border-radius: 4px;
  font-size: 14px;
}

input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

small {
  display: block;
  color: #666;
  font-size: 12px;
  margin-top: 3px;
}

.checkbox-group {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 0.75rem;
  padding: 0.9rem;
  border: 1px solid #d8e0ef;
  border-radius: 12px;
  background: linear-gradient(180deg, #f9fbff 0%, #ffffff 100%);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.8rem 0.95rem;
  border: 1px solid #dce7f7;
  border-radius: 999px;
  background: white;
  font-weight: normal;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(2, 47, 157, 0.04);
}

.checkbox-label:hover {
  border-color: #00CDFF;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 205, 255, 0.12);
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  cursor: pointer;
  accent-color: #00CDFF;
  flex-shrink: 0;
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px;
  border: 1px solid #CCCCCC;
  border-radius: 4px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: normal;
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.radio-label:hover {
  background-color: #f5f5f5;
}

.radio-label input[type="radio"] {
  width: auto;
  cursor: pointer;
  margin: 0;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.btn-submit {
  flex: 1;
  background-color: #022F9D;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-submit:hover:not(:disabled) {
  background-color: #00CDFF;
  color: #000000;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  flex: 1;
  background-color: #CCCCCC;
  color: #000000;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-cancel:hover {
  background-color: #999999;
}

.error {
  color: #dc3545;
  margin-top: 10px;
  padding: 10px;
  background-color: #f8d7da;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .panel-content {
    width: 95%;
    padding: 20px;
  }

  .checkbox-group {
    grid-template-columns: 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
