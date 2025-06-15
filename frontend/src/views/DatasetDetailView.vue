<template>
  <div class="space-y-6">
    <!-- Back Button -->
    <div>
      <button @click="router.back()" class="flex items-center text-gray-600 hover:text-gray-900">
        ← Back to datasets
      </button>
    </div>

    <!-- Dataset Header -->
    <div v-if="store.currentDataset" class="card">
      <div class="flex items-start justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">
            {{ store.currentDataset.codigo }}
          </h1>
          <p class="text-gray-600 mb-4">{{ store.currentDataset.nombre }}</p>
          <div class="flex items-center space-x-4 text-sm text-gray-500">
            <span
              v-if="store.currentDataset.cod_ioe"
              class="bg-blue-100 text-blue-800 px-3 py-1 rounded"
            >
              IOE: {{ store.currentDataset.cod_ioe }}
            </span>
            <a
              v-if="store.currentDataset.url"
              :href="store.currentDataset.url"
              target="_blank"
              class="text-blue-600 hover:text-blue-800"
            >
              📄 Documentation
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Data Actions -->
    <div class="card">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">Data Operations</h2>
      <div class="flex space-x-4">
        <button
          @click="loadRawData"
          :disabled="store.loading"
          class="btn-primary"
          :class="{ 'opacity-50 cursor-not-allowed': store.loading }"
        >
          <span v-if="store.loading && isLoadingRaw" class="mr-2">
            <div
              class="animate-spin rounded-full h-4 w-4 border-b-2 border-white inline-block"
            ></div>
          </span>
          📥 {{ store.loading && isLoadingRaw ? 'Loading...' : 'Fetch Raw Data' }}
        </button>
        <button
          @click="loadProcessedData"
          :disabled="store.loading"
          class="btn-primary"
          :class="{ 'opacity-50 cursor-not-allowed': store.loading }"
        >
          <span v-if="store.loading && isLoadingProcessed" class="mr-2">
            <div
              class="animate-spin rounded-full h-4 w-4 border-b-2 border-white inline-block"
            ></div>
          </span>
          ⚙️ {{ store.loading && isLoadingProcessed ? 'Loading...' : 'Fetch Processed Data' }}
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="store.loading" class="card">
      <div class="flex items-center space-x-3">
        <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
        <span>
          {{
            isLoadingRaw
              ? 'Fetching raw data...'
              : isLoadingProcessed
                ? 'Processing data...'
                : 'Loading...'
          }}
        </span>
      </div>
    </div>

    <!-- Error State -->
    <div v-if="store.error" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <div class="flex">
        <div class="text-red-600">❌</div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">Error</h3>
          <div class="mt-2 text-sm text-red-700">{{ store.error }}</div>
          <div class="mt-3 space-x-2">
            <button @click="loadRawData" class="text-sm text-red-600 hover:text-red-800 underline">
              Try Raw Data Again
            </button>
            <button
              @click="loadProcessedData"
              class="text-sm text-red-600 hover:text-red-800 underline"
            >
              Try Processed Data Again
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Raw Data Display -->
    <div v-if="store.rawData" class="card">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">Raw Data</h2>
      <div class="mb-4 flex items-center space-x-4 text-sm text-gray-600">
        <span>Records: {{ store.rawData.record_count || 'N/A' }}</span>
        <span v-if="store.rawData.message">{{ store.rawData.message }}</span>
        <button @click="store.clearData" class="text-red-600 hover:text-red-800 text-xs">
          Clear Data
        </button>
      </div>
      <div class="bg-gray-50 rounded-lg p-4 max-h-96 overflow-auto">
        <pre class="text-xs">{{ JSON.stringify(store.rawData.raw_data, null, 2) }}</pre>
      </div>
    </div>

    <!-- Processed Data Display -->
    <div v-if="store.processedData" class="card">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">Processed Data</h2>
      <div class="mb-4 flex items-center justify-between">
        <div class="flex items-center space-x-4 text-sm text-gray-600">
          <span>Records: {{ store.processedData.record_count }}</span>
          <span>Columns: {{ store.processedData.columns?.length || 0 }}</span>
        </div>
        <div class="space-x-2">
          <button @click="exportData" class="btn-secondary text-xs">💾 Export CSV</button>
          <button @click="store.clearData" class="text-red-600 hover:text-red-800 text-xs">
            Clear Data
          </button>
        </div>
      </div>

      <!-- Data Table -->
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                v-for="column in store.processedData.columns"
                :key="column"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {{ column }}
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="(row, index) in store.processedData.processed_data.slice(0, 50)"
              :key="index"
              class="hover:bg-gray-50"
            >
              <td
                v-for="column in store.processedData.columns"
                :key="column"
                class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
              >
                {{ row[column] }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div
        v-if="store.processedData.processed_data.length > 50"
        class="mt-4 text-sm text-gray-500 text-center"
      >
        Showing first 50 records of {{ store.processedData.record_count }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDatasetsStore } from '../stores/datasets'

const route = useRoute()
const router = useRouter()
const store = useDatasetsStore()

const datasetCode = route.params.code as string

// Local loading states
const isLoadingRaw = ref(false)
const isLoadingProcessed = ref(false)

const loadRawData = async () => {
  console.log('🔄 Loading raw data for:', datasetCode) // Debug log
  isLoadingRaw.value = true
  isLoadingProcessed.value = false
  try {
    await store.fetchRawData(datasetCode)
    console.log('✅ Raw data loaded successfully') // Debug log
  } catch (error) {
    console.error('❌ Failed to load raw data:', error) // Debug log
  } finally {
    isLoadingRaw.value = false
  }
}

const loadProcessedData = async () => {
  console.log('🔄 Loading processed data for:', datasetCode) // Debug log
  isLoadingProcessed.value = true
  isLoadingRaw.value = false
  try {
    await store.fetchProcessedData(datasetCode)
    console.log('✅ Processed data loaded successfully') // Debug log
  } catch (error) {
    console.error('❌ Failed to load processed data:', error) // Debug log
  } finally {
    isLoadingProcessed.value = false
  }
}

const exportData = () => {
  if (!store.processedData) return

  const csvContent = [
    store.processedData.columns.join(','),
    ...store.processedData.processed_data.map((row: any) =>
      store.processedData!.columns.map((col) => `"${row[col]}"`).join(','),
    ),
  ].join('\n')

  const blob = new Blob([csvContent], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${datasetCode}_data.csv`
  a.click()
  URL.revokeObjectURL(url)
}

// Watch store loading state
watch(
  () => store.loading,
  (newVal) => {
    console.log('🔄 Store loading state changed:', newVal) // Debug log
    if (!newVal) {
      isLoadingRaw.value = false
      isLoadingProcessed.value = false
    }
  },
)

// Watch for data changes
watch(
  () => store.rawData,
  (newVal) => {
    console.log('📊 Raw data changed:', !!newVal) // Debug log
  },
)

watch(
  () => store.processedData,
  (newVal) => {
    console.log('📊 Processed data changed:', !!newVal) // Debug log
  },
)

onMounted(async () => {
  console.log('📍 DatasetDetailView mounted for:', datasetCode) // Debug log
  await store.selectDataset(datasetCode)
  store.clearData()
})
</script>
