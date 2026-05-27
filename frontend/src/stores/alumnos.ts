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

  async function fetchAlumnos(page: number = 1) {
    loading.value = true
    error.value = null
    try {
      currentPage.value = page
      const response = await ApiService.get(`/alumnos/?page=${page}`)
      alumnos.value = response.data.items || []
      totalPages.value = response.data.total_pages || 1
      totalCount.value = response.data.total_count || 0
      pageSize.value = response.data.page_size || 10
    } catch (e: any) {
      error.value = e.message
      console.error('Error fetching alumnos:', e)
    } finally {
      loading.value = false
    }
  }

  async function fetchAlumno(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get(`/alumnos/${id}`)
      alumno.value = response.data
    } catch (e: any) {
      error.value = e.message
      console.error('Error fetching alumno:', e)
    } finally {
      loading.value = false
    }
  }

  async function createAlumno(alumnoData: Partial<Alumno>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.post('/alumnos/', alumnoData)
      await fetchAlumnos(currentPage.value)
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateAlumno(id: number, alumnoData: Partial<Alumno>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.put(`/alumnos/${id}`, alumnoData)
      await fetchAlumnos(currentPage.value)
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteAlumno(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.delete(`/alumnos/${id}`)
      await fetchAlumnos(currentPage.value)
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
    fetchAlumnos,
    fetchAlumno,
    createAlumno,
    updateAlumno,
    deleteAlumno
  }
})
