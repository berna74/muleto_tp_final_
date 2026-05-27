import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/ApiService'
import type { Alumno } from '@/interfaces/Alumno'

export const useAlumnosStore = defineStore('alumnos', () => {
  const alumnos = ref<Alumno[]>([])
  const alumno = ref<Alumno | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const currentPage = ref(1)
  const totalPages = ref(1)
  const totalCount = ref(0)
  const pageSize = ref(10)

  async function cargarAlumnos(page: number = 1) {
    loading.value = true
    error.value = null
    try {
      currentPage.value = page
      const response = await ApiService.obtener(`/alumnos/?page=${page}`)
      alumnos.value = response.data.items || []
      totalPages.value = response.data.total_pages || 1
      totalCount.value = response.data.total_count || 0
      pageSize.value = response.data.page_size || 10
    } catch (e: any) {
      error.value = e.message
      console.error('Error al cargar alumnos:', e)
    } finally {
      loading.value = false
    }
  }

  async function cargarAlumno(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.obtener(`/alumnos/${id}`)
      alumno.value = response.data
    } catch (e: any) {
      error.value = e.message
      console.error('Error al cargar alumno:', e)
    } finally {
      loading.value = false
    }
  }

  async function crearAlumno(alumnoData: Partial<Alumno>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.enviar('/alumnos/', alumnoData)
      await cargarAlumnos(currentPage.value)
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function actualizarAlumno(id: number, alumnoData: Partial<Alumno>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.modificar(`/alumnos/${id}`, alumnoData)
      await cargarAlumnos(currentPage.value)
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function eliminarAlumno(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.eliminar(`/alumnos/${id}`)
      await cargarAlumnos(currentPage.value)
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    alumnos,
    alumno,
    loading,
    error,
    currentPage,
    totalPages,
    totalCount,
    pageSize,
    cargarAlumnos,
    cargarAlumno,
    crearAlumno,
    actualizarAlumno,
    eliminarAlumno
  }
})
