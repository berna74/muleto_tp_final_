<template>
  <div class="alumnos-view">
    <AlumnosCreate 
      v-if="showCreate" 
      @close="showCreate = false" 
      @created="handleCreated" 
    />
    <AlumnosShow 
      v-if="showView && selectedAlumnoId" 
      :alumno-id="selectedAlumnoId"
      @close="showView = false" 
    />
    <AlumnosList 
      @create="showCreate = true" 
      @edit="handleEdit"
      @show="handleShow"
    />
    <AlumnosUpdate 
      v-if="showEdit && selectedAlumnoId" 
      :alumno-id="selectedAlumnoId"
      @close="showEdit = false" 
      @updated="handleUpdated" 
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AlumnosList from '@/components/alumnos/AlumnosList.vue'
import AlumnosCreate from '@/components/alumnos/AlumnosCreate.vue'
import AlumnosUpdate from '@/components/alumnos/AlumnosUpdate.vue'
import AlumnosShow from '@/components/alumnos/AlumnosShow.vue'

const showCreate = ref(false)
const showEdit = ref(false)
const showView = ref(false)
const selectedAlumnoId = ref<number | null>(null)

function handleCreated() {
  showCreate.value = false
}

function handleEdit(id: number) {
  selectedAlumnoId.value = id
  showEdit.value = true
}

function handleShow(id: number) {
  selectedAlumnoId.value = id
  showView.value = true
}

function handleUpdated() {
  showEdit.value = false
  selectedAlumnoId.value = null
}
</script>

<style scoped>
.alumnos-view {
  padding: 20px;
}
</style>
