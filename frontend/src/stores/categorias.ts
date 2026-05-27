import type {Categoria} from '@/interfaces/Categoria';
import { defineStore } from 'pinia';
import { ref } from 'vue';
import ApiService from '../services/ApiService';

export const useCategoriaStore = defineStore('categorias', () => {
  const categorias = ref<Categoria[]>([])
  const categoria = ref<Categoria | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const currentPage = ref(1)
  const totalPages = ref(1)
  const totalCount = ref(0)
  const pageSize = ref(10)

  async function fetchCategorias(page: number = 1) {
    loading.value = true
    error.value = null
    try {
      currentPage.value = page
      const response = await ApiService.get(`/categorias/?page=${page}`)
      categorias.value = response.data.items || []
      totalPages.value = response.data.total_pages || 1
      totalCount.value = response.data.total_count || 0
      pageSize.value = response.data.page_size || 10
    } catch (err: any) {
      error.value = err.message || 'Error al cargar las categorías'
    } finally {
      loading.value = false
    }
  }

  async function fetchCategoria(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get(`/categorias/${id}`)
      categoria.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error al cargar la categoría'
    } finally {
      loading.value = false
    }
  }

  async function createCategoria(categoriaData: any) {
    loading.value = true
    error.value = null
    try {
      await ApiService.post('/categorias/', categoriaData)
      await fetchCategorias(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al crear la categoría'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateCategoria(id: number, categoriaData: any) {
    loading.value = true
    error.value = null
    try {
      await ApiService.put(`/categorias/${id}`, categoriaData)
      await fetchCategorias(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al actualizar la categoría'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteCategoria(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.delete(`/categorias/${id}`)
      await fetchCategorias(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al eliminar la categoría'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    categorias,
    categoria,
    loading,
    error,
    currentPage,
    totalPages,
    totalCount,
    pageSize,
    fetchCategorias,
    fetchCategoria,
    createCategoria,
    updateCategoria,
    deleteCategoria
  }
})
export default useCategoriaStore;
export { useCategoriaStore as useCategoriasStore };