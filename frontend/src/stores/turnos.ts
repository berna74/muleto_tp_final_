import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Turno } from '@/interfaces/Turno'
import ApiService from '@/services/ApiService'

export const useTurnosStore = defineStore('turnos', () => {
  const turnos = ref<Turno[]>([])
  const turno = ref<Turno | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const currentPage = ref(1)
  const totalPages = ref(1)
  const totalCount = ref(0)
  const pageSize = ref(10)

  async function cargarTurnos(page: number = 1) {
    loading.value = true
    error.value = null
    try {
      currentPage.value = page
      const response = await ApiService.obtener(`/turnos/?page=${page}`)
      turnos.value = response.data.items || []
      totalPages.value = response.data.total_pages || 1
      totalCount.value = response.data.total_count || 0
      pageSize.value = response.data.page_size || 10
    } catch (e: any) {
      error.value = e.message || 'Error al cargar turnos'
      console.error('Error al cargar turnos:', e)
    } finally {
      loading.value = false
    }
  }

  async function cargarTurno(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.obtener(`/turnos/${id}`)
      turno.value = response.data
    } catch (e: any) {
      error.value = e.message || 'Error al cargar turno'
      console.error('Error al cargar turno:', e)
    } finally {
      loading.value = false
    }
  }

  async function crearTurno(turnoData: Partial<Turno>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.enviar('/turnos/', turnoData)
      await cargarTurnos(currentPage.value)
    } catch (e: any) {
      error.value = e.message || 'Error al crear turno'
      console.error('Error al crear turno:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function actualizarTurno(id: number, turnoData: Partial<Turno>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.modificar(`/turnos/${id}`, turnoData)
      await cargarTurnos(currentPage.value)
    } catch (e: any) {
      error.value = e.message || 'Error al actualizar turno'
      console.error('Error al actualizar turno:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function eliminarTurno(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.eliminar(`/turnos/${id}`)
      await cargarTurnos(currentPage.value)
    } catch (e: any) {
      error.value = e.message || 'Error al eliminar turno'
      console.error('Error al eliminar turno:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    turnos,
    turno,
    loading,
    error,
    currentPage,
    totalPages,
    totalCount,
    pageSize,
    cargarTurnos,
    cargarTurno,
    crearTurno,
    actualizarTurno,
    eliminarTurno
  }
})
