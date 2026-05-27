import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Cancha } from '@/interfaces/Cancha'
import ApiService from '@/services/ApiService'

export const useCanchasStore = defineStore('canchas', () => {
  const canchas = ref<Cancha[]>([])
  const cancha = ref<Cancha | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchCanchas() {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get('/canchas/')
      canchas.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error al cargar las canchas'
    } finally {
      loading.value = false
    }
  }

  async function fetchCancha(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get(`/canchas/${id}`)
      cancha.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error al cargar la cancha'
    } finally {
      loading.value = false
    }
  }

  async function createCancha(canchaData: Omit<Cancha, 'id'>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.post('/canchas/', canchaData)
      await fetchCanchas()
    } catch (err: any) {
      error.value = err.message || 'Error al crear la cancha'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateCancha(id: number, canchaData: Partial<Cancha>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.put(`/canchas/${id}`, canchaData)
      await fetchCanchas()
    } catch (err: any) {
      error.value = err.message || 'Error al actualizar la cancha'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteCancha(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.delete(`/canchas/${id}`)
      await fetchCanchas()
    } catch (err: any) {
      error.value = err.message || 'Error al eliminar la cancha'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    canchas,
    cancha,
    loading,
    error,
    fetchCanchas,
    fetchCancha,
    createCancha,
    updateCancha,
    deleteCancha
  }
})
