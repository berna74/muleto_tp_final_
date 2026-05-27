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

  const cargarPelotitas = async (page: number = 1) => {
    loading.value = true
    error.value = null
    try {
      currentPage.value = page
      const response = await ApiService.obtener(`/pelotitas/?page=${page}`)
      pelotitas.value = response.data.items || []
      totalPages.value = response.data.total_pages || 1
      totalCount.value = response.data.total_count || 0
      pageSize.value = response.data.page_size || 10
    } catch (err: any) {
      error.value = err.message || 'Error al cargar pelotitas'
      console.error('Error al cargar pelotitas:', err)
    } finally {
      loading.value = false
    }
  }

  const cargarPelotita = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.obtener(`/pelotitas/${id}`)
      pelotita.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error al cargar pelotita'
      console.error('Error al cargar pelotita:', err)
    } finally {
      loading.value = false
    }
  }

  const crearPelotita = async (data: Pelotita) => {
    loading.value = true
    error.value = null
    try {
      await ApiService.enviar('/pelotitas/', data)
      await cargarPelotitas(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al crear pelotita'
      console.error('Error al crear pelotita:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const actualizarPelotita = async (id: number, data: Partial<Pelotita>) => {
    loading.value = true
    error.value = null
    try {
      await ApiService.modificar(`/pelotitas/${id}`, data)
      await cargarPelotitas(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al actualizar pelotita'
      console.error('Error al actualizar pelotita:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const eliminarPelotita = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      await ApiService.eliminar(`/pelotitas/${id}`)
      await cargarPelotitas(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al eliminar pelotita'
      console.error('Error al eliminar pelotita:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const cargarResumen = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.obtener('/pelotitas/resumen')
      resumen.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error al cargar resumen'
      console.error('Error al cargar resumen:', err)
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
    cargarPelotitas,
    cargarPelotita,
    crearPelotita,
    actualizarPelotita,
    eliminarPelotita,
    cargarResumen
  }
})
