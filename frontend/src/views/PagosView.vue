<template>
  <div class="pagos-view">
    <PagosCreate 
      v-if="showCreate" 
      @close="showCreate = false" 
      @created="handleCreated" 
    />
    <PagosList 
      @create="showCreate = true" 
      @edit="handleEdit"
      @show="handleShow"
    />
    <PagosUpdate 
      v-if="showEdit && selectedPagoId" 
      :pago-id="selectedPagoId"
      @close="showEdit = false" 
      @updated="handleUpdated" 
    />
    <PagosShow 
      v-if="showView && selectedPagoId" 
      :pago-id="selectedPagoId"
      @close="showView = false" 
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import PagosList from '@/components/pagos/PagosList.vue'
import PagosCreate from '@/components/pagos/PagosCreate.vue'
import PagosUpdate from '@/components/pagos/PagosUpdate.vue'
import PagosShow from '@/components/pagos/PagosShow.vue'

const showCreate = ref(false)
const showEdit = ref(false)
const showView = ref(false)
const selectedPagoId = ref<number | null>(null)

function handleCreated() {
  showCreate.value = false
}

function handleEdit(id: number) {
  selectedPagoId.value = id
  showEdit.value = true
}

function handleShow(id: number) {
  selectedPagoId.value = id
  showView.value = true
}

function handleUpdated() {
  showEdit.value = false
  selectedPagoId.value = null
}
</script>

<style scoped>
.pagos-view {
  padding: 20px;
}
</style>
