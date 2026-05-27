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

  async function cargarPagos(page: number = 1) {
    loading.value = true
    error.value = null
    try {
      currentPage.value = page
      const response = await ApiService.obtener(`/pagos/?page=${page}`)
      pagos.value = response.data.items || []
      totalPages.value = response.data.total_pages || 1
      totalCount.value = response.data.total_count || 0
      pageSize.value = response.data.page_size || 10
    } catch (e: any) {
      error.value = e.message || 'Error al cargar pagos'
      console.error('Error al cargar pagos:', e)
    } finally {
      loading.value = false
    }
  }

  async function cargarPago(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.obtener(`/pagos/${id}`)
      pago.value = response.data
    } catch (e: any) {
      error.value = e.message || 'Error al cargar pago'
      console.error('Error al cargar pago:', e)
    } finally {
      loading.value = false
    }
  }

  async function crearPago(pagoData: Partial<Pago>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.enviar('/pagos/', pagoData)
      await cargarPagos(currentPage.value)
    } catch (e: any) {
      error.value = e.message || 'Error al crear pago'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function actualizarPago(id: number, pagoData: Partial<Pago>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.modificar(`/pagos/${id}`, pagoData)
      await cargarPagos(currentPage.value)
    } catch (e: any) {
      error.value = e.message || 'Error al actualizar pago'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function eliminarPago(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.eliminar(`/pagos/${id}`)
      await cargarPagos(currentPage.value)
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
    cargarPagos,
    cargarPago,
    crearPago,
    actualizarPago,
    eliminarPago
  }
})
