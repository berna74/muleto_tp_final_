<template>
  <div class="panel-wrapper">
    <div class="panel-content">
      <h3>Editar Profesor</h3>
      <div v-if="loading">Cargando...</div>
      <form v-else-if="profesor" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="nombre">Nombre:</label>
          <input v-model="form.nombre" type="text" id="nombre" required />
        </div>

        <div class="form-group">
          <label for="apellido">Apellido:</label>
          <input v-model="form.apellido" type="text" id="apellido" required />
        </div>

        <div class="form-group">
          <label for="dni">DNI:</label>
          <input v-model="form.dni" type="text" id="dni" required />
        </div>

        <div class="form-group">
          <label for="horarios_clases">Horarios de clases:</label>
          <input v-model="form.horarios_clases" type="text" id="horarios_clases" placeholder="Ej: Lunes y Miércoles 10-12hs" required />
        </div>

        <div class="form-group">
          <label for="telefono">Teléfono:</label>
          <input v-model="form.telefono" type="tel" id="telefono" required />
        </div>

        <div class="form-group">
          <label for="email">Email:</label>
          <input v-model="form.email" type="email" id="email" required />
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-primary">Actualizar</button>
          <button type="button" @click="$emit('close')" class="btn-secondary">Cancelar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useProfesoresStore } from '@/stores/profesores'
import { storeToRefs } from 'pinia'

const props = defineProps<{ id: number }>()
const emit = defineEmits(['close', 'updated'])

const profesoresStore = useProfesoresStore()
const { profesor, loading } = storeToRefs(profesoresStore)

const form = ref({
  nombre: '',
  apellido: '',
  dni: '',
  horarios_clases: '',
  telefono: '',
  email: ''
})

onMounted(() => {
  profesoresStore.fetchProfesor(props.id)
})

watch(profesor, (newProfesor) => {
  if (newProfesor) {
    form.value = {
      nombre: newProfesor.nombre,
      apellido: newProfesor.apellido,
      dni: newProfesor.dni,
      horarios_clases: newProfesor.horarios_clases,
      telefono: newProfesor.telefono,
      email: newProfesor.email
    }
  }
})

async function handleSubmit() {
  try {
    await profesoresStore.updateProfesor(props.id, form.value)
    emit('updated')
  } catch (error) {
    console.error('Error al actualizar profesor:', error)
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
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  width: 100%;
  min-width: 0;
  max-width: 600px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 6px 18px rgba(2, 47, 157, 0.08);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.btn-primary,
.btn-secondary {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary {
  background-color: #022F9D;
  color: #FFFFFF;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #00CDFF;
  color: #000000;
}

.btn-secondary {
  background-color: #CCCCCC;
  color: #000000;
  transition: background-color 0.3s ease;
}

.btn-secondary:hover {
  background-color: #999999;
}
</style>
