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

  async function cargarCategorias(page: number = 1) {
    loading.value = true
    error.value = null
    try {
      currentPage.value = page
      const response = await ApiService.obtener(`/categorias/?page=${page}`)
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

  async function cargarCategoria(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.obtener(`/categorias/${id}`)
      categoria.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error al cargar la categoría'
    } finally {
      loading.value = false
    }
  }

  async function crearCategoria(categoriaData: any) {
    loading.value = true
    error.value = null
    try {
      await ApiService.enviar('/categorias/', categoriaData)
      await cargarCategorias(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al crear la categoría'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function actualizarCategoria(id: number, categoriaData: any) {
    loading.value = true
    error.value = null
    try {
      await ApiService.modificar(`/categorias/${id}`, categoriaData)
      await cargarCategorias(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al actualizar la categoría'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function eliminarCategoria(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.eliminar(`/categorias/${id}`)
      await cargarCategorias(currentPage.value)
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
    cargarCategorias,
    cargarCategoria,
    crearCategoria,
    actualizarCategoria,
    eliminarCategoria
  }
})
export default useCategoriaStore;
export { useCategoriaStore as useCategoriasStore };