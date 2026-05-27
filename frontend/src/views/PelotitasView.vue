<template>
  <div class="pelotitas-view">
    <PelotitasCreate
      v-if="showCreatePanel"
      @close="showCreatePanel = false"
      @saved="handleSaved"
    />
    <PelotitasShow
      v-if="showViewPanel && selectedId"
      :pelotita-id="selectedId"
      @close="showViewPanel = false"
    />
    <PelotitasList
      @showCreate="showCreatePanel = true"
      @showEdit="handleEdit"
      @showView="handleView"
    />
    <PelotitasUpdate
      v-if="showEditPanel && selectedId"
      :pelotita-id="selectedId"
      @close="showEditPanel = false"
      @updated="handleUpdated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import PelotitasList from '@/components/pelotitas/PelotitasList.vue'
import PelotitasCreate from '@/components/pelotitas/PelotitasCreate.vue'
import PelotitasUpdate from '@/components/pelotitas/PelotitasUpdate.vue'
import PelotitasShow from '@/components/pelotitas/PelotitasShow.vue'
import { usePelotitasStore } from '@/stores/pelotitas'

const pelotitasStore = usePelotitasStore()
const showCreatePanel = ref(false)
const showEditPanel = ref(false)
const showViewPanel = ref(false)
const selectedId = ref<number | null>(null)

const handleEdit = (id: number) => {
  selectedId.value = id
  showEditPanel.value = true
}

const handleView = (id: number) => {
  selectedId.value = id
  showViewPanel.value = true
}

const handleSaved = async () => {
  await pelotitasStore.fetchPelotitas()
  await pelotitasStore.fetchResumen()
}

const handleUpdated = async () => {
  await pelotitasStore.fetchPelotitas()
  await pelotitasStore.fetchResumen()
}
</script>

<style scoped>
.pelotitas-view {
  background: #f5f7fa;
}
</style>
