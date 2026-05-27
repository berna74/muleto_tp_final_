import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Cancha } from '@/interfaces/Cancha'
import ApiService from '@/services/ApiService'

export const useCanchasStore = defineStore('canchas', () => {
  const canchas = ref<Cancha[]>([])
  const cancha = ref<Cancha | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function cargarCanchas() {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.obtener('/canchas/')
      canchas.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error al cargar las canchas'
    } finally {
      loading.value = false
    }
  }

  async function cargarCancha(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.obtener(`/canchas/${id}`)
      cancha.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error al cargar la cancha'
    } finally {
      loading.value = false
    }
  }

  async function crearCancha(canchaData: Omit<Cancha, 'id'>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.enviar('/canchas/', canchaData)
      await cargarCanchas()
    } catch (err: any) {
      error.value = err.message || 'Error al crear la cancha'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function actualizarCancha(id: number, canchaData: Partial<Cancha>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.modificar(`/canchas/${id}`, canchaData)
      await cargarCanchas()
    } catch (err: any) {
      error.value = err.message || 'Error al actualizar la cancha'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function eliminarCancha(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.eliminar(`/canchas/${id}`)
      await cargarCanchas()
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
    cargarCanchas,
    cargarCancha,
    crearCancha,
    actualizarCancha,
    eliminarCancha
  }
})
