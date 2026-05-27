<template>
  <div class="panel-wrapper">
    <div class="panel-content">
      <h2>Editar Alumno</h2>
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
            <input type="text" v-model="formData.dni" required />
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
          <label>Fecha de Inscripción:*</label>
          <input type="date" v-model="formData.fecha_inscripcion" required />
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Profesor:*</label>
            <select v-model.number="formData.profesor_id" required>
              <option :value="null" disabled>Seleccionar</option>
              <option v-for="prof in profesores" :key="prof.id" :value="prof.id">
                {{ prof.nombre }} {{ prof.apellido }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Nivel:</label>
            <select v-model="formData.nivel">
              <option value="">Seleccionar</option>
              <option value="Principiante">Principiante</option>
              <option value="Intermedio">Intermedio</option>
              <option value="Avanzado">Avanzado</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label>
            <input type="checkbox" v-model="formData.activo" />
            Activo
          </label>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn-submit" :disabled="submitLoading">
            {{ submitLoading ? 'Actualizando...' : 'Actualizar Alumno' }}
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
import { useAlumnosStore } from '@/stores/alumnos'
import { useProfesoresStore } from '@/stores/profesores'
import { storeToRefs } from 'pinia'

const props = defineProps<{
  alumnoId: number
}>()

const emit = defineEmits(['close', 'updated'])
const alumnosStore = useAlumnosStore()
const profesoresStore = useProfesoresStore()
const { profesores } = storeToRefs(profesoresStore)

const formData = ref({
  nombre: '',
  apellido: '',
  dni: '',
  email: '',
  telefono: '',
  fecha_inscripcion: '',
  profesor_id: null as number | null,
  nivel: '',
  activo: true
})

const submitLoading = ref(false)
const error = ref<string | null>(null)

onMounted(async () => {
  await profesoresStore.fetchProfesores()
  await alumnosStore.fetchAlumno(props.alumnoId)
  
  const alumno = alumnosStore.alumno
  if (alumno) {
    formData.value = {
      nombre: alumno.nombre,
      apellido: alumno.apellido,
      dni: alumno.dni,
      email: alumno.email,
      telefono: alumno.telefono,
      fecha_inscripcion: alumno.fecha_inscripcion.split('T')[0],
      profesor_id: alumno.profesor?.id || null,
      nivel: alumno.nivel || '',
      activo: alumno.activo
    }
  }
})

async function handleSubmit() {
  submitLoading.value = true
  error.value = null
  
  if (!formData.value.profesor_id) {
    error.value = 'Debe seleccionar un profesor'
    submitLoading.value = false
    return
  }
  
  try {
    await alumnosStore.updateAlumno(props.alumnoId, formData.value)
    emit('updated')
  } catch (e: any) {
    error.value = e.response?.data?.mensaje || 'Error al actualizar alumno'
    console.error('Error completo:', e)
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

input[type="text"],
input[type="email"],
input[type="tel"],
input[type="date"],
select {
  width: 100%;
  padding: 8px;
  border: 1px solid #CCCCCC;
  border-radius: 4px;
}

input[type="checkbox"] {
  margin-right: 8px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.btn-submit,
.btn-cancel {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-submit {
  background-color: #022F9D;
  color: white;
}

.btn-submit:hover:not(:disabled) {
  background-color: #00CDFF;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background-color: #CCCCCC;
  color: #000000;
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
</style>
