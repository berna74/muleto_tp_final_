<template>
  <div class="panel-wrapper">
    <div class="panel-content">
      <h2>Editar Turno</h2>
      <div v-if="loading && !formData.cancha">Cargando...</div>
      <form v-else @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Cancha:</label>
          <select v-model="formData.cancha" required>
            <option value="">Seleccionar cancha</option>
            <option value="Cancha Central">Cancha Central</option>
            <option value="Cancha 1">Cancha 1</option>
            <option value="Cancha 2">Cancha 2</option>
            <option value="Cancha 3">Cancha 3</option>
            <option value="Cancha 4">Cancha 4</option>
            <option value="Cancha 5">Cancha 5</option>
          </select>
        </div>

        <div class="form-group">
          <label>Fecha:</label>
          <input type="date" v-model="formData.fecha" required />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Hora Inicio:</label>
            <input type="time" v-model="formData.hora_inicio" required step="1800" />
          </div>
          <div class="form-group">
            <label>Hora Fin:</label>
            <input type="time" v-model="formData.hora_fin" required step="1800" />
          </div>
        </div>

        <div class="form-group">
          <label>Socio que Reserva (ID):</label>
          <input type="number" v-model.number="formData.socio_reserva_id" min="1" />
        </div>

        <div class="form-group">
          <label>Estado:</label>
          <select v-model="formData.estado" required>
            <option value="disponible">Disponible</option>
            <option value="reservado">Reservado</option>
          </select>
        </div>

        <div class="form-group">
          <label>Jugadores (uno por línea):</label>
          <textarea v-model="jugadoresText" rows="4" placeholder="Nombre Jugador 1&#10;Nombre Jugador 2"></textarea>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-submit" :disabled="submitLoading">
            {{ submitLoading ? 'Guardando...' : 'Actualizar' }}
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
import { useTurnosStore } from '@/stores/turnos'
import { storeToRefs } from 'pinia'

const props = defineProps<{ id: number }>()
const emit = defineEmits(['close', 'updated'])

const turnosStore = useTurnosStore()
const { turno, loading } = storeToRefs(turnosStore)

const formData = ref({
  cancha: '',
  fecha: '',
  hora_inicio: '',
  hora_fin: '',
  socio_reserva_id: null as number | null,
  estado: 'disponible',
})

const jugadoresText = ref('')
const submitLoading = ref(false)
const error = ref<string | null>(null)

onMounted(async () => {
  await turnosStore.fetchTurno(props.id)
  if (turno.value) {
    formData.value = {
      cancha: turno.value.cancha,
      fecha: turno.value.fecha,
      hora_inicio: turno.value.hora_inicio,
      hora_fin: turno.value.hora_fin,
      socio_reserva_id: turno.value.socio_reserva_id,
      estado: turno.value.estado
    }
    jugadoresText.value = turno.value.jugadores.join('\n')
  }
})

async function handleSubmit() {
  submitLoading.value = true
  error.value = null
  
  try {
    const jugadores = jugadoresText.value
      .split('\n')
      .map(j => j.trim())
      .filter(j => j.length > 0)
    
    await turnosStore.updateTurno(props.id, {
      ...formData.value,
      jugadores
    })
    emit('updated')
  } catch (e: any) {
    error.value = e.response?.data?.mensaje || 'Error al actualizar turno'
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
  max-width: 500px;
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

input, select, textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #CCCCCC;
  border-radius: 4px;
  font-size: 14px;
}

textarea {
  resize: vertical;
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
}

.btn-submit:hover:not(:disabled) {
  background-color: #00CDFF;
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
