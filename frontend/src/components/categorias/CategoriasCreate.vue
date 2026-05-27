<template>
    <div class="container">
      <h2>Crear Categoría</h2>
      <form @submit.prevent="crear">
        <div class="form-group">
          <label for="nombre">Nombre de la categoría</label>
          <input type="text" id="nombre" v-model="nuevaCategoria.nombre" placeholder="Ingrese el nombre" />
        </div>
        
        <div class="botonera">
          <router-link :to="{ name: 'categorias_list' }">
            <button type="button">Volver</button>
          </router-link>
          <button type="submit">Guardar</button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import useCategoriaStore from '@/stores/categorias';
  import type { Categoria } from '@/interfaces/Categoria';
  
  const router = useRouter();
  const store = useCategoriaStore(); 
  
  const nuevaCategoria = ref<Categoria>({
    id: 0,
    nombre: ''
  });
  
  const crear = async () => { 
    if (!nuevaCategoria.value.nombre) {
      alert('Por favor, ingrese un nombre para la categoría.');
      return;
    }
  
    try {
      await store.createCategoria(nuevaCategoria.value); 
      router.push({ name: 'categorias_list' });
    } catch (error) {
      console.error('Error al crear la categoría:', error);
      alert('Hubo un error al crear la categoría. Por favor, inténtalo de nuevo.');
    }
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 700px;
    margin: 2rem auto;
    padding: 2rem;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  }
  
  .form-group {
    margin-bottom: 1.5rem;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #333;
  }
  
  .form-group input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }
  
  .form-group input:focus {
    outline: none;
    border-color: #1976d2;
    box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
  }
  
  .botonera {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #eee;
  }
  
  .botonera button {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .botonera button[type="button"] {
    background-color: #f5f5f5;
    color: #333;
  }
  
  .botonera button[type="button"]:hover {
    background-color: #e0e0e0;
  }
  
  .botonera button[type="submit"] {
    background-color: #1976d2;
    color: white;
  }
  
  .botonera button[type="submit"]:hover {
    background-color: #1565c0;
  }
  
  </style>