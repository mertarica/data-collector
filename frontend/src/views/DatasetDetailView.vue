<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
          <BackButton text="Back to Datasets" />

          <button
            v-if="currentDataset && currentData"
            @click="exportJson"
            class="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-sm hover:shadow-md transition-all duration-200"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            Export JSON
          </button>
        </div>

        <!-- Dataset Info -->
        <div
          class="bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-gray-200/50"
        >
          <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div class="flex-1">
              <div class="flex items-center space-x-3 mb-3">
                <span
                  class="inline-flex items-center px-3 py-1.5 bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-800 text-sm font-mono font-medium rounded-lg"
                >
                  {{ currentDataset?.codigo || datasetCode }}
                </span>
                <span
                  v-if="currentDataset?.cod_ioe"
                  class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-md"
                >
                  ID: {{ currentDataset.cod_ioe }}
                </span>
              </div>
              <h1 class="text-2xl lg:text-3xl font-bold text-gray-900 leading-relaxed">
                {{ currentDataset?.nombre || 'Dataset Details' }}
              </h1>
            </div>

            <!-- Data Type Toggle -->
            <div class="flex items-center space-x-3">
              <span class="text-sm font-medium text-gray-700">Data Type:</span>
              <div class="relative inline-flex bg-gray-100 rounded-lg p-1">
                <button @click="setDataType('raw')" :class="dataTypeButtonClass('raw')">Raw</button>
                <button @click="setDataType('processed')" :class="dataTypeButtonClass('processed')">
                  Processed
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <LoadingState
        v-if="store.loading"
        title="Loading dataset..."
        :subtitle="`Fetching ${dataType} data from INE API`"
      />

      <!-- Error State -->
      <ErrorState
        v-else-if="store.error"
        title="Failed to load data"
        :message="store.error"
        @retry="loadCurrentData"
        @go-home="goToHome"
      />

      <!-- Data Display -->
      <div v-else-if="currentData" class="space-y-6">
        <!-- Data Summary -->
        <div
          class="bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-gray-200/50"
        >
          <div class="flex items-center space-x-4">
            <div class="inline-flex items-center justify-center w-12 h-12 bg-green-100 rounded-xl">
              <svg
                class="w-6 h-6 text-green-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"
                />
              </svg>
            </div>
          </div>
        </div>

        <!-- Data Chart -->
        <DataChart :data="currentData" :data-type="dataType" />

        <!-- JSON Data Display -->
        <JsonViewer
          :data="currentData"
          :title="`${dataType === 'raw' ? 'Raw' : 'Processed'} JSON Data`"
          :filename="`${datasetCode}_${dataType}_data.json`"
        />
      </div>

      <!-- Empty State -->
      <EmptyState
        v-else
        title="No data available"
        description="This dataset might not have any data available or there could be an issue with the data source."
        :show-primary-action="true"
        primary-action-text="Retry Loading"
        :show-secondary-action="true"
        secondary-action-text="Browse Datasets"
        @primary-action="loadCurrentData"
        @secondary-action="goToHome"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDatasetsStore } from '../stores/datasets'

// Components
import BackButton from '../components/BackButton.vue'
import LoadingState from '../components/LoadingState.vue'
import ErrorState from '../components/ErrorState.vue'
import EmptyState from '../components/EmptyState.vue'
import JsonViewer from '../components/JsonViewer.vue'
import DataChart from '../components/DataChart.vue'

const route = useRoute()
const router = useRouter()
const store = useDatasetsStore()

const datasetCode = route.params.code as string
const dataType = ref<'raw' | 'processed'>('raw')

// Computed properties
const currentDataset = computed(() => store.datasets.find((d) => d.codigo === datasetCode))

const currentData = computed(() => (dataType.value === 'raw' ? store.rawData : store.processedData))

// Methods
const dataTypeButtonClass = (type: 'raw' | 'processed') => {
  const baseClass = 'relative px-4 py-2 text-sm font-medium rounded-md transition-all duration-200'
  const activeClass = 'bg-white text-blue-600 shadow-sm'
  const inactiveClass = 'text-gray-600 hover:text-gray-900'

  return `${baseClass} ${dataType.value === type ? activeClass : inactiveClass}`
}

const setDataType = async (type: 'raw' | 'processed') => {
  if (dataType.value === type) return

  dataType.value = type
  await loadCurrentData()
}

const loadCurrentData = async () => {
  if (!datasetCode) return

  if (dataType.value === 'raw') {
    await store.fetchRawData(datasetCode)
  } else {
    await store.fetchProcessedData(datasetCode)
  }
}

const goToHome = () => {
  router.push('/')
}

const exportJson = () => {
  if (!currentData.value) return

  const dataStr = JSON.stringify(currentData.value, null, 2)
  const blob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${datasetCode}_${dataType.value}_data.json`
  a.click()
  URL.revokeObjectURL(url)
}

// Lifecycle
onMounted(async () => {
  store.clearData()

  if (store.datasets.length === 0) {
    await store.fetchDatasets()
  }

  await loadCurrentData()
})
</script>
