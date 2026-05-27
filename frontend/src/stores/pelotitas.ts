import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Pelotita, ResumenPelotitas } from '@/interfaces/Pelotita'
import ApiService from '@/services/ApiService'

export const usePelotitasStore = defineStore('pelotitas', () => {
  const pelotitas = ref<Pelotita[]>([])
  const pelotita = ref<Pelotita | null>(null)
  const resumen = ref<ResumenPelotitas[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const currentPage = ref(1)
  const totalPages = ref(1)
  const totalCount = ref(0)
  const pageSize = ref(10)

  const fetchPelotitas = async (page: number = 1) => {
    loading.value = true
    error.value = null
    try {
      currentPage.value = page
      const response = await ApiService.get(`/pelotitas/?page=${page}`)
      pelotitas.value = response.data.items || []
      totalPages.value = response.data.total_pages || 1
      totalCount.value = response.data.total_count || 0
      pageSize.value = response.data.page_size || 10
    } catch (err: any) {
      error.value = err.message || 'Error al cargar pelotitas'
      console.error('Error fetching pelotitas:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchPelotita = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get(`/pelotitas/${id}`)
      pelotita.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error al cargar pelotita'
      console.error('Error fetching pelotita:', err)
    } finally {
      loading.value = false
    }
  }

  const createPelotita = async (data: Pelotita) => {
    loading.value = true
    error.value = null
    try {
      await ApiService.post('/pelotitas/', data)
      await fetchPelotitas(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al crear pelotita'
      console.error('Error creating pelotita:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updatePelotita = async (id: number, data: Partial<Pelotita>) => {
    loading.value = true
    error.value = null
    try {
      await ApiService.put(`/pelotitas/${id}`, data)
      await fetchPelotitas(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al actualizar pelotita'
      console.error('Error updating pelotita:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deletePelotita = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      await ApiService.delete(`/pelotitas/${id}`)
      await fetchPelotitas(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al eliminar pelotita'
      console.error('Error deleting pelotita:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchResumen = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get('/pelotitas/resumen')
      resumen.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error al cargar resumen'
      console.error('Error fetching resumen:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    pelotitas,
    pelotita,
    resumen,
    loading,
    error,
    currentPage,
    totalPages,
    totalCount,
    pageSize,
    fetchPelotitas,
    fetchPelotita,
    createPelotita,
    updatePelotita,
    deletePelotita,
    fetchResumen
  }
})
