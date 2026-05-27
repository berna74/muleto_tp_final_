<template>
  <div class="inicio-contenedor">
    <h1>SiPePa - Pelota a Paleta - Club Sol de Mayo</h1>
    <p>
      Bienvenido al <b>Si</b>stema de administración de <b>Pe</b>lota a <b>Pa</b>leta del Club Sol de Mayo.<br>
      Acá podés gestionar socios, turnos, profes y categorías desde un solo lugar.
    </p>
    <div class="inicio-grilla">
      <router-link to="/socios" class="inicio-tarjeta">
        <Icon icon="mdi:account-group" width="40" height="40" />
        <strong>Socios</strong>
        <small>Gestioná socios del club</small>
      </router-link>
      <router-link to="/alumnos" class="inicio-tarjeta">
        <Icon icon="mdi:file-account-outline" width="40" height="40" />
        <strong>Alumnos</strong>
        <small>Gestioná alumnos de clases</small>
      </router-link>
      <router-link to="/turnos" class="inicio-tarjeta">
        <Icon icon="mdi:clock-outline" width="40" height="40" />
        <strong>Turnos</strong>
        <small>Reservá turnos de cancha</small>
      </router-link>
      <router-link to="/profesores" class="inicio-tarjeta">
        <Icon icon="mdi:account-child" width="40" height="40" />
        <strong>Profesores</strong>
        <small>Gestioná profes</small>
      </router-link>
      <router-link to="/categorias" class="inicio-tarjeta">
        <Icon icon="mdi:signal" width="40" height="40" />
        <strong>Categorías</strong>
        <small>Definí niveles de juego</small>
      </router-link>
      <router-link to="/pagos" class="inicio-tarjeta">
        <Icon icon="mdi:cash-multiple" width="40" height="40" />
        <strong>Pagos</strong>
        <small>Registrá pagos y abonos</small>
      </router-link>
      <router-link to="/pelotitas" class="inicio-tarjeta">
        <Icon icon="mdi:dots-triangle" width="40" height="40" />
        <strong>Pelotitas</strong>
        <small>Gestioná compra y venta</small>
      </router-link>
    </div>
    <footer class="inicio-pie">
      <img src="/images/logo-club.png" alt="Logo Club Sol de Mayo" class="pie-logo">
      <p class="pie-direccion">Club Sol de Mayo - Av. Francisco de Viedma 1057, Viedma, Río Negro.</p>
    </footer>
  </div>
</template>

<script setup>

</script>

<style scoped>
.inicio-contenedor {
  max-width: 700px;
  margin: 3rem auto;
  padding: 2rem;
  background: #FFFFFF;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(2, 47, 157, 0.15);
  text-align: center;
}
.logo {
  width: 220px;
  margin-bottom: 0.5rem;
}
.inicio-contenedor h1 {
  margin-bottom: 0.5rem;
  color: #022F9D;
  font-size: 2rem;
}
.inicio-contenedor p {
  color: #444;
  margin-bottom: 2rem;
  font-size: 1rem;
}
.inicio-contenedor p b {
  color: #022F9D;
}
.inicio-grilla {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.5rem;
}
.inicio-tarjeta {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f6f8fa;
  border-radius: 12px;
  padding: 2rem 1.5rem;
  text-decoration: none;
  color: #022F9D;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
  border: 2px solid transparent;
}
.inicio-tarjeta:hover {
  background: #e3f0fc;
  box-shadow: 0 4px 16px rgba(2,47,157,0.2);
  border-color: #00CDFF;
  transform: translateY(-2px);
}
.inicio-tarjeta .ov-icon {
  color: #00CDFF;
  margin-bottom: 1rem;
  transition: color 0.3s ease;
}
.inicio-tarjeta:hover .ov-icon {
  color: #022F9D;
}
.inicio-tarjeta strong {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: #022F9D;
}
.inicio-tarjeta small {
  color: #666;
  text-align: center;
  font-size: 0.9rem;
}
.inicio-pie {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #e0e0e0;
  text-align: center;
}
.pie-logo {
  max-width: 84px;
  height: auto;
  opacity: 0.9;
  margin-bottom: 0.5rem;
}
.pie-direccion {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

/* Responsive para tablets */
@media (max-width: 768px) {
  .inicio-contenedor {
    margin: 2rem auto;
    padding: 1.5rem;
    max-width: 90%;
  }

  .inicio-contenedor h1 {
    font-size: 1.5rem;
  }

  .inicio-contenedor p {
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
  }

  .inicio-grilla {
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 1rem;
  }

  .inicio-tarjeta {
    padding: 1.5rem 1rem;
  }

  .inicio-tarjeta strong {
    font-size: 1.1rem;
  }

  .inicio-tarjeta small {
    font-size: 0.85rem;
  }

  .inicio-pie {
    margin-top: 2rem;
    padding-top: 1.5rem;
  }
}

/* Responsive para móviles */
@media (max-width: 480px) {
  .inicio-contenedor {
    margin: 1rem auto;
    padding: 1rem;
    max-width: 95%;
    border-radius: 8px;
  }

  .inicio-contenedor h1 {
    font-size: 1.3rem;
    line-height: 1.3;
  }

  .inicio-contenedor p {
    font-size: 0.9rem;
    margin-bottom: 1.25rem;
  }

  .inicio-grilla {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }

  .inicio-tarjeta {
    padding: 1.25rem 0.75rem;
    border-radius: 10px;
  }

  .inicio-tarjeta strong {
    font-size: 1rem;
  }

  .inicio-tarjeta small {
    font-size: 0.8rem;
  }

  .inicio-pie {
    margin-top: 1.5rem;
    padding-top: 1rem;
  }

  .pie-logo {
    max-width: 70px;
  }

  .pie-direccion {
    font-size: 0.8rem;
  }
}

/* Para pantallas muy pequeñas */
@media (max-width: 360px) {
  .inicio-contenedor h1 {
    font-size: 1.1rem;
  }

  .inicio-grilla {
    gap: 0.5rem;
  }

  .inicio-tarjeta {
    padding: 1rem 0.5rem;
  }

  .inicio-tarjeta strong {
    font-size: 0.95rem;
  }

  .inicio-tarjeta small {
    font-size: 0.75rem;
  }
}
</style>