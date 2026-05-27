import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useContadorStore = defineStore('contador', () => {
  const conteo = ref(0)
  const conteoDoble = computed(() => conteo.value * 2)
  function sumarUno() {
    conteo.value++
  }

  return { conteo, conteoDoble, sumarUno }
})

export const useCounterStore = useContadorStore
