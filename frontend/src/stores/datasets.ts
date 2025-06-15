import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  apiService,
  type Dataset,
  type RawDataResponse,
  type ProcessedDataResponse,
} from '../services/api'

export const useDatasetsStore = defineStore('datasets', () => {
  // State
  const datasets = ref<Dataset[]>([])
  const currentDataset = ref<Dataset | null>(null)
  const rawData = ref<RawDataResponse | null>(null)
  const processedData = ref<ProcessedDataResponse | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const datasetsCount = computed(() => datasets.value.length)
  const hasData = computed(() => rawData.value !== null || processedData.value !== null)

  // Actions
  async function fetchDatasets() {
    loading.value = true
    error.value = null
    try {
      console.log('Fetching datasets...') // Debug log
      const data = await apiService.getDatasets()
      console.log('Fetched datasets:', data.length) // Debug log
      datasets.value = data
    } catch (err) {
      console.error('Error fetching datasets:', err) // Debug log
      error.value = err instanceof Error ? err.message : 'Unknown error'
    } finally {
      loading.value = false
    }
  }

  async function searchDatasets(query: string, limit: number = 20) {
    loading.value = true
    error.value = null
    try {
      console.log('Searching datasets:', query) // Debug log
      const data = await apiService.searchDatasets(query, limit)
      datasets.value = data
    } catch (err) {
      console.error('Error searching datasets:', err) // Debug log
      error.value = err instanceof Error ? err.message : 'Unknown error'
    } finally {
      loading.value = false
    }
  }

  async function selectDataset(code: string) {
    loading.value = true
    error.value = null
    try {
      console.log('Selecting dataset:', code) // Debug log
      currentDataset.value = await apiService.getDatasetInfo(code)
    } catch (err) {
      console.error('Error selecting dataset:', err) // Debug log
      error.value = err instanceof Error ? err.message : 'Unknown error'
    } finally {
      loading.value = false
    }
  }

  async function fetchRawData(code: string) {
    loading.value = true
    error.value = null
    processedData.value = null

    try {
      console.log('Fetching raw data for:', code) // Debug log
      const data = await apiService.getRawData(code)
      console.log('Raw data received:', data) // Debug log
      rawData.value = data
    } catch (err) {
      console.error('Error fetching raw data:', err) // Debug log
      error.value = err instanceof Error ? err.message : 'Unknown error'
      rawData.value = null
    } finally {
      loading.value = false
    }
  }

  async function fetchProcessedData(code: string) {
    loading.value = true
    error.value = null
    rawData.value = null

    try {
      console.log('Fetching processed data for:', code) // Debug log
      const data = await apiService.getProcessedData(code)
      console.log('Processed data received:', data) // Debug log
      processedData.value = data
    } catch (err) {
      console.error('Error fetching processed data:', err) // Debug log
      error.value = err instanceof Error ? err.message : 'Unknown error'
      processedData.value = null
    } finally {
      loading.value = false
    }
  }

  function clearData() {
    rawData.value = null
    processedData.value = null
    currentDataset.value = null
    error.value = null
  }

  return {
    // State - reactive refs'leri return et
    datasets: datasets,
    currentDataset: currentDataset,
    rawData: rawData,
    processedData: processedData,
    loading: loading,
    error: error,
    // Getters
    datasetsCount,
    hasData,
    // Actions
    fetchDatasets,
    searchDatasets,
    selectDataset,
    fetchRawData,
    fetchProcessedData,
    clearData,
  }
})
