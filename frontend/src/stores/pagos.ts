import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/ApiService'
import type { Pago } from '@/interfaces/Pago'

export const usePagosStore = defineStore('pagos', () => {
  const pagos = ref<Pago[]>([])
  const pago = ref<Pago | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const currentPage = ref(1)
  const totalPages = ref(1)
  const totalCount = ref(0)
  const pageSize = ref(10)

  async function fetchPagos(page: number = 1) {
    loading.value = true
    error.value = null
    try {
      currentPage.value = page
      const response = await ApiService.get(`/pagos/?page=${page}`)
      pagos.value = response.data.items || []
      totalPages.value = response.data.total_pages || 1
      totalCount.value = response.data.total_count || 0
      pageSize.value = response.data.page_size || 10
    } catch (e: any) {
      error.value = e.message || 'Error al cargar pagos'
      console.error('Error fetching pagos:', e)
    } finally {
      loading.value = false
    }
  }

  async function fetchPago(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get(`/pagos/${id}`)
      pago.value = response.data
    } catch (e: any) {
      error.value = e.message || 'Error al cargar pago'
      console.error('Error fetching pago:', e)
    } finally {
      loading.value = false
    }
  }

  async function createPago(pagoData: Partial<Pago>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.post('/pagos/', pagoData)
      await fetchPagos(currentPage.value)
    } catch (e: any) {
      error.value = e.message || 'Error al crear pago'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updatePago(id: number, pagoData: Partial<Pago>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.put(`/pagos/${id}`, pagoData)
      await fetchPagos(currentPage.value)
    } catch (e: any) {
      error.value = e.message || 'Error al actualizar pago'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deletePago(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.delete(`/pagos/${id}`)
      await fetchPagos(currentPage.value)
    } catch (e: any) {
      error.value = e.message || 'Error al eliminar pago'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    pagos,
    pago,
    loading,
    error,
    currentPage,
    totalPages,
    totalCount,
    pageSize,
    fetchPagos,
    fetchPago,
    createPago,
    updatePago,
    deletePago
  }
})
