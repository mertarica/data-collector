<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div>
      <h1 class="text-3xl font-bold text-gray-900">Data Viewer</h1>
      <p class="mt-2 text-sm text-gray-600">Interactive data exploration and visualization</p>
    </div>

    <!-- Dataset Selector -->
    <div class="card">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">Select Dataset</h2>
      <div class="flex space-x-4">
        <div class="flex-1">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search datasets..."
            class="input-field"
            @input="handleSearch"
          />
        </div>
        <select
          v-model="selectedDatasetCode"
          class="input-field w-auto min-w-[200px]"
          @change="handleDatasetSelect"
        >
          <option value="">Choose a dataset...</option>
          <option v-for="dataset in datasets" :key="dataset.codigo" :value="dataset.codigo">
            {{ dataset.codigo }} - {{ dataset.nombre.slice(0, 50) }}...
          </option>
        </select>
      </div>
    </div>

    <!-- Data Loading -->
    <div v-if="selectedDatasetCode && !processedData && !error" class="card">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="font-semibold text-gray-900">{{ selectedDatasetCode }}</h3>
          <p class="text-sm text-gray-600 mt-1">Ready to load data</p>
        </div>
        <div class="space-x-2">
          <button @click="loadData" :disabled="loading" class="btn-primary">
            {{ loading ? 'Loading...' : '📊 Load Data' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Error Display -->
    <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <div class="flex">
        <div class="text-red-600">❌</div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">Error Loading Data</h3>
          <div class="mt-2 text-sm text-red-700">{{ error }}</div>
          <button @click="loadData" class="mt-2 text-sm text-red-600 hover:text-red-800">
            Try Again
          </button>
        </div>
      </div>
    </div>

    <!-- Data Display -->
    <div v-if="processedData" class="space-y-6">
      <!-- Data Summary -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-gray-900">
            {{ processedData.dataset_name }}
          </h2>
          <div class="flex items-center space-x-4 text-sm text-gray-600">
            <span>{{ processedData.record_count }} records</span>
            <span>{{ processedData.columns.length }} columns</span>
            <button @click="exportData" class="btn-secondary text-xs">💾 Export CSV</button>
          </div>
        </div>

        <!-- Column Info -->
        <div class="mb-4">
          <h3 class="text-sm font-medium text-gray-700 mb-2">Columns:</h3>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="column in processedData.columns"
              :key="column"
              class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded"
            >
              {{ column }}
            </span>
          </div>
        </div>

        <!-- Filters -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"> Search in data: </label>
            <input
              v-model="dataFilter"
              type="text"
              placeholder="Filter rows..."
              class="input-field text-sm"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"> Records per page: </label>
            <select v-model="pageSize" class="input-field text-sm">
              <option :value="25">25</option>
              <option :value="50">50</option>
              <option :value="100">100</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"> Page: </label>
            <div class="flex items-center space-x-2">
              <button
                @click="currentPage--"
                :disabled="currentPage <= 1"
                class="btn-secondary text-sm px-2 py-1"
              >
                ←
              </button>
              <span class="text-sm">{{ currentPage }} / {{ totalPages }}</span>
              <button
                @click="currentPage++"
                :disabled="currentPage >= totalPages"
                class="btn-secondary text-sm px-2 py-1"
              >
                →
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Data Table -->
      <div class="card">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  v-for="column in processedData.columns"
                  :key="column"
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                  @click="sortBy(column)"
                >
                  <div class="flex items-center space-x-1">
                    <span>{{ column }}</span>
                    <span v-if="sortColumn === column" class="text-blue-600">
                      {{ sortDirection === 'asc' ? '↑' : '↓' }}
                    </span>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(row, index) in paginatedData" :key="index" class="hover:bg-gray-50">
                <td
                  v-for="column in processedData.columns"
                  :key="column"
                  class="px-4 py-3 text-sm text-gray-900"
                >
                  <div class="max-w-xs truncate" :title="String(row[column])">
                    {{ row[column] }}
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="paginatedData.length === 0" class="text-center py-8 text-gray-500">
          No data matches your filters
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useDatasetsStore } from '../stores/datasets'

const store = useDatasetsStore()

// State
const searchQuery = ref('')
const selectedDatasetCode = ref('')
const dataFilter = ref('')
const pageSize = ref(25)
const currentPage = ref(1)
const sortColumn = ref('')
const sortDirection = ref<'asc' | 'desc'>('asc')
const searchTimeout = ref<number | null>(null)

// Store state
const { datasets, processedData, loading, error } = store

// Computed
const filteredData = computed(() => {
  if (!processedData.value || !dataFilter.value) {
    return processedData.value?.processed_data || []
  }

  const filter = dataFilter.value.toLowerCase()
  return processedData.value.processed_data.filter((row: any) =>
    Object.values(row).some((value: any) => String(value).toLowerCase().includes(filter)),
  )
})

const sortedData = computed(() => {
  if (!sortColumn.value) return filteredData.value

  return [...filteredData.value].sort((a: any, b: any) => {
    const aVal = a[sortColumn.value]
    const bVal = b[sortColumn.value]

    if (aVal === bVal) return 0

    const result = aVal < bVal ? -1 : 1
    return sortDirection.value === 'asc' ? result : -result
  })
})

const totalPages = computed(() => Math.ceil(sortedData.value.length / pageSize.value))

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return sortedData.value.slice(start, end)
})

// Methods
const handleSearch = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }

  searchTimeout.value = setTimeout(() => {
    if (searchQuery.value.trim()) {
      store.searchDatasets(searchQuery.value.trim(), 100)
    } else {
      store.fetchDatasets(100)
    }
  }, 300)
}

const handleDatasetSelect = () => {
  if (selectedDatasetCode.value) {
    store.clearData()
    currentPage.value = 1
  }
}

const loadData = () => {
  if (selectedDatasetCode.value) {
    store.fetchProcessedData(selectedDatasetCode.value)
  }
}

const sortBy = (column: string) => {
  if (sortColumn.value === column) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortColumn.value = column
    sortDirection.value = 'asc'
  }
  currentPage.value = 1
}

const exportData = () => {
  if (!processedData.value) return

  const csvContent = [
    processedData.value.columns.join(','),
    ...processedData.value.processed_data.map((row: any) =>
      processedData.value!.columns.map((col) => `"${row[col]}"`).join(','),
    ),
  ].join('\n')

  const blob = new Blob([csvContent], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${selectedDatasetCode.value}_data.csv`
  a.click()
  URL.revokeObjectURL(url)
}

// Watchers
watch(pageSize, () => {
  currentPage.value = 1
})

watch(dataFilter, () => {
  currentPage.value = 1
})

// Lifecycle
onMounted(() => {
  store.fetchDatasets(100)
})
</script>
