import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { DataProvider } from '../types/providers'

export const useProvidersStore = defineStore('providers', () => {
  // State
  const providers = ref<DataProvider[]>([
    {
      id: 'ine',
      name: 'INE',
      description: 'Spanish National Statistics Institute',
      color: 'blue',
      website: 'https://www.ine.es',
      enabled: true,
    },
    {
      id: 'eurostat',
      name: 'Eurostat',
      description: 'European Statistical Office',
      color: 'indigo',
      website: 'https://ec.europa.eu/eurostat',
      enabled: false, // Coming soon
    },
    {
      id: 'worldbank',
      name: 'World Bank',
      description: 'World Bank Open Data',
      color: 'green',
      website: 'https://data.worldbank.org',
      enabled: false, // Coming soon
    },
  ])

  // Getters
  const enabledProviders = computed(() => providers.value.filter((p) => p.enabled))

  const getProviderById = (id: string) => {
    return providers.value.find((p) => p.id === id)
  }

  return {
    // State
    providers,
    // Getters
    enabledProviders,
    // Actions
    getProviderById,
  }
})