import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Profesor } from '@/interfaces/Profesor'
import ApiService from '@/services/ApiService'

export const useProfesoresStore = defineStore('profesores', () => {
  const profesores = ref<Profesor[]>([])
  const profesor = ref<Profesor | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const currentPage = ref(1)
  const totalPages = ref(1)
  const totalCount = ref(0)
  const pageSize = ref(10)

  async function cargarProfesores(page: number = 1) {
    loading.value = true
    error.value = null
    try {
      currentPage.value = page
      const response = await ApiService.obtener(`/profesores/?page=${page}`)
      profesores.value = response.data.items || []
      totalPages.value = response.data.total_pages || 1
      totalCount.value = response.data.total_count || 0
      pageSize.value = response.data.page_size || 10
    } catch (err: any) {
      error.value = err.message || 'Error al cargar los profesores'
    } finally {
      loading.value = false
    }
  }

  async function cargarProfesor(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.obtener(`/profesores/${id}`)
      profesor.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error al cargar el profesor'
    } finally {
      loading.value = false
    }
  }

  async function crearProfesor(profesorData: Omit<Profesor, 'id'>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.enviar('/profesores/', profesorData)
      await cargarProfesores(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al crear el profesor'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function actualizarProfesor(id: number, profesorData: Partial<Profesor>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.modificar(`/profesores/${id}`, profesorData)
      await cargarProfesores(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al actualizar el profesor'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function eliminarProfesor(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.eliminar(`/profesores/${id}`)
      await cargarProfesores(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al eliminar el profesor'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    profesores,
    profesor,
    loading,
    error,
    currentPage,
    totalPages,
    totalCount,
    pageSize,
    cargarProfesores,
    cargarProfesor,
    crearProfesor,
    actualizarProfesor,
    eliminarProfesor
  }
})
