<template>
  <div class="home-container">
    <h1>SiPePa - Pelota a Paleta - Club Sol de Mayo</h1>
    <p>
      Bienvenido al <b>Si</b>stema de administración de <b>Pe</b>lota a <b>Pa</b>leta del Club Sol de Mayo.<br>
      Aquí podrás gestionar socios, turnos, profesores y categorías desde un solo lugar.
    </p>
    <div class="home-grid">
      <router-link to="/socios" class="home-card">
        <Icon icon="mdi:account-group" width="40" height="40" />
        <strong>Socios</strong>
        <small>Gestión de socios del club</small>
      </router-link>
      <router-link to="/alumnos" class="home-card">
        <Icon icon="mdi:file-account-outline" width="40" height="40" />
        <strong>Alumnos</strong>
        <small>Gestión de alumnos de clases</small>
      </router-link>
      <router-link to="/turnos" class="home-card">
        <Icon icon="mdi:clock-outline" width="40" height="40" />
        <strong>Turnos</strong>
        <small>Reserva de turnos de cancha</small>
      </router-link>
      <router-link to="/profesores" class="home-card">
        <Icon icon="mdi:account-child" width="40" height="40" />
        <strong>Profesores</strong>
        <small>Gestiona los profesores</small>
      </router-link>
      <router-link to="/categorias" class="home-card">
        <Icon icon="mdi:signal" width="40" height="40" />
        <strong>Categorías</strong>
        <small>Niveles de juego</small>
      </router-link>
      <router-link to="/pagos" class="home-card">
        <Icon icon="mdi:cash-multiple" width="40" height="40" />
        <strong>Pagos</strong>
        <small>Registro de pagos y abonos</small>
      </router-link>
      <router-link to="/pelotitas" class="home-card">
        <Icon icon="mdi:dots-triangle" width="40" height="40" />
        <strong>Pelotitas</strong>
        <small>Compra y venta de pelotitas</small>
      </router-link>
    </div>
    <footer class="home-footer">
      <img src="/images/logo-club.png" alt="Logo Club Sol de Mayo" class="footer-logo">
      <p class="footer-address">Club Sol de Mayo - Av. Francisco de Viedma 1057, Viedma, Río Negro.</p>
    </footer>
  </div>
</template>

<script setup>

</script>

<style scoped>
.home-container {
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
.home-container h1 {
  margin-bottom: 0.5rem;
  color: #022F9D;
  font-size: 2rem;
}
.home-container p {
  color: #444;
  margin-bottom: 2rem;
  font-size: 1rem;
}
.home-container p b {
  color: #022F9D;
}
.home-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.5rem;
}
.home-card {
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
.home-card:hover {
  background: #e3f0fc;
  box-shadow: 0 4px 16px rgba(2,47,157,0.2);
  border-color: #00CDFF;
  transform: translateY(-2px);
}
.home-card .ov-icon {
  color: #00CDFF;
  margin-bottom: 1rem;
  transition: color 0.3s ease;
}
.home-card:hover .ov-icon {
  color: #022F9D;
}
.home-card strong {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: #022F9D;
}
.home-card small {
  color: #666;
  text-align: center;
  font-size: 0.9rem;
}
.home-footer {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #e0e0e0;
  text-align: center;
}
.footer-logo {
  max-width: 84px;
  height: auto;
  opacity: 0.9;
  margin-bottom: 0.5rem;
}
.footer-address {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

/* Responsive para tablets */
@media (max-width: 768px) {
  .home-container {
    margin: 2rem auto;
    padding: 1.5rem;
    max-width: 90%;
  }

  .home-container h1 {
    font-size: 1.5rem;
  }

  .home-container p {
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
  }

  .home-grid {
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 1rem;
  }

  .home-card {
    padding: 1.5rem 1rem;
  }

  .home-card strong {
    font-size: 1.1rem;
  }

  .home-card small {
    font-size: 0.85rem;
  }

  .home-footer {
    margin-top: 2rem;
    padding-top: 1.5rem;
  }
}

/* Responsive para móviles */
@media (max-width: 480px) {
  .home-container {
    margin: 1rem auto;
    padding: 1rem;
    max-width: 95%;
    border-radius: 8px;
  }

  .home-container h1 {
    font-size: 1.3rem;
    line-height: 1.3;
  }

  .home-container p {
    font-size: 0.9rem;
    margin-bottom: 1.25rem;
  }

  .home-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }

  .home-card {
    padding: 1.25rem 0.75rem;
    border-radius: 10px;
  }

  .home-card strong {
    font-size: 1rem;
  }

  .home-card small {
    font-size: 0.8rem;
  }

  .home-footer {
    margin-top: 1.5rem;
    padding-top: 1rem;
  }

  .footer-logo {
    max-width: 70px;
  }

  .footer-address {
    font-size: 0.8rem;
  }
}

/* Para pantallas muy pequeñas */
@media (max-width: 360px) {
  .home-container h1 {
    font-size: 1.1rem;
  }

  .home-grid {
    gap: 0.5rem;
  }

  .home-card {
    padding: 1rem 0.5rem;
  }

  .home-card strong {
    font-size: 0.95rem;
  }

  .home-card small {
    font-size: 0.75rem;
  }
}
</style>