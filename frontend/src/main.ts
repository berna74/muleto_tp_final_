import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import './assets/main.css'
import App from './App.vue'
import router from './router'

// Iconify
import { Icon } from '@iconify/vue'
import './plugins/customIcons'

// oh-vue-icons (mantener por compatibilidad)
import { OhVueIcon, addIcons } from "oh-vue-icons";
import { 
  FaDesktop, 
  FaTags, 
  FaTruck, 
  FaFolderOpen,
  FaUsers,
  FaUserGraduate,
  FaClock,
  FaUserCheck,
  FaLayerGroup,
  FaCreditCard
} from 'oh-vue-icons/icons'

addIcons(
  FaDesktop, 
  FaTags, 
  FaTruck, 
  FaFolderOpen,
  FaUsers,
  FaUserGraduate,
  FaClock,
  FaUserCheck,
  FaLayerGroup,
  FaCreditCard
);


const app = createApp(App)

app.use(createPinia())
app.use(router)

app.component("v-icon", OhVueIcon)
app.component("Icon", Icon)

app.mount('#app')
