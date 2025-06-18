import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService } from '../services/api'
import type { Dataset, RawDataResponse, ProcessedDataResponse } from '../services/api'

export const useDatasetsStore = defineStore('datasets', () => {
  // State
  const datasets = ref<Dataset[]>([])
  const rawData = ref<RawDataResponse | null>(null)
  const processedData = ref<ProcessedDataResponse | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const datasetsCount = computed(() => datasets.value.length)

  // Actions
  async function fetchDatasets() {
    loading.value = true
    error.value = null
    try {
      const data = await apiService.getDatasets()
      datasets.value = data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error'
    } finally {
      loading.value = false
    }
  }

  async function fetchRawData(codigo: string) {
    loading.value = true
    error.value = null
    rawData.value = null

    try {
      const data = await apiService.getRawData(codigo)
      rawData.value = data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error'
    } finally {
      loading.value = false
    }
  }

  async function fetchProcessedData(codigo: string) {
    loading.value = true
    error.value = null
    processedData.value = null

    try {
      const data = await apiService.getProcessedData(codigo)
      processedData.value = data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error'
    } finally {
      loading.value = false
    }
  }

  function clearData() {
    rawData.value = null
    processedData.value = null
    error.value = null
  }

  return {
    // State
    datasets,
    rawData,
    processedData,
    loading,
    error,
    // Getters
    datasetsCount,
    // Actions
    fetchDatasets,
    fetchRawData,
    fetchProcessedData,
    clearData,
  }
})
