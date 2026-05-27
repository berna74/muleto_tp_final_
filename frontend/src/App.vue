<template>
  <nav>
    <a href="/" class="enlace-logo">
      <img src="../public/images/logo.svg" alt="Logo" class="logo-principal" />
    </a>
    
    <button class="boton-menu" @click="alternarMenu" :aria-label="menuAbierto ? 'Cerrar menú' : 'Abrir menú'">
      <Icon :icon="menuAbierto ? 'mdi:close' : 'mdi:menu'" width="28" height="28" />
    </button>

    <div class="enlaces-nav" :class="{ 'enlaces-nav-abiertos': menuAbierto }">
      <RouterLink :to="{ name: 'home' }" @click="cerrarMenu"></RouterLink>
      <RouterLink :to="{ name: 'socios' }" @click="cerrarMenu">Socios</RouterLink>
      <RouterLink :to="{ name: 'alumnos' }" @click="cerrarMenu">Alumnos</RouterLink>
      <RouterLink :to="{ name: 'turnos' }" @click="cerrarMenu">Turnos</RouterLink>
      <RouterLink :to="{ name: 'profesores' }" @click="cerrarMenu">Profesores</RouterLink>
      <RouterLink :to="{ name: 'pagos' }" @click="cerrarMenu">Pagos</RouterLink>
      <RouterLink :to="{ name: 'pelotitas' }" @click="cerrarMenu">Pelotitas</RouterLink>
      
      <div class="enlaces-sociales">
        <a href="https://www.facebook.com/paletasoldemayo" target="_blank" rel="noopener noreferrer" title="Facebook">
          <Icon icon="mdi:facebook" width="24" height="24" />
        </a>
        <a href="https://www.instagram.com/paletasoldemayo" target="_blank" rel="noopener noreferrer" title="Instagram">
          <Icon icon="mdi:instagram" width="24" height="24" />
        </a>
      </div>
    </div>
  </nav>
  <main>
    <RouterView />
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { Icon } from '@iconify/vue'

const menuAbierto = ref(false)

const alternarMenu = () => {
  menuAbierto.value = !menuAbierto.value
}

const cerrarMenu = () => {
  menuAbierto.value = false
}
</script>

<style>
/* Navegación base */
nav {
  background: #022F9D;
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 4rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  position: relative;
}

.enlace-logo {
  display: flex;
  align-items: center;
  z-index: 1001;
}

.logo-principal {
  width: 15rem;
  height: auto;
  margin: 0;
}

/* Botón hamburguesa (oculto en desktop) */
.boton-menu {
  display: none;
  background: none;
  border: none;
  color: #FFFFFF;
  cursor: pointer;
  padding: 0.5rem;
  z-index: 1001;
  transition: color 0.3s ease;
}

.boton-menu:hover {
  color: #00CDFF;
}

/* Enlaces de navegación */
.enlaces-nav {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1;
  justify-content: flex-start;
  margin-left: 2rem;
}

.enlaces-nav a {
  color: #FFFFFF;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
  white-space: nowrap;
}

.enlaces-nav a:hover {
  color: #00CDFF;
}

.enlaces-nav a.router-link-exact-active {
  color: #FFCD00;
  font-weight: 600;
}

.enlaces-sociales {
  margin-left: auto;
  display: flex;
  gap: 1rem;
}

.enlaces-sociales a {
  color: #FFFFFF;
  transition: color 0.3s ease;
}

.enlaces-sociales a:hover {
  color: #00CDFF;
}

/* Estilos responsive para tablets y móviles */
@media (max-width: 768px) {
  nav {
    padding: 0.75rem 1rem;
    height: 3.5rem;
  }

  .logo-principal {
    width: 10rem;
  }

  /* Mostrar botón hamburguesa */
  .boton-menu {
    display: block;
  }

  /* Enlaces de navegación en modo móvil */
  .enlaces-nav {
    position: fixed;
    top: 3.5rem;
    left: 0;
    right: 0;
    background: #022F9D;
    flex-direction: column;
    align-items: stretch;
    gap: 0;
    margin: 0;
    padding: 1rem 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    max-height: 0;
    overflow: hidden;
    opacity: 0;
    transition: max-height 0.4s ease, opacity 0.3s ease;
    z-index: 1000;
  }

  /* Menú abierto */
  .enlaces-nav-abiertos {
    max-height: calc(100vh - 3.5rem);
    opacity: 1;
  }

  .enlaces-nav a {
    padding: 1rem 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    text-align: left;
  }

  .enlaces-nav a:last-of-type {
    border-bottom: none;
  }

  .enlaces-sociales {
    margin: 1rem 0 0 0;
    padding: 1rem 1.5rem 0;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    justify-content: center;
  }
}

/* Estilos para móviles pequeños */
@media (max-width: 480px) {
  .logo-principal {
    width: 8rem;
  }

  nav {
    padding: 0.5rem 1rem;
    height: 3rem;
  }

  .enlaces-nav {
    top: 3rem;
  }

  .boton-menu {
    padding: 0.25rem;
  }
}

/* Mejoras para tablets en orientación landscape */
@media (min-width: 769px) and (max-width: 1024px) {
  .logo-principal {
    width: 12rem;
  }

  .enlaces-nav {
    gap: 1rem;
    margin-left: 1rem;
  }

  .enlaces-nav a {
    font-size: 0.9rem;
  }
}
</style>