<template>
  <nav>
    <a href="/" class="logo-link">
      <img src="../public/images/logo.svg" alt="Logo" class="logo" />
    </a>
    
    <button class="menu-toggle" @click="toggleMenu" :aria-label="menuOpen ? 'Cerrar menú' : 'Abrir menú'">
      <Icon :icon="menuOpen ? 'mdi:close' : 'mdi:menu'" width="28" height="28" />
    </button>

    <div class="nav-links" :class="{ 'nav-links-open': menuOpen }">
      <RouterLink :to="{ name: 'home' }" @click="closeMenu"></RouterLink>
      <RouterLink :to="{ name: 'socios' }" @click="closeMenu">Socios</RouterLink>
      <RouterLink :to="{ name: 'alumnos' }" @click="closeMenu">Alumnos</RouterLink>
      <RouterLink :to="{ name: 'turnos' }" @click="closeMenu">Turnos</RouterLink>
      <RouterLink :to="{ name: 'profesores' }" @click="closeMenu">Profesores</RouterLink>
      <RouterLink :to="{ name: 'pagos' }" @click="closeMenu">Pagos</RouterLink>
      <RouterLink :to="{ name: 'pelotitas' }" @click="closeMenu">Pelotitas</RouterLink>
      
      <div class="social-links">
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

const menuOpen = ref(false)

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const closeMenu = () => {
  menuOpen.value = false
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

.logo-link {
  display: flex;
  align-items: center;
  z-index: 1001;
}

.logo {
  width: 15rem;
  height: auto;
  margin: 0;
}

/* Botón hamburguesa (oculto en desktop) */
.menu-toggle {
  display: none;
  background: none;
  border: none;
  color: #FFFFFF;
  cursor: pointer;
  padding: 0.5rem;
  z-index: 1001;
  transition: color 0.3s ease;
}

.menu-toggle:hover {
  color: #00CDFF;
}

/* Enlaces de navegación */
.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1;
  justify-content: flex-start;
  margin-left: 2rem;
}

.nav-links a {
  color: #FFFFFF;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
  white-space: nowrap;
}

.nav-links a:hover {
  color: #00CDFF;
}

.nav-links a.router-link-exact-active {
  color: #FFCD00;
  font-weight: 600;
}

.social-links {
  margin-left: auto;
  display: flex;
  gap: 1rem;
}

.social-links a {
  color: #FFFFFF;
  transition: color 0.3s ease;
}

.social-links a:hover {
  color: #00CDFF;
}

/* Estilos responsive para tablets y móviles */
@media (max-width: 768px) {
  nav {
    padding: 0.75rem 1rem;
    height: 3.5rem;
  }

  .logo {
    width: 10rem;
  }

  /* Mostrar botón hamburguesa */
  .menu-toggle {
    display: block;
  }

  /* Enlaces de navegación en modo móvil */
  .nav-links {
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
  .nav-links-open {
    max-height: calc(100vh - 3.5rem);
    opacity: 1;
  }

  .nav-links a {
    padding: 1rem 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    text-align: left;
  }

  .nav-links a:last-of-type {
    border-bottom: none;
  }

  .social-links {
    margin: 1rem 0 0 0;
    padding: 1rem 1.5rem 0;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    justify-content: center;
  }
}

/* Estilos para móviles pequeños */
@media (max-width: 480px) {
  .logo {
    width: 8rem;
  }

  nav {
    padding: 0.5rem 1rem;
    height: 3rem;
  }

  .nav-links {
    top: 3rem;
  }

  .menu-toggle {
    padding: 0.25rem;
  }
}

/* Mejoras para tablets en orientación landscape */
@media (min-width: 769px) and (max-width: 1024px) {
  .logo {
    width: 12rem;
  }

  .nav-links {
    gap: 1rem;
    margin-left: 1rem;
  }

  .nav-links a {
    font-size: 0.9rem;
  }
}
</style>