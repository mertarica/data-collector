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

  const selectedProvider = ref<string>('all')

  // Mock data for dataset counts - replace with real data later
  const datasetCountByProvider = ref<Record<string, number>>({
    ine: 150,
    eurostat: 0,
    worldbank: 0,
  })

  // Getters
  const enabledProviders = computed(() => providers.value.filter((p) => p.enabled))

  const totalDatasets = computed(() => {
    return Object.values(datasetCountByProvider.value).reduce((sum, count) => sum + count, 0)
  })

  const getProviderById = (id: string) => {
    return providers.value.find((p) => p.id === id)
  }

  // Actions
  const setSelectedProvider = (providerId: string) => {
    selectedProvider.value = providerId
  }

  const updateDatasetCount = (providerId: string, count: number) => {
    datasetCountByProvider.value[providerId] = count
  }

  return {
    // State
    providers,
    selectedProvider,
    datasetCountByProvider,
    // Getters
    enabledProviders,
    totalDatasets,
    // Actions
    getProviderById,
    setSelectedProvider,
    updateDatasetCount,
  }
})
