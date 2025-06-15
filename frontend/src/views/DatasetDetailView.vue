<template>
    <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Enhanced Header -->
        <div class="mb-8">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
            <BackButton text="Back to Datasets" />
            
            <div v-if="currentDataset" class="flex items-center space-x-4">
              <button 
                @click="exportJson" 
                class="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-sm hover:shadow-md transition-all duration-200" 
                :disabled="!store.rawData"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                Export JSON
              </button>
            </div>
          </div>
  
          <!-- Dataset Info Card -->
          <div v-if="currentDataset" class="bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-gray-200/50">
            <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
              <div class="flex-1">
                <div class="flex items-center space-x-3 mb-3">
                  <span class="inline-flex items-center px-3 py-1.5 bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-800 text-sm font-mono font-medium rounded-lg">
                    {{ currentDataset.codigo }}
                  </span>
                  <span v-if="currentDataset.cod_ioe" class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-md">
                    ID: {{ currentDataset.cod_ioe }}
                  </span>
                </div>
                <h1 class="text-2xl lg:text-3xl font-bold text-gray-900 leading-relaxed">
                  {{ currentDataset.nombre }}
                </h1>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Loading State -->
        <LoadingState
          v-if="store.loading"
          title="Loading dataset..."
          subtitle="Fetching data from INE API"
        />
  
        <!-- Error State -->
        <ErrorState
          v-else-if="store.error"
          title="Failed to load data"
          :message="store.error"
          @retry="loadData"
        />
  
        <!-- Data Display -->
        <div v-else-if="store.rawData" class="space-y-6">
          <!-- Data Summary Card -->
          <div class="bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-gray-200/50">
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div class="flex items-center space-x-4">
                <div class="inline-flex items-center justify-center w-12 h-12 bg-green-100 rounded-xl">
                  <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-gray-900">Data Successfully Loaded</h3>
                  <p class="text-gray-600">
                    <span class="font-medium text-blue-600">{{ store.rawData.record_count.toLocaleString() }}</span> 
                    records retrieved from INE API
                  </p>
                </div>
              </div>
            </div>
          </div>
  
          <!-- JSON Data Display -->
          <JsonViewer
            :data="store.rawData.raw_data"
            title="Raw JSON Data"
            :filename="`${datasetCode}_data.json`"
          />
        </div>
  
        <!-- Empty State -->
        <EmptyState
          v-else
          title="No data available"
          description="This dataset might not have any data available or there could be an issue with the data source."
          :show-primary-action="true"
          primary-action-text="Retry Loading"
          @primary-action="loadData"
        />
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import { useDatasetsStore } from '../stores/datasets'
  
  // Components
  import BackButton from '../components/BackButton.vue'
  import LoadingState from '../components/LoadingState.vue'
  import ErrorState from '../components/ErrorState.vue'
  import EmptyState from '../components/EmptyState.vue'
  import JsonViewer from '../components/JsonViewer.vue'
  
  const route = useRoute()
  const store = useDatasetsStore()
  
  const datasetCode = route.params.code as string
  
  const currentDataset = computed(() => 
    store.datasets.find(d => d.codigo === datasetCode)
  )
  
  const loadData = async () => {
    if (datasetCode) {
      await store.fetchRawData(datasetCode)
    }
  }
  
  const exportJson = () => {
    if (!store.rawData) return
    
    const dataStr = JSON.stringify(store.rawData.raw_data, null, 2)
    const blob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${datasetCode}_data.json`
    a.click()
    URL.revokeObjectURL(url)
  }
  
  onMounted(async () => {
    // Load datasets if not loaded
    if (store.datasets.length === 0) {
      await store.fetchDatasets()
    }
    // Load data for this dataset
    await loadData()
  })
  </script>