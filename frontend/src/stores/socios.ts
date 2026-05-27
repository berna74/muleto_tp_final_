import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Socio } from '@/interfaces/Socio'
import ApiService from '@/services/ApiService'

export const useSociosStore = defineStore('socios', () => {
  const socios = ref<Socio[]>([])
  const socio = ref<Socio | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const currentPage = ref(1)
  const totalPages = ref(1)
  const totalCount = ref(0)
  const pageSize = ref(10)

  async function fetchSocios(page: number = 1) {
    loading.value = true
    error.value = null
    try {
      currentPage.value = page
      const response = await ApiService.get(`/socios/?page=${page}`)
      socios.value = response.data.items || []
      totalPages.value = response.data.total_pages || 1
      totalCount.value = response.data.total_count || 0
      pageSize.value = response.data.page_size || 10
    } catch (err: any) {
      error.value = err.message || 'Error al cargar los socios'
    } finally {
      loading.value = false
    }
  }

  async function fetchSocio(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get(`/socios/${id}`)
      socio.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error al cargar el socio'
    } finally {
      loading.value = false
    }
  }

  async function createSocio(socioData: any) {
    loading.value = true
    error.value = null
    try {
      await ApiService.post('/socios/', socioData)
      await fetchSocios(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al crear el socio'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateSocio(id: number, socioData: any) {
    loading.value = true
    error.value = null
    try {
      await ApiService.put(`/socios/${id}`, socioData)
      await fetchSocios(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al actualizar el socio'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteSocio(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.delete(`/socios/${id}`)
      await fetchSocios(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al eliminar el socio'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    socios,
    socio,
    loading,
    error,
    currentPage,
    totalPages,
    totalCount,
    pageSize,
    fetchSocios,
    fetchSocio,
    createSocio,
    updateSocio,
    deleteSocio
  }
})
